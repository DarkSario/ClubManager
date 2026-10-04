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

## Tests

```bash
pytest                      # inclut la couverture (seuil CI : 50 %)
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

`.github/workflows/tests.yml` (Python 3.8–3.11 : pylint, flake8, black, mypy, pytest + codecov) et
`.github/workflows/release.yml` (release sur tag `v*`).
