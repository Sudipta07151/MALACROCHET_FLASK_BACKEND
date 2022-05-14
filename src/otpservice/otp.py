import pyotp
import time
import datetime

class Otp:
    def __init__(self):
        self.base32secret = pyotp.random_base32()
    def generateSeretKey(self):
        print('Secret:', self.base32secret)
        return self.base32secret
    def generateOTP(self):
        totp = pyotp.TOTP(self.base32secret,interval=3000)
        time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
        print(time_remaining)
        otp_code=totp.now()
        print('OTP code:', otp_code)
        return otp_code

    def verifyOTP(self,otp):
        base32secret = self.base32secret
        print('Secret:', base32secret)
        totp = pyotp.TOTP(base32secret)
        your_code = otp
        # print(totp.verify(your_code))
        return totp.verify(your_code)


