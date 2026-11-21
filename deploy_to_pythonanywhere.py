#!/usr/bin/env python3
"""
Automated deployment script for PythonAnywhere via REST API.
Usage:
  python3 deploy_to_pythonanywhere.py <username> <api_token>
"""

import sys
import os
import time
import requests

def deploy(username, token):
    domain = f"{username}.pythonanywhere.com"
    base_url = f"https://www.pythonanywhere.com/api/v0/user/{username}"
    headers = {"Authorization": f"Token {token}"}

    print(f"[*] Starting deployment to {domain}...")

    # 1. Create or check webapp
    webapps_url = f"{base_url}/webapps/"
    resp = requests.get(webapps_url, headers=headers)
    if resp.status_code != 200:
        print(f"[!] Error authenticating with PythonAnywhere API: {resp.status_code} {resp.text}")
        return False

    existing_webapps = [w["domain_name"] for w in resp.json()]
    if domain not in existing_webapps:
        print(f"[*] Creating new web app for {domain}...")
        create_resp = requests.post(
            webapps_url,
            headers=headers,
            json={"domain_name": domain, "python_version": "3.10"}
        )
        if create_resp.status_code not in (200, 201):
            print(f"[!] Failed to create web app: {create_resp.status_code} {create_resp.text}")
            return False
        print(f"[✓] Web app created.")
    else:
        print(f"[✓] Web app {domain} already exists.")

    # 2. Update Webapp configuration
    app_url = f"{base_url}/webapps/{domain}/"
    virtualenv_path = f"/home/{username}/.virtualenvs/screening-env"
    update_resp = requests.patch(
        app_url,
        headers=headers,
        json={"virtualenv_path": virtualenv_path}
    )
    print(f"[✓] Virtualenv path set to: {virtualenv_path}")

    # 3. Configure WSGI file
    wsgi_path = f"/var/www/{username}_pythonanywhere_com_wsgi.py"
    wsgi_content = f"""import os
import sys

path = '/home/{username}/screening-system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'screening_exercise.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""
    files_url = f"{base_url}/files/path{wsgi_path}"
    wsgi_resp = requests.post(
        files_url,
        headers=headers,
        files={"content": wsgi_content}
    )
    if wsgi_resp.status_code in (200, 201):
        print(f"[✓] WSGI configuration written to {wsgi_path}")
    else:
        print(f"[!] Warning writing WSGI file: {wsgi_resp.status_code} {wsgi_resp.text}")

    # 4. Configure Static Files
    static_url = f"{base_url}/webapps/{domain}/static_files/"
    existing_static = requests.get(static_url, headers=headers).json()
    existing_urls = [s["url"] for s in existing_static]

    mappings = [
        {"url": "/static/", "path": f"/home/{username}/screening-system/staticfiles"},
        {"url": "/media/", "path": f"/home/{username}/screening-system/media"}
    ]

    for m in mappings:
        if m["url"] not in existing_urls:
            r = requests.post(static_url, headers=headers, json=m)
            print(f"[✓] Added static mapping: {m['url']} -> {m['path']}")
        else:
            print(f"[✓] Static mapping exists: {m['url']}")

    # 5. Open a bash console to run setup commands
    print("[*] Creating Bash console on PythonAnywhere to run project setup...")
    consoles_url = f"{base_url}/consoles/"
    console_resp = requests.post(
        consoles_url,
        headers=headers,
        json={"executable": "bash"}
    )
    if console_resp.status_code in (200, 201):
        console_id = console_resp.json()["id"]
        print(f"[✓] Console {console_id} started. Executing commands...")
        
        setup_cmds = f"""
if [ -d ~/screening-system ]; then
    cd ~/screening-system && git pull origin main
else
    git clone https://github.com/ademola-b/screening-system.git ~/screening-system
fi
mkvirtualenv --python=/usr/bin/python3.10 screening-env || workon screening-env
workon screening-env
cd ~/screening-system
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
echo "DEPLOY_COMPLETE_FLAG"
"""
        send_url = f"{base_url}/consoles/{console_id}/send_input/"
        requests.post(send_url, headers=headers, json={"input": setup_cmds + "\n"})

        # Wait for completion
        print("[*] Waiting for setup (pip install, migrations, collectstatic) to finish...")
        for _ in range(30):
            time.sleep(5)
            out_resp = requests.get(f"{base_url}/consoles/{console_id}/latest_output/", headers=headers)
            out_text = out_resp.json().get("output", "")
            if "DEPLOY_COMPLETE_FLAG" in out_text:
                print("[✓] Project setup finished successfully!")
                break
        else:
            print("[*] Setup is continuing in background.")

    # 6. Reload webapp
    reload_url = f"{base_url}/webapps/{domain}/reload/"
    reload_resp = requests.post(reload_url, headers=headers)
    if reload_resp.status_code == 200:
        print(f"\n[✓] Deployment complete! App is live at https://{domain}")
        return True
    else:
        print(f"[!] Error reloading app: {reload_resp.status_code} {reload_resp.text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        u = os.environ.get("PYTHONANYWHERE_USERNAME")
        t = os.environ.get("PYTHONANYWHERE_API_TOKEN")
        if not u or not t:
            print("Usage: python3 deploy_to_pythonanywhere.py <username> <api_token>")
            sys.exit(1)
        deploy(u, t)
    else:
        deploy(sys.argv[1], sys.argv[2])
