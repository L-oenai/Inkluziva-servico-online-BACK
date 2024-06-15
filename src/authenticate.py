from flask import jsonify
import oauth2 as oauth
import urllib.parse
import os

from dotenv import load_dotenv

load_dotenv()

consumer_key_env = os.getenv("CONSUMER_KEY")
consumer_secret_env = os.getenv("CONSUMER_SECRET")
request_token_url_env = os.getenv("REQUEST_TOKEN_URL")
authenticate_url_env = os.getenv("AUTHENTICATE_URL")
access_token_url_env = os.getenv("ACCESS_TOKEN_URL")

consumer_key = consumer_key_env
consumer_secret = consumer_secret_env

# Configuração da URL para requisição de autenticação
request_token_url = request_token_url_env
authenticate_url = authenticate_url_env
access_token_url = access_token_url_env

# Criando um cliente OAuth
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

# Solicitando oauth_token
resp_oauth_token, content_oauth_token = client.request(request_token_url, 'GET')
if resp_oauth_token['status'] != '200':
    raise Exception('Falha ao obter token de requisição: %s' % resp_oauth_token['status'])

print(f"content_oauth_token: {content_oauth_token}")

# Gerando o oauth_token
content_oauth_token_str = content_oauth_token.decode('utf-8')
oauth_token_params = urllib.parse.parse_qs(content_oauth_token_str)
oauth_token_params = {key: value[0] for key, value in oauth_token_params.items()}

oauth_token = oauth_token_params['oauth_token']

print(f"oauth_toke: {oauth_token}")
oauth_token_secret = oauth_token_params['oauth_token_secret']

# Gere o oauth_verifier
oauth_verifier_url = f"{authenticate_url}?oauth_token={oauth_token}"
print('Por favor, acesse a seguinte URL e autorize o aplicativo:')
print(oauth_verifier_url)

oauth_verifier = input('Informe a chave de verificação: ')

# # Convertendo o oauth_verifier em o oauth_token de acesso
token = oauth.Token(oauth_token, oauth_token_secret)
token.set_verifier(oauth_verifier)
client = oauth.Client(consumer, token)

resp_oauth_token_access, content_oauth_token_access = client.request(access_token_url, 'POST')
access_token = dict(urllib.parse.parse_qsl(content_oauth_token_access))

oauth_token_access_str = content_oauth_token_access.decode('utf-8')
oauth_token_access_params = urllib.parse.parse_qs(oauth_token_access_str)
oauth_token_access_params = {key: value[0] for key, value in oauth_token_access_params.items()}

oauth_token_access = oauth_token_access_params['oauth_token']
oauth_token_secret_access = oauth_token_access_params['oauth_token_secret']
user_name = oauth_token_access_params['screen_name']

print(oauth_token_access)
print(oauth_token_secret_access)
print(user_name)
