from django.shortcuts import render, redirect
from django.conf import settings
from .forms import CreditCardForm
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def add_credit_card(request):
    if request.method == "POST":
        card_form = CreditCardForm(request.POST)
        if card_form.is_valid():
            token=card_form.cleaned_data['stripe_id']
            customer = stripe.Customer.create(
                source=token,
                email=request.user.email,
                )
            request.user.profile.stripe_id = customer.id
            request.user.profile.card_ending = customer.sources.data[0].last4
            request.user.profile.save()
            return redirect("profile")
    else:
        form = CreditCardForm()
        return render(request, "billing/add_credit_card.html", {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE_KEY})
        
        
        
def remove_credit_card(request):
    request.user.profile.stripe_id = ""
    request.user.profile.card_ending = ""
    request.user.profile.save()
    return redirect("profile")
    
    
def make_payment(request):
    amount = int(request.POST['amount'])
    total_in_cent = amount * 100
    
    charge = stripe.Charge.create(
            amount=total_in_cent,
            currency='EUR',
            customer=request.user.profile.stripe_id,
            )

    return redirect("profile")
    

def subscribe(request):
    if request.method == "POST":
        plan = request.POST['plan']
        
        subscription = stripe.Subscription.create(
          customer=request.user.profile.stripe_id,
          items=[{'plan': plan}],
        )
        request.user.profile.subscription_id = subscription.id
        request.user.profile.save()
        return redirect('profile')
    else:
        return render(request, 'billing/subscribe.html')
        
        
def unsubscribe(request):
    stripe.Subscription.modify(request.user.profile.subscription_id, cancel_at_period_end=True)
    return redirect('profile')