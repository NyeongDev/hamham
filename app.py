# 패키지
import request
import certifi

from flask import Flask, render_template, jsonify
from pymongo import MongoClient

# mongodb
ca = certifi.where()
client = MongoClient('mongodb+srv://hcm:hcm1234@cluster0.9mbklpq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbhcm

app = Flask(__name__)

# 메인 페이지
@app.route('/')
def home():
    return render_template('main.html')

# 포스팅
@app.route('/post', methods=['POST'])
def posting():
    title_receive = request.form["title_give"]
    desc_receive = request.form["desc_give"]

    doc = {
        'title': title_receive,
        'desc': desc_receive
    }
    db.reviews.insert_one(doc)

    return jsonify({'msg':'등록 완료!'})
    err_display()

# 리뷰 리스트
@app.route('/reviews', methods=["GET"])
def reviews_get():
    reviews_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': reviews_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)