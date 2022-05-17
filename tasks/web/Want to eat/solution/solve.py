import hmac
import hashlib

# dHJ1ZQ==
secret_key = b"vova_secret"
total_params = b"2|1:0|10:1652574810|5:admin|8:dHJ1ZQ==|"  # your message
hash = hmac.new(secret_key, digestmod=hashlib.sha256)
hash.update(total_params)
print(total_params.decode() + hash.hexdigest())
