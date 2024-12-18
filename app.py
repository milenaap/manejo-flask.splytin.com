from flask import Flask, render_template

from cliente import Cliente
from cliente_dao import ClienteDAO

app = Flask(__name__)

titulo_app = 'Zona Fit (GYM) Proxima Estación-'


@app.route('/') #url: http://localhost:5000/
@app.route('/index.html') #url https: //localhost:5000/index.html

def inicio():
    app.logger.debug('Entramos al path de inicio /')
    clientes_db = ClienteDAO.seleccionar()
    return render_template('index.html', titulo=titulo_app, clientes=clientes_db)

if __name__ == '__main__':
    app.run(debug=True)