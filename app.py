from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
EXCEL_FILE = 'rent.xlsx'

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["학번", "이름", "전화번호", "우산번호", "대여일자"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/')
def index():
    df = pd.read_excel(EXCEL_FILE)
    today = datetime.today()
    df['연체일수'] = (today - pd.to_datetime(df['대여일자'])).dt.days
    return render_template('index.html', data=df.to_dict('records'))

@app.route('/rent', methods=['POST'])
def rent():
    학번 = request.form['student_id']
    이름 = request.form['name']
    전화 = request.form['phone']
    우산번호 = request.form['umbrella_no']
    날짜 = datetime.today().strftime('%Y-%m-%d')

    df = pd.read_excel(EXCEL_FILE)
    df = pd.concat([df, pd.DataFrame([{
        "학번": 학번,
        "이름": 이름,
        "전화번호": 전화,
        "우산번호": 우산번호,
        "대여일자": 날짜
    }])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    return redirect('/')

@app.route('/return', methods=['POST'])
def return_umbrella():
    학번 = request.form['student_id']
    이름 = request.form['name']
    df = pd.read_excel(EXCEL_FILE)
    df = df[~((df['학번'] == 학번) & (df['이름'] == 이름))]
    df.to_excel(EXCEL_FILE, index=False)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)


