from flask import Flask, request, jsonify
from config import Config
from models import db, Usuario, SaldoDiario, Aporte

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    data = request.json
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    usuario = Usuario(
        email=data['email'],
        nome=data['nome']
    )
    usuario.set_senha(data['senha'])
    
    db.session.add(usuario)
    db.session.commit()
    
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)