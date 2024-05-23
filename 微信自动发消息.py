from time import sleep
from tkinter import Tk, Entry, Button, Label, mainloop, messagebox
from uiautomation import WindowControl, SendKeys, Click, MoveTo, WheelDown

wx = WindowControl(searchDepth=1, Name="微信")

def image():
    times_contain = int(times.get())
    wx.SwitchToThisWindow()
    SendKeys("{Alt}e", waitTime=0)
    a1 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[2].GetChildren()[2].BoundingRectangle
    Click(a1.xcenter(), a1.ycenter(), waitTime=0)
    a2 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].BoundingRectangle
    Click(a2.xcenter(), a2.ycenter(), waitTime=0)

    for i in range(times_contain - 1):
        SendKeys("{Alt}e", waitTime=0)
        Click(a2.xcenter(), a2.ycenter(), waitTime=0)
        try:
            a2 = wx.GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[0].GetChildren()[1].BoundingRectangle
            Click(a2.xcenter(), a2.ycenter(), waitTime=0)
        except IndexError:
            pass


def send():
    try:
        times_contain = times.get()
        message_contain = message.get()
        name_contain = name.get()
        if not message_contain or not times_contain:
            messagebox.showerror("警告", "信息或次数为空")
            return 0
        else:
            times_contain = int(times_contain)
    except ValueError:
        messagebox.showerror("警告", "次数形式错误")
        return 0
    edit = wx.EditControl(Name=name_contain)
    edit_rect = edit.BoundingRectangle
    Click(edit_rect.xcenter(), edit_rect.ycenter())
    for i in range(times_contain):
        SendKeys(message_contain, waitTime=0)
        SendKeys("{Alt}s", waitTime=0)


def dialogue(tool, a1=True):
    name_contain = name.get()
    wx.SwitchToThisWindow()
    wx.MoveToCenter()
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


top = Tk()
top.title("WeChatTool")
top.geometry("500x200")

Label(top, text="名字:", font=("times", 10)).grid(row=0, column=0)
name = Entry(top, width=20)
name.grid(row=0, column=1, padx=10)

Label(top, text="次数:", font=("times", 10)).grid(row=0, column=2)
times = Entry(top, width=20)
times.grid(row=0, column=3, padx=10)

Label(top, text="信息:", font=("times", 10)).grid(row=1, column=0, pady=20)
message = Entry(top, width=20)
message.grid(row=1, column=1, padx=10, pady=20)
Button(top, text="执行发送信息", font=("times", 10), command=lambda: dialogue(send)).grid(row=1, column=2)

Label(top, text="表情包: (将想发的表情放在前面)", font=("times", 10)).grid(sticky="w", row=2, column=0, pady=(0, 20), columnspan=2)
Button(top, text="执行发送表情包", font=("times", 10), command=lambda: dialogue(image)).grid(row=2, column=2, pady=(0, 20))

mainloop()


