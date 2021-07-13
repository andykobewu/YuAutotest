import pytest,time
import allure
from selenium import webdriver

from testcase.conftest import driver_path,url_path

@allure.feature("测试登录")
class Test_Login(object):
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


    @allure.story('正确用户名和密码')
    def test_normal_login(self):
        login_el=self.driver.find_element_by_id("submitBtn")
        login_el.click()
        time.sleep(3)
        result = self.driver.find_element_by_xpath('//*[@id="RT_frame"]/div/div/div[1]/div[1]/i/span')
        with allure.step("打开首页"):
            allure.attach('找到欢迎页面')
        assert result.text == 'PC内管应用'

    @classmethod
    @allure.story('退出浏览器')
    def teardown_class(self):
        with allure.step("准备退出"):
            allure.attach('准备退出')
        self.driver.quit()






