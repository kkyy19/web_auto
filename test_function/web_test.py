from selenium import webdriver #从selenium工具里导入webdriver库
from selenium.webdriver.common.by import By
import time


#option = webdriver.ChromeOptions()
#option.add_experimental_option("detach", True)
#driver_path = r"D:\anaconda3\envs\test37\chromedriver.exe"
#driver = webdriver.Chrome(executable_path=driver_path)

#driver = webdriver.Chrome()#选择Chrome浏览器，初始化driver，可以浏览器进行沟通，建立会话session
#driver.implicitly_wait(10) #隐式等待，默认等待10s
'''
#1、打开一个网址
driver.get("https://www.baidu.com") #打开一个网址http://120.78.128.25:8765
#2、浏览器窗口最大化
driver.maximize_window()
#3、打开新页面
time.sleep(3) #等待，默认为秒
driver.get("http://erp.lemfix.com")
#4、向前 退后 刷新页面
#time.sleep(2)
driver.back() #退回上一个页面
#time.sleep(2)
driver.forward() #前进到下一个页面
#time.sleep(2)
driver.refresh() #刷新页面
#5、退出
driver.quit() #关闭驱动，session关闭
#driver.close() #关闭当前窗口，不会退出会话

#以上是浏览器常规操作
'''


#非常规操作实现——元素定位（先了解前端页面，F12）
'''
web页面 == HTML + CSS + JavaScript
HTML：标签语言，<标签名> 值 </标签名>  ——呈现页面内容
CSS：页面布局设置，如字体颜色、字体大小样式
JavaScript：依据不同情形展示不同效果
'''
#元素的特征：根据页面设计规则，有些特征是唯一的
# id：类比身份证号——仅限于当前页面，username
# xpath: 绝对路径：/html/body/div/div/div[1]/a/b（从根节点开始）
# 找到元素后的操作：点击click，输入内容send_keys，获取文本text，获取属性attribute

'''
## 对测试用例进行测试
# 用例1、输入ERP地址
driver.get("http://erp.lemfix.com")

# 用例2 输入正确的用户和密码能正常登录
driver.find_element(by=By.ID, value="username").send_keys("test123") #找到了有username这个id的元素
driver.find_element(by=By.ID, value="password").send_keys("123456")
driver.find_element(by=By.ID, value="btnSubmit").click()
#driver.find_element(by=By.XPATH, value="//input[@id='username']").send_keys("test123") #相对路径

# 用例3、验证页面标题
#方法一
page_text =driver.find_element(by=By.XPATH, value="//div[@class='login-logo']//b").text #层级定位，找到这个元素的位置之后获取文本，并赋值
if page_text == "柠檬ERP":
    print("这个页面的标题是：{}".format(page_text))
else:
    print("这个测试用例不通过")
#方法二
page_title = driver.title #直接获取页面的标题
print("这个页面的标题是：{}".format(page_title))

# 用例4、判断正常登录，登录成功
#time.sleep(5) #强制等待5秒
login_user = driver.find_element(by=By.XPATH, value="//p[text()='测试用户']").text #获取到登录用例名
if login_user == "测试用户":
    print("这个登录的用户是：{}".format(login_user))
else:
    print("这个测试用例不通过")

#用例5、点击“零售出库”菜单能正常打开
driver.find_element(by=By.XPATH, value="//span[text()='零售出库']").click()

#用例6、搜索单据编号
#driver.find_element(by=By.ID, value="searchNumber").send_keys("248") #不能找到元素，原因：所在页面是子HTML页面，需要先切换iframe
#id = driver.find_element(by=By.XPATH, value="//iframe[@id='tabpanel-e1cc60a453-frame']") #不能找到，iframe的id是动态变化的
#driver.switch_to.frame('tabpanel-e1cc60a453-frame')
P_id = driver.find_element(by=By.XPATH, value="//div[text()='零售出库']/..").get_attribute("id") #通过找到“零售出库”元素获取其上级的ID属性
F_id = P_id + "-frame" #得到iframe的id
#方法一：通过id进行的iframe切换
#driver.switch_to.frame(F_id) #切换到子页面
#driver.find_element(by=By.ID, value="searchNumber").send_keys("248") #搜索单据编号
#方法二：通过元素定位得到的表达式xpath，进行iframe切换
#driver.switch_to.frame(driver.find_element(by=By.XPATH, value="//iframe[@id='{}']".format(F_id))) #找到iframe元素，再进行切换
#driver.find_element(by=By.ID, value="searchNumber").send_keys("248")
#方法三：通过iframe下标切换
driver.switch_to.frame(1)
driver.find_element(by=By.ID, value="searchNumber").send_keys("248")

driver.find_element(by=By.ID, value="searchBtn").click() #点击查询
time.sleep(1) #查询后页面可能没有加载完，强制睡眠1秒
num = driver.find_element(by=By.XPATH, value="//tr[@id='datagrid-row-r1-2-0']//td[@field='number']/div").text #输出单据编号
if "248" in num:
    print("搜索结果是正确的")
else:
    print("测试用例不通过")
'''


##封装函数
#将 打开网址 封装为函数
def open_url(url, driver):
    driver.get(url)
    driver.maximize_window()

#将 输入用户和密码 封装为函数
def login_page(username, password, driver):
    driver.find_element(by=By.ID, value="username").send_keys(username) #找到了有username这个id的元素
    driver.find_element(by=By.ID, value="password").send_keys(password)
    driver.find_element(by=By.ID, value="btnSubmit").click()

#将 搜索操作 封装为函数
def search_key(url, driver, username, password, s_key):
    open_url(url, driver)
    login_page(username, password, driver)
    driver.find_element(by=By.XPATH, value="//span[text()='零售出库']").click()
    P_id = driver.find_element(by=By.XPATH, value="//div[text()='零售出库']/..").get_attribute("id") #通过找到“零售出库”元素获取其上级的ID属性
    F_id = P_id + "-frame" #得到iframe的id
    driver.switch_to.frame(1)
    driver.find_element(by=By.ID, value="searchNumber").send_keys(s_key)
    driver.find_element(by=By.ID, value="searchBtn").click() #点击查询
    time.sleep(1) #查询后页面可能没有加载完，强制睡眠1秒
    num = driver.find_element(by=By.XPATH, value="//tr[@id='datagrid-row-r1-2-0']//td[@field='number']/div").text #输出单据编号
    return num















'''
作业：
1、完成任意整数序列的相加——生成一个整数序列，里面全是数字，求所有数字的和
def add_fun(num):
    sum = 0
    for i in range(num):
        sum += i
    print(sum)
或
num = int(input("input正数："))
for i in range(num):
    sum += i
print(sum)
    
    
2、定义函数：判断一个对象（列表、字典、字符串）的长度是否大于5，如果大于5，输出True，否则输出False
def function_len(object):
    if type(object) == dict or type(object) == list or type(object) == str:
    #if isinstance(object, str) or isinstance(object, list) or isinstance(object, dict): 
        length = len(object)
        if length >= 5:
            print("True")
        else:
            print("False")
    else:
        print("数据类型不能计算长度！")
'''






















