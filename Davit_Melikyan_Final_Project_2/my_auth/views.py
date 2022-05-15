from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView
from rest_framework.authtoken.models import Token
from Quotes_web import settings
from quotes.models import Authors
from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_bytes, force_text
from .token import generate_token
from my_auth.models import UserHistory


def home(request):
    account = request.user
    if account.is_authenticated:
        return redirect("quotes:quotes_list")
    else:
        return redirect("my_auth:login")


def not_found_404(request, exception):
    return render(request, '404.html', status=404)


def about(request):
    return render(request, 'about.html', {})


def register(request):
    account = request.user
    if account.is_authenticated:
        return redirect("quotes:quotes_list")

    if request.method == 'POST':
        myform = request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        context = {'form': myform}

        if not username or not email or not firstname or not lastname\
                or not password1 or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "register.html", context=context)

        if len(username) < 5:
            messages.error(request, "Username is too short.")
            return render(request, "register.html", context=context)

        if len(username) > 10:
            messages.error(request, "Username is too long.")
            return render(request, "register.html", context=context)

        if email and '@' not in email:
            messages.error(request, "Wrong email")
            return render(request, "register.html", context=context)

        if not username.isalnum():
            messages.error(request, "Username must be Numeric.")
            return render(request, "register.html", context=context)

        if password1 != password2:
            messages.error(request, "Passwords didn't match.")
            return render(request, "register.html", context=context)

        if User.objects.filter(username=username):
            messages.error(request, f"{username} username is not available.")
            return render(request, "register.html", context=context)

        if User.objects.filter(email=email):
            messages.error(request, f"{email} email is already registered.")
            return render(request, "register.html", context=context)

        user = User.objects.create_user(username, email, password1)
        user.first_name = firstname
        user.last_name = lastname
        user.is_active = False

        user.save()

        messages.success(request, f'Hi {user.first_name} {user.last_name}, you have successfully registered.'
                                  f'We sent you a confirmation email, please confirm your email !!!')

        # Send email for verification
        # subject = 'Email verification'
        # message = f"Hello {user.first_name} {user.last_name} !!! \n" \
        #           f"Thank you for registration. \n" \
        #           f"Please verify your email to activate your account."
        #
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [user.email]
        #
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        send_register_email(request, user, user.pk, user.first_name, user.last_name, user.email)
        #Confirmation email
        # current_site = get_current_site(request)
        # email_subject = "Confirm your email !!!"
        # message2 = render_to_string('email_confirmation.html', {
        #     'name': user.first_name,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': generate_token.make_token(user)
        # })
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [user.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect("my_auth:login")

    context = {}
    return render(request, 'register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("quotes:quotes_list")
    else:
        return render(request, "activation_faild.html")


def login_request(request):
    account = request.user
    if account.is_authenticated:
        return redirect("quotes:quotes_list")

    if request.method == "POST":
        myform = request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        context = {'form': myform}
        user = authenticate(username=username, password=password)

        if not username or not password:
            messages.error(request, "Username and password are required.")
            context = {}
            return render(request, "login.html", context)

        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("quotes:quotes_list")

        elif account.is_active is False:
            messages.error(request, "Your account is not active.")
            return render(request, "login.html", context)

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", context)

    context = {}
    return render(request, "login.html", context)


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("my_auth:login")


# def send_email(request):
#     # subject = request.POST.get('subject', '')
#     # message = request.POST.get('message', '')
#     # from_email = request.POST.get('from_email', '')
#     subject = 'Email verification'
#     message = f"Hello "
#     from_email = 'admin@aca.am'
#
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ['it@ssa.am'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return HttpResponseRedirect('/contact/thanks/')
#     else:
#         # In reality we'd use a form class
#         # to get proper validation errors.
#         return HttpResponse('Make sure all fields are entered and valid.')


def send_register_email(request, myuser, userid, firstname, lastname, email):
    # Send email for verification
    # subject = 'Email verification'
    # message = f"Hello {user.first_name} {user.last_name} !!! \n" \
    #           f"Thank you for registration. \n" \
    #           f"Please verify your email to activate your account."
    #
    # from_email = settings.EMAIL_HOST_USER
    # to_list = [user.email]
    #
    # send_mail(subject, message, from_email, to_list, fail_silently=True)

    # Confirmation email
    current_site = get_current_site(request)
    email_subject = "Confirm your email !!!"
    message2 = render_to_string('email_confirmation.html', {
        'name': f"{firstname} {lastname}",
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(userid)),
        'token': generate_token.make_token(myuser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = True
    email.send()


@login_required
def profile(request):
    account = request.user
    author = Authors.objects.filter(user=account.id).values('id', 'name', 'image')
    context = {'form': account, 'author': author}
    return render(request, "profile.html", context=context)


class AuthorUpdateView(UpdateView):
    model = Authors
    fields = ('name', 'image')
    success_url = reverse_lazy('my_auth:profile')
    template_name = "authorupdate.html"

    def get_queryset(self):
        return Authors.objects.filter(user_id=self.request.user.pk)

    def form_valid(self, form):
        authorname = form.cleaned_data['name']
        # authorimage = form.cleaned_data['image']

        # print(authorimage)
        # if not authorimage:
        #     messages.error(self.request, "No image !!!")
        #     context = {'form': form}
        #     return render(self.request, "authorupdate.html", context=context)

        if not authorname:
            messages.error(self.request, "Author's name is required !!!")
            context = {'form': form}
            return render(self.request, "authorupdate.html", context=context)

        authornamecheck = Authors.objects.filter(name=authorname).values('user', 'name')
        account = self.request.user
        if authornamecheck:
            if authornamecheck[0]['user'] != account.id and authornamecheck[0]['name'] == authorname:
                messages.error(self.request, "Sorry, that name already exist, please try another one !!!")
                context = {'form': form}
                return render(self.request, "authorupdate.html", context=context)

        messages.success(self.request, f"Your info was successfully updated !!!")
        context = {'form': form}
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name')
    success_url = reverse_lazy('my_auth:profile')
    template_name = "userupdate.html"

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def form_valid(self, form):
        firstname = form.cleaned_data['first_name']
        lastname = form.cleaned_data['last_name']

        if not firstname or not lastname:
            messages.error(self.request, "All fields are required.")
            context = {'form': form}
            return render(self.request, "userupdate.html", context=context)

        account = self.request.user
        if firstname == account.first_name and lastname == account.last_name:
            messages.error(self.request, "Sorry, but this is your current full name !!!")
            context = {'form': form}
            return render(self.request, "userupdate.html", context=context)

        userhistory = UserHistory.objects.create(user_id=account.id,
                                                 first_name=account.first_name,
                                                 last_name=account.last_name,
                                                 email=account.email,
                                                 is_active=account.is_active)
        userhistory.save()
        messages.success(self.request, f"Your info was successfully updated !!!")
        return super().form_valid(form)


def send_api_token_email(request, token):
    # Send API token
    currentuser = request.user
    subject = 'API Token'
    message = f"Hello {currentuser.first_name} {currentuser.last_name} !!! \n" \
              f"This is your API Token\n" \
              f"Token: {token}"

    from_email = settings.EMAIL_HOST_USER
    to_list = [currentuser.email]

    send_mail(subject, message, from_email, to_list, fail_silently=True)
    messages.success(request, "We sent you API Token !!!")
    return redirect("my_auth:profile")


@login_required
def get_api_token(request):
    #create or get token
    currentuser = request.user
    usertoken = Token.objects.filter(user_id=currentuser.id)
    if usertoken:
        token = usertoken
    else:
        token = Token.objects.create(user_id=currentuser.id)
    context = {'userinfo': currentuser, 'token': token}
    return render(request, "api_token.html", context=context)



