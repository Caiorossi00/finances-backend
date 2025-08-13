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


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    usuario = Usuario.query.filter_by(email=data['email']).first()

    if not usuario or not usuario.check_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas'}), 401

    return jsonify({
        'mensagem': 'Login realizado com sucesso!',
        'usuario': {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email
        }
    })

@app.route('/api/saldo', methods=['POST'])
def registrar_saldo():
    data = request.json
    usuario_id = data['usuario_id']
    data_registro = data['data']
    saldo_valor = data['saldo']

    saldo_existente = SaldoDiario.query.filter_by(
        usuario_id=usuario_id,
        data=data_registro
    ).first()

    if saldo_existente:
        saldo_existente.saldo = saldo_valor
        mensagem = 'Saldo atualizado com sucesso!'
    else:
        novo_saldo = SaldoDiario(
            usuario_id=usuario_id,
            data=data_registro,
            saldo=saldo_valor
        )
        db.session.add(novo_saldo)
        mensagem = 'Saldo registrado com sucesso!'

    db.session.commit()
    return jsonify({'mensagem': mensagem})

@app.route('/api/saldo', methods=['GET'])
def listar_saldo():
    usuario_id = request.args.get('usuario_id')
    data_inicio = request.args.get('data_inicio')  
    data_fim = request.args.get('data_fim')       

    query = SaldoDiario.query.filter_by(usuario_id=usuario_id)

    if data_inicio:
        query = query.filter(SaldoDiario.data >= data_inicio)
    if data_fim:
        query = query.filter(SaldoDiario.data <= data_fim)

    registros = query.order_by(SaldoDiario.data).all()

    resultado = [
        {
            'id': r.id,
            'data': r.data.strftime('%Y-%m-%d'),
            'saldo': float(r.saldo)
        }
        for r in registros
    ]

    return jsonify(resultado)

@app.route('/')
def index():
    usuario_id = request.args.get('usuario_id')
    if not usuario_id:
        return "Informe o parametro 'usuario_id' na URL, ex: /?usuario_id=1"

    registros = SaldoDiario.query.filter_by(usuario_id=usuario_id).order_by(SaldoDiario.data).all()
    
    if not registros:
        return f"Usuário {usuario_id} não tem registros de saldo."

    resultado = [
        f"Data: {r.data.strftime('%Y-%m-%d')}, Saldo: {float(r.saldo)}"
        for r in registros
    ]

    return "<br>".join(resultado)


if __name__ == '__main__':
    app.run(debug=True)