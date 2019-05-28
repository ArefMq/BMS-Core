from django.conf.urls import url, include, path
from rest_framework import routers
from bms.backend import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', views.CustomObtainAuthToken.as_view()),
    url(r'^profile/$', views.ProfileView),
    url(r'^upload/', views.UploadView),
    url(r'^changepass/$', views.ChangePassView),
    url(r'^deleteuser/$', views.DeleteUserView),
    url(r'^edituser/$', views.EditUserView),
    url(r'^users/$', views.UserView),
    url(r'^accessoriesList/$', views.AllAccessoriesView),
    url(r'^accessory/$', views.AccessoryView),
    url(r'^editAccessories/$', views.EditAccessoriesView),
    url(r'^group/$', views.GroupView),
    url(r'^groupList/$', views.GroupListView),
    url(r'^deleteGroup/$', views.DeleteGroupView),
    url(r'^editGroup/$', views.EditGroupView),
    url(r'^command/$', views.CommandView),
    url(r'^sceneList/$', views.SceneListView),
    url(r'^triger/$', views.TrigerView),

    path('hvacs/<int:hvac_id>/status/$', views.GetHVACStatus),
    path('hvacs/<int:hvac_id>/targetTemperature/<int:value>/$', views.SetHVACStatus),
    path('hvacs/<int:hvac_id>/targetHeatingCoolingState/<int:value>/$', views.SetHVACCoolingMode),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
