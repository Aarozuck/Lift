from django import forms
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import DriverRegistrationForm, RideRequestForm, RiderRegistrationForm, UpdateDriverInfoForm
from .models import Driver, Notification, RideRequest, Rider
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

def intro(request):
    return render(request, 'intro.html')


@login_required
@require_GET
def driver_home(request):
    approved_drivers = Driver.objects.filter(is_approved=True)
    return render(request, 'driver_home.html', {'approved_drivers': approved_drivers})

def rider_home(request):
    approved_drivers = Driver.objects.filter(is_approved=True)
    return render(request, 'rider_home.html', {'approved_drivers': approved_drivers})

def driver_login(request):
    if request.method == 'POST':
        # Obtain username and password from the login form
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('driver-profile')  # Redirect to the home page
        else:
            # Display an error message if authentication fails
            error_message = 'Invalid username or password'
            return render(request, 'driver_login.html', {'error_message': error_message})
    else:
        return render(request, 'driver_login.html')


def driver_profile(request):
    driver = Driver.objects.get(user=request.user)  # Assuming you have a User foreign key in the Driver model
    ride_requests = RideRequest.objects.filter(driver=driver)

    context = {
        'ride_requests': ride_requests
    }
    if request.method == 'POST':
        current_location = request.POST.get('current_location')
        online_status = request.POST.get('online_status') == 'True'
        
        # Update the driver's current location and online status
        driver.current_location = current_location
        driver.online_status = online_status
        driver.save()
        # Redirect to the driver profile page to display the updated information
        return redirect('driver_profile')

    return render(request, 'driver_profile.html', {'driver': driver})

def rider_profile(request):
    rider = request.user.rider
    ride_requests = RideRequest.objects.filter(rider=rider)

    context = {
        'ride_requests': ride_requests
    }
    

    return render(request, 'rider_profile.html',{'rider': rider})

def rider_login(request):
    if request.method == 'POST':
        # Obtain username and password from the login form
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('rider-profile')  # Redirect to the home page
        else:
            # Display an error message if authentication fails
            error_message = 'Invalid username or password'
            return render(request, 'rider_login.html', {'error_message': error_message})
    else:
        return render(request, 'rider_login.html')





def driver_registration(request):
    form = DriverRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        driver = Driver.objects.create(
            user=user,
            full_name=form.cleaned_data['full_name'],
            vehicle_type=form.cleaned_data['vehicle_type'],
            address=form.cleaned_data['address'],
            phone_number=form.cleaned_data['phone_number'],
            license_plate=form.cleaned_data['license_plate']
        )
        return redirect('driver_login')
    return render(request, 'driver_registration.html', {'form': form})

def rider_registration(request):
    form = RiderRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        rider = Rider.objects.create(
            user=user,
            full_name=form.cleaned_data['full_name'],
            address=form.cleaned_data['address'],
            phone_number=form.cleaned_data['phone_number']
        )
        return redirect('rider_login')
    return render(request,'rider_registration.html', {'form': form})


def driver_logout(request):
    logout(request)
    return redirect('intro')

def rider_logout(request):
    logout(request)
    return redirect('intro')

def update_driver_info(request):
    driver = request.user.driver  # Assuming you have a driver model associated with the user

    if request.method == 'POST':
        form = UpdateDriverInfoForm(request.POST)
        if form.is_valid():
            online_status = (form.cleaned_data['online_status'] == 'online')
            current_location = form.cleaned_data['current_location']

            driver.online_status = online_status
            driver.current_location = current_location
            driver.save()

            return redirect('driver-profile')
    else:
        form = UpdateDriverInfoForm(initial={
            'online_status': 'online' if driver.online_status else 'offline',
            'current_location': driver.current_location,
        })

    context = {
        'form': form,
    }

    return render(request, 'update_driver_info.html', context)

def request_ride(request, driver_id):
    driver = get_object_or_404(Driver, id=driver_id)
    rider = Rider.objects.get(user=request.user)

    if request.method == 'POST':
        form = RideRequestForm(request.POST)
        if form.is_valid():
            current_location = form.cleaned_data['current_location']
            destination = form.cleaned_data['destination']

            ride_request = RideRequest.objects.create(
                rider=rider,
                driver=driver,
                current_location=current_location,
                destination=destination
            )

            # Send notification to the driver (you need to implement this)

            return redirect('rider-profile')
    else:
        form = RideRequestForm()

    context = {
        'form': form,
        'driver': driver
    }

    return render(request, 'request_ride.html', context)


def accept_ride_request(request, ride_request_id):
    ride_request = get_object_or_404(RideRequest, id=ride_request_id)
    ride_request.accepted = True
    ride_request.save()

    # Create notification for the rider
    notification = Notification.objects.create(
        rider=ride_request.rider,
        driver=ride_request.driver,
        message=f"Your ride request has been accepted by {ride_request.driver.user.get_full_name()}.",
    )

    # Send notification to the rider (you need to implement this)

    return redirect('driver-profile')

def decline_ride_request(request, ride_request_id):
    ride_request = get_object_or_404(RideRequest, id=ride_request_id)
    ride_request.delete()

    # Create notification for the rider
    notification = Notification.objects.create(
        rider=ride_request.rider,
        driver=ride_request.driver,
        message=f"Your ride request has been declined by {ride_request.driver.user.get_full_name()}.",
    )

    # Send notification to the rider (you need to implement this)

    return redirect('driver-profile')