import requests

import friartuck_config

# pickle file
# {"device_token": token, "token_type": bearer, "access_token": 1, "expiration_epoch": 12332.4, "refresh_token": rt}

class FriarTuck:
    def __init__(self, mfa_code=None):
        # Robinhood Login credentials
        self.username = friartuck_config.ROBINHOOD_USERNAME
        self.password = friartuck_config.ROBINHOOD_PASSWORD
        self.mfa_code = mfa_code

        # Authorization timeout constraints
        self.session_expiration_seconds = friartuck_config.SESSION_EXPIRATION_SECONDS
        self.session_expiration_tolerance = friartuck_config.SESSION_EXPIRATION_TOLERANCE
        self.session_expiration_epoch_time = None

        # Authorization persistence
        self.session_file = friartuck_config.SESSION_FILE

        # HTTPS Session
        self.session = requests.session()
        self.session.headers = {
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

    def load_session(self):
        print('hi')
        pass
        
    def login(self, mfa_code=None):
        payload = {
            "device_token": None,
            "client_id": "c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS",
            "expires_in": 86400,
            "grant_type": "password",
            "scope": "internal",
            "username": self.username,
            "password": self.password
        }

        if mfa_code:
            payload["try_passkeys"] = False
            payload["mfa_code"] = mfa_code

        json_payload = json.dumps(payload)
        res = SESSION.post(url, data=json_payload)

        return res.text

    def logout(self):
        pass

    def get_open_option_orders(self):
        pass

    def get_open_option_positions(self):
        pass

