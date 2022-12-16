"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
import importlib
module = importlib.import_module('.task_input_output', 'practice.2_python_part_2')
read_numbers = module.read_numbers
from unittest.mock import patch


@patch('builtins.input', side_effect=['1', '2', '3','4'])
def test_read_numbers_without_text_input(self):
    assert read_numbers(4) == 'Avg: 2.5'

@patch('builtins.input', side_effect=['text', 'hello', 'bye','cat'])
def test_read_numbers_with_text_input(self):
    assert read_numbers(4) == 'No numbers entered'
