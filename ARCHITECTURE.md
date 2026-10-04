# Architecture de Club Manager

Application desktop PyQt5 avec une base SQLite par saison.

```
club_manager/
├── main.py, main_window.py   # Point d'entrée et fenêtre principale
├── config.py                 # Classe Config (variables d'environnement / .env)
├── core/                     # Logique métier (sans dépendance UI sauf dialogues d'export)
│   ├── database.py           # Singleton Database (SQLite, thread-safe)
│   ├── migrations.py         # MigrationManager (versions de schéma)
│   ├── logger.py             # Logging centralisé avec rotation
│   ├── members.py            # CRUD / filtres des membres
│   ├── export.py             # Exports CSV/PDF, prévisualisation, traductions de champs
│   ├── smtp_util.py          # Configuration et envoi SMTP (mot de passe chiffré Fernet)
│   └── ...                   # backup, audit, cotisations, mailing, rgpd, etc.
└── ui/                       # Onglets et dialogues (fichiers *_ui.py générés)
tests/                        # Tests pytest
```

## Base de données

`Database.instance(path)` retourne l'instance active ; `Database.change_database(path)` change de saison.
La connexion utilise `check_same_thread=False` : l'accès concurrent n'est pas sérialisé au-delà du
singleton, il n'y a pas de pool de connexions.

## Migrations

La version du schéma est stockée dans `PRAGMA user_version`. `MigrationManager.migrate()` applique, dans l'ordre,
les migrations enregistrées dans `MIGRATIONS` :

| Version | Description |
|---------|-------------|
| 1 | Champs de paiement (`cash_amount`, `check1..3_amount`, `total_paid`) |
| 2 | `birth_date`, `other_mjc_clubs` |
| 3 | Suppression de `health` et `external_club` |

Pour ajouter une migration : écrire une fonction `(connection) -> None` et l'enregistrer avec le numéro suivant.

## Configuration

Variables : `CLUBMANAGER_DATA_DIR`, `CLUBMANAGER_LOG_DIR`, `CLUBMANAGER_LOG_LEVEL`, `CLUBMANAGER_DB_PATH`,
`APP_SECRET_KEY` (voir `.env.example`).

## Logging

`get_logger(__name__)` retourne un logger enfant de `clubmanager`, écrit sur la console et dans
`~/.clubmanager/logs/clubmanager.log` (rotation 1 Mo × 5).
