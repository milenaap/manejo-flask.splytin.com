from flask import Flask, render_template, jsonify, send_from_directory, redirect, url_for
import os
import logging
from logging.handlers import RotatingFileHandler

import cliente_forma
from cliente import Cliente
from cliente_dao import ClienteDAO
from cliente_forma import ClienteForma
from src.utils import message_channel
from dotenv import load_dotenv

titulo_app = 'Zona Fit (GYM) Dama'
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/app.log')


def create_app():

    # Carga las variables desde el archivo .env
    load_dotenv()

    app = Flask(__name__)

    # Crear la carpeta "logs" si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configurar logging
    handler = RotatingFileHandler(
        LOG_PATH, maxBytes=1000000, backupCount=5
    )  # Archivo de log, 1 MB máx., 5 backups
    handler.setLevel(logging.ERROR)  # Registrar solo errores y mayores
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )  # Formato de los logs
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)



    @app.route('/') #url: http://localhost:5000/
    @app.route('/index.html') #url https: //localhost:5000/index.html
    def inicio():
        app.logger.debug('Entramos al path de inicio /')
        clientes_db = ClienteDAO.seleccionar()
        # Creamos un objeto de cliente vacio
        cliente= Cliente()
        cliente_forma= ClienteForma(obj=cliente)
        return render_template('index.html', titulo=titulo_app, clientes=clientes_db,
                               forma=cliente_forma)

    @app.route('/guardar', methods=['POST'])
    def guardar():
        # Creamos los objetos de cliente inicialmete vacios
        cliente = Cliente()
        cliente_forma = ClienteForma(obj=cliente)
        if cliente_forma.validate_on_submit():
            # llenamos el objeto cliente con los valores del formulario
            cliente_forma.populate_obj(cliente)# tambien se recupera el id oculto
            if not cliente.id:
                # Guardamos el nuevo cliente en la BD
                ClienteDAO.insertar(cliente)
            else:
                ClienteDAO.actualizar(cliente)
        # Redireccionar a la pagina de inicio
        return redirect(url_for('inicio'))

    @app.route('/limpiar')
    def limpiar():
        return redirect(url_for('inicio'))

    @app.route('/editar/<int:id>') # localhost:5000/editar/1
    def editar(id):
        cliente = ClienteDAO.seleccionar_por_id(id)
        cliente_forma = ClienteForma(obj=cliente)
        #Recuperar el listado de clientes para volver a mostrarlo
        clientes_db= ClienteDAO.seleccionar()
        return render_template('index.html', titulo=titulo_app,
                               clientes=clientes_db,
                               forma=cliente_forma)
    @app.route('/eliminar/<int:id>')
    def eliminar(id):
        cliente = Cliente(id=id)
        ClienteDAO.eliminar(cliente)
        return redirect(url_for('inicio'))

    @app.route('/error')
    def error():
        v = 1 / 0
        return jsonify({"mensaje": "Esto nunca se ejecutará"})


    @app.route('/test')
    def test():
        message_channel.send("Este es un mensaje de prueba", "Test")
        return jsonify({"mensaje": "Se envió el mensaje"})




    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')


    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Error interno del servidor"}), 500



    return app



app = create_app()

app.config['SECRET_KEY'] = 'llave secreta_123' # Llave secreta para proteger formularios



if __name__ == '__main__':

    app.run(debug=True)

