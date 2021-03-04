from pymongo import MongoClient
import jwt
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.hangst99

@app.route('/')
def home():
   return render_template('join.html')

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    # 클라이언트단에서 아이디, 비밀번호, 이름을 받아온다.
    userid_receive = request.form['userid_give']
    password_receive = request.form['password_give']
    username_receive = request.form['username_give']

    # 비밀번호는 해시함수로 암호화
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "userid": userid_receive,       # 아이디
        "password": password_hash,      # 비밀번호
        "username": username_receive,   # 이름

    }

    # DB에 해당 데이터를 저장한다.
    db.users.insert_one(doc)

    return jsonify({'result': 'success'})

# 회원가입 시 아이디 중복 확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():

    # 클라이언트단에서 넘겨받은 아이디를 DB에 조회 -> DB에 해당 id가 존재한다면 true, 조회되지 않는다면 false
    userid_receive = request.form['userid_give']
    exists = bool(db.users.find_one({"userid": userid_receive}))
    return jsonify({'result': 'success', 'exists': exists})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)