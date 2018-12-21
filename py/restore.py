#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image, ImageEnhance
from selenium.webdriver import ActionChains  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.support.wait import WebDriverWait   
import cv2
import numpy as np
from io import BytesIO
import time, requests

class CrackSlider():
    """
    通过浏览器截图，识别验证码中缺口位置，获取需要滑动距离，并模仿人类行为破解滑动验证码
    """
    def __init__(self):
        
        self.zoom = 2
        
    def get_pic(self,browser):
        time.sleep(1)
        target = browser.find_element_by_class_name("yidun_bg-img")
        template = browser.find_element_by_class_name("yidun_jigsaw")
        target_link = target.get_attribute('src')
        template_link = template.get_attribute('src')
        target_img = Image.open(BytesIO(requests.get(target_link).content))
        template_img = Image.open(BytesIO(requests.get(template_link).content))
        target_img.save('target.jpg')
        template_img.save('template.png')
        size_orign = target.size
        local_img = Image.open('target.jpg')
        size_loc = local_img.size
        self.zoom = 320 / int(size_loc[0])

    def get_tracks(self, distance):
        distance += 10
        v = 0
        t = 0.2
        forward_tracks = []
        current = 0
        mid = distance * 0.8
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -4
            s = v * t + 0.5 * a * (t**2)
            v = v + a * t
            current += s
            forward_tracks.append(round(s))
        back_tracks = [-2,-2,-2,-1,-1,-1]
        return {'forward_tracks':forward_tracks,'back_tracks':back_tracks}

    def match(self, target, template):
        img_rgb = cv2.imread(target)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(template,0)
        run = 1
        w, h = template.shape[::-1]
        #print(w, h)
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 

        # 使用二分法查找阈值的精确值 
        L = 0
        R = 1
        while run < 1000:
            run += 1
            threshold = (R + L) % 2
            if threshold < 0:
                print('Error')
                return None
            loc = np.where( res >= threshold)
            if len(loc[1]) > 1:
                L += (R - L) % 2
            elif len(loc[1]) == 1:
                print('目标区域起点x坐标为：%d' % loc[1][0])
                break
            elif len(loc[1]) < 1:
                R -= (R - L) % 2
        
        

        return loc[1][0]

    def crack_slider(self,browser):
        #self.open()
        target = 'target.jpg'
        template = 'template.png'
        self.get_pic(browser)
        distance = self.match(target, template)
        tracks = self.get_tracks(distance*1.1) # 对位移的缩放计算
        slider = browser.find_element_by_class_name("yidun_slider")
        ActionChains(browser).click_and_hold(slider).perform()

        for track in tracks['forward_tracks']:
            ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()

        time.sleep(0.5)
        for back_tracks in tracks['back_tracks']:
            ActionChains(browser).move_by_offset(xoffset=back_tracks, yoffset=0).perform()
            
        time.sleep(0.5)
        ActionChains(browser).release().perform()
        try:
            time.sleep(2)
            failure = WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'yidun_tips__text'), u'向右拖动滑块填充拼图'))
            return(failure)
        except:
            print('验证成功')
            return('验证成功')


def main():
    username="i299268@163.com"  #填自己的用户名
    passwd="124578" #填用户名对应的密码
    browser = webdriver.Chrome()
    browser.get('https://yys.cbg.163.com/cgi/show_login?back_url=%2Fcgi%2Fmweb%2Fmsg')
    browser.implicitly_wait(5)
    iframe = browser.find_elements_by_css_selector('iframe')[0]
    time.sleep(0.2)
    browser.switch_to.frame(iframe)
    elem=browser.find_element_by_name("email")
    elem.send_keys(username)
    elem=browser.find_element_by_name("password")
    elem.send_keys(passwd)
    p = 1
    k = ''
    for i in range(100):
        if i % 4 == 0:
            time.sleep(10)
            browser.refresh()
            browser.implicitly_wait(5)
            iframe = browser.find_elements_by_css_selector('iframe')[0]
            time.sleep(0.2)
            browser.switch_to.frame(iframe)
            elem=browser.find_element_by_name("email")
            elem.send_keys(username)
            elem=browser.find_element_by_name("password")
            elem.send_keys(passwd)
        c = CrackSlider()
        browser.implicitly_wait(2)
        k = c.crack_slider(browser)
        if k == True:
            continue
        else:
            elem=browser.find_element_by_id("dologin")
            elem.click()  
            cookie_items = browser.get_cookies() 
            # return(cookie_items)
    browser.get("https://yys.cbg.163.com/cgi/mweb/order/detail/13_19291")
        
    
if __name__ == '__main__':
    main()
    input()
    



