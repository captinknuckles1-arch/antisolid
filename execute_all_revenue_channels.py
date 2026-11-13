"""Legacy revenue orchestrator intentionally disabled.

The previous script invoked optional/missing modules, ignored subprocess
failures, and printed a successful completion message regardless of outcomes.
It did not verify revenue collection, contracts, or execution success.
"""


def execute_all():
    raise RuntimeError(
        "Legacy revenue orchestrator disabled. No agents, invoices, payment requests, or external actions were run."
    )


if __name__ == "__main__":
    execute_all()
