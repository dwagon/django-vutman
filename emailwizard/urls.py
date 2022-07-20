from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
        path("vutman/", include("vutman.urls")),
        path("admin/vutman/", admin.site.urls),
        path("", RedirectView.as_view(url="/vutman/")),
        path("accounts/", include("django.contrib.auth.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
