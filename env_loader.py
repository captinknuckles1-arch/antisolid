#!/usr/bin/env python3
"""Minimal .env loader. Presence is not proof that a credential is valid."""
import os


def load_dotenv(dotenv_path=".env"):
    loaded = {}
    if not os.path.exists(dotenv_path):
        return loaded
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key:
                os.environ.setdefault(key, value)
                loaded[key] = True
    return loaded


def is_configured(key_name):
    """Return whether a value is present; this does not validate credentials."""
    value = os.environ.get(key_name, "")
    return bool(value and not value.startswith("REPLACE_WITH_") and len(value) >= 8)


def mask_value(key_name):
    return "PRESENT (NOT VALIDATED)" if is_configured(key_name) else "MISSING"


def get_auth_summary():
    load_dotenv()
    return {
        "sam_gov_present": is_configured("SAM_GOV_API_KEY"),
        "sam_gov_status": mask_value("SAM_GOV_API_KEY"),
        "ercot_present": is_configured("ERCOT_OCP_APIM_SUBSCRIPTION_KEY"),
        "ercot_status": mask_value("ERCOT_OCP_APIM_SUBSCRIPTION_KEY"),
        "outlook_client_id_present": is_configured("OUTLOOK_CLIENT_ID"),
        "outlook_client_id_status": mask_value("OUTLOOK_CLIENT_ID"),
        "env_permissions": oct(os.stat(".env").st_mode)[-3:] if os.path.exists(".env") else "MISSING",
    }


if __name__ == "__main__":
    summary = get_auth_summary()
    print(
        f"[ENV_LOADER] SAM.gov: {summary['sam_gov_status']} | "
        f"ERCOT: {summary['ercot_status']} | .env mode: {summary['env_permissions']}"
    )
