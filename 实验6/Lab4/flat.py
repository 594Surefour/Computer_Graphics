import wx
import numpy as np
import math
import random
import Oval


class Trans2D(wx.Frame):
    def __init__(self):
        super().__init__(None, title="二维图像变换", size=(800, 800))
        self.Center()
        self.initmenu()
        # 设置绘制的设备
        self.dc = wx.ClientDC(self)
        self.dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        # 随机选择画笔颜色
    def initmenu(self):
        menubar = wx.MenuBar()  # 新建菜单bar

        # 变换选择的菜单
        trans_menu = wx.Menu()
        trans_menu.AppendRadioItem(101, '&平移\tAlt+P')
        trans_menu.AppendRadioItem(102, '&旋转\tAlt+S')
        trans_menu.AppendRadioItem(103, '&放缩\tAlt+Z')
        menubar.Append(trans_menu, '变换(&T)')

        #图形选择的菜单
        graph_menu = wx.Menu()
        graph_menu.AppendRadioItem(201, '&直线\tAlt+L')
        graph_menu.AppendRadioItem(202, '&椭圆\tAlt+O')
        graph_menu.AppendRadioItem(203, '&填充图形\tAlt+F')
        menubar.Append(graph_menu, '图形(&G)')

        # 绘制图形的菜单
        paint_menu = wx.Menu()
        paint_menu.Append(301, '&绘制\tAlt+P')
        menubar.Append(paint_menu, '操作(&O)')

        # 个人信息菜单
        inform_menu = wx.Menu()
        menubar.Append(inform_menu, '关于(&I)')

        # 显示菜单
        self.SetMenuBar(menubar)

        # 绑定自己的绘制函数
        self.Bind(wx.EVT_MENU, self.MyPaint, id=301)

    def MyPaint(self, event):
        self.dc.Clear()
        linecolors = [
            '#671392', '#00FF00', '#FF00FF', '#ABCDEF', '#FEDCBA', '#0F0F0F',
            '#FFF000'
        ]
        # 设置画笔粗细
        width = 2
        # 设置画笔颜色
        color = random.sample(linecolors, 1)[0]
        pen = wx.Pen(color, width=width, style=wx.PENSTYLE_SOLID)
        self.dc.SetPen(pen)
        # 判断各个单选菜单的状态
        # 是否平移
        pan = self.GetMenuBar().FindItemById(101).IsChecked()
        # 是否旋转
        spin = self.GetMenuBar().FindItemById(102).IsChecked()
        # 是否放缩
        zoom = self.GetMenuBar().FindItemById(103).IsChecked()

        # 对于直线进行操作
        line = self.GetMenuBar().FindItemById(201).IsChecked()
        # 对于椭圆进行操作
        oval = self.GetMenuBar().FindItemById(202).IsChecked()
        # 对于封闭图形进行操作
        graph = self.GetMenuBar().FindItemById(203).IsChecked()
        sita = 0
        yzoom = 1
        # 输入平移的参数
        if pan:
            dlg = wx.TextEntryDialog(self, '请分别输入平移x,y坐标', '平移参数')
            if dlg.ShowModal() == wx.ID_OK:
                x0, y0 = map(int, dlg.GetValue().split())
            parameter = 'T'
        # 输入旋转的参数
        if spin:
            dlg = wx.TextEntryDialog(self, '请分别输入旋转中心x,y坐标和旋转角度', '旋转参数')
            if dlg.ShowModal() == wx.ID_OK:
                x0, y0, sita = map(float, dlg.GetValue().split())
            parameter = 'R'

        # 输入放缩的参数
        if zoom:
            dlg = wx.TextEntryDialog(self, '请分别输入放缩中心x,y坐标和x,y的放缩倍数', '旋转参数')
            if dlg.ShowModal() == wx.ID_OK:
                x0, y0, sita, yzoom = map(float, dlg.GetValue().split())
            parameter = 'S'

        # test
        if line:
            # 获取直线的起点和终点
            dlg_graph = wx.TextEntryDialog(self, '请输入直线的起始坐标', '坐标参数')
            # 获取直线端点坐标
            if dlg_graph.ShowModal() == wx.ID_OK:
                lx0, ly0, lx1, ly1 = map(int, dlg_graph.GetValue().split())
            # 绘制初始直线
            self.dc.DrawLine((lx0, ly0), (lx1, ly1))
            # 修改画笔颜色
            color = random.sample(linecolors, 1)[0]
            pen = wx.Pen(color, width=width, style=wx.PENSTYLE_SOLID)
            self.dc.SetPen(pen)
            # 计算变换后顶点坐标
            tx0, ty0 = self.TransFunction(lx0, ly0, x0, y0, parameter, sita,
                                          yzoom)
            tx1, ty1 = self.TransFunction(lx1, ly1, x0, y0, parameter, sita,
                                          yzoom)
            #绘制变换后的直线
            self.dc.DrawLine((tx0, ty0), (tx1, ty1))

        if oval:
            # 获取椭圆的参数
            dlg_graph = wx.TextEntryDialog(self, '请输入椭圆的中心坐标和长短轴', '坐标参数')
            # 获取椭圆的左上角和右上角的点坐标
            if dlg_graph.ShowModal() == wx.ID_OK:
                Ox, Oy, a, b = map(int, dlg_graph.GetValue().split())
            ovalpoints = Oval.Ovalpoints(Ox, Oy, a, b)
            self.dc.DrawPointList(ovalpoints)
            tran_points = []
            for point in ovalpoints:
                ox, oy = point
                tx, ty = self.TransFunction(ox, oy, x0, y0, parameter, sita,
                                            yzoom)
                tran_points.append((tx, ty))
            # 修改画笔颜色
            color = random.sample(linecolors, 1)[0]
            pen = wx.Pen(color, width=width, style=wx.PENSTYLE_SOLID)
            self.dc.SetPen(pen)
            self.dc.DrawPointList(tran_points)

        if graph:
            # 自定义菱形顶点坐标
            lx0, ly0 = 400, 10
            lx1, ly1 = 475, 110
            lx2, ly2 = 400, 210
            lx3, ly3 = 325, 110
            pointlist = [(lx0, ly0), (lx1, ly1), (lx2, ly2), (lx3, ly3)]

            tranlist = []  # 存储变换后的顶点坐标

            # 修改画刷的颜色
            color = random.sample(linecolors, 1)[0]
            brush = wx.Brush(color)
            self.dc.SetBrush(brush)

            # 绘制原始图形
            self.dc.DrawPolygon(pointlist)
            # 计算每个点变化后的坐标
            for point in pointlist:
                x, y = point
                tx, ty = self.TransFunction(x, y, x0, y0, parameter, sita,
                                            yzoom)
                tranlist.append((tx, ty))
            # 修改画刷的颜色
            color = random.sample(linecolors, 1)[0]
            brush = wx.Brush(color)
            self.dc.SetBrush(brush)
            # 绘制变换后的菱形
            self.dc.DrawPolygon(tranlist)

    def TransFunction(self,
                      x,
                      y,
                      x0,
                      y0,
                      para='T',
                      sita=0,
                      yzoom=1):  # 定义 对点进行变化的函数

        if para == 'T':  # 平移矩阵
            matlist = [[1, 0, x0], [0, 1, y0], [0, 0, 1]]
            mat = np.array(matlist)  # 转化为ndarry格式
            point = np.array([[x], [y], [1]])  # 将点转换为齐次坐标
            trans_point = mat.dot(point).tolist()
            trans_x = int(trans_point[0][0])
            trans_y = int(trans_point[1][0])
        if para == 'R':  # 旋转矩阵，需要通过角度换成弧度
            pi = math.pi
            sita = -sita / 180 * pi
            cos = math.cos(sita)
            sin = math.sin(sita)
            matlist = [[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]]
            mat = np.array(matlist)  # 转化为ndarry格式
            point = np.array([[x - x0], [y - y0], [1]])  # 将点转换为齐次坐标
            trans_point = mat.dot(point).tolist()
            trans_x = int(trans_point[0][0] + x0)
            trans_y = int(trans_point[1][0] + y0)
        if para == 'S':  # 放缩矩阵
            matlist = [[sita, 0, 0], [0, yzoom, 0], [0, 0, 1]]
            mat = np.array(matlist)  # 转化为ndarry格式
            point = np.array([[x - x0], [y - y0], [1]])  # 将点转换为齐次坐标
            trans_point = mat.dot(point).tolist()
            trans_x = int(trans_point[0][0] + x0)
            trans_y = int(trans_point[1][0] + y0)
        return trans_x, trans_y


def main():
    app = wx.App()
    trans2d = Trans2D()
    trans2d.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()