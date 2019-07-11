#!flask/bin/python
from flask import Flask, request, jsonify

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