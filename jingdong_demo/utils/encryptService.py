import jwt
from datetime import datetime, timedelta
from flask import abort
# from config import PRIVATE_KEY
import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

#操作token
class OperateToken:

    def __init__(self):
        self._private_key = "123456"
        pass

    # 创建token
    def create_token(self, user_id, user_name, expiry_seconds):
        # Calculate expiry time
        expiry_time = datetime.now() + timedelta(seconds=expiry_seconds)
        # print(expiry_time)
        payload = {
            'exp': expiry_time,
            'user_id': user_id,
            'username': user_name
        }

        # 加密
        encode_jwt = jwt.encode(payload, self._private_key, algorithm='HS512')
        # print(encode_jwt)
        return encode_jwt

    # 验证token
    def check_token(self, token):
        decode_jwt = "-1"
        # 解密
        try:
            decode_jwt = jwt.decode(token, self._private_key, algorithms=['HS512'])
        except jwt.PyJWTError:
            print("Token is error!")
            abort(400)
        # print(decode_jwt)
        return decode_jwt


operate_token = OperateToken()
#
# print(operate_token.check_token(operate_token.create_token('admin','sgz',60*60)))

#rsa 加密解密
class rsa_obj():

    def get_key(self):
        return RSA.importKey(PRIVATE_KEY)


    def encrypt(self,msg):
        key = self.get_key()
        cipher = PKCS1_cipher.new(key)
        encrypt_msg = cipher.encrypt(msg.encode("utf-8"))
        return base64.b64encode(encrypt_msg).decode()


    def decrypt(self,msg):
        key = self.get_key()
        cipher = PKCS1_cipher.new(key)
        decrypt_data = cipher.decrypt(base64.b64decode(msg), 0)
        return decrypt_data.decode("utf-8")


