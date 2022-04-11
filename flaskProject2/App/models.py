from .ext import db


class Dogs(db.Model):
    __tablename__ = 'dogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    food = db.Column(db.String(30))
    flag = db.Column(db.String(100))

    def __repr__(self):
        return '<dogs %r>' % self.name


class Cats(db.Model):
    __tablename__ = 'cats'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    food = db.Column(db.String(30))
    flag = db.Column(db.String(100))

    def __repr__(self):
        return '<dogs %r>' % self.name