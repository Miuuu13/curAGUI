import sys
from PyQt5 import *
from viewClassification import ViewClassification
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QLabel, QStackedWidget, QListWidget, QListWidgetItem, QFileDialog, QStyle)
from PyQt5.QtGui import QPainter, QLinearGradient, QBrush, QColor
from PyQt5.QtCore import Qt, QDateTime

class GradientWidget(QWidget):
    def __init__(self, startColor, endColor):
        super().__init__()
        self.startColor = startColor
        self.endColor = endColor

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, self.startColor)
        gradient.setColorAt(1, self.endColor)
        painter.fillRect(self.rect(), QBrush(gradient))

class CustomWidget(GradientWidget):
    def __init__(self, startColor, endColor, section, mainWindow):
        super().__init__(startColor, endColor)
        self.section = section
        self.mainWindow = mainWindow
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        if self.section == "Search":
            self.searchInput = QLineEdit(self)
            self.startSearchButton = QPushButton("Start search", self)
            layout.addWidget(self.searchInput)
            layout.addWidget(self.startSearchButton)
        elif self.section == "Dashboard":
            self.pathInput = QLineEdit(self)
            self.browseButton = QPushButton("Choose Directory", self)
            self.startReportButton = QPushButton("Start report", self)
            layout.addWidget(self.pathInput)
            layout.addWidget(self.browseButton)
            layout.addWidget(self.startReportButton)
            self.setAcceptDrops(True)
            self.browseButton.clicked.connect(self.openFileDialog)
            self.startReportButton.clicked.connect(self.report_button_clicked)
        elif self.section == "Report":
            self.label = QLabel(" ")
            self.label.setStyleSheet("background-color: white;")
            layout.addWidget(self.label)
        elif self.section == "Media":
            self.showMediaButton = QPushButton("Show media", self)
            layout.addWidget(self.showMediaButton)
        elif self.section == "Profile":
          #start add code for matplotlib
            self.canvas = MplCanvas(self, width=10, height=8, dpi=100)
            self.plot_data()
            layout.addWidget(self.canvas)
            self.setLayout(layout)
            #end add code for matplotlib
            currentTime = QDateTime.currentDateTime().toString("HH:mm, dd MMMM yyyy")
            profileText = f"Profile of Prof. Dr. med. A. Sclerosis \nLogged in since: {currentTime}"
            self.profileLabel = QLabel(profileText, self)
            layout.addWidget(self.profileLabel)
        elif self.section == "Sign out":
            self.signOutButton = QPushButton("Sign out", self)
            self.loggedOutLabel = QLabel(" ")
            layout.addWidget(self.signOutButton)
            layout.addWidget(self.loggedOutLabel)
            self.signOutButton.clicked.connect(self.showLoggedOut)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def openFileDialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory", "")
        self.pathInput.setText(dir_path)

    def showLoggedOut(self):
        self.loggedOutLabel.setText("Logged out")
        self.loggedOutLabel.setStyleSheet("color: red;")
    
    def report_button_clicked(self):
        input_text = self.pathInput.text()
        if input_text:
            ViewClassification(input_text)
        self.mainWindow.displayStackedWidget(2)

    #function for matplotlib
    def plot_data(self):
        # Plot für Komorbiditäten
        comorbidities = [
            "Cardiovascular disease", "Myocardial infarction", "Stroke", "Chronic heart failure",
            "Coronary artery disease", "Atrial fibrillation", "Peripheral artery disease",
            "Chronic obstructive pulmonary disease", "Deep vein thrombosis", "Chronic kidney disease",
            "Chronic lung disease", "Cancer"
        ]
        percentages = [61, 42, 13, 98, 69, 78, 1, 32, 73, 12, 50, 51]
        self.canvas.axes1.barh(comorbidities, percentages, color='skyblue')
        self.canvas.axes1.set_title('Comorbidities Percentages')
        self.canvas.axes1.set_xlabel('Percent')

        # Plot für kardiovaskuläre Risikofaktoren
        risk_factors = ['Diabetes', 'Obesity', 'Smoking', 'Hypertension', 'Dyslipidemia', 'Family history of MI/Stroke']
        presence = ['Yes', 'No', 'No', 'No', 'Yes', 'Yes']
        self.canvas.axes2.axis('tight')
        self.canvas.axes2.axis('off')
        table = self.canvas.axes2.table(cellText=list(zip(risk_factors, presence)),
                                        colLabels=['Cardiovascular Risk Factor', 'Presence'],
                                        cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        self.canvas.axes2.set_title('Cardiovascular Risk Factors')    
#end function for matplotlib

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sidebarList = QListWidget()
        self.items = [
            ('Search', QStyle.SP_FileDialogContentsView),
            ('Dashboard', QStyle.SP_DirHomeIcon),
            ('Report', QStyle.SP_BrowserReload),
            ('Prediction', QStyle.SP_FileDialogListView),
            ('Media', QStyle.SP_MediaPlay),
            ('Profile', QStyle.SP_ComputerIcon),
            ('Sign out', QStyle.SP_ArrowRight)
        ]
        for item_text, icon in self.items:
            item = QListWidgetItem(item_text)
            item.setIcon(self.style().standardIcon(icon))
            self.sidebarList.addItem(item)
        
        self.stackedWidget = QStackedWidget()
        self.colors = [
            (QColor(255, 255, 0), QColor(255, 255, 102)),  # Yellow to Light Yellow for Search
            (QColor(255, 165, 0), QColor(255, 200, 100)),  # Orange to Light Orange for Dashboard
            (QColor(255, 0, 0), QColor(255, 102, 102)),  # Red to Light Red for Report
            (QColor(128, 0, 128), QColor(185, 130, 185)),  # Purple to Light Purple for Prediction
            (QColor(0, 0, 255), QColor(102, 102, 255)),  # Blue to Light Blue for Media
            (QColor(144, 238, 144), QColor(190, 255, 190)),  # Light Green to Lighter Green for Profile
            (QColor(0, 100, 0), QColor(60, 160, 60))  # Dark Green to Light Green for Sign out
        ]
        sections = ['Search', 'Dashboard', 'Report', 'Prediction', 'Media', 'Profile', 'Sign out']
        
        for (startColor, endColor), section in zip(self.colors, sections):
            widget = CustomWidget(startColor, endColor, section, self)
            self.stackedWidget.addWidget(widget)
        
        self.sidebarList.currentRowChanged.connect(self.displayStackedWidget)
        
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.sidebarList, 1)
        hbox.addWidget(self.stackedWidget, 4)

        self.setLayout(hbox)
        self.setWindowTitle('curAGUI')
        self.setGeometry(300, 300, 900, 600)

    def displayStackedWidget(self, index):
        self.stackedWidget.setCurrentIndex(index)

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
