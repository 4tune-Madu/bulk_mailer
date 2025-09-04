# mailer/utils.py
from dataclasses import dataclass
from typing import Optional, Tuple

# Known providers mapping; expand as needed
PROVIDER_SETTINGS = {
    "gmail.com":        {"smtp_server": "smtp.gmail.com",     "port": 587, "secure": "starttls"},
    "googlemail.com":   {"smtp_server": "smtp.gmail.com",     "port": 587, "secure": "starttls"},

    "outlook.com":      {"smtp_server": "smtp.office365.com", "port": 587, "secure": "starttls"},
    "hotmail.com":      {"smtp_server": "smtp.office365.com", "port": 587, "secure": "starttls"},
    "live.com":         {"smtp_server": "smtp.office365.com", "port": 587, "secure": "starttls"},
    "msn.com":          {"smtp_server": "smtp.office365.com", "port": 587, "secure": "starttls"},
    "office365.com":    {"smtp_server": "smtp.office365.com", "port": 587, "secure": "starttls"},

    "yahoo.com":        {"smtp_server": "smtp.mail.yahoo.com", "port": 465, "secure": "ssl"},
    "ymail.com":        {"smtp_server": "smtp.mail.yahoo.com", "port": 465, "secure": "ssl"},
    "rocketmail.com":   {"smtp_server": "smtp.mail.yahoo.com", "port": 465, "secure": "ssl"},

    "icloud.com":       {"smtp_server": "smtp.mail.me.com",    "port": 587, "secure": "starttls"},
    "me.com":           {"smtp_server": "smtp.mail.me.com",    "port": 587, "secure": "starttls"},
    "mac.com":          {"smtp_server": "smtp.mail.me.com",    "port": 587, "secure": "starttls"},

    "zoho.com":         {"smtp_server": "smtp.zoho.com",       "port": 465, "secure": "ssl"},
    "zohomail.com":     {"smtp_server": "smtp.zoho.com",       "port": 465, "secure": "ssl"},

    "aol.com":          {"smtp_server": "smtp.aol.com",        "port": 465, "secure": "ssl"},

    "yandex.com":       {"smtp_server": "smtp.yandex.com",     "port": 465, "secure": "ssl"},
    "yandex.ru":        {"smtp_server": "smtp.yandex.ru",      "port": 465, "secure": "ssl"},
}

def _domain(email: str) -> Optional[str]:
    if not email or "@" not in email:
        return None
    return email.split("@", 1)[1].lower().strip()

def guess_smtp_from_email(email: str) -> Tuple[str, int, bool, bool]:
    """
    Return (host, port, use_ssl, use_tls)
    """
    d = _domain(email)
    default = (f"smtp.{d}" if d else "localhost", 587, False, True)

    if not d:
        return default

    if d in PROVIDER_SETTINGS:
        entry = PROVIDER_SETTINGS[d]
        secure = entry.get("secure", "starttls").lower()
        use_ssl = (secure == "ssl")
        use_tls = (secure == "starttls")
        return (entry["smtp_server"], entry["port"], use_ssl, use_tls)

    return default

@dataclass
class SMTPConfig:
    host: str
    port: int
    use_ssl: bool
    use_tls: bool
    username: str
    password: str

def smtp_config_for_account(account) -> SMTPConfig:
    """
    Build SMTPConfig either from account.smtp_server/smtp_port or guessed from email.
    """
    try:
        server = (account.smtp_server or "").strip()
        port = int(account.smtp_port) if getattr(account, "smtp_port", None) not in (None, "") else None
    except Exception:
        server = ""
        port = None

    if server and port:
        host = server
        p = port
        if p == 465:
            use_ssl, use_tls = True, False
        else:
            use_ssl, use_tls = False, True
    else:
        host, p, use_ssl, use_tls = guess_smtp_from_email(account.email)

    return SMTPConfig(
        host=host,
        port=int(p),
        use_ssl=bool(use_ssl),
        use_tls=bool(use_tls),
        username=account.email,
        password=account.password,
    )

def build_django_connection(config: SMTPConfig):
    """
    Return Django email connection configured for this account.
    """
    from django.core.mail import get_connection
    return get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        host=config.host,
        port=config.port,
        username=config.username,
        password=config.password,
        use_tls=config.use_tls,
        use_ssl=config.use_ssl,
        timeout=30,
    )

def send_email_via_account(*, account, subject: str, body: str, recipients: list, attachments=None):
    """
    Send using per-account SMTP connection. attachments may be UploadedFile objects or tuples.
    Returns number of messages sent (int).
    """
    from django.core.mail import EmailMessage

    cfg = smtp_config_for_account(account)
    conn = build_django_connection(cfg)

    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=account.email,
        to=recipients,
        connection=conn,
    )

    if attachments:
        for f in attachments:
            if hasattr(f, "read"):
                msg.attach(f.name, f.read(), getattr(f, "content_type", None))
            else:
                name, content, mimetype = f
                msg.attach(name, content, mimetype)

    return msg.send()
