from flask import Flask, render_template
import datetime

app = Flask(__name__, static_folder='static')

def generate_list(target_date):
    # 1. 日付の取得と初期値の設定
    month = target_date.month
    day = target_date.day
    MAX_NUMBER = 39 # 出席番号の最大値 (1〜39)

    a = month
    b = day

    # 2. 初回計算
    initial_remainder = (a * b) % MAX_NUMBER 
    # 🌟 これが、次の番号に足していく値（あなたの例では 7）になります
    remainder_step = initial_remainder 
    R_1 = remainder_step + 1 # 最初の出席番号

    # 3. ループの生成
    results = []
    current_number = R_1

    for _ in range(MAX_NUMBER):
        # 現在の番号をリストに追加
        results.append(current_number)

        # 🌟 【ここを修正】次の番号の計算: 減算ではなく、剰余のステップ値 (remainder_step) を足す
        next_number = current_number + remainder_step 

        # 🌟 【ここを修正】MAX_NUMBER (39) を超えた場合、39を引いてループさせる
        if next_number > MAX_NUMBER:
            next_number -= MAX_NUMBER 
        
        current_number = next_number
    
    # ... (以下、変更なし)
    # 4. 結果を辞書形式で返す
    return {
        'month': month,
        'day': day,
        'results': results
    }

@app.route('/')
def index():
    # ... (変更なし)
    # 以下の部分は前回と変更ありません。
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    today_data = generate_list(today)
    tomorrow_data = generate_list(tomorrow)

    return render_template(
        'index.html',
        today=today_data,
        tomorrow=tomorrow_data
    )

if __name__ == '__main__':
    app.run(debug=True)