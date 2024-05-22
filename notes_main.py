#начни тут создавать приложение с умными заметками

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton, QButtonGroup, QLineEdit, QTextEdit, QListWidget, QInputDialog
import json

app = QApplication([])
mw = QWidget()



put1 = QPushButton('Создать заметку')
put2 = QPushButton('Удалить заметку')
put3 = QPushButton('Сохранить заметку')
put4 = QPushButton('Добавить к заметке')
put5 = QPushButton('Открепить от заметки')
put6 = QPushButton('Искать заметки по тегу')

nad1 = QLabel('Список заметок')
nad2 = QLabel('Список тегов')

pol1 = QListWidget()
pol2 = QListWidget()

polbg = QTextEdit()

le = QLineEdit()

gl_lb = QHBoxLayout()
mwlf = QVBoxLayout()
mwlf.addWidget(polbg)

mwrg = QVBoxLayout()
mwrg.addWidget(nad1)
mwrg.addWidget(pol1)
lb1 = QHBoxLayout()
lb1.addWidget(put1)
lb1.addWidget(put2)
mwrg.addLayout(lb1)

mwrg.addWidget(put3)

mwrg.addWidget(nad2)
mwrg.addWidget(pol2)

lb2 = QHBoxLayout()
lb2.addWidget(le)
mwrg.addLayout(lb2)

lb3 = QHBoxLayout()
lb3.addWidget(put4)
lb3.addWidget(put5)
mwrg.addLayout(lb3)

lb4 = QHBoxLayout()
lb4.addWidget(put6)
mwrg.addLayout(lb4)

gl_lb.addLayout(mwrg)
gl_lb.addLayout(mwlf)



with open('f.json', 'r') as file:
    notes = json.load(file)

def show_note():
    name = pol1.selectedItems()[0].text()
    polbg.setText(notes[name]['текст'])
    pol2.clear()
    pol2.addItems(notes[name]['теги'])

pol1.itemClicked.connect(show_note)
pol1.addItems(notes)



def add_note():
    note1, ok = QInputDialog.getText(
    mw, 'Добавить заметку', 'Название заметки:'
)
    if ok == True:
        notes[note1]=  {'текст' : '', 'теги' : []}
        pol1.addItem(note1)
put1.clicked.connect(add_note)

def del_note():
    note1 = pol1.selectedItems()[0].text()
    del notes[note1]
    with open('f.json', 'w') as file:
        json.dump(notes, file)
    pol1.clear()
    pol2.clear()
    polbg.clear()
    pol1.addItems(notes)
put2.clicked.connect(del_note)

def save_note():
    if pol1.selectedItems():
        note1 = pol1.selectedItems()[0].text()
        notes[note1]['текст']= polbg.toPlainText()
        with open('f.json', 'w') as file:
            json.dump(notes, file)
put3.clicked.connect(save_note)

def add_tag():
    if pol1.selectedItems():
        teg1 = le.text()
        pol2.addItem(teg1)
        note1 = pol1.selectedItems()[0].text()
        notes[note1]['теги'].append(teg1)
        le.clear()
        with open('f.json', 'w') as file:
            json.dump(notes, file)
put4.clicked.connect(add_tag)

def del_tag():
    if pol1.selectedItems():
        note1 = pol1.selectedItems()[0].text()
        teg1 = pol2.selectedItems()[0].text()
        notes[note1]['теги'].remove(teg1)
        with open('f.json', 'w') as file:
            json.dump(notes, file)
        pol2.clear()
        pol2.addItems(notes[note1]['теги'])
put5.clicked.connect(del_tag)

def search_teg():
    teg1 = le.text()
    if put6.text() =='Искать заметки по тегу' and teg1:
        tegs_ft = {}
        for note in notes:
            if teg1 in notes[note]['теги']:
                tegs_ft[note] = notes[note]
        put6.setText('Сбросить поиск')
        pol1.clear()
        pol2.clear()
        pol1.addItems(tegs_ft)
    elif put6.text() == 'Сбросить поиск':
        pol1.clear()
        pol2.clear()
        pol1.addItems(notes)
        put6.setText('Искать заметки по тегу')
        le.clear()
put6.clicked.connect(search_teg)

                


mw.setLayout(gl_lb)
mw.show()
app.exec_()