import os
import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from file_monitor import Watcher

class FileMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'FileMonitor'
    _svc_display_name_ = 'File Monitor Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        src_path = r"D:\Simon\Program_Files\dropbox_sync\Dropbox\Sync\ObNotes\03 Knowledge\blog_posts"
        dest_path = r"D:\Simon\Dev\blog\source\_posts"

        watcher = Watcher(src_path, dest_path)
        watcher.observer.start()

        while self.is_alive:
            time.sleep(5)

        watcher.observer.stop()
        watcher.observer.join()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FileMonitorService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FileMonitorService)
