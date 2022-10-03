#Importar flask
from flask import Flask

#Inicializar app
app = Flask(__name__)

#Declarar la llave secreta
app.secret_key = "Esta es mi llave secreta ;)"