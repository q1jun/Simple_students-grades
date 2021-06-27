import os

import xlrd
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import matplotlib
from matplotlib import pyplot as plt
from numpy import arange, sin, pi
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from xlutils.copy import copy

filePath = "students.xlsx"
filePath2 = "grade.xls"
username = []
password = []
loginFlag = 0
window = tk.Tk()


def get_image(filename, width, height):
    im = Image.open(filename).resize((width, height))
    return ImageTk.PhotoImage(im)


class Student:
    sId = []
    sClass = []
    sName = []
    gMath = []
    gChinese = []
    gEnglish = []
    """构造Student"""


def getUserInfo():
    user_data = xlrd.open_workbook(filePath)
    student_sheet = user_data.sheet_by_index(0)  # 第一个sheet表格
    """获取用户名密码"""
    for r in range(1, 4):
        username.append(student_sheet.cell_value(r, 0))
        password.append(student_sheet.cell_value(r, 1))
    for i in range(0, 3):
        print("Username: {0} Password: {1}".format(username[i], password[i]))


def getGrade(stu=Student()):
    student_data = xlrd.open_workbook(filePath2)
    student_sheet = student_data.sheet_by_index(0)  # 第一个sheet表格
    print(student_sheet.nrows)
    for row in range(1, student_sheet.nrows):
        stu.sId.append(student_sheet.cell_value(row, 0))
        stu.sClass.append(student_sheet.cell_value(row, 1))
        stu.sName.append(student_sheet.cell_value(row, 2))
        stu.gMath.append(student_sheet.cell_value(row, 3))
        stu.gChinese.append(student_sheet.cell_value(row, 4))
        stu.gEnglish.append(student_sheet.cell_value(row, 5))
    """打印获取的学生表"""
    for i in range(0, student_sheet.nrows - 1):
        print(
            "sId: {0} sClass: {1} sName :{2} gMath : {3} gChinese : {4} gEnglish : {5}"
                .format(stu.sId[i],
                        stu.sClass[i],
                        stu.sName[i],
                        stu.gMath[i],
                        stu.gChinese[i],
                        stu.gEnglish[i]))
    return stu


def loginWindow():
    window.title('登入界面')
    window.geometry('800x600+300+150')
    window.resizable(False, False)
    canvas = tk.Canvas(window, width=800, height=600)
    image_root = get_image("background.png", 800, 600)
    canvas.create_image(400, 300, image=image_root)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)
    l = tk.Label(window, text="Student Management System", fg="#06a099", font=("Sylfaen", 30))
    l2 = tk.Label(window, text='您好，请您先输入账号密码登入', fg="#06a099", font=('Arial', 12), width=30, height=2)
    l.grid(row=0, columnspan=4, padx=(160, 100), pady=(30, 0))
    # l.grid(row=1, columnspan=4, padx=(160, 100), pady=(30, 0))
    nameLabel = tk.Label(window, text="Enter your username", width=15, anchor='w',
                         font=("Sylfaen", 12)).grid(row=2, column=0, padx=(160, 0),
                                                    pady=(30, 0))
    passwordLabel = tk.Label(window, text="Enter your password", width=15, anchor='w',
                             font=("Sylfaen", 12)).grid(row=3, column=0, padx=(160, 0))
    username_text = tk.Entry(window, show=None, font=('Arial', 14))  # 显示成明文形式
    password_text = tk.Entry(window, show='*', font=('Arial', 14))  # 显示成密文形式
    username_text.insert(0, '请在此输入用户名')
    username_text.grid(row=2, column=1, padx=(0, 10), pady=(30, 0))
    password_text.grid(row=3, column=1, padx=(0, 10), pady=20)
    button = tk.Button(window, text="登 入", fg="#06a099", font=('Arial', 15), width=10,
                       command=lambda: login(username_text, password_text), takefocus=True)
    button.grid(row=4, columnspan=4, padx=(50, 10), pady=(10, 0))
    window.mainloop()


def login(username_text, password_text):
    """判断用户名密码"""
    uname = username_text.get()
    upwd = password_text.get()
    for i in range(0, 3):
        u1 = username[i]
        p1 = password[i]
        print("Username: {0} Password: {1}".format(u1, p1))
        print("uname: {0} upwd: {1}".format(uname, upwd))
        if (uname == u1) & (upwd == p1):
            """登入成功"""
            tk.messagebox.showinfo(title='登入成功', message='成功登入！欢迎，{0}。'.format(username[i]))
            window.destroy()
            """数据显示"""
            mainWindow()
            return
        else:
            if (uname == u1) & (upwd != p1):
                tk.messagebox.showinfo(title='登入失败', message='密码错误!'.format(username[i]))
            if (uname != u1) & (upwd == p1):
                tk.messagebox.showinfo(title='登入失败', message='用户名错误!'.format(username[i]))
    tk.messagebox.showinfo(title='登入失败', message='用户名和密码输入不正确！'.format(username[i]))


def showTable(secondWindow, stu=Student()):
    tree = ttk.Treeview(secondWindow)
    tree["columns"] = ("one", "two", "three", "four", "five", "six")
    tree.column("one", width=100)
    tree.column("two", width=100)
    tree.column("three", width=100)
    tree.column("four", width=100)
    tree.column("five", width=100)
    tree.column("six", width=100)
    tree.heading("one", text="Student No.")
    tree.heading("two", text="Class")
    tree.heading("three", text="Student Name")
    tree.heading("four", text="Math")
    tree.heading("five", text="Chinese")
    tree.heading("six", text="English")
    i = 0

    for row in range(0, len(stu.sId)):
        tree.insert('', i, text="Student " + str(stu.sId[row]),
                    values=(stu.sId[row],
                            stu.sClass[row],
                            stu.sName[row],
                            stu.gMath[row],
                            stu.gChinese[row],
                            stu.gEnglish[row]))
        i = i + 1
    """放置表格"""
    tree.pack(side='right', expand='yes', fill='both')
    return tree


def studentAppend(no, name, Class, math, Chinese, English):
    """将输入框的数据存入Student类中"""
    if no.get() == "" or name.get() == "" or Class.get() == "" or math.get() == "" or Chinese.get() == "" or English.get() == "":
        tk.messagebox.showinfo(title='添加失败', message='需要输入完整信息,请重新输入。')
        return -1
    for row in range(0, len(student_list.sId)):
        if no.get() == student_list.sId[row]:
            tk.messagebox.showinfo(title='添加失败', message='已存在学号{0},请重新输入。'.format(no.get()))
            return -1
    student_list.sId.append(no.get())
    student_list.sName.append(name.get())
    student_list.sClass.append(Class.get())
    student_list.gMath.append(math.get())
    student_list.gChinese.append(Chinese.get())
    student_list.gEnglish.append(English.get())
    tk.messagebox.showinfo(title='添加成功', message='学生{0}添加成功。'.format(name.get()))
    return student_list


def studentDelete(no, name, Class, math, Chinese, English):
    """将输入框的数据存入Student类中"""
    for row in range(0, len(student_list.sId)):
        if no.get() == student_list.sId[row]:
            tk.messagebox.showinfo(title='删除成功',
                                   message='已删除学号：{0}名字：{1}的信息，请刷新！'.format(no.get(), student_list.sName[row]))
            student_list.sId.pop(row)
            student_list.sName.pop(row)
            student_list.sClass.pop(row)
            student_list.gMath.pop(row)
            student_list.gChinese.pop(row)
            student_list.gEnglish.pop(row)
            return student_list
    tk.messagebox.showinfo(title='删除失败', message='未找到学号为{0}的学生信息。'.format(no.get()))
    return -1


def studentUpdate(no, name, Class, math, Chinese, English):
    """将输入框的数据存入Student类中"""
    if no.get() == "" or name.get() == "" or Class.get() == "" or math.get() == "" or Chinese.get() == "" or English.get() == "":
        tk.messagebox.showinfo(title='更新失败', message='需要输入完整信息,请重新输入。')
        return -1
    for row in range(0, len(student_list.sId)):
        if no.get() == student_list.sId[row]:
            tk.messagebox.showinfo(title='修改成功',
                                   message='已修改（更新）学号：{0}的信息，请刷新！'.format(no.get(), student_list.sName[row]))
            student_list.sId[row] = no.get()
            student_list.sName[row] = name.get()
            student_list.sClass[row] = Class.get()
            student_list.gMath[row] = math.get()
            student_list.gChinese[row] = Chinese.get()
            student_list.gEnglish[row] = English.get()
            return student_list
    tk.messagebox.showinfo(title='修改失败', message='未找到学号为{0}的学生信息。'.format(no.get()))
    return -1


def Refresh(secondWindow, tree):
    read = xlrd.open_workbook(filePath2)
    read_sheet = read.sheet_by_index(0)
    write = copy(read)
    write_sheet = write.get_sheet(0)
    for row in range(0, len(student_list.sId)):
        write_sheet.write(row + 1, 0, student_list.sId[row])
        write_sheet.write(row + 1, 1, student_list.sClass[row])
        write_sheet.write(row + 1, 2, student_list.sName[row])
        write_sheet.write(row + 1, 3, student_list.gMath[row])
        write_sheet.write(row + 1, 4, student_list.gChinese[row])
        write_sheet.write(row + 1, 5, student_list.gEnglish[row])
    write.save(filePath2)
    # tk.messagebox.showinfo(title='刷新成功', message='刷新成功，已保存至文件: {0}。'.format(filePath2))
    secondWindow.destroy()
    mainWindow()


def DataInfo():
    dataWindow = tk.Tk()
    dataWindow.title("显示数据信息")
    data = xlrd.open_workbook(filePath2)

    table = data.sheet_by_name("data")
    n = table.nrows
    scoreList = {}
    dMath = table.col_values(3)
    del dMath[0]
    scoreList['math'] = dMath

    dChinese = table.col_values(4)
    scoreList['chinese'] = dChinese
    del dChinese[0]
    dEnglish = list(table.col_values(5))
    scoreList['english'] = dEnglish
    del dEnglish[0]
    levelList = {}
    for k, v in scoreList.items():
        perfect = 0
        great = 0
        mid = 0
        unfail = 0
        fail = 0
        for i in v:
            if float(i) >= 90:
                perfect += 1
            elif float(i) >= 80 and float(i) <= 89:
                great += 1
            elif float(i) >= 70 and float(i) <= 79:
                mid += 1
            elif float(i) >= 60 and float(i) <= 69:
                unfail += 1
            else:
                fail += 1
        levelList[k] = [perfect, great, mid, unfail, fail]
    f = Figure(figsize=(5, 4), dpi=100)
    (ax1, ax2, ax3) = f.subplots(3)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    labels = '优秀', '良好', '中等', '及格', '不及格'
    sizes = levelList['math']
    explode = (0.1, 0, 0, 0, 0)  # only "explode" the 1nd slice (i.e. '优秀')

    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
    ax1.axis('equal')
    ax1.set_title("数学")

    sizes1 = levelList['chinese']
    ax2.pie(sizes1, labels=labels, autopct='%1.1f%%', shadow=True)
    ax2.axis('equal')
    ax2.set_title("语文")

    sizes2 = levelList['english']
    ax3.pie(sizes2, labels=labels, autopct='%1.1f%%', shadow=True)
    ax3.axis('equal')
    ax3.set_title("英语")
    f.legend(loc="upper right", fontsize=10, bbox_to_anchor=(1.1, 1.05), borderaxespad=0.3)
    # 绘制图形
    # 把绘制的图形显示到tkinter窗口上
    canvas = FigureCanvasTkAgg(f, master=dataWindow)
    canvas.draw()
    canvas.get_tk_widget().pack()
    tk.Label(dataWindow,
             text='学生总数：{0}人\n{6}：优秀：{1}人 良好：{2}人 中等：{3}人 及格：{4}人 不及格：{5}人 '.format(len(student_list.sId),
                                                                                    levelList['math'][0],
                                                                                    levelList['math'][1],
                                                                                    levelList['math'][2],
                                                                                    levelList['math'][3],
                                                                                    levelList['math'][4], '数学'),
             bg='pink').pack()
    tk.Label(dataWindow,
             text='{6}：优秀：{1}人 良好：{2}人 中等：{3}人 及格：{4}人 不及格：{5}人 '.format(len(student_list.sId),
                                                                         levelList['chinese'][0],
                                                                         levelList['chinese'][1],
                                                                         levelList['chinese'][2],
                                                                         levelList['chinese'][3],
                                                                         levelList['chinese'][4], '语文'),
             bg='pink').pack()
    tk.Label(dataWindow,
             text='{6}：优秀：{1}人 良好：{2}人 中等：{3}人 及格：{4}人 不及格：{5}人 '.format(len(student_list.sId),
                                                                         levelList['english'][0],
                                                                         levelList['english'][1],
                                                                         levelList['english'][2],
                                                                         levelList['english'][3],
                                                                         levelList['english'][4], '英语'),
             bg='pink').pack()
    dataWindow.mainloop()


def StudentSearch(no):
    for row in range(0, len(student_list.sId)):
        if no.get() == student_list.sId[row]:
            tk.messagebox.showinfo(title='查询成功',
                                   message='学号：{0}的信息:\n班级：{1} \t姓名：{2}\t数学成绩：{3}\t语文成绩：{4}\t英语成绩：{5}\t'.format(
                                       no.get(),
                                       student_list.sClass[
                                           row],
                                       student_list.sName[
                                           row],
                                       student_list.gMath[
                                           row],
                                       student_list.gChinese[
                                           row],
                                       student_list.gEnglish[
                                           row], ))
            return 1
    tk.messagebox.showinfo(title='查询失败', message='学号{0}不存在！！'.format(no.get()))


def mainWindow():
    secondWindow = tk.Tk()
    secondWindow.geometry('1400x800')
    secondWindow.title("Display results")
    menuBar(secondWindow)
    appLabel = tk.Label(secondWindow, text="Student Management System",
                        fg="#06a099", width=40)
    appLabel.config(font=("Sylfaen", 30))
    appLabel.pack(side='top', fill='x')
    tree = showTable(secondWindow)

    """左侧窗口(添加/修改/删除学生成绩)"""
    frameLeft = tk.Frame(secondWindow, relief='groove')
    frameLeft.pack(side='left', expand='no', fill='y')
    tk.Label(frameLeft, text='输入学生学号', bg='pink').grid(row=0, column=0, padx=(0, 20), pady=(0, 0))
    no = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    no.grid(row=0, column=1, padx=(0, 0),
            pady=(0, 0))
    no.insert(1, '例: 00001')
    tk.Label(frameLeft, text='输入学生姓名', bg='pink').grid(row=1, column=0, padx=(0, 20), pady=(0, 0))
    name = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    name.grid(row=1, column=1, padx=(0, 0), pady=(0, 0))
    name.insert(1, '张三')
    tk.Label(frameLeft, text='输入学生班级', bg='pink').grid(row=2, column=0, padx=(0, 20), pady=(0, 0))
    Class = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    Class.grid(row=2, column=1, padx=(0, 0), pady=(0, 0))
    Class.insert(1, '2020-1')
    tk.Label(frameLeft, text='输入数学成绩', bg='pink').grid(row=3, column=0, padx=(0, 20), pady=(0, 0))
    math = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    math.grid(row=3, column=1, padx=(0, 0), pady=(0, 0))
    math.insert(1, '0.0')
    tk.Label(frameLeft, text='输入语文成绩', bg='pink').grid(row=4, column=0, padx=(0, 20), pady=(0, 0))
    Chinese = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    Chinese.grid(row=4, column=1, padx=(0, 0), pady=(0, 0))
    Chinese.insert(1, '0.0')
    tk.Label(frameLeft, text='输入英语成绩', bg='pink').grid(row=5, column=0, padx=(0, 20), pady=(0, 0))
    English = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    English.grid(row=5, column=1, padx=(0, 0), pady=(0, 0))
    English.insert(1, '0.0')

    append = tk \
        .Button(frameLeft, text="Append增加",
                command=lambda: studentAppend(no, name, Class, math, Chinese, English), padx=20,
                pady=0, relief='flat', fg='pink',
                activeforeground='blue') \
        .grid(row=6, column=0, padx=(0, 0), pady=(20, 0))
    delete = tk. \
        Button(frameLeft, text="Delete删除", command=lambda: studentDelete(no, name, Class, math, Chinese, English),
               padx=20, pady=0, relief='flat', fg='pink',
               activeforeground='blue') \
        .grid(row=6, column=1, padx=(0, 0), pady=(20, 0))
    update = tk. \
        Button(frameLeft, text="Update修改", command=lambda: studentUpdate(no, name, Class, math, Chinese, English),
               padx=20, pady=0, relief='flat', fg='pink',
               activeforeground='blue') \
        .grid(row=6, column=2, padx=(0, 0), pady=(20, 0))
    tk.Label(frameLeft, text='输入所需查询的学号').grid(row=7, column=0, padx=(0, 20), pady=(20, 0))
    IDSearch = tk.Entry(frameLeft, highlightcolor='blue', state='normal', relief='flat')
    IDSearch.grid(row=7, column=1, padx=(0, 0), pady=(20, 0))
    Search = tk. \
        Button(frameLeft, text="查找学生", command=lambda: StudentSearch(IDSearch), padx=20, pady=0, fg='gray',
               activeforeground='blue') \
        .grid(row=7, column=2, padx=(0, 0), pady=(20, 0))
    refresh = tk. \
        Button(frameLeft, text="Refresh 刷新表格", command=lambda: Refresh(secondWindow, tree), padx=20, pady=0, fg='gray',
               activeforeground='blue') \
        .grid(row=8, column=1, padx=(0, 0), pady=(20, 0))
    DataInfomation = tk. \
        Button(frameLeft, text="显示数据信息", command=lambda: DataInfo(), padx=20, pady=0, fg='gray',
               activeforeground='blue') \
        .grid(row=9, column=1, padx=(0, 0), pady=(20, 0))
    secondWindow.mainloop()


def menuBar(secondWindow):
    menubar = tk.Menu(secondWindow)
    fileMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='设置', menu=fileMenu)
    fileMenu.add_command(label='Exit关闭程序', command=secondWindow.quit)
    secondWindow.config(menu=menubar)


if __name__ == '__main__':
    getUserInfo()
    student_list = getGrade(stu=Student())
    """登入界面"""
    loginWindow()
    """主界面测试"""
    # mainWindow()
