# -*- coding: utf-8 -*-
import pandas as pd
from club_manager.core.export import export_members_csv

def test_export_members_csv(tmp_path):
    members = [
        {"last_name": "Dupont", "first_name": "Marie"},
        {"last_name": "Durand", "first_name": "Paul"},
    ]
    outfile = tmp_path / "out.csv"
    pd.DataFrame(members).to_csv(outfile, index=False, encoding="utf-8")
    df = pd.read_csv(outfile)
    assert list(df["last_name"]) == ["Dupont", "Durand"]