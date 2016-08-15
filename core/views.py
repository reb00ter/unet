from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render_to_response


def index(request):
    return render(request=request, template_name="core/index.html")


def register(request):
    return render_to_response('register.html')

@login_required
def profile(request, login):
    user = get_object_or_404(User, username=login)
    return render_to_response('profile.html', context={'user': user})