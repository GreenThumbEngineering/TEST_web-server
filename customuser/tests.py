from django.test import TestCase
from django.contrib.auth.models import BaseUserManager
from customuser.models import UserManager

class UserManagerTestCase(TestCase):
    
    def userCreation(self):
        userEmail = "user@email.com"
        userPassword = "1234"
        userId = "123abc"
        goodUser = UserManager._create_user(BaseUserManager, userId, userEmail, userPassword, False, False)
        self.assertEqual(goodUser.email, userEmail)

