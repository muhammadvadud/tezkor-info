import os

PAYTECH_LICENSE_API_KEY = "2c678901-6a8a-4f59-b47f-dc0368f8403d"

PAYME_ID = os.getenv("PAYME_ID")
PAYME_KEY = os.getenv("PAYME_KEY")
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "total_price"
PAYME_ACCOUNT_MODEL = "core.apps.main.models.AdModel"
PAYME_ONE_TIME_PAYMENT = True
