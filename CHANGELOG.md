# Historique des versions - Club Manager

## Version 2.5.0

### Ce qui change

- **Tests & CI** : suite pytest (unitaires, `tests/integration/`, UI PyQt5 marker `ui` en mode headless), couverture
  ≥ 70 % sur `club_manager/core/` (seuil CI), workflows GitHub Actions `tests.yml` et `release.yml`
  (déclenchables via `workflow_dispatch`, mode *dry-run* pour la release, `contents: write` limité au job de publication).
- **Logging centralisé** (rotation) dans `<CLUBMANAGER_LOG_DIR>/clubmanager.log`, initialisé au démarrage
  (version de l'application et base ouverte journalisées). Plus de `print()` dans `club_manager/core/`.
- **Configuration** via `Config` et fichier `.env` (voir `.env.example`, README et DEVELOPMENT.md).
- **Migrations** : version du schéma dans `PRAGMA user_version`, chaque migration est **atomique**
  (`BEGIN`/`COMMIT`/`ROLLBACK`, `user_version` mis à jour dans la même transaction). En cas d'échec : rollback complet,
  `user_version` inchangé, erreur journalisée puis relancée.
- **Fusion `exports.py` → `export.py`**.
- **Validation stricte** des colonnes (`add_member`/`update_member`) et des clés de filtre
  (`get_filtered_members` lève `ValueError` pour une clé inconnue).
- **SMTP** : avertissement (log + message dans la fenêtre de configuration SMTP) si `APP_SECRET_KEY` n'est pas défini ;
  les mots de passe chiffrés avec l'ancienne clé par défaut restent lisibles.
- **Python 3.9+** requis (3.9 à 3.12 testés ; 3.8 n'est plus supporté).
- Corrections : `purge_rgpd` ne référence plus les colonnes supprimées (`health`, `external_club`, `mjc_elsewhere`) ;
  ajout de `Database.get_current_db_path()` utilisé par l'export ZIP.

### Guide d'upgrade

1. **Sauvegardez** vos bases (`*.db`, dossier `~/.clubmanager`) avant la mise à jour.
2. Utilisez **Python 3.9 ou supérieur**, puis installez les dépendances : `pip install -r requirements.txt`
   (développement : `pip install -r requirements-dev.txt`).
3. Copiez `.env.example` en `.env` si besoin et **définissez `APP_SECRET_KEY`** *avant* de ré-enregistrer la
   configuration SMTP (`python -c "import secrets; print(secrets.token_urlsafe(48))"`). Tant que la clé n'est pas
   définie, la clé par défaut (non sécurisée) est utilisée. Si vous définissez la clé après coup, l'ancien mot de passe
   reste lisible ; ré-enregistrez la configuration SMTP pour le rechiffrer avec la nouvelle clé.
4. Lancez l'application : les **migrations s'appliquent automatiquement** à l'ouverture de chaque base.
5. Remplacez les imports `club_manager.core.exports` par `club_manager.core.export`.

### Points de rupture possibles

- Python 3.8 n'est plus supporté.
- `club_manager.core.exports` n'existe plus (utiliser `club_manager.core.export`).
- `get_filtered_members` lève `ValueError` pour une clé inconnue (auparavant ignorée silencieusement) ;
  clés autorisées : `last_name`, `first_name`, `city`, `mail`, `cotisation_status`, `payment_type`, `rgpd`, `image_rights`.
- `add_member`/`update_member` lèvent `ValueError` pour une colonne inconnue.
- Les colonnes `health` et `external_club` sont supprimées de `members` (migration 3).

## Version 2.4 (En cours)

### 🚀 Nouvelles fonctionnalités

#### **Intégration SMTP complète et mailing centralisé**

L'application dispose maintenant d'un système d'envoi d'emails complet et sécurisé.

**Configuration SMTP:**
- Interface de configuration SMTP accessible depuis l'onglet Mailing (bouton ⚙ Configuration SMTP)
- Support de plusieurs modes de sécurité: Aucune, STARTTLS, SSL/TLS
- Chiffrement des mots de passe avec cryptographie Fernet
- Paramètres configurables:
  - Serveur SMTP (hôte, port)
  - Authentification (nom d'utilisateur, mot de passe)
  - Informations expéditeur (adresse email, nom, répondre à)
  - Envoi par lots (taille du lot, délai entre lots)
  - Nombre de tentatives en cas d'échec
  - Activation/désactivation des logs d'envoi
- Fonctions de test:
  - Test de connexion SMTP
  - Envoi d'email de test

**Envoi d'emails groupés:**
- Sélection des destinataires depuis la liste des membres
- Composition avec objet et corps du message
- Prévisualisation avant envoi
- Envoi par lots pour respecter les limitations SMTP
- Barre de progression en temps réel
- Retry automatique en cas d'échec temporaire
- Rapport détaillé des envois (succès et échecs)

**Logs d'envoi:**
- Table `mailing_logs` pour tracer tous les envois
- Enregistrement des destinataires, sujets, statuts et erreurs
- Horodatage de chaque envoi

**Sécurité:**
- Mots de passe chiffrés dans la base de données
- Clé de chiffrement dérivée de la variable d'environnement `APP_SECRET_KEY`
- Documentation sur la configuration de la clé en production

**Modifications de l'interface:**
- Bouton "Ouvrir Mailing" dans l'onglet Membres (au lieu de "Mailing")
- Texte d'aide dans l'onglet Mailing expliquant le fonctionnement
- Messages d'erreur explicites si la configuration SMTP n'est pas définie

### 🗄️ Modifications de la base de données

- Nouvelle table `settings` pour stocker les configurations (clé/valeur)
- Nouvelle table `mailing_logs` pour l'historique des envois
- Migration automatique lors de l'ouverture d'une base existante

### 📦 Nouvelles dépendances

- `cryptography` : Pour le chiffrement des mots de passe SMTP

### 🧪 Tests

- Suite de tests unitaires complète pour le module SMTP
- Tests de chiffrement/déchiffrement des mots de passe
- Tests de connexion SMTP (mocké)
- Tests d'envoi en masse avec retry
- Tests de sauvegarde/chargement de configuration

### 📝 Documentation

- Instructions de configuration SMTP dans le README
- Documentation de la variable d'environnement APP_SECRET_KEY
- Guide d'utilisation du mailing groupé

---

## Version 2.3 (Décembre 2024)
- ✨ **Export/Import ZIP complet** : Sauvegarde et restauration complète avec barre de progression
- ✨ **Export PDF professionnel** : Export des données au format PDF avec sélection de champs
- ✨ **Champ Objet dans Mailing** : Ajout d'un champ sujet éditable pour les mails groupés
- ✨ **Import de liste de clubs MJC** : Import en masse par copier-coller ou fichier texte
- 📦 Nouvelle dépendance : reportlab pour la génération de fichiers PDF
- 📝 Documentation complète dans IMPLEMENTATION_V2.3.md
- ✅ Tests complets pour toutes les nouvelles fonctionnalités

## Version 2.2 (Novembre 2024)
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

## Version 2.1 (Octobre 2024)
- ✨ **Suppression de l'onglet Sessions** : Le système multi-bases remplace complètement les sessions
- ✨ **Business logic complète** : Implémentation CRUD complète pour tous les onglets
- ✨ **Feedbacks utilisateur** : Dialogues de confirmation, validation, messages de succès/erreur
- 🔧 Édition de membres, cotisations, postes et champs personnalisés
- 🔧 Suppression avec confirmation pour toutes les entités
- 🔧 Export CSV pour membres, cotisations, postes et champs personnalisés
- 🔧 Affectation de postes aux membres
- 🔧 Relance automatique pour les paiements en retard
- 📝 Docstrings complètes sur toutes les méthodes

## Version 2.0 (Octobre 2024)
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

## Version 1.0 (Initial)
- Gestion des membres, cotisations, sessions
- Exports CSV/PDF
- Système d'audit
- Conformité RGPD de base
