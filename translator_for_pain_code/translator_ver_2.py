from PyQt5 import QtCore, QtGui, QtWidgets
import random, re
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon, QPixmap

WORKING_FILE_NAME = 'work_dict_2.txt'
word_dict = {} #Словарь хранящий набор слов из файла данных
list_of_try ={}   #Словарь хранящий количество попыток для каждого слова из выбранного файла данных(того же что и для word_dict) 
var_for_safe_key_from_func_play = str  #глобальная переменная для связи функций play() и not_know(). Нужна для того чтобы not_know() выдала именно то слово что сейчас в play()
first_20 = []  #переменная для функции sort(), хранящая 20 слов с наименьшим количеством попыток


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.eng_text_area = QtWidgets.QLineEdit(self.centralwidget)
        self.eng_text_area.setGeometry(QtCore.QRect(0, 90, 800, 65))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.eng_text_area.setFont(font)
        self.eng_text_area.setText("")
        self.eng_text_area.setObjectName("eng_text_area")
        self.rus_text_area = QtWidgets.QLabel(self.centralwidget)
        self.rus_text_area.setGeometry(QtCore.QRect(0, 10, 800, 75))
        MainWindow.setWindowIcon(QIcon('icon3.png'))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.rus_text_area.setFont(font)
        self.rus_text_area.setText("")
        self.rus_text_area.setObjectName("rus_text_area")
        self.btn_check = QtWidgets.QPushButton(self.centralwidget)
        self.btn_check.setGeometry(QtCore.QRect(70, 240, 671, 28))
        self.btn_check.setObjectName("btn_check")
        self.btn_play = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play.setGeometry(QtCore.QRect(70, 310, 671, 28))
        self.btn_play.setObjectName("btn_play")
        self.btn_not_know = QtWidgets.QPushButton(self.centralwidget)
        self.btn_not_know.setGeometry(QtCore.QRect(70, 275, 671, 28))
        self.btn_not_know.setObjectName("btn_not_know")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")

        self.progress = QtWidgets.QMenu(self.menubar)
        self.progress.setObjectName("progress")
        self.option = QtWidgets.QMenu(self.menubar)
        self.option.setObjectName("option")
        
        self.menubar.addAction(self.progress.menuAction())
        self.menubar.addAction(self.option.menuAction())

        self.saveProgress = QtWidgets.QAction(MainWindow)
        self.saveProgress.setObjectName("save_progress")
        self.saveProgress.triggered.connect(self.save_progress_clicked)
        self.progress.addAction(self.saveProgress)
        self.updateTry = QtWidgets.QAction(MainWindow)
        self.updateTry.setObjectName("updateTry")
        self.updateTry.triggered.connect(nullify_attempt)
        self.option.addAction(self.updateTry)

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_function()

        read_a_file(WORKING_FILE_NAME)
        sort()
        
       
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Translator for pain"))
        self.progress.setTitle(_translate("MainWindow", "Прогресс"))
        self.saveProgress.setText(_translate("MainWindow", "Сохранить прогресс"))
        self.option.setTitle(_translate("MainWindow", "Опции"))
        self.updateTry.setText(_translate("MainWindow", "Обновить попытки"))
        self.btn_check.setText(_translate("MainWindow", "Проверить"))
        self.btn_not_know.setText(_translate("MainWindow", "Не знаю"))
        self.btn_play.setText(_translate("MainWindow", "Play"))
    
    def add_function(self):
        self.btn_play.clicked.connect(self.play)
        self.btn_not_know.clicked.connect(self.not_know)
        self.btn_check.clicked.connect(self.check)
        self.btn_check.setAutoDefault(True)
        self.eng_text_area.returnPressed.connect(self.check)

    def play(self):
        """Основная функция, срабатывает при нажатии Play"""
        if len(first_20) > 0:
            key = random.choice(first_20)
            global var_for_safe_key_from_func_play 
            while True:
                if len(first_20) > 1 and key == var_for_safe_key_from_func_play:
                    key = random.choice(first_20)
                else:
                    break
            
            var_for_safe_key_from_func_play = key
            list_of_try[key] += 1
            self.rus_text_area.setText(word_dict[key])
            self.eng_text_area.setText("")
            if list_of_try[key] > 3:
                first_20.remove(key)
        else:
            self.congrat()
            
    
    def not_know(self):
        """Функция для кнопки "не знаю" показывает окно с правильным словом"""
        list_of_try[var_for_safe_key_from_func_play] -= 1
        try:
            know = QMessageBox()
            know.setWindowTitle('Запомни!')
            know.setText(var_for_safe_key_from_func_play)
            know.setStandardButtons(QMessageBox.Ok)
            know.exec_()
        except:
            return
          
    def check(self):
        """Проверяет слово введненное в английское поле на соответствие таковому в исходном словаре  и вызывает соответствующее окно"""
        wrong = QMessageBox()
        wrong.setWindowTitle('Результат')
        wrong.setText("Неправильно")
        wrong.setIconPixmap(QPixmap('icon.png'))
        wrong.setStandardButtons(QMessageBox.Ok)
        try:
            if self.rus_text_area.text()==word_dict[self.eng_text_area.text()]:
                correct = QMessageBox()
                correct.setWindowTitle('Результат')
                correct.setText("Правильно")
                correct.setIconPixmap(QPixmap('check_correct.png'))
                correct.setStandardButtons(QMessageBox.Ok)
                correct.buttonClicked.connect(self.play)
                correct.exec_()
            else:
                wrong.exec_()
        except(KeyError):
            wrong.exec_()

    def congrat(self):
        """Показывает окошко при превышении количества попыток"""
        congatulation = QMessageBox()
        congatulation.setWindowTitle('Поздравляем!')
        congatulation.setText("Ты выучил еще 20 слов!")
        congatulation.setIconPixmap(QPixmap('normalno.png'))
        congatulation.setStandardButtons(QMessageBox.Ok)
        congatulation.exec_()
        write_to_file(WORKING_FILE_NAME)

    def save_progress_clicked(self):
        write_to_file(WORKING_FILE_NAME)


def save_new_word_in_dict(word_eng,word_rus):
    """Сохраняет новую пару слов в промежуточный словарь"""
    if word_eng not in word_dict:
        word_dict[word_eng] = word_rus
        return("Ok")
    else: 
        return("This word is already in a dictionary")


def write_to_file(file_name):
    """Сохраняет промежуточный словарь и кол-во попыток в файл хранения"""
    file = open(file_name, 'w')
    for k,i in word_dict.items():
        file.write(k+":"+i+":"+str(list_of_try[k])+'\n')
    file.close


def read_a_file(file_name):
    """Достает из файла хранения данные и записывает их в промежуточный словарь"""
    file = open(file_name, 'r')
    pattern = r".+:.+:\d"
    for i in file.readlines():
        res = re.search(pattern,i)
        result = re.split(r':',res.group())
        word_dict[result[0]] = result[1]
        list_of_try[result[0]] = int(result[2])
    file.close()

def sort():
    """Возвращает 20 слов с наименьшим количеством попыток"""
    for k in range(5):
        for key in list_of_try.keys():
            value = list_of_try[key]
            if value == k:
                first_20.append(key)
            if len(first_20) == 20:
                break
        if len(first_20)==20:
            break
    return(first_20)
        
def nullify_attempt():
    """Обновляет количество попыток"""
    for key in list_of_try:
        list_of_try[key] = 0


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



