from django.contrib import admin
from django.urls import path ,re_path , include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [

re_path(r'^jet/', include('jet.urls', 'jet')),
re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
path('admin/', admin.site.urls),
path('api-auth/', include('rest_framework.urls')),
re_path(r'^accounts/', include('allauth.urls')),

path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
re_path(r'^api/token/verify/$', jwt_views.TokenVerifyView.as_view(), name='token_verify'),


re_path(r'user/',include(('user.urls','user'),namespace="user")),
re_path(r'car/',include(('car.urls','car'),namespace="car")),
re_path(r'post/',include(('post.urls','post'),namespace="post")),
re_path(r'notification/',include(('notification.urls','notification'),namespace="notification")),



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
