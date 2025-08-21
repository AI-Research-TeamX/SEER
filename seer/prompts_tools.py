from langchain.prompts import PromptTemplate

# 子任务处理器：tool-level prompt
TOOL_LOADDB_INSTRUCTION = """You are an expert in using the LoadDB tool to load a database. Given a question, you need to load the required database. The available databases are flight, coffee, yelp and airbnb.
Please use the following format when answering:
Question: The question
Answer: LoadDB[DBName]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_FILTERDB_INSTRUCTION = """You are an expert in using the FilterDB tool to filter data. Given a question which is related to a database, you need to find out all the filter conditions in the database by the column, the relation (e.g., =, >, etc.) and the value based on the question.
{columns_desc}
Please use the following format when answering:
Question: The question
Thought: Your thought
Answer: FilterDB[conditions]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Thought: """
TOOL_GETVALUE_INSTRUCTION = """You are an expert in using the GetValue tool to get value. Given a question which is related to a database, you need to find out the asked column in the database.
{columns_desc}
Please use the following format when answering:
Question: The question
Answer: GetValue[column]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """

TOOL_LOADGRAPH_INSTRUCTION = """You are an expert in using the LoadGraph tool to load a graph. Given a question, you need to load the required graph. The available graph is dblp.
Please use the following format when answering:
Question: The question
Answer: LoadGraph[GraphName]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_NODECHECK_INSTRUCTION= """You are an expert in using the NodeCheck tool to check nodes. Given a question which is related to a node in the graph, you need to find out the graph and the node you are asked about. There are two graphs: PaperNet and AuthorNet.
Please use the following format when answering:
Question: The question
Answer: NodeCheck[GraphName, Node]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_NEIGHBOURCHECK_INSTRUCTION = """You are an expert in using the NeighbourCheck tool to check neighbours of a node. Given a question which is related to a node in the graph, you need to find out the graph and the node you are asked about. There are two graphs: PaperNet and AuthorNet.
Please use the following format when answering:
Question: The question
Answer: NeighbourCheck[GraphName, Node]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_EDGECHECK_INSTRUCTION= """You are an expert in using the EdgeCheck tool to check the edge between Node1 and Node2. Given a question which is related to two nodes in the graph, you need to find out the graph and the nodes you are asked about. There are two graphs: PaperNet and AuthorNet.
Please use the following format when answering:
Question: The question
Answer: EdgeCheck[GraphName, Node1, Node2]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """

TOOL_RETRIEVEAGENDA_INSTRUCTION= """You are an expert on key information extraction. Given a question that may contain some key information of event, person, date, start_time, end_time, location. You need to extract them in the form of RetrieveAgenda[keywords].
Please use the following format when answering:
Question: This is the question
Answer: RetrieveAgenda[keywords]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_RETRIEVESCIREX_INSTRUCTION= """You are an expert on key information extraction. Given a question contained some key information of metric, method, dataset, task. You need to extract them in the form of RetrieveScirex[keywords].
Please use the following format when answering:
Question: This is the question
Answer: RetrieveScirex[keywords]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """

TOOL_SQLINTERPRETER0_INSTRUCTION= """You are an expert in writing SQL statements. Given a database query task, you need to write a syntactically correct SQL statement and then use the SQLInterpreter tool to execute it.
{columns_desc}
Please use the following format when answering:
Question: This is the question
Answer: SQLInterpreter[The SQL statement]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_SQLINTERPRETER1_INSTRUCTION= """You are an expert in SQL framework extraction. Given a database query question, you need to figure out what possible SQL framework to use to solve the question. You can think step by step.
{columns_desc}
Here are some possible frameworks:
(1)Single column query framework: The question only needs to query a single column. The framework is SELECT <column_name> FROM <table_name> WHERE <conditions>
(2)Multiple columns query framework: The question needs to query more than one column. The framework is SELECT <column_names> FROM <table_name> WHERE <conditions>
(3)Basic operation query framework: This is typically used for multiple columns query that require basic operations(+-*/) to get an answer. The framework is SELECT <(basic)column_names> FROM <table_name> WHERE <conditions>
(4)Aggregate function query framework: The answer is computed using an aggregate function(COUNT,SUM,AVG,MIN,MAX). The framework is SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Please use the following format when answering:
Question: This is the question
Thought: Your thought
Answer: The SQL framework
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Thought: """
TOOL_SQLINTERPRETER2_INSTRUCTION= """You are an expert in information matching. Given a question and the SQL framework, you need to associate the table name, column names and conditions in the natural language questions with those in the database. You can think step by step to make sure you find out all the information, and output the missing parts in the given SQL framework.
{columns_desc}
Please use the following format when answering:
Question: This is the question
Framework: The SQL framework for solving the question
Thought: Your thought
Answer: Your answer
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Framework: {framework}
Thought: """
TOOL_SQLINTERPRETER3_INSTRUCTION= """You are an expert in writing SQL statements. Given a database query task, you need to write a syntactically correct SQL statement and then use the SQLInterpreter tool to execute it. You can use the context information of Framework and Association to help generate the SQL statement:
Please use the following format when answering:
Question: This is the question
Framework: The framework of SQL statement
Association: The information of association
Answer: SQLInterpreter[The SQL statement]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Framework: {framework}
Association: {association}
Answer: """

TOOL_PYTHONINTERPRETER_INSTRUCTION= """You are an expert in writing python code. Note that: your code must contain a result variable named answer at last.
Please use the following format when answering:
Question: The question
Answer: PythonInterpreter[Python]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """
TOOL_CALCULATE_INSTRUCTION= """You are an expert in using the Calculate tool. Given a question, you need to write a correct mathematical formula to solve it.
Please use the following format when answering:
Question: The question
Answer: Calculate[formula]
Here are some examples:
{examples}(END OF EXAMPLES)
Question: {question}
Answer: """


TOOLS_PROMPT_LIST_MS = {
    'LoadDB': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_LOADDB_INSTRUCTION),
    'FilterDB': PromptTemplate(
        input_variables=['columns_desc', "examples", "question"],
        template = TOOL_FILTERDB_INSTRUCTION),
    'GetValue': PromptTemplate(
        input_variables=['columns_desc', "examples", "question"],
        template = TOOL_GETVALUE_INSTRUCTION),
    'LoadGraph': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_LOADGRAPH_INSTRUCTION),
    'NodeCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_NODECHECK_INSTRUCTION),
    'NeighbourCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_NEIGHBOURCHECK_INSTRUCTION),
    'EdgeCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_EDGECHECK_INSTRUCTION),
    'RetrieveAgenda': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_RETRIEVEAGENDA_INSTRUCTION),
    'RetrieveScirex': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_RETRIEVESCIREX_INSTRUCTION),
    'SQLInterpreter': {
        'framework': PromptTemplate(
            input_variables=["columns_desc", "examples", "question"],
            template = TOOL_SQLINTERPRETER1_INSTRUCTION),
        'association': PromptTemplate(
            input_variables=["columns_desc", "examples", "question", "framework"],
            template = TOOL_SQLINTERPRETER2_INSTRUCTION),
        'answer': PromptTemplate(
            input_variables=["examples", "question", "framework", "association"],
            template = TOOL_SQLINTERPRETER3_INSTRUCTION)
        },
    'PythonInterpreter': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_PYTHONINTERPRETER_INSTRUCTION),
    'Calculate': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_CALCULATE_INSTRUCTION)
}


TOOLS_PROMPT_LIST = {
    'LoadDB': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_LOADDB_INSTRUCTION),
    'FilterDB': PromptTemplate(
        input_variables=["columns_desc", "examples", "question"],
        template = TOOL_FILTERDB_INSTRUCTION),
    'GetValue': PromptTemplate(
        input_variables=["columns_desc", "examples", "question"],
        template = TOOL_GETVALUE_INSTRUCTION),
    'LoadGraph': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_LOADGRAPH_INSTRUCTION),
    'NodeCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_NODECHECK_INSTRUCTION),
    'NeighbourCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_NEIGHBOURCHECK_INSTRUCTION),
    'EdgeCheck': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_EDGECHECK_INSTRUCTION),
    'RetrieveAgenda': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_RETRIEVEAGENDA_INSTRUCTION),
    'RetrieveScirex': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_RETRIEVESCIREX_INSTRUCTION),
    'SQLInterpreter': PromptTemplate(
        input_variables=["columns_desc", "examples", "question"],
        template = TOOL_SQLINTERPRETER0_INSTRUCTION),
    'PythonInterpreter': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_PYTHONINTERPRETER_INSTRUCTION),
    'Calculate': PromptTemplate(
        input_variables=["examples", "question"],
        template = TOOL_CALCULATE_INSTRUCTION)
}



ONE_DIRECT_INSTRUCTION = """You are an expert in generating the correct parameters of tools. Given a question and a related tool, you need to get the parameter to solve the question in the format of TOOL[PARAMETER].
{columns_desc}
Please use the following format when answering:
Question: The question
Tool: The tool
Answer: TOOL[PARAMETER]
Here are some examples:
Question: Use LoadDB tool to load flight database.
TOOL: LoadDB
Answer: LoadDB[flight]
Question: the DL1575 flight take from ATL to MCO on 2022-01-12
Tool: FilterDB
Answer: FilterDB[IATA_Code_Marketing_Airline=DL, Flight_Number_Marketing_Airline=1575, Origin=ATL, Dest=MCO, FlightDate=2022-01-12]
Question: the flight AS715 from EWR to SEA on 2022-05-06
Tool: FilterDB
Answer: FilterDB[IATA_Code_Marketing_Airline=AS, Flight_Number_Marketing_Airline=715, Origin=EWR, Dest=SEA, FlightDate=2022-05-06]
Question: the Southwest Airlines Co. flight from MIA to BWI on 2022-06-18
Tool: FilterDB
Answer: FilterDB[Airline=Southwest Airlines Co., Origin=MIA, Dest=BWI, FlightDate=2022-06-18]
Question: Use GetValue tool to get the departure delayed time
Tool: GetValue
Answer: GetValue[DepDelay]
Question: Use LoadGraph tool to load the DBLP graph.
Tool: LoadGraph
Answer: LoadGraph[dblp]
Question: Check the node of the paper Learning the Principle of Least Action with Reinforcement Learning. from the PaperNet in DBLP graph.
Tool: NodeCheck
Answer: NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]
Question: Check the neighboring nodes of Chao Zhang from the AuthorNet in DBLP graph.
Tool: NeighbourCheck
Answer: NeighbourCheck[AuthorNet, Chao Zhang]
Question: Check the edges between Chao Zhang and Weihong Lin from the AuthorNet in DBLP graph.
Tool: EdgeCheck
Answer: EdgeCheck[AuthorNet, Chao Zhang, Weihong Lin]
Question: Where did Stephen's Opera performance take place?
Tool: RetrieveAgenda
Answer: RetrieveAgenda[Stephen, Opera performance, location]
Question: What did Christopher do from 6:00 PM to 9:00 PM on 2022/12/26?
Tool: RetrieveAgenda
Answer: RetrieveAgenda[Christopher, on December 26 2022, 6:00 PM, 9:00 PM]
Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Tool: RetrieveScirex
Answer: RetrieveScirex[Mean_IoU, FRRN, Cityscapes, Semantic_Segmentation]
Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-03?
Tool: SQLInterpreter
Answer: SQLInterpreter[SELECT ArrDelay-DepDelay FROM flight WHERE IATA_Code_Marketing_Airline='DL' AND Flight_Number_Marketing_Airline='1575' AND Origin='ATL' AND Dest='MCO' AND FlightDate='2022-01-03']
Question: What was the opening price of coffee on 2016-12-23?
Tool: SQLInterpreter
Answer: SQLInterpreter[SELECT Open FROM coffee WHERE Date='2016-12-23']
Question: What is the average star rating of Chinese businesses in Saint Petersburg?
Tool: SQLInterpreter
Answer: SQLInterpreter[SELECT AVG(stars) FROM yelp WHERE categories LIKE '%Chinese%' and city='Saint Petersburg']
Question: How many airbnbs are there in Crown Heights that have a review rate higher than 4?
Tool: SQLInterpreter
Answer: SQLInterpreter[SELECT COUNT(*) FROM airbnb WHERE neighbourhood='Crown Heights' and review_rate_number>=4]
Question: Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday?
Tool: PythonInterpreter
Answer: PythonInterpreter[# solution in Python:
# Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday,
# he lost 2 more. How many golf balls did he have at the end of wednesday?
golf_balls_initial = 58
golf_balls_lost_tuesday = 23
golf_balls_lost_wednesday = 2
golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday
answer = golf_balls_left]
Question: Use Calculate tool to subtract (-17.0) from (-7.0)
Tool: Calculate
Answer: Calculate[(-17.0)-(-7.0)]
(END OF EXAMPLES)
Question: {question}
Tool: {tool}
Answer: """


ONE_DIRECT_PROMPT = PromptTemplate(
    input_variables=["columns_desc", "question", "tool"],
    template = ONE_DIRECT_INSTRUCTION
)
