import os
import sys
import time
import threading
import clr

clr.AddReference('System.ServiceProcess')
from System.ServiceProcess import ServiceBase, ServiceController
from System.Threading import Thread

from file_monitor import Watcher

class FileMonitorServiceThreaded(ServiceBase):
    _svc_name_ = 'FileMonitor'
    _svc_display_name_ = 'File Monitor Service'

    def __init__(self, args):
        ServiceBase.__init__(self, args)
        self.thread = None

    def OnStart(self, args):
        thread_start = threading.ThreadStart(self.main)
        self.thread = Thread(thread_start)
        self.thread.Start()

    def OnStop(self):
        watcher.stop()
        self.thread.Join()

    def main(self):
        src_path = r"D:\Simon\Program_Files\dropbox_sync\Dropbox\Sync\ObNotes\03 Knowledge\blog_posts"
        dest_path = r"D:\Simon\Dev\blog\source\_posts"

        global watcher
        watcher = Watcher(src_path, dest_path)
        watcher.run()

if __name__ == '__main__':
    from System import Array
    from System.ServiceProcess import ServiceBase, ServiceProcessInstaller, ServiceInstaller
    from System.Configuration.Install import Installer, InstallContext
    import traceback

    if len(sys.argv) == 1:
        ServiceBase.Run(Array[ServiceBase]([FileMonitorServiceThreaded()]))
    elif sys.argv[1] == "install":
        try:
            # Install the service
            my_service = ServiceInstaller()
            my_service.Context = InstallContext("install.log", None)
            my_service.DisplayName = FileMonitorServiceThreaded._svc_display_name_
            my_service.ServiceName = FileMonitorServiceThreaded._svc_name_
            my_service.StartType = System.ServiceProcess.ServiceStartMode.Automatic

            process_installer = ServiceProcessInstaller()
            process_installer.Account = System.ServiceProcess.ServiceAccount.LocalSystem

            my_service.Parent = process_installer

            my_service.Install(New-Object System.Collections.Hashtable)

            print("Service installed successfully!")
        except Exception as e:
            print("Error installing service: ", e)
            traceback.print_exc()
    elif sys.argv[1] == "uninstall":
        try:
            controller = ServiceController(FileMonitorServiceThreaded._svc_name_)
            if controller.Status != System.ServiceProcess.ServiceControllerStatus.Stopped:
                print("Stopping service...")
                controller.Stop()

            # Uninstall the service
            my_service = ServiceInstaller()
            my_service.Context = InstallContext(None, sys.argv)
            my_service.ServiceName = FileMonitorServiceThreaded._svc_name_

            my_service.Uninstall(None)

            print("Service uninstalled successfully!")
        except Exception as e:
            print("Error uninstalling service: ", e)
            traceback.print_exc()
