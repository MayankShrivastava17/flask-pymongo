from flask import Flask, render_template, request, jsonify, url_for
import pymongo
from bson import json_util, ObjectId
import json
from datetime import datetime, date
from flask.helpers import url_for

# initilize flask application
app = Flask(__name__)
# add the secret key
app.secret_key = "pyblogger"
# add to localhost
client = pymongo.MongoClient(
    "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
)
# create the collection
db = client.get_database('pyblogger')
record = db.blog


@app.route('/', methods=['get', 'post'])
def index():
    try:
        blog = record.find({}, {"Title", "Blog", "Upload Time", "Upload Date"})
        return render_template('index.html', blogs=blog)
    except Exception as e:
        chk = {
            "Error": "This is error"
        }
        return jsonify(chk)


@app.route('/blog', methods=['get', 'post'])
def blog():
    title = request.form.get('tit')
    blog = request.form.get('blog')
    if title != '' and blog != '':
        now = datetime.now()
        curr = now.strftime("%H:%M:%S")
        today = date.today()
        td = today.strftime("%d/%m/%Y")
        user_input = {
            'Title': title,
            'Blog': blog,
            'Upload Date': td,
            'Upload Time': curr
        }
        chk = record.find_one({'Title': title})
        if chk:
            pass
        else:
            record.insert_one(user_input)
    return render_template('create.html')

# handing the error


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
