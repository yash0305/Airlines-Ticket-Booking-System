
from django.urls import path, include
from .views import Index,landingPage
from .views import Signup
from .views import Login , logout
from .views import Cart
from .views import OrderView
from .views import CheckOut
from .views import BookedTicketView

from . import views



urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('landingPage', landingPage , name='landingPage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('cart', Cart.as_view() , name='cart'),
    path('orders', OrderView.as_view(), name='orders'),
    path('checkout', CheckOut.as_view() , name='checkout'),
    path('BookedTicket', BookedTicketView.as_view() , name='BookedTicket'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
]