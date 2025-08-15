### Source Code


import os
import signal
import psutil
import webview
import ctypes
import webbrowser
import requests

class Api:
    def kill_task(self, task_name):
        killed = []
        for p in psutil.process_iter(['name', 'pid']):
            try:
                if p.info['name'].lower() == task_name.lower():
                    os.kill(p.info['pid'], signal.SIGTERM)
                    killed.append(p.info['pid'])
            except:
                pass
        if killed:
            return {"status": "success", "killed": killed}
        else:
            return {"status": "error", "error": "No process found with that name."}

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Task Killer</title>
<style>
body { background: #060606; font-family: 'gg sans'; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
.Frame1 { width: 302px; height: 243px; position: relative; }
.Rectangle1 { width: 302px; height: 243px; position: absolute; background: #060606; border-radius: 16px; top: 0; left: 0; }
.TaskKiller { position: absolute; top: 6px; left: 68px; color: white; font-size: 36px; font-weight: 700; }
.MadeByPafxo { position: absolute; top: 222px; left: 202px; color: white; font-size: 12px; font-weight: 700; }
.RectangleInput { width: 241px; height: 44px; position: absolute; top: 70px; left: 31px; background: #000E68; border-radius: 5px; }
.TaskInput { position: absolute; top: 77px; left: 40px; width: 220px; height: 30px; font-size: 18px; color: white; background: transparent; border: none; outline: none; }
.RectangleKill { width: 241px; height: 44px; position: absolute; top: 146px; left: 31px; background: #FF0004; border-radius: 5px; cursor: pointer; display: flex; justify-content: center; align-items: center; color: white; font-size: 20px; font-weight: 700; }
</style>
</head>
<body>
<div class="Frame1">
  <div class="Rectangle1"></div>
  <div class="TaskKiller">Task Killer</div>
  <div class="MadeByPafxo">Made By Pafxo</div>
  <div class="RectangleInput"></div>
  <input class="TaskInput" id="taskName" placeholder="Enter task name">
  <div class="RectangleKill" onclick="killTask()">KILL TASK</div>
</div>

<script>
async function killTask() {
    const name = document.getElementById("taskName").value.trim();
    if(!name) { alert("Enter a task name"); return; }
    const res = await pywebview.api.kill_task(name);
    if(res.status === "success") {
        alert("Killed PIDs: " + res.killed.join(", "));
        document.getElementById("taskName").value = "";
    } else {
        alert("Error: " + res.error);
    }
}
</script>
</body>
</html>
"""

def fetch_github_message(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.text.strip()
    except:
        pass
    return None

if __name__ == "__main__":
    github_url = "https://raw.githubusercontent.com/pafxo2/ToolsPAFXO/refs/heads/main/Message"
    message = fetch_github_message(github_url)
    if message:
        MB_YESNO = 0x04
        MB_ICONINFORMATION = 0x40
        result = ctypes.windll.user32.MessageBoxW(0, message, "Welcome!", MB_YESNO | MB_ICONINFORMATION)
        if result == 6:
            for part in message.split():
                if part.startswith("http"):
                    webbrowser.open(part)
                    break

    api = Api()
    webview.create_window("Task Killer", html=html_content, js_api=api, width=350, height=300)
    webview.start()

### made by pafxo
