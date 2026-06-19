from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.decorators import mentor_required, get_mentor_for_user
from mentorship.models import MentorshipBooking


@mentor_required
def mentor_home(request):
    mentor = get_mentor_for_user(request.user)
    upcoming = mentor.bookings.filter(status__in=['Requested', 'Approved']).count()
    completed = mentor.bookings.filter(status='Completed').count()
    recent = mentor.bookings.select_related('startup').all()[:5]
    return render(request, 'mentors/home.html', {
        'mentor': mentor,
        'upcoming': upcoming,
        'completed': completed,
        'recent_sessions': recent,
    })


@mentor_required
def mentor_profile(request):
    mentor = get_mentor_for_user(request.user)
    return render(request, 'mentors/profile.html', {'mentor': mentor})
