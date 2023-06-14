from flask import Flask, render_template, url_for, redirect
# url_for: usaremos o url_for para interagir a rota com alguma ação (ver home.html por exemplo)
# redirect: funcao para redirecionar o usuário

from flask_sqlalchemy import SQLAlchemy

# flask 
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# login_required: usado para dar uma condicao = o usuario tem que estar logado!

# usaremos o bycript para encriptar nossas senhas
from flask_bcrypt import Bcrypt

from streamlit.components.v1 import components

app = Flask(__name__)

# criando o objeto que vai receber os dados da aplicacao
db = SQLAlchemy(app)
# objeto que vai encriptar a senha
bcrypt = Bcrypt(app)

# a linha a sguir diz para nosso app flask onde está o banco de dados (testar outros nomes)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# vamos configurar uma chave secreta para proteger os cookies da sessão
app.config['SECRET_KEY'] = 'thisisasecretkey'
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# criando a tabela
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True) #nao pode ser nulo e o nome será unico
    password = db.Column(db.String(80), nullable=False)

#tudo isso a seguir sao funcionalidades de como criar formularios flask
#serao usados na classe userform
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

class RegisterForm(FlaskForm):
    # o username será um campo de string (string field) que terá que validar o imput com o tamanho minimo de 4 caracteres e maximo 20 e o renderizador mostrara o nome usuario
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Usuario"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Senha"})
    # adicionaremos um botao que terá o texto cadastrar
    submit = SubmitField('Cadastrar')

    # criando uma funcao que irá realizar uma busca no banco de dados user
    def validate_username(self, username):
        # como realizamos queries no sqlalchemy
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Nome de usuário já existe. Tente outro.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # criando uma variavel chamada form que vai receber a classe LoginForm
    form = LoginForm()
    if form.validate_on_submit(): #se a submissao for valida
        user = User.query.filter_by(username=form.username.data).first() # vamos procurar o usuario
        if user: # se o usuario for verdadeiro
            if bcrypt.check_password_hash(user.password, form.password.data): # vamos procurar a senha, sendo esta verdadeira
                login_user(user) #vamos usar o login_user do flask para logar e 
                return redirect(url_for('dashboard')) # redirecionar para dash
    return render_template('login.html', form=form) # o renderizador será login e o formulario vai receber a variavel da classe form

# -----------------------------------------------------------------------------------

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

    '''
    ALTERNATIVA:
    streamlit_code = components.declare_component("streamlit", path="dashboard.py")
    return render_template('dashboard.html', streamlit_code=streamlit_code) 
    '''

# -----------------------------------------------------------------------------------

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user() # deslogue o usuario
    return redirect(url_for('login'))


@ app.route('/register', methods=['GET', 'POST'])
def register():
    # criando uma variável chamada form que vai receber a classe register form
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) # gerando uma senha encriptada
        new_user = User(username=form.username.data, password=hashed_password) # objeto que vai receber um novo usuario
        db.session.add(new_user) # adicionando o usuário da sessão ao nosso banco de dados
        db.session.commit() # confirmar as mudancas
        return redirect(url_for('login')) # ao final, vamos redirecionar o usuario para a rota login

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
