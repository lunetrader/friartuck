"""Authentication functions for friartuck Robinhood Python Access for API version 1.431.4"""
import json
import os
import pickle
import time
import uuid

import requests

import config

SESSION = requests.Session()
SESSION_EXPIRATION_EPOCH = None
DEVICE_TOKEN = None
LOGGED_IN = False

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
    url = 'https://api.robinhood.com/oauth2/token/'

    payload = {
        "device_token": None,
        "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
        "expires_in": 86400,
        "grant_type": "password",
        "scope": "internal",
        "username": username,
        "password": password,
        "al_pk": "7F867EDC-C71B-467F-B0A1-8DCBA5D4D2E3",
        "al_token": "382638d246336f551.5063349101|r=us-east-1|metabgclr=transparent|guitextcolor=%23000000|metaiconclr=%23555555|meta=3|meta_height=456|meta_width=327|pk=7F867EDC-C71B-467F-B0A1-8DCBA5D4D2E3|at=40|sup=1|rid=85|atp=2|cdn_url=https%3A%2F%2Frobinhood-api.arkoselabs.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-us-east-1.arkoselabs.com|surl=https%3A%2F%2Frobinhood-api.arkoselabs.com|smurl=https%3A%2F%2Frobinhood-api.arkoselabs.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager"
    }

    # pickle file should have an epoch time that is the expiration time

    # Try loading session pickle file
        # two checks:
        # is session expiration below cutoff
        # call a real credentialed function to verify token is live
            # if both pass
                # set authorized headeres
                # return out of function if both pass
                # return dict with success and time to expiration
    
    # if that fails
    # login normally with mfa
        # if that works
            # set authorized headers
            # save pickle file

    # pickle file
    {"device_token": token, "token_type": bearer, "access_token": 1, "expiration_epoch": 12332.4, "refresh_token": rt}

    if os.path.exists(config.SESSION_FILE):
        saved_session = pickle.load(config.SESSION_FILE, 'rb')
        payload['Authorization'] = f"{saved_session['token_type']} {saved_session['access_token']}"
        
        SESSION_EXPIRATION_EPOCH = float(payload['expiration_epoch'])
        
        if (SESSION_EXPIRATION_EPOCH - time.time()) < session_expiration_tolerance:
            

    else:
        pass




    else:
        print("No pickle file found. Moving to attempt new session login.")

    if mfa_code:
        payload["try_passkeys"] = False
        payload["mfa_code"] = mfa_code

    json_payload = json.dumps(payload)
    res = SESSION.post(url, data=json_payload)

    return res.text

def logout():
    """Logs out of Robinhood and deletes session data."""
    pass

if __name__ == "__main__":
    login()
    mfa_code = int(input("MFA code: "))
    login(mfa_code=mfa_code)