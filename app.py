from flask import Flask, render_template
import datetime

app = Flask(__name__, static_folder='static')

# 日付を受け取って、その日の出席番号リストを生成する新しい関数
def generate_list(target_date):
    # 1. 日付の取得と初期値の設定
    month = target_date.month
    day = target_date.day
    MAX_NUMBER = 39 # 出席番号の最大値 (1〜39)

    a = month
    b = day

    # 2. 初回計算
    # 剰余が0なら1番、剰余が38なら39番となるシンプルなロジックを採用
    initial_remainder = (a * b) % MAX_NUMBER 
    R_1 = initial_remainder + 1

    # 3. ループの生成
    results = []
    current_number = R_1

    for _ in range(MAX_NUMBER):
        # 現在の番号をリストに追加
        results.append(current_number)

        # 次の番号の計算: 4ずつ減らす
        next_number = current_number - 4

        # 0 または負の数になった場合、MAX_NUMBER (39) を足してループさせる
        if next_number <= 0:
            next_number += MAX_NUMBER
        
        current_number = next_number

    # 4. 結果を辞書形式で返す
    return {
        'month': month,
        'day': day,
        'results': results
    }

@app.route('/')
def index():
    # 1. 今日の日付を取得 (タイムゾーンはRenderの環境変数で設定済み)
    today = datetime.date.today()
    
    # 2. 翌日の日付を取得
    tomorrow = today + datetime.timedelta(days=1)
    
    # 3. それぞれの日付でリストを生成
    today_data = generate_list(today)
    tomorrow_data = generate_list(tomorrow)

    # 4. HTMLに両方のデータを渡す
    return render_template(
        'index.html',
        today=today_data,
        tomorrow=tomorrow_data
    )

# ローカルテスト用コード
if __name__ == '__main__':
    app.run(debug=True)