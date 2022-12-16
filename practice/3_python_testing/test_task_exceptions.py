"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""
import importlib
import pytest 
module = importlib.import_module('.task_exceptions', 'practice.2_python_part_2')
division = module.division
DivisionByOneException = module.DivisionByOneException

def test_division_ok(capfd):
    value=division(6,2)
    out, err = capfd.readouterr()
    assert value == 3
    assert out ==  "Division finished\n"

def test_division_by_zero(capfd):
    value=division(1,0)
    out, err = capfd.readouterr()
    assert value == None 
    assert out ==  "Division by 0\nDivision finished\n"

def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException) as e:
        division(1,1)
    out, err = capfd.readouterr()
    assert 'Deletion on 1 get the same result' in str(e.value)
    assert out ==  "Division finished\n"
