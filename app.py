from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from geopy.geocoders import ArcGIS
import pandas
from os import remove

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
            return render_template(
                "index.html",
                tables=[],
                text_invalid_file="text_invalid_file.html",
            )

        filename = "uploaded" + file.filename
        file.save(secure_filename(filename))

        # open file with pandas
        df = pandas.read_csv(filename)

        remove(filename)

        # check for address or Address
        column_name = get_column_name(df, ["address", "Address"])
        if not column_name:
            return render_template(
                "index.html",
                tables=[],
                text_invalid_file="text_invalid_file.html",
            )

        # add latitude and longitude if available
        nominator = ArcGIS(timeout=None)
        df["Coordinates"] = df[column_name].apply(nominator.geocode)
        df["Latitude"] = df["Coordinates"].apply(
            lambda x: x.latitude if x != None else None
        )
        df["Longitude"] = df["Coordinates"].apply(
            lambda x: x.longitude if x != None else None
        )
        df = df.drop("Coordinates", axis=1)

        # save yourfile.csv
        df.to_csv("yourfile.csv")

        return render_template(
            "index.html",
            tables=[df.to_html(classes="result_table", header="true")],
            button_download="button_download.html",
        )


def get_column_name(dataframe, valid_column_names):
    """
    Checks which valid column name is in dataframe and returns it if it exists.
    If more than one valid column name exists the first one is considered only.
    """
    for valid_column_name in valid_column_names:
        if valid_column_name in dataframe.columns:
            return valid_column_name
    return None


@app.route("/download")
def download():
    """Starts the file download for the user"""
    return send_file(
        filename_or_fp="yourfile.csv",
        attachment_filename="yourfile.csv",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.debug = True
    app.run()
