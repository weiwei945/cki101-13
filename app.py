import os
import pymysql
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'cki101-dev-secret')

# -------------------------------------------------------
# 資料庫連線設定
# 本地開發：連 localhost:8625（docker expose 出來的 port）
# Container 內：連 mysql.cki101:3306（docker network 內部）
# 透過環境變數 DB_HOST / DB_PORT 切換，預設為本地開發設定
# -------------------------------------------------------
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 8625)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'database': os.environ.get('DB_NAME', 'cki101'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


def get_connection():git push origin main
    """取得 MySQL 連線"""
    return pymysql.connect(**DB_CONFIG)


def init_db():
    """初始化資料表（如不存在則建立）"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id   INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age  INT NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
        conn.commit()
    finally:
        conn.close()


# -------------------------------------------------------
# 路由
# -------------------------------------------------------

@app.route('/')
def index():
    return '我是功能一'


@app.route('/user', methods=['GET'])
def user_page():
    """顯示用戶管理頁面（含列表）"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, age FROM users ORDER BY id DESC;")
            users = cursor.fetchall()
        return render_template('user.html', users=users)
    finally:
        conn.close()


@app.route('/user', methods=['POST'])
def create_user():
    """新增用戶（表單送出）"""
    name = request.form.get('name', '').strip()
    age_str = request.form.get('age', '').strip()

    if not name or not age_str:
        flash('請填寫姓名與年紀', 'error')
        return redirect(url_for('user_page'))

    if not age_str.isdigit() or int(age_str) < 0:
        flash('年紀必須為非負整數', 'error')
        return redirect(url_for('user_page'))

    age = int(age_str)
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, age) VALUES (%s, %s);",
                (name, age)
            )
        conn.commit()
        flash(f'已成功新增用戶「{name}」', 'success')
    finally:
        conn.close()

    return redirect(url_for('user_page'))


@app.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """刪除用戶（表單送出）"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            affected = cursor.execute(
                "DELETE FROM users WHERE id = %s;", (user_id,)
            )
        conn.commit()
        if affected:
            flash(f'用戶 #{user_id} 已刪除', 'success')
        else:
            flash('找不到該用戶', 'error')
    finally:
        conn.close()

    return redirect(url_for('user_page'))


# -------------------------------------------------------
# 啟動
# -------------------------------------------------------

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
