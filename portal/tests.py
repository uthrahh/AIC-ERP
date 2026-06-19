from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from startups.models import Startup
from applications.models import Application
from services.models import ServiceRequest

User = get_user_model()

class PublicPagesTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('portal:home'))
        self.assertEqual(response.status_code, 200)

    def test_application_submit_page(self):
        response = self.client.get(reverse('applications:submit'))
        self.assertEqual(response.status_code, 200)

    def test_application_submission(self):
        response = self.client.post(reverse('applications:submit'), {
            'founder_name': 'Test Founder',
            'startup_name': 'Test Startup',
            'address': '123 Test St',
            'contact_number': '9876543210',
            'email': 'founder@test.com',
            'gender': 'Male',
            'domain': 'FinTech',
            'problem_statement': 'Problem',
            'solution': 'Solution',
            'reference_source': 'Web',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Application.objects.count(), 1)


class AuthTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='testadmin', password='pass12345', role='admin', email='a@test.com'
        )
        self.startup = Startup.objects.create(
            brand_name='Test Co',
            legal_name='Test Co Pvt Ltd',
            sector='AI/ML'
        )
        self.startup_user = User.objects.create_user(
            username='teststartup', password='pass12345', role='startup',
            email='su@test.com', startup=self.startup,
        )

    def test_admin_login_redirect(self):
        self.client.login(username='testadmin', password='pass12345')
        response = self.client.get(reverse('portal:admin_home'))
        self.assertEqual(response.status_code, 200)

    def test_startup_service_request(self):
        self.client.login(username='teststartup', password='pass12345')
        response = self.client.post(reverse('services:create'), {
            'service_type': 'Electricity',
            'description': 'Need repair',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ServiceRequest.objects.count(), 1)

    def test_startup_cannot_access_admin(self):
        self.client.login(username='teststartup', password='pass12345')
        response = self.client.get(reverse('portal:admin_home'))
        self.assertEqual(response.status_code, 403)
