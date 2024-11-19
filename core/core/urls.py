"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from todo.api.v1 import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

"""
This function initializes and configures the schema view for the API documentation.

Parameters:
- openapi.Info: Contains information about the API, such as title, version, description, terms of service, contact details, and license.
- public (bool): Indicates whether the API documentation is publicly accessible.
- permission_classes (tuple): Specifies the permission classes required to access the API documentation.

Returns:
- schema_view: An instance of the get_schema_view function, configured with the provided parameters.
"""
schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version="v1",
        description="This page is for the documentation task",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.DefaultPermission,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo.urls")),
    path("api-auth", include("rest_framework.urls")),
    path("accounts/", include("accounts.urls")),
    path("captcha/", include("captcha.urls")),
    path(
        "swagger/output.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)