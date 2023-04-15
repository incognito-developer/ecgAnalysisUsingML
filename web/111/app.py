from flask import Flask, render_template, request,send_file, Response
from werkzeug.utils import secure_filename
import pandas as pd
app = Flask(__name__)
@app.route('/')
def upload():
    return render_template('home.html')
if __name__ == '__main__':
    app.run(debug=True)