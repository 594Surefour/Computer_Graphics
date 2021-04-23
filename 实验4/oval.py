import wx
import time


class OVAL(wx.Frame):
    def __init__(self):
        #定义窗口的大小和位置
        super().__init__(None, title='中点画椭圆', size=(1000, 1000), pos=(30, 30))

        #输入参数
        self.Ox, self.Oy, self.a, self.b = map(
            int,
            input("请依次输入椭圆中心坐标和长短半轴：\n").split())
        #将事件与函数进行绑定
        self.Bind(wx.EVT_PAINT, self.On_Paint)

        #颜色
        self.color = '#0000FF'

    #绘图函数
    def DrawOval(self, Ox, Oy, a, b, dc):
        changed = 0 if a > b else 1  #用来判断取x或y为主方向
        a, b = max(a, b), min(a, b)
        point_list4 = []  #存储第四象限的点集
        A = a**2
        B = b**2
        x0 = int((A**2 / (A + B))**0.5)  #记录切线斜率为1的点横轴坐标
        x = 0
        y = b

        p = B + A * (0.25 - b)

        while x <= x0:
            if changed:
                point_list4.append((y, x))
            else:
                point_list4.append((x, y))
            if p < 0:
                p += B * (3 + 2 * x)
            else:
                p += B * (3 + 2 * x) + A * (2 - 2 * y)
                y -= 1
            x += 1

        p = B * (x + 0.5)**2 + A * (y - 1)**2 - A * B

        while y > 0:
            if changed:
                point_list4.append((y, x))
            else:
                point_list4.append((x, y))
            if p > 0:
                p += A * (3 - 2 * y)
            else:
                p += A * (3 - 2 * y) + B * (2 * x + 2)
                x += 1
            y -= 1
        point_list1 = [(x, -1 * y) for x, y in point_list4]  #第一象限的点
        point_list2 = [(-1 * x, -1 * y) for x, y in point_list4]  #第二象限的点
        point_list3 = [(-1 * x, y) for x, y in point_list4]  #第三象限的点
        #设置顺时针顺序进行绘画
        point_list1.sort()
        point_list2.sort()
        point_list3.sort(reverse=True)
        point_list4.sort(reverse=True)
        points_O = point_list1 + point_list4 + point_list3 + point_list2

        #平移坐标系
        points = [(x + Ox, y + Oy) for x, y in points_O]

        #这里利用time.sleep显示出动画效果
        #为了颜值设置了每隔STEP个点换一支画笔颜色

        STEP = 400
        for i, point in enumerate(points):
            if i % STEP == 0:
                dc.SetPen(wx.Pen(self.color))
            dc.DrawPoint(point)
            time.sleep(0.002)

    #定义绘图消息的接收
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        self.DrawOval(self.Ox, self.Oy, self.a, self.b, dc)


app = wx.App()  #app实例化

oval = OVAL()  #窗口类实例化

oval.Show()  #进行绘图

app.MainLoop()  #主循环
