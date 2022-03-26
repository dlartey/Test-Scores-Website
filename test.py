import os
import unittest
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import app, db, models
from flask_login import current_user
from app.models import Student, Module, Scores


class TestUser(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def test_login_page(self):
        tester = app.test_client(self)
        response = tester.get('/login',content_type='html/text')
        self.assertTrue(b'Login Page' in response.data)

    def test_register_page(self):
        tester = app.test_client(self)
        response = tester.get('/add_student',content_type='html/text')
        self.assertTrue(b'Please Register as a student below:' in response.data)

    def test_dashboard(self):
        tester = app.test_client(self)
        response = tester.get('/dashboard',content_type='html/text')
        self.assertTrue(b'Redirecting' in response.data)


    def tearDown(self):
        db.session.remove()

if __name__ == '__main__':
    unittest.main()
