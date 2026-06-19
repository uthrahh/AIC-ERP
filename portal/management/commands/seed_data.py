from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, time, timedelta
import random

from startups.models import Startup
from content.models import GalleryItem, ServiceOffering, IncubationStep, Sponsor
from labs.models import Lab, Equipment
from applications.models import Application

User = get_user_model()

SECTORS = [
    'HealthTech',
    'EdTech',
    'AgriTech',
    'FinTech',
    'CleanTech',
    'AI/ML',
    'IoT',
    'BioTech',
    'DeepTech',
    'Social Impact'
]

class Command(BaseCommand):
    help = 'Seed AIC-CIIC ERP with demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding AIC-CIIC ERP...')

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@AIC-CIIC.example.com',
                'role': User.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('admin12345')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin (admin / admin12345)'))

        for title, desc in [
            ('Mentorship', 'Expert guidance from industry mentors and faculty.'),
            ('Infrastructure', 'Office space, labs, and shared facilities.'),
            ('Funding Support', 'Seed funding and investor connect programmes.'),
            ('Market Connect', 'Industry partnerships and go-to-market support.'),
            ('Legal & IP', 'IP filing, compliance, and legal advisory.'),
            ('Lab Access', 'Research labs and prototyping equipment.'),
        ]:
            ServiceOffering.objects.get_or_create(title=title, defaults={'description': desc, 'display_order': 0})

        steps = [
            (1, 'Application', 'Submit your startup application online.'),
            (2, 'Review', 'Selection committee evaluates your proposal.'),
            (3, 'Selection', 'Approved startups receive onboarding details.'),
            (4, 'Onboarding', 'Profile setup, documentation, and orientation.'),
            (5, 'Incubation', 'Access services, labs, mentorship, and funding.'),
            (6, 'Graduation', 'Maturity assessment and alumni transition.'),
        ]
        for num, title, desc in steps:
            IncubationStep.objects.get_or_create(step_number=num, defaults={'title': title, 'description': desc})

        for i in range(1, 11):
            GalleryItem.objects.get_or_create(
                title=f'AIC-CIIC Event {i}',
                defaults={'description': f'Placeholder gallery image {i}', 'display_order': i},
            )

        Sponsor.objects.get_or_create(name='AIC-CIIC Seed Fund', defaults={'amount': 5000000})
        Sponsor.objects.get_or_create(name='Industry Partner A', defaults={'amount': 2000000})

        lab, _ = Lab.objects.get_or_create(
            lab_name='Innovation Lab',
            defaults={'location': 'Block A, Ground Floor', 'description': 'Main prototyping lab'},
        )
        Lab.objects.get_or_create(
            lab_name='Bio Lab',
            defaults={'location': 'Block B, First Floor', 'description': 'Biotechnology research lab'},
        )
        for eq_name in ['3D Printer', 'Oscilloscope', 'Microscope', 'CNC Machine']:
            Equipment.objects.get_or_create(lab=lab, equipment_name=eq_name)

        existing = Startup.objects.count()

        for i in range(existing, 140):
            sector = SECTORS[i % len(SECTORS)]

            Startup.objects.get_or_create(
                brand_name=f'Demo Startup {i+1:03d}',
                defaults={
                    'legal_name': f'Demo Startup {i+1:03d} Pvt Ltd',
                    'company_description': f'Placeholder profile for Demo Startup {i+1:03d}.',
                    'sector': sector,
                    'startup_status': 'Active' if i % 5 == 0 else 'Incubated',
                    'startup_valuation': random.randint(500000, 10000000),
                    'website': f'https://demo{i+1}.com',
                },
            )

        demo_startup = Startup.objects.filter(
            brand_name='Demo Startup Co'
        ).first()
        if not demo_startup:
            demo_startup = Startup.objects.create(
                brand_name='Demo Startup Co',
                legal_name='Demo Startup Co Pvt Ltd',
                company_description='Demo startup for testing the portal.',
                sector='AI/ML',
                startup_status='Active',
            )
            user, uc = User.objects.get_or_create(
                username='startup_demo',
                defaults={'email': 'demo@AIC-CIIC.example.com', 'role': User.Role.STARTUP, 'startup': demo_startup},
            )
            if uc:
                user.set_password('startup12345')
                user.save()
                self.stdout.write(self.style.SUCCESS('Created demo startup (startup_demo / startup12345)'))

        self.stdout.write(self.style.SUCCESS(f'Seed complete. Startups: {Startup.objects.count()}'))
