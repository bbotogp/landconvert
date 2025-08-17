from flask import Flask, render_template, request
# نفترض ان مكتبة yemen_land_converter مثبتة
from yemen_land_converter import LandConverter

app = Flask(__name__)
converter = LandConverter()

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    table = None
    if request.method == "POST":
        value = float(request.form["value"])
        from_unit = request.form["from_unit"]
        to_unit = request.form["to_unit"]
        gov = request.form.get("governorate") or None

        result = converter.convert(value, from_unit, to_unit, governorate=gov)
        table = converter.export_table(value, from_unit, governorate=gov)

    return render_template("index.html",
                           units=converter.list_units("Taiz"),
                           result=result, table=table)

if __name__ == "__main__":
    app.run(debug=True)
