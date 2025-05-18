#Libs
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

#Serializers
from . import serializers
from . import models

class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = models.Produto.objects.all().order_by('-data_criacao')
    serializer_class = serializers.ProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PartesProdutoViewSet(viewsets.ModelViewSet):

    queryset = models.PartesProduto.objects.all().order_by('-data_criacao')
    serializer_class = serializers.PartesProdutoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoViewSet(viewsets.ModelViewSet):

    queryset = models.Pedido.objects.all().order_by('-data_criacao')
    serializer_class = serializers.PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

class PedidoItemsViewSet(viewsets.ModelViewSet):

    queryset = models.PedidoItems.objects.all().order_by('-data_criacao')
    serializer_class = serializers.PedidoItemsSerializer
    permission_classes = [permissions.IsAuthenticated]



#Api
class ChatApiView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        return Response({'status': 'ok','message': 'API is running'})

    def post(self, request, format=None):
        data = request.data
        print(data)
        return Response({'status': 'ok','message': 'API is running'})