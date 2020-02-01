# image_searcher
- ブラウザ上で使うよ
- 画像にタグ付けできるよ
- [🐘PostgreSQL](https://www.postgresql.org/)に検索してもらいます


# Prerequisites 準備しておくもの
- [🐍Python3](https://www.python.org/)
- [🐘PostgreSQL](https://www.postgresql.org/)
- [🐍-🐘psycopg2](http://initd.org/psycopg/)

# Setup Database データベースの準備
1. データベース接続用のユーザーを作成します。パスワードは`imageuser`で
    ```bash
    $ createuser -U postgres imageuser
    ```
2. データベースを作ります
    ```bash
    $ createdb -U postgres imagedb
    ```
3. データベースのテーブルや権限を設定します
    ```bash
    $ psql -U postgres imagedb < imagedb_dump.sql
    ```

# Usage 使い方

1. 画像を登録します(このツールは未完成)
    ```bash
    $ python3 importer.py 登録したいフォルダのパス
    ```
2. Webサーバーを起動します
    ```bash
    $ python3 image_searcher.py
    ```
3. `index.html`を開きます
