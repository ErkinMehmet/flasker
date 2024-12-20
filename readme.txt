Pour que les changements soit mis à jour automatiquement sans le besoin d'arrêter le site web

$env:FLASK_ENV = "development"
$env:FLASK_APP="app.py"
flask run


"""
Jinja HTML
fonctions de string dans Jinja
safe capitalize lower upper title trim striptags
"""

créer une clé rsa
mkdir .ssh
cd .ssh
ssh-keygen.exe

créer l'env virtuel
python -m venv venv
venv\Scripts\activate

configurer git
git config --global user.name "Fernando"
git config --global user.email "hli@fqm.ca"
git config --global push.default matching
git config --global alias.co checkout
git init
git add .
git commit -am 'initial commit'
git remote add origin git@github.com:ErkinMehmet/flasker.git
git branch -M master
git push -u origin master or git push -f origin master

mettre à jour le code sur le serveur
git pull origin master
git add .
git commit -am 'changements'
git push


Création de la bd dans le dossier instance
from hello import app, db  # Import the app and db objects
with app.app_context():
    db.create_all()

Migration de données avec flask
flask db init
flask db migrate -m 'initial migration'
flask db upgrade

Pour jouer avec la BD dans le terminal: (vu que le contexte de BD est dans une fonction, c'est plus compliqué)
flask shell (PowerShell)
(Python)
from flasker.app import create_app
app=create_app()
with app.app_context():
    .....

créer le Procfile
echo web: gunicorn app:app > Procfile

heroku login
