#!flask/bin/python
from flask import Flask, request, jsonify
from utils import *

app = Flask(__name__)


@app.route('/api-bca')
def bcaApi():
    return jsonify('Hello, Congratulation!! You can access my trial BCA API :)')


@app.route('/api-bca/saldo', methods=['POST'])
def bca_balance_api():
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

        login = get_login(username, password)
        if len(login[1])>0:
            session = login[0]
            balance_information = get_balance_information(session)
            try:
                if len(balance_information) <1:
                    return jsonify({'detail':'Something wrong, please try 5 minutes later'})
                return jsonify({'Info rekening anda':balance_information})
            except:
                session.post('https://m.klikbca.com/authentication.do?value(actions)=logout')
            session.post('https://m.klikbca.com/authentication.do?value(actions)=logout')
        return jsonify({'detail': "Wrong Login Information"})

    return jsonify({"msg": "Not valid request"})


@app.route('/api-bca/transaksi', methods=['POST'])
def bca_api_transaction():
    """
    params : username & password
    :return:
    last 30 days transaction in json format
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    login = get_login(username, password)
    if len(login[1]) > 0:
        session = login[0]
        headers = login[2]
        statement_history = get_mutation_information(session, headers)
        try:
            if len(statement_history[1]) < 1:
                return jsonify({'detail': 'Something wrong, please try 5 minutes later'})
            return jsonify(
                                {'Info rekening anda':
                                     {
                                         'Informasi Saldo':statement_history[0],
                                         'Transaksi Mutasi Rekening': statement_history[1],
                                         'Ringkasan Mutasi': statement_history[2]
                                     }
                                }
                           )
        except:
            session.post('https://m.klikbca.com/authentication.do?value(actions)=logout')
        session.post('https://m.klikbca.com/authentication.do?value(actions)=logout')
    return jsonify({'detail': "Wrong Login Information"})


if __name__ == '__main__':
    app.run()