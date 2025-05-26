# LDAP Notify 🔔

**LDAP Notify** — это инструмент для отправки уведомлений на Email на основе данных из LDAP-сервера. Проект предназначен для автоматизации оповещений о событиях, таких как истечение срока действия паролей.

---

## ⚙️ Установка и настройка

### Требования
- Python 3.8+
- Доступ к LDAP-серверу 
- Установленный Docker
- Приложение для SMTP-рассылки

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/MaksimSamusik/ldap-notify.git
   cd ldap-notify
2. Создайте виртуальное окружение:
    ```bash
    python -m venv venv
    ```
3. Активируйте виртуальное окружение
    ```bash
   .\venv\Scripts\activate
    ```
4. Переместите зависимости из requirements.txt
    ```bash
   pip install -r requirements.txt
    ```
5. Создайте файл .env и укажите такие параметры как:
    ```bash
    # Адрес LDAP-сервера (протокол + хост + порт)
    LDAP_SERVER='ldap://ldap.example.com:389'
    
    # Учетные данные для подключения (DN администратора)
    LDAP_USER='cn=admin,dc=example,dc=com'
    
    # Пароль администратора LDAP
    LDAP_PASSWORD='s3cr3tP@ssw0rd'
    
    # Базовый DN для поиска пользователей
    BASE_DN='ou=users,dc=example,dc=com'
    
    # Фильтр поиска (все объекты класса inetOrgPerson)
    LDAP_FILTER='(objectClass=inetOrgPerson)'
    
    # Атрибут с датой изменения пароля
    PASSWORD_EXPIRY_ATTR='pwdChangedTime'
    
    # Атрибут для хранения времени последнего уведомления
    LAST_NOTIFY_ATTR='description'
    
    # За сколько дней предупреждать об истечении пароля
    EXPIRY_DAYS=3
   
   # SMTP-сервер для отправки почты
    SMTP_SERVER='smtp.gmail.com'
    
    # Порт SMTP (465 для SSL, 587 для STARTTLS)
    SMTP_PORT=465
    
    # Почта отправителя (полный адрес)
    SMTP_USER='notifications@example.com'
    
    # Пароль от почты (или app password)
    SMTP_PASS='appP@ssw0rdForSMTP'
   
    # Название организации
    LDAP_ORGANISATION="Acme Inc."
    
    # Домен организации
    LDAP_DOMAIN="example.com"
    
    # Пароль admin-пользователя LDAP
    LDAP_ADMIN_PASSWORD="Adm1nP@ss"
    
    # Порт для незашифрованного LDAP
    LDAP1_PORT="389:389"
    
    # Порт для LDAPS (SSL)
    LDAP2_PORT="636:636"
    
    # Порт веб-интерфейса phpLDAPadmin
    PHP_LDAP_ADMIN_PORT="6443:443"
6. Создайте файл .dockerignore и добавьте директории
   ```dockerfile
    ldap_data/
    ldap_config/
   ```
7. Запустите docker-compose.yml
    ```dockerfile
      docker-compose up
   ```
