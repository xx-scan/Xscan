from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_title = settings.SITE_NAME
admin.site.site_header = settings.SITE_NAME

urlpatterns = [
      url(r'^sta/admin-v0/', admin.site.urls),
      # url(r'^cso/admin-v1/', xadmin.site.urls),

  ]


urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

# urlpatterns += static(
#     settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
# )
