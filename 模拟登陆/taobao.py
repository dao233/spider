from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://login.taobao.com/'
USER = ''
PASSWORD = ''
chrome_options = Options()  #设置
#chrome_options.add_argument('--headless')  #浏览器不提供可视化界面
chrome_options.add_argument('--disable-gpu')  #规避bug

# 设置开发者模式启动，该模式下webdriver属性为正常值   一般反爬比较好的网址都会根据这个反爬
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(chrome_options=chrome_options)  #配置设置
wait = WebDriverWait(driver, 10)  #超时时长为10s
driver.get(URL)  #请求网址

#选择密码登录
login_click = wait.until(EC.presence_of_element_located((By.XPATH, '//i[@class="iconfont static"]')))
login_click.click()

#选择微博登录
weibo_click = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="weibo-login"]')))
weibo_click.click()

#等待微博账号输入框出现
weibo_user = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
weibo_user.send_keys(USER)

#等待微博密码输入框出现
weibo_pwd = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
weibo_pwd.send_keys(PASSWORD)

#等待登录按钮出现
submit = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
submit.click()

#在搜索框中输入搜索关键字
search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="q"]')))
search_input.send_keys('美食')

#driver.close()