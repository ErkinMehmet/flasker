from flask import Flask,render_template

# créer une instance
app=Flask(__name__)

# créer une décorateur de route
@app.route('/')
#def index():
    #return "<h1>hello world!</h1>"

def index():
    moi="Fernando"
    stuff="C'est la m<strong>**de</strong>"
    pizzas=['Pepe','Fromage','Coco',41]
    return render_template("index.html",nom=moi,contenu=stuff,pizzas=pizzas)

# localhost:5000/user/john
@app.route('/user/<name>')
def user(name):
    #return "<h1>hello {}!</h1>".format(name)
    return render_template("user.html",name=name)


# Créer une page d'erreur personalisée
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"),500