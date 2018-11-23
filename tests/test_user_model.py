#-*-coding:utf-8-*-
import unittest
from app.models import Role,Permission,User,AnonymousUser
class UserModelTestCase(unittest.TestCase):

    def test_roles_and_permission(self):
        Role.insert_roles()
        u=User(email='john@example.com',password='cat')
        self.assertTrue(u.can(Permission.WRITE))
        self.assertFalse(u.can(Permission.COMMENT))


    def test_anonymous_user(self):
        u=AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))