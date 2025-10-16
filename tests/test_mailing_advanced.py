# -*- coding: utf-8 -*-
from club_manager.core.mailing_advanced import personalize_template, select_recipients

def test_personalize_template():
    template = "Bonjour {prenom} {nom} !"
    context = {"prenom": "Marie", "nom": "Dupont"}
    msg = personalize_template(template, context)
    assert msg == "Bonjour Marie Dupont !"

def test_select_recipients():
    members = [
        {"last_name": "A", "status": "Payé"},
        {"last_name": "B", "status": "En attente"},
    ]
    sel = select_recipients(members, {"status": "Payé"})
    assert len(sel) == 1 and sel[0]["last_name"] == "A"