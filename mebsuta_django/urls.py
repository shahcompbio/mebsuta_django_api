from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
#from .users.views import UserViewSet, UserCreateViewSet
from .mebsuta_api import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cell_images', views.Cell_ImageViewSet)
router.register(r'mebsuta_users', views.Mebsuta_UsersViewSet)
router.register(r'all_annotations', views.AnnotationsViewSet)
router.register(r'lib_roll_up', views.LibraryViewSet, basename="Library")
router.register(r'cells', views.MasterCellsViewSet, basename="Cell_Image")
router.register(r'cell_data', views.CellDataViewSet, basename="Cell_Image")
router.register(r'debris', views.DebrisViewSet)
router.register(r'annotation_debris_roll_up', views.AnnotationDebrisRollUpViewSet, basename="DebrisRollUp")
router.register(r'annotation_user_roll_up', views.AnnotationRollUpViewSet, basename="AnnotationRollUp")


#router.register(r'users', UserViewSet)
#router.register(r'users', UserCreateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    #path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
