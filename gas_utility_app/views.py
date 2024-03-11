from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest, Account
from .forms import *
from django.core.files.storage import FileSystemStorage


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to customer dashboard after signup
    else:
        form = CustomerSignUpForm()
    return render(request, 'customer/customer_signup.html', {'form': form})
 
def staff_member_signup(request):
    if request.method == 'POST':
        form = StaffMemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Set is_staff to True for staff members
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')  # Redirect to staff dashboard after signup
    else:
        form = StaffMemberSignUpForm()
    return render(request, 'staff/staff_member_signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                elif user.is_staff:
                    return redirect('dashboard')  # Redirect to staff dashboard
                else:
                    return redirect(reverse('service_request_form'))  # Redirect to service request form
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def Customer_home(request):

    
    return render(request, 'customer/service_request_form.html')

@login_required
def staff_dashboard(request):
    data = ServiceRequest.objects.all()
    return render(request,'staff/staff_dashboard.html',{'data':data})

def edit_request(request, id):
    data = ServiceRequest.objects.get(id = id)
    if request.method == 'POST':
        print(request.POST)
        status = request.POST['status']
        data.status = status
        data.save()
        return redirect('staff-dashboard')
    return render(request,'staff/edit_request.html',{'data':data})


@login_required
def service_request_form(request):
    if request.method == 'POST' and request.FILES.get('file') :
        print(request.POST)
        customer = request.user
        request_type = request.POST['request_type']
        detail = request.POST['detail']

        attachment = request.FILES['file']
        print(customer)

        # fs = FileSystemStorage()
        print(request_type)
        print(detail)



        service_request = ServiceRequest(customer = customer, request_type = request_type, details = detail, attachment = attachment)
        service_request.save()

    elif request.method == 'POST' and not request.FILES.get('file'):
        # Handle case where no file was selected
        print(request.POST)
        customer = request.user
        request_type = request.POST['request_type']
        detail = request.POST['detail']

        # attachment = request.FILES['file']
        print(customer)

        # fs = FileSystemStorage()
        print(request_type)
        print(detail)



        service_request = ServiceRequest(customer = customer, request_type = request_type, details = detail)
        service_request.save()

        return redirect('dashboard')
      
            
    return render(request, 'customer/service_request_form.html')

def dashboard(request):
    user = request.user
    data = ServiceRequest.objects.filter(customer = user)
    return render(request, 'customer/dashboard.html', {'data':data})

@login_required
def service_request_list(request):
    service_requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'service_request_list.html', {'service_requests': service_requests})

@login_required
def account_info(request):
    account = Account.objects.get(user=request.user)
    return render(request, 'customer/account_info.html', {'account': account})

@login_required
def account_update(request):
    account = Account.objects.get(user=request.user)
    if request.method == 'POST':
        form = AccountUpdateForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_info')
    else:
        form = AccountUpdateForm(instance=account)
    return render(request, 'account_update.html', {'form': form})

@login_required
def support_tool(request):
    if not request.user.is_staff:
        return redirect('login')  # Redirect non-staff users
    service_requests = ServiceRequest.objects.all()
    return render(request, 'support_tool.html', {'service_requests': service_requests})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')  # Redirect to the home page or any other desired page after logout
