# -*- coding: utf-8 -*-
from club_manager.core.utils import is_email_valid, is_phone_valid, format_currency, safe_str

def test_is_email_valid():
    assert is_email_valid("foo@bar.com")
    assert not is_email_valid("foo@bar")
    assert not is_email_valid("foo.com")

def test_is_phone_valid():
    assert is_phone_valid("0601020304")
    assert is_phone_valid("06-01-02-03-04")
    assert not is_phone_valid("1234")

def test_format_currency():
    assert format_currency(10) == "10.00 €"
    assert format_currency("abc") == "abc"

def test_safe_str():
    assert safe_str(123) == "123"
    assert isinstance(safe_str(object()), str)