"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime
import pytest 


class  WrongFormatException(Exception):
    """WrongFormatException"""
    pass

def calculate_days(from_date: str) -> int:
    try:
        date=datetime.strptime(from_date, '%Y-%m-%d')
    except:
        raise WrongFormatException('WrongFormatException')
    
    now=datetime.now()
    diference = now - date
    return diference.days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

@pytest.fixture
def moving_date(freezer):
    return freezer.move_to('2021-10-06')

def test_wrong_format():
    with pytest.raises(WrongFormatException) as e:
        calculate_days('10-07-2021')
    assert 'WrongFormatException' in str(e.value)


def test_date_future(moving_date):
    assert calculate_days('2021-10-07') == -1

def test_date_past(moving_date):
    assert calculate_days('2021-10-05') == 1


