from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.task.models import TaskTimer, Task


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_task_creation_guest(self):
        data = {'first_name': 'Danik', 'last_name': 'Cuzea', 'email': 'cuzea@gmail.com', 'password': 'admin'}
        response = self.client.post('/users/register/', data, format='json')
        self.assertEqual(200, response.status_code)

    def test_users_month_time(self):
        self.user_1 = User.objects.create(username="cuzea@gmail.com", first_name="Danik", last_name="Cuzea",
                                          email="cuzea@gmail.com", password="admin")
        self.task_1 = Task.objects.create(title='dz', body="delai dz", status=False,
                                          worker=User.objects.get(id=self.user_1.id))
        self.time_1 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-02T19:11:40Z", stop_time="2021-05-04T19:11:49Z",
                                               time_final=timedelta(seconds=7200))
        self.time_2 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-04T19:11:40Z", stop_time="2021-05-04T19:11:49Z",
                                               time_final=timedelta(seconds=3600))
        refresh = RefreshToken.for_user(self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.get('/users/users/month_time/', format='json')
        self.assertEqual(200, response.status_code)

    def test_users_top(self):
        response = self.client.get('/users/users/top/', format='json')
        self.assertEqual(200, response.status_code)
