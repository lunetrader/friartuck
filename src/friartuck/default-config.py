"""Configuration for friartuck Python Robinhood API wrapper."""

# Robinhood credentials
ROBINHOOD_USERNAME = "email@email.com"
ROBINHOOD_PASSWORD = "password"

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
LOGIN_EXPIRATION_SECONDS = 86400