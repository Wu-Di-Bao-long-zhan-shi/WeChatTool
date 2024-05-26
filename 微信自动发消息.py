from os import startfile
from time import sleep
from tkinter import Tk, Label, mainloop, messagebox, Toplevel, ttk, BooleanVar
from uiautomation import WindowControl, SendKeys, Click, MoveTo, WheelDown
# 导入用的包

wx = WindowControl(searchDepth=1, Name="微信") # 寻找微信窗口
top = Tk()  # 创建程序
top.title("WeChatTool")  # 设置程序名字
top.geometry("500x200")  # 设置程序大小

def OpenWeChat():  # 按钮——打开微信
    startfile(r"C:\Program Files\Tencent\WeChat\WeChat.exe")

class setting:  # 类——程序设置窗口
    def __init__(self):
        self.calculator_bool = BooleanVar()  # 计数器是否启用，默认否
        self.picture_time_interval = 0.0  # 图片发送间隔
        self.information_intervals = 0.0  # 信息发送间隔
        self.start_counter_value = 1  # 计数器开始数字


    def change(self):  # 函数——创建窗口
        def sure():  # 按钮——确定
            try:
                self.picture_time_interval = float(image_s.get())
                self.information_intervals = float(message_s.get())
                self.start_counter_value = int(counter_s.get())
            except ValueError:  # 如果出现ValueError错误，弹出提示框
                messagebox.showerror("错误", "格式不对")
                return 0  # 返回0，避免执行下面代码
            set_w.destroy()

        def default():  # 按钮——默认
            for i in list(locals()):  # 列表化的原因——遍历字典时不能修改值
                if i != "self":  # self是多选框，不能正常删除
                    eval(f"{i}.delete(0, 'end')")  # 清空文本框

            counter_s.insert(0, "1")  # 分别插入1，0.0，0.0
            image_s.insert(0, "0.0")
            message_s.insert(0, "0.0")
            self.calculator_bool.set(False)  # 给多选框设置为否

        set_w = Toplevel(top)  # 创建设置窗口
        set_w.title("设置")
        set_w.geometry("500x500")

        Label(set_w, text="图片时间间隔(单位秒):", font=("times", 10)).grid()
        image_s = ttk.Entry(set_w)
        image_s.grid(row=0, column=1, columnspan=3, sticky="w")

        Label(set_w, text="信息时间间隔(单位秒):", font=("times", 10)).grid(row=1, column=0, pady=20)
        message_s = ttk.Entry(set_w)
        message_s.grid(row=1, column=1, pady=20, columnspan=3, sticky="w")

        Label(set_w, text="计数器(加在信息末尾):", font=("times", 10)).grid(row=2, column=0, sticky="w")
        Label(set_w, text="从", font=("times", 10)).grid(row=2, column=1, sticky="w", padx=(0, 75))
        counter_s = ttk.Entry(set_w, width=10)
        counter_s.grid(row=2, column=1, sticky="e")
        Label(set_w, text="开始", font=("times", 10)).grid(row=2, column=2, sticky="w")

        counter_b = ttk.Checkbutton(set_w, text="是否启用", variable=self.calculator_bool)
        counter_b.grid(row=2, column=3)

        counter_s.insert(0, str(self.start_counter_value))
        image_s.insert(0, str(self.picture_time_interval))
        message_s.insert(0, str(self.information_intervals))

        ttk.Button(set_w, text="确定", command=sure).grid(sticky="w", row=20, column=0)
        ttk.Button(set_w, text="默认", command=default).grid(row=20, column=1)



def image():  # 发送图片
    times_contain = int(times.get())  # 获取文本框里的内容，并转换格式
    wx.SwitchToThisWindow()  # 置顶窗口
    SendKeys("{Alt}e", interval=0,  waitTime=setting.picture_time_interval)  # 每个字符之间间隔0，发送之间间隔0
    a1 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[2].GetChildren()[2].BoundingRectangle  # 点击表情的“添加的单个表情”
    Click(a1.xcenter(), a1.ycenter(), waitTime=0)
    a2 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].BoundingRectangle  # 点击第一个表情
    Click(a2.xcenter(), a2.ycenter(), waitTime=0)

    for i in range(times_contain - 1):  # 进入循环（已经执行一次，所以-1）
        SendKeys("{Alt}e", interval=0, waitTime=setting.picture_time_interval)
        Click(a2.xcenter(), a2.ycenter(), waitTime=0)
        try:  # 如果点击未成功，获取在点击（报错为点击成功，因为窗口已关闭）
            a2 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].BoundingRectangle
            Click(a2.xcenter(), a2.ycenter(), waitTime=0)
        except IndexError:
            pass


def send():
    try:  # 获取值
        times_contain = times.get()
        message_contain = message.get()
        name_contain = name.get()
        if not times_contain:  # 如果信息或次数为空，弹出窗口
            messagebox.showerror("错误", "次数为空")
            return 0  # 停止执行下面代码
        else:  # 不是的话，转化次数格式
            times_contain = int(times_contain)
    except ValueError:  # 如果报错，则次数格式错误
        messagebox.showerror("错误", "次数形式错误")
        return 0
    edit = wx.EditControl(Name=name_contain)  # 获取微信文本框和rect，并点击
    edit_rect = edit.BoundingRectangle
    Click(edit_rect.xcenter(), edit_rect.ycenter())

    if not setting.calculator_bool.get():  # 如果计数器为否执行
        if not message_contain:
            messagebox.showerror("错误", "信息为空")
        for i in range(times_contain):
            SendKeys(message_contain, interval=0, waitTime=setting.information_intervals)
            SendKeys("{Alt}s", waitTime=0)
    else: # 不是的话执行
        num = setting.start_counter_value
        for i in range(times_contain):
            SendKeys(message_contain + str(num), waitTime=setting.information_intervals)
            SendKeys("{Alt}s", interval=0, waitTime=setting.information_intervals)
            num += 1


def dialogue(tool, a1=True):  # 该函数用于定位聊天栏
    name_contain = name.get()  # 获取名字
    wx.SwitchToThisWindow()  # 置顶窗口
    wx.MoveToCenter()  # 移动到中心
    group = wx.ListControl(8, Name="会话")
    group_rect = group.BoundingRectangle
    if a1:
        Click(group_rect.left + group_rect.width() - 5, group_rect.top)


    for item in group.GetChildren():
        if item.Name == name_contain:
            item_rect = item.BoundingRectangle
            Click(item_rect.xcenter(), item_rect.ycenter())
            tool()

    if name_contain not in [i.Name for i in group.GetChildren()]:
        bottom = group.GetChildren()[-1].Name
        MoveTo(group_rect.xcenter(), group_rect.ycenter(), 100)
        WheelDown(20, 0, 0)
        sleep(0.5)
        group = wx.ListControl(8, Name="会话")
        if group.GetChildren()[-1].Name != bottom:
            dialogue(tool, a1=False)
        else:
            messagebox.showwarning("警告", "未找到聊天")
            return 0


# 创建类——设置
setting = setting()

# 编写窗口内容
Label(top, text="名字:", font=("times", 10)).grid(row=0, column=0)
name = ttk.Entry(top, width=20)
name.grid(row=0, column=1, padx=10)

Label(top, text="次数:", font=("times", 10)).grid(row=0, column=2)
times = ttk.Entry(top, width=20)
times.grid(row=0, column=3, padx=10)

Label(top, text="信息:", font=("times", 10)).grid(row=1, column=0, pady=20)
message = ttk.Entry(top, width=20)
message.grid(row=1, column=1, padx=10, pady=20)
ttk.Button(top, text="执行发送信息", command=lambda: dialogue(send)).grid(row=1, column=2)

Label(top, text="表情包: (将想发的表情放在前面)", font=("times", 10)).grid(sticky="w", row=2, column=0, pady=(0, 20), columnspan=3)
ttk.Button(top, text="执行发送表情包", command=lambda: dialogue(image)).grid(row=2, column=2, pady=(0, 20))

ttk.Button(top, text="打开微信", command=OpenWeChat).grid(sticky="e", row=4, column=1)

ttk.Button(top, text="更多设置", command=setting.change).grid(sticky="w", row=4, column=0, columnspan=2)


mainloop()


