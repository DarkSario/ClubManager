# Guide de développement

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

## Lancer l'application

```bash
python -m club_manager.main
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

## Tests

```bash
pytest                      # inclut la couverture (seuil CI : 70 %)
QT_QPA_PLATFORM=offscreen pytest   # environnement sans écran
```

Les fixtures (`tests/conftest.py`) isolent les répertoires de données et fournissent une base temporaire (`db`).

## Qualité du code

Les modules suivis par la CI : `club_manager/config.py` et `club_manager/core/{logger,migrations,database,smtp_util,members,export}.py`.

```bash
black club_manager/config.py club_manager/core/<module>.py tests
flake8 <fichiers>
pylint --rcfile=.pylintrc <fichiers>
mypy
```

Configuration : `.pylintrc`, `.flake8`, `pyproject.toml`.

## Conventions

- Utiliser `get_logger(__name__)` à la place de `print()`.
- Type hints et docstrings sur les fonctions publiques.
- Chemins et réglages via `club_manager.config.Config`.
- Évolutions de schéma via `core/migrations.py`.
- Ne pas modifier à la main les fichiers `*_ui.py` générés si possible.

## CI/CD

`.github/workflows/tests.yml` (Python 3.9–3.12 : pylint, flake8, black, mypy, pytest + codecov) et
`.github/workflows/release.yml` (release sur tag `v*`).

### Tester les workflows sans publier

- **Manuellement** : onglet *Actions* → *Tests* ou *Release* → *Run workflow*. Pour *Release*, laissez `dry_run`
  à `true` (défaut) : tests et build sont exécutés mais aucune release n'est créée.
- **Avec un tag de test** : `git tag v2.5.0-test && git push origin v2.5.0-test` déclenche *Release* ; supprimez ensuite
  la release et le tag (`git push --delete origin v2.5.0-test`).
- Les permissions sont `contents: read` par défaut ; seul le job `publish` a `contents: write`.

### Tests UI

Les tests PyQt5 (marker `ui`) tournent en mode headless (`QT_QPA_PLATFORM=offscreen`, défini dans `tests/conftest.py`).
Sous Ubuntu : `sudo apt-get install -y libgl1 libegl1 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 libxcb-xfixes0`.
Exclure les tests UI : `pytest -m "not ui"`.
