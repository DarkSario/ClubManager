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

- Python 3.9 ou supérieur
- PyQt5
- pandas
- reportlab (pour les exports PDF)
- cryptography (pour le chiffrement des mots de passe SMTP)
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

## Variables d'environnement et fichier `.env`

Copiez `.env.example` en `.env` (à la racine du projet) puis adaptez les valeurs :

```bash
cp .env.example .env
```

| Variable | Rôle | Valeur par défaut |
|----------|------|-------------------|
| `CLUBMANAGER_DATA_DIR` | Répertoire de données | `~/.clubmanager` |
| `CLUBMANAGER_LOG_DIR` | Répertoire des logs (`clubmanager.log`) | `<CLUBMANAGER_DATA_DIR>/logs` |
| `CLUBMANAGER_LOG_LEVEL` | Niveau de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO` |
| `CLUBMANAGER_DB_PATH` | Base utilisée quand aucune n'est sélectionnée | `club_manager.db` |
| `APP_SECRET_KEY` | Clé de chiffrement du mot de passe SMTP | non définie (clé par défaut non sécurisée, avertissement) |

**Ordre de précédence** : variable d'environnement > fichier `.env` > valeur par défaut.

Générer une clé secrète robuste :

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

⚠️ Ne committez **jamais** votre fichier `.env` (il est ignoré par Git) : il contient des secrets.
Définissez `APP_SECRET_KEY` **avant** d'enregistrer (ou ré-enregistrer) la configuration SMTP.

## Configuration, logs et développement

- Configuration par variables d'environnement ou fichier `.env` (voir `.env.example`, classe `club_manager/config.py`).
- Logs : `~/.clubmanager/logs/clubmanager.log` (rotation automatique).
- Tests : `pip install -r requirements-dev.txt && pytest`.
- Voir [ARCHITECTURE.md](ARCHITECTURE.md), [DEVELOPMENT.md](DEVELOPMENT.md) et [CONTRIBUTING.md](CONTRIBUTING.md).

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

### Configuration SMTP

Avant de pouvoir envoyer des emails, vous devez configurer les paramètres SMTP :

1. Accédez à l'onglet **"Mailing"**
2. Cliquez sur **"⚙ Configuration SMTP"**
3. Remplissez les informations du serveur SMTP :
   - **Hôte SMTP** : L'adresse de votre serveur SMTP (ex: `smtp.gmail.com`, `smtp.office365.com`)
   - **Port** : Le port SMTP (587 pour STARTTLS, 465 pour SSL/TLS)
   - **Sécurité** : Choisissez le type de sécurité (STARTTLS recommandé)
   - **Nom d'utilisateur** : Votre identifiant SMTP
   - **Mot de passe** : Votre mot de passe SMTP
   - **Adresse email** : L'adresse email expéditeur
   - **Nom expéditeur** : Le nom qui apparaîtra comme expéditeur
   - **Répondre à** : Adresse pour les réponses (optionnel)

4. Configurez les paramètres d'envoi :
   - **Taille du lot** : Nombre d'emails envoyés par lot (défaut: 10)
   - **Délai entre lots** : Temps d'attente entre chaque lot en ms (défaut: 1000ms)
   - **Tentatives max** : Nombre de tentatives en cas d'échec (défaut: 2)
   - **Logs d'envoi** : Activer pour tracer les envois dans la base

5. Testez votre configuration :
   - Cliquez sur **"Tester la connexion"** pour vérifier les paramètres
   - Cliquez sur **"Envoyer un email de test"** pour recevoir un email de test

6. Cliquez sur **"OK"** pour enregistrer

#### Sécurité des mots de passe

Les mots de passe SMTP sont chiffrés dans la base de données en utilisant la bibliothèque `cryptography` (Fernet).

**Pour une sécurité maximale en production** :

1. Définissez une variable d'environnement `APP_SECRET_KEY` avec une valeur unique et complexe :

```bash
# Linux/Mac
export APP_SECRET_KEY="votre-clé-secrète-très-longue-et-complexe"

# Windows
set APP_SECRET_KEY=votre-clé-secrète-très-longue-et-complexe
```

2. Lancez l'application :

```bash
python -m club_manager.main
```

⚠️ **Important** : Sans cette variable d'environnement, une clé par défaut est utilisée. Cela convient pour les tests, mais **pas pour la production** où des données sensibles sont manipulées.

### Utilisation du mailing groupé

1. Accédez à l'onglet **"Mailing"**
2. Cliquez sur **"Sélection destinataires"** pour choisir les membres
   - Seuls les membres avec une adresse email sont affichés
   - Vous pouvez sélectionner plusieurs membres
3. Remplissez le champ **"Objet"** (obligatoire)
4. Rédigez votre message dans le champ corps
5. Cliquez sur **"Prévisualiser"** pour voir le rendu final
6. Cliquez sur **"Envoyer"** pour envoyer le mail
   - Une barre de progression affiche l'avancement de l'envoi
   - Un rapport détaillé est affiché à la fin :
     - Nombre d'emails envoyés avec succès
     - Nombre d'échecs avec les détails des erreurs

### Fonctionnalités avancées

- **Envoi par lots** : Les emails sont envoyés par lots pour éviter les limitations SMTP et réduire la charge serveur
- **Retry automatique** : En cas d'échec temporaire, le système réessaye automatiquement
- **Logs d'envoi** : Si activés, tous les envois sont enregistrés dans la table `mailing_logs` pour audit
- **Protection des destinataires** : Chaque email est envoyé individuellement pour préserver la confidentialité

### Depuis l'onglet Membres

Le bouton **"Ouvrir Mailing"** dans l'onglet Membres vous redirige vers l'onglet Mailing où vous pouvez composer et envoyer vos emails.

Note : La fonctionnalité d'envoi nécessite une configuration SMTP préalable.

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

### Version 2.4 (Janvier 2025)
- ✨ **Intégration SMTP complète** : Configuration et envoi d'emails via SMTP
- ✨ **Mailing centralisé** : Interface complète de composition et d'envoi d'emails groupés
- ✨ **Chiffrement des mots de passe** : Stockage sécurisé des credentials SMTP avec cryptography
- ✨ **Envoi par lots** : Configuration des lots et délais pour respecter les limitations SMTP
- ✨ **Retry automatique** : Tentatives automatiques en cas d'échec temporaire
- ✨ **Logs d'envoi** : Traçabilité complète des emails envoyés
- ✨ **Tests de configuration** : Test de connexion et envoi d'email de test
- 📦 Nouvelle dépendance : cryptography pour le chiffrement
- 🗄️ Nouvelles tables : settings, mailing_logs
- 📝 Documentation complète dans CHANGELOG.md
- ✅ Suite de tests unitaires pour le module SMTP

### Version 2.3 (Décembre 2024)
- ✨ **Export/Import ZIP complet** : Sauvegarde et restauration complète avec barre de progression
- ✨ **Export PDF professionnel** : Export des données au format PDF avec sélection de champs
- ✨ **Champ Objet dans Mailing** : Ajout d'un champ sujet éditable pour les mails groupés
- ✨ **Import de liste de clubs MJC** : Import en masse par copier-coller ou fichier texte
- 📦 Nouvelle dépendance : reportlab pour la génération de fichiers PDF
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
