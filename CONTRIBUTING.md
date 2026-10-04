# Contribuer à Club Manager

1. Forkez le dépôt et créez une branche (`feature/ma-fonctionnalite`).
2. Installez les dépendances de développement : `pip install -r requirements-dev.txt`.
3. Ajoutez des tests pour toute modification de la logique métier.
4. Vérifiez : `pytest`, `black`, `flake8`, `pylint`, `mypy` (voir [DEVELOPMENT.md](DEVELOPMENT.md)).
5. Mettez à jour la documentation et le `CHANGELOG.md` si nécessaire.
6. Ouvrez une Pull Request décrivant le changement.

Ne committez jamais de secrets (`.env`, mots de passe SMTP) ni de bases de données (`*.db`).
