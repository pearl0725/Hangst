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
app.secret_key = "CHOIDOA"

# DB Connection
db = client.dbsparta_plus_week4

# DB connection TEST
print(db)

user_select = db.user.find_one({'id': 'doa'})
TEST = db.user.find_one({'id': 'doa', 'pw': 1234})
print(TEST)


# 로그아웃시 테스트용이므로 무시해주세요.
@app.route('/')
def login_fail():
    return render_template('login2.html')


# @app.route('/login')
# def login_page():
#     if request.method == 'GET':
#         return render_template('login2.html')


# @app.route('/login', methods=['POST'])
# def login():
#     username_receive = request.form.get('id', False)
#     user_password = request.form.get('pw', False)
#     print(username_receive, user_password)
#
#     result = db.user.find_one({'id': username_receive}, {'pw': user_password})
#     print(result)
#
#     if result is not None:
#         session['id'] = username_receive
#         return redirect('/')
#     else:
#         return "로그인 실패"


# 로그인 인증 API
@app.route('/login', methods=['GET', 'POST'])   #  login 페이지 접속과 "action=/login" form 데이터(POST) 를 처리하기 위해 GET, POST 방식으로 모두 정의
def login():
    # 최초 /login 으로 접근시 요청방식이 GET 방식인 경우 login2.html 페이지 렌더링
    if request.method == 'GET':
        return render_template('login2.html')
    else:
        # GET 방식으로 요청된 데이터가 아닐 경우 사용자가 로그인 시도를 해서 데이터를 전달했다는 것이므로 거짓이 되어 하단의 동작을 수행합니다.
        # 사용자에게 입력받은 id 와 pw 값을 변수에 담습니다.
        username_receive = request.form.get('id', False)
        user_password = request.form.get('pw', False)
        print(username_receive, user_password)
        # 변수에 담긴 데이터로 컬렉션에 저장된 데이터의 값과 일치한 값이 있다면 유저의 id 를 세션에 저장합니다.
        # 아니라면 로그인 실패를 출력합니다. 로그인 실패 옆에는 데이터를 잘 받는지 테스트하기 위해 작성한 내용이므로 무시해주세요.
        try:
            result = db.user.find_one({'id': username_receive}, {'pw': user_password})
            print(type(result))
            if result is not None:
                session['id'] = username_receive
                return redirect('/')
            else:
                return "로그인 실패"
        except:
            return "로그인 실패 예외상황"

# 사용자가 로그아웃 버튼을 클릭하면 세션을 삭제하고 login2.html 페이지로 렌더링한다.
@app.route("/logout", methods=['POST'])
def logout():
    session.pop("id", None)
    return render_template('login2.html')

# 기존 서버가 동작하고 있는 상태에서 테스트를 하기 위해 5001 번 포트로 서버가 동작하게끔 하였습니다. 무시해주세용.
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

