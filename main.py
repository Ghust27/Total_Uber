from utils import *
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/get_total_uber", methods=['POST'])
def get_total_uber():
    data = request.json
    if not data or 'cookies' not in data:
        return jsonify({"Error": "Cookies not provided"}), 400
    
    cookies = data['cookies']
    total_uber = GetData()
    total_uber.headers["cookie"] = cookies
    result = total_uber.GetTotal()
    return jsonify(result)

app.run(host='0.0.0.0', debug=True)


#pra facilitar tua vida ta ai o link da api: http:/127.0.0.1:5000/get_total_uber?cookies= #aqui tu bota os cookies estando encoded#

#pra ligar a api da run nesse codigo,utils é as configs da api.