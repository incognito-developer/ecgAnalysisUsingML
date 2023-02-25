from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)

@app.route('/')
def upload():
    return render_template('upload.html')
@app.route('/data',methods=['GET','POST'])
def csvfile():
    if request.method == 'POST':
        f = request.files['csvfile']
        f.save(secure_filename(f.filename))
        csv_data = pd.read_csv(secure_filename(f.filename))
        return render_template('data.html', csv_data=csv_data)
if __name__ == '__main__':
    app.run(debug=True)