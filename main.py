from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from time import sleep
import re
from playsound import playsound

def auto_class(student_id=None , password=None, driver=None, send_message=False, *args, **kwargs):
    '''
    download driver:
    https://selenium-python.readthedocs.io/installation.html#drivers
    
    '''
    if student_id is None or password is None:
        raise AttributeError('شماره دانشجویی و رمزعبور خود را به برنامه بدهید')
    
    if driver is None:
        raise AttributeError('برنامه نیازمند درایور است از فانکشن های این برنامه میتوانید استفاده کنید')
        
    while True:
        try:
            driver = driver
            
            url = 'https://iau-tnb.daan.ir/'
            driver.get(url)
            assert 'دان |جلسات مجازی' in driver.title
            break
        except WebDriverException:
            print('!انگار اینترنت مشکل داره')
            sleep(15)
            print('...تلاش مجدد')
            continue
    
    # دکمه ورود
    driver.find_element(By.XPATH,'//a[@class="btn btn-primary loginBtn col-lg-4 col-sm-12 col-xs-12"]').click()
    
    # شماره دانشجویی
    driver.find_element(By.XPATH,'//input[@name="identification_number"]').send_keys(student_id)
    # رمز عبور
    driver.find_element(By.XPATH,'//input[@name="password"]').send_keys(password)
    
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'//button[@style="font-size: 14px; font-weight: bold"]').click()
    
    # جلسات
    driver.find_element(By.XPATH,'//a[@href=" https://iau-tnb.daan.ir/session-list"]').click()
    
    # پیدا کردن دکمه ورود به جلسه 
    while True:
        try:
            driver.find_element(By.XPATH,"//*[contains(text(),'ورود دانشجو')]").click()
            # چک کردن استاد هنوز وارد نشده وجود داره یا نه
            try :
                driver.find_element(By.XPATH,"//*[contains(text(),'استاد هنوز به جلسه وارد نشده است یا جلسه پایان یافته است.')]")
                print('استاد هنوز وارد کلاس نشده')
                print('تلاش در 30 ثانیه دیگر')
                sleep(30)
                print('تلاش محدد')
                continue
            except NoSuchElementException:    
                break
        except NoSuchElementException:
            print('هیچ کلاس فعالی پیدا نشد یا زمان کلاس هنوز نرسیده')
            print('تلاش مجدد در یک دقیقه دیگر')
            sleep(60)
            continue
    
    # دکمه زدن پخش صدا
    if send_message:
        sleep(5)
        # تایپ کردن سلام استاد
        driver.find_element(By.XPATH,'//textarea[@placeholder="ارسال پیام به گفتگوی عمومی"]').send_keys('سلام استاد')
        # ارسال پیام
        driver.find_element(By.XPATH,'//button[@aria-label="ارسال پیام"]').click()
    
    
    # گرفتن پیام ها
    sleep(8)
    # last_msg = ''
    last_person = ''
    
    end_msg_count = 0
    # repeat_msg = 0
    
    while True:
        js_codes = '''
        let btn = document.getElementsByClassName("button--Z2dosza sm--Q7ujg primary--1IbqAO unreadButton--ZSwgJG")[0]
        if (typeof btn !== "undefined") {
            btn.click()
        }
        
        const person_name = document.querySelectorAll('.name--ZfTXko span')
        if (typeof person_name !== "undefined") {
            console.log('name')
            const messages = document.getElementsByClassName("message--CeFIW")
            const msg = messages[messages.length - 1]
            console.log('msg')
            
            const person = person_name[person_name.length - 1]
            console.log(person.textContent)
            console.log('end')
            const result = {'name':person.textContent,'msg':msg.textContent}
            return result
        }
        '''
        msg = driver.execute_script(js_codes)
        # del print(msg['msg'],'--',msg['name'])
        
        # چک خسته نباشید
        # و ارسال خسته نباشید 
        # برای غیرفعال کردن خسته نباشید به 
        # kwargs = {'bye_msg': False} 
        try:
            bye_msg = kwargs['bye_msg']
        except KeyError:
            # default if its none
            bye_msg = True
            
        if bye_msg:
            regex = r'.*(خسته نباشید)'
            check = re.findall(msg['msg'],regex)
            if check :
                if msg['name'] != last_person:
                    end_msg_count += 1
                    if end_msg_count == 3 :
                        # اگر بیشتر از 3 تا خسته نباشید از سه فرد متفاوت بود 
                        # بنویس خسته نباشید و خارج شو
                        driver.find_element(By.XPATH,'//textarea[@placeholder="ارسال پیام به گفتگوی عمومی"]').send_keys('خسته نباشید')
                        driver.find_element(By.XPATH,'//button[@aria-label="ارسال پیام"]').click()
                        
                        sleep(5)
                        print('به نظر کلاس داره به پایان میرسه')
                        playsound('Windows_Xp__Turn_Off.mp3')
                        
                        # driver.quit()
                        
                last_person = msg['name']    
                
        sleep(0.5)
        

def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def firefox_driver():
    options = webdriver.FirefoxOptions()
    options.add_experimental_option("detach", True)
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    return webdriver.Firefox(options=options)


# auto_class(student_id, password, driver=chrome_driver() , send_message=False, kwargs={'bye_msg': False} )
