import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTextEdit, QLabel, QMessageBox, QFileDialog)
from PyQt5.QtGui import QFont

class NoteGui(QWidget):

    def __init__(self, email_message):
        super().__init__()
        self.message = email_message
        self.initializeUI()
        
    
    def initializeUI(self):

        self.setGeometry(100, 100, 400, 500)
        self.setWindowTitle('4.1 – Notepad GUI')
        self.notifWidgets()
        self.show()

    def notifWidgets(self):

        #NEW EMAIL TEXT
        new_email = QLabel(self)
        new_email.setText("New Email")
        new_email.move(120, 10)
        new_email.setFont(QFont('Georgia', 20))

        #Field where to display emails
        self.text_field = QTextEdit(self)
        self.text_field.resize(300, 400)
        self.text_field.move(50, 80)
        self.text_field.setText(self.message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteGui('Helloooooo')   #Just for testing
    sys.exit(app.exec_())