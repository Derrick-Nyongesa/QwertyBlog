import unittest
from app.models import User,Post,Comment
from app import db
from flask_login import current_user

class PostModelTest(unittest.TestCase):
    def setUp(self):
        self.user_Derrick = User(username = 'Derrick',email = 'derrick@ms.com',password = 'qwerty')
        self.new_post = Post(title='Test', post='This is a test blog', user=self.user_Derrick)

    def tearDown(self):
        Post.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_post,Post))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title, 'Test')
        self.assertEquals(self.new_post.post, 'This is a test blog')
        self.assertEquals(self.new_post.user, self.user_Derrick)
        

    def test_save_post(self):
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all()) > 0)

    def test_get_post_by_id(self):
        self.new_post.save_post()
        got_post = Post.get_post(1)
        self.assertTrue(got_post is not None)