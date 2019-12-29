import sys
import psutil
import notify2
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QAction
import threading
import images_rc

class MyProcess(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
    def run(self):
        while True:
            notify2.init("Battery Alerts")
            battery = psutil.sensors_battery()
            plugged = battery.power_plugged
            percent = str(round(battery.percent))
            msg = ""
            if plugged == False and int(percent) < 80:
                msg = "Charge is only " + percent + "% please charge the laptop now!!!"
                n = notify2.Notification("Battery is too low!", message=msg)
                n.set_urgency(notify2.URGENCY_CRITICAL)
                n.show()
            time.sleep(60)
        return
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)

        exitAction= QAction("&Quit", self,triggered=QtWidgets.QApplication.instance().quit)
        exitAction.setIcon(QtGui.QIcon('images/exit.png'))
        exitAction.triggered.connect(parent.close)
        menu.addAction(exitAction)
        self.setContextMenu(menu)

class windows(QtWidgets.QWidget):
    def __init__(self):
        super(windows, self).__init__()
        self.trayicon = SystemTrayIcon(QtGui.QIcon('images/bat.png'), self)
        self.trayicon.show()
        thread1 = MyProcess(self)
        thread1.start()
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = windows()
    window.setWindowTitle("Low Battery Notification")
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    sys.exit(app.exec_())


