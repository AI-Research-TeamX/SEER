# 这里写tdqa中的fewshots

# ------------------------------------------------------------
# ======== 分类器需要用到的数据库/数据集的相关信息 ========
DATABASES_INFO = """[flight]: It contains almost all flight information of airlines between 2022 and 2023. The keywords may be "flight", "flights", "flight number", or a flight number like "DL4130".
[coffee]: It contains the daily price of coffee, ranging from 2000 to 2022. The keywords may be "coffee", "coffee price", "volume of coffee", etc.
[yelp]: It is a subset of Yelp's business data across 8 metropolitan areas in the USA and Canada. The keywords may be "postal code", "business", "businesses", etc.
[airbnb]: It is a subset of Airbnb activities in New York. It's a dataset about online marketplace for lodging, primarily homestays for vacation rentals, and tourism activities. The keywords may be "room", "bedroom", "airbnbs", "apartment", "host", "host's name", etc.
[dblp]: It constructs the author-author and paper-paper relations formulated as two separate graphs. The organization, collaborators of authors, and citation relation of papers can be found in the graphs. The keywords may be "papers", "pages", "authors", "cite", "DBLP", etc.
[scirex]: It is a dataset based on a collection of scientific papers. Including specific methods, their metrics, and the evaluated datasets. The keywords may be "method", "metrics", "dataset", "datasets", "evaluated", etc.
[agenda]: It is a synthetic dataset to model real-world personal agenda data. Each question is related to someone's schedule on a specific date with a year/month/day format. The keywords may be "agenda", "schedule", "events", etc.
[gsm8k]: It is a grade school math problems dataset. Each question does not contain obvious keywords, but it is clearly a math problem that could be solved by using basic arithmetic operations.
"""

# ======== 分类器需要用到的示例 ========
EXAMPLES_CLASSIFIER = """Question: How long did UA3449 delay when arrival on 2022-03-24?
Answer: "UA3449" is a flight number, so the dataset related to the question is flight. [flight]

Question: What was the opening price of coffee on 2011-05-18?
Answer: The keyword in the question is "coffee", so the dataset related to the question is coffee. [coffee]

Question: Which city is The Pink Daisy located in PA?
Answer: The Pink Daisy is a business's name, so the dataset related to the question is yelp. [yelp]

Question: How much does it cost per night to stay at the most expensive entire home/apt in Eastchester?
Answer: It's about lodging, so the dataset related to the question is airbnb. [airbnb]

Question: What organization is Bradley E. Rucker from?
Answer: Bradley E. Rucker is the name of an author, and the organization of the author can be found in dblp graphs, so the dataset related to the question is dblp. [dblp]

Question: What is the corresponding Accuracy score of the PixelGAN_Autoencoders method on MNIST dataset for Unsupervised_image_classification task?
Answer: PixelGAN_Autoencoders is a method and MNIST is a scientific dataset, and the accuracy score can be retrieved in scirex papers, so the dataset related to the question is scirex. [scirex]

Question: When did Grace attend Broadway Show on 2022/02/17?
Answer: The question is about Grace's schedule on a specific date, 2022/02/17, and the date is in a year/month/day format, so the dataset related to the question is agenda. [agenda]

Question: Marilyn's first record sold 10 times as many copies as Harald's. If they sold 88,000 copies combined, how many copies did Harald sell?
Answer: It's a math problem and can be solved using basic arithmetic operations, so the dataset is gsm8k. [gsm8k]

"""


# ======== 分解器需要用到的工具信息 ========
TOOLS_INFO = """(1) Calculate[FORMULA], which calculates the formula FORMULA and returns the result.
(2) RetrieveAgenda[KEYWORD], which retrieves the agenda related to the keyword KEYWORD.
(3) RetrieveScirex[KEYWORD], which retrieves machine learning papers' paragraphs related to the keyword KEYWORD.
(4) LoadDB[DATABASE], which loads the database DATABASE and returns the database. The DATABASE can be one of the following: flight/coffee/airbnb/yelp.
(5) FilterDB[CONDITION], which filters the database DATABASE by the column COLUMN the relation (e.g., =, >, etc.) and the value VALUE, and returns the filtered database.
(6) GetValue[COLUMN], which returns the value of the column COLUMN in the database DATABASE.
(7) LoadGraph[GRAPH], which loads the graph GRAPH and returns the graph. The GRAPH can be one of the following: PaperNet/AuthorNet.
(8) NeighbourCheck[GRAPH, NODE], which lists the neighbours of the node NODE in the graph GRAPH and returns the neighbours. 
(9) NodeCheck[GRAPH, NODE], which returns the detailed attribute information of NODE. 
(10) EdgeCheck[GRAPH, NODE1, NODE2], which returns the detailed attribute information of the edge between NODE1 and NODE2. 
(11) SQLInterpreter[SQL_CODE], which interprets the SQL query SQL_CODE and returns the result.
(12) PythonInterpreter[PYTHON_CODE], which interprets the Python code PYTHON_CODE and returns the result.
(13) Finish[ANSWER], which returns the ANSWER and finishes the task.
"""

COLUMNS_DESC_LIST = {
    'flight': """There are some important columns descriptions of flight: {{DepTime: the departure time of flight; ArrTime: the arrival time of flight; CRSDepTime: CRS recorded departure time; CRSArrTime: CRS recorded arrival time; DepDelay: Difference in minutes between CRS recorded and actual departure time; ArrDelay: Difference in minutes between CRS recorded and actual arrival time; DepDelayMinutes: Difference in minutes between CRS recorded and actual departure time (early departures set to 0); ArrDelayMinutes: Difference in minutes between CRS recorded and actual arrival time (early arrivals set to 0); Airline: the airline name; IATA_Code_Marketing_Airline: Code assigned by IATA and commonly used to identify a carrier; Flight_Number_Marketing_Airline: flight number; AirTime: flight time in minutes; TaxiIn: taxi in time in minutes; DayOfWeek: day of week; Distance: distance between airports (miles); Cancelled: cancelled flight indicator (1=Yes); Diverted: diverted flight indicator (1=Yes)}}. """,
    'coffee': """There are some important columns descriptions of coffee: {{Date: the trading date; Open: price at market open; High: maximum price during the day; Low: minimum price during the day; Close: price at market close; Volume: the trading volume; Currency: currency in which prices are quoted}}. """,
    'yelp': """There are some important columns descriptions of yelp: {{name: the name of the business; address: the street address of the business; city: the city where the business is located; state: the state or province where the business is located; postal_code: the postal code for the business's location; latitude: the latitude coordinate of the business's location; longitude: the longitude coordinate of the business's location; stars: the average star rating of the business; review_count: the number of reviews the business has received; is_open: whether the business is open (1) or closed (0); attributes: additional attributes of the business; categories: a list of categories the business belongs to; hours: the business's operating hours}}. """,
    'airbnb': """There are some important columns descriptions of airbnb: {{id: Airbnb's unique identifier for the listing; NAME: name of the listing; [host name]: name of the host (usually just the first name(s)); neighbourhood: neighbourhood; lat: uses the World Geodetic System (WGS84) projection for latitude; long: Uses the World Geodetic System (WGS84) projection for longitude; cancellation_policy: cancellation policy; [room type]: room type; [Construction year]: year built of property; price: how much does a room cost per night; [service fee]: service fee; [minimum nights]: minimum number of night stay for the listing; [number of reviews]: the number of reviews the listing has; [last review]: the date of the last/newest review; [reviews per month]: the number of reviews the listing has over the lifetime of the listing; [review rate number]: review rate number; [calculated host listings count]: calculated host listings count; [availability 365]: the availability of the listing x days in the future as determined by the calendar}}. """,
    'dblp': """""",
    'scirex': """""",
    'agenda': """""",
    'gsm8k': """"""
}

import copy
COLUMNS_DESC_LIST_SQL = copy.deepcopy(COLUMNS_DESC_LIST)
COLUMNS_DESC_LIST_SQL['airbnb'] = """There are some important columns descriptions of airbnb: {{id: Airbnb's unique identifier for the listing; NAME: name of the listing; host_name: name of the host (usually just the first name(s)); neighbourhood: neighbourhood; lat: uses the World Geodetic System (WGS84) projection for latitude; long: Uses the World Geodetic System (WGS84) projection for longitude; cancellation_policy: cancellation policy; room_type: room type; Construction_year: year built of property; price: how much does a room cost per night; service_fee: service fee; minimum_nights: minimum number of night stay for the listing; number_of_reviews: the number of reviews the listing has; last_review: the date of the last/newest review; reviews_per_month: the number of reviews the listing has over the lifetime of the listing; review_rate_number: review rate number; calculated_host_listings_count: calculated host listings count; availability_365: the availability of the listing x days in the future as determined by the calendar}}. """

# ======== 分解器需要用到的来自分类器的提示 ========
ALL_HINTS_ORIGIN = {
    'flight': """Hint: The question is about flight. You can select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate], [SQLInterpreter]} to solve the question step by step until you can decide the final answer by using the tool [Finish]. Note that: no need to convert time format of result.""",
    'coffee': """Hint: The question is about coffee. You can select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate], [SQLInterpreter]} to solve the question step by step until you can decide the final answer by using the tool [Finish].""",
    'yelp': """Hint: The question is about yelp. You can select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate], [SQLInterpreter]} to solve the question step by step until you can decide the final answer by using the tool [Finish].""",
    'airbnb': """Hint: The question is about airbnb. You can select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate], [SQLInterpreter]} to solve the question step by step until you can decide the final answer by using the tool [Finish].""",
    'dblp': """Hint: The question is about dblp. You can select tools from {[LoadGraph], [NeighbourCheck], [NodeCheck], [EdgeCheck]} to solve the question step by step until you can decide the final answer by using the tool [Finish].""",
    'scirex': """Hint: The question is about scirex. You can use tool [RetrieveScirex] to solve the question and then decide the final answer by using the tool [Finish].""",
    'agenda': """Hint: The question is about agenda. You can use tool [RetrieveAgenda] to solve the question and then decide the final answer by using the tool [Finish].""",
    'gsm8k': """Hint: The question is about gsm8k. You can use tool [PythonInterpreter] to solve the question and then decide the final answer by using the tool [Finish]."""
}

ALL_HINTS_PREFERENCE = {
    'flight': """Hint: The question is about flight. You can first consider using [SQLInterpreter] tool to solve this problem. As an alternative option, you can also select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate]} to solve the question step by step. At last, you decide the final answer by using the tool [Finish]. Note that: no need to convert time format of result.""",
    'coffee': """Hint: The question is about coffee. You can first consider using [SQLInterpreter] tool to solve this problem. As an alternative option, you can also select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate]} to solve the question step by step. At last, you decide the final answer by using the tool [Finish].""",
    'yelp': """Hint: The question is about yelp. You can first consider using [SQLInterpreter] tool to solve this problem. As an alternative option, you can also select tools from {[LoadDB], [FilterDB], [GetValue], [Calculate]} to solve the question step by step. At last, you decide the final answer by using the tool [Finish].""",
    'airbnb': """Hint: The question is about airbnb. You can use tool [SQLInterpreter] to solve the question and then decide the final answer by using the tool [Finish].""",
    'dblp': """Hint: The question is about dblp. You can select tools from {[LoadGraph], [NeighbourCheck], [NodeCheck], [EdgeCheck]} to solve the question step by step until you can decide the final answer by using the tool [Finish].""",
    'scirex': """Hint: The question is about scirex. You can use tool [RetrieveScirex] to solve the question and then decide the final answer by using the tool [Finish].""",
    'agenda': """Hint: The question is about agenda. You can use tool [RetrieveAgenda] to solve the question and then decide the final answer by using the tool [Finish].""",
    'gsm8k': """Hint: The question is about gsm8k. You can use tool [PythonInterpreter] to solve the question and then decide the final answer by using the tool [Finish]."""
}

# ======== 分解器的示例 ========
EXAMPLES_DECOMPOSER = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Subtask 1: We can use LoadDB tool to load flight database. [LoadDB]<Use LoadDB tool to load flight database>
Result 1: We have successfully loaded the flight database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings.
Subtask 2: Before computing the extra minutes, we need to filter the flight database. [FilterDB]<Use FilterDB tool to fliter flight database: the DL1575 flight take from ATL to MCO on 2022-01-12>
Result 2: We have successfully filtered the data (1 rows).
Subtask 3: To compute the extra minutes, we should get the values of the departure delayed time and the arrival delayed time. First, use GetValue tool to get the departure delayed time(get the arrival delayed time in the next subtask). [GetValue]<Use GetValue tool to get the departure delayed time>
Result 3: -7.0
Subtask 4: Second, use GetValue tool to get the arrival delayed time. [GetValue]<Use GetValue tool to get the arrival delayed time>
Result 4: -17.0
Subtask 5: To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time. [Calculate]<Use Calculate tool to calculate -17.0 minus -7.0>
Result 5: -10
Subtask 6: There are no more questions left to ask. [Finish]<The final answer is -10>
Result 6: -10

Question: What was the opening price of coffee on 2011-05-18?
Subtask 1: We can use SQLInterpreter tool to solve it. [SQLInterpreter]<[coffee] What was the opening price of coffee on 2011-05-18?>
Result 1: 268.0
Subtask 2: There are no more questions left to ask. [Finish]<The final answer is 268.0>
Result 2: 268.0

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the published date of a paper. We need to check the node from the PaperNet in DBLP graph. [NodeCheck]<Check the node of the paper Learning the Principle of Least Action with Reinforcement Learning. from the PaperNet in DBLP graph.>
Result 2: {'title': 'Learning the Principle of Least Action with Reinforcement Learning.', 'authors': [{'id': '', 'name': 'Zehao Jin', 'org': ''}, {'id': '', 'name': 'Joshua Yao-Yu Lin', 'org': ''}, {'id': '', 'name': 'Siao-Fong Li', 'org': ''}], 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 8, 'keywords': [], 'doc_type': 'Conference', 'page_start': '307', 'page_end': '321'}
Subtask 3: According to the result above, we know the authors of the paper are Zehao Jin, Joshua Yao-Yu, Siao-Fong Li; the published year is 2021; the venue of the paper is AAAI Spring Symposium - MLPS; the paper is 321-307+1=15 pages. There are no more questions left to ask. [Finish]<The final answer is 2021>
Result 3: 2021

Question: How many collaborators does Chao Zhang have in the DBLP graph?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the collaborators of a person, we need to check the neighboring nodes from the AuthorNet in DBLP graph. [NeighbourCheck]<Check the neighboring nodes of Chao Zhang from the AuthorNet in DBLP graph.>
Result 2: ['Rao Fu', 'Jingdong Wang', 'Weihong Lin', 'X Chen', 'YUHUI YUAN', 'Lang Huang']
Subtask 3: There are no more questions left to ask. According to the result above, we know the number of collaborators of Chao Zhang is 6. [Finish]<The final answer is 6>
Result 3: 6

Question: What venue did Chao Zhang and Weihong Lin collaborate most in the DBLP citation network?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the most venue of two persons, we need to check the edges between them to get more information from the AuthorNet in DBLP graph. [EdgeCheck]<Check the edges between Chao Zhang and Weihong Lin from the AuthorNet in DBLP graph.>
Result 2: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Subtask 3: There is only one paper on which they collaborate. We can check the paper in PaperNet to get the venue(the most venue). [NodeCheck]<Check the node of the paper HRFormer: High-Resolution Vision Transformer for Dense Predict. from the PaperNet.>
Result 3: {'title': 'HRFormer: High-Resolution Vision Transformer for Dense Predict.', 'venue': {'raw': 'Annual Conference on Neural Information Processing Systems'}, 'n_citation': 95, 'page_start': '7281', 'page_end': '7293'}
Subtask 4: The venue of this paper is Annual Conference on Neural Information Processing Systems. There are no more questions left to ask. [Finish]<The final answer is Annual Conference on Neural Information Processing Systems>
Result 4: Annual Conference on Neural Information Processing Systems

Question: Where did Stephen's Opera performance take place?
Subtask 1: We can use RetrieveAgenda tool to retrieve relevant information. [RetrieveAgenda]<Where did Stephen's Opera performance take place?>
Result 1: On January 29, 2022, there will be an opera performance at the Lyric Opera House, featuring Stephen. The show will start at 7:00 PM and end at 9:00 PM. It promises to be a wonderful evening of beautiful music and powerful performances in a stunning venue. Come and experience the magic of opera at its finest!
Subtask 2: There are no more questions left to ask. According to the result above, we know the event happened in Lyric Opera. [Finish]<The final answer is Lyric Opera>
Result 2: Lyric Opera

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Subtask 1: We can use RetrieveScirex tool to retrieve relevant information. [RetrieveScirex]<What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?>
Result 1: The other stream undergoes a sequence of pooling operations to obtain robust features for recognition. The two streams are coupled at the full image resolution using residuals. Without additional processing steps and without pretraining, our approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset.
Subtask 2: There are no more questions left to ask. As the approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset, the answer should be 71.8%. [Finish]<The final answer is 71.8%>
Result 2: 71.8%

Question: Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday? 
Subtask 1: We can use PythonInterpreter tool to solve the question. [PythonInterpreter]<Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday?>
Result 1: 33
Subtask 2: There are no more questions left to ask. After execution of Python Code, we know that the answer is 33. [Finish]<The final answer is 33>
Result 2: 33

"""

EXAMPLES_DECOMPOSER_PREFERENCE = """Question: How many extra minutes did the WN2361 flight take from LAX to IAH on 2022-05-24?
Subtask 1: According to the hint, we know it is a question about flight database, we can consider using SQLInterpreter tool to solve it. [SQLInterpreter]<How many extra minutes did the WN2361 flight take from LAX to IAH on 2022-05-24?>
Result 1: ArrDelay-DepDelay: -9
Subtask 2: There are no more questions left to ask. [Finish]<The final answer is -9>

Question: What was the percentage change in coffee price on 2010-08-23, based on the difference between the opening and closing prices?
Subtask 1: We can use SQLInterpreter tool to solve this coffee question. [SQLInterpreter]<What was the percentage change in coffee price on 2010-08-23, based on the difference between the opening and closing prices?>
Result 1: (Close-Open)/Open: -0.013854930725346434
Subtask 2: There are no more questions left to ask. Round the result to two decimal places. [Finish]<The final answer is -1.38%>

Question: Does Schweiger Dermatology Group require appointment in area with postal code 19468, Limerick, PA?
Subtask 1: Try to use SQLInterpreter tool to solve the question related to yelp database. [SQLInterpreter]<Does Schweiger Dermatology Group require appointment in area with postal code 19468, Limerick, PA?>
Result 1: attributes: | {'RestaurantsDelivery': 'True', 'RestaurantsTakeOut': 'True', 'BusinessAcceptsCreditCards': 'True', 'BikeParking': 'True', 'RestaurantsAttire': "u'casual'", 'Ambience': "{'romantic': False, 'intimate': False, 'classy': False, 'hipster': False, 'divey |
Subtask 2: There are no ByAppointmentOnly attribute, so it does not require appointment. [Finish]<The final answer is no>

Question: What is the host's name for Cozy Brooklyn Room in Bushwick?
Subtask 1: The question is about airbnb database, we should use SQLInterpreter tool to solve it. [SQLInterpreter]<What is the host's name for Cozy Brooklyn Room in Bushwick?>
Result 1: host_name: Jessica
Subtask 2: The host's name is Jessica. [Finish]<The final answer is Jessica>

Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Subtask 1: We can use LoadDB tool to load flight database. [LoadDB]<Use LoadDB tool to load flight database>
Result 1: We have successfully loaded the flight database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, ...
Subtask 2: Before computing the extra minutes, we need to filter the flight database. [FilterDB]<Use FilterDB tool to fliter flight database: the DL1575 flight take from ATL to MCO on 2022-01-12>
Result 2: We have successfully filtered the data (1 rows).
Subtask 3: To compute the extra minutes, we should get the values of the departure delayed time and the arrival delayed time. First, use GetValue tool to get the departure delayed time(get the arrival delayed time in the next subtask). [GetValue]<Use GetValue tool to get the departure delayed time>
Result 3: -7.0
Subtask 4: Second, use GetValue tool to get the arrival delayed time. [GetValue]<Use GetValue tool to get the arrival delayed time>
Result 4: -17.0
Subtask 5: To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time. [Calculate]<Use Calculate tool to calculate -17.0 minus -7.0>
Result 5: -10
Subtask 6: There are no more questions left to ask. [Finish]<The final answer is -10>

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the published date of a paper. We need to check the node from the PaperNet in DBLP graph. [NodeCheck]<Check the node of the paper Learning the Principle of Least Action with Reinforcement Learning. from the PaperNet in DBLP graph.>
Result 2: {'title': 'Learning the Principle of Least Action with Reinforcement Learning.', 'authors': [{'id': '', 'name': 'Zehao Jin', 'org': ''}, {'id': '', 'name': 'Joshua Yao-Yu Lin', 'org': ''}, {'id': '', 'name': 'Siao-Fong Li', 'org': ''}], 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 8, 'keywords': [], 'doc_type': 'Conference', 'page_start': '307', 'page_end': '321'}
Subtask 3: According to the result above, we know the authors of the paper are Zehao Jin, Joshua Yao-Yu, Siao-Fong Li; the published year is 2021; the venue of the paper is AAAI Spring Symposium - MLPS; the paper is 321-307+1=15 pages. There are no more questions left to ask. [Finish]<The final answer is 2021>

Question: How many collaborators does Chao Zhang have in the DBLP graph?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the collaborators of a person, we need to check the neighboring nodes from the AuthorNet in DBLP graph. [NeighbourCheck]<Check the neighboring nodes of Chao Zhang from the AuthorNet in DBLP graph.>
Result 2: ['Rao Fu', 'Jingdong Wang', 'Weihong Lin', 'X Chen', 'YUHUI YUAN', 'Lang Huang']
Subtask 3: There are no more questions left to ask. According to the result above, we know the number of collaborators of Chao Zhang is 6. [Finish]<The final answer is 6>

Question: What venue did Chao Zhang and Weihong Lin collaborate most in the DBLP citation network?
Subtask 1: We can use LoadGraph tool to load the DBLP graph. [LoadGraph]<Use LoadGraph tool to load the DBLP graph.>
Result 1: DBLP graph is loaded.
Subtask 2: The question is asking the most venue of two persons, we need to check the edges between them to get more information from the AuthorNet in DBLP graph. [EdgeCheck]<Check the edges between Chao Zhang and Weihong Lin from the AuthorNet in DBLP graph.>
Result 2: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Subtask 3: There is only one paper on which they collaborate. We can check the paper in PaperNet to get the venue(the most venue). [NodeCheck]<Check the node of the paper HRFormer: High-Resolution Vision Transformer for Dense Predict. from the PaperNet.>
Result 3: {'title': 'HRFormer: High-Resolution Vision Transformer for Dense Predict.', 'venue': {'raw': 'Annual Conference on Neural Information Processing Systems'}, 'n_citation': 95, 'page_start': '7281', 'page_end': '7293'}
Subtask 4: The venue of this paper is Annual Conference on Neural Information Processing Systems. There are no more questions left to ask. [Finish]<The final answer is Annual Conference on Neural Information Processing Systems>

Question: Where did Stephen's Opera performance take place?
Subtask 1: We can use RetrieveAgenda tool to retrieve relevant information. [RetrieveAgenda]<Where did Stephen's Opera performance take place?>
Result 1: On January 29, 2022, there will be an opera performance at the Lyric Opera House, featuring Stephen. The show will start at 7:00 PM and end at 9:00 PM. It promises to be a wonderful evening of beautiful music and powerful performances in a stunning venue. Come and experience the magic of opera at its finest!
Subtask 2: There are no more questions left to ask. According to the result above, we know the event happened in Lyric Opera. [Finish]<The final answer is Lyric Opera>

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Subtask 1: We can use RetrieveScirex tool to retrieve relevant information. [RetrieveScirex]<What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?>
Result 1: The other stream undergoes a sequence of pooling operations to obtain robust features for recognition. The two streams are coupled at the full image resolution using residuals. Without additional processing steps and without pretraining, our approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset.
Subtask 2: There are no more questions left to ask. As the approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset, the answer should be 71.8%. [Finish]<The final answer is 71.8%>

Question: Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday? 
Subtask 1: We can use PythonInterpreter tool to solve the question. [PythonInterpreter]<Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday?>
Result 1: 33
Subtask 2: There are no more questions left to ask. After execution of Python Code, we know that the answer is 33. [Finish]<The final answer is 33>

"""


# ======== 静态 Solver 的示例 ========
EXAMPLES_SOLVER = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Step 1: We can use LoadDB tool to load flight database. <CALL_BEGIN>LoadDB[flight]<CALL_END>
Result 1: We have successfully loaded the flight database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings.
Step 2: Before computing the extra minutes, we need to filter the flight database. <CALL_BEGIN>FilterDB[IATA_Code_Marketing_Airline=DL, Flight_Number_Marketing_Airline=1575, Origin=ATL, Dest=MCO, FlightDate=2022-01-12]<CALL_END>
Result 2: We have successfully filtered the data (1 rows).
Step 3: To compute the extra minutes, we should get the values of the departure delayed time and the arrival delayed time. First, use GetValue tool to get the departure delayed time(get the arrival delayed time in the next subtask). <CALL_BEGIN>GetValue[DepDelay]<CALL_END>
Result 3: -7.0
Step 4: Second, use GetValue tool to get the arrival delayed time. <CALL_BEGIN>GetValue[ArrDelay]<CALL_END>
Result 4: -17.0
Step 5: To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time. <CALL_BEGIN>Calculate[(-17)-(-7)]<CALL_END>
Result 5: -10
Step 6: There are no more questions left to ask. The final answer is -10. <CALL_BEGIN>Finish[-10]<CALL_END>
Result 6: -10

Question: What was the opening price of coffee on 2011-05-18?
Step 1: We can use SQLInterpreter tool to solve it. <CALL_BEGIN>SQLInterpreter[SELECT Open FROM coffee WHERE Date='2011-05-18']<CALL_END>
Result 1: 268.0
Step 2: There are no more questions left to ask. The final answer is 268.0. <CALL_BEGIN>Finish[268.0]<CALL_END>
Result 2: 268.0

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?
Step 1: We can use LoadGraph tool to load the DBLP graph. <CALL_BEGIN>LoadGraph[dblp]<CALL_END>
Result 1: DBLP graph is loaded.
Step 2: The question is asking the published date of a paper. We need to check the node from the PaperNet in DBLP graph. <CALL_BEGIN>NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]<CALL_END>
Result 2: {'title': 'Learning the Principle of Least Action with Reinforcement Learning.', 'authors': [{'id': '', 'name': 'Zehao Jin', 'org': ''}, {'id': '', 'name': 'Joshua Yao-Yu Lin', 'org': ''}, {'id': '', 'name': 'Siao-Fong Li', 'org': ''}], 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 8, 'keywords': [], 'doc_type': 'Conference', 'page_start': '307', 'page_end': '321'}
Step 3: According to the result above, we know the authors of the paper are Zehao Jin, Joshua Yao-Yu, Siao-Fong Li; the published year is 2021; the venue of the paper is AAAI Spring Symposium - MLPS; the paper is 321-307+1=15 pages. There are no more questions left to ask. The final answer is 2021. <CALL_BEGIN>Finish[2021]<CALL_END>
Result 3: 2021

Question: How many collaborators does Chao Zhang have in the DBLP graph?
Step 1: We can use LoadGraph tool to load the DBLP graph. <CALL_BEGIN>LoadGraph[dblp]<CALL_END>
Result 1: DBLP graph is loaded.
Step 2: The question is asking the collaborators of a person, we need to check the neighboring nodes from the AuthorNet in DBLP graph. <CALL_BEGIN>NeighbourCheck[AuthorNet, Chao Zhang]<CALL_END>
Result 2: ['Rao Fu', 'Jingdong Wang', 'Weihong Lin', 'X Chen', 'YUHUI YUAN', 'Lang Huang']
Step 3: There are no more questions left to ask. According to the result above, we know the number of collaborators of Chao Zhang is 6. <CALL_BEGIN>Finish[6]<CALL_END>
Result 3: 6

Question: What venue did Chao Zhang and Weihong Lin collaborate most in the DBLP citation network?
Step 1: We can use LoadGraph tool to load the DBLP graph. <CALL_BEGIN>LoadGraph[dblp]<CALL_END>
Result 1: DBLP graph is loaded.
Step 2: The question is asking the most venue of two persons, we need to check the edges between them to get more information from the AuthorNet in DBLP graph. <CALL_BEGIN>EdgeCheck[AuthorNet, Chao Zhang, Weihong Lin]<CALL_END>
Result 2: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Step 3: There is only one paper on which they collaborate. We can check the paper in PaperNet to get the venue(the most venue). <CALL_BEGIN>NodeCheck[PaperNet, HRFormer: High-Resolution Vision Transformer for Dense Predict.]<CALL_END>
Result 3: {'title': 'HRFormer: High-Resolution Vision Transformer for Dense Predict.', 'venue': {'raw': 'Annual Conference on Neural Information Processing Systems'}, 'n_citation': 95, 'page_start': '7281', 'page_end': '7293'}
Step 4: The venue of this paper is Annual Conference on Neural Information Processing Systems. There are no more questions left to ask. <CALL_BEGIN>Finish[Annual Conference on Neural Information Processing Systems]<CALL_END>
Result 4: Annual Conference on Neural Information Processing Systems

Question: Where did Stephen's Opera performance take place?
Step 1: We can use RetrieveAgenda tool to retrieve relevant information. <CALL_BEGIN>RetrieveAgenda[Stephen, Opera performance, location]<CALL_END>
Result 1: On January 29, 2022, there will be an opera performance at the Lyric Opera House, featuring Stephen. The show will start at 7:00 PM and end at 9:00 PM. It promises to be a wonderful evening of beautiful music and powerful performances in a stunning venue. Come and experience the magic of opera at its finest!
Step 2: There are no more questions left to ask. According to the result above, we know the event happened in Lyric Opera. <CALL_BEGIN>Finish[Lyric Opera]<CALL_END>
Result 2: Lyric Opera

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Step 1: We can use RetrieveScirex tool to retrieve relevant information. <CALL_BEGIN>RetrieveScirex[Mean_IoU, FRRN, Cityscapes, Semantic_Segmentation]<CALL_END>
Result 1: The other stream undergoes a sequence of pooling operations to obtain robust features for recognition. The two streams are coupled at the full image resolution using residuals. Without additional processing steps and without pretraining, our approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset.
Step 2: There are no more questions left to ask. As the approach achieves an intersection-over-union score of 71.8% on the Cityscapes dataset, the answer should be 71.8%. <CALL_BEGIN>Finish[71.8%]<CALL_END>
Result 2: 71.8%

Question: Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday? 
Step 1: We can use PythonInterpreter tool to solve the question. <CALL_BEGIN>PythonInterpreter[# solution in Python:
# Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday,
# he lost 2 more. How many golf balls did he have at the end of wednesday?
golf_balls_initial = 58
golf_balls_lost_tuesday = 23
golf_balls_lost_wednesday = 2
golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday
answer = golf_balls_left]<CALL_END>
Result 1: 33
Step 2: There are no more questions left to ask. After execution of Python Code, we know that the answer is 33. <CALL_BEGIN>Finish[33]<CALL_END>
Result 2: 33

"""


# ======== 处理器需要用到的列名信息 ========
COLUMNS_INFO = """Table flight, columns = [FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings]
Table coffee, columns = [Date, Open, High, Low, Close, Volume, Currency]
Table yelp, columns = [business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours]
Table airbnb, columns = [id, NAME, host id, host_identity_verified, host name, neighbourhood group, neighbourhood, lat, long, country, country code, instant_bookable, cancellation_policy, room type, Construction year, price, service fee, minimum nights, number of reviews, last review, reviews per month, review rate number, calculated host listings count, availability 365, house_rules, license]
"""

PARAMETER_INFO = """
"""

EXAMPLES_HANDLER_DIRECT = """
"""

EXAMPLES_HANDLER_COMBO = """
"""

EXAMPLES_HANDLER_HIERARCHICAL = """
"""

# ------------------------- tools fewshots -------------------------
TOOL_LOADDB_EXAMPLES = """Question: Use LoadDB tool to load flight database.
Answer: LoadDB[flight]
"""
TOOL_FILTERDB_EXAMPLES = """Question: the DL1575 flight take from ATL to MCO on 2022-01-12
Thought: Extract key conditions to filter from the given question:
(1)DL1575 flight's carrier code is DL --> <IATA_Code_Marketing_Airline=DL>
(2)DL1575 flight's flight number is 1575 --> <Flight_Number_Marketing_Airline=1575>
(3)from ALT --> <Origin=ATL>
(4)to MCO --> <Dest=MCO>
(5)on 2022-01-12 --> <FlightDate=2022-01-12>
Answer: FilterDB[IATA_Code_Marketing_Airline=DL, Flight_Number_Marketing_Airline=1575, Origin=ATL, Dest=MCO, FlightDate=2022-01-12]
Question: the flight AS715 from EWR to SEA on 2022-05-06
Thought: Extract the conditions from the given question:
(1)AS715 flight's carrier code is AS --> <IATA_Code_Marketing_Airline=AS>
(2)AS715 flight's flight number is 715 --> <Flight_Number_Marketing_Airline=715>
(3)from EWR --> <Origin=EWR>
(4)to SEA --> <Dest=SEA>
(5)on 2022-05-06 --> <FlightDate=2022-05-06>
Answer: FilterDB[IATA_Code_Marketing_Airline=AS, Flight_Number_Marketing_Airline=715, Origin=EWR, Dest=SEA, FlightDate=2022-05-06]
Question: the Southwest Airlines Co. flight from MIA to BWI on 2022-06-18
Thought: Extract filter conditions from the given:
(1)the Southwest Airlines Co. flight --> <Airline=Southwest Airlines Co.>
(3)from MIA --> <Origin=MIA>
(4)to BWI --> <Dest=BWI>
(5)on 2022-06-18 --> <FlightDate=2022-06-18>
Answer: FilterDB[Airline=Southwest Airlines Co., Origin=MIA, Dest=BWI, FlightDate=2022-06-18]
"""
TOOL_GETVALUE_EXAMPLES = """Question: Use GetValue tool to get the departure delayed time
Answer: GetValue[DepDelay]
"""
TOOL_LOADGRAPH_EXAMPLES = """Question: Use LoadGraph tool to load the DBLP graph.
Answer: LoadGraph[dblp]
"""
TOOL_NODECHECK_EXAMPLES = """Question: Check the node of the paper Learning the Principle of Least Action with Reinforcement Learning. from the PaperNet in DBLP graph.
Answer: NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]
"""
TOOL_NEIGHBOURCHECK_EXAMPLES = """Question: Check the neighboring nodes of Chao Zhang from the AuthorNet in DBLP graph.
Answer: NeighbourCheck[AuthorNet, Chao Zhang]
"""
TOOL_EDGECHECK_EXAMPLES = """Question: Check the edges between Chao Zhang and Weihong Lin from the AuthorNet in DBLP graph.
Answer: EdgeCheck[AuthorNet, Chao Zhang, Weihong Lin]
"""
TOOL_RETRIEVEAGENDA_EXAMPLES = """Question: Where did Stephen's Opera performance take place?
Answer: RetrieveAgenda[Stephen, Opera performance, location]
Question: What did Christopher do from 6:00 PM to 9:00 PM on 2022/12/26?
Answer: RetrieveAgenda[Christopher, on December 26 2022, 6:00 PM, 9:00 PM]
"""
TOOL_RETRIEVESCIREX_EXAMPLES = """Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Answer: RetrieveScirex[Mean_IoU, FRRN, Cityscapes, Semantic_Segmentation]
"""
TOOL_SQLINTERPRETER0_EXAMPLES = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-03?
Answer: SQLInterpreter[SELECT ArrDelay-DepDelay FROM flight WHERE IATA_Code_Marketing_Airline='DL' AND Flight_Number_Marketing_Airline='1575' AND Origin='ATL' AND Dest='MCO' AND FlightDate='2022-01-03']
Question: What was the opening price of coffee on 2016-12-23?
Answer: SQLInterpreter[SELECT Open FROM coffee WHERE Date='2016-12-23']
Question: What is the average star rating of Chinese businesses in Saint Petersburg?
Answer: SQLInterpreter[SELECT AVG(stars) FROM yelp WHERE categories LIKE '%Chinese%' and city='Saint Petersburg']
Question: How many airbnbs are there in Crown Heights that have a review rate higher than 4?
Answer: SQLInterpreter[SELECT COUNT(*) FROM airbnb WHERE neighbourhood='Crown Heights' and review_rate_number>=4]
"""
TOOL_PYTHONINTERPRETER_EXAMPLES = """Question: Michael had 58 golf balls. On Tuesday, he lost 23 golf balls. On Wednesday, he lost 2 more. How many golf balls did he have at the end of Wednesday?
Answer: PythonInterpreter[# solution in Python:
# Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday,
# he lost 2 more. How many golf balls did he have at the end of wednesday?
golf_balls_initial = 58
golf_balls_lost_tuesday = 23
golf_balls_lost_wednesday = 2
golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday
answer = golf_balls_left]
"""
TOOL_CALCULATE_EXAMPLES = """Question: Use Calculate tool to subtract (-17.0) from (-7.0)
Answer: Calculate[(-17.0)-(-7.0)]
"""

TOOL_SQLINTERPRETER1_EXAMPLES = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-03?
Thought: The "extra minutes" does not directly correspond to one of the column names in the database and requires some basic operations to obtain, so the framework is Basic operation query framework.
Answer: SELECT <(basic)column_names> FROM <table_name> WHERE <conditions>
Question: What was the opening price of coffee on 2016-12-23?
Thought: We can query the column of Open to get the value of opening price on 2016-12-23. The framework is Single column query framework.
Answer: SELECT <column_name> FROM <table_name> WHERE <conditions>
Question: What is the average star rating of Chinese businesses in Saint Petersburg?
Thought: We need to use AVG aggregate function to query. So the framework is Aggregate function query framework.
Answer: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Question: How many airbnbs are there in Crown Heights that have a review rate higher than 4?
Thought: We need to COUNT the all airbnbs in Crown Heights that have a review rate higher than 4, So the framework is Aggregate function query framework.
Answer: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
"""
TOOL_SQLINTERPRETER2_EXAMPLES = """Question: [flight] How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-03?
Framework: SELECT <(basic)column_names> FROM <table_name> WHERE <conditions>
Thought: The database related to the question is flight, so we need table_name=<flight>. In the question, we are asked 
(1)"extra minutes", we need to subtract the departure delayed time from the arrival delayed time to compute the extra minutes. So <(basic)column_names>=<ArrDelay-DepDelay>; 
(2)DL1575 flight's carrier code is DL, <IATA_Code_Marketing_Airline='DL'>
(3)DL1575 flight's flight number is 1575, <Flight_Number_Marketing_Airline='1575'>
(4)"from ALT", so we need <Origin='ATL'>
(5)"to MCO", so we need <Dest='MCO'>
(6)"on 2022-01-03", so we need <FlightDate='2022-01-03'>
Answer: table_name=<flight>, (basic)column_names=<ArrDelay-DepDelay>, conditions=<IATA_Code_Marketing_Airline='DL' AND Flight_Number_Marketing_Airline='1575' AND Origin='ATL' AND Dest='MCO' AND FlightDate='2022-01-03'>
Question: [coffee] What was the opening price of coffee on 2016-12-23?
Framework: SELECT <column_name> FROM <table_name> WHERE <conditions>
Thought: The database related to the question is coffee, so we need table_name=<coffee>. In the question, we are asked 
(1)"the opening price", so we need column_name=<Open>; 
(2)"2016-12-23", so we need conditions=<Date='2016-12-23'>.
Answer: table_name=<coffee>, column_name=<Open>, conditions=<Date='2016-12-23'>
Question: [yelp] What is the average star rating of Chinese businesses in Saint Petersburg?
Framework: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Thought: The database is yelp, the aggregate function is AVG(stars), and we can get the conditions: the categories column contains 'Chinese' and city='Saint Petersburg'
Answer: table_name=<yelp>, (aggregate)column_names=<AVG(stars)>, conditions=<categories LIKE '%Chinese%' AND city='Saint Petersburg'>
Question: [airbnb] How many airbnbs are there in Crown Heights that have a review rate higher than 4?
Framework: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Thought: The database is airbnb, the aggregate function is COUNT(*) and the conditions are: neighbourhood='Crown Heights' and review_rate_number>=4
Answer: table_name=<airbnb>, (aggregate)column_names=<COUNT(*)>, conditions=<neighbourhood='Crown Heights' AND review_rate_number>=4>
"""
TOOL_SQLINTERPRETER3_EXAMPLES = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-03?
Framework: SELECT <(basic)column_names> FROM <table_name> WHERE <conditions>
Association: table_name=<flight>, (basic)column_names=<ArrDelay-DepDelay>, conditions=<IATA_Code_Marketing_Airline='DL' AND Flight_Number_Marketing_Airline='1575' AND Origin='ATL' AND Dest='MCO' AND FlightDate='2022-01-03'>
Answer: SQLInterpreter[SELECT ArrDelay-DepDelay FROM flight WHERE IATA_Code_Marketing_Airline='DL' AND Flight_Number_Marketing_Airline='1575' AND Origin='ATL' AND Dest='MCO' AND FlightDate='2022-01-03']
Question: What was the opening price of coffee on 2016-12-23?
Framework: SELECT <column_name> FROM <table_name> WHERE <conditions>
Association: table_name=<coffee>, column_name=<Open>, conditions=<Date='2016-12-23'>
Answer: SQLInterpreter[SELECT Open FROM coffee WHERE Date='2016-12-23']
Question: What is the average star rating of Chinese businesses in Saint Petersburg?
Framwork: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Association: table_name=<yelp>, (aggregate)column_names=<AVG(stars)>, conditions=<categories LIKE '%Chinese%' AND city='Saint Petersburg'>
Answer: SQLInterpreter[SELECT AVG(stars) FROM yelp WHERE categories LIKE '%Chinese%' and city='Saint Petersburg']
Question: How many airbnbs are there in Crown Heights that have a review rate higher than 4?
Framwork: SELECT <(aggregate)column_names> FROM <table_name> WHERE <conditions>
Association: table_name=<airbnb>, (aggregate)column_names=<COUNT(*)>, conditions=<neighbourhood='Crown Heights' AND review_rate_number>=4>
Answer: SQLInterpreter[SELECT COUNT(*) FROM airbnb WHERE neighbourhood='Crown Heights' and review_rate_number>=4]
"""
TOOL_EXAMPLES_MS = {
    "LoadDB": TOOL_LOADDB_EXAMPLES,
    "FilterDB": TOOL_FILTERDB_EXAMPLES,
    "GetValue": TOOL_GETVALUE_EXAMPLES,
    "LoadGraph": TOOL_LOADGRAPH_EXAMPLES,
    "NodeCheck": TOOL_NODECHECK_EXAMPLES,
    "NeighbourCheck": TOOL_NEIGHBOURCHECK_EXAMPLES,
    "EdgeCheck": TOOL_EDGECHECK_EXAMPLES,
    "RetrieveAgenda": TOOL_RETRIEVEAGENDA_EXAMPLES,
    "RetrieveScirex": TOOL_RETRIEVESCIREX_EXAMPLES,
    "SQLInterpreter": {
        "1": TOOL_SQLINTERPRETER1_EXAMPLES,
        "2": TOOL_SQLINTERPRETER2_EXAMPLES,
        "3": TOOL_SQLINTERPRETER3_EXAMPLES,
    },
    "PythonInterpreter": TOOL_PYTHONINTERPRETER_EXAMPLES,
    "Calculate": TOOL_CALCULATE_EXAMPLES
}
TOOL_EXAMPLES = {
    "LoadDB": TOOL_LOADDB_EXAMPLES,
    "FilterDB": TOOL_FILTERDB_EXAMPLES,
    "GetValue": TOOL_GETVALUE_EXAMPLES,
    "LoadGraph": TOOL_LOADGRAPH_EXAMPLES,
    "NodeCheck": TOOL_NODECHECK_EXAMPLES,
    "NeighbourCheck": TOOL_NEIGHBOURCHECK_EXAMPLES,
    "EdgeCheck": TOOL_EDGECHECK_EXAMPLES,
    "RetrieveAgenda": TOOL_RETRIEVEAGENDA_EXAMPLES,
    "RetrieveScirex": TOOL_RETRIEVESCIREX_EXAMPLES,
    "SQLInterpreter": TOOL_SQLINTERPRETER0_EXAMPLES,
    "PythonInterpreter": TOOL_PYTHONINTERPRETER_EXAMPLES,
    "Calculate": TOOL_CALCULATE_EXAMPLES
}

# ------------------------------------------------------------

# react方法中的fewshots
TOOLQA_EASY8 = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Thought 1: This is a question related to flights. We need to load the flights database.
Action 1: LoadDB[flights]
Observation 1: We have successfully loaded the flights database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings
Thought 2: We need to filter the information related to the query.
Action 2: FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]
Observation 2: We have successfully filtered the data (1 row).
Thought 3: We then need to know the departure delayed time.
Action 3: GetValue[DepDelay]
Observation 3: -7.0
Thought 4: We then need to know the arrival delayed time.
Action 4: GetValue[ArrDelay]
Observation 4: -17.0
Thought 5: To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time.
Action 5: Calculate[(-17)-(-7)]
Observation 5: -10
Thought 6: After calculation, we know that the answer is -10.
Action 6: Finish[-10]

Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
Thought 1: Maybe I can write a python program to solve this problem.
Action 1: PythonInterpreter[# solution in Python:
def solution():
    # Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
    golf_balls_initial = 58
    golf_balls_lost_tuesday = 23
    golf_balls_lost_wednesday = 2
    golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday
    result = golf_balls_left
    return result]
Observation 1: 33
Thought 2: After execution of Python Code, we know that the answer is 33.
Action 2: Finish[33]

Question: What is the corresponding Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task?
Thought 1: The question is asking some performance information about Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task, we need to retrieve some useful information from the scirex database.
Action 1: RetrieveScirex[Mean_IoU score of the FRRN method on Cityscapes dataset for Semantic_Segmentation task]
Observation 1: section : Abstract Semantic image segmentation is an essential component of modern autonomous driving systems , as an accurate understanding of the surrounding scene is crucial to navigation and action planning . Current state - of - the - art approaches in semantic image segmentation rely on pretrained networks that were initially developed for classifying images as a whole . While these networks exhibit outstanding recognition performance ( i.e. , what is visible ? ) , they lack localization accuracy ( i.e. , where precisely is something located ? ) . Therefore , additional processing steps have to be performed in order to obtain pixel - accurate segmentation masks at the full image resolution . To alleviate this problem we propose a novel ResNet - like architecture that exhibits strong localization and recognition performance . We combine multi - scale context with pixel - level accuracy by using two processing streams within our network : One stream carries information at the full image resolution , enabling precise adherence to segment boundaries . The other stream undergoes a sequence of pooling operations to obtain robust features for recognition . The two streams are coupled at the full image resolution using residuals . Without additional processing steps and without pretraining , our approach achieves an intersection - over - union score of 71.8 % on the Cityscapes dataset .
Thought 2: As the approach achieves an intersection - over - union score of 71.8 % on the Cityscapes dataset, the answer should be 71.8%.
Action 2: Finish[71.8%]

Question: When was the paper Learning the Principle of Least Action with Reinforcement Learning. published?
Thought 1: The question is asking some basic information of a dblp paper. We need to load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the published date of a paper, we need to check the node from the PaperNet in DBLP graph.
Action 2: NodeCheck[PaperNet, Learning the Principle of Least Action with Reinforcement Learning.]
Observation 2: {'title': 'Learning the Principle of Least Action with Reinforcement Learning.', 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 0, 'keywords': [], 'doc_type': 'Conference', 'page_start': '', 'page_end': ''}
Thought 3: The published date of the paper is 2021.
Action 3: Finish[2021]

Question: How many collaborators does Chao Zhang have in the DBLP graph?
Thought 1: The question is asking the number of collaborators of a person, we need load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the collaborators of a person, we need to check the neighboring nodes from the AuthorNet in DBLP graph.
Action 2: NeighbourCheck[AuthorNet, Chao Zhang]
Observation 2: ['YUHUI YUAN', 'Rao Fu', 'Lang Huang', 'Weihong Lin', 'X Chen', 'Jingdong Wang']
Thought 3: The number of collaborators of Chao Zhang is 6.
Action 3: Finish[6]

Question: How many papers does Chao Zhang and Weihong Lin have in common in the DBLP graph?
Thought 1: The question is asking the number of common papers of two persons, we need load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: The question is asking the common papers of two persons, we need to check the edges between them from the PaperNet in DBLP graph.
Action 2: EdgeCheck[PaperNet, Chao Zhang, Weihong Lin]
Observation 2: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Thought 3: The number of common papers of Chao Zhang and Weihong Lin is 1.

Question: Where did Stephen's Opera performance take place?
Thought 1: The question is asking the location of Stephen's Opera performance from agenda.
Action 1: RetrieveAgenda[Stephen's Opera performance]
Observation 1: On January 29, 2022, there will be an opera performance at the Lyric Opera House, featuring Stephen. The show will start at 7:00 PM and end at 9:00 PM. It promises to be a wonderful evening of beautiful music and powerful performances in a stunning venue. Come and experience the magic of opera at its finest!
Thought 2: The event happened in Lyric Opera.
Action 2: Finish[Lyric Opera]

Question: What was the trading volume of coffee on 2000-01-14?
Thought 1: Maybe I can write a SQL query to solve this problem.
Action 1: SQLInterpreter(SELECT Volume FROM coffee.coffee_data WHERE Date = '2000-01-14';
Observation 1: Volume: 10115
Thought 2: The volume of coffee on 2000-01-14 is 10115.
Action 2: Finish[10115]
"""

TOOLQA_HARD3 = """Question: What is the average airtime of the flights from PHX to LGA host by Spirit Air Lines?
Thought 1: This is a question related to flights. We need to load the flights database.
Action 1: LoadDB[flights]
Observation 1: We have successfully loaded the flights database, including the following columns: FlightDate, Airline, Origin, Dest, Cancelled, Diverted, CRSDepTime, DepTime, DepDelayMinutes, DepDelay, ArrTime, ArrDelayMinutes, AirTime, CRSElapsedTime, ActualElapsedTime, Distance, Year, Quarter, Month, DayofMonth, DayOfWeek, Marketing_Airline_Network, Operated_or_Branded_Code_Share_Partners, DOT_ID_Marketing_Airline, IATA_Code_Marketing_Airline, Flight_Number_Marketing_Airline, Operating_Airline, DOT_ID_Operating_Airline, IATA_Code_Operating_Airline, Tail_Number, Flight_Number_Operating_Airline, OriginAirportID, OriginAirportSeqID, OriginCityMarketID, OriginCityName, OriginState, OriginStateFips, OriginStateName, OriginWac, DestAirportID, DestAirportSeqID, DestCityMarketID, DestCityName, DestState, DestStateFips, DestStateName, DestWac, DepDel15, DepartureDelayGroups, DepTimeBlk, TaxiOut, WheelsOff, WheelsOn, TaxiIn, CRSArrTime, ArrDelay, ArrDel15, ArrivalDelayGroups, ArrTimeBlk, DistanceGroup, DivAirportLandings
Thought 2: We need to filter the information related to the query.
Action 2: FilterDB[Origin=PHX, Dest=ATL, Airline=Spirit Air Lines]
Observation 2: We have successfully filtered the data (16 rows).
Thought 2: We then obtain all the AirTime values of filtered records.
Action 2: GetValue[AirTime]
Observation 2: [247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, nan, 229.0, nan, 259.0, 253.0]
Thought 3: We then calculate the average of the values. NaN values are ignored.
Action 3: Calculate(mean(247.0, 253.0, 230.0, 264.0, 254.0, 275.0, 227.0, 258.0, 245.0, 253.0, 242.0, 229.0, 259.0, 253.0))
Observation 3: 249.214
Thought 4: The average airtime of the flights from PHX to LGA host by Spirit Air Lines is 249.2.
Action 4: Finish[249.2]

Question: Can you recommend a Guamanian business with the highest star rating within a 5-mile radius of 6830 Rising Sun Ave?
Thought 1: This is a question related to business. We need to load the yelp database.
Action 1: LoadDB[yelp]
Observation 1: We have successfully loaded the yelp database, including the following columns: business_id, name, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, attributes, categories, hours
Thought 2: Maybe we can write SQL code to obtain the latitude and longitude of the address.
Action 2: SQLInterpreter[SELECT latitude, longitude FROM yelp.yelp_data WHERE address='6830 Rising Sun Ave']  
Observation 2: latitude: 40.05555, longitude: -75.090723 
Thought 3: Maybe we can write another python code to calculate the coordinates range of 5-mile radius.
Action 3: import geopy\nimport geopy.distance\nlatitude = 40.05555\nlongitude = -75.090723\n_, lo_max, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=90)\n_, lo_min, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=270)\nla_max, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=0)\nla_min, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=180)\nans = (la_max, la_min, lo_max, lo_min)
Observation 3: (40.10058038657396, 40.010519262352226, -75.03212327463275, -75.14932272536724)
Thought 4: We then filter the information related to the query in the yelp database.
Action 4: FilterDB[latitude>=40.010519262352226, longitude>=-75.14932272536724, latitude<=40.10058038657396, longitude<=-75.03212327463275, categories=Guamanian]
Observation 4: We have successfully filtered the data (2 rows).
Thought 5: We then obtain all the stars values of filtered records.
Action 5: GetValue[stars]
Observation 5: [4.0, 4.5]
Thought 6: The highest star rating is 4.5. Select the business with the highest star rating.
Action 6: FilterDB[stars=4.5]
Observation 6: We have successfully filtered the data (1 row).
Thought 7: Get the corresponding name.
Action 7: GetValue[name]
Observation 7: Damaso Painting
Thought 8: The business with the highest star rating is Damaso Painting.
Action 8: Finish[Damaso Painting]

Question: What venue does Chao Zhang with his collarborator publish paper on?
Thought 1: This is a question related to DBLP. We need to load the DBLP graph.
Action 1: LoadGraph[dblp]
Observation 1: DBLP graph is loaded.
Thought 2: We need to check the neighbouring nodes of Chao Zhang in AuthorNet.
Action 2: NeighbourCheck[AuthorNet, Chao Zhang]
Observation 2: Weihong Lin
Thought 3: We need to check the between Chao Zhang and Weihong Lin to check their collaboration.
Action 3: EdgeCheck[AuthorNet, Chao Zhang, Weihong Lin]
Observation 3: {'weight': 1, 'papers': ['HRFormer: High-Resolution Vision Transformer for Dense Predict.'], 'n_citation': [95]}
Thought 4: We need to check the paper detail in the node feature from PaperNet they published.
Action 4: NodeCheck[PaperNet, HRFormer: High-Resolution Vision Transformer for Dense Predict.]
Observation 4: {'title': 'HRFormer: High-Resolution Vision Transformer for Dense Predict.', 'year': 2021, 'venue': {'raw': 'AAAI Spring Symposium - MLPS'}, 'n_citation': 0, 'keywords': [], 'doc_type': 'Conference', 'page_start': '', 'page_end': ''}
Thought 5: The paper is published on AAAI Spring Symposium - MLPS.
Action 5: Finish[AAAI Spring Symposium - MLPS]
"""
COTQA_SIMPLE6 = """Question: How many extra minutes did the DL1575 flight take from ATL to MCO on 2022-01-12?
Let's think step by step. I need to first load the flights database with LoadDB[flights]. And then, I need to filter the information I want according to the query with FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]. Then, I need to get the value of the departure time from the database with GetValue[DepDelay]. We then need to know the arrival delayed time with GetValue[ArrDelay]. To compute the extra minutes, we need to subtract the departure delayed time from the arrival delayed time with Calculate[(-17)-(-7)].  After calculation, we know that the answer is -10.
Action 1: LoadDB[flights]-->FilterDB[Flight_Number_Marketing_Airline=1575, FlightDate=2022-01-12, Origin=ATL, Dest=MCO]-->GetValue[DepDelay]-->GetValue[ArrDelay]-->Calculate[(-17)-(-7)]-->Finish[-10]
"""
COT = """
"""

COT_REFLECT = """
"""

REFLECTIONS = """
"""