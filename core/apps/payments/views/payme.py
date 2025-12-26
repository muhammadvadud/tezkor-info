from payme.views import PaymeWebHookAPIView
from rest_framework.permissions import AllowAny
from payme.models import PaymeTransactions
from core.apps.main.models import AdModel
from core.apps.main.choices import PaymentsTypeChoice, PaymentsStatusChoice
from core.services.payme_pay import payme_pay
from core.services.cashback import give_cashback
import json
import logging

logger = logging.getLogger(__name__)


class PaymeCallBackAPIView(PaymeWebHookAPIView):
    permission_classes = [AllowAny]

    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")
        try:
            transaction_id = params.get("id")
            transaction = PaymeTransactions.objects.filter(transaction_id=transaction_id).first()
            ad = AdModel.objects.get(id=transaction.account_id)
            ad.payments_type = PaymentsTypeChoice.PAYME
            ad.status = PaymentsStatusChoice.PAID
            ad.save()
            payme_pay(ad)
            give_cashback(ad)
        except AdModel.DoesNotExist:
            print(f"Ad with ID not found.")
        except Exception as e:
            print(f"===========\n\n{e}\n\n========================")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")
        try:
            transaction_id = params.get("id")
            transaction = PaymeTransactions.objects.filter(transaction_id=transaction_id).first()
            ad = AdModel.objects.get(id=transaction.account_id)
            ad.status = PaymentsStatusChoice.CANCELED
            ad.save()
        except AdModel.DoesNotExist:
            print(f"Ad with ID not found.")
        except Exception as e:
            print(f"===========\n\n{e}\n\n========================")
