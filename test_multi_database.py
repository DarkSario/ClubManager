#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simple pour valider les fonctionnalités de base du système multi-bases.
"""

import sys
import os
import tempfile

# Ajouter le répertoire parent au path pour pouvoir importer club_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from club_manager.core.database import Database
from club_manager.core.members import add_member, get_all_members, delete_member
from club_manager.core.cotisations import add_cotisation, get_all_cotisations
from club_manager.core.sessions import add_session, get_all_sessions

def test_database_creation():
    """Test de création d'une base de données."""
    print("Test 1: Création de base de données...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    # Créer une base temporaire
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        # Initialiser la base
        db = Database.instance(db_path)
        
        # Vérifier que les tables existent
        tables = db.query("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [t["name"] for t in tables]
        
        assert "members" in table_names, "Table 'members' manquante"
        assert "cotisations" in table_names, "Table 'cotisations' manquante"
        assert "sessions" in table_names, "Table 'sessions' manquante"
        
        print("✓ Base de données créée avec succès")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def test_member_operations():
    """Test des opérations sur les membres."""
    print("\nTest 2: Opérations sur les membres...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Ajouter un membre
        add_member(
            last_name="Dupont",
            first_name="Jean",
            address="123 rue de la Paix",
            postal_code="75000",
            city="Paris",
            phone="0123456789",
            mail="jean.dupont@example.com",
            rgpd=1,
            image_rights=1,
            cash=0.0,
            total_paid=0.0,
            club_part=0.0,
            mjc_part=0.0
        )
        
        # Récupérer tous les membres
        members = get_all_members()
        assert len(members) == 1, "Le membre n'a pas été ajouté"
        assert members[0]["last_name"] == "Dupont", "Nom incorrect"
        assert members[0]["first_name"] == "Jean", "Prénom incorrect"
        
        print("✓ Ajout de membre réussi")
        
        # Supprimer le membre
        member_id = members[0]["id"]
        delete_member(member_id)
        
        members = get_all_members()
        assert len(members) == 0, "Le membre n'a pas été supprimé"
        
        print("✓ Suppression de membre réussie")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def test_cotisation_operations():
    """Test des opérations sur les cotisations."""
    print("\nTest 3: Opérations sur les cotisations...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Créer un membre et une session d'abord
        add_member(last_name="Test", first_name="User", rgpd=1)
        members = get_all_members()
        member_id = members[0]["id"]
        
        add_session("2024-2025", "2024-09-01", "2025-08-31", 150.0, 50.0, True)
        sessions = get_all_sessions()
        session_id = sessions[0]["id"]
        
        # Ajouter une cotisation avec chèque
        add_cotisation(
            member_id=member_id,
            session_id=session_id,
            amount=200.0,
            paid=200.0,
            payment_date="2024-09-15",
            method="Chèque",
            status="Payé",
            cheque_number="1234567"
        )
        
        cotisations = get_all_cotisations()
        assert len(cotisations) == 1, "La cotisation n'a pas été ajoutée"
        assert cotisations[0]["amount"] == 200.0, "Montant incorrect"
        assert cotisations[0]["cheque_number"] == "1234567", "Numéro de chèque incorrect"
        
        print("✓ Ajout de cotisation avec numéro de chèque réussi")
        
        # Ajouter une cotisation sans chèque
        add_cotisation(
            member_id=member_id,
            session_id=session_id,
            amount=50.0,
            paid=50.0,
            payment_date="2024-09-16",
            method="Espèce",
            status="Payé",
            cheque_number=None
        )
        
        cotisations = get_all_cotisations()
        assert len(cotisations) == 2, "La seconde cotisation n'a pas été ajoutée"
        
        print("✓ Ajout de cotisation sans chèque réussi")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def test_database_change():
    """Test du changement de base de données."""
    print("\nTest 4: Changement de base de données...")
    
    fd1, db_path1 = tempfile.mkstemp(suffix='.db')
    os.close(fd1)
    fd2, db_path2 = tempfile.mkstemp(suffix='.db')
    os.close(fd2)
    
    try:
        # Réinitialiser le singleton
        Database._instance = None
        Database._current_db_path = None
        
        # Base 1
        db1 = Database.instance(db_path1)
        add_member(last_name="Base1", first_name="User1", rgpd=1)
        members = get_all_members()
        assert len(members) == 1, f"Membre non ajouté dans base 1 (got {len(members)})"
        assert members[0]["last_name"] == "Base1", "Mauvais membre dans base 1"
        
        print("✓ Base 1 créée avec 1 membre")
        
        # Changer pour la base 2
        db2 = Database.change_database(db_path2)
        members = get_all_members()
        assert len(members) == 0, f"Base 2 devrait être vide (got {len(members)})"
        
        print("✓ Changement vers base 2 réussi (vide)")
        
        # Ajouter dans la base 2
        add_member(last_name="Base2", first_name="User2", rgpd=1)
        members = get_all_members()
        assert len(members) == 1, "Membre non ajouté dans base 2"
        assert members[0]["last_name"] == "Base2", "Mauvais membre dans base 2"
        
        print("✓ Ajout dans base 2 réussi")
        
        # Retour à la base 1
        db1 = Database.change_database(db_path1)
        members = get_all_members()
        assert len(members) == 1, "Base 1 devrait avoir 1 membre"
        assert members[0]["last_name"] == "Base1", "Mauvais membre après retour à base 1"
        
        print("✓ Retour à base 1 réussi")
        
        db1.close()
        return True
    finally:
        os.remove(db_path1)
        os.remove(db_path2)

def main():
    """Fonction principale de test."""
    print("=" * 60)
    print("Tests de validation du système multi-bases")
    print("=" * 60)
    
    tests = [
        test_database_creation,
        test_member_operations,
        test_cotisation_operations,
        test_database_change
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Échec: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Résultats: {passed} réussis, {failed} échoués")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
