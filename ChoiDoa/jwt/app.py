from lib2to3.pgen2 import driver

from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

# JWT Secret key create
SECRET_KEY = ''

# DB Connection
db = client.dbsparta_plus_week4

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('logout.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg=""))

# login 이 되면 로그아웃 페이지로 이동
@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/logout_click', methods=['GET'])
def logout_click():
    return redirect('index.html')

# 로그인 페이지 라우팅
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

# 회원가입 페이지 라우팅
@app.route('/join')
def join():
    msg = request.args.get("msg")
    return render_template('join.html', msg=msg)

# 메인페이지 라우팅
@app.route('/main')
def main():
    msg = request.args.get("msg")
    return render_template('index.html', msg=msg)

# 클라이언트가 요청한 데이터를 검증하여 매칭되는 유저 데이터가 있을 경우 토큰을 발행하며, 매칭되는 유저 정보가 없을 경우 토큰을 발행하지 않는다.
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인, 클라이언트가 보낸 데이터를 가지고 데이터베이스에서 해당 데이터가 실제로 존재하는지 검증
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    # 해시값을 만들어준다.
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # 아이디와 패스워드중 매칭되는 값이 있다면 성공
    result = db.user.find_one({'username': username_receive, 'password': pw_hash})

    # 클라이언트의 요청 데이터가 존재하는 데이터일 경우 JWT 를 발급
    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # JSON 타입의 HTTP 응답 데이터를 생성하여 return
        return jsonify({'result': 'success', 'token': token})
        render_template('logout.html')
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# 토큰이 잘 발행이 되었는지도 확인이 필요합니다.
# https://velog.io/@hwang-eunji/backend-django-JWT-%EB%B0%9C%ED%96%89%ED%95%98%EA%B8%B0