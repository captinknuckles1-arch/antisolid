#!/usr/bin/env python3
# Solid Integrations LLC - Zero-Dependency .env Loader & Key Masker
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
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'").strip('"')
            os.environ[k] = v
            loaded[k] = v
    return loaded

def is_configured(key_name):
    val = os.environ.get(key_name, "")
    return bool(val and not val.startswith("REPLACE_WITH_") and len(val) >= 8)

def mask_value(key_name):
    val = os.environ.get(key_name, "")
    if not is_configured(key_name):
        return "UNSET (FALLBACK MODE)"
    return f"CONFIGURED ({val[:4]}...{val[-4:]})"

def get_auth_summary():
    load_dotenv()
    return {
        "sam_gov_configured": is_configured("SAM_GOV_API_KEY"),
        "sam_gov_mask": mask_value("SAM_GOV_API_KEY"),
        "ercot_configured": is_configured("ERCOT_OCP_APIM_SUBSCRIPTION_KEY"),
        "ercot_mask": mask_value("ERCOT_OCP_APIM_SUBSCRIPTION_KEY"),
        "outlook_configured": is_configured("OUTLOOK_CLIENT_ID"),
        "outlook_mask": mask_value("OUTLOOK_CLIENT_ID"),
        "env_permissions": oct(os.stat(".env").st_mode)[-3:] if os.path.exists(".env") else "MISSING"
    }

if __name__ == "__main__":
    summary = get_auth_summary()
    print(f"[ENV_LOADER] SAM.gov: {summary['sam_gov_mask']} | ERCOT: {summary['ercot_mask']} | .env mode: {summary['env_permissions']}")
