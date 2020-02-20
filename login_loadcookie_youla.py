import pickle
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import seller_or_not


def login():
    
    driver = webdriver.Firefox(executable_path=r'/home/pasha/Рабочий стол/AvitoParsing/Sel/geckodriver')
    driver.header_overrides = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'}
    driver.implicitly_wait(4)
    driver.get("https://youla.ru/login")
    driver.find_element_by_xpath("//*[contains(text(), 'По номеру телефона')]").click()
    driver.implicitly_wait(4)

    driver.find_element_by_xpath("//input[@class='form_control--simple form_control']").send_keys('9179179419')
    driver.implicitly_wait(4)

    driver.find_element_by_xpath("//*[contains(text(), 'Получить код для входа')]").click()
    driver.implicitly_wait(4)
    code=str(input('Введи код:' ))
    driver.find_element_by_xpath("//input[@class='sc-kTUwUJ kifSgu']").send_keys(code)
    driver.implicitly_wait(4)
    driver.find_element_by_xpath("//span[@class='sc-cJSrbW iElBmz']").click()
    time.sleep(30)
    save_cookies(driver, 'cookies.txt')
    time.sleep(20)
    driver.quit()





def save_cookies(driver, location):

    pickle.dump(driver.get_cookies(), open(location, "wb"))


def load_cookies(driver, location, url='https://youla.ru/mvb,v,bv,vb,bvvb,bvv,b'):

    cookies = pickle.load(open(location, "rb"))
    
    
    driver.get(url)
    driver.delete_all_cookies()
    print(cookies)
    for cookie in cookies:
        driver.add_cookie(cookie)

cookies_location = "/home/pasha/Рабочий стол/AvitoParsing/Sel/cookies.txt"

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count+=1
        if count > 20:
            print("Timing out")
            return
        time.sleep(.6)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return              


def main():
    if os.stat("/home/pasha/Рабочий стол/AvitoParsing/Sel/cookies.txt").st_size == 0:
        login()
    
    global driver2
    driver2=webdriver.Firefox(executable_path=r'/home/pasha/Рабочий стол/AvitoParsing/Sel/geckodriver')
    driver2.header_overrides = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'}

    load_cookies(driver2, cookies_location)
    driver2.get("https://youla.ru/")
   


main()    #ссылка,по которой будем парсить.Ее завести в переменную. 
driver2.get("https://youla.ru/all/muzhskaya-odezhda/obuv?attributes[muzhskaya_odezhda_obuv_tip][0]=8459&attributes[muzhskaya_odezhda_tzvet][0]=8418&attributes[price][from]=200000&attributes[price][to]=320000&attributes[sostojanie_garderob][0]=166111")

while True:
    driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    try:
        driver2.find_element_by_xpath("//*[contains(text(), 'Измените условия поиска, чтобы увидеть больше товаров')]")
        break
    except:
        pass
            
    

with open("sellers.txt", "rb") as fp:   # файл с покупателями,которым уже отправили сообщ.
    s = pickle.load(fp)

#в этом блоке собираем все наши объявления в список.
item_list = []
elements = driver2.find_elements_by_xpath("//li[@class = 'product_item']")
for elem in elements:
    item_list.append(elem.find_element_by_tag_name('a').get_attribute('href'))
   
#находим продавцов по объявлениям,пишем им сообщение.Проверяем писали ли мы им ранее.
for i in item_list:
    driver2.get(i)
    seller = driver2.find_element_by_xpath("//a[@data-test-component = 'UserNameClick']").get_attribute('href')
    if seller in s:
        continue
    text = driver2.find_element_by_xpath("//p[@class = 'sc-fzoaKM hNuJKS']").text
    if seller_or_not.seller_or_not(text):
        message_link = driver2.find_element_by_xpath("//div[@class = 'sc-fzpkqZ cMUTLN']").find_element_by_tag_name('a').get_attribute('href')
        time.sleep(3)
        driver2.get(message_link)
        
        waitForLoad(driver2)
        
        element = driver2.find_element_by_xpath("//div[@class = 'c_create_message__placeholder']")
        actions = ActionChains(driver2)
        actions.move_to_element(element).send_keys('hey',Keys.RETURN).perform()
        
        s.add(seller)
        with open("sellers.txt", "wb") as fp:   
            pickle.dump(s, fp) 
        time.sleep(30)    



def text_generator():
    first = ['Здравствуйте','Добрый день','Приветсвую']
    second = []
    third = []
    fourth = []
    fifth = []
    '\n' ставим в списках,для переноса строки.
 '''1.О чем.В связи с закрытием своего магазина,продаю свой товар оптом\n
    Перестал заниматься кроссовками,поэтому распродаю то,что осталосб\n
    Завязал с продажей кросс,ищу покупателя на свой ассортимент\n
    Возможно вас заинтересует мои кроссовки,продаю оптом,ниже цены всех поставщиков\n
    Заказывал модели у Монтана шоп,Кроссовки-опт-Мск.
    В основном заказывал в Монтана-опт.
 2.Условия.Размеры остались разные,продам от 4х пар любой модели.Цены от 900р-до 1300.
    Отправка СДЭк или любой другой компанией.
 3.Весь ассортимент в профиле,можете выбрать.После договоримся о цене.
   Все модели посмотрите на моем акаунте.Выберете,по цене соориентирую.    
   По стоимостии оставшимся размерам соориетирую.Если нужно оставлю свои контакты для связи'''
  s = first[random] + second[random] + third[random]
  return s         





#Собираем текст для наших сообщений
#Смысл в том,что каждое сообщение должно немного отличаться



