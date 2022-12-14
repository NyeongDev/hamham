# 패키지GET / HTTP/1.1" 200 -
import certifi
import jwt
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime, timedelta

# mongodb
ca = certifi.where()
client = MongoClient('mongodb+srv://hello:sparta@cluster0.re0stef.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta_plus_week4

app = Flask(__name__)
app.config.update(
    ENV="development",
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True
)
SECRET_KEY = 'SPARTA'


# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')

# 리뷰 리스트
@app.route('/index', methods=["GET"])
def reviews_get():
    reviews_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': reviews_list})

@app.route('/tk')
def tk():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "profile_name": username_receive,  # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})
    return "success"


# 포스트 페이지
@app.route('/post')
def post():
    return render_template('post.html')

# 포스팅
@app.route('/post/send', methods=['POST'])
def posting():
    desc_receive = request.form["desc_give"]
    title_receive = request.form["title_give"]

    doc = {
        'title': title_receive,
        'desc': desc_receive
          }
    db.reviews.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)