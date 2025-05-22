import os
from dotenv import load_dotenv
from ldap3 import Server, ALL

load_dotenv()


class MailSettings:
    subject = "Ваш пароль мог истечь"
    body = f"Здравствуйте, \nВаш пароль мог истечь. Пожалуйста, измените его как можно скорее."


class LDAPSettings:
    server = Server(os.getenv('LDAP_SERVER'), get_info=ALL)


mail_settings = MailSettings()
ldap_settings = LDAPSettings()
