import os
from flask import Flask

# siver para hacer testing o crear varias instancias 
def create_app():
    #todas la aplicaciones son una instacia de Flask
    app = Flask(__name__)
    # permite definir variables de comuciuacion que despues nos sirve para utlicxar en nuestra app
    app.config.from_mapping(
        # es una llave la cual se utlixara para definir las secines en nnuestra app | coke
        SECRET_KEY= 'mikey',
        # INGRESO DE MIS DATOS SET
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    # llamamos a la base de datos
    from . import db
    db.init_app(app)

    from . import auth
    from. import todo

    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    @app.route('/home')
    def home():
        return 'Home'

    @app.route('/hi')
    def hi():
        return 'hiiiiiii'

    return app