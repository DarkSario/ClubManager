# Version 2.3 - Nouvelles Fonctionnalités

## Vue d'ensemble

Cette version 2.3 apporte 4 améliorations majeures à ClubManager :

1. **Sauvegarde/Restauration ZIP complète**
2. **Export PDF professionnel**
3. **Champ Objet dans le Mailing**
4. **Import de liste de clubs MJC**

---

## 1. Sauvegarde : Import/Export ZIP

### Fonctionnalité
- **Export ZIP** : Crée une archive complète contenant la base de données et la configuration
- **Import ZIP** : Restaure une base de données depuis une archive ZIP
- Barre de progression lors des opérations
- Gestion des erreurs avec messages clairs
- Conservation optionnelle de la configuration

### Utilisation

#### Export ZIP
1. Aller dans l'onglet **Sauvegarde**
2. Cliquer sur **Exporter (zip)**
3. Choisir l'emplacement de sauvegarde
4. L'archive contient :
   - Le fichier de base de données (.db)
   - Le fichier de configuration (config.json)

#### Import ZIP
1. Aller dans l'onglet **Sauvegarde**
2. Cliquer sur **Importer (zip)**
3. Sélectionner l'archive à importer
4. Choisir l'emplacement pour la base restaurée
5. Option de restaurer ou non la configuration

### Implémentation
- **Fichier** : `club_manager/core/backup.py`
- **Fonctions** : `export_zip_archive()`, `import_zip_archive()`
- **UI** : `club_manager/ui/backup_tab.py`

---

## 2. Export PDF

### Fonctionnalité
- Export professionnel au format PDF
- Mise en page automatique avec tables
- Sélection des champs à exporter
- Support de tous les types de données :
  - Membres
  - Postes
  - Clubs MJC
  - Prix annuels

### Utilisation

1. Aller dans l'onglet **Exports**
2. Cliquer sur **Exporter PDF**
3. Sélectionner le type de données à exporter
4. Choisir les champs à inclure (optionnel)
5. Sélectionner l'emplacement du fichier PDF

### Caractéristiques du PDF
- En-tête avec titre et date
- Table formatée avec couleurs alternées
- Largeur de colonnes automatique
- Pied de page avec total d'éléments
- Format A4
- Encodage UTF-8

### Implémentation
- **Fichier** : `club_manager/core/export.py`
- **Fonction** : `export_to_pdf()`
- **UI** : `club_manager/ui/exports_tab.py`
- **Dépendance** : reportlab

---

## 3. Champ Objet du Mail

### Fonctionnalité
- Nouveau champ "Objet" dans l'onglet Mailing
- Validation obligatoire avant envoi
- Affichage dans la prévisualisation
- Interface cohérente avec le reste de l'application

### Utilisation

1. Aller dans l'onglet **Mailing**
2. Remplir le champ **Objet** (obligatoire)
3. Rédiger le message dans le champ **Corps**
4. Cliquer sur **Prévisualiser** pour voir le rendu
5. Cliquer sur **Envoyer** pour envoyer le mail

### Interface
- Champ "Objet" : ligne de texte au-dessus du corps du message
- Placeholder : "Saisissez l'objet du mail..."
- Validation : message d'erreur si vide

### Implémentation
- **Fichier UI** : `resources/ui/mailing_tab.ui`
- **Fichier UI généré** : `club_manager/ui/mailing_tab_ui.py`
- **Logique** : `club_manager/ui/mailing_tab.py`

---

## 4. Import de Liste de Clubs MJC

### Fonctionnalité
- Import de plusieurs clubs MJC en une seule opération
- Support du copier-coller
- Import depuis fichier texte
- Détection automatique des doublons
- Rapport détaillé après import

### Utilisation

#### Méthode 1 : Copier-Coller
1. Aller dans l'onglet **Clubs MJC**
2. Cliquer sur **Importer/Coller une liste**
3. Coller la liste (un club par ligne)
4. Cliquer sur **OK**

#### Méthode 2 : Depuis un fichier
1. Aller dans l'onglet **Clubs MJC**
2. Cliquer sur **Importer/Coller une liste**
3. Cliquer sur **Charger depuis un fichier**
4. Sélectionner le fichier texte (.txt)
5. Cliquer sur **OK**

### Format du fichier
```
MJC Centre
MJC Nord
MJC Sud
MJC Est
MJC Ouest
```

### Gestion des doublons
- Les clubs existants sont automatiquement ignorés
- Rapport final indique le nombre de clubs ajoutés et ignorés
- Pas de duplication même si le nom existe déjà

### Implémentation
- **Fichier** : `club_manager/ui/mjc_clubs_tab.py`
- **Fonctions** : `import_clubs_list()`, `_load_clubs_from_file()`

---

## Installation des dépendances

Pour utiliser toutes les nouvelles fonctionnalités, installer les dépendances :

```bash
pip install -r requirements.txt
```

### Nouvelles dépendances
- **reportlab** : Pour la génération de PDF

---

## Tests

Un nouveau fichier de tests a été créé pour valider toutes les fonctionnalités :

```bash
python test_v2_3_features.py
```

### Tests inclus
1. Import de liste de clubs MJC avec gestion des doublons
2. Export/Import ZIP avec validation du contenu
3. Export PDF avec génération de table
4. Présence du champ sujet dans l'interface mailing

---

## Fichiers modifiés

### Core (Logique métier)
- `club_manager/core/backup.py` : Ajout export/import ZIP complet
- `club_manager/core/export.py` : Ajout export PDF professionnel

### UI (Interface utilisateur)
- `club_manager/ui/backup_tab.py` : Activation boutons ZIP
- `club_manager/ui/exports_tab.py` : Activation export PDF + sélection champs
- `club_manager/ui/mailing_tab.py` : Utilisation du champ sujet
- `club_manager/ui/mailing_tab_ui.py` : Ajout du widget sujet (généré)
- `club_manager/ui/mjc_clubs_tab.py` : Ajout import de liste

### Ressources
- `resources/ui/mailing_tab.ui` : Ajout du champ sujet dans la définition UI

### Configuration
- `requirements.txt` : Ajout de reportlab

### Tests
- `test_v2_3_features.py` : Nouveau fichier de tests pour v2.3

---

## Migration

### Depuis version 2.2
Aucune migration nécessaire. Les nouvelles fonctionnalités sont compatibles avec les bases de données existantes.

### Installation de reportlab
Si vous n'avez pas reportlab installé :
```bash
pip install reportlab
```

---

## Prochaines améliorations possibles

1. **Mailing** : Intégration SMTP réelle pour l'envoi de mails
2. **PDF** : Templates personnalisables
3. **Import** : Support de formats supplémentaires (CSV, Excel)
4. **Backup** : Planification automatique des sauvegardes

---

## Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation complète dans README.md
