import sys
import time
import os
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
import subprocess
import datetime
import time

# build with /c/Python34/python -m py2exe.build_exe watcher.py --bundle-files 0 -d ./

try:
    path = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

def run_tiled2unity(event):
    CREATE_NO_WINDOW = 0x08000000
    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    p = subprocess.Popen([os.path.join(path,"Tiled2Unity/Tiled2Unity.exe"), 
            "-a", "-s=0.05", "-v", event.src_path, "../../"], 
            creationflags=CREATE_NO_WINDOW, startupinfo=info)
    p.wait()
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print ("[{}] Updating {} complete".format(st, os.path.basename(event.src_path)))

if __name__ == "__main__":
    print ("Watching for changes in tmx files")
    event_handler = RegexMatchingEventHandler(regexes=[r'.*\.tmx$'])
    event_handler.on_modified = run_tiled2unity
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()