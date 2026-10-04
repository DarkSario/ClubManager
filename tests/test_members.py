# -*- coding: utf-8 -*-
"""Tests de la gestion des membres."""

import pytest

from club_manager.core import members


def _add(last="Dupont", first="Jean", **kw):
    members.add_member(last_name=last, first_name=first, **kw)


def test_add_and_get_all(db):
    _add()
    _add("Martin", "Paul")
    assert len(members.get_all_members()) == 2


def test_get_by_id(db):
    _add()
    mid = members.get_all_members()[0]["id"]
    assert members.get_member_by_id(mid)["last_name"] == "Dupont"
    assert members.get_member_by_id(9999) is None


def test_update(db):
    _add()
    mid = members.get_all_members()[0]["id"]
    members.update_member(mid, city="Lyon")
    assert members.get_member_by_id(mid)["city"] == "Lyon"


def test_delete(db):
    _add()
    mid = members.get_all_members()[0]["id"]
    members.delete_member(mid)
    assert members.get_all_members() == []


def test_filters(db):
    _add("Dupont", "Jean", city="Lyon", rgpd=1)
    _add("Martin", "Paul", city="Paris", rgpd=0)
    assert len(members.get_filtered_members({})) == 2
    assert len(members.get_filtered_members(None)) == 2
    assert [m["last_name"] for m in members.get_filtered_members({"city": "ly"})] == ["Dupont"]
    assert [m["last_name"] for m in members.get_filtered_members({"rgpd": 0})] == ["Martin"]
    assert len(members.get_filtered_members({"city": "a", "rgpd": 1})) == 0


def test_unknown_column_rejected(db):
    with pytest.raises(ValueError):
        members.add_member(**{"last_name) VALUES ('x'); DROP TABLE members; --": 1})
    _add()
    with pytest.raises(ValueError):
        members.update_member(1, bogus="x")
