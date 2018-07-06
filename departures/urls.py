from django.conf.urls import url

from .views import DepartureView
from departures import views

urlpatterns = [
    url(r'^load-fixtures', views.load_fixtures, name="load_fixtures"),
    url(r'^', DepartureView.as_view()),

]
