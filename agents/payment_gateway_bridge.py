"""Legacy payment bridge intentionally disabled.

The previous implementation accepted unsigned Stripe/PayPal-shaped JSON,
credited arbitrary amounts to a local ledger, and could double-count replayed
events. It did not verify provider signatures or payment status. No event is
accepted and no revenue is credited by this module.
"""


class PaymentProcessingDisabled(RuntimeError):
    pass


def init_payment_tables():
    raise PaymentProcessingDisabled(
        "Payment bridge disabled pending provider signature verification, idempotency, and reconciliation."
    )


def record_gateway_payment(*args, **kwargs):
    raise PaymentProcessingDisabled(
        "No payment recorded. Use the provider's verified transaction record and approved accounting workflow."
    )


if __name__ == "__main__":
    raise SystemExit(
        "Payment bridge disabled. No listener started and no ledger entries were created."
    )
