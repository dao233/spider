from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

URL = 'https://weibo.com'
USER = ''
PASSWORD = ''
chrome_options = Options()  #设置
#chrome_options.add_argument('--headless')  #浏览器不提供可视化界面
chrome_options.add_argument('--disable-gpu')  #规避bug

# 设置开发者模式启动，该模式下webdriver属性为正常值   一般反爬比较好的网址都会根据这个反爬
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(chrome_options=chrome_options)  #配置设置
driver.maximize_window()  #全屏打开浏览器
wait = WebDriverWait(driver, 10) #超时时长为10s

driver.get(URL)

# 等待微博账号输入框出现
weibo_user = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="loginname"]')))
weibo_user.click()  # 用来模拟手工点击一下再输入账号
time.sleep(0.5)  # 延时一下，速度太快好像会导致验证码的出现
weibo_user.send_keys(USER)  #输入账号

# 等待微博密码输入框出现
weibo_pwd = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="input_wrap"]/input[@name="password"]')))
weibo_pwd.send_keys(PASSWORD)

# 直接按坐标点击登录按钮
ActionChains(driver).move_by_offset(1360, 280).click().perform() # 鼠标左键点击

#driver.close()
