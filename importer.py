import psycopg2
import json
import sys
from pathlib import Path

DATABASE_NAME="imagedb"

db_connection=psycopg2.connect(dbname=DATABASE_NAME,user="imageuser",password="imageuser")
db_connection.autocommit=True

with db_connection.cursor() as cur:
    for dir_path in sys.argv[1:]:
        for image_f in Path(dir_path).iterdir():
            if not image_f.is_file():
                continue

            try:
                cur.execute("insert into images (name,path) values (%s,%s)",
                (
                    image_f.name,
                    image_f.resolve(),
                ))
            except Exception as e:
                print(e)
