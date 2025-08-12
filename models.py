from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SaldoDiario(db.Model):
    __tablename__ = 'saldo_diario'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    saldo = db.Column(db.Numeric(12, 2), nullable=False)
