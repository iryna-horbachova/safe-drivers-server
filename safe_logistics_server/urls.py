from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from users import views as users_views

#router = routers.DefaultRouter()
#router.register(r'users', users_views.UserViewSet)
#router.register(r'drivers', users_views.DriverViewSet)
#router.register(r'managers', users_views.ManagerViewSet)

#urlpatterns = [
 #   path('', include(router.urls)),
#]

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('users/', include('users.urls')),
    path('routes/', include('routes.urls')),
    path('drivers/', include('users.urls'))
   # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui')
]
