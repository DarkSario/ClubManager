# Club Manager

Club Manager est une application de gestion complète pour les associations sportives et clubs. Elle permet de gérer les adhérents, les cotisations, les sessions, et bien plus encore.

## Fonctionnalités principales

- **Gestion des membres** : Ajout, modification, suppression et recherche d'adhérents
- **Gestion des prix annuels** : Configuration des prix Club et MJC pour chaque année
- **Gestion des clubs MJC** : Enregistrement des autres clubs MJC partenaires (avec import en masse)
- **Système multi-bases** : Une base de données par saison/année pour faciliter la gestion (remplace l'ancien système de sessions)
- **Gestion des postes** : Attribution des responsabilités au sein du club
- **Exports** : Export des données en CSV ou PDF (avec sélection de champs)
- **Mailing** : Envoi d'emails groupés aux adhérents (avec champ objet)
- **Audit** : Traçabilité des modifications
- **Sauvegarde/Restauration** : Backup et restauration des données (format ZIP complet)
- **Conformité RGPD** : Gestion des consentements et des données personnelles
- **Thèmes personnalisables** : Interface adaptable selon vos préférences

## Système multi-bases de données

### Concept

Depuis la version 2.0, Club Manager utilise un système multi-bases où **chaque base de données correspond à une saison ou une année**. Cela présente plusieurs avantages :

- **Séparation claire des données** : Chaque saison a ses propres membres, cotisations et activités
- **Performance améliorée** : Les bases sont plus légères et plus rapides
- **Archivage simplifié** : Conservez facilement l'historique de chaque saison
- **Sécurité renforcée** : Les données d'une saison ne peuvent pas être altérées par accident lors de la gestion d'une autre

### Au démarrage

Au lancement de l'application, un dialogue vous propose de :

1. **Ouvrir une base existante** : La liste des bases détectées s'affiche automatiquement
2. **Parcourir** : Sélectionner une base dans un autre emplacement
3. **Créer une nouvelle base** : Pour démarrer une nouvelle saison

La dernière base utilisée est automatiquement pré-sélectionnée pour faciliter la navigation.

### Changement de base

À tout moment, vous pouvez changer de base de données via le menu :
- **Fichier → Changer de base de données...**

Cela vous permettra de passer d'une saison à une autre sans redémarrer l'application.

### Stockage des bases

Par défaut, les bases de données sont stockées dans :
- **Linux/Mac** : `~/.clubmanager/`
- **Windows** : `C:\Users\<username>\.clubmanager\`

Vous pouvez également créer et ouvrir des bases dans n'importe quel emplacement.

## Migration annuelle

### Créer une nouvelle base pour la saison suivante

À chaque début de saison, il est recommandé de créer une nouvelle base de données :

1. Au démarrage de l'application, sélectionnez **"Créer une nouvelle base"**
2. Donnez-lui un nom explicite, par exemple : `ClubManager_2024-2025.db`
3. La nouvelle base est créée vide et prête à l'emploi

### Réutiliser des données de la saison précédente

Si vous souhaitez reprendre certains membres de la saison précédente :

1. Ouvrez l'ancienne base
2. Utilisez la fonction **Exports → Exporter les membres** pour créer un fichier CSV
3. Ouvrez la nouvelle base
4. Utilisez la fonction d'import (si disponible) ou ajoutez manuellement les membres

**Note** : Les membres doivent être ajoutés à nouveau chaque saison pour garantir que leurs informations sont à jour (adresse, téléphone, consentements RGPD, etc.).

## Installation

### Prérequis

- Python 3.8 ou supérieur
- PyQt5
- pandas
- reportlab (pour l'export PDF)
- SQLite3 (généralement inclus avec Python)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :

```bash
pip install PyQt5 pandas reportlab
```

### Lancement de l'application

```bash
python -m club_manager.main
```

Ou depuis le répertoire du projet :

```bash
python club_manager/main.py
```

## Utilisation

### Gestion des membres

1. Accédez à l'onglet **"Membres"**
2. Cliquez sur **"Ajouter"** pour créer un nouveau membre
3. Remplissez le formulaire avec les informations de l'adhérent
4. Les champs obligatoires incluent :
   - Nom et prénom
   - Consentement RGPD
5. Choisissez le type de paiement :
   - **Club + MJC** : Paiement global
   - **Club uniquement** : Si la part MJC a été réglée dans un autre club MJC (sélectionner le club)
6. Saisissez le montant ANCV si applicable
7. Indiquez le statut de cotisation (Non payée, Payée, Partiellement payée)
8. Cliquez sur **"OK"** pour enregistrer

Le tableau se rafraîchit automatiquement après l'ajout.

### Gestion des prix annuels

1. Accédez à l'onglet **"Prix annuels"**
2. Cliquez sur **"Ajouter"** pour définir les prix d'une nouvelle année
3. Remplissez :
   - **Année** (ex: 2024-2025)
   - **Prix Club**
   - **Prix MJC**
   - Cochez "Définir comme année courante" si nécessaire
4. Cliquez sur **"Ajouter"** pour enregistrer

### Gestion des clubs MJC

1. Accédez à l'onglet **"Clubs MJC"**
2. Saisissez le nom d'un club MJC partenaire
3. Cliquez sur **"Ajouter"** pour l'enregistrer
4. Ces clubs apparaîtront dans le formulaire membre pour les adhérents ayant réglé leur part MJC ailleurs

#### Import en masse de clubs MJC (Nouveau v2.3)

Pour importer plusieurs clubs d'un coup :

1. Cliquez sur **"Importer/Coller une liste"**
2. Deux options :
   - **Copier-coller** : Collez une liste de clubs (un par ligne)
   - **Depuis un fichier** : Cliquez sur "Charger depuis un fichier" et sélectionnez un fichier .txt
3. Les doublons sont automatiquement ignorés
4. Un rapport indique le nombre de clubs ajoutés et ignorés

Format du fichier texte :
```
MJC Centre
MJC Nord
MJC Sud
```

### Note sur les Sessions et Cotisations

L'onglet Sessions a été supprimé de l'interface. Le système multi-bases (une base = une saison) remplace maintenant complètement la fonctionnalité de sessions. Les données de sessions restent disponibles dans la base pour la compatibilité, mais l'interface de gestion a été retirée pour simplifier l'utilisation.

L'onglet Cotisations a également été supprimé. La gestion des paiements est maintenant intégrée directement dans le formulaire membre avec :
- Type de paiement (Club+MJC ou Club uniquement)
- Montant ANCV
- Statut de cotisation
- Référence au club MJC si la part MJC a été réglée ailleurs

## Sauvegarde et restauration

### Créer une sauvegarde

- **Fichier → Exporter une sauvegarde...**
- Choisissez un emplacement et un nom pour le fichier de sauvegarde

### Export ZIP complet (Nouveau v2.3)

Pour créer une archive complète de votre base :

1. Accédez à l'onglet **"Sauvegarde"**
2. Cliquez sur **"Exporter (zip)"**
3. Choisissez l'emplacement pour l'archive
4. L'archive contient :
   - La base de données complète
   - La configuration de l'application

### Restaurer une sauvegarde

- **Fichier → Restaurer une sauvegarde...**
- Sélectionnez le fichier de sauvegarde
- **Attention** : Cette opération remplacera les données actuelles

### Import ZIP (Nouveau v2.3)

Pour restaurer une archive ZIP :

1. Accédez à l'onglet **"Sauvegarde"**
2. Cliquez sur **"Importer (zip)"**
3. Sélectionnez l'archive à importer
4. Choisissez où enregistrer la base restaurée
5. Option de restaurer ou non la configuration

## Exports de données

### Export CSV

1. Accédez à l'onglet **"Exports"**
2. Cliquez sur **"Exporter CSV"**
3. Sélectionnez le type de données (Membres, Postes, Clubs MJC, Prix annuels)
4. Choisissez l'emplacement du fichier

### Export PDF (Nouveau v2.3)

Pour créer un export PDF professionnel :

1. Accédez à l'onglet **"Exports"**
2. Cliquez sur **"Exporter PDF"**
3. Sélectionnez le type de données à exporter
4. Choisissez d'exporter tous les champs ou seulement certains
5. Si sélection : cochez les champs souhaités
6. Le PDF généré contient :
   - En-tête avec titre et date
   - Table formatée avec vos données
   - Total d'éléments exportés

## Mailing groupé

### Utilisation (Nouveau v2.3 : champ Objet)

1. Accédez à l'onglet **"Mailing"**
2. Cliquez sur **"Sélection destinataires"** pour choisir les membres
3. Remplissez le champ **"Objet"** (obligatoire)
4. Rédigez votre message dans le champ corps
5. Cliquez sur **"Prévisualiser"** pour voir le rendu final
6. Cliquez sur **"Envoyer"** pour envoyer le mail

Note : La fonctionnalité d'envoi nécessite une configuration SMTP (à venir).

## Conformité RGPD

L'application respecte le RGPD et vous aide à le faire :

- Consentement obligatoire lors de l'ajout d'un membre
- Droit à l'image géré séparément
- Fonction de purge des données anciennes (disponible dans l'onglet concerné)
- Export des données personnelles d'un membre sur demande

## Support et contribution

Pour signaler un bug ou proposer une amélioration :
- Ouvrez une issue sur le dépôt GitHub
- Contactez l'équipe de développement

## Licence

© 2024 DarkSario - Club Manager
Tous droits réservés.

## Historique des versions

### Version 2.3 (Décembre 2024)
- ✨ **Export/Import ZIP complet** : Sauvegarde et restauration complète avec barre de progression
- ✨ **Export PDF professionnel** : Export des données au format PDF avec sélection de champs
- ✨ **Champ Objet dans Mailing** : Ajout d'un champ sujet éditable pour les mails groupés
- ✨ **Import de liste de clubs MJC** : Import en masse par copier-coller ou fichier texte
- 📦 Nouvelle dépendance : reportlab pour la génération PDF
- 📝 Documentation complète dans IMPLEMENTATION_V2.3.md
- ✅ Tests complets pour toutes les nouvelles fonctionnalités

### Version 2.2 (Novembre 2024)
- ✨ **Gestion annuelle des prix Club/MJC** : Configuration des prix pour chaque année
- ✨ **Gestion des clubs MJC** : Enregistrement des clubs MJC partenaires
- ✨ **Amélioration du formulaire membre** : 
  - Type de paiement (Club+MJC ou Club uniquement)
  - Sélection du club MJC si part réglée ailleurs
  - Montant ANCV
  - Statut de cotisation intégré
- 🔧 **Suppression de l'onglet Cotisations** : Logique intégrée dans le formulaire membre
- 🔧 **Suppression de l'onglet Champs personnalisés** : Simplification de l'interface
- 📝 Mise à jour de la documentation

### Version 2.1 (Octobre 2024)
- ✨ **Suppression de l'onglet Sessions** : Le système multi-bases remplace complètement les sessions
- ✨ **Business logic complète** : Implémentation CRUD complète pour tous les onglets
- ✨ **Feedbacks utilisateur** : Dialogues de confirmation, validation, messages de succès/erreur
- 🔧 Édition de membres, cotisations, postes et champs personnalisés
- 🔧 Suppression avec confirmation pour toutes les entités
- 🔧 Export CSV pour membres, cotisations, postes et champs personnalisés
- 🔧 Affectation de postes aux membres
- 🔧 Relance automatique pour les paiements en retard
- 📝 Docstrings complètes sur toutes les méthodes

### Version 2.0 (Octobre 2024)
- ✨ **Nouveau système multi-bases** : Une base par saison/année
- ✨ Dialogue de sélection de base au démarrage
- ✨ Menu pour changer de base à tout moment
- ✨ Stockage du chemin de la dernière base utilisée
- 🔧 Actualisation automatique des tableaux après ajout de membres
- 🔧 Actualisation automatique des tableaux après ajout de cotisations
- 🔧 Validation des montants comme nombres décimaux
- 🔧 Affichage/saisie du numéro de chèque pour les paiements par chèque
- 🔧 Ajout du champ `cheque_number` dans la table cotisations
- 📝 Documentation complète du nouveau système multi-bases

### Version 1.0 (Initial)
- Gestion des membres, cotisations, sessions
- Exports CSV/PDF
- Système d'audit
- Conformité RGPD de base
