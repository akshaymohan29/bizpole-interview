from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404

import requests

from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Activity, User


def fetch_activities(activity_type):
    url = f'http://www.boredapi.com/api/activity?type={activity_type.lower()}'

    print(url)
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data['activity']
    return []


def register_user(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('user_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        activity = request.POST.get('activity')
        if password1 != password2:
            print('pass')
            messages.error(request, 'Passwords do not match.')
        else:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                print('user')
                messages.error(request, 'Username is already taken. Please choose a different username.')
            else:
                print('hello')
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                x = User.objects.all()
                print(x)
                # Fetch 10 activities based on the user's selected type
                created_activities = 0
                while created_activities < 10:
                    try:
                        activities = fetch_activities(activity)

                        Activity.objects.create(user=user, name=activities, type=activity)
                        created_activities += 1

                    except (IntegrityError, Exception) as e:
                        print(f"An error occurred while creating activity for user {user.username}. Skipping.")

                print(username, password2)
                authenticated_user = authenticate(username=username, password=password2)
                print(authenticated_user)
                if authenticated_user:
                    print('login')
                    login(request, authenticated_user)

                # send_welcome_mail(user)
                return redirect('home')
    else:
        messages.warning(request, 'Invalid request.')

    return render(request, 'registration.html')


def is_admins(user):
    return user.is_superuser

@login_required
def home(request):
    activities = None
    is_admin = False
    user = User.objects.exclude(is_superuser=True).all()

    if is_admins(request.user):
        print('hello')
        # Admin user
        activities = Activity.objects.all()

        is_admin = True
        paginator = Paginator(activities, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        # Regular user
        activities = Activity.objects.filter(user=request.user)

        paginator = Paginator(activities, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'id': request.user.id,
        'is_admin': is_admin,
        'users':user
    }
    return render(request, 'home.html', context)




@login_required
def edit_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    if request.method == 'POST':
        print(request)
        updated_data = request.POST.get('updated_data')
        activity.name = updated_data
        activity.save()
        return JsonResponse({'message': 'Activity updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})


@login_required
def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    print(activity)
    if request.method == 'POST':
        print(request)
        activity.delete()
        return JsonResponse({'message': 'Activity deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})

@login_required
def delete_user(request, activity_id):
    user = User.objects.get(id=activity_id)

    if request.method == 'POST':
        print(request)
        user.delete()
        return JsonResponse({'message': 'Activity deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})

from datetime import datetime, timedelta

@login_required
def fetch_activity(request, user_id):
    print('activity_id:', user_id)
    activities = Activity.objects.filter(user_id=user_id)
    print(activities)
    types = [i.type for i in activities]
    last_fetched = activities.first().last_fetched.date() if activities.exists() and activities.first().last_fetched else None

    if not activities.exists():
        return JsonResponse({'error': 'Activity not found.'})

    activity = activities.first()
    print(activity)

    if request.method == 'POST':
        today = datetime.now().date()

        if last_fetched and last_fetched == today:
            return JsonResponse({'error': 'This activity has already been fetched today.'})

        created_activities = 0
        while created_activities < 2:
            try:
                print('try')
                activities = fetch_activities(types[0])
                print(activities, 'activities')

                Activity.objects.create(user=activity.user, name=activities, type=activity)
                created_activities += 1

            except (IntegrityError, Exception) as e:
                # time.sleep(10)
                print(f"An error occurred while creating activity for user. Skipping.")

        # Update the last fetched date for the user
        activity.last_fetched = datetime.now()
        activity.save()

        return JsonResponse({'message': 'Activity fetched and created successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request.'})


def user_activities(request, user_id):
    user = get_object_or_404(User, id=user_id)
    activities = Activity.objects.filter(user=user)
    print(list(activities.values()))
    return JsonResponse({'activities': list(activities.values())})
