import pandas as pd
import jsonlines
import json
import re
import sys

class table_toolkits():
    # init
    def __init__(self, path):
        self.data = None
        self.backup_data = None
        self.path = path
        self.db = ''

    def db_loader(self, target_db):
        if target_db == 'flight': target_db = 'flights' # target db name can be 'flight'
        if target_db != self.db:
            self.db = target_db
            if target_db == 'flights':
                file_path = "{}/data/external_corpus/flights/Combined_Flights_2022.csv".format(self.path)
                self.data = pd.read_csv(file_path)
            elif target_db == 'coffee':
                file_path = "{}/data/external_corpus/coffee/coffee_price.csv".format(self.path)
                self.data = pd.read_csv(file_path)
            elif target_db =='airbnb':
                file_path = "{}/data/external_corpus/airbnb/Airbnb_Open_Data.csv".format(self.path)
                self.data = pd.read_csv(file_path, low_memory=False)
            elif target_db == 'yelp':
                data_file = open("{}/data/external_corpus/yelp/yelp_academic_dataset_business.json".format(self.path))
                data = []
                for line in data_file:
                    data.append(json.loads(line))
                self.data = pd.DataFrame(data)
                data_file.close()
            else:
                raise ValueError(f"Wrong database name: {target_db}")
            self.data = self.data.astype(str)
            self.backup_data = self.data
        else:
            self.data = self.backup_data

        column_names = ', '.join(self.data.columns.tolist())
        return "We have successfully loaded the {} database, including the following columns: {}.".format(target_db, column_names)

    # def get_column_names(self, target_db):
    #     return ', '.join(self.data.columns.tolist())

    def data_filter(self, argument):
        # commands = re.sub(r' ', '', argument)
        # backup_data = self.data
        argument = argument.replace("'","").replace('"','')
        commands = argument.split(', ')
        
        for i in range(len(commands)):
            try:
                # commands[i] = commands[i].replace(' ', '')
                if '>=' in commands[i]:
                    command = commands[i].split('>=')
                    column_name = command[0]
                    value = command[1]
                    self.data = self.data[self.data[column_name] >= value]
                elif '<=' in commands[i]:
                    command = commands[i].split('<=')
                    column_name = command[0]
                    value = command[1]
                    self.data = self.data[self.data[column_name] <= value]
                elif '>' in commands[i]:
                    command = commands[i].split('>')
                    column_name = command[0]
                    value = command[1]
                    self.data = self.data[self.data[column_name] > value]
                elif '<' in commands[i]:
                    command = commands[i].split('<')
                    column_name = command[0]
                    value = command[1]
                    self.data = self.data[self.data[column_name] < value]
                elif '=' in commands[i]:
                    command = commands[i].split('=')
                    column_name = command[0]
                    value = command[1]
                    self.data = self.data[self.data[column_name] == value]
                if len(self.data) == 0:
                    self.data = self.backup_data
                    return "The filtering query {} is incorrect. Please modify the condition.".format(commands[i])
            except Exception as e:
                print(e)
                return "we have failed when conducting the {} command. Please make changes.".format(commands[i])
        current_length = len(self.data)
        if len(self.data) > 0:
            return "We have successfully filtered the data ({} rows).".format(current_length)
        else:
            # convert to strings, with comma as column separator and '\n' as row separator
            return_answer = []
            for i in range(len(self.data)):
                outputs = []
                for attr in list(self.data.columns):
                    outputs.append(str(attr)+": "+str(self.data.iloc[i][attr]))
                outputs = ', '.join(outputs)
                return_answer.append(outputs)
            return_answer = '\n'.join(return_answer)
            return return_answer

    def get_value(self, argument):
        column = argument
        if len(self.data) == 1:
            return str(self.data.iloc[0][column])
        else:
            # modified: START
            tmp = self.data[column].tolist()
            if sys.getsizeof(tmp) > 1024:    # do not display data bigger than 1k
                return "An Error Occurred: Too Many Values to Display."
            # modified: END
            return ', '.join(self.data[column].tolist())

if __name__ == "__main__":
    db = table_toolkits("toolqa_data")
    print(db.db_loader('flights'))
    print(db.data_filter('IATA_Code_Marketing_Airline=AA, Flight_Number_Marketing_Airline=5647, Origin=BUF, Dest=PHL, FlightDate=2022-04-20'))
    print(db.get_value('DepTime'))