#!/usr/bin/python
# -*- coding: utf-8 -*-
from jingdong_demo.extensions import db


class BaseModel():
    # 添加一条数据
    def save(self):
        try:
            # self 代表当前当前实例化的对象
            db.session.add(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    # 添加多条数据
    @staticmethod
    def save_all(*args):
        try:
            db.session.add_all(args)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    # 删除
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
