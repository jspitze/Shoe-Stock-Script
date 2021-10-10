# This code scrapes the Vivobarefoot webpage for Primus Lite III's and checks if shoes are
# in stock for the "Deep Sea Blue" color. If they are in stock, it will send me an email

import requests
import json
from bs4 import BeautifulSoup
import re
import smtplib, ssl
import time
from automailcreds import mailpassword, sender_email, receiver_email

#Email setup
port = 465
smtp_server = 'smtp.gmail.com'
sender = sender_email
receiver = receiver_email
password = mailpassword
message = """\
Subject: In Stock Notification

Hi! There are Vivobarefoot shoes in Deep Sea Blue in stock on their website. Link here:

    https://www.vivobarefoot.com/us/primus-lite-iii-mens

** This message sent via Python automation **
"""
context = ssl.create_default_context()

url = 'https://www.vivobarefoot.com/us/primus-lite-iii-mens'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Accept': 'image/webp,*/*',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

page = requests.get(url, headers=header)
soup = BeautifulSoup(page.content, 'html.parser')
scriptlist=[]
for items in soup.find_all('script', type = 'text/x-magento-init'):
    scriptlist.append(items)
data = str(scriptlist[10])
data = re.sub(r'<script type="text/x-magento-init">\n', "", data)
data = re.sub(r'</script>', "", data)
newdata = json.loads(data)
dsb = (newdata['[data-role=swatch-options]']['Magento_Swatches/js/swatch-renderer']['jsonConfig']
    ['attributes']['93']['options'][2])

if len(dsb['products']) > 0:
    print("Shoes in stock for color: " + dsb['label'])
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
else:
    print("Not in stock")
