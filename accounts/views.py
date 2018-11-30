from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, ProfileForm
from django.conf import settings
from datetime import date

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, "index.html")

def profile(request):
    if request.user.profile.subscription_id:
        subscription = stripe.Subscription.retrieve(request.user.profile.subscription_id)
        end_date_str = subscription.current_period_end
        end_date = date.fromtimestamp(float(end_date_str))
        start_date_str = subscription.current_period_start
        start_date = date.fromtimestamp(float(start_date_str))
        if subscription.canceled_at:
            cancelled_at_str = subscription.canceled_at
            cancelled_on = date.fromtimestamp(float(cancelled_at_str))
        else:
            cancelled_on = "not_applicable"
        
        return render(request, "profile.html", {"subscription":subscription, "end_date":end_date, "start_date":start_date, "cancelled_on":cancelled_on})
    else:
        return render(request, "profile.html")
        
        
def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
        return render(request, 'registration/signup.html', 
            {
                'user_form': user_form, 
                'profile_form': profile_form
            })