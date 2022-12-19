"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""
import re
import pytest 


def is_http_domain(domain: str) -> bool:
    val = re.search("^http:|https:.*/$", domain)
    if val:
        return True
    else:
        return False


"""
write tests for is_http_domain function
"""

def test_http_domain():
    assert is_http_domain('http://wikipedia.org') == True

def test_https_domain():
    assert is_http_domain('https://ru.wikipedia.org/') == True

def test_fake_domain():
    assert is_http_domain('griddynamics.com') == False