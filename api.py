#!flask/bin/python
from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)


@app.route('/api-bca')
def bcaApi():
    return jsonify('Hello, Congratulation!! You can access my trial BCA API :)')


@app.route('/api-bca/saldo', methods=['POST'])
def bcaApiSaldo():
    """
        params : username & password
        :return:
        your current saldo
    """
    if request.method == 'POST':

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if not username:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        login = getLogin(username, password)
        if len(login[1])>0:
            session = login[0]
            saldo = getSaldo(session)
            try:
                if len(saldo) <1:
                    return jsonify({'detail':'Something wrong, please try 5 minutes later'})
                return jsonify({'Info rekening anda':saldo})
            except:
                pass
            session.post('https://m.klikbca.com/authentication.do?value(actions)=logout')
        return jsonify({'detail': "Wrong Login Information"})


    return jsonify({"msg": "Not valid request"})


@app.route('/api-bca/transaksi', methods=['POST'])
def bcaApiTransaksi():
    """
    params : username & password
    :return:
    last 30 days transaction in json format
    """
    return 'Check Transaksi'


if __name__ == '__main__':
    app.run()