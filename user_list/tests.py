from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(name="test_user", password="test_passwd")
        self.client = Client(enforce_csrf_checks=False)

    def test_user_create(self):
        """创建用户测试"""
        response = self.client.post('/user/', {'username': 'test_create_user', 'password': 'passwd'})
        # response.json()['code']
        pass

    def test_exist_create(self):
        """重复创建"""
        response = self.client.post('/user/', {'username': 'test_user', 'password': 'passwd'})
        pass

    def test_user_update(self):
        """修改密码"""
        response = self.client.patch('/user/', {'username': 'test_create_user', 'password': 'passwd1'})
        pass

    def test_not_exist_user_update(self):
        """修改不存在用户密码"""
        response = self.client.patch('/user/', {'username': 'not_exist_user', 'password': 'passwd1'})
        pass

    def test_user_delete(self):
        """删除用户"""
        response = self.client.delete('/user/', {'username': 'test_create_user'})
        pass

    def test_not_exist_user_delete(self):
        """删除不存在用户"""
        response = self.client.delete('/user/', {'username': 'not_exist_user'})
        pass
