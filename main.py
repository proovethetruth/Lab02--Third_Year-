from logging import exception
import time
from threading import Thread
from threading import Lock

import threading
from numpy import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
QPushButton, QTableWidget, QWidget, QRadioButton, QTableWidgetItem)
from PyQt5.QtGui import QIcon

# - - - - - - - - - - - - - - LOGGING - - - - - - - - - - - - - -  # 



# - - - - - - - - - - - - - - THREADING - - - - - - - - - - - - - -  # 

def threading_gen(arr):
    global arr2
    arr2 = arr
    start = time.perf_counter()
    th1 = threading.Thread(target = first_thread, args = arr2)
    th2 = threading.Thread(target = second_thread, args = arr2)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    th3 = threading.Thread(target = third_thread, args = arr2)
    th3.start()
    th3.join()
    t_lbl2.setText('Время многопоточной обработки:' + str(time.perf_counter() - start))
    return arr2


def first_thread(arr):
    lock = Lock()
    tmp = arr
    
    for i in range(len(arr)):
        if i > 1 and i < 12:
            tmp[i] = -(tmp[i]**2)
        else:
            tmp[i] = tmp[i] - 1
    lock.acquire()
    arr2 = tmp
    lock.release()

def second_thread(arr):
    tmp = arr
    maxim = -9999
    max_i = 0
    for i in range(len(arr)):
        if i > 1 and i < 12:
            if -(arr[i]**2) > maxim:
                maxim = -(arr[i]**2)
                max_i = i
        else:
            if (arr[i] - 1) > maxim:
                maxim = arr[i] - 1
                max_i = i
    arr2[max_i] = maxim

def third_thread(arr):
    max1 = max(arr)
    arr[arr.index(max1)] = -max1
    if arr.index(max(arr)) + 1 < arr.index(min(arr)):
        for i in range(arr.index(max(arr)) + 1, arr.index(min(arr))):
            arr[i] = 0
    else:
        for i in range(arr.index(min(arr)) + 1, arr.index(max(arr))):
            arr[i] = 0
    return arr



# - - - - - - - - - - - - - ARRAY FUNCTIONS - - - - - - - - - - - - - # 

def array_gen(arr):
    start = time.perf_counter()
    resultArray = []
    for i in range(len(arr)):
        if arr[i] % 3 == 0 and arr[i] % 5 == 0 and arr[i] != 0:
            resultArray.append(i + 1)

    t_lbl1.setText('Время однопоточной обработки:' + str(time.perf_counter() - start))
    return resultArray


def get_arr():
    arr = []
    try:
        arr = [ int(arrays_table.item(0, column).text()) for column in range(arrays_table.columnCount()) if int(arrays_table.item(0, column).text())]
    except ValueError:
        print("Неверный ввод")
    if (len (arr) == 0):
        return [0 for i in range (arrays_table.columnCount())]
    else:
       return arr

def resize():
    try:
        int(len_edit.text())
        arrays_table.setColumnCount(int(len_edit.text()))
    except:
        exception('Введено не число')

def fill():
    arr = [0 for i in range (arrays_table.columnCount())]
    if manualInput.isChecked():
        arr = get_arr()
    elif randomInput.isChecked():
        arr = random.random_integers(1, 100, arrays_table.columnCount())
    elif randomPeriodInput.isChecked():
        temp_arr = random.random_integers(1, 100, 4)
        for i in range(arrays_table.columnCount()):
            arr[i] = temp_arr[i % 4]

    for i in range(arrays_table.columnCount()):
        item = QTableWidgetItem(str(arr[i]))
        if randomInput.isChecked() or randomPeriodInput.isChecked():
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            arrays_table.setItem(0, i, item)

    resultArray = array_gen(arr)
    # threading_gen(arr)

    if len(resultArray) == 0:
        arrays_table.setItem(1, 0, QTableWidgetItem("None"))
    else:
        for i in range(len(resultArray)):
            item2 = QTableWidgetItem(str(resultArray[i]))
            item2.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            arrays_table.setItem(1, i, item2)

        for i in range(arrays_table.columnCount() - len(resultArray)):
            arrays_table.setItem(1, i + len(resultArray), QTableWidgetItem(""))

def table_dis():
    for i in range(arrays_table.columnCount()):
        item = QTableWidgetItem()
        item2 = QTableWidgetItem()
        item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        item2.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        arrays_table.setItem(0, i, item)
        arrays_table.setItem(1, i, item2)


def table_en():
    for i in range(arrays_table.columnCount()):
        item = QTableWidgetItem()
        item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
        arrays_table.setItem(0, i, QTableWidgetItem('0'))
        arrays_table.setItem(1, i, item)



# - - - - - - - - - - - - - - - MAIN - - - - - - - - - - - - - - - # 

app = QApplication([])
app.setApplicationName("Lab02 (3rd year)")
app.setWindowIcon(QIcon('C:\\Users\\asus\\Desktop\\Projects\\SUAI\\Labs\\3-ий курс\\C++\\Lab02 Python\\plex.jpg'))
window = QWidget()
window.setGeometry(100, 100, 900, 320)
window.show()

grid1 = QGridLayout()
window.setLayout(grid1)

lbl = QLabel('Введите длину массива:')
grid1.addWidget(lbl, 0, 0)
len_edit = QLineEdit()
grid1.addWidget(len_edit, 1, 0)
btn_resize = QPushButton('Ввод')
btn_resize.clicked.connect(resize)
grid1.addWidget(btn_resize, 1, 1)


btn_fill = QPushButton('Заполнить')
btn_fill.clicked.connect(fill)
grid1.addWidget(btn_fill, 2, 0)

lbl2 = QLabel('Способ заполнения массива:')
grid1.addWidget(lbl2, 0, 3)

manualInput = QRadioButton('Заполнение вручную')
manualInput.toggled.connect(table_en)
grid1.addWidget(manualInput, 1, 3)

randomInput = QRadioButton('Заполнение случаными числами')
randomInput.toggled.connect(table_dis)
grid1.addWidget(randomInput, 2, 3)

randomPeriodInput = QRadioButton('Заполнение случаными числами с периодом 4')
randomPeriodInput.toggled.connect(table_dis)
grid1.addWidget(randomPeriodInput, 3, 3)

arrays_table = QTableWidget(2, 10)
arrays_table.setVerticalHeaderLabels(['Исходный массив', 'Полученый массив'])


for i in range(arrays_table.columnCount()):
    item = QTableWidgetItem()
    item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
    arrays_table.setItem(1, i, item)
grid1.addWidget(arrays_table, 4, 0, 1, 4)


t_lbl1 = QLabel('Время однопоточной обработки:')
grid1.addWidget(t_lbl1, 5, 0)

t_lbl2 = QLabel('Время многопоточной обработки:')
grid1.addWidget(t_lbl2, 5, 2)

t_lbl2 = QLabel('Сумма положительных элементов, значения которых меньше 10:')
grid1.addWidget(t_lbl2, 6, 0)

t_lbl2 = QLabel('Есть ли пара соседних элементов с суммой, равной заданному числу?')
grid1.addWidget(t_lbl2, 7, 0)

table_dis()

app.exec_()
