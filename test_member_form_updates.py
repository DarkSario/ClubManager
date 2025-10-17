#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour valider les modifications du formulaire de membre et la gestion des tarifs.
"""

import sys
import os
from pathlib import Path
import tempfile

# Ajouter le répertoire parent au path pour pouvoir importer club_manager
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from club_manager.core.database import Database
from club_manager.core.members import add_member, get_all_members, get_member_by_id, update_member, delete_member
from club_manager.core.annual_prices import add_annual_price, get_all_annual_prices, get_current_annual_price, update_annual_price

def test_member_payment_fields():
    """Test des nouveaux champs de paiement du formulaire membre."""
    print("\nTest 1: Nouveaux champs de paiement...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Ajouter un membre avec tous les champs de paiement
        add_member(
            last_name='Martin',
            first_name='Sophie',
            address='10 Avenue Test',
            postal_code='69001',
            city='Lyon',
            phone='0687654321',
            mail='sophie.martin@test.fr',
            rgpd=1,
            image_rights=1,
            payment_type='club_mjc',
            ancv_amount=15.0,
            cash_amount=75.0,
            check1_amount=50.0,
            check2_amount=25.0,
            check3_amount=10.0,
            total_paid=160.0,
            mjc_club_id=None,
            cotisation_status='Payée'
        )
        
        members = get_all_members()
        assert len(members) == 1, f"Expected 1 member, got {len(members)}"
        
        member = members[0]
        assert member['cash_amount'] == 75.0, f"Cash amount incorrect: {member['cash_amount']}"
        assert member['check1_amount'] == 50.0, f"Check1 amount incorrect: {member['check1_amount']}"
        assert member['check2_amount'] == 25.0, f"Check2 amount incorrect: {member['check2_amount']}"
        assert member['check3_amount'] == 10.0, f"Check3 amount incorrect: {member['check3_amount']}"
        assert member['total_paid'] == 160.0, f"Total paid incorrect: {member['total_paid']}"
        assert member['ancv_amount'] == 15.0, f"ANCV amount incorrect: {member['ancv_amount']}"
        
        print("✓ Tous les champs de paiement sont correctement enregistrés")
        
        # Vérifier que les anciens champs ont été supprimés
        assert 'health' not in member.keys(), "Field 'health' should not exist"
        assert 'external_club' not in member.keys(), "Field 'external_club' should not exist"
        print("✓ Anciens champs (health, external_club) supprimés avec succès")
        
        # Test de modification
        member_id = member['id']
        update_member(
            member_id,
            last_name='Martin',
            first_name='Sophie',
            address='10 Avenue Test',
            postal_code='69001',
            city='Lyon',
            phone='0687654321',
            mail='sophie.martin@test.fr',
            rgpd=1,
            image_rights=1,
            payment_type='club_mjc',
            ancv_amount=20.0,
            cash_amount=100.0,
            check1_amount=0.0,
            check2_amount=0.0,
            check3_amount=0.0,
            total_paid=100.0,
            mjc_club_id=None,
            cotisation_status='Payée'
        )
        
        updated_member = get_member_by_id(member_id)
        assert updated_member['cash_amount'] == 100.0, "Update failed"
        assert updated_member['total_paid'] == 100.0, "Total paid update failed"
        assert updated_member['ancv_amount'] == 20.0, "ANCV update failed"
        print("✓ Modification des champs de paiement réussie")
        
    finally:
        os.unlink(db_path)

def test_database_migration():
    """Test de la migration des bases de données existantes."""
    print("\nTest 2: Migration de base existante...")
    
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        # Créer une "ancienne" base avec les anciens champs
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT,
                first_name TEXT,
                health TEXT,
                external_club TEXT,
                payment_type TEXT,
                ancv_amount REAL
            )
        """)
        cursor.execute("""
            INSERT INTO members (last_name, first_name, health, external_club, payment_type, ancv_amount)
            VALUES ('Test', 'User', 'Good health', 'Other club', 'club_mjc', 10.0)
        """)
        conn.commit()
        conn.close()
        
        # Maintenant initialiser avec notre Database qui devrait migrer
        db = Database.instance(db_path)
        
        # Vérifier que la migration a ajouté les nouveaux champs
        cursor = db.connection.cursor()
        cursor.execute("PRAGMA table_info(members)")
        columns = [row[1] for row in cursor.fetchall()]
        
        assert 'cash_amount' in columns, "Migration failed: cash_amount not added"
        assert 'check1_amount' in columns, "Migration failed: check1_amount not added"
        assert 'check2_amount' in columns, "Migration failed: check2_amount not added"
        assert 'check3_amount' in columns, "Migration failed: check3_amount not added"
        assert 'total_paid' in columns, "Migration failed: total_paid not added"
        assert 'health' not in columns, "Migration failed: health not removed"
        assert 'external_club' not in columns, "Migration failed: external_club not removed"
        
        print("✓ Migration réussie: nouveaux champs ajoutés")
        print("✓ Migration réussie: anciens champs supprimés")
        
        # Vérifier que les données existantes sont préservées
        members = get_all_members()
        assert len(members) == 1, "Migration lost existing data"
        assert members[0]['last_name'] == 'Test', "Migration corrupted data"
        print("✓ Migration réussie: données existantes préservées")
        
    finally:
        os.unlink(db_path)

def test_annual_prices_workflow():
    """Test du workflow de configuration des tarifs."""
    print("\nTest 3: Workflow de gestion des tarifs...")
    
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Simuler la configuration initiale
        add_annual_price('2024-2025', 120.0, 60.0, is_current=True)
        
        current_price = get_current_annual_price()
        assert current_price is not None, "Current price not set"
        assert current_price['year'] == '2024-2025', "Year incorrect"
        assert current_price['club_price'] == 120.0, "Club price incorrect"
        assert current_price['mjc_price'] == 60.0, "MJC price incorrect"
        assert current_price['is_current'] == 1, "is_current flag incorrect"
        print("✓ Configuration initiale des tarifs réussie")
        
        # Test de modification des tarifs
        update_annual_price(
            current_price['id'],
            '2024-2025',
            130.0,
            65.0,
            True
        )
        
        updated_price = get_current_annual_price()
        assert updated_price['club_price'] == 130.0, "Update failed"
        assert updated_price['mjc_price'] == 65.0, "Update failed"
        print("✓ Modification des tarifs réussie")
        
        # Vérifier qu'il n'y a qu'un seul tarif courant
        all_prices = get_all_annual_prices()
        current_count = sum(1 for p in all_prices if p['is_current'] == 1)
        assert current_count == 1, f"Should have exactly 1 current price, got {current_count}"
        print("✓ Un seul tarif courant à la fois")
        
    finally:
        os.unlink(db_path)

def test_member_validation():
    """Test de la validation des champs obligatoires."""
    print("\nTest 4: Validation des champs...")
    
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Test avec montants valides
        add_member(
            last_name='Validation',
            first_name='Test',
            address='',
            postal_code='',
            city='',
            phone='',
            mail='',
            rgpd=1,
            image_rights=0,
            payment_type='club_mjc',
            ancv_amount=0.0,
            cash_amount=50.5,
            check1_amount=25.75,
            check2_amount=0.0,
            check3_amount=0.0,
            total_paid=76.25,
            mjc_club_id=None,
            cotisation_status='Partiellement payée'
        )
        
        members = get_all_members()
        assert len(members) == 1, "Member not added"
        print("✓ Validation: montants valides acceptés")
        
        # Vérifier les montants décimaux
        member = members[0]
        assert abs(member['cash_amount'] - 50.5) < 0.01, "Decimal values not preserved"
        assert abs(member['check1_amount'] - 25.75) < 0.01, "Decimal values not preserved"
        print("✓ Validation: montants décimaux corrects")
        
    finally:
        os.unlink(db_path)

def test_complete_workflow():
    """Test du workflow complet: création base → configuration tarifs → ajout membre."""
    print("\nTest 5: Workflow complet...")
    
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        # 1. Créer une nouvelle base
        db = Database.instance(db_path)
        print("✓ Base de données créée")
        
        # 2. Configurer les tarifs initiaux
        add_annual_price('2024-2025', 100.0, 50.0, is_current=True)
        current_price = get_current_annual_price()
        assert current_price is not None, "Initial prices not configured"
        print("✓ Tarifs initiaux configurés")
        
        # 3. Ajouter un membre
        add_member(
            last_name='Workflow',
            first_name='Complete',
            address='Test address',
            postal_code='75000',
            city='Paris',
            phone='0123456789',
            mail='workflow@test.fr',
            rgpd=1,
            image_rights=1,
            payment_type='club_mjc',
            ancv_amount=0.0,
            cash_amount=150.0,
            check1_amount=0.0,
            check2_amount=0.0,
            check3_amount=0.0,
            total_paid=150.0,
            mjc_club_id=None,
            cotisation_status='Payée'
        )
        
        members = get_all_members()
        assert len(members) == 1, "Member not added in complete workflow"
        print("✓ Membre ajouté avec succès")
        
        # 4. Modifier les tarifs
        update_annual_price(
            current_price['id'],
            '2024-2025',
            110.0,
            55.0,
            True
        )
        
        updated_price = get_current_annual_price()
        assert updated_price['club_price'] == 110.0, "Price update failed"
        print("✓ Tarifs modifiés avec succès")
        
        # 5. Vérifier que le membre existe toujours
        members = get_all_members()
        assert len(members) == 1, "Member lost after price update"
        print("✓ Données membre préservées après modification tarifs")
        
    finally:
        os.unlink(db_path)

def main():
    print("=" * 60)
    print("Tests des nouvelles fonctionnalités - Formulaire et Tarifs")
    print("=" * 60)
    
    tests = [
        test_member_payment_fields,
        test_database_migration,
        test_annual_prices_workflow,
        test_member_validation,
        test_complete_workflow
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ Test échoué: {test.__name__}")
            print(f"  Erreur: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Résultats: {passed} réussis, {failed} échoués")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
