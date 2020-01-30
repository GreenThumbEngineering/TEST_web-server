from django.test import TestCase
from django.contrib.auth.models import BaseUserManager
from myapp.models import UserManager

class UserManagerTestCase(TestCase)
    def setUp(self):
        userEmail = "user@email.com"
        userPassword = "1234"
        userId = "123abc"
        goodUser = UserManager._create_user(BaseUserManager, userId, userEmail, userPassword)

    def userCreation(self):
        self.assertEqual(gooduser.email, userEmail)

