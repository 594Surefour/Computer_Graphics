# -*- coding: utf-8 -*-
import wx
import time

class CIRCLE(wx.Frame):
    def __init__(self):
        #定义窗口的大小和位置
        super().__init__(None, title='中点画圆法', size=(1000, 1000), pos=(30, 30))

        #输入参数
        self.x, self.y, self.r = map(int, input("请依次输入圆心坐标和半径：\n").split())
        #将事件与函数进行绑定
        self.Bind(wx.EVT_PAINT, self.On_Paint)

        #颜色表
        self.color = '#0000FF'

    #绘图函数
    def DrawCircle(self, a, b, R, dc):
        L4=[] #存储第四象限的数组(对于窗口的坐标系而言是第一象限)
        x, y, p = 0, R, 1 - R
        #将p设置为1-R能够避免浮点运算，而且其绘图的拟合程度较好
        while (x < y):
            if p < 0:
                p += (2 * x + 3)
            else:
                p += (2 * x - 2 * y + 5)
                y -= 1
            x+=1
            L4.append((x,y)) #八分之一点的集合
            L4.append((y,x)) #将点做关于y=-x(对于窗口坐标系而言是y=x)的对称
            #L4所得点的集合是四分之一圆弧的点

        L3 = [(-1*e[0],e[1])for e in L4] #第三象限
        L2 = [(-1 * e[0], -1*e[1]) for e in L4] #第二象限
        L1 = [(e[0], -1*e[1]) for e in L4] #第一象限

        #为绘图时按照顺时针绘画，将各个象限进行排序
        L1.sort()
        L2.sort()
        L3.sort(reverse=True)
        L4.sort(reverse=True)

        #按照一四三二的象限顺序生成总的点集
        p_points = [(e[0]+a,e[1]+b)for e in L1+L4+L3+L2]
        points = list(set(p_points))
        points.sort(key=p_points.index)

        #这里利用time.sleep显示出动画效果
        #为了颜值设置了每隔STEP个点换一支画笔颜色
        STEP = 400
        for i,point in enumerate(points):
            if i % STEP == 0:
                dc.SetPen(wx.Pen(self.color))
            dc.DrawPoint(point)
            time.sleep(0.003)

    #定义绘图消息的接收
    def On_Paint(self, event):
        dc = wx.PaintDC(self)
        a, b, R = self.x, self.y, self.r
        self.DrawCircle(a, b, R, dc)

app = wx.App() #app实例化

circle = CIRCLE() #窗口类实例化

circle.Show() #进行绘图

app.MainLoop() #主循环
