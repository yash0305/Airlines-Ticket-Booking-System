from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import FlightDetail,Passenger,Booking,Place
from django.contrib.auth.hashers import make_password
from django.views import View
from django.core.validators import MinLengthValidator
from django.views.decorators.csrf import csrf_exempt
from . import Checksum
from .filters import Flight


MERCHANT_KEY = 'bKMfNxPPf_QdZppa'

from django.contrib.auth.hashers import  check_password
def index(request):
    flights = FlightDetail.get_all_flight()
    context = {'flights':flights}
    return render(request, 'index.html',context)



class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        em = request.session['email'] = email
        passenger = Passenger.get_passenger_by_email(email)
        error_message = None
        if passenger:
            flag = check_password(password, passenger.password)
            if flag:
                request.session['passenger'] = passenger.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')





class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        passenger = Passenger(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(passenger)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            passenger.password = make_password(passenger.password)
            passenger.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, passenger):
        error_message = None;
        if (not passenger.first_name):
            error_message = "First Name Required !!"
        elif len(passenger.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not passenger.last_name:
            error_message = 'Last Name Required'
        elif len(passenger.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not passenger.phone:
            error_message = 'Phone Number required'
        elif len(passenger.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(passenger.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(passenger.email) < 5:
            error_message = 'Email must be 5 char long'
        elif passenger.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message



class Index(View):

    def post(self , request):
        flight = request.POST.get('flight')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        print(f'flight{flight}')
        print(f'cart{cart}')


        if cart:
            ticket = cart.get(flight)
            print(f'ticket{ticket}')
            if ticket:
                if remove:
                    if ticket<=1:
                        cart.pop(flight)
                    else:
                        cart[flight] = ticket-1
                else:
                    cart[flight] = ticket+1

            else:
                cart[flight] = 1
        else:
            cart = {}
            cart[flight] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}
    # flights = None
    flights = FlightDetail.get_all_flight()
    # flight = flights.filter(AirlineName__iexact=name)
    # print(flight)
    myFilter =  Flight(request.GET, queryset=flights)
    flights = myFilter.qs

    data = {}
    data['flights'] = flights
    data['myFilter'] = myFilter

    print('you are : ', request.session.get('passenger'))
    return render(request, 'index.html', data)



class OrderView(View):


    def get(self , request ):
        passenger = request.session.get('passenger')
        booking = Booking.get_Bookings_by_passenger(passenger)
        print(booking)
        return render(request , 'BookedTicket.html'  , {'booking' : booking})



class Cart(View):
    def get(self , request):
        de = request.GET.get('delete')
        print(f"this is {de}")
        # de.delete()
        ids = list(request.session.get('cart').keys())
        print(ids)
        flights = FlightDetail.get_Flights_by_id(ids)
        print(flights)
        return render(request , 'cart.html' , {'flights' : flights} )



class CheckOut(View):
    def post(self, request):
        # address = request.POST.get('address')
        # phone = request.POST.get('phone')

        passenger = request.session.get('passenger')
        cart = request.session.get('cart')
        email = request.session.get('email')
        Flights = FlightDetail.get_Flights_by_id(list(cart.keys()))
        confirm_payment = request.POST.get("confirm_payment")
        print(passenger, cart, Flights)
        print(f"confirm_payment-------{confirm_payment}")

        for Flight in Flights:
            print(cart.get(str(Flight.id)))

            booking = Booking(passenger=Passenger(id=passenger),
                          flight=Flight,
                          Price=Flight.Price,

                          NumberOfTraveller=cart.get(str(Flight.id)))
            booking.save()
            id = booking.id
            print(f"the booking id is OREDRID_{id}")

            print(f"the passenger id is {passenger}")
            print(f"the passenger email is {email}")
            o = str(f"BOOKINGID_{id}")
            # request.session['cart'] = {}
            param_dict = {

                'MID': 'DIY12386817555501617',
                'ORDER_ID': o,
                'TXN_AMOUNT': str((Flight.Price )* cart.get(str(Flight.id))),
                'CUST_ID': str(id),
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

            }
            b = Booking.objects.get(id = id)
            b.BookingId = o
            b.save()
            param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
            return render(request, 'paytm.html', {'param_dict': param_dict})



        return redirect('cart')




@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            response_dict['ORDERID']
            bookingId = Booking.objects.get(BookingId = response_dict['ORDERID']) 
            bookingId.status = True
            bookingId.save()
            request.session['cart'] = {}
            print('order successful')
            
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})



class BookedTicketView(View):


    def get(self , request ):
        passenger = request.session.get('passenger')
        Bookings = Booking.get_Bookings_by_passenger(passenger)
        print(Bookings)
        return render(request , 'BookedTicket.html'  , {'Bookings' : Bookings})


