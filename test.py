import time
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdminPanelTests(unittest.TestCase):
    BASE_URL = 'http://localhost:5273'
    TIMEOUT = 120

    @classmethod
    def setUpClass(cls):
        print('⚙️ Launching Admin Panel Tests...')
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 10)

        print('🚀 Waiting for Admin Panel to be ready...')
        cls.wait_for_app_ready()
        print('✅ Admin Panel is ready!')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @staticmethod
    def is_server_running():
        try:
            res = requests.get(AdminPanelTests.BASE_URL, timeout=1)
            return 200 <= res.status_code < 400
        except:
            return False

    @classmethod
    def wait_for_app_ready(cls, retries=10, delay=5):
        for i in range(retries):
            if not cls.is_server_running():
                print(f'⏳ Waiting for admin panel... ({i+1}/{retries})')
                time.sleep(delay)
                continue
            try:
                cls.driver.get(cls.BASE_URL)
                cls.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                return
            except:
                time.sleep(delay)
        raise Exception("❌ Admin Panel not reachable after retries.")

    def test_home_page_title(self):
        self.driver.get(self.BASE_URL)
        self.assertTrue(self.driver.title)

    def test_dashboard_route_loads(self):
        self.driver.get(f'{self.BASE_URL}/dashboard')
        self.wait.until(EC.url_contains('/dashboard'))
        self.assertIn('/dashboard', self.driver.current_url)

    def test_login_page(self):
        self.driver.get(f'{self.BASE_URL}/login')
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'form')))
        self.assertIn('/login', self.driver.current_url)

    def test_check_h1_presence(self):
        self.driver.get(self.BASE_URL)
        headers = self.driver.find_elements(By.TAG_NAME, 'h1')
        self.assertTrue(len(headers) > 0)

    def test_check_body_element(self):
        self.driver.get(self.BASE_URL)
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.assertTrue(body.is_displayed())

    def test_no_404_on_main_routes(self):
        routes = ['/', '/dashboard', '/login']
        for route in routes:
            self.driver.get(f'{self.BASE_URL}{route}')
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.assertNotIn('404', self.driver.page_source.lower())

    def test_favicon_loaded(self):
        self.driver.get(self.BASE_URL)
        favicons = self.driver.find_elements(By.XPATH, "//link[contains(@rel,'icon')]")
        self.assertTrue(len(favicons) > 0)

    def test_meta_charset_present(self):
        self.driver.get(self.BASE_URL)
        meta_charset = self.driver.find_elements(By.XPATH, "//meta[@charset='UTF-8']")
        self.assertTrue(len(meta_charset) > 0)

    # ✅ New Simple Test 1: check for divs
    def test_page_contains_div(self):
        self.driver.get(self.BASE_URL)
        divs = self.driver.find_elements(By.TAG_NAME, 'div')
        self.assertTrue(len(divs) > 0)

    # ✅ New Simple Test 2: check for buttons or link
    def test_contains_button_or_link(self):
        self.driver.get(self.BASE_URL)
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        links = self.driver.find_elements(By.TAG_NAME, 'a')
        self.assertTrue(len(buttons) + len(links) > 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AdminPanelTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"\n--- Test Summary ---")
    print(f"Total tests: {result.testsRun}")
    print(f"Passed tests: {passed}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
