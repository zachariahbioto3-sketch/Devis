from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from messaging.models import Thread


class MessagingFlowTests(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            email='client@example.com',
            username='client',
            password='testpass123',
            role='client',
        )
        self.dev_user = User.objects.create_user(
            email='developer@example.com',
            username='developer',
            password='testpass123',
            role='developer',
        )

    def test_new_thread_creates_conversation_and_sends_message(self):
        self.client.force_login(self.client_user)

        response = self.client.post(
            reverse('new_thread', kwargs={'user_pk': self.dev_user.pk}),
            {'body': 'Hello from test'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Thread.objects.filter(participants=self.client_user)
            .filter(participants=self.dev_user)
            .exists()
        )
        self.assertEqual(self.client_user.sent_messages.count(), 1)
        self.assertEqual(self.client_user.sent_messages.first().body, 'Hello from test')
