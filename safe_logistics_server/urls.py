from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('routes/', include('routes.urls')),
    path('users/', include('users.urls')),
    path('health-condition/', include('health_condition.urls')),
    path('assignment/', include('business_logic.urls'))
]
