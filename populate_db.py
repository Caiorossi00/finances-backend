from app import app, db, SaldoDiario
from datetime import date

with app.app_context():
    registro = SaldoDiario(data=date.today(), saldo=1000.00)
    
    db.session.add(registro)
    db.session.commit()
    
    print(f"Registro inserido: {registro.data} - {registro.saldo}")
