from selenium.webdriver.chrome.webdriver import Webdriver


from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

     # @classmethod will run when TitleTest is run

    @classmethod
    def setUpClass(cls):
        super.setUpClass()
        cls.selenium = Webdriver()
        # this interacts with web browser
        cls.implicitly_wait(10)
        # makes sure browser is running before code runs

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super.tearDownClass()

    def test_title_on_home_page(self):
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)

