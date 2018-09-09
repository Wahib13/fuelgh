from django.conf.urls import url

import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^omcs/(?P<fuel_type>[A-z]+)/', views.omcs, name='omcs'),

		#OMCs
		url(r'^api/omcs/$', views.OmcList.as_view()),
		url(r'^api/omcs/(?P<pk>[0-9]+)/$', views.OmcDetail.as_view()),
		
		#FuelStations
		#accepts omc longitude and latitude params
		url(r'^api/fuelstations/$', views.FuelStationList.as_view()),
		url(r'^api/fuelstations/(?P<pk>[0-9]+)/$', views.FuelStationDetail.as_view()),

		#Users
		url(r'^api/users/$', views.UserList.as_view()),
		url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
		url(r'^api/google_users/$', views.googleUsers),

		# url('^api/fuelstations/bylocation/$', views.FuelStationByLocation.as_view()),
	]

