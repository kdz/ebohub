from twilio.rest import TwilioRestClient
import os # TODO: avoid os, use a env.py module to centralize all env-vars

TW_account = os.getenv("TW_ACCOUNT_SID") #"my_twilio_account_number"
TW_password = os.getenv("TW_AUTH_TOKEN") #"my_twilio_auth_token"
TW_phone = os.getenv("TW_PHONE") #"+my_twilio_phone_number"  # format: "+15121234567"
TW_client = TwilioRestClient(TW_account, TW_password)