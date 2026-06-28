# Work Log

## [2026-06-28] Initial project setup
- Created `history/work_log.md`
- Created `requirements.txt`
- Created `app.py`
- Created `Dockerfile`
- Created `.dockerignore`
- Created Python virtual environment `.venv` and installed dependencies from `requirements.txt`
- Created `docker-compose.yml` for container orchestration with port mapping (80:5000)
- Created `.gitignore` for git version control exclusion
- Optimized `docker-compose.yml` by removing obsolete `version` attribute

## [2026-06-28] 新增 MySQL 8.4 服務與用戶 CRUD 功能
- `docker-compose.yml`：追加 MySQL 8.4 service（container name: mysql.cki101，port 8625:3306，db_data volume）
- `docker-compose.yml`：web service 加入 depends_on mysql 與環境變數（DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME）
- `requirements.txt`：追加 PyMySQL==1.1.1
- `app.py`：新增用戶 CRUD API
  - `GET  /users` — 查詢所有用戶
  - `GET  /users/<id>` — 查詢單一用戶
  - `POST /users` — 新增用戶（body: name, age）
  - `DELETE /users/<id>` — 刪除用戶
  - 透過環境變數切換本地（localhost:8625）與 container 內（mysql.cki101:3306）連線
  - 啟動時自動建立 users 資料表（若不存在）

## [2026-06-28] 改為圖形化介面（Web UI）
- `templates/user.html`：新建深色系用戶管理頁面，含新增表單與刪除按鈕
- `app.py`：移除 JSON API，改用 render_template + HTML 表單 POST
  - `GET  /user` — 顯示用戶列表頁面
  - `POST /user` — 新增用戶（表單送出後 redirect）
  - `POST /user/<id>/delete` — 刪除用戶（表單送出後 redirect）
  - 加入 flash 訊息顯示操作結果






