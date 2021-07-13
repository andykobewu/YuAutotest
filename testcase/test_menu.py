import pytest,time
import allure
from selenium import webdriver
from testcase.conftest import driver_path,url_path


@allure.feature("测试菜单")
class Test_Menu(object):
    @classmethod
    @allure.story('初始化浏览器')
    def setup_class(self):
        self.driver_path = driver_path
        self.url_path = url_path
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.get(self.url_path)
        self.driver.maximize_window()
        self.driver.implicitly_wait(2)
        with allure.step("打开登录页面"):
            allure.attach('最大化')


    @allure.story('菜单正常打开')
    def test_menu(self):
        login_el=self.driver.find_element_by_id("submitBtn")
        login_el.click()
        time.sleep(3)
        menu_el = self.driver.find_element_by_xpath('//*[@id="RT_frame"]/div/div/div[1]/div[2]/div/div[1]/div/ul/div[2]/li/div/span')
        menu_el.click()
        time.sleep(2)

        with allure.step("打开菜单"):
            allure.attach('展开')
        assert menu_el.text=="模板示例"

    @classmethod
    @allure.story('退出浏览器')
    def teardown_class(self):
        with allure.step("准备退出"):
            allure.attach('准备退出')
        self.driver.quit()






