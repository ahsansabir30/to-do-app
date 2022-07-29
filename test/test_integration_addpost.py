from flask_testing import LiveServerTestCase
from selenium import webdriver 
from urllib.request import urlopen
from flask import url_for
from application import app, db
# We dont need everything from these files -> just the things we are testing
from application.models import Task
from application.forms import ToDoForm

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050

    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            LIVESERVER_PORT = self.TEST_PORT,
            DEBUG = True,
            TESTING = True
        )
        return app

    def setUp(self):
        # for this test we do need to add sample data
        # if we updating an existing post - we would need to add a record here 
        db.create_all()
        options = webdriver.chrome.options.Options()
        # makes it so we dont have a gui interface - is all done in the terminal
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(f'http://localhost:{self.TEST_PORT}/add-task/')

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()

    def test_server_connectivity(self):
        response = urlopen(f'http://localhost:{self.TEST_PORT}/add-task/')
        assert response.status == 200

class TestAddPost(TestBase):
    def submit_input(self, test_case):
        name_field = self.driver.find_element_by_xpath('/html/body/div[1]/form/input[2]')
        description_field = self.driver.find_element_by_xpath('/html/body/div[1]/form/textarea')
        due_date_field = self.driver.find_element_by_xpath('/html/body/div[1]/form/input[3]')
        submit_field = self.driver.find_element_by_xpath('/html/body/div[1]/form/input[5]')

        # we will be sending the test case as a tuple
        name_field.send_keys(test_case[0])
        description_field.send_keys(test_case[1])
        due_date_field.click()
        due_date_field.send_keys(test_case[2])
        submit.click()

    def test_add_post(self):
        test_case = "Test 1", "Hello World", "31052023"
        self.submit_input(test_case)

        assert list(Post.query.all()) != []
        assert Post.query.filter_by(name="Test 1").first() is not None

    def test_add_post_validation(self):
        test_case = "", "Hello World", "2022/07/28"
        self.submit_input(test_case)

        assert list(Post.query.all()) == []
        assert Post.query.filter_by(name="").first() is None