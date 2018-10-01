from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
base_url = "https://www.zhihuishu.com/"
browser = webdriver.Chrome(executable_path='chromedriver.exe')
browser.get(base_url)
wait = WebDriverWait(browser,10)


def login(username,password):
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#login-register > li:nth-child(1) > a'))).click()
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#lUsername')))
        username_input.send_keys(username)
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lPassword')))
        password_input.send_keys(password)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#f_sign_up > div > span'))).click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#myBody > div.mainBox.clearfix > div.schoolLeft.fl > div.userInfoBox > div.identitySelBox.clearfix > span'),'这里是学生端'))
        print('登录%s成功！' % username)
        study()
    except NoSuchElementException as msg:
        print('查找元素异常%s'%msg)

def study():
    login_windows = browser.current_window_handle
    try:
        study_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#course_recruit_studying_ul > li.Stu_courseFocusItem.courseListOn > div.new_stuCurseInfoBox.fr > div.promoteSchedule.mt15.clearfix > a')))
        study_button.click()

        all_handles = browser.window_handles
        for handle in all_handles:
            if handle != login_windows:
                browser.close()
                browser.switch_to.window(handle)

        time.sleep(2)
        cancel()

    except NoSuchElementException as msg:
        print('查找元素异常%s'%msg)

def cancel():
    while True:
        try:
            browser.find_element_by_class_name('popbtn_yes').click()
            time.sleep(2)
            browser.find_element_by_class_name('popup_delete').click()
            time.sleep(10)
            speed_voice_config()
        except Exception:
            time.sleep(2)
            try:
                browser.find_element_by_class_name('popboxes_close').click()
                print('成功跳过题目测试')
            except  Exception:
                pass
            get_time()
            pass

a = []
b = 0
def get_time():
    global b
    content = browser.find_element_by_class_name('progressbar')
    reselt = content.get_attribute('style')
    title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#lessonOrder'))).text
    time.sleep(3)
    if reselt:
        if len(a) < 3:
            a.append(reselt)
            if len(a) > 1:
                if a[1] != a[0]:
                    a.remove(a[0])
                    print(title,' - ',str(reselt).replace('width', '正在播放'))
                    b = 0
                elif a[1] == a[0]:
                    a.remove(a[0])
                    b +=1
                    print('正在尝试第%s次,重新连接'%b)
                    if b == 5:
                        print('第%s次重新连接失败，小C开始刷新'%b)
                        browser.refresh()
                        time.sleep(10)
                        speed_voice_config()
                        b = 0



    if reselt == 'width: 100%;':
        try:
            browser.find_element_by_class_name('next_lesson_bg').click()
            print('进行下一节课')
            time.sleep(5)
            speed_voice_config()
        except Exception:
            print('似乎已经撸完所有视频啦~小C就告退了~')



def speed_voice_config():
    try:
        mouse = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea")))
        ActionChains(browser).move_to_element(mouse).perform()
        browser.find_element_by_xpath('//*[@id="vjs_mediaplayer"]/div[10]/div[8]/div[1]').click() #静音''
        time.sleep(1)
        print('嘘嘘~静音啦')
    except Exception:
        print('静音失败')
        speed_voice_config()
        pass

    time.sleep(2)
    try:
        mouse = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.videoArea.container")))
        ActionChains(browser).move_to_element(mouse).perform()
        mouse2 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#vjs_mediaplayer > div.controlsBar > div.speedBox")))
        ActionChains(browser).move_to_element(mouse2).perform()
        browser.find_element_by_xpath('//*[@id="vjs_mediaplayer"]/div[10]/div[5]/div/div[3]').click()  # 1.5倍速
        print('1.5倍速观看中~')
    except Exception:
        print('1.5倍启动失败，小C已经汇报原因')
        speed_voice_config()
        pass


def mian():
    print('=======这里是最不智能的小C智能看视频小程序=======')
    print('=(#^.^#)=')
    print('=======GO GO GO=======')
    username=input('username:')
    password=input('password:')
    if password:
        login(username,password)
    else:
        print('请输入密码！')


if __name__ == '__main__':
    mian()
