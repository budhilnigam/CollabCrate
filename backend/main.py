from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
SQLAlchemy(app)

@app.route('/api', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World'})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
if __name__ == '__main__':
    app.run(debug=True)