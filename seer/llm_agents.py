import os
import tiktoken
import openai
from langchain_openai import AzureChatOpenAI

from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

# from prompts import classifier_prompt, classifier_prompt_thought
# from fewshots import EXAMPLES_CLASSIFIER, EXAMPLES_CLASSIFIER_THOUGHT, DATABASES_INFO
from utils import *

from tools.math import calculator
from tools.text import agenda_retriever, scirex_retriever
from tools.table import tabtools
from tools.graph import graphtools
from tools.code import sql_interpreter, python_interpreter

from prompt_library.selection import ExampleSelection

class Controller:
    def __init__(self, args, selector:ExampleSelection=None) -> None:
        self.args = args
        self.table_toolkits = TABLES
        self.graph_toolkits = GRAPHS
        
        self.classifier = TaskClassifier(args)
        self.classification = None
        # self.decomposer = TaskDecomposer(args)
        # self.handler = SubtaskHandler(args)
        # self.verifier = Verifier()
        # self.summarizer = Summarizer()
        self.selector = selector

        self.solver = Solver(args)
        self.solve_step = 0
        self.solve_max_steps = 6

        self.decom_step = 0
        self.decom_max_steps = 6

        self.reflection = args.self_reflection

    def generate_hint_for_decomposer(self, classification, preference):
        ALL_HINTS = ALL_HINTS_PREFERENCE if preference else ALL_HINTS_ORIGIN
        if classification and classification in ALL_HINTS.keys():
            # save the classification
            self.classification = classification
            if self.decomposer.prompt_tag == "decomposer_no_hint":
                return "Hint: No hint.\n"
            else:
                return ALL_HINTS[classification] + '\n' + COLUMNS_DESC_LIST[classification] + '\n'
        else:
            return "Hint: None\n"

    def generate_hint(self, classification):
        if classification and classification in ALL_HINTS_ORIGIN.keys():
            # save the classification
            self.classification = classification
            return ALL_HINTS_ORIGIN[classification] + '\n' + COLUMNS_DESC_LIST[classification] + '\n'
        else:
            return "Hint: None\n"

    def _reset(self, question, key):
        self.question = question
        self.scratchpad = ''
        self.scratchpad_library = f"Question: {self.question}\n"
        self.history = ''
        self.answer = None
        self.key = key
        self.finished = False
        self.execution_error_halted = False

        self.solve_step = 0
        self.decom_step = 0
        self.tools = []
        self.paras = []
        self.steps = []
        self.results = []

    def run_tap(self, question, key, classifier_tag=True, preference_tag=False):
        self._reset(question, key)

        print(f"{'='*10}Question: {question}, GT: {key}{'='*10}")

        if classifier_tag:
            # classifier 进行问题分类
            response_classifier = self.classifier.run(self.question)
            response_classifier = parse_last_classification(response_classifier)
            self.scratchpad += self.generate_hint(response_classifier)
            print(f"##Task Classifier: {response_classifier}", flush=True)

        # 如果最大步数前尚未finish，循环进行分解
        while self.solve_step < self.solve_max_steps and not self.finished and (self.reflection or not self.execution_error_halted):
            self.solve_step += 1
            print(f"##Step {self.solve_step} SOLVING...")

            # 分解任务
            self.scratchpad += f"Step {self.solve_step}: "
            self.scratchpad_library += f"Step {self.solve_step}: "
            if self.solver.prompt_tag == "solver_adaptive" and (
                (self.solver.select_strategy == "goal_oriented" and self.solve_step == 1) or
                (self.solver.select_strategy == "process_oriented")
            ):
                self.solver.examples = self.selector.solver_select(self.solver.select_strategy, self.solver.select_num, self.question, self.classification, self.tools, self.paras, self.steps)
            response_solver = self.solver.run(self.question, self.scratchpad)
            self.scratchpad += f"{response_solver}\n"
            self.scratchpad_library += f"{response_solver}\n"
            step_i = f"Step {self.solve_step}: {response_solver}"
            print(f"##Step {self.solve_step}: {response_solver}", flush=True)
            
            # ===分解处理===
            tool_parameters = parse_solution(response_solver)
            tool = "None"
            para = "None"
            self.execution_error_halted = False
            # 如果没有解析出，或解析出的tool不在list里面，分解错误
            if not tool_parameters:
                self.execution_error_halted = True
                result = f"The format is invalid. The output must contain <CALL_BEGIN>TOOL[PARAMETERS]<CALL_END>. Please try again."
            elif not (tool_parameters[0] in ACTION_LIST.keys()):
                self.execution_error_halted = True
                result = f"The {tool_parameters[0]} is not in the tool list. Please try again."
            else:
                tool = tool_parameters[0]
                para = tool_parameters[1]
                result = self._exe_tool(tool, para)

            self.scratchpad += f"Result {self.solve_step}: {result}\n"
            self.scratchpad_library += f"Result {self.solve_step}: Omitted_Retrieve_Results\n" if tool in ['RetrieveAgenda', 'RetrieveScirex'] else f"Result {self.solve_step}: {result}\n"
            
            print(f"##Step {self.solve_step} Result: {tool}[{para}] --> {result}", flush=True)
            self.tools.append(tool)
            self.paras.append(para)
            self.steps.append(step_i)
            self.results.append(f"{'#FAILED#' if self.execution_error_halted else '#PASSED#'}")

        if self.answer == self.key:
            print(f"{'='*10}AnswerCorrect{'='*10}")
        else:
            print(f"{'='*10}AnswerIncorrect: GT=<{self.key}> Answer=<{self.answer}> Question=<{self.question}>{'='*10}")
        
        sum_result = {}
        sum_result['question'] = self.question
        sum_result['key'] = self.key
        sum_result['class'] = self.classification
        sum_result['tools'] = self.tools
        sum_result['paras'] = self.paras
        sum_result['steps'] = self.steps
        sum_result['results'] = self.results
        sum_result['answer'] = self.answer
        sum_result['scratchpad'] = self.scratchpad
        sum_result['scratchpad_library'] = self.scratchpad_library
        """
        {
            'question':str
            'key':str
            'class':str
            'tools':[]
            'paras':[]
            'steps':[]
            'results':[]
            'answer':str
            'scratchpad':str
            'scratchpad_library':str
        }
        """
        return sum_result


    def _exe_tool(self, tool_name: str, argument: str) -> str:
        """
        ACTION_LIST = {
            'Calculate': WolframAlphaCalculator,
            'RetrieveAgenda': query_llm_agenda,
            'RetrieveScirex': query_llm_scirex,
            'LoadDB': db.db_loader,
            'FilterDB': db.data_filter,
            'GetValue': db.get_value,
            'LoadGraph': gt.load_graph,
            'NeighbourCheck': gt.check_neighbours,
            'NodeCheck': gt.check_nodes,
            'EdgeCheck': gt.check_edges,
            'SQLInterpreter': sql_interpreter,
            'PythonInterpreter': python_interpreter,
            'Finish': finish
        }
        """
        assert tool_name in ACTION_LIST.keys()
        result = ''
        if tool_name == 'Finish':
            result = argument
            self.finished = True
            self.answer = argument
        elif tool_name == 'Calculate':
            try:
                result = str(calculator.WolframAlphaCalculator(argument)).strip('\n').strip()
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'Execution Error: Illegal Mathematical Expression. Note that: Provide the specific number involved in the calculation, not just the variable name. Please try again.'
        elif tool_name == 'RetrieveAgenda':
            try:
                result = agenda_retriever.query_llm([0], argument).strip('\n').strip()
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is no information that can be matched in the database. Please try another query.'
        elif tool_name == 'RetrieveScirex':
            try:
                result = scirex_retriever.query_llm([0], argument).strip('\n').strip()
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is no information that can be matched in the database. Please try another query.'
        elif tool_name == 'LoadDB':
            try:
                result = self.table_toolkits.db_loader(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'The database you want to query in not in the list. Please change another database for query.'
        elif tool_name == 'FilterDB':
            try:
                result = self.table_toolkits.data_filter(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is something wrong with the arguments you send for filtering. Please modify it.'
        elif tool_name == 'GetValue':
            try:
                result = self.table_toolkits.get_value(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                if argument.count(", "):
                    result = f'GetValue only supports one column. Please modify it.'
                else:
                    result = f'The value you are querying does not exist. Please modify it.'
        elif tool_name == 'LoadGraph':
            try:
                result = self.graph_toolkits.load_graph(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'The graph you want to query in not in the list. Please change another graph for query.'
        elif tool_name == 'NeighbourCheck':
            try:
                result = self.graph_toolkits.check_neighbours(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is something wrong with the arguments you send for neighbour checking. Please modify it.'
        elif tool_name == 'NodeCheck':
            try:
                if argument.count('"') == 2 or argument.count("'") == 2:
                    argument = argument.replace('"','').replace("'","")
                result = self.graph_toolkits.check_nodes(argument)
            except KeyError as e:
                print(e); self.execution_error_halted = True
                result = f'The node does not exist in the graph. Please modify it.'
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is something wrong with the arguments you send for node checking. Please modify it.'
        elif tool_name == 'EdgeCheck':
            try:
                result = self.graph_toolkits.check_edges(argument)
            except KeyError as e:
                print(e); self.execution_error_halted = True
                result = f'There is no edge between the two nodes. Please modify it.'
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is something wrong with the arguments you send for edge checking. Please modify it.'
        elif tool_name == 'SQLInterpreter':
            try:
                # mapping the name to mysql table name
                _reps = {
                    ' flight ': ' flights.flights_data ',
                    ' flights ': ' flights.flights_data ',
                    ' coffee ': ' coffee.coffee_data ',
                    ' yelp ': ' yelp.yelp_data ',
                    ' airbnb ': ' airbnb.airbnb_data ',
                }
                for _n in _reps:
                    argument = argument.replace(_n, _reps[_n])
                result = sql_interpreter.execute(argument)
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f'There is something wrong with the SQL command you send. Please modify it.'
        elif tool_name == 'PythonInterpreter':
            try:
                result = python_interpreter.execute(argument)
            except KeyError as e:
                print(e); self.execution_error_halted = True
                result = "Python Code must contain a result variable named answer. Please modify it."
            except Exception as e:
                print(e); self.execution_error_halted = True
                result = f"Execution Error: Illegal Python Code. Please try again."
        
        result = str(result)
        # dont set length limit of Retrieve Result
        if tool_name in ['RetrieveAgenda', 'RetrieveScirex']:
            return result
        # set the result length limit
        if len(result) > 2048:
            return result[:2048] + '...[too long, cannot be fully displayed]'
        return result


class Base_Agent:
    def __init__(self, 
                args
                ) -> None:
        self.args = args
        self.llm: llms = None

    def _llm_response(self, prompt: str):
        try:
            response = self.llm(prompt)
        except Exception as e:
            return f"llm reponse error: {e}"
        return response
    
    def _agent_response(self) -> str:
        debugging = True
        if debugging: print(f"{'-'*20}#{self.__class__.__name__} START DEBUGGING#{'-'*20}", flush=True)
        prompt_content = self._agent_prompt()
        if debugging: print(f"PROMPT: {self.prompt.input_variables}\n{remove_fewshot(prompt_content)}", flush=True)
        # message = HumanMessage(content=prompt_content)
        response = self._llm_response(prompt=prompt_content)
        if debugging: print(f"RAW_RESPONSE: {response}", flush=True)
        response = self._post_processing(response)
        if debugging: print(f"RESPONSE: {response}", flush=True)
        if debugging: print(f"{'-'*20}#{self.__class__.__name__} END DEBUGGING#{'-'*20}", flush=True)
        if False:
            print(f"{'-'*20}#{self.__class__.__name__} START DEBUGGING#{'-'*20}")
            print(f"PROMPT:")
            print(self.prompt.input_variables)
            print(remove_fewshot(prompt_content))
            print(f"RESPONSE:")
            print(response)
            print(f"{'-'*20}#{self.__class__.__name__} END DEBUGGING#{'-'*20}", flush=True)
        return response
    
    def _agent_prompt(self) -> str:
        raise NotImplementedError
    
    def _reset(self, question):
        self.question = question
        self.step_n = 0
        self.finished = False

    def _post_processing(self, output) -> str:
        output = output.split('\n')[0]
        return output

    def is_finished(self) -> bool:
        return self.finished
    
    def is_halted(self) -> bool:
        """是否被终止：没完成 且 (超过最大步数 or 超过token限制)"""
        halt = not self.finished and ((self.step_n >= self.max_steps) or self.llm.is_excessive_token(self._agent_prompt()))
        if halt:
            print(f"{self.__class__.__name__} is halted")
        return halt

class TaskClassifier(Base_Agent):
    def __init__(self, args) -> None:
        super().__init__(args)

        self.llm = create_llm(
            engine = self.args.classifier_engine,
            temperature = self.args.classifier_engine_temperature, 
            max_tokens = self.args.classifier_engine_max_tokens
        )

        self.prompt_tag = self.args.classifier_prompt
        self.prompt = PROMPT_TAGS[self.prompt_tag]

        self.databases_info = DATABASES_INFO
        self.examples = EXAMPLES_CLASSIFIER
        
        self.max_steps = self.args.classifier_max_steps

    def run(self, question) -> str:
        self._reset(question)
        result = None

        # (not finished) and (step_n < max_steps) and (token_len <= token_limit)
        while not self.is_finished() and not self.is_halted():
            self.step_n += 1
            response = self._agent_response()

            # llm output processing
            # result = response.split('\n')[0]
            result = response

            self.finished = True

        return result

    def _agent_prompt(self) -> str:
        if self.prompt_tag == 'classifier':
            kwargs = {
                'databases_info': self.databases_info,
                'examples_classifier': self.examples,
                'question': self.question
            }
        elif self.prompt_tag == 'classifier_no_info':
            kwargs = {
                'examples_classifier': self.examples,
                'question': self.question
            }
        elif self.prompt_tag == 'classifier_zero_shot':
            kwargs = {
                'databases_info': self.databases_info,
                'question': self.question
            }
        else:
            raise ValueError("Classifier: wrong prompt tag")

        # print(kwargs)
        return self.prompt.format(**kwargs)

    def _reset(self, question):
        return super()._reset(question)

    def _post_processing(self, output: str) -> str:
        if "<think>" in output and "</think>" in output:
            output = remove_thinking(output)
        return output.strip()

class TaskDecomposer(Base_Agent):
    def __init__(self, args) -> None:
        super().__init__(args)

        self.llm = create_llm(
            engine = self.args.decomposer_engine,
            temperature = self.args.decomposer_engine_temperature, 
            max_tokens = self.args.decomposer_engine_max_tokens
        )

        self.prompt_tag = self.args.decomposer_prompt
        self.prompt = PROMPT_TAGS[self.prompt_tag]
        
        self.tools_info = TOOLS_INFO
        self.examples = EXAMPLES_DECOMPOSER
        
        self.max_steps = self.args.decomposer_max_steps

    def run(self, question, scratchpad) -> str:
        self._reset(question, scratchpad)
        result = None
        
        # (not finished) and (step_n < max_steps) and (token_len <= token_limit)
        while not self.is_halted() and not self.is_finished():
            self.step_n += 1
            response = self._agent_response()
            
            # llm output processing
            # result = response.split('\n')[0]
            result = response

            self.finished = True

        return result
    
    def _agent_prompt(self) -> str:
        if self.prompt_tag in ['decomposer', 'decomposer_no_hint', 'decomposer_adaptive']:
            kwargs = {
                'tools_info': self.tools_info,
                'examples_decomposer': self.examples,
                'question': self.question,
                'scratchpad': self.scratchpad
            }
        else:
            raise ValueError("Decomposer: wrong prompt tag")
        content = self.prompt.format(**kwargs)
        # print(f"The prompt of decomposer: {content}")
        return content
    
    def _reset(self, question, scratchpad):
        super()._reset(question)
        self.scratchpad = scratchpad

class SubtaskHandler(Base_Agent):
    def __init__(self, args) -> None:
        super().__init__(args)
        
        self.llm = create_llm(
            engine = self.args.handler_engine,
            temperature = self.args.handler_engine_temperature, 
            max_tokens = self.args.handler_engine_max_tokens
        )
        
        self.prompt_tag = self.args.handler_prompt_strategy

        self.max_steps = self.args.handler_max_steps
        self.examples = None

    def run(self, question, history, tool, subtask, classification) -> str:
        self.classification = classification
        self._reset(question, history, tool, subtask)
        if tool == 'Finish':
            return self._get_answer(subtask)
        result = None

        # (not finished) and (step_n < max_steps) and (token_len <= token_limit)
        while not self.is_halted() and not self.is_finished():
            self.step_n += 1
            response = self._agent_response()
            
            # llm output processing
            # result = response.split('\n')[0]
            result = response

            self.finished = True

        if tool == 'SQLInterpreter':
            result = self._get_sql_result(result)
        return result
    
    def _get_sql_result(self, result: str) -> str:
        try:
            import re
            split_word = 'Flight_Number_Marketing_Airline'
            if result.count(split_word):
                tmp = result.split(split_word)[1].strip('= ').split("'")[1]
                new_str = re.sub('[a-zA-Z]', '', tmp)
                result = result.replace(tmp, new_str)
        finally: return result

    def _post_processing(self, output: str) -> str:
        # handler may output more than one lines
        if self.tool == 'PythonInterpreter':
            if output.count('answer = '):
                tmp = output.split('answer = ')
                return tmp[0] + 'answer = ' + tmp[1].split(']')[0] + ']'
            else:
                return output
        elif self.tool == 'FilterDB':
            if output.count('Answer:'):
                tmp = output.split('Answer:')
                return tmp[0] + 'Answer:' + tmp[1].split('\n')[0]
            else:
                return output
        else:
            return output.split('\n')[0]
    
    def _get_answer(self, s: str) -> str:
        # assert s.count('The final answer is '), "Handler: [Finish] error: can't get answer."
        answer = str.replace(s, 'The final answer is ', '').strip()
        return f'[{answer}]'
    
    def _agent_prompt(self) -> str:
        tools = ['Calculate','RetrieveAgenda','RetrieveScirex','LoadDB','FilterDB','GetValue','LoadGraph','NeighbourCheck','NodeCheck','EdgeCheck','SQLInterpreter','PythonInterpreter']
        assert self.tool in tools, "Handler: error: WRONG tool."

        if self.prompt_tag == "handler_tools_prompt":
            # 对每个工具进行prompt
            self.prompt = PROMPT_TAGS[self.prompt_tag][self.tool]
            if self.tool in ['LoadDB', 'LoadGraph', 'RetrieveAgenda', 'RetrieveScirex', 'PythonInterpreter', 'Calculate']:
                kwargs = {
                    'examples': TOOL_EXAMPLES_MS[self.tool],
                    'question': self.subtask
                }
            elif self.tool in ['FilterDB','GetValue']:
                kwargs = {
                    'columns_desc': COLUMNS_DESC_LIST[self.classification] if self.classification else '\n'.join(COLUMNS_DESC_LIST.values()),
                    'examples': TOOL_EXAMPLES_MS[self.tool],
                    'question': self.subtask
                }
            elif self.tool in ['NeighbourCheck','NodeCheck','EdgeCheck']:
                kwargs = {
                    'examples': TOOL_EXAMPLES_MS[self.tool],
                    'question': self.subtask
                }
            elif self.tool in ['SQLInterpreter']:
                # extract framework
                kwargs = {
                    'columns_desc': COLUMNS_DESC_LIST_SQL[self.classification] if self.classification else '\n'.join(COLUMNS_DESC_LIST_SQL.values()),
                    'examples': TOOL_EXAMPLES_MS[self.tool]["1"],
                    'question': self.question
                }
                framework = self._llm_response(self.prompt['framework'].format(**kwargs))
                ## extract the answer
                if framework.count('Answer:'):
                    framework = framework.split('Answer:')[1].split('\n')[0].strip()
                else:
                    framework = framework.replace('\n',' ').strip()
                print(f"FRAMEWORK RESPONSE: {framework}")

                #sijia: extract the query statement
                if not re.match(r'^(.*)select(.+)from(.+)where <conditions>$' ,framework):
                    framework = ''
                # information matching
                kwargs = {
                    'columns_desc': COLUMNS_DESC_LIST_SQL[self.classification] if self.classification else '\n'.join(COLUMNS_DESC_LIST_SQL.values()),
                    'examples': TOOL_EXAMPLES_MS[self.tool]["2"],
                    'question': f'[{self.classification}] {self.question}',
                    'framework': framework
                }
                association = self._llm_response(self.prompt['association'].format(**kwargs))
                ## extract the answer
                if association.count('Answer:'):
                    association = association.split('Answer:')[1].split('\n')[0].strip()
                else:
                    association = association.replace('\n',' ').strip()
                print(f"ASSOCIATION RESPONSE: {association}")

                # get final sql
                self.prompt = self.prompt['answer']
                kwargs = {
                    'examples': TOOL_EXAMPLES_MS[self.tool]["3"],
                    'question': self.question,
                    'framework': framework,
                    'association': association
                }

        elif self.prompt_tag == "handler_direct":
            self.prompt = PROMPT_TAGS[self.prompt_tag]
            columns_tmp = COLUMNS_DESC_LIST_SQL if self.tool == 'SQLInterpreter' else COLUMNS_DESC_LIST
            columns_tmp = columns_tmp[self.classification] if self.classification else '\n'.join(columns_tmp.values())
            kwargs = {
                'columns_desc': columns_tmp,
                'question': self.subtask,
                'tool': self.tool
            }
        
        elif self.prompt_tag == "handler_adaptive":
            # 对每个工具进行prompt
            self.prompt = PROMPT_TAGS[self.prompt_tag][self.tool]
            assert self.examples, "Handler: error: NO EXAMPLES."
            if self.tool in ['LoadDB', 'LoadGraph', 'RetrieveAgenda', 'RetrieveScirex', 'PythonInterpreter', 'Calculate', 'NeighbourCheck','NodeCheck','EdgeCheck']:
                kwargs = {
                    'examples': self.examples,
                    'question': self.subtask
                }
            elif self.tool in ['FilterDB','GetValue']:
                kwargs = {
                    'columns_desc': COLUMNS_DESC_LIST[self.classification] if self.classification else '\n'.join(COLUMNS_DESC_LIST.values()),
                    'examples': self.examples,
                    'question': self.subtask
                }
            elif self.tool in ['SQLInterpreter']:
                # extract framework
                kwargs = {
                    'columns_desc': COLUMNS_DESC_LIST_SQL[self.classification] if self.classification else '\n'.join(COLUMNS_DESC_LIST_SQL.values()),
                    'examples': self.examples,
                    'question': self.question
                }
        else:
            raise ValueError("Handler: error: WRONG PROMPT TAG.")

        return self.prompt.format(**kwargs)
    
    def _reset(self, question, history, tool, subtask):
        super()._reset(question)
        self.history = history
        self.tool = tool
        self.subtask = subtask

class Solver(Base_Agent):
    def __init__(self, args) -> None:
        super().__init__(args)

        self.llm = create_llm(
            engine = self.args.solver_engine,
            temperature = self.args.solver_engine_temperature, 
            max_tokens = self.args.solver_engine_max_tokens
        )

        self.prompt_tag = self.args.solver_prompt
        self.prompt = PROMPT_TAGS[self.prompt_tag]
        
        self.tools_info = TOOLS_INFO
        self.examples = EXAMPLES_SOLVER
        
        self.max_steps = self.args.solver_max_steps
        self.select_strategy = self.args.solver_select_strategy
        self.select_num = self.args.solver_select_num

    def run(self, question, scratchpad) -> str:
        self._reset(question, scratchpad)
        result = None
        
        # (not finished) and (step_n < max_steps) and (token_len <= token_limit)
        while not self.is_halted() and not self.is_finished():
            self.step_n += 1
            response = self._agent_response()
            
            # llm output processing
            # result = response.split('\n')[0]
            result = response

            self.finished = True

        return result
    
    def _agent_prompt(self) -> str:
        if self.prompt_tag in ['solver_adaptive']:
            kwargs = {
                'tools_info': self.tools_info,
                'examples_solver': self.examples,
                'question': self.question,
                'scratchpad': self.scratchpad
            }
        elif self.prompt_tag == "solver_static":
            kwargs = {
                'tools_info': self.tools_info,
                'examples_solver': EXAMPLES_SOLVER,
                'question': self.question,
                'scratchpad': self.scratchpad
            }
        else:
            raise ValueError("Solver: wrong prompt tag")
        content = self.prompt.format(**kwargs)
        # print(f"The prompt of solver: {content}")
        return content
    
    def _reset(self, question, scratchpad):
        super()._reset(question)
        self.scratchpad = scratchpad

    def _post_processing(self, output):
        if "<think>" in output and "</think>" in output:
            output = remove_thinking(output)
        output = output.strip()
        # output may contain more than one lines
        res = output.split('\n')
        for i in range(len(res)):
            if res[i].count("<CALL_END>"):
                return '\n'.join(res[:i+1])

        return output.split('\n')[0]

class Verifier:
    pass


class Summarizer:
    pass


class llms:
    def __init__(self) -> None:
        pass
    def __call__(self, prompt) -> str:
        pass
    def is_excessive_token(self, prompt) -> bool:
        pass


class azuregpt(llms):
    def __init__(self, engine, temperature, max_tokens) -> None:
        self.client = AzureChatOpenAI(
            deployment_name = engine,
            temperature = temperature, 
            max_tokens = max_tokens
        )
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens

    def __call__(self, prompt) -> str:
        self.client([HumanMessage(content=prompt)]).content

    def is_excessive_token(self, prompt) -> bool:
        token_limit_gpt35 = 3896 # gpt3.5 4k, set limit 3896
        return tiktoken.encoding_for_model(self.engine).encode(prompt) > token_limit_gpt35


class qwen(llms):
    def __init__(self, engine, temperature, max_tokens) -> None:
        from openai import OpenAI
        import os
        if engine == 'Qwen1.5-72B-Chat':
            self.client = OpenAI(base_url=os.getenv("QWEN_BASE"), api_key="XXX")
        elif engine == 'Qwen2-72B-Instruct':
            self.client = OpenAI(base_url=os.getenv("QWEN2_BASE"), api_key=os.getenv("QWEN2_KEY"))
        elif engine == 'Qwen2.5-72B-Instruct':
            self.client = OpenAI(base_url=os.getenv("QWEN2_BASE"), api_key=os.getenv("QWEN2_KEY"))
        else:
            raise ValueError("Error: wrong engine name")
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.token_limit = 32*1024 # set limit <str length> 32k (approximately 8k token)

    def __call__(self, prompt) -> str:
        response = self.client.chat.completions.create(
            model=self.engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
    
    def is_excessive_token(self, prompt) -> bool:
        return len(prompt) > self.token_limit


class qwen_bailian(qwen):
    def __init__(self, engine, temperature, max_tokens) -> None:
        from openai import OpenAI
        import os
        self.client = OpenAI(base_url=os.getenv("BAILIAN_BASE"), api_key=os.getenv("BAILIAN_KEY"))
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.token_limit = 32*1024 # set limit <str length> 32k (approximately 8k token)

class sf_model(qwen):
    def __init__(self, engine, temperature, max_tokens) -> None:
        from openai import OpenAI
        import os
        self.client = OpenAI(base_url=os.getenv("SF_BASE"), api_key=os.getenv("SF_KEY"))
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.token_limit = 32*1024 # set limit <str length> 32k (approximately 8k token)

class llama2(llms):
    pass

import re
def remove_thinking(text: str) -> str:
    clean_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return clean_text

def create_llm(engine: str, temperature, max_tokens) -> llms:
    # assert engine in LLM_MODELS.keys(), f"wrong model name, available: {LLM_MODELS.keys()}"
    if engine.startswith("bailian:"):
        llm = qwen_bailian(LLM_MODELS[engine], temperature, max_tokens)
    elif engine.startswith("qwen"):
        llm = qwen(LLM_MODELS[engine], temperature, max_tokens)
    elif engine.startswith('gpt'):
        llm = azuregpt(LLM_MODELS[engine], temperature, max_tokens)
    elif engine.startswith('sf'):
        llm = sf_model(engine.split(':', 1)[-1], temperature, max_tokens)
    elif engine.startswith('llama'):
        raise NotImplementedError
    return llm
