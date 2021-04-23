import wx

TOP = 8  # 1000
BOTTOM = 4  # 0100
RIGHT = 2  # 0010
LEFT = 1  # 0001
INSIDE = 0  # 0000


class Crop(wx.Frame):
    def __init__(self):
        super().__init__(None, title='线段裁剪算法', size=(800, 800))
        self.Center()

        # 绑定用户交互的函数
        self.Bind(wx.EVT_LEFT_DOWN, self.left_down)
        self.Bind(wx.EVT_LEFT_UP, self.left_up)
        self.Bind(wx.EVT_MOTION, self.mouse_move)

        # 设置绘制的设备
        self.dc1 = wx.ClientDC(self)
        self.dc1.SetBackground(wx.Brush(self.GetBackgroundColour()))
        self.dc2 = wx.ClientDC(self)
        self.dc2.SetBackground(wx.Brush(self.GetBackgroundColour()))
        # 设置绘制的画笔和画刷颜色
        brush_color = '#000000'
        brush = wx.Brush(brush_color, wx.TRANSPARENT)
        pen_color = '#ff0000'
        pen = wx.Pen(pen_color, width=1, style=wx.PENSTYLE_LONG_DASH)
        self.dc2.SetBrush(brush)
        self.dc2.SetPen(pen)

        self.flag = False
        self.line_posx0 = 0  # 直线起点坐标的x值
        self.line_posy0 = 0  # 直线终点坐标的y值
        self.line_posx1 = 0  # 直线终点坐标的x值
        self.line_posy1 = 0  # 直线终点坐标的y值
        self.rec_posx0 = 0  # 矩形起点坐标的x值
        self.rec_posy0 = 0  # 矩形起点坐标的y值
        self.rec_posx1 = 0  # 矩形终点坐标的x值
        self.rec_posy1 = 0  # 矩形终点坐标的y值

    def left_down(self, event):
        # 获取绘制直线或矩形的起始坐标值
        pos = event.GetPosition()
        if self.flag:
            self.rec_posx0, self.rec_posy0 = pos
        else:
            self.line_posx0, self.line_posy0 = pos

    def mouse_move(self, event):
        # 动态绘制直线或矩形的函数
        if self.flag:
            # 绘制矩形
            if event.Dragging() and event.LeftIsDown():
                self.dc2.Clear()
                self.dc1.DrawLine(self.line_posx0, self.line_posy0,
                                  self.line_posx1, self.line_posy1)

                self.rec_posx1, self.rec_posy1 = event.GetPosition()
                # 计算矩形的宽度和高度并绘制
                width = self.rec_posx1 - self.rec_posx0
                height = self.rec_posy1 - self.rec_posy0
                self.dc2.DrawRectangle(self.rec_posx0, self.rec_posy0, width,
                                       height)
        else:
            # 绘制直线
            if event.Dragging() and event.LeftIsDown():
                self.dc1.Clear()
                self.line_posx1, self.line_posy1 = event.GetPosition()
                self.dc1.DrawLine(self.line_posx0, self.line_posy0,
                                  self.line_posx1, self.line_posy1)

    def left_up(self, event):
        
        
        if self.flag:
            # 确定矩形区域之后
            # 计算裁剪之后的线段端点
            accept,linex0,liney0,linex1,liney1 = self.compute(self.line_posx0,self.line_posy0,self.line_posx1,self.line_posy1)
            self.dc1.Clear()
            width = self.rec_posx1 - self.rec_posx0
            height = self.rec_posy1 - self.rec_posy0
            self.dc2.DrawRectangle(self.rec_posx0, self.rec_posy0, width,
                                       height)
            if accept:
                self.dc1.DrawLine(linex0,liney0,linex1,liney1)
        # 每次鼠标左键up之后切换绘制的形状
        self.flag = not self.flag

    def Code(self, x, y):
        """
        x,y 指目标点的坐标
        x0,y0 指裁剪的矩形区域的起始坐标
        x1,y1 指裁剪的矩形区域的结束坐标
        """
        # 先计算矩形的区域的边界
        x_min, x_max = min(self.rec_posx0,
                           self.rec_posx1), max(self.rec_posx0, self.rec_posx1)
        y_min, y_max = min(self.rec_posy0,
                           self.rec_posy1), max(self.rec_posy0, self.rec_posy1)
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP

        return code

    # 计算是否进行裁剪，并返回裁剪后线段的端点坐标
    def compute(self, x0, y0, x1, y1):
        """
        x0,y0指线段起始点的坐标
        x1,y1指线段终止点的坐标
        """
        x_min, x_max = min(self.rec_posx0,
                           self.rec_posx1), max(self.rec_posx0, self.rec_posx1)
        y_min, y_max = min(self.rec_posy0,
                           self.rec_posy1), max(self.rec_posy0, self.rec_posy1)
        # 生成两个坐标的区域码
        code0 = self.Code(x0, y0)
        code1 = self.Code(x1, y1)
        accept = False  # 表示线段是否需要裁剪
        while True:
            if not (code0 | code1): # 线段在裁剪区域内部
                accept = True
                break
            elif code0 & code1: # 线段在裁剪区域外部
                break
            else:
                outcode = code0 if code0 else code1  # 选取在区域外部的点进行运算

                if outcode & TOP:
                    x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                    y = y_max
                elif outcode & BOTTOM:
                    x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                    y = y_min
                elif outcode & RIGHT:
                    y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                    x = x_max
                elif outcode & LEFT:
                    y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                    x = x_min

                if outcode == code0:
                    x0 = x
                    y0 = y
                    code0 = self.Code(x0,y0)
                else:
                    x1 = x
                    y1 = y
                    code1 = self.Code(x1,y1)
        return accept,int(x0),int(y0),int(x1),int(y1)


def main():
    app = wx.App() # 实例化wx对象
    crop = Crop() # 实例化自定义类对象
    crop.Show() # 生成界面
    app.MainLoop() # wx主循环


if __name__ == '__main__':
    main()
