import pytest
from capstone import Cli
import uuid
from pathlib import Path
import json 
import os

def cli_mock(index):
    return Cli(index)

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def is_valid_datetime(val):
    return str(type(val)) == "<class 'float'>" or "<type 'float'>"

def is_valid_rand(f,to,value):
    if value in range(f,to+1):
        return True

def is_in_list(value,list):
    if value in list:
        return True

def valid_stand_alone(value,expected):
    return value==expected

def is_valid_empty_value(value,type):
    if(type=='str'):
        return value==''
    elif(type=='int'):
        return value==None

@pytest.fixture
def file(tmpdir):
    d = tmpdir.mkdir("sub")
    p = d.join('temp_file.json')
    dictionary = {"date":"timestamp:","name":"str:rand","type":"['client', 'partner', 'government']" ,"age":"int:rand(1, 90)"}
    json_object = json.dumps(dictionary, indent = 4) 
    p.write(json_object)
    return d

@pytest.mark.parametrize("index,expected", [(["--path_to_save_files","./result/", "--file_count","10","--file_name","super_data","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema","{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\" , \"age\": \"int:rand(1, 90)\"}"],True)])
def test_data_types(index, expected):
    cli_object = cli_mock(index)
    result = cli_object.validate()

    for lines in result:
        for dic in lines:
            assert is_valid_datetime(dic['date'])
            assert is_valid_uuid(dic['name'])
            assert is_in_list(dic['type'],['client', 'partner', 'government'])
            assert is_valid_rand(1,90,dic['age'])

@pytest.mark.parametrize("index,expected", [(["--path_to_save_files","./result/", "--file_count","10","--file_name","super_data","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema","{\"name\": \"str:Jose\",\"IVA\": \"int:\",\"Service\": \"['food', 'clothes', 'delivery']\" , \"cost\": \"int:rand(1, 90)\"}"],True)])
def test_schema(index, expected):
    cli_object = cli_mock(index)
    result = cli_object.validate()
    
    for lines in result:
        for dic in lines:
            assert valid_stand_alone(dic['name'],'Jose')
            assert is_valid_empty_value(dic['IVA'],'int')
            assert is_in_list(dic['Service'],['food', 'clothes', 'delivery'])
            assert is_valid_rand(1,90,dic['cost'])

def test_temporary_json(file):
    f=str(file.join('temp_file.json'))

    cli_object = cli_mock(
        ["--path_to_save_files",f"{str(file)}", "--file_count","10","--file_name","testing_file","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema",f"{f}"]
    )

    result = cli_object.validate()
    
    for lines in result:
        for dic in lines:
            assert is_valid_datetime(dic['date'])
            assert is_valid_uuid(dic['name'])
            assert is_in_list(dic['type'],['client', 'partner', 'government'])
            assert is_valid_rand(1,90,dic['age'])

def test_for_clear_path(file):
    f=str(file)
    cli_object = cli_mock(
        ["--path_to_save_files",f"{f}", "--file_count","10","--file_name","temp_file","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema",f"{f}"]
    )

    cli_object.clear_path()
    dir_list = os.listdir(str(file))
    assert len(dir_list)==0

def test_check_saving_files_disk(file):
    f=str(file)
    
    cli_object = cli_mock(
        ["--path_to_save_files",f"{f}", "--file_count","10","--file_name","temp_file","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema",f"{f}"]
    )

    data=['/testing_file',[]]

    cli_object.writeData(data)

    dir_list = os.listdir(str(file))
    assert 'testing_file.json' in dir_list

def test_number_created_files(file):
    f=str(file)+'/'
    
    cli_object = cli_mock(
        ["--path_to_save_files",f"{f}", "--file_count","10","--file_name","temp_file","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema","{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\" , \"age\": \"int:rand(1, 90)\"}"]
    )

    result = cli_object.validate()

    dir_list = os.listdir(f)
    assert len(dir_list)==10

def test_data_lines(file):
    f=str(file)+'/'
    
    cli_object = cli_mock(
        ["--path_to_save_files",f"{f}", "--file_count","10","--file_name","temp_file","--prefix","uuid","--data_line","20","--clear_path","True","--multiprocessing","4","--data_schema","{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\" , \"age\": \"int:rand(1, 90)\"}"]
    )

    result = cli_object.validate() 
    
    assert len(result[0]) == 20

