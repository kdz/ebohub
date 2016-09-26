from twilio.rest import TwilioRestClient
TW_account = "my_twilio_account_number"
TW_password = "my_twilio_auth_token"
TW_phone = "+my_twilio_phone_number"  # format: "+15121234567"
TW_client = TwilioRestClient(TW_account, TW_password)