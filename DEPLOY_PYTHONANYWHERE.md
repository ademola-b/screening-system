# PythonAnywhere Deployment Guide for Screening System

This guide walks you through deploying the **Screening System** Django application onto [PythonAnywhere](https://www.pythonanywhere.com).

---

## 1. Prerequisites
- A PythonAnywhere account (free or paid) at [pythonanywhere.com](https://www.pythonanywhere.com).
- Your PythonAnywhere username (referred to below as `<username>`).

---

## 2. In PythonAnywhere: Open Bash Console & Clone Project

1. Log in to PythonAnywhere.
2. Go to the **Consoles** tab and click on **Bash** to open a new bash terminal.
3. Clone the repository into your home directory:
   ```bash
   git clone https://github.com/ademola-b/screening-system.git
   cd screening-system
   ```

---

## 3. Create Virtual Environment & Install Dependencies

In the Bash console, run:
```bash
# Create a virtual environment using Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 screening-env

# Ensure virtualenv is active (prompt will show (screening-env))
workon screening-env

# Install requirements
pip install -r requirements.txt
```

---

## 4. Run Migrations & Collect Static Files

In the same Bash console (still inside `~/screening-system` with the virtualenv active):
```bash
# 1. Apply database migrations
python manage.py migrate

# 2. Collect all static files for the web server
python manage.py collectstatic --noinput

# 3. Create your Django superuser / admin account
python manage.py createsuperuser
```
Follow the prompts to enter your admin username, email, and password.

---

## 5. Configure the Web App

1. Click the **Web** tab at the top of PythonAnywhere.
2. Click **Add a new web app**.
3. When prompted about domain name, click **Next** (it will be `<username>.pythonanywhere.com`).
4. On the framework selection screen, select **Manual configuration** (do **NOT** select "Django").
5. Select **Python 3.10** and click **Next**.

### A. Set Code & Working Directory
Scroll down to the **Code** section:
- **Source code:** `/home/<username>/screening-system`
- **Working directory:** `/home/<username>/screening-system`

*(Replace `<username>` with your actual PythonAnywhere username)*

### B. Set Virtualenv
Scroll down to the **Virtualenv** section:
- Click the edit icon and enter:
  `/home/<username>/.virtualenvs/screening-env`
- Click the checkmark to save.

### C. Map Static and Media Files
Scroll down to the **Static files** section and add these two mappings:

| URL | Directory |
|---|---|
| `/static/` | `/home/<username>/screening-system/staticfiles` |
| `/media/` | `/home/<username>/screening-system/media` |

*(Replace `<username>` with your actual PythonAnywhere username)*

### D. Configure WSGI File
Under the **Code** section, click on the **WSGI configuration file** link (usually `/var/www/<username>_pythonanywhere_com_wsgi.py`).

1. Delete everything inside that file.
2. Paste the following configuration:

```python
import os
import sys

# Path to your project directory
path = '/home/<username>/screening-system'
if path not in sys.path:
    sys.path.append(path)

# Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'screening_exercise.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `<username>` on line 5 with your actual PythonAnywhere username)*

3. Click **Save** in the top right corner.

---

## 6. Reload and Launch

1. Go back to the **Web** tab.
2. Click the green **Reload <username>.pythonanywhere.com** button.
3. Open a browser and visit:
   `https://<username>.pythonanywhere.com`

---

## 7. Useful Management Commands
Whenever you pull new changes or need to manage the site:
```bash
# Open Bash console, activate env, and navigate to project
workon screening-env
cd ~/screening-system

# Pull latest updates
git pull origin main

# Apply any new migrations
python manage.py migrate

# Collect static files if static assets changed
python manage.py collectstatic --noinput

# Then hit "Reload" on the Web tab
```
