import os

PAYME_ID = os.environ.get("PAYME_ID")
PAYME_KEY = os.environ.get("PAYME_KEY")
PAYME_ACCOUNT_FIELD = "order_id"
PAYME_AMOUNT_FIELD = "total_price"
PAYME_ACCOUNT_MODEL = "core.apps.main.models.AdModel"
PAYME_ONE_TIME_PAYMENT = True
