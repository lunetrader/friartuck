"""Authentication for friartuck Robinhood Python Access for API version 1.431.4"""
import json
import os
import pickle
import uuid

import requests

import config

DEVICE_TOKEN = None
LOGGED_IN = False
SESSION = requests.Session()
EXPIRATION_EPOCH_TIME = None

SESSION.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://robinhood.com/",
    "Content-Type": "application/json",
    "X-Robinhood-API-Version": "1.431.4",
    "Origin": "https://robinhood.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers"
}

def login(
    username=config.ROBINHOOD_USERNAME,
    password=config.ROBINHOOD_PASSWORD,
    mfa_code=None,
    session_expiration_seconds=config.SESSION_EXPIRATION_SECONDS,
    session_expiration_tolerance=config.SESSION_EXPIRATION_TOLERANCE):
    """Login to Robinhood API. If already logged in, there is no effect. 
    To reset session expiration you must run friartuck.auth.logout() 
    and then friartuck.auth.login(). If you do not provide an MFA code
    the function will try to load the current session from the 
    SESSION_FILE saved session. Session will be purged if the expiration 
    time is less than 14400 (default). You can adjust it downward.
    """

    # Try loading pickle file


    if os.path.exists(config.SESSION_FILE):
        saved_session = pickle.load(config.SESSION_FILE, 'rb')


    url = 'https://api.robinhood.com/oauth2/token/'

    payload = {
        "device_token": f'{uuid.uuid4()}',
        "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
        "expires_in": 86400,
        "grant_type": "password",
        "scope": "internal",
        "username": username,
        "password": password,
        "al_pk": "7F867EDC-C71B-467F-B0A1-8DCBA5D4D2E3",
        "al_token": "382638d246336f551.5063349101|r=us-east-1|metabgclr=transparent|guitextcolor=%23000000|metaiconclr=%23555555|meta=3|meta_height=456|meta_width=327|pk=7F867EDC-C71B-467F-B0A1-8DCBA5D4D2E3|at=40|sup=1|rid=85|atp=2|cdn_url=https%3A%2F%2Frobinhood-api.arkoselabs.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-us-east-1.arkoselabs.com|surl=https%3A%2F%2Frobinhood-api.arkoselabs.com|smurl=https%3A%2F%2Frobinhood-api.arkoselabs.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager"
    }

    if mfa_code:
        payload["try_passkeys"] = False
        payload["mfa_code"] = mfa_code

    json_payload = json.dumps(payload)
    res = SESSION.post(url, data=json_payload)

    return res.text

def logout():


if __name__ == "__main__":
    login()
    mfa_code = int(input("MFA code: "))
    login(mfa_code=mfa_code)