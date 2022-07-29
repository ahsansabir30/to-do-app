from flask import url_for
from application import app, db
from application.models import *
from flask_testing import TestCase
from datetime import date

class TestBase(TestCase):
    # need to change the config from the original app so that we are able to do a unit test
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test-app.db',
            WTF_CSRF_ENABLED = False,
            DEBUG = True,
            SECRET_KEY = 'NADSKJADSNJDA54DSAJKNDAJ4'  # Dont have to add this
        )
        return app

    # Used to initialise the database with sample data
    def setUp(self):
        db.create_all()
        # if we had multiple tables - we would create dummy data for them aswell
        # this would be even more relevant if the tables had a relationship 
        new_post = Task(name='Dummy Task', description='Test Data', due_date=date.today(), status=False)
        db.session.add(new_post)
        db.session.commit()

    # is to 'tear down' any test - thus making it possible for us to do another test on our application
    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestHomeView(TestBase):
    def test_get_home(self):
        response = self.client.get(url_for('home'))
        self.assert200(response)
        # will check if something exist on page -> example below will check if the page is loaded and that 'TO DO APP' has loaded
        self.assertIn(b'TO DO APP', response.data)
    
    def test_get_new_task(self):
        response = self.client.get(url_for('new_task'))
        self.assert200(response)
        self.assertIn(b'TO DO APP', response.data)

    def test_get_update_task(self):
        response = self.client.get(url_for('update_task', id=1))
        self.assert200(response)
        self.assertIn(b'TO DO APP', response.data)

    def test_get_delete_task(self):
        response = self.client.get(url_for('delete_task', id=1), follow_redirects=True)
        self.assert200(response)
        # then we can check if the data is missing from the response data
        # self.assertNotIn('')

class TestPostRequest(TestBase):
    # we have two post request -> adding a new task and updating a task
    def test_add_task(self):
        response = self.client.post(
            url_for('new_task'),
            data = dict(name = 'Task 1', description='NEW DATA', due_date=date.today(), status=False),
            follow_redirects = True
        )
        
        self.assert200(response)
        self.assertIn(b'Task 1', response.data)
        # we also can check the database directly
        assert Task.query.filter_by(name='Task 1').first() is not None

    def test_update_task(self):
        response = self.client.post(
            url_for('update_task', id=1),
            data = dict(name = 'Task Update', description='NEW DATA', due_date=date.today(), status=False),
            follow_redirects = True
        )

        self.assert200(response)
        self.assertIn(b'Task Update', response.data)

        assert Task.query.filter_by(name='Task Update').first() is not None
        assert Task.query.filter_by(name='Dummy Task').first() is None