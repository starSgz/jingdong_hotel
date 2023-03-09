# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/9 22:56
@Auth ： star
@File ：test.py
"""
from werkzeug.security import generate_password_hash

print(generate_password_hash('123456'))