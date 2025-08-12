from flask import Flask
from config import Config
from models import db, SaldoDiario

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/')
def index():
    registros = SaldoDiario.query.all()
    if not registros:
        return "SaldoDiario não tem registros cadastrados."
    
    detalhes = []
    for r in registros:
        detalhes.append(f"ID: {r.id} | Data: {r.data} | Saldo: R$ {r.saldo}")
    
    return "<br>".join(detalhes)

if __name__ == '__main__':
    app.run(debug=True)
