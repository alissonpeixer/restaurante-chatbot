#Django
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'produto', views.ProdutoViewSet)
router.register(r'partes_produto', views.PartesProdutoViewSet)
router.register(r'pedido', views.PedidoViewSet)
router.register(r'pedido_item', views.PedidoItemsViewSet)

urlpatterns = [
  path('', include(router.urls))
]	 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)