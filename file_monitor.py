# import sys
# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import shutil
# import os

# class Watcher:
#     def __init__(self, src_path, dest_path):
#         self.src_path = src_path
#         self.dest_path = dest_path
#         self.observer = Observer()

#     def run(self):
#         event_handler = Handler(self.src_path, self.dest_path)
#         self.observer.schedule(event_handler, self.src_path, recursive=True)
#         self.observer.start()
        
#         try:
#             while True:
#                 time.sleep(5)
#         except KeyboardInterrupt:
#             self.observer.stop()
        
#         self.observer.join()

# class Handler(FileSystemEventHandler):
#     def __init__(self, src_path, dest_path):
#         self.src_path = src_path
#         self.dest_path = dest_path

#     def on_modified(self, event):
#         if event.is_directory:
#             return None
#         else:
#             self.copy_file(event.src_path)

#     def on_created(self, event):
#         if event.is_directory:
#             return None
#         else:
#             self.copy_file(event.src_path)

#     def copy_file(self, file_path):
#         shutil.copy2(file_path, self.dest_path)
#         print(f"Copied '{file_path}' to '{self.dest_path}'")

# if __name__ == "__main__":
#     src_path = r"D:\Simon\Program_Files\dropbox_sync\Dropbox\Sync\ObNotes\03 Knowledge\blog_posts"
#     dest_path = r"D:\Simon\Dev\blog\source\_posts"
    
#     watcher = Watcher(src_path, dest_path)
#     watcher.run()
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os

class Watcher:
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path
        self.observer = Observer()

    def run(self):
        event_handler = Handler(self.src_path, self.dest_path)
        self.observer.schedule(event_handler, self.src_path, recursive=True)

    def stop(self):
        self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def on_modified(self, event):
        if event.is_directory:
            return None
        else:
            self.copy_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            self.copy_file(event.src_path)

    def copy_file(self, file_path):
        shutil.copy2(file_path, self.dest_path)
        print(f"Copied '{file_path}' to '{self.dest_path}'")
