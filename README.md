# image_searcher
- ブラウザ上で使うよ
- 画像にタグ付けできるよ
- [🐘PostgreSQL](https://www.postgresql.org/)に検索してもらいます


# Prerequisites 準備しておくもの
- [🐍Python3](https://www.python.org/)
- [🐘PostgreSQL](https://www.postgresql.org/)
- [🐍-🐘psycopg2](http://initd.org/psycopg/)

# Setup Database データベースの準備
1. データベースを作ります
    ```bash
    $ createdb -U postgres imagedb
    ```
2. テーブルとかを作ります
    ```bash
    $ psql -U postgres imagedb < imagedb_dump.sql
    ```

# Usage 使い方

1. Webサーバーを起動します
    ```bash
    $ python3 image_searcher.py
    ```
2. `index.html`を開きます
