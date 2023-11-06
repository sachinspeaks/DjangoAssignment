import os
import json
import requests
import firebase_admin

from django.contrib.auth.models import User
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication

from .exceptions import FirebaseError
from .exceptions import InvalidAuthToken

cred_obj = {
    "type": "service_account",
    "project_id": os.environ.get("PROJECT_ID"),
    "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
    "private_key": os.environ.get("PRIVATE_KEY"),
    "client_email": os.environ.get("CLIENT_EMAIL"),
    "client_id": os.environ.get("CLIENT_ID"),
    "auth_uri": os.environ.get("AUTH_URI"),
    "token_uri": os.environ.get("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("CLIENT_X509_CERT_URL"),
    "universe_domain": os.environ.get("UNIVERSE_DOMAIN"),
}

cred = credentials.Certificate(cred_obj)

default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return None

        custom_token = auth_header.split(" ").pop()

        api_key = os.environ.get("API_KEY")
        token_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={api_key}"

        response = requests.post(
            token_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"token": custom_token, "returnSecureToken": True}),
        )
        response_data = response.json()

        id_token = response_data.get("idToken")

        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as e:
            print(e)
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            user = User.objects.get(username=decoded_token['uid'])
            return user
        except Exception as e:
            print(e)
            raise FirebaseError() 
