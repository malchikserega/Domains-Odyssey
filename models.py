# -*- coding: utf-8 -*-
'''
Модуль с моделью базы данных, хранящая адреса.
'''
from app import db


class Domains(db.Model):
    name = db.Column(db.String(128), unique=True, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Domain %r>' % self.name


class Whitelist(db.Model):
    name = db.Column(db.String(128), unique=True, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Whitelist %r>' % self.name


class Filtered(db.Model):
    name = db.Column(db.String(128), unique=True, primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Filtered %r>' % self.name

class Results(db.Model):
    name = db.Column(db.String(128), unique=True, primary_key=True)
    description = db.Column(db.String(512), unique=True, primary_key=True)
    img = db.Column(db.BLOB, unique=True, primary_key=True)

    def __init__(self, l):
        self.name = l[0]
        self.description = l[1]
        self.img = l[2]

    def __repr__(self):
        return '<Results %r>' % self.name
