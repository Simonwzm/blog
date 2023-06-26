import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os

class MyHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dst_dir):
        self.src_dir = src_dir
        self.dst_dir = dst_dir

    def on_modified(self, event):
        if not event.is_directory:
            shutil.copy2(event.src_path, os.path.join(self.dst_dir, os.path.basename(event.src_path)))

    def on_created(self, event):
        if not event.is_directory:
            shutil.copy2(event.src_path, os.path.join(self.dst_dir, os.path.basename(event.src_path)))

if __name__ == "__main__":
    src_path = r"D:\Simon\Program_Files\dropbox_sync\Dropbox\Sync\ObNotes\03 Knowledge\blog_posts"
    dst_path = r"D:\Simon\Dev\blog\source\_posts"

    event_handler = MyHandler(src_path, dst_path)
    observer = Observer()
    observer.schedule(event_handler, src_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
