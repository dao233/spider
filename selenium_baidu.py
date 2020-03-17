from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import random

def get_track(distance):
    """
    利用加速度公式构建滑动路径
    :param distance: 滑动距离
    :return:
    """
    tracks = []
    current = 0
    mid = distance * 3 / 4
    t = random.randint(20, 40) * 0.01
    v = 0
    while current < distance:
        a = 10 if current < mid else -20
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        tracks.append(round(move))
    return tracks

def move_to_right(button, driver, distance):
    """
    移动滑块到最右
    :param button: 滑动按钮
    :param driver: selenium驱动
    :param distance: 滑动距离
    :return:
    """
    tracks = get_track(distance)
    print("验证码移动轨迹：{msg}".format(msg=tracks.__repr__() + 'moving...'))
    action = ActionChains(driver)
    action.click_and_hold(button).perform()     # 模拟按下
    begin = button.location['x']

    for x in tracks:
        try:
            action.move_by_offset(xoffset=x, yoffset=0).perform()       # 模拟移动

            driver.switch_to.parent_frame()
            now = button.location['x'] - begin
            process = round((now / distance) * 100, 2)
            print('当前验证码进度：{process}%'.format(process=process))
        except selenium_error.StaleElementReferenceException:
            break
    process = 100.00
    print('当前验证码进度：{process}%'.format(process=process))
    time.sleep(3)

def handle_roboot_check():

    btn_id = driver.find_element_by_class_name('vcode-slide-button').get_attribute('id')
    btn = driver.find_element_by_id(btn_id)
    distance = driver.find_element_by_class_name('vcode-slide-bottom').size['width'] - btn.size['width'] + random.randint(0, 4)
    move_to_right(btn, driver, distance)
    print(driver.page_source)


chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.baidu.com/s?wd=python&pn=60")
print(driver.page_source)
if len(driver.page_source):
    handle_roboot_check()
    print(driver.page_source)


