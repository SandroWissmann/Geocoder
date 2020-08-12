from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas

app = Flask(__name__)


@app.route("/")
def index():
    """Shows the main page of the webapp"""
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def success():
    """
    If a valid CSV file is uploaded generate add geometrical 
    information to the file and return it
    """
    if request.method == "POST":
        file = request.files["file"]
        if not file.filename.endswith(".csv"):
            return render_template("index.html")

        filename = "uploaded" + file.filename
        file.save(secure_filename(filename))

        # open file with pandas

        # check for address or Address

        # add latitude and longitude if available

        # save yourfile.csv

        return render_template(
            "index.html", button_download="button_download.html"
        )


@app.route("/download")
def download():
    pass


if __name__ == "__main__":
    app.debug = True
    app.run()
