from flask import Flask, render_template
import datetime

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 出席番号を計算し、リストとして返す関数
def calculate_attendance_loop():
    # プログラムを実行した日の日付を取得
    today = datetime.date.today()
    a = today.month
    b = today.day
    MODULO = 39

    # 計算ロジック
    x = (a * b) % MODULO
    R1 = x + 1
    if R1 >= MODULO:
        R1 -= MODULO

    results = []
    current_value = R1
    
    while current_value not in results:
        results.append(current_value)
        next_value = current_value + x
        if next_value >= MODULO:
            next_value -= MODULO
        current_value = next_value
        
    return a, b, results # 月、日、結果のリストを返す

# ルート (‘/’) にアクセスしたときの処理を定義
@app.route('/')
def home():
    # 計算関数を実行し、結果を受け取る
    month, day, attendance_list = calculate_attendance_loop()
    
    # HTMLテンプレートに結果を渡して表示
    return render_template('index.html', 
                           month=month, 
                           day=day, 
                           results=attendance_list)

# ファイルが直接実行されたときにサーバーを起動
if __name__ == '__main__':
    # 開発用サーバーの起動
    app.run(debug=True)