import unittest
from app.models import User,Post,Comment
from app import db
from flask_login import current_user



class TestComment(unittest.TestCase):
    def setUp(self):
        self.user_Derrick = User(username = 'Derrick',email = 'derrick@ms.com',password = 'qwerty')
        self.new_post = Post(title='Test', post='This is a test blog', user=self.user_Derrick)
        self.new_comment = Comment(comment="This is a test comment", user=self.user_Derrick,post=self.new_post)


    def tearDown(self):
        Post.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment, 'This is a test comment')
        self.assertEquals(self.new_comment.user, self.user_Derrick)
        self.assertEquals(self.new_comment.post, self.new_post)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comments_by_id(self):

        self.new_comment.save_comment()()
        got_comments = Comment.get_comments(1)
        self.assertTrue(len(got_comments) == 1)

