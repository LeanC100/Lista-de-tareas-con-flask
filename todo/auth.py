# set e funciones
import functools

from flask import(
    #son configurables | nos permite enviar mensajes de manera generica a las plantillas
    Blueprint,flash,g, render_template,request,url_for, session,redirect
)

#                              verifica la contraseña  | encripta la contraseña
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

    #atoga la url que le indicamos

bp= Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register(): # creacion del registro de la app
# valida si el metodo es post
    if request.method== 'POST':
        username= request.form['username']
        password= request.form['password']
        #sacamos nuestra base de datos
        db,c = get_db()
        error= None
        c.execute(
            'select id from user where username = %s', (username,)
        )
        #validar ingreso de datos
        if not username:
            error = 'Username is required'
        if not password:
            error = 'Password is required'
        elif c.fetchone() is not None:
        #validar que no tenga error
            error = 'User {} is registered'.format(username)

 # si nos robas los datos el hacker va a ver hash en ves de las contraseñas
        if error is None:
            c.execute(        
                "insert into user (username, password) values (%s, %s)",
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
            
        flash(error)
    # en caso de que haga una peticacion de GET
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method== 'POST':
        username= request.form['username']
        password= request.form['password']
        db,c = get_db()
        error= None
        c.execute(
            'select * from user where username = %s',(username,)
        )
        user = c.fetchone()
        if user is None:
        #no le decimos que datos son invalidos
            error='Los datos ingrasados son invalidos'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña invalidos'
        #redifige al usuario a la pagina del inicio
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')

#funcion decoradora
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        #el suuario no inicio secion
        g.user = None
    else:
        #busca el usuario en la base de datos
        db, c= get_db()
        c.execute (
            "select * from user where id= %s", (user_id,)
        )
        g.user = c.fetchone()

#funcion decoradora
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # si es None el usuario no inicio secion todavia
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view

# cierra la secion
@bp.route("/logout")
def logout():
    session.clear()
    return redirect (url_for('auth.login'))