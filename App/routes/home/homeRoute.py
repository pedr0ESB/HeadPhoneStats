from flask import Blueprint, render_template, url_for, session, request
from Controllers.WebServiceSpotify import *

# ROTAS DA PÁGINA HOME 

Logon = Blueprint('Home', __name__)

# -> ROTA Logon <- #

@Logon.route('/')
def home():
    return acceptTermsSpotify()

# callback do spotify 

@Logon.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        session['auth_code'] = code
    return redirect(url_for('Home.token_page'))


@Logon.route('/Home')
def token_page():
    code = session['auth_code']
    if not code:
        return "Erro: Código de autorização não encontrado.", 400
    
    token = token_session(code)
    session['token'] = token
    return render_template('index.html')




