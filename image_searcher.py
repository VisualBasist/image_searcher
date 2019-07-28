from http.server import *
from http import HTTPStatus
import shutil
import os
import urllib
import psycopg2
import json

SERVER_PORT=55000
SERVER_LISTEN_ADDRESS="127.0.0.1"
DATABASE_NAME="imagedb"

db_connection=psycopg2.connect(dbname=DATABASE_NAME,user="imageuser",password="imageuser")
db_connection.autocommit=True

class WebServer(BaseHTTPRequestHandler):
    def __init__(self,request, client_address, server):
        super().__init__(request,client_address,server)

    def fetch_images(self,sql_query):
        try:
            with db_connection.cursor() as cur:
                cur.execute(f"select distinct on (path) id,url,path,name,tags,(select name from authors where authors.author_id=images.author_id) as author_name from images,unnest(tags) as tag where {sql_query}")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type","application/json; charset=UTF-8")
                self.send_header("Access-Control-Allow-Origin","*")
                self.end_headers()

                #カラム名との辞書を作る
                name_data_map=[{d.name:f for d,f in zip(cur.description,row)} for row in cur.fetchall()]
                self.wfile.write(json.dumps(name_data_map,default=lambda date:date.isoformat()).encode())
        except psycopg2.ProgrammingError as e:
            self.send_response(HTTPStatus.BAD_REQUEST)
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps(str(e)).encode())
            
    def add_tag(self):
        taginfo=json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with db_connection.cursor() as cur:
            cur.execute("update images set tags=array_append(tags,%s) where id=%s",(taginfo["tag"],taginfo["id"]) )
        self.send_response(HTTPStatus.OK)
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()

    def do_GET(self):
        parsed_url=urllib.parse.urlparse(self.path)
        path=urllib.parse.unquote_plus(parsed_url.path)
        query_dict=urllib.parse.parse_qs(parsed_url.query)

        if path=="/images":
            self.fetch_images(query_dict["sql"][0])
            return
        
        self.send_error(HTTPStatus.BAD_REQUEST)
        self.end_headers()

    def do_POST(self):
        parsed_url=urllib.parse.urlparse(self.path)
        path=urllib.parse.unquote_plus(parsed_url.path)

        if path=="/add_tag":
            self.add_tag()
            return
        
        self.send_error(HTTPStatus.BAD_REQUEST)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=WebServer):
    httpd = server_class((SERVER_LISTEN_ADDRESS,SERVER_PORT), handler_class)
    httpd.serve_forever()

run(ThreadingHTTPServer)
