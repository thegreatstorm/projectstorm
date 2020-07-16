

def check_rest_key(user_key, system_key):
    if not user_key.get("api_key"):
        return 401

    if user_key["api_key"] == "":
        return 401

    if not user_key["api_key"] == system_key:
        return 401