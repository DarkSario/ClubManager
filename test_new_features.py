#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider les nouvelles fonctionnalités de gestion des clubs MJC et prix annuels.
"""

import sys
import os
import tempfile

# Ajouter le répertoire parent au path pour pouvoir importer club_manager
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from club_manager.core.database import Database
from club_manager.core.members import add_member, get_all_members, get_member_by_id, update_member
from club_manager.core.mjc_clubs import add_mjc_club, get_all_mjc_clubs, update_mjc_club, delete_mjc_club
from club_manager.core.annual_prices import add_annual_price, get_all_annual_prices, get_current_annual_price, set_current_annual_price

def test_mjc_clubs():
    """Test des opérations sur les clubs MJC."""
    print("\nTest 1: Opérations sur les clubs MJC...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Ajouter des clubs MJC
        add_mjc_club("MJC Centre")
        add_mjc_club("MJC Nord")
        add_mjc_club("MJC Sud")
        
        clubs = get_all_mjc_clubs()
        assert len(clubs) == 3, f"Expected 3 clubs, got {len(clubs)}"
        assert clubs[0]['name'] == "MJC Centre", "Premier club incorrect"
        print("✓ Ajout de clubs MJC réussi")
        
        # Modifier un club
        club_id = clubs[0]['id']
        update_mjc_club(club_id, "MJC Centre-Ville")
        clubs = get_all_mjc_clubs()
        assert clubs[0]['name'] == "MJC Centre-Ville", "Modification échouée"
        print("✓ Modification de club MJC réussie")
        
        # Supprimer un club
        delete_mjc_club(clubs[2]['id'])
        clubs = get_all_mjc_clubs()
        assert len(clubs) == 2, "Suppression échouée"
        print("✓ Suppression de club MJC réussie")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def test_annual_prices():
    """Test des opérations sur les prix annuels."""
    print("\nTest 2: Opérations sur les prix annuels...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Ajouter des prix annuels
        add_annual_price("2023-2024", 140.0, 45.0, False)
        add_annual_price("2024-2025", 150.0, 50.0, True)
        
        prices = get_all_annual_prices()
        assert len(prices) == 2, f"Expected 2 prices, got {len(prices)}"
        print("✓ Ajout de prix annuels réussi")
        
        # Vérifier le prix courant
        current = get_current_annual_price()
        assert current is not None, "Aucun prix courant"
        assert current['year'] == "2024-2025", "Prix courant incorrect"
        assert current['club_price'] == 150.0, "Prix club incorrect"
        assert current['mjc_price'] == 50.0, "Prix MJC incorrect"
        print("✓ Prix courant défini correctement")
        
        # Changer le prix courant
        # Note: prices[0] est 2024-2025 (DESC order), prices[1] est 2023-2024
        set_current_annual_price(prices[1]['id'])
        current = get_current_annual_price()
        assert current['year'] == "2023-2024", "Changement de prix courant échoué"
        print("✓ Changement de prix courant réussi")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def test_member_with_new_fields():
    """Test des opérations sur les membres avec les nouveaux champs."""
    print("\nTest 3: Opérations sur les membres avec nouveaux champs...")
    
    # Réinitialiser le singleton
    Database._instance = None
    Database._current_db_path = None
    
    fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    
    try:
        db = Database.instance(db_path)
        
        # Ajouter un club MJC d'abord
        add_mjc_club("MJC Test")
        clubs = get_all_mjc_clubs()
        mjc_club_id = clubs[0]['id']
        
        # Ajouter un membre avec paiement Club uniquement
        add_member(
            last_name="Dupont",
            first_name="Jean",
            rgpd=1,
            payment_type="club_only",
            ancv_amount=25.0,
            mjc_club_id=mjc_club_id,
            cotisation_status="Payée"
        )
        
        members = get_all_members()
        assert len(members) == 1, "Membre non ajouté"
        
        member = members[0]
        assert member['payment_type'] == "club_only", "Type de paiement incorrect"
        assert member['ancv_amount'] == 25.0, "Montant ANCV incorrect"
        assert member['mjc_club_id'] == mjc_club_id, "Club MJC ID incorrect"
        assert member['cotisation_status'] == "Payée", "Statut cotisation incorrect"
        print("✓ Membre avec paiement Club uniquement créé")
        
        # Ajouter un membre avec paiement Club+MJC
        add_member(
            last_name="Martin",
            first_name="Marie",
            rgpd=1,
            payment_type="club_mjc",
            ancv_amount=0.0,
            mjc_club_id=None,
            cotisation_status="Non payée"
        )
        
        members = get_all_members()
        assert len(members) == 2, "Deuxième membre non ajouté"
        
        member2 = members[1]
        assert member2['payment_type'] == "club_mjc", "Type de paiement Club+MJC incorrect"
        assert member2['mjc_club_id'] is None, "Club MJC devrait être None"
        print("✓ Membre avec paiement Club+MJC créé")
        
        # Modifier un membre
        update_member(
            member['id'],
            last_name="Dupont",
            first_name="Jean",
            rgpd=1,
            payment_type="club_mjc",
            ancv_amount=50.0,
            mjc_club_id=None,
            cotisation_status="Partiellement payée"
        )
        
        updated_member = get_member_by_id(member['id'])
        assert updated_member['payment_type'] == "club_mjc", "Modification type paiement échouée"
        assert updated_member['ancv_amount'] == 50.0, "Modification ANCV échouée"
        assert updated_member['cotisation_status'] == "Partiellement payée", "Modification statut échouée"
        print("✓ Modification de membre réussie")
        
        db.close()
        return True
    finally:
        os.remove(db_path)

def main():
    """Fonction principale de test."""
    print("=" * 60)
    print("Tests de validation des nouvelles fonctionnalités")
    print("=" * 60)
    
    tests = [
        test_mjc_clubs,
        test_annual_prices,
        test_member_with_new_fields
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Échec: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Résultats: {passed} réussis, {failed} échoués")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
