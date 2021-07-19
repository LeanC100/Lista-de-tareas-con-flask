import mysql.connector
# herramienta que sirve para ejecutar comandos en la terminar en vez de codigo
import click
# mantiene la appa que estamos ejecutando, 
# g es una variable que se encuentra en toda la aplicacion que la podemos llamar cuando querramos
from flask import current_app, g
# sirve cuando ejecuramos el script de la base de datos, permite acxedes a las variables
from flask.cli import with_appcontext
# va a contener todos los script que necitamos para crear las bases de datos
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db , g.c


#permite cerrar la conexcion de la base de datos cada vez que realizacemos una peticion
def class_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#traemos la base de datos/ importamos 
def init_db():
    db,c=get_db()

    for i in instructions:
        c.execute(i)
    
    db.commit()

# se encarga de corrar toda la logica, aca se hace uso de CLICK
            # usa este nombre
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')


#agrega la funcion que tiene que ejecutar cuando se llama o termina la peticion
def init_app(app):
    app.teardown_appcontext(class_db)
    app.cli.add_command(init_db_command)
