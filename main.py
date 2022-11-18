from logging import exception
import time

import numpy as np
import threading
from numpy import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
QPushButton, QTableWidget, QWidget, QRadioButton, QTableWidgetItem)
from PyQt5.QtGui import QIcon

# - - - - - - - - - - - - - - LOGGING - - - - - - - - - - - - - -  # 


# - - - - - - - - - - - - - ARRAY FUNCTIONS - - - - - - - - - - - - - # 

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
        arr = random.random_integers(1, 25, arrays_table.columnCount())
    elif randomPeriodInput.isChecked():
        temp_arr = random.random_integers(1, 25, 4)
        for i in range(arrays_table.columnCount()):
            arr[i] = temp_arr[i % 4]

    for i in range(arrays_table.columnCount()):
        item = QTableWidgetItem(str(arr[i]))
        if randomInput.isChecked() or randomPeriodInput.isChecked():
            item.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            arrays_table.setItem(0, i, item)

    start = time.perf_counter()
    solve_threads(arr)
    t_lbl2.setText('Время многопоточной обработки: ' + str(time.perf_counter() - start))

    solve_first_task(arr)
    solve_second_task(arr)
    solve_third_task(arr)



# - - - - - - - - - - - -  TABLE EDITING PERMISSIONS - - - - - - - - - - - - # 

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



# - - - - - - - - - - - - - - THREADING - - - - - - - - - - - - - -  # 

def solve_threads(arr):
    global thread_result_array
    thread_result_array = []

    thread_list = []
    numpy_array = np.array_split(arr, 4)
    for i in range(4):
        thread_list.append(threading.Thread(target = thread_worker, args = (numpy_array[i], i)))
        thread_list[i].start()

    for i in range(len(thread_list)):
        thread_list[i].join()
    print(thread_result_array)


def thread_worker(arr, i):
    for i in range(len(arr)):
        if arr[i] % 3 == 0 and arr[i] % 5 == 0 and arr[i] != 0:
            thread_result_array.append(i + 1)


# - - - - - - - - - - - - - SOLVING TASKS - - - - - - - - - - - - - # 

def solve_first_task(arr):
    start = time.perf_counter()
    
    resultArray = []
    for i in range(len(arr)):
        if arr[i] % 3 == 0 and arr[i] % 5 == 0 and arr[i] != 0:
            resultArray.append(i + 1)

    t_lbl1.setText('Время однопоточной обработки: ' + str(time.perf_counter() - start))

    if len(resultArray) == 0:
        arrays_table.setItem(1, 0, QTableWidgetItem("None"))
        for i in range(arrays_table.columnCount() - 1):
            arrays_table.setItem(1, i + 1, QTableWidgetItem(""))
    else:
        for i in range(len(resultArray)):
            item2 = QTableWidgetItem(str(resultArray[i]))
            item2.setFlags( Qt.ItemIsSelectable | Qt.ItemIsEnabled )
            arrays_table.setItem(1, i, item2)

        for i in range(arrays_table.columnCount() - len(resultArray)):
            arrays_table.setItem(1, i + len(resultArray), QTableWidgetItem(""))
 

def solve_second_task(arr):
    result = 0
    for i in range(len(arr)):
        if arr[i] < 10:
            result += arr[i]
    task2.setText('Сумма положительных элементов, значения которых меньше 10: ' + str(result))


def solve_third_task(arr):
    result = False
    try:
        num = int(num_edit.text())
    except:
        exception('Введено не число')
        task3.setText('Есть ли пара соседних элементов с суммой, равной заданному числу? Число не задано')
        return

    for i in range(len(arr) - 1):
        if arr[i] + arr[i + 1] == num:
            result = True
    task3.setText('Есть ли пара соседних элементов с суммой, равной заданному числу? ' + ''.join("Да" if result == True else "Нет"))


# - - - - - - - - - - - - - - - MAIN - - - - - - - - - - - - - - - # 

app = QApplication([])
app.setApplicationName("Lab02 (3rd year)")
app.setWindowIcon(QIcon('C:\\Users\\asus\\Desktop\\Projects\\SUAI\\Labs\\3-ий курс\\C++\\Lab02 Python\\plex.jpg'))
window = QWidget()
window.setGeometry(100, 100, 900, 450)
window.show()

grid1 = QGridLayout()
window.setLayout(grid1)

lbl = QLabel('Введите длину массива:')
grid1.addWidget(lbl, 0, 0)
len_edit = QLineEdit()
grid1.addWidget(len_edit, 1, 0)

num_lbl = QLabel('Введите число:')
grid1.addWidget(num_lbl, 2, 0)
num_edit = QLineEdit()
grid1.addWidget(num_edit, 3, 0)


btn_resize = QPushButton('Ввод')
btn_resize.clicked.connect(resize)
grid1.addWidget(btn_resize, 1, 1)

btn_fill = QPushButton('Заполнить')
btn_fill.clicked.connect(fill)
grid1.addWidget(btn_fill, 4, 3)

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
grid1.addWidget(arrays_table, 5, 0, 1, 4)


t_lbl1 = QLabel('Время однопоточной обработки: ')
grid1.addWidget(t_lbl1, 6, 0)

t_lbl2 = QLabel('Время многопоточной обработки: ')
grid1.addWidget(t_lbl2, 6, 2)

task2 = QLabel('Сумма положительных элементов, значения которых меньше 10: ')
grid1.addWidget(task2, 7, 0)

task3 = QLabel('Есть ли пара соседних элементов с суммой, равной заданному числу? ')
grid1.addWidget(task3, 8, 0)

table_dis()

app.exec_()
