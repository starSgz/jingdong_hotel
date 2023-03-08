#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from jingdong_demo.models.model import UserModel

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('common/base.html')
