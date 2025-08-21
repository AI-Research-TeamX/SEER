import re
import json
import argparse
from tools.code.python_interpreter import execute as python_interpreter
from tools.code.sql_interpreter import execute as sql_interpreter
from tools.graph.graphtools import graph_toolkits
from tools.math.calculator import WolframAlphaCalculator
from tools.table.tabtools import table_toolkits
from tools.text.agenda_retriever import query_llm as query_llm_agenda
from tools.text.scirex_retriever import query_llm as query_llm_scirex
from tools.finish import finish
from prompts import *
from fewshots import *

def print_args(args):
    print('====Input Arguments====')
    print(json.dumps(vars(args), indent=2, sort_keys=False))

def load_args_from_config(temp:float=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_name', type=str, default='config_1')
    parser.add_argument('--data_path', type=str, default='toolqa_data')
    parser.add_argument('--path', type=str, default='SEER')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument("--dataset", type=str, default="")
    parser.add_argument("--hardness", type=str, default="")
    
    parser.add_argument("--logs", type=bool, default=False)
    parser.add_argument("--fpath", type=str, required=True)
    parser.add_argument('--self_reflection', action='store_true', help='enable self-reflection')
    
    temp_args, _ = parser.parse_known_args()

    # module prediction parameters
    with open('configs.json', 'r') as f:
        config = json.load(f)
    config = config[temp_args.config_name]
    # classifier
    parser.add_argument('--classifier_engine', type=str, default=config['classifier_engine'])
    parser.add_argument('--classifier_engine_temperature', type=float, default=float(config['classifier_engine_temperature']))
    parser.add_argument('--classifier_engine_max_tokens', type=int, default=int(config['classifier_engine_max_tokens']))
    parser.add_argument('--classifier_max_steps', type=int, default=int(config['classifier_max_steps']))
    parser.add_argument('--classifier_prompt', type=str, default=config['classifier_prompt'])

    # decomposer
    parser.add_argument('--decomposer_engine', type=str, default=config['decomposer_engine'])
    parser.add_argument('--decomposer_engine_temperature', type=float, default=float(config['decomposer_engine_temperature']))
    parser.add_argument('--decomposer_engine_max_tokens', type=int, default=int(config['decomposer_engine_max_tokens']))
    parser.add_argument('--decomposer_max_steps', type=int, default=int(config['decomposer_max_steps']))
    parser.add_argument('--decomposer_prompt', type=str, default=config['decomposer_prompt'])

    # handler
    parser.add_argument('--handler_engine', type=str, default=config['handler_engine'])
    parser.add_argument('--handler_engine_temperature', type=float, default=float(config['handler_engine_temperature']))
    parser.add_argument('--handler_engine_max_tokens', type=int, default=int(config['handler_engine_max_tokens']))
    parser.add_argument('--handler_max_steps', type=int, default=int(config['handler_max_steps']))
    parser.add_argument('--handler_prompt_strategy', type=str, default=config['handler_prompt_strategy'])

    # solver
    parser.add_argument('--solver_engine', type=str, default=config['solver_engine'])
    parser.add_argument('--solver_engine_temperature', type=float, default=float(config['solver_engine_temperature']))
    parser.add_argument('--solver_engine_max_tokens', type=int, default=int(config['solver_engine_max_tokens']))
    parser.add_argument('--solver_max_steps', type=int, default=int(config['solver_max_steps']))
    parser.add_argument('--solver_prompt', type=str, default=config['solver_prompt'])
    parser.add_argument('--solver_select_strategy', type=str, default=config['solver_select_strategy'])
    parser.add_argument('--solver_select_num', type=int, default=int(config['solver_select_num']))

    # verifier
    parser.add_argument('--verifier_engine', type=str, default=config['verifier_engine'])
    parser.add_argument('--verifier_engine_temperature', type=float, default=float(config['verifier_engine_temperature']))
    parser.add_argument('--verifier_engine_max_tokens', type=int, default=int(config['verifier_engine_max_tokens']))
    parser.add_argument('--verifier_max_steps', type=int, default=int(config['verifier_max_steps']))
    parser.add_argument('--verifier_prompt', type=str, default=config['verifier_prompt'])

    # summarizer
    parser.add_argument('--summarizer_engine', type=str, default=config['summarizer_engine'])
    parser.add_argument('--summarizer_engine_temperature', type=float, default=float(config['summarizer_engine_temperature']))
    parser.add_argument('--summarizer_engine_max_tokens', type=int, default=int(config['summarizer_engine_max_tokens']))
    parser.add_argument('--summarizer_max_steps', type=int, default=int(config['summarizer_max_steps']))
    parser.add_argument('--summarizer_prompt', type=str, default=config['summarizer_prompt'])

    args = parser.parse_args()

    if temp != None:
        args.classifier_engine_temperature = temp
        args.decomposer_engine_temperature = temp
        args.handler_engine_temperature = temp
        args.verifier_engine_temperature = temp
        args.summarizer_engine_temperature = temp
    return args


TABLES = table_toolkits(path="toolqa_data")
GRAPHS = graph_toolkits(path="toolqa_data")

ACTION_LIST = {
    'Calculate': WolframAlphaCalculator,
    'RetrieveAgenda': query_llm_agenda,
    'RetrieveScirex': query_llm_scirex,
    'LoadDB': TABLES.db_loader,
    'FilterDB': TABLES.data_filter,
    'GetValue': TABLES.get_value,
    'LoadGraph': GRAPHS.load_graph,
    'NeighbourCheck': GRAPHS.check_neighbours,
    'NodeCheck': GRAPHS.check_nodes,
    'EdgeCheck': GRAPHS.check_edges,
    'SQLInterpreter': sql_interpreter,
    'PythonInterpreter': python_interpreter,
    'Finish': finish
}

def parse_classification(string):
    string = str(string)
    pattern = r'^(.*)\[(.+)\](.*)$'
    match = re.match(pattern, string)
    
    if match:
        return match.group(2)
    else:
        return None

def parse_last_classification(string):
    string = str(string)
    pattern = r'\[(.+?)\]'
    matches = re.findall(pattern, string)
    if matches:
        return matches[-1]
    else:
        return None

def parse_decomposition(string):
    string = str(string)
    pattern = r'^(.*)\[(.+)\](.*)<(.+)>(.*)$'
    match = re.match(pattern, string)
    
    if match:
        tool = match.group(2)
        subtask = match.group(4)
        return tool, subtask
    else:
        return None

def parse_solution(string):
    string = str(string)
    try:
        assert "<CALL_BEGIN>" in string and "<CALL_END>" in string, "No call begin or call end"
        string = string.split("<CALL_BEGIN>")[1].split("<CALL_END>")[0]
        sbeg = string.find('[')
        send = string.rfind(']')
    except:
        return None
    else:
        tool = string[:sbeg]
        para = string[sbeg + 1:send]
        return tool, para


def parse_parameter(string):
    string = str(string)
    sbeg = string.find('[')
    send = string.rfind(']')
    if sbeg + 1 and send + 1:
        return string[sbeg + 1:send]
    else:
        return None
    pattern = r'^(.*)\[(.+)\](.*)$'
    match = re.match(pattern, string, re.S)
    
    if match:
        para = match.group(2)
        return para
    else:
        return None
    

def remove_fewshot(prompt: str) -> str:
    prefix = prompt.split('Here are ')[0]
    if prompt.count('(END OF EXAMPLES)'):
        suffix = prompt.split('(END OF EXAMPLES)')[1]
    else:
        # remove_fewshot for classifier_instruction_zero_shot
        suffix = prompt.split('Answer: These are your thoughts. [DATASET]')[1]
    return prefix.strip('\n').strip() + '\n' +  suffix.strip('\n').strip()


PROMPT_TAGS = {
    "classifier": classifier_prompt,
    "classifier_no_info": classifier_prompt_no_info,
    "classifier_zero_shot": classifier_prompt_zero_shot,

    "decomposer": decomposer_prompt,
    "decomposer_no_hint": decomposer_prompt,
    "decomposer_adaptive": decomposer_prompt,

    "handler_tools_prompt": TOOLS_PROMPT_LIST_MS,
    "handler_direct": ONE_DIRECT_PROMPT,
    "handler_combo": handler_prompt_combo,
    "handler_hierarchical": handler_prompt_hierarchical,
    "handler_adaptive": TOOLS_PROMPT_LIST,

    "solver_adaptive": solver_prompt,
    "solver_static": solver_prompt,
    "verifier": verifier_prompt,
    "summarizer": summarizer_prompt
}

LLM_MODELS = {
    "gpt3.5": "gpt-35-turbo", # azure openai
    "qwen1.5-72b": "Qwen1.5-72B-Chat",
    "qwen2-72b": "Qwen2-72B-Instruct",
    "qwen2.5-72b": "Qwen2.5-72B-Instruct",
    "bailian:qwen2.5-0.5b": "qwen2.5-0.5b-instruct", # bailian api
    "bailian:qwen2.5-1.5b": "qwen2.5-1.5b-instruct",
    "bailian:qwen2.5-72b": "qwen2.5-72b-instruct", 
    # "sf:XXXX/XXXX", # support siliconflow models
}
