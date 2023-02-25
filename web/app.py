from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # CSV 파일을 읽기
    with open('1.csv') as f:
        csv_data = [row for row in csv_data.reader(f)]

    # 렌더링할 HTML 템플릿에 데이터 전달
    
    return render_template('index.html', csv_data=csv_data)

if __name__ == '__main__':
    app.run()