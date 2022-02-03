from datetime import timedelta

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from apps.task.models import Task, TaskTimer


class TaskTestCase(TestCase):
    def setUp(self):
        self.guest_client = APIClient()
        self.admin_client = APIClient()
        self.user_1 = User.objects.create(username='cuzea@gmail.com', first_name="Danik", last_name="Cuzea",
                                          email="cuzea@gmail.com",
                                          password="admin")
        refresh = RefreshToken.for_user(self.user_1)
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_task_get(self):
        response = self.admin_client.get('/task/tasks/', format='json')
        self.assertEqual(200, response.status_code)

    def test_task_creation_guest(self):
        data = {'title': 'new idea', 'body': 'davai', 'status': False, 'worker': self.user_1.id}
        response = self.guest_client.post('/task/tasks/', data, format='json')
        self.assertEqual(401, response.status_code)

    def test_task_creation_admin(self):
        data = {'title': 'new idea', 'body': 'davai', 'status': False, 'worker': self.user_1.id}
        response = self.admin_client.post('/task/tasks/', data, format='json')
        self.assertEqual(201, response.status_code)

    def test_task_done(self):
        response = self.admin_client.get('/task/tasks/done_tasks/', format='json')
        self.assertEqual(200, response.status_code)

    def test_task_my_tasks(self):
        response = self.admin_client.get('/task/tasks/my_tasks/', format='json')
        self.assertEqual(200, response.status_code)

    def test_task_sum_time(self):
        self.task_1 = Task.objects.create(title='BD', body="Delai", status=False,
                                          worker=User.objects.get(id=self.user_1.id))
        self.time_1 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-02T19:11:40Z", stop_time="2021-05-06T19:11:49Z",
                                               time_final=timedelta(seconds=7200))
        self.time_2 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-04T19:11:40Z", stop_time="2021-05-04T19:11:49Z",
                                               time_final=timedelta(seconds=3600))
        response = self.admin_client.get('/task/tasks/1/timers/sum_time/',
                                         kwargs={'pk': Task.objects.get(id=self.task_1.id)}, format='json')
        self.assertEqual(200, response.status_code)

    """def test_task_assign(self):
        self.task_1 = Task.objects.create(title='BD', body="Delai", status=False,
                                          worker=User.objects.get(id=self.user_1.id))
        response = self.admin_client.patch('/task/tasks/1/assign/', {'worker': User.objects.get(id=self.user_1.id)},
                                           content_type='application/json')
        self.assertEqual(200, response.status_code)"""


class CommentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_1 = User.objects.create(username='cuzea@gmail.com', first_name="Danik", last_name="Cuzea",
                                          email="cuzea@gmail.com",
                                          password="admin")
        self.task_1 = Task.objects.create(title='BD', body="Delai", status=False,
                                          worker=User.objects.get(id=self.user_1.id))
        refresh = RefreshToken.for_user(self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_task_comments(self):
        response = self.client.get('/task/tasks/1/comments/', format='json')
        self.assertEqual(200, response.status_code)

    def test_task_create_comment(self):
        data = {'body': 'good idea', 'task': Task.objects.get(id=self.task_1.id),
                'author': User.objects.get(id=self.user_1.id)}
        response = self.client.post('/task/tasks/1/comments/', data)
        self.assertEqual(201, response.status_code)


class TaskTimerTestCase(TestCase):
    def setUp(self):
        self.time_client = APIClient()
        self.user_1 = User.objects.create(username='cuzea@gmail.com', first_name="Danik", last_name="Cuzea",
                                          email="cuzea@gmail.com",
                                          password="admin")
        self.task_1 = Task.objects.create(title='BD', body="Delai", status=False,
                                          worker=User.objects.get(id=self.user_1.id))
        refresh = RefreshToken.for_user(self.user_1)
        self.time_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.time_1 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-02T19:11:40Z", stop_time="2021-05-04T19:11:49Z",
                                               time_final=timedelta(seconds=7200))
        self.time_2 = TaskTimer.objects.create(task=Task.objects.get(id=self.task_1.id),
                                               author=User.objects.get(id=self.user_1.id),
                                               start_time="2021-05-04T19:11:40Z", stop_time="2021-05-04T19:11:49Z",
                                               time_final=timedelta(seconds=3600))

    def test_task_start_timer(self):
        response = self.time_client.post('/task/tasks/1/timers/start_timer/', format='json')
        self.assertEqual(200, response.status_code)
        response = self.time_client.post('/task/tasks/1/timers/stop_timer/', format='json')
        self.assertEqual(200, response.status_code)

    def test_task_log_timer(self):
        data = {'stop_time': '2021-05-04T19:11:49Z', 'time_final': timedelta(seconds=3600)}
        response = self.time_client.post('/task/tasks/1/timers/log_time/', data, format='json')
        self.assertEqual(200, response.status_code)
