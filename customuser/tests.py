from django.test import TestCase
from django.contrib.auth.models import BaseUserManager
from customuser.models import UserManager

class UserManagerTestCase(TestCase):
    
    def test_create_user(self):
        userEmail = "user@email.com"
        userPassword = "1234"
        userId = "123abc"
        goodUser = UserManager.create_user(userId, userEmail, userPassword)
        self.assertEqual(goodUser.email, userEmail)

