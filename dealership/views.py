from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests


def home(request):
    try:
        state = request.GET.get('state', '')

        if state:
            response = requests.get(f'http://localhost:5001/api/dealers/state/{state}')
        else:
            response = requests.get('http://localhost:5001/api/dealers')

        dealers_data = response.json()

        # Transform the data to use 'id' instead of '_id'
        dealers = []
        for dealer in dealers_data:
            dealer['id'] = dealer['_id']  # Create a new 'id' field
            dealers.append(dealer)

        states = sorted(set(dealer['location']['state'] for dealer in dealers))

        return render(request, 'home.html', {
            'dealers': dealers,
            'states': states,
            'selected_state': state
        })
    except Exception as e:
        print("Error:", str(e))
        return render(request, 'home.html', {
            'error': f'Unable to fetch dealers: {str(e)}'
        })

def about(request):
    return render(request, './about.html')


def contact(request):
    return render(request, './contact.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}")
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, './login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, './signup.html', {'form': form})


def dealer_details(request, dealer_id):
    try:
        print(f"Fetching dealer with ID: {dealer_id}")  # Debug print
        response = requests.get(f'http://localhost:5001/api/dealers/{dealer_id}')
        print(f"Response status: {response.status_code}")  # Debug print
        dealer = response.json()
        dealer['id'] = dealer['_id']  # Add id field for template
        return render(request, 'dealer_details.html', {'dealer': dealer})
    except Exception as e:
        print("Error in dealer_details:", str(e))  # Debug print
        return redirect('home')


@login_required
def add_review(request, dealer_id):
    try:
        if request.method == 'POST':
            review_data = {
                'user': request.user.username,
                'rating': int(request.POST.get('rating')),
                'comment': request.POST.get('comment')
            }

            response = requests.post(
                f'http://localhost:5001/api/dealers/{dealer_id}/reviews',
                json=review_data
            )

            if response.status_code == 200:
                return redirect('dealer_details', dealer_id=dealer_id)

        # Get dealer info for the form
        dealer_response = requests.get(f'http://localhost:5001/api/dealers/{dealer_id}')
        dealer = dealer_response.json()
        dealer['id'] = dealer['_id']  # Add id field for template
        return render(request, 'add_review.html', {'dealer': dealer})

    except Exception as e:
        print("Error:", str(e))
        return redirect('home')


def sentiment_analyzer(request):
    return render(request, './sentiment.html')