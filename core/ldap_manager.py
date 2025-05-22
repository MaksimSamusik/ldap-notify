import os
import asyncio
from datetime import datetime, timezone
from ldap3 import Connection
import logging
from dotenv import load_dotenv
from core.settings import ldap_settings

load_dotenv()

logger = logging.getLogger(__name__)


class LDAPManager:
    LDAP_SERVER = os.getenv('LDAP_SERVER')
    LDAP_USER = os.getenv('LDAP_USER')
    LDAP_PASSWORD = os.getenv('LDAP_PASSWORD')
    BASE_DN = os.getenv('BASE_DN')
    LDAP_FILTER = os.getenv('LDAP_FILTER')
    PASSWORD_EXPIRY_ATTR = os.getenv('PASSWORD_EXPIRY_ATTR')
    LAST_NOTIFY_ATTR = os.getenv('LAST_NOTIFY_ATTR')
    EXPIRY_DAYS = int(os.getenv('EXPIRY_DAYS', 90))

    def __init__(self):
        self.server = ldap_settings.server
        self.conn = None

    async def connect(self):
        loop = asyncio.get_running_loop()
        try:
            self.conn = await loop.run_in_executor(
                None,
                lambda: Connection(
                    self.server,
                    self.LDAP_USER,
                    self.LDAP_PASSWORD,
                    auto_bind=True
                )
            )
            return True
        except Exception as e:
            logger.error(f"LDAP connection error: {str(e)}", exc_info=True)
            return False

    async def search_users(self):
        if not self.conn:
            if not await self.connect():
                return []

        loop = asyncio.get_running_loop()
        try:
            await loop.run_in_executor(
                None,
                lambda: self.conn.search(
                    self.BASE_DN,
                    self.LDAP_FILTER,
                    attributes=['mail', 'cn', self.PASSWORD_EXPIRY_ATTR, self.LAST_NOTIFY_ATTR]
                )
            )
            return self.conn.entries
        except Exception as e:
            logger.error(f"LDAP search error: {str(e)}", exc_info=True)
            return []

    async def process_users(self) -> list:
        entries = await self.search_users()
        if not entries:
            return []

        now = datetime.now(timezone.utc)
        logger.info(f"Current time (UTC): {now.isoformat()}")

        users_to_notify = []
        for entry in entries:
            if not entry['mail'] or not entry['cn']:
                continue

            try:
                user_data = {
                    'email': entry['mail'].value,
                    'name': entry['cn'].value,
                    'pwd_changed_time': self.parse_ldap_date(entry[self.PASSWORD_EXPIRY_ATTR].value),
                    'days_since_change': None
                }

                delta_days = (now - user_data['pwd_changed_time']).days
                user_data['days_since_change'] = delta_days
                logger.info(f"{user_data['name']}: Password changed {delta_days} days ago")

                if delta_days >= self.EXPIRY_DAYS:
                    users_to_notify.append(user_data)

            except Exception as e:
                logger.error(f"Error processing user {entry.get('cn', 'unknown')}: {str(e)}", exc_info=True)
                continue

        return users_to_notify

    def parse_ldap_date(self, raw_date):
        try:
            return datetime.fromisoformat(str(raw_date))
        except ValueError:
            try:
                dt = datetime.strptime(str(raw_date), '%Y%m%d%H%M%SZ')
                return dt.replace(tzinfo=timezone.utc)
            except Exception as e:
                logger.error(f"Failed to parse date {raw_date}: {str(e)}")
                raise ValueError(f"Unsupported date format: {raw_date}")

    async def close(self):
        if self.conn:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.conn.unbind)
            self.conn = None