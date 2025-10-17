# -*- coding: utf-8 -*-
"""
Fichier : club_manager/ui/tutorial_dialog.py
Rôle : Fenêtre modale Tutoriel interactif embarqué, navigation pas-à-pas.
Hérite de QDialog et Ui_TutorialDialog.
Connexion de tous les boutons/actions à des slots effectifs.
Dépendances : PyQt5, Ui_TutorialDialog généré par pyuic5 à partir de resources/ui/tutorial_dialog.ui
"""

from PyQt5 import QtWidgets
from club_manager.ui.tutorial_dialog_ui import Ui_TutorialDialog

class TutorialDialog(QtWidgets.QDialog, Ui_TutorialDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buttonNext.clicked.connect(self.next_step)
        self.buttonPrev.clicked.connect(self.prev_step)
        self.buttonClose.clicked.connect(self.reject)
        self.steps = [
            "Bienvenue dans Club Manager v2.3 !\n\nCe tutoriel vous guidera pour la prise en main de toutes les fonctionnalités.",
            "📂 Système multi-bases\n\nChaque base de données = une saison/année.\nChangez de base via Fichier → Changer de base de données.\nCréez une nouvelle base pour chaque saison.",
            "👥 Onglet Membres\n\nAjoutez, modifiez et recherchez vos adhérents.\nType de paiement : Club+MJC ou Club uniquement.\nGestion ANCV et statut de cotisation intégrés.\nConsentement RGPD obligatoire.",
            "🏢 Onglet Postes\n\nGérez les rôles et responsabilités du club :\n- Président, Trésorier, Secrétaire...\n- Affectez des postes aux membres\n- Suivez l'organisation de votre structure",
            "🏛️ Onglet Clubs MJC\n\nEnregistrez les clubs MJC partenaires.\nNouveau : Import en masse !\n- Copier-coller une liste\n- Importer depuis un fichier .txt\n- Détection automatique des doublons",
            "💾 Onglet Sauvegarde\n\nProtégez vos données :\n- Export/Import classique\n- Nouveau : Export/Import ZIP complet\n- Archive complète avec base et configuration\n- Barres de progression en temps réel",
            "📊 Onglet Exports\n\nExportez vos données en plusieurs formats :\n- CSV pour tableurs\n- Nouveau : PDF professionnel avec mise en page\n- Sélection de champs personnalisée\n- Export de tous types de données",
            "📧 Onglet Mailing\n\nEnvoyez des emails groupés aux adhérents :\n- Nouveau : Champ Objet obligatoire\n- Sélection de destinataires\n- Prévisualisation avant envoi\n- Configuration SMTP à venir",
            "🔍 Onglet Audit\n\nSuivez toutes les modifications :\n- Historique complet des actions\n- Traçabilité des changements\n- Filtres par date et type d'action\n- Conformité RGPD",
            "🎨 Onglet Thème\n\nPersonnalisez l'interface :\n- Thèmes clairs et sombres\n- Changement en temps réel\n- Préférences sauvegardées",
            "💰 Tarifs annuels\n\nConfigurez les prix Club et MJC.\nMenu : Fichier → Modifier les tarifs.\nUn tarif par année/saison.\nUtilisés automatiquement dans les formulaires.",
            "✅ Points clés version 2.3\n\n✨ Export/Import ZIP complet\n✨ Export PDF professionnel\n✨ Champ Objet dans Mailing\n✨ Import de liste de clubs MJC\n\nConsultez la documentation pour plus de détails !"
        ]
        self.current_step = 0
        self.refresh_step()

    def refresh_step(self):
        self.labelStep.setText(self.steps[self.current_step])
        self.buttonPrev.setEnabled(self.current_step > 0)
        self.buttonNext.setEnabled(self.current_step < len(self.steps)-1)

    def next_step(self):
        if self.current_step < len(self.steps)-1:
            self.current_step += 1
            self.refresh_step()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.refresh_step()