from flask import Flask, render_template, request
import os
from parser import parse_resume

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            data = parse_resume(file_path)
            return render_template("index.html", data=data)
    return render_template("index.html", data=None)

if __name__ == "__main__":
    app.run(debug=True)
