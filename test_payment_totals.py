#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests simples pour la fonction calculate_payment_totals.
"""

import sys
sys.path.insert(0, '/home/runner/work/ClubManager/ClubManager')

from club_manager.core.utils import calculate_payment_totals

def test_empty_list():
    """Test avec une liste vide."""
    result = calculate_payment_totals([])
    assert result == {'total': 0.0, 'cash': 0.0, 'checks': 0.0, 'ancv': 0.0}
    print("✓ Test liste vide réussi")

def test_single_member():
    """Test avec un seul membre."""
    members = [{
        'cash_amount': 10.0,
        'check1_amount': 20.0,
        'check2_amount': 30.0,
        'check3_amount': 0.0,
        'ancv_amount': 5.0
    }]
    result = calculate_payment_totals(members)
    assert result['cash'] == 10.0
    assert result['checks'] == 50.0  # 20 + 30 + 0
    assert result['ancv'] == 5.0
    assert result['total'] == 65.0  # 10 + 50 + 5
    print("✓ Test membre unique réussi")

def test_multiple_members():
    """Test avec plusieurs membres."""
    members = [
        {
            'cash_amount': 10.0,
            'check1_amount': 20.0,
            'check2_amount': 0.0,
            'check3_amount': 0.0,
            'ancv_amount': 5.0
        },
        {
            'cash_amount': 15.0,
            'check1_amount': 25.0,
            'check2_amount': 10.0,
            'check3_amount': 5.0,
            'ancv_amount': 0.0
        }
    ]
    result = calculate_payment_totals(members)
    assert result['cash'] == 25.0  # 10 + 15
    assert result['checks'] == 60.0  # (20 + 0 + 0) + (25 + 10 + 5)
    assert result['ancv'] == 5.0  # 5 + 0
    assert result['total'] == 90.0
    print("✓ Test membres multiples réussi")

def test_null_values():
    """Test avec des valeurs nulles."""
    members = [{
        'cash_amount': None,
        'check1_amount': None,
        'check2_amount': 20.0,
        'check3_amount': None,
        'ancv_amount': None
    }]
    result = calculate_payment_totals(members)
    assert result['cash'] == 0.0
    assert result['checks'] == 20.0
    assert result['ancv'] == 0.0
    assert result['total'] == 20.0
    print("✓ Test valeurs nulles réussi")

def test_string_to_float_conversion():
    """Test conversion de chaînes en float."""
    members = [{
        'cash_amount': '10.50',
        'check1_amount': '20.75',
        'check2_amount': 0,
        'check3_amount': 0,
        'ancv_amount': '5.25'
    }]
    result = calculate_payment_totals(members)
    assert result['cash'] == 10.50
    assert result['checks'] == 20.75
    assert result['ancv'] == 5.25
    assert result['total'] == 36.50
    print("✓ Test conversion string->float réussi")

def test_rounding():
    """Test de l'arrondi à 2 décimales."""
    members = [{
        'cash_amount': 10.123,
        'check1_amount': 20.456,
        'check2_amount': 0,
        'check3_amount': 0,
        'ancv_amount': 5.789
    }]
    result = calculate_payment_totals(members)
    assert result['cash'] == 10.12
    assert result['checks'] == 20.46
    assert result['ancv'] == 5.79
    # Total: 10.123 + 20.456 + 5.789 = 36.368, arrondi à 36.37
    assert result['total'] == 36.37
    print("✓ Test arrondi réussi")

if __name__ == '__main__':
    print("Exécution des tests pour calculate_payment_totals...")
    test_empty_list()
    test_single_member()
    test_multiple_members()
    test_null_values()
    test_string_to_float_conversion()
    test_rounding()
    print("\n✅ Tous les tests sont passés avec succès!")
