"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math
import pytest 

class OperationNotFoundException(Exception):
    """OperationNotFoundException"""
    pass


def math_calculate(function: str, *args):
    try:
        function = getattr(math, function)
        if(len(args)>2):
            return
        if(len(args)==1):
            a=float(args[0])
            return function(a)
        else:
            a,b=args
            return function(a,b)
    except:
        raise OperationNotFoundException('OperationNotFoundException')

"""
Write tests for math_calculate function
"""

def test_one_argument_operation():
    assert math_calculate('ceil', 10.7)==11

def test_two_arguments_operatio():
    assert math_calculate('log', 1024, 2) == 10.0

def test_OperationNotFoundException():
    with pytest.raises(OperationNotFoundException) as e:
        math_calculate('test', [1024, 2])
    assert 'OperationNotFoundException' in str(e.value)

    



