from flask import Flask, render_template

from toapi import Api

app = Flask(__name__)


@app.route("/")
def index():
    html = Api().fetch("https://movie.douban.com/")
    return render_template("index.html", **{"html": html})


app.run(debug=True)
