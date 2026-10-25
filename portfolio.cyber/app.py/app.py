from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Inicialização de Módulos de Segurança e BD
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- MODELOS DE BANCO DE DADOS (Prevenção contra SQL Injection) ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class MensagemContato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    # Projetos de Amostra
    fullstack_projects = [
        {"title": "Sistema ERP Cloud", "desc": "Dashboard analítico de alta performance feito em React e Python.", "techs": ["Python", "Flask", "React", "PostgreSQL"]},
        {"title": "E-Commerce Microservices", "desc": "Plataforma de vendas escalável com arquitetura orientada a microsserviços.", "techs": ["Python", "Docker", "Redis", "FastAPI"]}
    ]
    
    pentest_projects = [
        {"title": "Web Vulnerability Scanner", "desc": "Automação em Python para detecção de falhas XSS e SQLi em aplicações web.", "techs": ["Python", "Pentesting", "Sockets", "HTTP"]},
        {"title": "Auditoria de Infraestrutura Network", "desc": "Análise e hardening de regras de firewall, mapeamento de portas e simulação de exploits.", "techs": ["Nmap", "Wireshark", "Metasploit", "Hardening"]}
    ]
    
    return render_template('index.html', fullstack=fullstack_projects, pentest=pentest_projects)

@app.route('/contato', methods=['POST'])
def salvar_contato():
    nome = request.form.get('nome')
    email = request.form.get('email')
    msg = request.form.get('mensagem')
    
    if nome and email and msg:
        # Consulta ORM parametrizada segura contra SQL Injection
        nova_msg = MensagemContato(nome=nome, email=email, mensagem=msg)
        db.session.add(nova_msg)
        db.session.commit()
        flash("Mensagem enviada com sucesso para o mainframe!", "success")
    else:
        flash("Erro no envio. Verifique os campos.", "danger")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        # Validação segura com Hash Bcrypt
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Acesso negado: Credenciais inválidas.', 'danger')
            
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    mensagens = MensagemContato.query.all()
    return render_template('admin.html', mensagens=mensagens)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- INICIALIZAÇÃO E CRIAÇÃO DO USUÁRIO ADMIN COM CRIPTOGRAFIA ---
def setup_database():
    with app.app_context():
        db.create_all()
        # Criação do usuário solicitado com senha criptografada via Bcrypt
        admin_user = User.query.filter_by(username='MateusAntonioMacacari').first()
        if not admin_user:
            hashed_pw = bcrypt.generate_password_hash('Eduarda551499@@').decode('utf-8')
            new_admin = User(username='MateusAntonioMacacari', password_hash=hashed_pw)
            db.session.add(new_admin)
            db.session.commit()

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)