#Libs
from rest_framework import serializers

#Models
from . import models
from authentication.serializers import UserSerializer


class PartesProdutoSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.PartesProduto
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class ProdutoSerializer(serializers.ModelSerializer):

  partes_produto = PartesProdutoSerializer(many=True, read_only=True,source='partes')
  class Meta:
    model = models.Produto
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class PedidoItemsSerializer(serializers.ModelSerializer):
  
  dados_partes_produto = PartesProdutoSerializer(many=True, read_only=True,source='partes_produto')

  class Meta:
    model = models.PedidoItems
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']


class PedidoSerializer(serializers.ModelSerializer):
  pedido_items = PedidoItemsSerializer(many=True, read_only=True,source='items')
  
  class Meta:
    model = models.Pedido
    fields = '__all__'
    read_only_fields = ['codigo', 'data_criacao']
