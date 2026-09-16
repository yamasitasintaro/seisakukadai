import json
import random
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# jsonから読み込む

# ファイル名を指定して読み込むための関数
def load_json(filename):
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
player_status = load_json("player.json")["sutatus"].copy()

# json に保存する関数
def save_json(filename, data):
    filepath = os.path.join(BASE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)



class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("GET:", self.path)

        # if self.path == "/":
        if self.path.startswith("/static/"):
            self.serve_static(self.path)
            return
        
        if self.path == "/":
            html = self.render_template("index.html")

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))
            return

        if self.path.startswith("/menu"):

            status = player_status
            html = self.render_template("menu.html")

            status_html = f"""
            <div>
                <p>名前：{status["name"]}</p>
                <p>HP：{status["HP"]}</p>
                <p>ATK：{status["ATK"]}</p>
                <p>所持ゴールド：{status["G"]}</p>
                <p>現在の階層：{status["froa"]}</p>
            </div>
            """
            html = html.replace("{{ p_status }}",status_html)       

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))
            return
        
        if self.path.startswith("/load"):

            html = self.render_template("lode.html")

            save_html = ""

            for i in range(1, 4):

                filename = f"save{i}.json"
                filepath = os.path.join(BASE_DIR, filename)

                save_data = None

                if os.path.exists(filepath):
                    try:
                        save_data = load_json(filename)
                    except (json.JSONDecodeError, FileNotFoundError):
                        save_data = None

                if save_data:
                    save_html += f"""
                    <div>
                        <h2>データ{i}</h2>
                        <p>名前：{save_data["name"]}</p>
                        <p>HP：{save_data["HP"]}</p>
                        <p>ATK：{save_data["ATK"]}</p>
                        <p>G：{save_data["G"]}</p>
                        <p>階層：{save_data["froa"]}</p>

                        <form method="post" action="/load">
                            <button type="submit" name="slot" value="{i}">
                                ロード
                            </button>
                        </form>
                    </div>
                    <hr>
                    """
                else:
                    save_html += f"""
                    <div>
                        <h2>データ{i}</h2>
                        <p>空きデータ</p>
                    </div>
                    <hr>
                    """

            html = html.replace("{{ save_data }}", save_html)

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(html.encode("utf-8"))

            return
        if self.path.startswith("/save"):
            html = self.render_template("save.html")

            save_data_html = ""

            for i in range(1, 4):
                filename = f"save{i}.json"
                filepath = os.path.join(BASE_DIR, filename)

                data = None

                if os.path.exists(filepath):
                    try:
                        data = load_json(filename)
                    except (json.JSONDecodeError, FileNotFoundError):
                        data = None

                if data:
                    save_data_html += f"""
                    <div class="save-slot">
                        <h3>セーブ{i}</h3>
                        <p>名前：{data["name"]}</p>
                        <p>HP：{data["HP"]}</p>
                        <p>ATK：{data["ATK"]}</p>
                        <p>G：{data["G"]}</p>
                        <p>階層：{data["froa"]}</p>

                        <form method="post" action="/save">
                            <input type="hidden" name="slot" value="{i}">
                            <button type="submit">このスロットにセーブ</button>
                        </form>
                    </div>
                    """
                
                else:
                    save_data_html += f"""
                    <div class="save-slot">
                        <h3>セーブ{i}</h3>
                        <p>空きデータ</p>

                        <form method="post" action="/save">
                            <input type="hidden" name="slot" value="{i}">
                            <button type="submit">このスロットにセーブ</button>
                        </form>
                    </div>
                    """

            html = html.replace("{{ save_data }}", save_data_html)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

            return

        
    # ゲームの挙動やボタン操作など
    def do_POST(self):
        # if self.path == "/":
        
        if self.path == "/start":
            # 送られてきたデータのサイズを取得
            content_length = int(self.headers["Content-Length"])

            # データを読み込む
            post_data = self.rfile.read(content_length).decode("utf-8")

           # フォームのデータを辞書に変換
            data = parse_qs(post_data)

            # 名前を取得
            name = data.get("name", [""])[0]
            player_status["name"] = name

            print("プレイヤー名:", name)

            # ゲーム画面を表示
            self.send_response(303)
            self.send_header("Location", "/menu")
            self.end_headers()
            return

        if self.path == "/end":
            html = self.render_template("index.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

       
        if self.path == "/save":

            content_length = int(self.headers["Content-Length"])

            post_data = self.rfile.read(content_length).decode("utf-8")

            data = parse_qs(post_data)

            slot = data.get("slot", ["1"])[0]

            filename = f"save{slot}.json"

            save_json(filename, player_status)

            self.send_response(303)
            self.send_header("Location", "/menu")
            self.end_headers()

            return

        if self.path.startswith("/load"):

            content_length = int(self.headers["Content-Length"])

            post_data = self.rfile.read(content_length).decode("utf-8")

            data = parse_qs(post_data)

            slot = data.get("slot", ["1"])[0]

            filename = f"save{slot}.json"

            save_data = load_json(filename)

            player_status.clear()
            player_status.update(save_data)

            self.send_response(303)
            self.send_header("Location", "/menu")
            self.end_headers()

            return
        

    # htmlの取り込み
    def render_template(self, filename):
        filepath = os.path.join(BASE_DIR, "templates", filename)

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
        
    # cssの取り込み
    def serve_static(self, path):

        filepath = path[1:]

        with open(filepath, "rb") as f:
            content = f.read()

        if path.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        else:
            content_type = "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

        self.wfile.write(content)

    


def run():
    server = HTTPServer(("", 8000), MyHandler)
    print("🚀 サーバーを起動しました")
    print("http://localhost:8000")

    server.serve_forever()


if __name__ == "__main__":
    run()