from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired, regexp
from datetime import datetime
from despesas import db


class BankModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.String(30))

    def __repr__(self):
        return '<Bank %r>' % (self.bank)


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(30))

    def __repr__(self):
        return '<Item %r>' % (self.item)


class PersonModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    site = db.Column(db.String(50))
    job = db.Column(db.String(50))
    created_at = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, email, site, job, created_at=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.site = site
        self.job = job
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at

    def __repr__(self):
        return '<Person %r %r>' % (self.first_name, self.last_name)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history = db.Column(db.String(50))
    expense = db.Column(db.Boolean, default=True)
    price = db.Column(db.Numeric(6, 2))
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    paid = db.Column(db.Boolean, default=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


class PersonForm(Form):
    first_name = StringField("Nome")
    last_name = StringField("Sobrenome")
    email = StringField("E-mail", validators=[DataRequired()])
    site = StringField("Site")
    job = StringField("Profissão")
