
from django.urls import path
from . import views
app_name = "appointments"
urlpatterns = [
    path("",                    views.TherapistListView.as_view(),    name="therapists"),
    path("book/",               views.BookAppointmentView.as_view(),  name="book"),
    path("mine/",               views.MyAppointmentsView.as_view(),   name="my_appointments"),
    path("cancel/<int:pk>/",    views.CancelAppointmentView.as_view(),name="cancel"),
    path("success/",            views.AppointmentSuccessView.as_view(),name="success"),
    path("price/",              views.GetSessionPriceView.as_view(),  name="get_price"),
]
