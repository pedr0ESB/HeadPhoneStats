from flask import Flask
from routes.home.homeRoute import *
from routes.busca.buscaRoute import *
import os 

load_dotenv()

mhsApp = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY') 
mhsApp.secret_key = SECRET_KEY 

#Registro da rota do logon

mhsApp.register_blueprint(Logon)

#Registro da rota de Busca

mhsApp.register_blueprint(BuscMSZ)

