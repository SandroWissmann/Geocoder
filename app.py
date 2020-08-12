from flask import Flask, render_template, request, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def success():
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
