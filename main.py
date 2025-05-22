import asyncio
import logging
from core.email_sender import EmailSender
from core.ldap_manager import LDAPManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    ldap_manager = LDAPManager()
    try:
        users_to_notify = await ldap_manager.process_users()
        if not users_to_notify:
            logging.info("No users to notify")
            return

        tasks = []
        for user in users_to_notify:
            email_sender = EmailSender(user['email'], user['name'])
            tasks.append(email_sender.send_email())

        results = await asyncio.gather(*tasks)
        success_count = sum(1 for result in results if result)
        logging.info(f"Total: successfully sent {success_count} out of {len(tasks)} emails")

    except Exception as e:
        logging.error(f"Main function error: {str(e)}", exc_info=True)
    finally:
        await ldap_manager.close()

if __name__ == '__main__':
    asyncio.run(main())