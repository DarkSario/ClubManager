# Club Manager

Club Manager est une application de gestion complète pour les associations sportives et clubs. Elle permet de gérer les adhérents, les cotisations, les sessions, et bien plus encore.

## Fonctionnalités principales

- **Gestion des membres** : Ajout, modification, suppression et recherche d'adhérents
- **Gestion des cotisations** : Suivi des paiements avec plusieurs méthodes (chèque, espèce, ANCV, virement)
- **Système multi-bases** : Une base de données par saison/année pour faciliter la gestion
- **Gestion des postes** : Attribution des responsabilités au sein du club
- **Exports** : Export des données en CSV ou PDF
- **Mailing** : Envoi d'emails groupés aux adhérents
- **Audit** : Traçabilité des modifications
- **Sauvegarde/Restauration** : Backup et restauration des données
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
- SQLite3 (généralement inclus avec Python)

### Installation des dépendances

```bash
pip install PyQt5
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
5. Cliquez sur **"OK"** pour enregistrer

Le tableau se rafraîchit automatiquement après l'ajout.

### Gestion des cotisations

1. Accédez à l'onglet **"Cotisations"**
2. Cliquez sur **"Ajouter"** pour enregistrer un paiement
3. Remplissez le formulaire :
   - **Montant** et **Payé** doivent être des nombres décimaux (ex: 150.50)
   - **Méthode** : Chèque, Espèce, ANCV, Virement, Autre
   - Si vous sélectionnez **"Chèque"**, le champ numéro de chèque apparaît et devient obligatoire
4. Cliquez sur **"OK"** pour enregistrer

Le tableau se met à jour automatiquement après l'ajout.

### Sessions (pour information)

Bien que le système de sessions existe toujours dans la base de données, il est maintenant secondaire par rapport au système multi-bases. Vous pouvez toujours utiliser les sessions pour organiser des périodes spécifiques au sein d'une saison (ex: trimestres, stages d'été, etc.).

## Sauvegarde et restauration

### Créer une sauvegarde

- **Fichier → Exporter une sauvegarde...**
- Choisissez un emplacement et un nom pour le fichier de sauvegarde

### Restaurer une sauvegarde

- **Fichier → Restaurer une sauvegarde...**
- Sélectionnez le fichier de sauvegarde
- **Attention** : Cette opération remplacera les données actuelles

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
