from django.contrib.auth import login as auth_login,logout,authenticate
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes,force_text
from django.core.mail import EmailMessage
import requests
#from rest_framework.authtoken.models import Token
from .forms import UserForm
from django.shortcuts import render
from .models import User


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True

        txtCaptcha=request.POST.get('txtCaptcha')
        CaptchaInput=request.POST.get('CaptchaInput')
        txtCaptcha.replace(" ", "")
        CaptchaInput.replace(" ", "")
        if CaptchaInput==txtCaptcha:
            username = request.POST.get('username')
            try:
                check=User.objects.get(username=username)
            except:
                check=None
            if check is not None:
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return render(request, 'home.html')
                    else:
                        messages.error(request,
                                       'Your account is inactive. Please verify you account by clicking the link sent to your email.')
                        return render(request, 'login.html')

                else:
                    messages.error(request, 'Please re-check your password and try again')
                    return render(request, 'login.html')
            else:
                messages.error(request, 'Username doesnot exist')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid Captcha')
            return render(request, 'login.html')

    else:
        storage = messages.get_messages(request)
        storage.used = True
        return render(request, 'login.html')

def signup(request):

    if request.method == 'POST':
        storage = messages.get_messages(request)
        storage.used = True

        user_form = UserForm(request.POST)

        if request.POST.get('password') == request.POST.get('confirm_password'):

            email = request.POST.get('email')
            try:
                email_check = User.objects.get(email=email)
            except:
                email_check = None

            if email_check is None:

                username = request.POST.get('username')
                try:
                    username_check = User.objects.get(username=username)
                except:
                    username_check = None

                if username_check is None:

                    if user_form.is_valid():

                        response = requests.get(
                            "http://api.quickemailverification.com/v1/verify?email=" + email + "&apikey=15aef1e3ebf4f0e3357b6aab94bb77833e639fc261b2d32903e1895bd330")
                        result = response.json()

                        if (result['did_you_mean'] == '' and result['result'] == "valid"):

                            user = user_form.save(commit=False)
                            user.is_active = False
                            user.set_password(user.password)
                            user.save()

                            current_site = get_current_site(request)
                            message = render_to_string('acc_active_email.html', {
                                'user': user,
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                            })

                            mail_subject = 'Activate your IChoose account.'
                            email = EmailMessage(mail_subject, message, to=[email])
                            try:
                                email.send()
                                return render(request, 'emailsent.html')
                            except:
                                u = User.objects.get(username=username)
                                u.delete()
                                messages.error(request, 'Server problem please register again')
                                return render(request, 'signup.html', {'user_form': user_form})

                        else:
                            messages.error(request, 'Give a valid email')
                            return render(request, 'signup.html', {'user_form': user_form})

                    else:
                        messages.error(request, 'Invalid Submission')
                        return render(request, 'signup.html', {'user_form': user_form})

                else:
                    messages.error(request, 'Username already exists')
                    return render(request, 'signup.html', {'user_form': user_form})

            else:
                messages.error(request, 'Email already exists')
                return render(request, 'signup.html', {'user_form': user_form})

        else:
            messages.error(request, 'passwords do not match')
            return render(request, 'signup.html', {'user_form': user_form})

    else:
        storage = messages.get_messages(request)
        storage.used = True
        user_form = UserForm()
        return render(request, 'signup.html', {'user_form': user_form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        return render(request, 'home.html')
    else:
        messages.error(request,'Activation link is invalid!')
        return render(request, 'index.html')
