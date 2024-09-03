from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase
from selenium.webdriver.support.select import Select


# class NewVisitorTests(unittest.TestCase):
#     def setUp(self):
#         options = Options()
#         options.add_argument("--start-maximized")
#         self.browser = webdriver.Chrome(options=options)

# self.browser.get("http://127.0.0.1:8000/")

# def test_page_login(self):
#     '''Проверка наличия страницы "Вход"'''
#     self.assertIn('Сервис онлайн печати баннеров', self.browser.title)
#
# def test_login_page(self):
#     self.browser.find_element(By.CSS_SELECTOR, "[name='username']").send_keys("vasa@mail.ru")
#     self.browser.find_element(By.CSS_SELECTOR, "[name='password']").send_keys("q911ww1234")
#     self.browser.find_element(By.CSS_SELECTOR, "[name='button']").click()
#     time.sleep(3)
#     self.assertIn('Дашборд', self.browser.title)  # переход в дашборд
# def tearDown(self):
#     self.browser.quit()


class AddressDeliveryTests(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.browser = webdriver.Chrome(options=options)
        User.objects.create()

    def test_add_address_page(self):
        self.browser.get(self.live_server_url)

        self.browser.find_element(By.CSS_SELECTOR, "[name='username']").send_keys("vasa@mail.ru")
        self.browser.find_element(By.CSS_SELECTOR, "[name='password']").send_keys("q911ww1234")
        self.browser.find_element(By.CSS_SELECTOR, "[name='button']").click()
        time.sleep(7)
        # Добавляем новый адрес доставки
        self.browser.get("http://127.0.0.1:8000/account/delivery_list/")
        self.browser.find_element(By.CSS_SELECTOR, "[class='text']").click()
        time.sleep(3)
        self.browser.find_element(By.CSS_SELECTOR, "[name='region']").send_keys("Московская область")
        self.browser.find_element(By.CSS_SELECTOR, "[name='city']").send_keys("Краснознаменск")
        self.browser.find_element(By.CSS_SELECTOR, "[name='street']").send_keys("Ленина")
        self.browser.find_element(By.CSS_SELECTOR, "[name='house']").send_keys("66")
        self.browser.find_element(By.CSS_SELECTOR, "[name='entrance']").send_keys("5")
        self.browser.find_element(By.CSS_SELECTOR, "[name='floor']").send_keys("1")
        self.browser.find_element(By.CSS_SELECTOR, "[name='flat']").send_keys("97")
        self.browser.find_element(By.CSS_SELECTOR, "[name='first_name']").send_keys("Юрий")
        self.browser.find_element(By.CSS_SELECTOR, "[name='second_name']").send_keys("Борисович")
        self.browser.find_element(By.CSS_SELECTOR, "[name='phone']").send_keys("+7984455175")
        select = Select(self.browser.find_element(By.CSS_SELECTOR, "[name='delivery_method']"))
        select.select_by_value('1')
        self.browser.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        time.sleep(5)

    def test_edit_address_page(self):
        '''Редактирование адреса пользователя'''
        self.browser.get("http://127.0.0.1:8000/")
        self.browser.find_element(By.CSS_SELECTOR, "[name='username']").send_keys("vasa@mail.ru")
        self.browser.find_element(By.CSS_SELECTOR, "[name='password']").send_keys("q911ww1234")
        self.browser.find_element(By.CSS_SELECTOR, "[name='button']").click()
        self.browser.get("http://127.0.0.1:8000/account/delivery_list/")
        self.browser.find_element(By.CSS_SELECTOR, "td:nth-child(5) a").click()
        time.sleep(1)
        region = self.browser.find_element(By.CSS_SELECTOR, "[name='region']")
        region.clear()
        region.send_keys("Воронежская область")
        city = self.browser.find_element(By.CSS_SELECTOR, "[name='city']")
        city.clear()
        city.send_keys("Лисабон")
        street = self.browser.find_element(By.CSS_SELECTOR, "[name='street']")
        street.clear()
        street.send_keys("Лизюкова")
        house = self.browser.find_element(By.CSS_SELECTOR, "[name='house']")
        house.clear()
        house.send_keys("53")
        entrance = self.browser.find_element(By.CSS_SELECTOR, "[name='entrance']")
        entrance.clear()
        entrance.send_keys("7")
        floor = self.browser.find_element(By.CSS_SELECTOR, "[name='floor']")
        floor.clear()
        floor.send_keys("7")
        flat = self.browser.find_element(By.CSS_SELECTOR, "[name='flat']")
        flat.clear()
        flat.send_keys("188")
        first_name = self.browser.find_element(By.CSS_SELECTOR, "[name='first_name']")
        first_name.clear()
        first_name.send_keys("Александр")
        second_name = self.browser.find_element(By.CSS_SELECTOR, "[name='second_name']")
        second_name.clear()
        second_name.send_keys("Николаевич")
        phone = self.browser.find_element(By.CSS_SELECTOR, "[name='phone']")
        phone.clear()
        phone.send_keys("+79001112233")
        select = Select(self.browser.find_element(By.CSS_SELECTOR, "[name='delivery_method']"))
        select.select_by_value('SAMOVIVOZ')
        self.browser.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        time.sleep(1)

    def test_delete_address_page(self):
        '''Удаление адреса пользователя'''
        self.browser.get("http://127.0.0.1:8000")
        self.browser.find_element(By.CSS_SELECTOR, "[name='username']").send_keys("vasa@mail.ru")
        self.browser.find_element(By.CSS_SELECTOR, "[name='password']").send_keys("q911ww1234")
        self.browser.find_element(By.CSS_SELECTOR, "[name='button']").click()
        self.browser.get("http://127.0.0.1:8000/account/delivery_list/")

        self.browser.find_element(By.CSS_SELECTOR,
                                  '#content > div > div.row > div > table > tbody:nth-child(2) > tr > td:nth-child(6) > a').click()
        self.browser.find_element(By.CSS_SELECTOR, '[type="submit"]').click()
        time.sleep(1)

    #
    def tearDown(self):
        self.browser.quit()


#
#
if __name__ == '__main__':
    unittest.main(warnings='ignore')

'sfsdf'.capitalize()
