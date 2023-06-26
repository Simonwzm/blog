import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import subprocess
import threading


def deploy_blog():
    blog_dir = "D:\\Simon\\Dev\\blog"
    os.chdir(blog_dir)

    # Deploy with hexo
    hexo_command = 'hexo deploy -g'
    process = subprocess.Popen(hexo_command, shell=True)
    process.wait()

    # Execute git commands
    git_commands = [
        'git add -A',
        'git commit -m "update posts"',
        'git push origin main'
    ]

    for cmd in git_commands:
        process = subprocess.Popen(cmd, shell=True)
        process.wait()
deploy_blog()