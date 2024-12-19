from flask import Flask, render_template, jsonify, send_from_directory
import os
import logging
from logging.handlers import RotatingFileHandler
from cliente_dao import ClienteDAO
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
        return render_template('index.html', titulo=titulo_app, clientes=clientes_db)


    @app.route('/error')
    def error():
        v = 1 / 0
        return jsonify({"mensaje": "Esto nuna se ejecutará"})


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

if __name__ == '__main__':

    app.run(debug=True)

