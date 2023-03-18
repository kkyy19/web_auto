#启动文件
from test_function import web_test #导入函数文件
from test_data import test_data #导入数据文件
from selenium import webdriver
driver = webdriver.Chrome()
driver.implicitly_wait(10)
#调用函数
#取参数
url = test_data.url["url"] #取网址
user = test_data.login_data["username"] #取用户名
pwd = test_data.login_data["password"] #取密码
s_key = test_data.s_key["s_key"] #取搜索关键字
#传参到函数调用里
result = web_test.search_key(driver=driver, url=url, username=user, password=pwd, s_key=s_key)
if s_key in result:
    print("搜索结果是正确的")
else:
    print("测试用例不通过")