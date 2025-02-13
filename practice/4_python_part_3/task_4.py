"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
from faker import Faker
from unittest.mock import patch 


def print_name_address() -> None:
    dic = {}

    parser = argparse.ArgumentParser()
    parser.add_argument("number",type=int)
    parser.add_argument("--data", nargs='+')
    args = parser.parse_args()

    for item in args.data:
        i = item.split('=')
        dic[i[0]] = i[1]

    return create_faker(dic,args.number)
    

def create_faker(dic,n):
    fake=Faker()
    answer=[]
    result = {}

    for i in range(0,n):
        for i in range(n):
            
            for key, value in dic.items():
                fake_val = getattr(fake, value)
                result[key] = fake_val()
        print(str(result))
        answer.append(result)
    return answer


"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""

#We test the creation of the dictionaries base on the given args
@patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(number=4, data=['--fake-address=address','--some_name=name']))
def test_print_name_address(mock_args):
    result=print_name_address()
    assert len(result)==4
    

def test_create_faker():
    #With seed we make sure that faker returns the expected value
    Faker.seed(10)
    dict = {'--fake-address':'address','--some_name':'name'}
    expected_result=[
        {'--fake-address': '9037 Colon Shoal Apt. 087\nCharlesstad, AZ 55603', '--some_name': 'Lindsey James'}]
    result=create_faker(dict,1)

    assert expected_result==result
