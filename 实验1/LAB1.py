from tkinter import *
from tkinter import messagebox
from tkinter.colorchooser import askcolor

#画布尺寸及背景色
win_width = 600
win_height = 400
bgcolor = '#708090'


class Application(Frame):

    def __init__(self, master=None):
        """初始化方法"""
        super().__init__(master)  # 调用父类的初始化方法
        self.x = 0
        self.y = 0
        self.fgcolor = 'yellow'
        self.lastdraw = 0
        self.start_flag = False
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        """创建画图区域"""
        self.drawpad = Canvas(self, width=win_width, height=win_height, bg=bgcolor)
        self.drawpad.pack()
        # 创建按钮
        self.btn_pen = Button(self, name='pen', text='画笔',font=('黑体', 30, 'bold'))
        self.btn_pen.pack(side='left', padx=25)
        self.btn_clear = Button(self, name='clear', text='清屏', font=('黑体', 30, 'bold'))
        self.btn_clear.pack(side='left', padx=25)
        self.btn_color = Button(self, name='color', text='颜色', font=('黑体', 30, 'bold'))
        self.btn_color.pack(side='right', padx=25)
        # 绑定事件
        self.btn_pen.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.btn_clear.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.btn_color.bind('<Button-1>', self.eventManager)  # 点击按钮事件
        self.master.bind('<KeyPress-r>', self.hotKey)  # 绑定快捷键
        self.master.bind('<KeyPress-g>', self.hotKey)  # 绑定快捷键
        self.master.bind('<KeyPress-b>', self.hotKey)  # 绑定快捷键
        self.master.bind('<KeyPress-y>', self.hotKey)  # 绑定快捷键
        self.drawpad.bind('<ButtonRelease-1>', self.stopDraw)  # 左键释放按钮

    def eventManager(self, event):
        name = event.widget.winfo_name()
        print(name)
        self.start_flag = True
        if name == 'pen':
            self.drawpad.bind('<B1-Motion>', self.mypen)
        elif name == 'clear':
            self.drawpad.delete('all')
        elif name == 'color':
            c = askcolor(color=self.fgcolor, title='请选择颜色')
            print(c)  # c的值 ((128.5, 255.99609375, 0.0), '#80ff00')
            self.fgcolor = c[1]

    def startDraw(self, event):
        self.drawpad.delete(self.lastdraw)
        if self.start_flag:
            self.start_flag = False
            self.x = event.x
            self.y = event.y

    def stopDraw(self, event):
        self.start_flag = True
        self.lastdraw = 0

    def mypen(self, event):
        self.startDraw(event)
        print('self.x=', self.x, ',self.y=', self.y)
        self.drawpad.create_line(self.x, self.y, event.x, event.y, fill=self.fgcolor)
        self.x = event.x
        self.y = event.y


    def hotKey(self, event):
        c = event.char
        if c == 'r':
            self.fgcolor = 'red'
        elif c == 'g':
            self.fgcolor = 'green'
        elif c == 'b':
            self.fgcolor = 'blue'
        elif c == 'y':
            self.fgcolor = 'yellow'


if __name__ == '__main__':
    root = Tk()
    root.title('画图窗口')
    root.geometry('600x500+200+200')
    app = Application(master=root)
    root.mainloop()
