from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- ヘルパー関数 (修正なし) ---
def read_tasks_from_file():
    """ファイルからタスクを読み込んで辞書のリストとして返す"""
    try:
        with open("tasks.txt", "r", encoding="utf-8") as f:
            tasks = []
            for line in f.readlines():
                parts = line.strip().split(",", 1)
                if len(parts) == 2:
                    text, done_str = parts
                    done = (done_str == "True")
                    tasks.append({"text": text, "done": done})
            return tasks
    except FileNotFoundError:
        return []

def write_tasks_to_file(tasks):
    """タスクの辞書リストをファイルに書き込む"""
    with open("tasks.txt", "w", encoding="utf-8") as f:
        for task in tasks:
            done_str = str(task['done'])
            f.write(task['text'] + "," + done_str + "\n")

# --- アプリケーションの初期化 (修正なし) ---
tasks = read_tasks_from_file()

# --- 1. トップページ（/）の役割 ---
# GETリクエストのみを受け付け、タスク一覧を表示することに専念する
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

# --- 2. タスク追加（/add）の役割 ---
# POSTリクエストを受け付け、タスクを追加することに専念する
@app.route('/add', methods=['POST'])
def add_task():
    new_task_text = request.form['task']
    if new_task_text: # 空のタスクが追加されないようにチェック
        # 新しいデータ構造（辞書）でタスクを追加
        tasks.append({"text": new_task_text, "done": False})
        write_tasks_to_file(tasks)
    return redirect(url_for('index'))

# --- 3. タスク削除（/delete/<task_id>）の役割 (修正なし) ---
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        write_tasks_to_file(tasks)
    return redirect(url_for('index'))

# --- 4. タスク編集ページの表示（/edit/<task_id>）の役割 ---
# ロジックをシンプルに修正
@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    if 0 <= task_id < len(tasks):
        task_to_edit = tasks[task_id]
        # taskという名前で辞書ごと渡す
        return render_template('edit.html', task_id=task_id, task=task_to_edit)
    else:
        # 存在しないIDの場合はトップページに戻す
        return redirect(url_for('index'))

# --- 5. タスク更新処理（/update/<task_id>）の役割 ---
# ロジックを修正
@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if 0 <= task_id < len(tasks):
        updated_task_text = request.form['updated_task']
        # 辞書の中の'text'キーの値を上書きする
        tasks[task_id]['text'] = updated_task_text
        write_tasks_to_file(tasks) # 更新後もファイルに書き込む
    return redirect(url_for('index'))

# --- 6. タスクの完了状態を切り替える役割 ---
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        # 'done'の状態を反転させる (True -> False, False -> True)
        tasks[task_id]['done'] = not tasks[task_id]['done']
        write_tasks_to_file(tasks)
    return redirect(url_for('index'))

# この書き方で実行する場合
if __name__ == '__main__':
    app.run(debug=True)