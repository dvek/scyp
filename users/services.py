from decimal import Decimal


def update_payments(payments_qs, percent):
    """
    update all payments with new percent increment
    """
    for pay in payments_qs:
        pay.amount = Decimal((1 + percent) * float(pay.amount))
        pay.save()