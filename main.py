import wx
import wx.grid
from mydb import Sql_operation
from tkinter import filedialog
import tkinter
import os
import shutil


# 创建登录界面类
class UserLogin(wx.Frame):
    '''
    登录界面
    '''

    # 初始化登录界面
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(UserLogin, self).__init__(*args, **kw)
        # 设置窗口屏幕居中
        self.flag = 0
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        # self.pnl.SetBackgroundColour("#6F6F6F")

        # 调用登录界面函数
        self.LoginInterface()

    def LoginInterface(self):
        pic = "1.jpg"
        # 声明图片对象
        if pic.split('.')[1] == "jpg":
            image = wx.Image(pic, wx.BITMAP_TYPE_JPEG)
        elif pic.split('.')[1] == "png":
            image = wx.Image(pic, wx.BITMAP_TYPE_PNG)
        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))
        portion = 1
        w = image.GetWidth() * portion
        h = image.GetHeight() * portion
        image.Rescale(w, h)
        mypic = image.ConvertToBitmap()
        # 显示图片
        wx.StaticBitmap(self.pnl, -1, bitmap=mypic, pos=(0, 0))

        # 创建垂直方向box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="中华医药专家名录检索数据库")
        font = logo.GetFont()
        font.PointSize += 20
        font = font.Bold()
        logo.SetFont(font)

        # 添加logo静态文本到vbox布局管理器
        font1 = wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)

        vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=230)
        #################################################################################
        # 创建静态框
        sb_username = wx.StaticBox(self.pnl, label="用户名")
        sb_username.SetFont(font1)
        sb_password = wx.StaticBox(self.pnl, label="密  码")
        sb_password.SetFont(font1)
        # 创建水平方向box布局管理器
        hsbox_username = wx.StaticBoxSizer(sb_username, wx.HORIZONTAL)
        hsbox_password = wx.StaticBoxSizer(sb_password, wx.HORIZONTAL)
        # 创建用户名、密码输入框
        self.user_name = wx.TextCtrl(self.pnl, size=(210, 40))
        self.user_password = wx.TextCtrl(self.pnl, size=(210, 40), style=wx.TE_PASSWORD)

        self.user_name.SetFont(font1)
        self.user_password.SetFont(font1)

        self.user_name.SetForegroundColour("#3385FF")
        # vbox.Add(self.user_name, 0, wx.EXPAND | wx.TOP, 5)

        # 添加用户名和密码输入框到hsbox布局管理器
        hsbox_username.Add(self.user_name, 0, wx.EXPAND | wx.TOP, 5)
        hsbox_password.Add(self.user_password, 0, wx.EXPAND | wx.TOP, 5)
        # 将水平box添加到垂直box
        vbox.Add(hsbox_username, proportion=0, flag=wx.CENTER | wx.TOP, border=80)
        vbox.Add(hsbox_password, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=20)
        #################################################################################
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()
        # 创建登录按钮、绑定事件处理
        login_button = wx.Button(self.pnl, label="登录", size=(100, 50))
        login_button.SetFont(font1)
        login_button.Bind(wx.EVT_BUTTON, self.LoginButton)
        register_button = wx.Button(self.pnl, label="注册", size=(100, 50))
        register_button.SetFont(font1)
        register_button.Bind(wx.EVT_BUTTON, self.RegisterButton)
        # login_button.SetForegroundColour("#FFFFFF")
        # login_button.SetBackgroundColour("#3385FF")

        # 添加登录按钮到hbox布局管理器
        hbox.Add(register_button, 0, flag=wx.RIGHT | wx.TOP, border=10)
        hbox.Add(login_button, 0, flag=wx.LEFT | wx.TOP, border=10)
        # 将水平box添加到垂直box
        vbox.Add(hbox, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER)
        #################################################################################
        # 设置面板的布局管理器vbox
        self.pnl.SetSizer(vbox)

    def LoginButton(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll1("users")
        print(np)
        # 匹配标记
        login_sign = 0
        # 匹配用户名和密码
        for i in np:
            if (i[1] == self.user_name.GetValue()) and (i[2] == self.user_password.GetValue()):
                login_sign = 1
                break
        if login_sign == 0:
            print("用户名或密码错误！")
            wx.MessageBox("用户名或密码错误！", u"提示")
        elif login_sign == 1:
            print("登录成功！")
            operation = ShowPic(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            operation.Show()
            self.Close(True)

    def RegisterButton(self, event):
        op = Sql_operation("login_users")
        np = op.FindAll1("users")
        for i in np:
            if (i[1] == self.user_name.GetValue()):
                wx.MessageBox("用户名已经注册！", u"提示")
                self.flag = 1
                break

        if self.user_name.GetValue() == "" and self.user_password.GetValue() == "":
            wx.MessageBox("用户名和密码不能为空！", u"提示")
        elif self.user_name.GetValue() == "" and self.user_password.GetValue() != "":
            wx.MessageBox("用户名不能为空！", u"提示")
        elif self.user_password.GetValue() == "" and self.user_name.GetValue() != "":
            wx.MessageBox("密码不能为空！", u"提示")
        elif self.flag == 0:
            op.InsertUser(self.user_name.GetValue(), self.user_password.GetValue())
            print("注册成功！")
            wx.MessageBox("注册成功！", u"提示")
            login = UserLogin(None, title="中华医药专家名录检索数据库", size=(960, 700))
            login.Show()
            self.Close(True)
        if self.flag == 1:
            self.flag = 0


class UserOperation(wx.Frame):
    '''
    操作界面
    '''

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(UserOperation, self).__init__(*args, **kw)
        # 设置窗口屏幕居中
        self.count = 0
        self.x = 1
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundColour("#8fd2ff")
        # 调用操作界面函数
        self.OperationInterface()

    def OperationInterface(self):

        # 创建垂直方向box布局管理器
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="中华医药专家名录检索数据库")
        font = logo.GetFont()
        font.PointSize += 30
        font = font.Bold()
        logo.SetFont(font)
        # 添加logo静态文本到vbox布局管理器
        self.vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=20)
        #################################################################################
        # 创建静态框
        font1 = wx.Font(20, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        # sb_button = wx.StaticBox(self.pnl, label="",size=(1000,100))
        # sb_button.SetFont(font1)
        # 创水平方向box布局管理器
        # vsbox_button = wx.StaticBoxSizer(sb_button,wx.HORIZONTAL)
        vsbox_button = wx.BoxSizer(wx.HORIZONTAL)
        # 创建操作按钮、绑定事件处理
        self.check_button = wx.Button(self.pnl, id=10, label="专家列表", size=(150, 70))
        self.check_button.SetFont(font1)
        self.add_button = wx.Button(self.pnl, id=11, label="专家新增", size=(150, 70))
        self.add_button.SetFont(font1)
        self.delete_button = wx.Button(self.pnl, id=12, label="专家删除", size=(150, 70))
        self.delete_button.SetFont(font1)
        self.quit_button = wx.Button(self.pnl, id=13, label="退出系统", size=(150, 70))
        self.quit_button.SetFont(font1)
        self.modify_button = wx.Button(self.pnl, id=14, label="专家修改", size=(150, 70))
        self.modify_button.SetFont(font1)
        self.inquire_button = wx.Button(self.pnl, id=15, label="专家查询", size=(150, 70))
        self.inquire_button.SetFont(font1)
        self.export_button = wx.Button(self.pnl, id=16, label="专家导出", size=(150, 70))
        self.export_button.SetFont(font1)
        self.picture_button = wx.Button(self.pnl, id=17, label="上传图片", size=(150, 70))
        self.picture_button.SetFont(font1)
        self.people_button = wx.Button(self.pnl, id=18, label="个人信息", size=(150, 70))
        self.people_button.SetFont(font1)
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=10, id2=18)
        # 添加操作按钮到vsbox布局管理器
        vsbox_button.Add(self.check_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.inquire_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.add_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.modify_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.delete_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.people_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.picture_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.export_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(self.quit_button, 0, wx.LEFT | wx.BOTTOM, 10)

        # 创建静态框
        sb_show_operation = wx.StaticBox(self.pnl, size=(1800, 1000))
        # 创建垂直方向box布局管理器
        self.vsbox_show_operation = wx.StaticBoxSizer(sb_show_operation, wx.VERTICAL)
        # 创建水平方向box布局管理器

        hbox = wx.BoxSizer()
        hbox.Add(vsbox_button, 0, wx.EXPAND | wx.TOP, 20)
        # hbox1=wx.BoxSizer()
        # hbox1.Add(self.vsbox_show_operation, 0, wx.EXPAND | wx.BOTTOM, 5)

        # 将hbox添加到垂直box
        self.vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        self.vbox.Add(self.vsbox_show_operation, proportion=0, flag=wx.CENTER)
        # self.vbox.Add(vsbox_show_operation, proportion=0, flag=wx.CENTER)
        #################################################################################
        self.pnl.SetSizer(self.vbox)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            print("专家删除操作！")
            del_button = DelOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            del_button.Show()
            self.Close(True)
        elif source_id == 13:
            self.Close(True)
        elif source_id == 14:
            print("专家修改操作！")
            add_button = ModifyOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)


class ShowPic(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ShowPic, self).__init__(*args, **kw)
        self.count = 0
        self.x = 1
        self.Center()
        # 创建窗口
        self.pnl = wx.Panel(self)
        self.pnl.SetBackgroundColour("#8fd2ff")
        # 调用操作界面函数
        self.OperationInterface()

        pic = "1.jpg"
        # 声明图片对象
        if pic.split('.')[1] == "jpg":
            image = wx.Image(pic, wx.BITMAP_TYPE_JPEG)
        elif pic.split('.')[1] == "png":
            image = wx.Image(pic, wx.BITMAP_TYPE_PNG)
        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))
        portion = 1.9
        w = image.GetWidth() * portion
        h = image.GetHeight() * 2.3
        image.Rescale(w, h)
        mypic = image.ConvertToBitmap()
        # 显示图片
        wx.StaticBitmap(self.pnl, -1, bitmap=mypic, pos=(50, 550))

    def OperationInterface(self):
        # 创建垂直方向box布局管理器
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        #################################################################################
        # 创建logo静态文本，设置字体属性
        logo = wx.StaticText(self.pnl, label="中华医药专家名录检索数据库")
        font = logo.GetFont()
        font.PointSize += 60
        font = font.Bold()
        logo.SetFont(font)
        # 添加logo静态文本到vbox布局管理器
        self.vbox.Add(logo, proportion=0, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=100)
        #################################################################################
        # 创建静态框
        font1 = wx.Font(40, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        # sb_button = wx.StaticBox(self.pnl, label="",size=(1000,100))
        # sb_button.SetFont(font1)
        # 创水平方向box布局管理器
        # vsbox_button = wx.StaticBoxSizer(sb_button,wx.HORIZONTAL)
        vsbox_button = wx.BoxSizer(wx.HORIZONTAL)
        # 创建操作按钮、绑定事件处理
        check_button = wx.Button(self.pnl, id=10, label="专家列表", size=(280, 150))
        check_button.SetFont(font1)
        add_button = wx.Button(self.pnl, id=11, label="专家新增", size=(280, 150))
        add_button.SetFont(font1)
        # delete_button = wx.Button(self.pnl, id=12, label="专家删除", size=(120, 50))
        # delete_button.SetFont(font1)
        quit_button = wx.Button(self.pnl, id=13, label="退出系统", size=(280, 150))
        quit_button.SetFont(font1)
        # modify_button = wx.Button(self.pnl, id=14, label="专家修改", size=(120, 50))
        # modify_button.SetFont(font1)
        inquire_button = wx.Button(self.pnl, id=15, label="专家查询", size=(280, 150))
        inquire_button.SetFont(font1)
        export_button = wx.Button(self.pnl, id=16, label="专家导出", size=(280, 150))
        export_button.SetFont(font1)
        # picture_button = wx.Button(self.pnl, id=17, label="上传图片", size=(120, 50))
        # picture_button.SetFont(font1)
        # people_button = wx.Button(self.pnl, id=17, label="个人信息", size=(120, 50))
        # people_button.SetFont(font1)
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=10, id2=17)
        # 添加操作按钮到vsbox布局管理器
        vsbox_button.Add(check_button, 0, wx.CENTER | wx.TOP, 50)
        vsbox_button.Add(inquire_button, 0, wx.CENTER | wx.TOP, 50)
        vsbox_button.Add(add_button, 0, wx.CENTER | wx.TOP, 50)
        '''
        vsbox_button.Add(modify_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(delete_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(people_button, 0, wx.LEFT | wx.BOTTOM, 10)
        vsbox_button.Add(picture_button, 0, wx.LEFT | wx.BOTTOM, 10)
        '''
        vsbox_button.Add(export_button, 0, wx.CENTER | wx.TOP, 50)
        vsbox_button.Add(quit_button, 0, wx.CENTER | wx.TOP, 50)

        # 创建静态框
        # sb_show_operation = wx.StaticBox(self.pnl, size=(1800, 1000))
        # 创建垂直方向box布局管理器
        # self.vsbox_show_operation = wx.StaticBoxSizer(sb_show_operation, wx.VERTICAL)
        # 创建水平方向box布局管理器

        hbox = wx.BoxSizer()
        hbox.Add(vsbox_button, 0, wx.EXPAND | wx.TOP, 20)
        # hbox1=wx.BoxSizer()
        # hbox1.Add(self.vsbox_show_operation, 0, wx.EXPAND | wx.BOTTOM, 5)

        # 将hbox添加到垂直box
        self.vbox.Add(hbox, proportion=0, flag=wx.CENTER)
        # self.vbox.Add(self.vsbox_show_operation, proportion=0, flag=wx.CENTER)
        # self.vbox.Add(vsbox_show_operation, proportion=0, flag=wx.CENTER)
        #################################################################################
        self.pnl.SetSizer(self.vbox)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            pass
        elif source_id == 13:
            login = UserLogin(None, title="中华医药专家名录检索数据库", size=(960, 700))
            login.Show()
            self.Close(True)
        elif source_id == 14:
            pass
        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)


class InquireOp(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(InquireOp, self).__init__(*args, **kw)
        # 创建信息网格
        self.index = ""
        self.name = ""
        self.hospital = ""
        self.department = ""
        self.skill = ""
        self.content = ""
        self.phone = ""
        self.link = ""
        self.x = 1
        self.picture_button.Destroy()


    def getconut(self):
        opera = Sql_operation("login_users")
        npp = opera.FindAll1("expert_info")
        self.count = int(len(npp))
        return self.count

    def show(self, x, count):
        opera = Sql_operation("login_users")
        npp = opera.FindAll1("expert_info")
        self.count = int(len(npp))
        self.x = x
        cou = self.count % 18
        if cou == 0:
            self.count = int(self.count / 18)
        else:
            self.count = int(self.count / 18) + 1
        print(self.count)
        pages = self.Page(self.x, self.count)

    def Page(self, x, count):
        font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.page = wx.Button(self.pnl, label="<上一页", id=90, size=(120, 50))
        self.page.SetFont(font1)
        self.page1 = wx.Button(self.pnl, label="下一页>", id=91, size=(120, 50))
        self.page1.SetFont(font1)
        self.page3 = wx.Button(self.pnl, label="跳转", id=92, size=(120, 50))
        self.page3.SetFont(font1)
        self.page4 = wx.Button(self.pnl, label="首页", id=93, size=(120, 50))
        self.page4.SetFont(font1)
        self.page5 = wx.Button(self.pnl, label="尾页", id=94, size=(120, 50))
        self.page5.SetFont(font1)
        page_number1 = wx.Button(self.pnl, label=str(x), id=(x + 99), size=(50, 50))
        page_number1.SetFont(font1)
        page_number2 = wx.Button(self.pnl, label=str(x + 1), id=(x + 100), size=(50, 50))
        page_number2.SetFont(font1)
        page_number3 = wx.Button(self.pnl, label=str(x + 2), id=(x + 101), size=(50, 50))
        page_number3.SetFont(font1)
        page_number4 = wx.Button(self.pnl, label=str(x + 3), id=(x + 102), size=(50, 50))
        page_number4.SetFont(font1)
        page_number5 = wx.Button(self.pnl, label=str(x + 4), id=(x + 103), size=(50, 50))
        page_number5.SetFont(font1)
        page_number6 = wx.Button(self.pnl, label=str(x + 5), id=(x + 104), size=(50, 50))
        page_number6.SetFont(font1)
        page_number7 = wx.Button(self.pnl, label=str(x + 6), id=(x + 105), size=(50, 50))
        page_number7.SetFont(font1)
        page_number8 = wx.Button(self.pnl, label=str(x + 7), id=(x + 106), size=(50, 50))
        page_number8.SetFont(font1)
        page_number9 = wx.Button(self.pnl, label=str(x + 8), id=(x + 107), size=(50, 50))
        page_number9.SetFont(font1)
        page_number10 = wx.Button(self.pnl, label=str(x + 9), id=(x + 108), size=(50, 50))
        page_number10.SetFont(font1)
        allpage = [page_number1, page_number2, page_number3, page_number4, page_number5, page_number6, page_number7,
                   page_number8, page_number9, page_number10]
        self.page2 = wx.TextCtrl(self.pnl, size=(120, 50))
        self.page2.SetFont(font1)
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=1, id2=100000)

        vsbox_button = wx.BoxSizer(wx.HORIZONTAL)
        vsbox_button.Add(self.page4, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page, 0, wx.CENTER | wx.BOTTOM, 10)

        for i in range(10):
            if i >= count:
                allpage[i].Destroy()
            else:
                vsbox_button.Add(allpage[i], 0, wx.CENTER | wx.BOTTOM, 10)

        vsbox_button.Add(self.page1, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page5, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page2, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page3, 0, wx.CENTER | wx.BOTTOM, 10)

        self.vbox.Add(vsbox_button, 0, wx.CENTER | wx.BOTTOM)
        return allpage

    def ClickButton(self, event):
        source_id = event.GetId()
        if self.count >= 10:
            if source_id > 80:
                if source_id >= 105 and source_id <= (self.count + 95):
                    # print("source_id:"+str(self.count))
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, 10)
                    flush.show(source_id - 104, 10)
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id >= 100 and source_id < 105:
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id > (self.count + 95):
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, flush.getconut())
                    flush.show(self.count - 9, flush.getconut())
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id == 90:
                    if self.x == 1:
                        pass
                    elif self.x >= 7 and self.x <= (self.count - 3):
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show((self.x - 6), flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > 1 and self.x < 7:
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > (self.count - 3):
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show(self.count - 9, flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                elif source_id == 91:
                    if self.x == self.count:
                        pass
                    elif self.x >= 5 and self.x <= (self.count - 5):
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show((self.x - 4), flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                    elif self.x >= 1 and self.x < 5:
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > (self.count - 5):
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show(self.count - 9, flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                elif source_id == 93:
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.Show()
                    self.Close(True)
                elif source_id == 94:
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.count, flush.getconut())
                    flush.show(self.count - 9, flush.getconut())
                    flush.x = self.count
                    flush.Show()
                    self.Close(True)
                elif source_id == 92:
                    value = self.page2.GetValue()
                    if value.isdigit() == True:
                        if int(value) >= 6 and int(value) <= (self.count - 4):
                            flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show((int(value) - 5), flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        elif int(value) < 6 and int(value) >= 1:
                            flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show(1, flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        elif int(value) > (self.count - 4) and int(value) <= self.count:
                            flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show(self.count - 9, flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        else:
                            wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
                    else:
                        wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
        else:
            if source_id == 100:
                print(self.count)
            if source_id >= 100 and source_id <= self.count + 99:
                print(self.count)
                flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(source_id - 99, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = source_id - 99
                flush.Show()
                self.Close(True)
            elif source_id == 90:
                if self.x == 1:
                    pass
                else:
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.x - 1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
            elif source_id == 91:
                if self.x == self.count:
                    pass
                else:
                    flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.x + 1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = self.x + 1
                    flush.Show()
                    self.Close(True)
            elif source_id == 93:
                flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(1, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = 1
                flush.Show()
                self.Close(True)
            elif source_id == 94:
                flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(self.count, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = self.count
                flush.Show()
                self.Close(True)
            elif source_id == 92:
                value = self.page2.GetValue()
                if value.isdigit() == True:
                    if int(value) >= 1 and int(value) <= self.count:
                        flush = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(int(value), flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = int(value)
                        flush.Show()
                        self.Close(True)

                    else:
                        wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
                else:
                    wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")

        if source_id == 10:
            pass
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12 and self.index != "":
            print(self.index[0])

            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否确定删除？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                op = Sql_operation("login_users")
                np = op.Del(int(self.index[0]))
                if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                    filelist = []
                    rootdir = "E:/中华医药专家照片/" + str(self.index[0])
                    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
                    if not os.listdir(rootdir):
                        shutil.rmtree(rootdir, True)
                    else:
                        for i in filelist:
                            filepath = rootdir + "/" + i
                            os.remove(filepath)
                        shutil.rmtree(rootdir, True)
                        print("success")

                del_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                del_button.creategrid(1, del_button.getconut())
                del_button.show(1, del_button.getconut())
                del_button.Show()
                self.Close(True)
                self.index = ""
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()


        elif source_id == 13:
            login = UserLogin(None, title="中华医药专家名录检索数据库", size=(960, 700))
            login.Show()
            self.Close(True)

        elif source_id == 14 and self.index != "":
            print("专家修改操作！")
            op = Sql_operation("login_users")
            np = op.FindOne(int(self.index[0]))
            add_button = ModifyOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.mod_id = self.index[0]
            add_button.name.AppendText(self.index[1])
            add_button.hospital.AppendText(self.index[2])
            add_button.department.AppendText(self.index[3])
            add_button.skill.AppendText(self.index[4])
            add_button.content.AppendText(self.index[5])
            add_button.phone.AppendText(self.index[6])
            add_button.link.AppendText(self.index[7])
            add_button.Show()
            self.Close(True)
        elif source_id == 17 and self.index != "":
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            default_dir = r"文件路径"
            file_path = tkinter.filedialog.askopenfilename(title=u'选择图片', initialdir=(os.path.expanduser(default_dir)),
                                                           filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
            if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index[0]) + "/")
            else:
                os.makedirs("E:/中华医药专家照片/" + str(self.index[0]))
                shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index[0]) + "/")

        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)
        elif source_id == 18 and self.index != "":
            op = Sql_operation("login_users")
            info = op.FindOne(self.index[0])

            if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                filelist = []
                rootdir = "E:/中华医药专家照片/" + str(self.index[0])
                filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
                if os.listdir(rootdir):
                    filepath = rootdir + "/" + filelist[0]
                    person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    person.index=int(self.index[0])
                    person.name.AppendText(info[0][1])
                    person.phone.AppendText(info[0][6])
                    person.hospital.AppendText(info[0][2])
                    person.department.AppendText((info[0][3]))
                    person.skill.AppendText((info[0][4]))
                    person.content.AppendText((info[0][5]))
                    person.link.AppendText(info[0][7])
                    person.showinformation(filepath)
                    person.Show()
                    self.Close(True)
                else:
                    person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    person.index = int(self.index[0])
                    person.name.AppendText(info[0][1])
                    person.phone.AppendText(info[0][6])
                    person.hospital.AppendText(info[0][2])
                    person.department.AppendText((info[0][3]))
                    person.skill.AppendText((info[0][4]))
                    person.content.AppendText((info[0][5]))
                    person.link.AppendText(info[0][7])
                    person.Show()
                    self.Close(True)
            else:
                person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                person.index = int(self.index[0])
                person.name.AppendText(info[0][1])
                person.phone.AppendText(info[0][6])
                person.hospital.AppendText(info[0][2])
                person.department.AppendText((info[0][3]))
                person.skill.AppendText((info[0][4]))
                person.content.AppendText((info[0][5]))
                person.link.AppendText(info[0][7])
                person.Show()
                self.Close(True)

    def creategrid(self, x, count):
        self.stu_grid = self.CreateGrid(x, count)
        self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        self.vsbox_show_operation.Add(self.stu_grid, 0, wx.ALL | wx.CENTER | wx.TOP | wx.EXPAND)

    def CreateGrid(self, x, count):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取stu_information表中的信息，返回为二维元组
        np = op.FindAll("expert_info", x, count)
        column_names = ("专家姓名", "医院", "科室", "研究方向", "节目内容", "联系电话", "节目链接")
        stu_grid = wx.grid.Grid(self.pnl)
        stu_grid.CreateGrid(len(np), len(np[0]) - 1)
        print(len(np))
        print(len(np[0]) - 1)
        stu_grid.SetRowLabelSize(100)
        stu_grid.SetColLabelSize(50)
        stu_grid.SetLabelFont(wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False))

        for row in range(len(np)):
            stu_grid.SetRowSize(row, 35)
            stu_grid.SetRowLabelValue(row, str(np[row][0]))  # 确保网格序列号与数据库id保持一致
            for col in range(1, len(np[row])):
                stu_grid.SetCellFont(row, col - 1, wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False))
                stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
                stu_grid.SetReadOnly(row, col - 1, True)

        stu_grid.SetColSize(0, 150)
        stu_grid.SetColSize(1, 250)
        stu_grid.SetColSize(2, 200)
        stu_grid.SetColSize(3, 250)
        stu_grid.SetColSize(4, 400)
        stu_grid.SetColSize(5, 200)
        stu_grid.SetColSize(6, 270)
        # stu_grid.AutoSize()
        return stu_grid

    def OnLabelleftClick(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll("expert_info", self.x, self.count)
        print("RowIdx: {0}".format(event.GetRow()))
        print("ColIdx: {0}".format(event.GetRow()))
        print(np[event.GetRow()])
        self.index = np[event.GetRow()]
        event.Skip()


class InquireOp1(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(InquireOp1, self).__init__(*args, **kw)
        self.check_button.Destroy()
        self.add_button.Destroy()
        self.delete_button.Destroy()
        self.quit_button.Destroy()
        self.modify_button.Destroy()
        self.inquire_button.Destroy()
        self.export_button.Destroy()
        self.picture_button.Destroy()
        self.people_button.Destroy()

        # 创建添加信息输入框、添加按钮
        self.index = ""
        font1 = wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.name = wx.TextCtrl(self.pnl, size=(300, 40))
        self.name.SetFont(font1)
        self.hospital = wx.TextCtrl(self.pnl, size=(300, 40))
        self.hospital.SetFont(font1)
        self.department = wx.TextCtrl(self.pnl, size=(300, 40))
        self.department.SetFont(font1)
        self.skill = wx.TextCtrl(self.pnl, size=(650, 40))
        self.skill.SetFont(font1)
        self.content = wx.TextCtrl(self.pnl, size=(650, 150), style=wx.TE_MULTILINE)
        self.content.SetFont(font1)
        self.phone = wx.TextCtrl(self.pnl, size=(300, 40))
        self.phone.SetFont(font1)
        self.link = wx.TextCtrl(self.pnl, size=(650, 40))
        self.link.SetFont(font1)
        self.inq_affirm = wx.Button(self.pnl, label="查询", size=(150, 70))
        self.back = wx.Button(self.pnl, label="返回", size=(150, 70))

        # 为添加按钮组件绑定事件处理
        self.inq_affirm.Bind(wx.EVT_BUTTON, self.InqAffirm)
        self.back.Bind(wx.EVT_BUTTON, self.BackAffirm)
        #################################################################################
        # 创建静态框
        # font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.inq_affirm.SetFont(font1)
        self.back.SetFont(font1)
        sb_name = wx.StaticBox(self.pnl, label="专家姓名")
        sb_name.SetFont(font1)
        sb_phone = wx.StaticBox(self.pnl, label="联系电话")
        sb_phone.SetFont(font1)
        sb_hospital = wx.StaticBox(self.pnl, label="医  院")
        sb_hospital.SetFont(font1)
        sb_department = wx.StaticBox(self.pnl, label="科  室")
        sb_department.SetFont(font1)
        sb_skill = wx.StaticBox(self.pnl, label="研究方向")
        sb_skill.SetFont(font1)
        sb_content = wx.StaticBox(self.pnl, label="节目内容")
        sb_content.SetFont(font1)
        sb_link = wx.StaticBox(self.pnl, label="节目链接")
        sb_link.SetFont(font1)

        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_phone = wx.StaticBoxSizer(sb_phone, wx.HORIZONTAL)
        hsbox_hospital = wx.StaticBoxSizer(sb_hospital, wx.HORIZONTAL)
        hsbox_department = wx.StaticBoxSizer(sb_department, wx.HORIZONTAL)
        hsbox_skill = wx.StaticBoxSizer(sb_skill, wx.HORIZONTAL)
        hsbox_content = wx.StaticBoxSizer(sb_content, wx.HORIZONTAL)
        hsbox_link = wx.StaticBoxSizer(sb_link, wx.HORIZONTAL)

        hsbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.name, 0, wx.EXPAND | wx.TOP, 5)
        hsbox_phone.Add(self.phone, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox1.Add(hsbox_name, 0, wx.RIGHT | wx.TOP, 20)
        hsbox1.Add(hsbox_phone, 0, wx.LEFT | wx.TOP, 20)

        hsbox_hospital.Add(self.hospital, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_department.Add(self.department, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox2.Add(hsbox_hospital, 0, wx.RIGHT | wx.BOTTOM, 20)
        hsbox2.Add(hsbox_department, 0, wx.LEFT | wx.BOTTOM, 20)

        hsbox_skill.Add(self.skill, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_content.Add(self.content, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_link.Add(self.link, 0, wx.EXPAND | wx.BOTTOM, 20)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_name, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_phone, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox1, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox2, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        # self.vsbox_show_operation.Add(hsbox_hospital, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_department, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_skill, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_link, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_content, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.anniu=wx.BoxSizer(wx.HORIZONTAL)
        self.anniu.Add(self.inq_affirm, 0, wx.RIGHT | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.anniu.Add(self.back, 0, wx.LEFT | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(self.anniu, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12 and self.index != "":
            pass
        elif source_id == 13:
            self.Close(True)
        elif source_id == 14:
            pass
        elif source_id == 15:
            pass
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)

    def BackAffirm(self,event):
        print("专家列表")
        inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
        inquire_button.creategrid(1, inquire_button.getconut())
        inquire_button.show(1, inquire_button.getconut())
        inquire_button.Show()
        self.Close(True)
    def InqAffirm(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        stu_name = self.name.GetValue()
        print(stu_name)
        stu_hospital = self.hospital.GetValue()
        print(stu_hospital)
        stu_department = self.department.GetValue()
        print(stu_department)
        stu_skill = self.skill.GetValue()
        print(stu_skill)
        stu_content = self.content.GetValue()
        print(stu_content)
        stu_phone = self.phone.GetValue()
        print(stu_phone)
        stu_link = self.link.GetValue()
        print(stu_link)
        if stu_name == "" and stu_hospital == "" and stu_department == "" and stu_skill == "" and stu_content == "" and stu_phone == "" and stu_link == "":
            del_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            del_button.creategrid(1, del_button.getconut())
            del_button.show(1, del_button.getconut())
            del_button.Show()
            self.Close(True)
        else:
            op.DelAll()
            np = op.Find1(stu_name, stu_hospital, stu_department, stu_skill, stu_content, stu_phone, stu_link)
            if np == ():
                wx.MessageBox("无符合条件数据！", u"提示")
                print("专家查询操作！")
                inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.Show()
                self.Close(True)
            else:
                op.Find(stu_name, stu_hospital, stu_department, stu_skill, stu_content, stu_phone, stu_link)
                inq_button = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inq_button.creategrid(1, inq_button.getconut())
                inq_button.show(1, inq_button.getconut())
                inq_button.Show()
                self.Close(True)




class InquireOp2(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(InquireOp2, self).__init__(*args, **kw)
        # 创建信息网格
        self.index = ""
        self.name = ""
        self.hospital = ""
        self.department = ""
        self.skill = ""
        self.content = ""
        self.phone = ""
        self.link = ""
        self.x = 1
        '''
        self.stu_grid = self.CreateGrid()
        self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        self.vsbox_show_operation.Add(self.stu_grid, 0, wx.ALL | wx.CENTER | wx.TOP | wx.EXPAND)
'''

    def getconut(self):
        opera = Sql_operation("login_users")
        npp = opera.FindAll1("inquire")
        self.count = int(len(npp))
        return self.count

    def show(self, x, count):
        opera = Sql_operation("login_users")
        npp = opera.FindAll1("inquire")
        self.count = int(len(npp))
        self.x = x
        cou = self.count % 18
        if cou == 0:
            self.count = int(self.count / 18)
        else:
            self.count = int(self.count / 18) + 1
        print(self.count)
        pages = self.Page(self.x, self.count)

    def Page(self, x, count):

        font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.page = wx.Button(self.pnl, label="<上一页", id=90, size=(120, 50))
        self.page.SetFont(font1)
        self.page1 = wx.Button(self.pnl, label="下一页>", id=91, size=(120, 50))
        self.page1.SetFont(font1)
        self.page3 = wx.Button(self.pnl, label="跳转", id=92, size=(120, 50))
        self.page3.SetFont(font1)
        self.page4 = wx.Button(self.pnl, label="首页", id=93, size=(120, 50))
        self.page4.SetFont(font1)
        self.page5 = wx.Button(self.pnl, label="尾页", id=94, size=(120, 50))
        self.page5.SetFont(font1)
        page_number1 = wx.Button(self.pnl, label=str(x), id=(x + 99), size=(50, 50))
        page_number1.SetFont(font1)
        page_number2 = wx.Button(self.pnl, label=str(x + 1), id=(x + 100), size=(50, 50))
        page_number2.SetFont(font1)
        page_number3 = wx.Button(self.pnl, label=str(x + 2), id=(x + 101), size=(50, 50))
        page_number3.SetFont(font1)
        page_number4 = wx.Button(self.pnl, label=str(x + 3), id=(x + 102), size=(50, 50))
        page_number4.SetFont(font1)
        page_number5 = wx.Button(self.pnl, label=str(x + 4), id=(x + 103), size=(50, 50))
        page_number5.SetFont(font1)
        page_number6 = wx.Button(self.pnl, label=str(x + 5), id=(x + 104), size=(50, 50))
        page_number6.SetFont(font1)
        page_number7 = wx.Button(self.pnl, label=str(x + 6), id=(x + 105), size=(50, 50))
        page_number7.SetFont(font1)
        page_number8 = wx.Button(self.pnl, label=str(x + 7), id=(x + 106), size=(50, 50))
        page_number8.SetFont(font1)
        page_number9 = wx.Button(self.pnl, label=str(x + 8), id=(x + 107), size=(50, 50))
        page_number9.SetFont(font1)
        page_number10 = wx.Button(self.pnl, label=str(x + 9), id=(x + 108), size=(50, 50))
        page_number10.SetFont(font1)
        allpage = [page_number1, page_number2, page_number3, page_number4, page_number5, page_number6, page_number7,
                   page_number8, page_number9, page_number10]
        self.page2 = wx.TextCtrl(self.pnl, size=(120, 50))
        self.page2.SetFont(font1)
        self.Bind(wx.EVT_BUTTON, self.ClickButton, id=1, id2=100000)

        vsbox_button = wx.BoxSizer(wx.HORIZONTAL)
        vsbox_button.Add(self.page4, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page, 0, wx.CENTER | wx.BOTTOM, 10)

        for i in range(10):
            if i >= count:
                allpage[i].Destroy()
            else:
                vsbox_button.Add(allpage[i], 0, wx.CENTER | wx.BOTTOM, 10)

        vsbox_button.Add(self.page1, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page5, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page2, 0, wx.CENTER | wx.BOTTOM, 10)
        vsbox_button.Add(self.page3, 0, wx.CENTER | wx.BOTTOM, 10)

        self.vbox.Add(vsbox_button, 0, wx.CENTER | wx.BOTTOM)
        return allpage

    def ClickButton(self, event):
        source_id = event.GetId()
        if self.count >= 10:
            if source_id > 80:
                if source_id >= 105 and source_id <= (self.count + 95):
                    # print("source_id:"+str(self.count))
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, 10)
                    flush.show(source_id - 104, 10)
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id >= 100 and source_id < 105:
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id > (self.count + 95):
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(source_id - 99, flush.getconut())
                    flush.show(self.count - 9, flush.getconut())
                    flush.x = source_id - 99
                    flush.Show()
                    self.Close(True)
                elif source_id == 90:
                    if self.x == 1:
                        pass
                    elif self.x >= 7 and self.x <= (self.count - 3):
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show((self.x - 6), flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > 1 and self.x < 7:
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > (self.count - 3):
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x - 1, flush.getconut())
                        flush.show(self.count - 9, flush.getconut())
                        flush.x = self.x - 1
                        flush.Show()
                        self.Close(True)
                elif source_id == 91:
                    if self.x == self.count:
                        pass
                    elif self.x >= 5 and self.x <= (self.count - 5):
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show((self.x - 4), flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                    elif self.x >= 1 and self.x < 5:
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                    elif self.x > (self.count - 5):
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(self.x + 1, flush.getconut())
                        flush.show(self.count - 9, flush.getconut())
                        flush.x = self.x + 1
                        flush.Show()
                        self.Close(True)
                elif source_id == 93:
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.Show()
                    self.Close(True)
                elif source_id == 94:
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.count, flush.getconut())
                    flush.show(self.count - 9, flush.getconut())
                    flush.x = self.count
                    flush.Show()
                    self.Close(True)
                elif source_id == 92:
                    value = self.page2.GetValue()
                    if value.isdigit() == True:
                        if int(value) >= 6 and int(value) <= (self.count - 4):
                            flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show((int(value) - 5), flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        elif int(value) < 6 and int(value) >= 1:
                            flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show(1, flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        elif int(value) > (self.count - 4) and int(value) <= self.count:
                            flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                            flush.creategrid(int(value), flush.getconut())
                            flush.show(self.count - 9, flush.getconut())
                            flush.x = int(value)
                            flush.Show()
                            self.Close(True)
                        else:
                            wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
                    else:
                        wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
        else:
            if source_id == 100:
                print(self.count)
            if source_id >= 100 and source_id <= self.count + 99:
                print(self.count)
                flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(source_id - 99, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = source_id - 99
                flush.Show()
                self.Close(True)
            elif source_id == 90:
                if self.x == 1:
                    pass
                else:
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.x - 1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = self.x - 1
                    flush.Show()
                    self.Close(True)
            elif source_id == 91:
                if self.x == self.count:
                    pass
                else:
                    flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    flush.creategrid(self.x + 1, flush.getconut())
                    flush.show(1, flush.getconut())
                    flush.x = self.x + 1
                    flush.Show()
                    self.Close(True)
            elif source_id == 93:
                flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(1, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = 1
                flush.Show()
                self.Close(True)
            elif source_id == 94:
                flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                flush.creategrid(self.count, flush.getconut())
                flush.show(1, flush.getconut())
                flush.x = self.count
                flush.Show()
                self.Close(True)
            elif source_id == 92:
                value = self.page2.GetValue()
                if value.isdigit() == True:
                    if int(value) >= 1 and int(value) <= self.count:
                        flush = InquireOp2(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                        flush.creategrid(int(value), flush.getconut())
                        flush.show(1, flush.getconut())
                        flush.x = int(value)
                        flush.Show()
                        self.Close(True)

                    else:
                        wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")
                else:
                    wx.MessageBox("共" + str(self.count) + "页，请输入正确的页数！", u"提示")

        if source_id == 10:
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12 and self.index != "":
            print(self.index[0])
            print("专家删除操作！")
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否确定删除？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                op = Sql_operation("login_users")
                np = op.Del(int(self.index[0]))
                if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                    filelist = []
                    rootdir = "E:/中华医药专家照片/" + str(self.index[0])
                    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
                    if not os.listdir(rootdir):
                        shutil.rmtree(rootdir, True)
                    else:
                        for i in filelist:
                            filepath = rootdir + "/" + i
                            os.remove(filepath)
                        shutil.rmtree(rootdir, True)
                        print("success")

                del_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                del_button.creategrid(1, del_button.getconut())
                del_button.show(1, del_button.getconut())
                del_button.Show()
                self.Close(True)
                self.index = ""
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()
        elif source_id == 13:
            self.Close(True)
        elif source_id == 14 and self.index != "":
            print("专家修改操作！")
            op = Sql_operation("login_users")
            np = op.FindOne(int(self.index[0]))
            add_button = ModifyOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.mod_id = self.index[0]
            add_button.name.AppendText(self.index[1])
            add_button.hospital.AppendText(self.index[2])
            add_button.department.AppendText(self.index[3])
            add_button.skill.AppendText(self.index[4])
            add_button.content.AppendText(self.index[5])
            add_button.phone.AppendText(self.index[6])
            add_button.link.AppendText(self.index[7])
            add_button.Show()
            self.Close(True)
        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)
        elif source_id == 17 and self.index != "":
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            default_dir = r"文件路径"
            file_path = tkinter.filedialog.askopenfilename(title=u'选择图片', initialdir=(os.path.expanduser(default_dir)),
                                                           filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
            if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index[0]) + "/")
            else:
                os.makedirs("E:/中华医药专家照片/" + str(self.index[0]))
                shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index[0]) + "/")
        elif source_id == 18 and self.index != "":
            op = Sql_operation("login_users")
            info = op.FindOne(self.index[0])

            if os.path.exists("E:/中华医药专家照片/" + str(self.index[0])):  # 如果文件存在
                filelist = []
                rootdir = "E:/中华医药专家照片/" + str(self.index[0])
                filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
                if os.listdir(rootdir):
                    filepath = rootdir + "/" + filelist[0]
                    person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    person.index = int(self.index[0])
                    person.name.AppendText(info[0][1])
                    person.phone.AppendText(info[0][6])
                    person.hospital.AppendText(info[0][2])
                    person.department.AppendText((info[0][3]))
                    person.skill.AppendText((info[0][4]))
                    person.content.AppendText((info[0][5]))
                    person.link.AppendText(info[0][7])
                    person.showinformation(filepath)
                    person.Show()
                    self.Close(True)
                else:
                    person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                    person.index = int(self.index[0])
                    person.name.AppendText(info[0][1])
                    person.phone.AppendText(info[0][6])
                    person.hospital.AppendText(info[0][2])
                    person.department.AppendText((info[0][3]))
                    person.skill.AppendText((info[0][4]))
                    person.content.AppendText((info[0][5]))
                    person.link.AppendText(info[0][7])
                    person.Show()
                    self.Close(True)
            else:
                person = Person(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                person.index = int(self.index[0])
                person.name.AppendText(info[0][1])
                person.phone.AppendText(info[0][6])
                person.hospital.AppendText(info[0][2])
                person.department.AppendText((info[0][3]))
                person.skill.AppendText((info[0][4]))
                person.content.AppendText((info[0][5]))
                person.link.AppendText(info[0][7])
                person.Show()
                self.Close(True)

    def creategrid(self, x, count):
        self.stu_grid = self.CreateGrid(x, count)
        self.stu_grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelleftClick)
        self.vsbox_show_operation.Add(self.stu_grid, 0, wx.ALL | wx.CENTER | wx.TOP | wx.EXPAND)

    def CreateGrid(self, x, count):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取stu_information表中的信息，返回为二维元组
        np = op.FindAll("inquire", x, count)
        column_names = ("专家姓名", "医院", "科室", "研究方向", "节目内容", "联系电话", "节目链接")
        stu_grid = wx.grid.Grid(self.pnl)
        stu_grid.CreateGrid(len(np), len(np[0]) - 1)
        print(len(np))
        print(len(np[0]) - 1)
        stu_grid.SetRowLabelSize(100)
        stu_grid.SetColLabelSize(50)
        stu_grid.SetLabelFont(wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False))

        for row in range(len(np)):
            stu_grid.SetRowSize(row, 35)
            stu_grid.SetRowLabelValue(row, str(np[row][0]))  # 确保网格序列号与数据库id保持一致
            for col in range(1, len(np[row])):
                stu_grid.SetCellFont(row, col - 1, wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False))
                stu_grid.SetColLabelValue(col - 1, column_names[col - 1])
                stu_grid.SetCellValue(row, col - 1, str(np[row][col]))
                stu_grid.SetReadOnly(row, col - 1, True)

        stu_grid.SetColSize(0, 150)
        stu_grid.SetColSize(1, 250)
        stu_grid.SetColSize(2, 200)
        stu_grid.SetColSize(3, 250)
        stu_grid.SetColSize(4, 400)
        stu_grid.SetColSize(5, 200)
        stu_grid.SetColSize(6, 270)
        # stu_grid.AutoSize()
        return stu_grid

    def OnLabelleftClick(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 获取users表中的用户名和密码信息，返回为二维元组
        np = op.FindAll("inquire", self.x, self.count)
        print("RowIdx: {0}".format(event.GetRow()))
        print("ColIdx: {0}".format(event.GetRow()))
        print(np[event.GetRow()])
        self.index = np[event.GetRow()]
        event.Skip()


class Person(UserOperation):
    def __init__(self, *args, **kw):
        super(Person, self).__init__(*args, **kw)
        self.index=0
        self.check_button.Destroy()
        self.add_button.Destroy()
        self.delete_button.Destroy()
        self.quit_button.Destroy()
        self.modify_button.Destroy()
        self.inquire_button.Destroy()
        self.export_button.Destroy()
        self.picture_button.Destroy()
        self.people_button.Destroy()
        # 连接login_users数据库
        op = Sql_operation("login_users")
        # 创建添加信息输入框、添加按钮
        font1 = wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.name = wx.TextCtrl(self.pnl, size=(300, 40), style=wx.TE_READONLY)
        self.name.SetFont(font1)
        self.hospital = wx.TextCtrl(self.pnl, size=(300, 40), style=wx.TE_READONLY)
        self.hospital.SetFont(font1)
        self.department = wx.TextCtrl(self.pnl, size=(300, 40), style=wx.TE_READONLY)
        self.department.SetFont(font1)
        self.skill = wx.TextCtrl(self.pnl, size=(650, 40), style=wx.TE_READONLY)
        self.skill.SetFont(font1)
        self.content = wx.TextCtrl(self.pnl, size=(650, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.content.SetFont(font1)
        self.phone = wx.TextCtrl(self.pnl, size=(300, 40), style=wx.TE_READONLY)
        self.phone.SetFont(font1)
        self.link = wx.TextCtrl(self.pnl, size=(650, 40), style=wx.TE_READONLY)
        self.link.SetFont(font1)
        self.picture_button = wx.Button(self.pnl, label="上传图片", size=(150, 70))
        self.picture_button.SetFont(font1)
        self.back = wx.Button(self.pnl, label="返回", size=(150, 70))
        self.back.SetFont(font1)
        self.picture_button.Bind(wx.EVT_BUTTON, self.ShangAffirm)
        self.back.Bind(wx.EVT_BUTTON, self.BackAffirm)
        self.anniu=wx.BoxSizer(wx.HORIZONTAL)
        self.anniu.Add(self.picture_button,0,wx.TOP | wx.RIGHT,20)
        self.anniu.Add(self.back, 0, wx.TOP | wx.LEFT, 20)

        sb_name = wx.StaticBox(self.pnl, label="专家姓名")
        sb_name.SetFont(font1)
        sb_phone = wx.StaticBox(self.pnl, label="联系电话")
        sb_phone.SetFont(font1)
        sb_hospital = wx.StaticBox(self.pnl, label="医  院")
        sb_hospital.SetFont(font1)
        sb_department = wx.StaticBox(self.pnl, label="科  室")
        sb_department.SetFont(font1)
        sb_skill = wx.StaticBox(self.pnl, label="研究方向")
        sb_skill.SetFont(font1)
        sb_content = wx.StaticBox(self.pnl, label="节目内容")
        sb_content.SetFont(font1)
        sb_link = wx.StaticBox(self.pnl, label="节目链接")
        sb_link.SetFont(font1)

        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_phone = wx.StaticBoxSizer(sb_phone, wx.HORIZONTAL)
        hsbox_hospital = wx.StaticBoxSizer(sb_hospital, wx.HORIZONTAL)
        hsbox_department = wx.StaticBoxSizer(sb_department, wx.HORIZONTAL)
        hsbox_skill = wx.StaticBoxSizer(sb_skill, wx.HORIZONTAL)
        hsbox_content = wx.StaticBoxSizer(sb_content, wx.HORIZONTAL)
        hsbox_link = wx.StaticBoxSizer(sb_link, wx.HORIZONTAL)

        hsbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.name, 0, wx.EXPAND | wx.TOP, 5)
        hsbox_phone.Add(self.phone, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox1.Add(hsbox_name, 0, wx.RIGHT | wx.TOP, 20)
        hsbox1.Add(hsbox_phone, 0, wx.LEFT | wx.TOP, 20)

        hsbox_hospital.Add(self.hospital, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_department.Add(self.department, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox2.Add(hsbox_hospital, 0, wx.RIGHT | wx.BOTTOM, 20)
        hsbox2.Add(hsbox_department, 0, wx.LEFT | wx.BOTTOM, 20)

        hsbox_skill.Add(self.skill, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_content.Add(self.content, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_link.Add(self.link, 0, wx.EXPAND | wx.BOTTOM, 20)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_name, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_phone, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox1, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox2, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        # self.vsbox_show_operation.Add(hsbox_hospital, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_department, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_skill, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_link, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_content, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(self.anniu,0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        #self.vbox.Add(self.vsbox_show_operation,0,wx.CENTER | wx.TOP)
        #self.vbox.Add(self.anniu, 0, wx.CENTER )

    def ShangAffirm(self,event):
        root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
        root.withdraw()  # 将Tkinter.Tk()实例隐藏
        default_dir = r"文件路径"
        file_path = tkinter.filedialog.askopenfilename(title=u'选择图片', initialdir=(os.path.expanduser(default_dir)),
                                                       filetypes=[("PNG", ".png"), ("JPG", ".jpg")])
        if os.path.exists("E:/中华医药专家照片/" + str(self.index)):  # 如果文件存在
            shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index) + "/")
            wx.MessageBox("上传成功！", u"提示")
        else:
            os.makedirs("E:/中华医药专家照片/" + str(self.index))
            shutil.copy(file_path, "E:/中华医药专家照片/" + str(self.index) + "/")
        print("专家列表")
        inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
        inquire_button.creategrid(1, inquire_button.getconut())
        inquire_button.show(1, inquire_button.getconut())
        inquire_button.Show()
        self.Close(True)



    def BackAffirm(self, event):
        print("专家列表")
        inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
        inquire_button.creategrid(1, inquire_button.getconut())
        inquire_button.show(1, inquire_button.getconut())
        inquire_button.Show()
        self.Close(True)

    def showinformation(self, pic):
        # pic="2.jpg"
        if pic.split('.')[1] == "jpg":
            image = wx.Image(pic, wx.BITMAP_TYPE_JPEG)
        elif pic.split('.')[1] == "png":
            image = wx.Image(pic, wx.BITMAP_TYPE_PNG)
        print('图片的尺寸为{0}x{1}'.format(image.GetWidth(), image.GetHeight()))
        portion = 0
        if image.GetWidth() <= 400 and image.GetHeight() <= 400:
            if image.GetWidth() >= image.GetHeight():
                portion = 400 / image.GetWidth()
            else:
                portion = 400 / image.GetHeight()
        elif image.GetWidth() >= 400 and image.GetHeight() >= 400:
            if image.GetWidth() >= image.GetHeight():
                portion = 400 / image.GetWidth()
            else:
                portion = 400 / image.GetHeight()
        elif image.GetWidth() <= 400 and image.GetHeight() >= 400:
            portion = 400 / image.GetHeight()
        elif image.GetWidth() >= 400 and image.GetHeight() <= 400:
            portion = 400 / image.GetWidth()

        w = int(image.GetWidth() * portion)
        h = int(image.GetHeight() * portion)
        image.Rescale(w, h)
        mypic = image.ConvertToBitmap()
        # 显示图片
        wx.StaticBitmap(self.pnl, -1, bitmap=mypic, pos=(100, 240))

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)

        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            pass
        elif source_id == 13:
            self.Close(True)

        elif source_id == 14:
            pass
        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)


# 继承UserOperation类，实现初始化操作界面
class AddOp(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(AddOp, self).__init__(*args, **kw)
        self.check_button.Destroy()
        self.add_button.Destroy()
        self.delete_button.Destroy()
        self.quit_button.Destroy()
        self.modify_button.Destroy()
        self.inquire_button.Destroy()
        self.export_button.Destroy()
        self.picture_button.Destroy()
        self.people_button.Destroy()
        # 创建添加信息输入框、添加按钮
        font1 = wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.name = wx.TextCtrl(self.pnl, size=(300, 40))
        self.name.SetFont(font1)
        self.hospital = wx.TextCtrl(self.pnl, size=(300, 40))
        self.hospital.SetFont(font1)
        self.department = wx.TextCtrl(self.pnl, size=(300, 40))
        self.department.SetFont(font1)
        self.skill = wx.TextCtrl(self.pnl, size=(650, 40))
        self.skill.SetFont(font1)
        self.content = wx.TextCtrl(self.pnl, size=(650, 150), style=wx.TE_MULTILINE)
        self.content.SetFont(font1)
        self.phone = wx.TextCtrl(self.pnl, size=(300, 40))
        self.phone.SetFont(font1)
        self.link = wx.TextCtrl(self.pnl, size=(650, 40))
        self.link.SetFont(font1)
        self.add_affirm = wx.Button(self.pnl, label="增加", size=(150, 70))
        self.back = wx.Button(self.pnl, label="返回", size=(150, 70))

        # 为添加按钮组件绑定事件处理
        self.add_affirm.Bind(wx.EVT_BUTTON, self.AddAffirm)
        self.back.Bind(wx.EVT_BUTTON, self.BackAffirm)
        #################################################################################
        # 创建静态框
        # font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.add_affirm.SetFont(font1)
        self.back.SetFont(font1)
        sb_name = wx.StaticBox(self.pnl, label="专家姓名")
        sb_name.SetFont(font1)
        sb_phone = wx.StaticBox(self.pnl, label="联系电话")
        sb_phone.SetFont(font1)
        sb_hospital = wx.StaticBox(self.pnl, label="医  院")
        sb_hospital.SetFont(font1)
        sb_department = wx.StaticBox(self.pnl, label="科  室")
        sb_department.SetFont(font1)
        sb_skill = wx.StaticBox(self.pnl, label="研究方向")
        sb_skill.SetFont(font1)
        sb_content = wx.StaticBox(self.pnl, label="节目内容")
        sb_content.SetFont(font1)
        sb_link = wx.StaticBox(self.pnl, label="节目链接")
        sb_link.SetFont(font1)

        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_phone = wx.StaticBoxSizer(sb_phone, wx.HORIZONTAL)
        hsbox_hospital = wx.StaticBoxSizer(sb_hospital, wx.HORIZONTAL)
        hsbox_department = wx.StaticBoxSizer(sb_department, wx.HORIZONTAL)
        hsbox_skill = wx.StaticBoxSizer(sb_skill, wx.HORIZONTAL)
        hsbox_content = wx.StaticBoxSizer(sb_content, wx.HORIZONTAL)
        hsbox_link = wx.StaticBoxSizer(sb_link, wx.HORIZONTAL)

        hsbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.name, 0, wx.EXPAND | wx.TOP, 5)
        hsbox_phone.Add(self.phone, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox1.Add(hsbox_name, 0, wx.RIGHT | wx.TOP, 20)
        hsbox1.Add(hsbox_phone, 0, wx.LEFT | wx.TOP, 20)

        hsbox_hospital.Add(self.hospital, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_department.Add(self.department, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox2.Add(hsbox_hospital, 0, wx.RIGHT | wx.BOTTOM, 20)
        hsbox2.Add(hsbox_department, 0, wx.LEFT | wx.BOTTOM, 20)

        hsbox_skill.Add(self.skill, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_content.Add(self.content, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_link.Add(self.link, 0, wx.EXPAND | wx.BOTTOM, 20)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_name, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_phone, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox1, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox2, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        # self.vsbox_show_operation.Add(hsbox_hospital, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_department, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_skill, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_link, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_content, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.anniu=wx.BoxSizer(wx.HORIZONTAL)
        self.anniu.Add(self.add_affirm, 0, wx.RIGHT | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.anniu.Add(self.back, 0, wx.LEFT | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(self.anniu, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '数据未保存，是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.AddAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()

        elif source_id == 11:
            pass
        elif source_id == 12:
            pass
        elif source_id == 13:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '数据未保存，是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.AddAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                self.Close(True)
            app.MainLoop()

        elif source_id == 14:
            pass
        elif source_id == 15:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '数据未保存，是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.AddAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家查询操作！")
                inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()

        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)

    def BackAffirm(self, event):
        op = Sql_operation("login_users")
        stu_name = self.name.GetValue()
        print(stu_name)
        stu_hospital = self.hospital.GetValue()
        print(stu_hospital)
        stu_department = self.department.GetValue()
        print(stu_department)
        stu_skill = self.skill.GetValue()
        print(stu_skill)
        stu_content = self.content.GetValue()
        print(stu_content)
        stu_phone = self.phone.GetValue()
        print(stu_phone)
        stu_link = self.link.GetValue()
        if stu_name == "" and stu_hospital == "" and stu_department == "" and stu_skill == "" and stu_content == "" and stu_phone == "" and stu_link == "":
            print("专家列表")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)
        else:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否保存当前专家信息？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.AddAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()


    def AddAffirm(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        stu_name = self.name.GetValue()
        print(stu_name)
        stu_hospital = self.hospital.GetValue()
        print(stu_hospital)
        stu_department = self.department.GetValue()
        print(stu_department)
        stu_skill = self.skill.GetValue()
        print(stu_skill)
        stu_content = self.content.GetValue()
        print(stu_content)
        stu_phone = self.phone.GetValue()
        print(stu_phone)
        stu_link = self.link.GetValue()
        print(stu_link)
        if stu_name=="" and stu_hospital=="" and stu_department=="" and stu_skill=="" and stu_content=="" and stu_phone=="" and stu_link=="" :
            wx.MessageBox("输入为空，请输入数据后保存！", u"提示")
        else:
            np = op.Insert(stu_name, stu_hospital, stu_department, stu_skill, stu_content, stu_phone, stu_link)
            del_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            del_button.Show()
            self.Close(True)



class ModifyOp(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(ModifyOp, self).__init__(*args, **kw)
        self.check_button.Destroy()
        self.add_button.Destroy()
        self.delete_button.Destroy()
        self.quit_button.Destroy()
        self.modify_button.Destroy()
        self.inquire_button.Destroy()
        self.export_button.Destroy()
        self.picture_button.Destroy()
        self.people_button.Destroy()

        # 创建专家删除信息输入框、按钮
        # self.del_id = wx.TextCtrl(self.pnl, pos=(407, 78), size=(210, 20))
        self.mod_id = ""
        font1 = wx.Font(18, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.name = wx.TextCtrl(self.pnl, size=(300, 40))
        self.name.SetFont(font1)
        self.hospital = wx.TextCtrl(self.pnl, size=(300, 40))
        self.hospital.SetFont(font1)
        self.department = wx.TextCtrl(self.pnl, size=(300, 40))
        self.department.SetFont(font1)
        self.skill = wx.TextCtrl(self.pnl, size=(650, 40))
        self.skill.SetFont(font1)
        self.content = wx.TextCtrl(self.pnl, size=(650, 150), style=wx.TE_MULTILINE)
        self.content.SetFont(font1)
        self.phone = wx.TextCtrl(self.pnl, size=(300, 40))
        self.phone.SetFont(font1)
        self.link = wx.TextCtrl(self.pnl, size=(650, 40))
        self.link.SetFont(font1)
        self.modify_affirm = wx.Button(self.pnl, label="保存", size=(150, 70))
        self.nonmodify_affirm = wx.Button(self.pnl, label="返回", size=(150, 70))

        # 为添加按钮组件绑定事件处理
        self.modify_affirm.Bind(wx.EVT_BUTTON, self.ModAffirm)
        self.nonmodify_affirm.Bind(wx.EVT_BUTTON, self.NonModAffirm)
        #################################################################################
        # 创建静态框
        # font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.BOLD, False)
        self.modify_affirm.SetFont(font1)
        self.nonmodify_affirm.SetFont(font1)
        sb_name = wx.StaticBox(self.pnl, label="专家姓名")
        sb_name.SetFont(font1)
        sb_phone = wx.StaticBox(self.pnl, label="联系电话")
        sb_phone.SetFont(font1)
        sb_hospital = wx.StaticBox(self.pnl, label="医  院")
        sb_hospital.SetFont(font1)
        sb_department = wx.StaticBox(self.pnl, label="科  室")
        sb_department.SetFont(font1)
        sb_skill = wx.StaticBox(self.pnl, label="研究方向")
        sb_skill.SetFont(font1)
        sb_content = wx.StaticBox(self.pnl, label="节目内容")
        sb_content.SetFont(font1)
        sb_link = wx.StaticBox(self.pnl, label="节目链接")
        sb_link.SetFont(font1)

        # 创建水平方向box布局管理器
        hsbox_name = wx.StaticBoxSizer(sb_name, wx.HORIZONTAL)
        hsbox_phone = wx.StaticBoxSizer(sb_phone, wx.HORIZONTAL)
        hsbox_hospital = wx.StaticBoxSizer(sb_hospital, wx.HORIZONTAL)
        hsbox_department = wx.StaticBoxSizer(sb_department, wx.HORIZONTAL)
        hsbox_skill = wx.StaticBoxSizer(sb_skill, wx.HORIZONTAL)
        hsbox_content = wx.StaticBoxSizer(sb_content, wx.HORIZONTAL)
        hsbox_link = wx.StaticBoxSizer(sb_link, wx.HORIZONTAL)

        hsbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hsbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # 添加到hsbox布局管理器
        hsbox_name.Add(self.name, 0, wx.EXPAND | wx.TOP, 5)
        hsbox_phone.Add(self.phone, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox1.Add(hsbox_name, 0, wx.RIGHT | wx.TOP, 20)
        hsbox1.Add(hsbox_phone, 0, wx.LEFT | wx.TOP, 20)

        hsbox_hospital.Add(self.hospital, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox_department.Add(self.department, 0, wx.EXPAND | wx.BOTTOM, 5)
        hsbox2.Add(hsbox_hospital, 0, wx.RIGHT | wx.BOTTOM, 20)
        hsbox2.Add(hsbox_department, 0, wx.LEFT | wx.BOTTOM, 20)

        hsbox_skill.Add(self.skill, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_content.Add(self.content, 0, wx.EXPAND | wx.BOTTOM, 20)
        hsbox_link.Add(self.link, 0, wx.EXPAND | wx.BOTTOM, 20)
        #################################################################################
        # 添加到vsbox_show_operation布局管理器
        # self.vsbox_show_operation.Add(hsbox_name, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_phone, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox1, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox2, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        # self.vsbox_show_operation.Add(hsbox_hospital, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        # self.vsbox_show_operation.Add(hsbox_department, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(hsbox_skill, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_link, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        self.vsbox_show_operation.Add(hsbox_content, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)
        vs1 = wx.BoxSizer(wx.HORIZONTAL)
        vs1.Add(self.modify_affirm, 0, wx.RIGHT | wx.BOTTOM, 20)
        vs1.Add(self.nonmodify_affirm, 0, wx.LEFT | wx.BOTTOM, 20)
        self.vsbox_show_operation.Add(vs1, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 20)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.ModAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()

        elif source_id == 11:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.ModAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("添加操作！")
                add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                add_button.Show()
                self.Close(True)
            app.MainLoop()

        elif source_id == 12:
            pass
        elif source_id == 13:
            self.Close(True)
        elif source_id == 14:
            pass
        elif source_id == 15:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.ModAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家查询操作！")
                inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()

        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)

    def NonModAffirm(self, event):
        op = Sql_operation("login_users")
        stu_name = self.name.GetValue()
        print(stu_name)
        stu_hospital = self.hospital.GetValue()
        print(stu_hospital)
        stu_department = self.department.GetValue()
        print(stu_department)
        stu_skill = self.skill.GetValue()
        print(stu_skill)
        stu_content = self.content.GetValue()
        print(stu_content)
        stu_phone = self.phone.GetValue()
        print(stu_phone)
        stu_link = self.link.GetValue()
        print(stu_link)
        data=op.Find1(stu_name,stu_hospital,stu_department,stu_skill,stu_content,stu_phone,stu_link)
        print(len(data))
        if len(data) ==0:
            app = wx.App()
            font1 = wx.Font(15, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)
            dlg = wx.MessageDialog(None, '是否保存当前专家修改？', '提示', wx.YES_NO or wx.ICON_QUESTION)
            dlg.SetFont(font1)
            if dlg.ShowModal() == wx.ID_YES:
                print("yes")
                dlg.Destroy()
                self.ModAffirm(event)
            else:
                print("no")
                dlg.Destroy()
                print("专家列表")
                inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
                inquire_button.creategrid(1, inquire_button.getconut())
                inquire_button.show(1, inquire_button.getconut())
                inquire_button.Show()
                self.Close(True)
            app.MainLoop()
        else:
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)




    def ModAffirm(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")
        stu_name = self.name.GetValue()
        print(stu_name)
        stu_hospital = self.hospital.GetValue()
        print(stu_hospital)
        stu_department = self.department.GetValue()
        print(stu_department)
        stu_skill = self.skill.GetValue()
        print(stu_skill)
        stu_content = self.content.GetValue()
        print(stu_content)
        stu_phone = self.phone.GetValue()
        print(stu_phone)
        stu_link = self.link.GetValue()
        print(stu_link)
        np = op.Modify(int(self.mod_id), stu_name, stu_hospital, stu_department, stu_skill, stu_content, stu_phone,
                       stu_link)
        del_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
        del_button.creategrid(1, del_button.getconut())
        del_button.show(1, del_button.getconut())
        del_button.Show()
        self.Close(True)


# 继承UserOperation类，实现初始化操作界面
class DelOp(UserOperation):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(DelOp, self).__init__(*args, **kw)
        # 创建专家删除信息输入框、专家删除按钮
        self.del_id = wx.TextCtrl(self.pnl, pos=(407, 78), size=(210, 20))
        self.del_affirm = wx.Button(self.pnl, label="专家删除", pos=(620, 78), size=(80, 20))
        # 为专家删除按钮组件绑定事件处理
        self.del_affirm.Bind(wx.EVT_BUTTON, self.DelAffirm)
        #################################################################################
        # 创建静态框
        sb_del = wx.StaticBox(self.pnl, label="请选择需要专家删除的专家的id")
        # 创建水平方向box布局管理器
        hsbox_del = wx.StaticBoxSizer(sb_del, wx.HORIZONTAL)
        # 添加到hsbox_name布局管理器
        hsbox_del.Add(self.del_id, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 添加到vsbox_show_operation布局管理器
        self.vsbox_show_operation.Add(hsbox_del, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)
        self.vsbox_show_operation.Add(self.del_affirm, 0, wx.CENTER | wx.TOP | wx.FIXED_MINSIZE, 5)

    def ClickButton(self, event):
        source_id = event.GetId()
        if source_id == 10:
            print("专家列表！")
            inquire_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.creategrid(1, inquire_button.getconut())
            inquire_button.show(1, inquire_button.getconut())
            inquire_button.Show()
            self.Close(True)
        elif source_id == 11:
            print("添加操作！")
            add_button = AddOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            add_button.Show()
            self.Close(True)
        elif source_id == 12:
            pass
        elif source_id == 13:
            self.Close(True)
        elif source_id == 14:
            pass
        elif source_id == 15:
            print("专家查询操作！")
            inquire_button = InquireOp1(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
            inquire_button.Show()
            self.Close(True)
        elif source_id == 16:
            print("专家导出操作！")
            root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
            root.withdraw()  # 将Tkinter.Tk()实例隐藏
            fname = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("EXCEL", "xls")])
            filename1 = str(fname) + ".xls"
            op = Sql_operation("login_users")
            op.export('expert_info', filename1)
            print(filename1)

    def DelAffirm(self, event):
        # 连接login_users数据库
        op = Sql_operation("login_users")

        del_id = self.del_id.GetValue()
        print(del_id)
        np = op.Del(int(del_id))
        del_button = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
        del_button.creategrid(1, del_button.getconut())
        del_button.show(1, del_button.getconut())
        del_button.Show()
        self.Close(True)


if __name__ == '__main__':
    app = wx.App()
    login = UserLogin(None, title="中华医药专家名录检索数据库", size=(960, 700))
    login.Show()
    #operation = InquireOp(None, title="中华医药专家名录检索数据库", size=(1900, 1040))
    #operation.creategrid(1,operation.getconut())
    #operation.show(1,operation.getconut())
    #operation.Show()
    app.MainLoop()
