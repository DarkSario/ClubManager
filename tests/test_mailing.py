# -*- coding: utf-8 -*-
import pytest
from club_manager.core.mailing import send_mailing

def test_send_mailing(monkeypatch):
    smtp_calls = []
    class DummySMTP:
        def __init__(self, host, port): pass
        def starttls(self): pass
        def login(self, user, password): pass
        def sendmail(self, from_, to, msg): smtp_calls.append((from_, to, msg))
        def __enter__(self): return self
        def __exit__(self, *a): pass
    monkeypatch.setattr("smtplib.SMTP", DummySMTP)
    send_mailing(
        "Sujet test", "Message test",
        ["foo@bar.com"], {"from": "me@bar.com", "host": "localhost"},
        parent=None
    )
    assert smtp_calls