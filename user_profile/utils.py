# user_profile/utils.py

def detect_smtp_settings(email):
    """
    Detect SMTP server & port automatically from email domain.
    Defaults to smtp.<domain>:587 if not in mapping.
    """
    domain = email.split("@")[-1].lower()

    provider_map = {
        "gmail.com": ("smtp.gmail.com", 587),
        "outlook.com": ("smtp.office365.com", 587),
        "hotmail.com": ("smtp.office365.com", 587),
        "live.com": ("smtp.office365.com", 587),
        "yahoo.com": ("smtp.mail.yahoo.com", 587),
        "yahoo.co.uk": ("smtp.mail.yahoo.com", 587),
    }

    return provider_map.get(domain, ("smtp." + domain, 587))