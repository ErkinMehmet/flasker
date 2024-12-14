Pour que les changements soit mis à jour automatiquement sans le besoin d'arrêter le site web

$env:FLASK_ENV = "development"
$env:FLASK_APP="hello.py"
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

git pull origin master
