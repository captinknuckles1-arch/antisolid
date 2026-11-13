"""Legacy background scheduler disabled.

The prior installer modified the user's crontab and ran a status-only engine
hourly. It did not establish a verified revenue collection workflow. Do not
install local scheduled jobs from this script.
"""


def install_background_daemon():
    raise RuntimeError(
        "Legacy cron installation disabled. No crontab changes were made."
    )


if __name__ == "__main__":
    install_background_daemon()
