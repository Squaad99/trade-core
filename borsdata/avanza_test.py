import hashlib
import pyotp
totp = pyotp.TOTP('ZON3P6GL43EPD7YG4UGCYYKJOJGISBV3', digest=hashlib.sha1)
print(totp.now())