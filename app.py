from flask import Flask, render_template, request
import datetime

app = Flask(__name__, static_folder='static')

def generate_list(target_date):
    # 1. 日付の取得と初期値の設定
    month = target_date.month
    day = target_date.day
    MAX_NUMBER = 39 # 出席番号の最大値

    a = month
    b = day

    # 2. 初回計算
    initial_remainder = (a * b) % MAX_NUMBER 
    remainder_step = initial_remainder 
    R_1 = remainder_step + 1 # 最初の出席番号

    # 3. ループの生成 (加算ロジック)
    results = []
    current_number = R_1

    for _ in range(MAX_NUMBER):
        results.append(current_number)
        
        # 次の番号の計算: 剰余のステップ値を足す
        next_number = current_number + remainder_step 

        # MAX_NUMBER (39) を超えた場合、39を引いてループさせる
        if next_number > MAX_NUMBER:
            next_number -= MAX_NUMBER 
        
        current_number = next_number
    
    return {
        'month': month,
        'day': day,
        'results': results
    }

# methods=['GET', 'POST'] を追加して、フォームからの送信を許可する
@app.route('/', methods=['GET', 'POST'])
def index():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    today_data = generate_list(today)
    tomorrow_data = generate_list(tomorrow)
    
    # 検索結果を入れる変数（最初は空っぽ）
    search_result = None

    # もし「調べる」ボタンが押されたら (POSTリクエスト)
    if request.method == 'POST':
        # フォームから日付を受け取る
        date_str = request.form.get('target_date')
        if date_str:
            # 文字列 '2025-01-01' を日付データに変換
            year, month, day = map(int, date_str.split('-'))
            target_date = datetime.date(year, month, day)
            # その日付でリストを作成
            search_result = generate_list(target_date)

    return render_template(
        'index.html',
        today=today_data,
        tomorrow=tomorrow_data,
        search_result=search_result # 検索結果も渡す
    )

if __name__ == '__main__':
    app.run(debug=True)