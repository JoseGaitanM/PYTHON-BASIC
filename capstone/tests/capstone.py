import argparse
import datetime
import logging
import random 
import uuid
import sys 
import os
import json
import random
from random import randint as rand
import multiprocessing
import time 




class Cli:
    def __init__(self,argv=None):
        self.DEFAULT_DIRECTORY = './'
        self.DEFAULT_FILE_NAME = 'file'
        self.p = multiprocessing.Pool()
        self.parser = argparse.ArgumentParser(description='Capstone')

        self.parser.add_argument('-p', '--path_to_save_files', type=str, default=self.DEFAULT_DIRECTORY, 
                            action='store', help='Where all files need to save')
                            
        self.parser.add_argument('-fc', '--file_count', type=int, default=1, 
                            action='store', help='How much json files to generate')

        self.parser.add_argument('-fn', '--file_name', type=str, default=self.DEFAULT_FILE_NAME, 
                            action='store', help='Base file name')

        self.parser.add_argument('-fp', '--prefix', type=str, default='count', 
                            action='store', help='What prefix for file name to use', choices=['count', 'random', 'uuid'])

        self.parser.add_argument('-ds', '--data_schema', type=str, 
                            action='store', help='Its a string with json schema',required=True)

        self.parser.add_argument('-dl', '--data_line', type=int, default=1000, 
                            action='store', help='Count of lines for each file')


        self.parser.add_argument('-cp', '--clear_path', default=True, 
                            action='store', help='''If this flag is on, before the script starts creating 
                                                new data files, all files in path_to_save_files that match file_name 
                                                will be deleted.''')

        self.parser.add_argument('-mp', '--multiprocessing', type=int, default=1, 
                            action='store', help='The number of processes used to create files.', nargs=1)

        self.args = self.parser.parse_args(argv)

    def clear_path(self):
        if(self.args.clear_path=='True'):
            dir_list = os.listdir(self.args.path_to_save_files)
            for x in dir_list:
                if self.args.file_name in x:
                    os.remove(self.args.path_to_save_files+'/'+x)


    def get_time(self):
        return datetime.datetime.now().timestamp()

    def validate_path_to_save_files(self):
        if not os.path.exists(self.args.path_to_save_files):
            logging.error("The path to save the files does not exits")
            sys.exit(1)
        else:
            if not os.path.isdir(self.args.path_to_save_files):
                logging.error("The path is not a dir")
                sys.exit(1)

    def validate_file_count(self):
        if self.args.file_count < 0:
            logging.error("The number of files can not be negative")
            sys.exit(1)

    def validate_multiprocessing(self):
        if self.args.multiprocessing[0] < 0 :
            logging.error("Multiprocessings must be a positive number.")
            sys.exit(1)
        if self.args.multiprocessing[0] > os.cpu_count(): 
            self.args.multiprocessing[0] = os.cpu_count()
            self.p = multiprocessing.Pool(processes=self.args.multiprocessing[0])
        return True

    def create_file_name(self):
        names=[]
        name=self.args.file_name+'_'
        prefix=self.args.prefix
        file_count=self.args.file_count

        for i in range(0,int(file_count)):
            if(prefix=='count'):
                names.append(name+str(i))
            elif(prefix=='random'):
                names.append(name+str(random.random())[3:])
            elif(prefix=='uuid'):
                names.append(name+str(uuid.uuid4()))

        return names


    def validate_data_schema(self):
        schema = ''

        try:
            schema = json.loads(self.args.data_schema)
        except:
            if not os.path.isfile(self.args.data_schema):
                logging.error("The file for import the data_schema does not exits")
                sys.exit(1)
            else:
                try:
                    file = open(self.args.data_schema)
                    schema = json.load(file)
                except:
                    logging.error("The content of the file for import the data_schema is not valid")
                    sys.exit(1)
        return schema

    def get_eval(self,statement,list,type_val,complete):
        try:
            if(type_val=='str'):
                statement=str(statement)
            elif(type_val=='int'):
                statement=int(statement)
            if complete:
                return str(type(eval(statement))) in list
            else:
                return str(type(statement)) in list
        except:
            return False 
        

    def get_randint(self,statement):
        try:
            if(statement[0:5]+statement[-1]=='rand()'):
                return True
        except:
            return False 
        return False

    def generate_data_lines(self,list,key,statement):
        for i in range(0,self.args.data_line):
            list[i][key]=eval(statement)
        return list

    def generate_data_lines_const(self,list,key,statement):
        for i in range(0,self.args.data_line):
            list[i][key]=statement
        return list

    def generate_data(self,schema):
        instruccions=[]
        
        for x in schema:
            values=schema[x].split(':')

            if(len(values)>1 and values[1]!=''):
                if(values[0] == 'str'):
                    if(values[1]=='rand'):
                        instruccions.append([x,'str(uuid.uuid4())'])
                    elif self.get_eval(values[1],["<type 'list'>","<class 'list'>"],'str',True):
                        instruccions.append([x,'str(random.choice(eval(str({}))))'.format(values[1])])
                    elif self.get_eval(values[1],["<type 'str'>","<class 'str'>"],'str',False):
                        instruccions.append([x,values[1],False])

                elif(values[0] == 'int'):
                    if(values[1]=='rand'):
                        instruccions.append([x,'random.randint(0, 10000)'])
                    elif self.get_randint(values[1]):
                        instruccions.append([x,str(values[1])])
                    elif self.get_eval(values[1],["<type 'list'>","<class 'list'>"],'str',True):
                        instruccions.append([x,'int(random.choice(eval(str({}))))'.format(values[1])])
                    elif (self.get_eval(values[1],["<type 'int'>","<class 'int'>"],'int',False)):
                        instruccions.append([x,int(values[1]),False])
                elif(values[0]=='timestamp'):
                    instruccions.append([x,time.time(),False])  
                else:
                    logging.error("Error in {} : {}".format(x,schema[x]))
                    sys.exit(1)    
            else:
                if self.get_eval(values[0],["<type 'list'>","<class 'list'>"],'str',True):
                    instruccions.append([x,'str(random.choice(eval(str({}))))'.format(values[0])])
                elif(values[0]=='str'):
                    instruccions.append([x,'',False])
                elif(values[0]=='int'):
                    instruccions.append([x,None,False])
                elif(values[0]=='timestamp'):
                    instruccions.append([x,time.time(),False])
                else:
                    logging.error("Error in {} : {}".format(x,schema[x]))
                    sys.exit(1)

        names=self.create_file_name()
        result=[]
        
        lines=[]

        if(len(names)>0):
            for i in range(len(names)):
                result.append([names[i],instruccions])
            for i in range(int(self.args.file_count)):
                self.p.apply_async(lines.append(self.writeData(result[i])))
        else:
            text=self.generate_content_file(instruccions)
            print(text)
            lines.append(text)
        
        return lines

    def generate_content_file(self,instruccions):
        result=[]

        for _ in range(0,self.args.data_line):
            result.append({})

        for instruccion in instruccions:
            if(len(instruccion)==2):
                result=self.generate_data_lines(result,instruccion[0],instruccion[1])
            else:
                result=self.generate_data_lines_const(result,instruccion[0],instruccion[1])
        return result

    def writeData(self,data):
        result=[]
        file = open(self.args.path_to_save_files+data[0]+'.json','w')
        
        logging.info("Creting the file {}".format(str(data[0])))
        print("Creting the file {}".format(str(data[0])))
        result=self.generate_content_file(data[1])

        json_object = json.dumps(result, indent=4)
        file.write(json_object)
        
        logging.info("File {} Done!".format(str(data[0])))
        print("File {} Done!".format(str(data[0])))
        return result
        
    def validate(self):
        self.validate_multiprocessing()
        self.validate_path_to_save_files()
        self.validate_file_count()
        self.clear_path()
        schema=self.validate_data_schema()
        result=self.generate_data(schema)
        return result

if __name__ == "__main__":
    cli_object = Cli()
    cli_object.validate()