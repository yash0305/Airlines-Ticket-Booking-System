from django.db import models
import datetime
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget,AdminTimeWidget,AdminSplitDateTime


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name

    def register(self):
        self.save()

    @staticmethod
    def get_passenger_by_email(email):
        try:
            return Passenger.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Passenger.objects.filter(email=self.email):
            return True

        return False

# ----------------------------------------------------------------------------------------------

class Place(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.name

class FlightDetail(models.Model):
    AirlineName = models.CharField(max_length=30,)
    FromLocation = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='From',null=True,blank=True)
    ToLocation = models.ForeignKey(Place,on_delete=models.CASCADE,related_name='To',null=True,blank=True)
    DepartureTime = models.DateTimeField()
    ArrivalTime = models.DateTimeField(null=True, blank=True)

    Price = models.IntegerField()
    Duration = models.DurationField()
    AvailableSeat = models.IntegerField(null=True)

    def __str__(self):
        return self.AirlineName



    @staticmethod
    def get_Flights_by_id(ids):
        return FlightDetail.objects.filter(id__in=ids)

    @staticmethod
    def get_all_flight():
        return FlightDetail.objects.all()

    # @staticmethod
    # def get_all_products_by_categoryid(category_id):
    #     if category_id:
    #         return FlightDetail.objects.filter(category=category_id)
    #     else:
    #         return FlightDetail.get_all_flight()
    #

# ----------------------------------------------------------------------------------------------


class Booking(models.Model):
    flight = models.ForeignKey(FlightDetail,
                                on_delete=models.CASCADE)
    passenger = models.ForeignKey(Passenger,
                                 on_delete=models.CASCADE)
    NumberOfTraveller = models.IntegerField(default=1)
    Price = models.IntegerField()


    # phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateTimeField(default=timezone.now)
    # status = models.BooleanField(default=False)
    BookingId = models.CharField(max_length=50,null=True,blank=True)
    status = models.BooleanField(default=False)

    # def SaveBooking(self):
    #     self.save()

    def save(self, *args, **kwargs):
        if self.BookingId is None and self.date and self.id:
            self.BookingId = self.date.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


    @staticmethod
    def get_Bookings_by_passenger(passenger_id):
        return Booking.objects.filter(passenger=passenger_id).order_by('-date')

