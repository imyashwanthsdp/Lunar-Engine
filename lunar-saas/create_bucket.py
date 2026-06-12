import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request("https://api.keyvalue.xyz/new", method="POST", data=b"visits=385")
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        token_url = response.read().decode('utf-8').strip()
        print("TOKEN_URL:", token_url)
except Exception as e:
    print("Error:", e)
