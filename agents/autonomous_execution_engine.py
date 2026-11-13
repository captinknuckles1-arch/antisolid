"""Legacy execution engine disabled.

The previous cycle only wrote notification rows for open balances and printed
that multiple agents were synchronized. It did not collect invoices, contact
customers, or verify payments.
"""


def execute_autonomous_cycle():
    raise RuntimeError(
        "Legacy autonomous engine disabled. No collection, payment, or customer action was performed."
    )


if __name__ == "__main__":
    execute_autonomous_cycle()
