from django.contrib.auth import login
from django.shortcuts import render, redirect

from accounts.forms import ApplicantRegistrationForm


def register(request):

    print("REGISTER HIT")
    print(request.method)
    if request.method == "POST":

        form = ApplicantRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            print("USER CREATED")
            print(user.email)
            print(user.role)

            login(request, user)

            return redirect(
                "applications:submit"
            )

        else:

            print(form.errors)

    else:

        form = ApplicantRegistrationForm()

    return render(
        request,
        "applicants/register.html",
        {
            "form": form
        }
    )