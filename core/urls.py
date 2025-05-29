#Django
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'produto', views.ProdutoViewSet)
router.register(r'partes-produto', views.PartesProdutoViewSet)
router.register(r'pedido', views.PedidoViewSet)
router.register(r'pedido-item', views.PedidoItemsViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('chat', views.ChatApiView.as_view(), name='chat_api'),
]