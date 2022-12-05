"""Configuration for friartuck Python Robinhood API wrapper."""
import os

# IMPORTANT
# Fill out the config file
# and rename to friartuck_config.py
# END IMPORTANT

# Robinhood credentials
ROBINHOOD_USERNAME = "your_email@your_domain.com"
ROBINHOOD_PASSWORD = "your_robinhood_password"

# Session expiration timeout in seconds. 
# Default in Robinhood API version 1.431.4 is 86400 (24 Hours)
# Robinhood does not seem to honor timeouts longer than 259200 (three days).
# If you attempt a longer expiration time than three days,
# the API will occasionally respond with a confirmation time matching
# your request, but I haven't tested if the server will in fact
# honor those longer times.
# In the spirit of honoring Robinhood's API standards, I recommend leaving
# this value at 86400 and handling your sessions and code with
# that limitation in mind.
SESSION_EXPIRATION_SECONDS = 86400

# When running auth.login(), this setting will terminate current session
# if the time to session expiration is less than this number (in seconds).
# The default (14400) remove the session if under 4 hours is left.
# It's best practice to always provide an MFA code when logging in if
# you are unsure of the time to expiration.
SESSION_EXPIRATION_TOLERANCE = 14400

# Directory and file name for storing persistent session authorization.
# Allows you to stop a script and restart without providing
# another MFA code to get a new authentication token.
# The default config is to place it in the home directory of the user
# running the script: [home]/.friartuck/session.pickle
# If this is confusing just leave it alone. It shouldn't need to be
# modified unless you have a very particular use case.
SESSION_FILE_NAME  = "session" # File name
SESSION_DIR_NAME   = ".friartuck" # Directory name
SESSION_BASE_DIR   = os.path.expanduser("~") # Base dir, user's home is default
### DO NOT EDIT BELOW
SESSION_DIR = os.path.join(
    SESSION_BASE_DIR,
    SESSION_DIR_NAME
    )
if not os.path.exists(SESSION_DIR):
    os.makedirs(SESSION_DIR)
SESSION_FILE = os.path.join(SESSION_DIR, SESSION_FILE_NAME)
### END DO NOT EDIT