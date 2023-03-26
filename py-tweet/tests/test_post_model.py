import unittest
from app import create_app, db
from app.models import User, Role, Post, Comment
from add_data import add_data
from datetime import datetime



class PostModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        with self.app.app_context():
            add_data(db, Role, User, Post, Comment)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_to_json(self):
        post = Post(content="test_content", user_id=1)
        db.session.add(post)
        db.session.commit()
        with self.app.test_request_context('/'):
            post_json=post.to_json()
        self.assertEqual(post_json["content"], "test_content")

    def test_timestamp(self):
        post = Post(content="test_content_2")
        db.session.add(post)
        db.session.commit()
        self.assertTrue(
            (datetime.utcnow() - post.created_time).total_seconds() < 3)