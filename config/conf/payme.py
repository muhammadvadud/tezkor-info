import os

PAYME_ID = os.getenv("PAYME_ID")
PAYME_KEY = os.getenv("PAYME_KEY")
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "total_price"
PAYME_ACCOUNT_MODEL = "core.apps.main.models.AdModel"
PAYTECH_API_KEY = "6bb7d17e-c22b-44ee-96f3-d93f8b0d750b"
PAYME_ONE_TIME_PAYMENT = True
