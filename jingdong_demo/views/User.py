# -*- coding: utf-8 -*-
"""
@Time ： 2023/3/8 22:28
@Auth ： star
@File ：User.py
"""

from flask import Blueprint, render_template
from jingdong_demo.models.model import UserModel

user = Blueprint('user', __name__)


@user.route('/')
def index():
    return render_template('common/base.html')
