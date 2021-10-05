import logging
import json
import random
from datetime import datetime

from django.contrib.auth import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from djangoapp.restapis import (
    get_dealer_by_id_from_cf,
    get_dealer_reviews_from_cf,
    get_dealers_from_cf,
)
from django.shortcuts import render

# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from . import models, restapis

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/about.html", context)


# Create a `contact` view to return a static contact page
# def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/contact.html", context)


# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST["username"]
        password = request.POST["psw"]
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect("djangoapp:index")
        else:
            # If not, return to login page again
            return render(request, "djangoapp/user_login.html", context)
    else:
        return render(request, "djangoapp/user_login.html", context)


# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    # If it is a POST request
    elif request.method == "POST":
        # Get user information from request.POST
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = dict()
        url = "https://ff984dbc.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context["dealership_list"] = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, "djangoapp/index.html", context)
        # return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        review_url = "https://ff984dbc.us-south.apigw.appdomain.cloud/api/review"
        dealer_url = "https://ff984dbc.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context = dict()
        context["reviews"] = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["dealer"] = get_dealer_by_id_from_cf(dealer_url, dealer_id)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealerships)

        return render(request, "djangoapp/dealer_details.html", context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

# def add_review(request, dealer_id):
#     if request.method == "GET":
#         # Get dealers from the URL
#         url = "https://ff984dbc.us-south.apigw.appdomain.cloud/api/review"
#         document = request.POST
#         deale
#         # Concat all dealer's short name
#         # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
#         # Return a list of dealer short name
#         return HttpResponse(dealerships)


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        context = {"cars": models.CarModel.objects.all(), "dealerId": dealer_id}
        return render(request, "djangoapp/add_review.html", context)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": str(request.user.first_name) + " " + str(request.user.username),
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": False,
                "id": random.randint(1, 5000),
            }
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(
                    form.get("purchasedate"), "%m/%d/%Y"
                ).isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")
            return redirect(f"/djangoapp/dealer/{dealer_id}")
        else:
            return redirect("/djangoapp/login")
