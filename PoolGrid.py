import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.newWindows = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Okno główne')
        self.setGeometry(100, 100, 800, 400)
        
        for i in range(8):
            for j in range(4):
                button = QPushButton(f'{i},{j}', self)
                button.setStyleSheet('background-color: white;')
                button.clicked.connect(self.openNewWindow)
                button.setFixedSize(100, 100)
                button.move(i * 100, j * 100)
                
        self.show()

    def check_collision(self, new_window_rect):
        for window in self.newWindows:
            if window.geometry().intersects(new_window_rect):
                return True
        return False

    def closeNewWindow(self):
        new_window = self.sender().parent()
        new_window.close()
        self.newWindows.remove(new_window)
        
    def openNewWindow(self):
        button = self.sender()
        pos = button.pos()

        x = pos.x() + self.frameGeometry().x()
        y = pos.y() + self.frameGeometry().y() + 30
        max_width = (self.geometry().width() - x) // 100
        max_height = (self.geometry().height() - y) // 100
        min_width = 1
        min_height = 1

        # szukanie największego możliwego obszaru bez kolizji
        for height in range(max_height, -1, -1):
            for width in range(max_width, -1, -1):
                new_window_rect = QRect(x, y, (width+1) * 100, (height+1) * 100)
                if not self.check_collision(new_window_rect) and (width+1>1 or height+1>1):
                    min_width = width+1
                    min_height = height+1
                    break
            if min_width > 1:
                break

        if min_width < 1 and min_height < 1:
            QMessageBox.warning(self, "ALERT", "F u c k Y o u !")
            return

        new_window = QWidget(self, Qt.Window | Qt.FramelessWindowHint)
        new_window.setGeometry(x, y, min_width * 100, min_height * 100)

        # ustawienie kształtu okna na prostokąt lub kwadrat
        if min_width >= 1 or min_height >= 1:
            new_window.setFixedSize(min_width * 100, min_height * 100)

        closeButton = QPushButton('X', new_window)
        closeButton.setGeometry(0, 0, 50, 25)
        closeButton.clicked.connect(self.closeNewWindow)


        new_window.show()
        self.newWindows.append(new_window)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
