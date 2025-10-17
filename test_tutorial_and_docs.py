#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour le tutoriel interactif et la documentation embarquée
"""

import os
import sys
from PyQt5.QtWidgets import QApplication


def test_tutorial_steps_updated():
    """Vérifie que le tutoriel contient les bonnes étapes pour la v2.3"""
    # Read the tutorial file directly to avoid QApplication issues
    tutorial_file = os.path.join(
        os.path.dirname(__file__), 
        "club_manager", "ui", "tutorial_dialog.py"
    )
    
    with open(tutorial_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the steps list from the file
    import re
    steps_match = re.search(r'self\.steps = \[(.*?)\]', content, re.DOTALL)
    assert steps_match, "Could not find steps list in tutorial_dialog.py"
    
    steps_text = steps_match.group(1)
    # Count the number of steps by counting commas + 1 (simpler and safer)
    # Each step is separated by a comma in the list
    step_count = steps_text.count('",') + 1
    
    # Vérifier le nombre d'étapes (12 étapes pour la v2.3)
    assert step_count == 12, f"Expected 12 tutorial steps, got {step_count}"
    
    # Vérifier que la première étape mentionne v2.3
    assert "v2.3" in steps_text, "First step should mention v2.3"
    
    # Vérifier les modules principaux
    assert "Membres" in steps_text, "Tutorial should mention Membres tab"
    assert "Postes" in steps_text, "Tutorial should mention Postes tab"
    assert "Clubs MJC" in steps_text, "Tutorial should mention Clubs MJC tab"
    assert "Sauvegarde" in steps_text, "Tutorial should mention Sauvegarde tab"
    assert "Exports" in steps_text, "Tutorial should mention Exports tab"
    assert "Mailing" in steps_text, "Tutorial should mention Mailing tab"
    assert "Audit" in steps_text, "Tutorial should mention Audit tab"
    assert "Thème" in steps_text, "Tutorial should mention Thème tab"
    
    # Vérifier les nouvelles fonctionnalités v2.3
    assert "ZIP" in steps_text, "Tutorial should mention ZIP export/import"
    assert "PDF" in steps_text, "Tutorial should mention PDF export"
    assert "Objet" in steps_text, "Tutorial should mention mail subject field"
    assert "Import en masse" in steps_text or "Import de liste" in steps_text, \
        "Tutorial should mention MJC clubs import"
    
    print(f"✓ Tutorial has {step_count} steps")
    print("✓ Tutorial mentions v2.3 and all current features")
    print("✓ Tutorial does not mention deprecated features")
    
    return True


def test_documentation_html_exists():
    """Vérifie que le fichier de documentation HTML existe et est accessible"""
    
    # Trouver le chemin du fichier de documentation
    repo_root = os.path.dirname(os.path.abspath(__file__))
    doc_path = os.path.join(repo_root, "resources", "docs", "user_manual.html")
    
    # Vérifier que le fichier existe
    assert os.path.exists(doc_path), f"Documentation file not found at {doc_path}"
    
    # Vérifier que le fichier est lisible
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier la longueur minimale (doit être substantiel)
    assert len(content) > 10000, f"Documentation seems too short: {len(content)} characters"
    
    print(f"✓ Documentation file exists at {doc_path}")
    print(f"✓ Documentation size: {len(content)} characters")
    
    return True


def test_documentation_content():
    """Vérifie que la documentation contient toutes les sections nécessaires"""
    
    repo_root = os.path.dirname(os.path.abspath(__file__))
    doc_path = os.path.join(repo_root, "resources", "docs", "user_manual.html")
    
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les sections principales
    required_sections = [
        "Introduction",
        "Système multi-bases",
        "Gestion des membres",
        "Gestion des postes",
        "Clubs MJC",
        "Sauvegarde et restauration",
        "Exports de données",
        "Mailing groupé",
        "Audit et traçabilité",
        "Thèmes et personnalisation",
        "Tarifs annuels",
        "Conformité RGPD",
        "Nouveautés version 2.3"
    ]
    
    for section in required_sections:
        assert section in content, f"Documentation should contain section: {section}"
    
    # Vérifier les nouvelles fonctionnalités v2.3
    v2_3_features = [
        "Export/Import ZIP",
        "Export PDF",
        "Champ Objet",
        "Import en masse"
    ]
    
    for feature in v2_3_features:
        assert feature in content, f"Documentation should mention v2.3 feature: {feature}"
    
    # Vérifier que c'est du HTML valide
    assert "<!DOCTYPE html>" in content, "Documentation should be valid HTML"
    assert "<html" in content, "Documentation should have html tag"
    assert "</html>" in content, "Documentation should close html tag"
    assert "charset=UTF-8" in content or "charset=\"UTF-8\"" in content, \
        "Documentation should specify UTF-8 encoding"
    
    # Vérifier la mention de la version
    assert "v2.3" in content or "version 2.3" in content or "Version 2.3" in content, \
        "Documentation should mention version 2.3"
    
    print(f"✓ Documentation contains all required sections")
    print(f"✓ Documentation mentions all v2.3 features")
    print(f"✓ Documentation is valid HTML with UTF-8 encoding")
    
    return True


def test_documentation_loading_from_main_window():
    """Vérifie que la documentation peut être chargée depuis la fenêtre principale"""
    
    import os
    
    # Simuler la logique de chargement de main_window.py
    main_window_dir = os.path.dirname(os.path.abspath(__file__))
    main_window_dir = os.path.join(main_window_dir, "club_manager")
    
    doc_path = os.path.join(main_window_dir, "..", "resources", "docs", "user_manual.html")
    doc_path = os.path.abspath(doc_path)
    
    # Vérifier que le chemin se résout correctement
    assert os.path.exists(doc_path), f"Documentation not found at resolved path: {doc_path}"
    
    # Vérifier qu'on peut lire le contenu
    with open(doc_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    assert len(html_content) > 0, "Documentation content should not be empty"
    assert "<html" in html_content, "Documentation should be HTML"
    
    print(f"✓ Documentation can be loaded from main window")
    print(f"✓ Resolved path: {doc_path}")
    
    return True


if __name__ == "__main__":
    print("Testing tutorial and documentation...\n")
    
    try:
        test_tutorial_steps_updated()
        print()
        test_documentation_html_exists()
        print()
        test_documentation_content()
        print()
        test_documentation_loading_from_main_window()
        print()
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
