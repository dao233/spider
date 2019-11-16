from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

URL = 'https://www.zhihu.com/signin'
USER = ''
PASSWORD = ''
chrome_options = Options()  #设置
#chrome_options.add_argument('--headless')  #浏览器不提供可视化界面
chrome_options.add_argument('--disable-gpu')  #规避bug


# 设置开发者模式启动，该模式下webdriver属性为正常值   一般反爬比较好的网址都会根据这个反爬
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()  #全屏打开浏览器
wait = WebDriverWait(driver, 10) #超时时长为10s

driver.get(URL)

#转到密码登录
change = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="SignFlow-tab"]')))
change.click()
# 等待知乎账号输入框出现
zhihu_user = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
zhihu_user.click()
time.sleep(1)
zhihu_user.send_keys(USER)

# 等待知乎密码输入框出现
zhihu_pwd = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
zhihu_pwd.click()
zhihu_pwd.send_keys(PASSWORD)

time.sleep(1.5)
#直接点击登录按钮
ActionChains(driver).move_by_offset(930, 500).click().perform() # 鼠标左键点击， 200为x坐标， 100为y坐标

#driver.close()



