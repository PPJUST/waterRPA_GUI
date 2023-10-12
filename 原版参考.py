import pyautogui
import time
import xlrd
import pyperclip
import time
import os


#定义鼠标事件

#pyautogui库其他用法 https://blog.csdn.net/qingfengxd1/article/details/108270159

def mouseClick(clickTimes,lOrR,img,reTry):
    if reTry == 1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                break
            print("未找到匹配图片,0.1秒后重试")
            time.sleep(0.1)
    elif reTry == -1:
        while True:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
            location=pyautogui.locateCenterOnScreen(img,confidence=0.9)
            if location is not None:
                pyautogui.click(location.x,location.y,clicks=clickTimes,interval=0.2,duration=0.2,button=lOrR)
                print("重复")
                i += 1
            time.sleep(0.1)


#定义热键事件

#hotkey_get方法用来判断热键组合个数,还是文字输入。此方法由B站up主 尔茄无双 提供。
def hotkey_get(hk_g_inputValue):
    try:
        newinput = hk_g_inputValue.split(',')
        pyautogui.hotkey(*tuple(newinput))
    except:
        pyperclip.copy(hk_g_inputValue)
        pyautogui.hotkey('ctrl', 'v')

#hotkey_get方法用来判断热键组合个数，并把热键传到对应的变量上newinput[0],[1],[2],[3]……[9]只写了10个后续可以添加。【老方法弃用】
    # newinput = hk_g_inputValue.split(',')
    #         if len(newinput)==1: 
    #        			 pyautogui.hotkey(hk_g_inputValue)
    #         elif len(newinput)==2:
    #        			 pyautogui.hotkey(newinput[0],newinput[1])
    #         elif len(newinput)==3:
    #        			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2])
    #         elif len(newinput)==4:
    #        			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3])
    #         elif len(newinput)==4:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3])
    #         elif len(newinput)==5:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4])
    #         elif len(newinput)==6:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4],newinput[5])
    #         elif len(newinput)==7:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4],newinput[5],newinput[6])       
    #         elif len(newinput)==8:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4],newinput[5],newinput[6],newinput[7])     
    #         elif len(newinput)==9:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4],newinput[5],newinput[6],newinput[7],newinput[8])
    #         elif len(newinput)==10:
    #            			 pyautogui.hotkey(newinput[0],newinput[1],newinput[2],newinput[3],newinput[4],newinput[5],newinput[6],newinput[7],newinput[8],newinput[9])   
                                                                                                                                                         
#hotkey_Group方法调用hotkey_get方法，并判断其热键内容是否需要循环。
def hotkeyGroup(reTry,hkg_inputValue):
    if reTry == 1:
            hotkey_get(hkg_inputValue)                  
            print("执行了：",hkg_inputValue)
            time.sleep(0.1)
    elif reTry == -1:
        while True:
            hotkey_get(hkg_inputValue)
            print("执行了：",hkg_inputValue)
            time.sleep(0.1)
    elif reTry > 1:
        i = 1
        while i < reTry + 1:
                hotkey_get(hkg_inputValue)
                print("执行了：",hkg_inputValue)
                i += 1
                time.sleep(0.1)



# 数据检查
# cmdType.value  1.0 左键单击    2.0 左键双击  3.0 右键单击  4.0 输入  5.0 等待  6.0 滚轮  
# 7.0 热键组合（最多4个）
# 8.0 粘贴当前时间
# 9.0 系统命令集
# ctype     空：0
#           字符串：1
#           数字：2
#           日期：3
#           布尔：4
#           error：5
def dataCheck(sheet1):
    checkCmd = True
    #行数检查
    if sheet1.nrows<2:
        print("没数据啊哥")
        checkCmd = False
    #每行数据检查
    i = 1
    while i < sheet1.nrows:
        # 第1列 操作类型检查
        cmdType = sheet1.row(i)[0]
        if cmdType.ctype != 2 or (cmdType.value != 1.0 and cmdType.value != 2.0 and cmdType.value != 3.0 
        and cmdType.value != 4.0 and cmdType.value != 5.0 and cmdType.value != 6.0 
        and cmdType.value != 7.0 and cmdType.value != 8.0 and cmdType.value != 9.0):
            print('第',i+1,"行,第1列数据有毛病")
            checkCmd = False
        # 第2列 内容检查
        cmdValue = sheet1.row(i)[1]
        # 读图点击类型指令，内容必须为字符串类型
        if cmdType.value ==1.0 or cmdType.value == 2.0 or cmdType.value == 3.0:
            if cmdValue.ctype != 1:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 输入类型，内容不能为空
        if cmdType.value == 4.0:
            if cmdValue.ctype == 0:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 等待类型，内容必须为数字
        if cmdType.value == 5.0:
            if cmdValue.ctype != 2:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 滚轮事件，内容必须为数字
        if cmdType.value == 6.0:
            if cmdValue.ctype != 2:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 7.0 热键组合，内容不能为空
        if cmdType.value == 7.0:
            if cmdValue.ctype == 0:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 8.0 时间，内容不能为空
        if cmdType.value == 8.0:
            if cmdValue.ctype == 0:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        # 9.0 系统命令集模式，内容不能为空
        if cmdType.value == 9.0:
            if cmdValue.ctype == 0:
                print('第',i+1,"行,第2列数据有毛病")
                checkCmd = False
        i += 1
    return checkCmd

#任务
def mainWork(img):
    i = 1
    while i < sheet1.nrows:
        #取本行指令的操作类型
        cmdType = sheet1.row(i)[0]
        if cmdType.value == 1.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1,"left",img,reTry)
            print("单击左键",img)
        #2代表双击左键
        elif cmdType.value == 2.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(2,"left",img,reTry)
            print("双击左键",img)
        #3代表右键
        elif cmdType.value == 3.0:
            #取图片名称
            img = sheet1.row(i)[1].value
            #取重试次数
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            mouseClick(1,"right",img,reTry)
            print("右键",img) 
        #4代表输入
        elif cmdType.value == 4.0:
            inputValue = sheet1.row(i)[1].value
            pyperclip.copy(inputValue)
            pyautogui.hotkey('ctrl','v')
            print("输入:",inputValue) 
            time.sleep(0.5)                                       
        #5代表等待
        elif cmdType.value == 5.0:
            #取图片名称
            waitTime = sheet1.row(i)[1].value
            time.sleep(waitTime)
            print("等待",waitTime,"秒")
        #6代表滚轮
        elif cmdType.value == 6.0:
            #取图片名称
            scroll = sheet1.row(i)[1].value
            pyautogui.scroll(int(scroll))
            print("滚轮滑动",int(scroll),"距离")     
       #7代表_热键组合
        elif cmdType.value == 7.0:
            #取重试次数,并循环。
            reTry = 1
            if sheet1.row(i)[2].ctype == 2 and sheet1.row(i)[2].value != 0:
                reTry = sheet1.row(i)[2].value
            inputValue = sheet1.row(i)[1].value
            hotkeyGroup(reTry,inputValue)
            time.sleep(0.5)
       #8代表_粘贴当前时间
        elif cmdType.value == 8.0:      
            #设置本机当前时间。
            localtime = time.strftime("%Y-%m-%d %H：%M：%S", time.localtime()) 
            pyperclip.copy(localtime)
            pyautogui.hotkey('ctrl','v')
            print("粘贴了本机时间:",localtime)
            time.sleep(0.5)
       #9代表_系统命令集模式
        elif cmdType.value == 9.0:      
            wincmd = sheet1.row(i)[1].value
            os.system(wincmd)
            print("运行系统命令:",wincmd)
            time.sleep(0.5) 
        i += 1

#主程序
while True:
    if __name__ == '__main__':
        file = 'cmd.xls'
        #打开文件
        wb = xlrd.open_workbook(filename=file)
        #通过索引获取表格sheet页
        sheet1 = wb.sheet_by_index(0)
        print('欢迎使用不高兴就喝水牌RPA~')
        print('大羽改良版_v211207')
        print('')
        #避免多次循环导致的ctrl+v导入到，按ESC进行取消。
        pyautogui.hotkey('esc')
        #数据检查
        checkCmd = dataCheck(sheet1)

        #输入选项实现功能
        if checkCmd:
            key=input('选择功能: 1.做一次 2.循环几次 3.循环到死 0.退出程序\n特殊功能：c.清理屏幕显示\n———————————————————————————————————————\n')
            if key=='1':
                #循环拿出每一行指令 
                print("正在执行第1次命令")  
                print("")
                mainWork(sheet1)
                print("")
                print("已经完成第1次命令")  
                print("——————————————————分割线——————————————————")  
                print("")

            elif key=='2':
                print("")
                count=0
                times=input('输入需要循环的次数，务必输入正整数。\n')
                times=int(times)
                if count < times:
                    while count < times:
                            count+=1 
                            print("正在执行第",count,"次","命令")
                            print("")
                            mainWork(sheet1)
                            time.sleep(0.1)
                            print("等待0.1秒") 
                            print("") 
                            print("已经完成第",count,"次","命令") 
                            print("——————————————————分割线——————————————————")  
                            print("") 
                else:
                    print('输入有误或者已经退出!')
                    os.system('pause')
                    print("") 
                    print("——————————————————————————————————————————")  

            elif key=='3':
                count=0
                while True:
                    count+=1
                    print("正在执行第",count,"次","命令")
                    print("")
                    mainWork(sheet1)
                    time.sleep(0.1)
                    print("等待0.1秒")  
                    print("")
                    print("已经完成第",count,"次","命令")  
                    print("——————————————————分割线——————————————————")  
                    print("")  

            elif key=='0':
                print("正清理缓存文件...")
                os.system('@echo off & for /d %i in (%temp%\^_MEI*) do (rd /s /q "%i")>nul')
                exit("正在退出程序...")
                
            elif key=='c':
                os.system('cls')
                
            else:
                print('输入有误或者已经退出!')
                os.system('pause')
                print("") 
                print("——————————————————————————————————————————")  