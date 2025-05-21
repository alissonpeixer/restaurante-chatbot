#Django
from django.db import models
#Libs
import shortuuid
from shortuuid.django_fields import ShortUUIDField


def get_path_produto_imagem(instance, filename):
  return f'produtos/{instance.codigo}/{shortuuid.uuid()}.{str(filename).split('.')[len(str(filename).split('.'))-1]}'
def get_path_partes_produto_imagem(instance, filename):
  return f'partes_produto/{instance.codigo}/{shortuuid.uuid()}.{str(filename).split('.')[len(str(filename).split('.'))-1]}'


class Produto(models.Model):

  codigo        = ShortUUIDField(length=7,max_length=9,prefix="pr",alphabet="abcdefg1234",unique=True,editable=False)
  
  nome          = models.CharField(max_length=100)
  descricao     = models.TextField(blank=True,null=True)
  preco         = models.DecimalField(max_digits=10, decimal_places=2)
  imagem        = models.ImageField(upload_to=get_path_produto_imagem,max_length=400)
  partes        = models.ManyToManyField('PartesProduto', blank=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name = 'Produto'
    verbose_name_plural = 'Produtos'
    ordering = ['-data_criacao']


class PartesProduto(models.Model):

  codigo        = ShortUUIDField(length=7,max_length=9,prefix="pr",alphabet="abcdefg1234",unique=True,editable=False)

  nome          = models.CharField(max_length=100)
  descricao     = models.TextField(blank=True,null=True)
  imagem        = models.ImageField(upload_to=get_path_partes_produto_imagem,max_length=400)
  preco         = models.DecimalField(max_digits=10, decimal_places=2,default=0)
  ativo         = models.BooleanField(default=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.nome
  
  class Meta:
    verbose_name = 'Parte do Produto'
    verbose_name_plural = 'Partes do Produto'
    ordering = ['-data_criacao']


class Pedido(models.Model):
  PEDIDO_STATUS_CHOICES = ( 
    ('P', 'Pendente'),
    ('A', 'Aprovado'),
    ('R', 'Rejeitado')
  )


  codigo          = ShortUUIDField(length=7,max_length=9,prefix="pe",alphabet="abcdefg1234",unique=True,editable=False)

  status          = models.CharField(choices=PEDIDO_STATUS_CHOICES,default='P',max_length=1)
  cliente         = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True)

  items           = models.ManyToManyField('PedidoItems', blank=True)
  data_criacao    = models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return f'Pedido {self.id} - {self.cliente} - {self.status}'
  
  class Meta:
    verbose_name = 'Pedido'
    verbose_name_plural = 'Pedidos'
    ordering = ['-data_criacao']


class PedidoItems(models.Model):
  codigo          = ShortUUIDField(length=7,max_length=9,prefix="cr",alphabet="abcdefg1234",unique=True,editable=False)

  produto        = models.ForeignKey(Produto, on_delete=models.CASCADE)
  partes_produto = models.ManyToManyField(PartesProduto, blank=True)
  data_criacao   = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Pedido Items -> {self.id}'
  
  class Meta:
    verbose_name = 'Pedido Items'
    verbose_name_plural = 'PedidoItems'
    ordering = ['-data_criacao']



# Fluxo Chat
class Chat(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="ch", alphabet="abcdefg1234", unique=True, editable=False)

  user          = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True)
  etapa_fluxo   = models.ForeignKey('ChatFluxo', on_delete=models.CASCADE, null=True, blank=True, related_name='fluxo')
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Chat {self.codigo} - {self.user}"

  class Meta:
    verbose_name = 'Chat'
    verbose_name_plural = 'Chats'
    ordering = ['-data_criacao']



class ChatMensagem(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="ms", alphabet="abcdefg1234", unique=True, editable=False)

  chat          = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='mensagens')
  autor         = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True)
  mensagem      = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.mensagem

  class Meta:
    verbose_name = 'Chat Mensagem'
    verbose_name_plural = 'Chat Mensagens'
    ordering = ['data_criacao']



class ChatFluxo(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="fl", alphabet="abcdefg1234", unique=True, editable=False)

  etapa_fluxo   = models.CharField(max_length=100,default='')
  resposta      = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.etapa_fluxo
  
  class Meta:
    verbose_name = 'Chat Fluxo'
    verbose_name_plural = 'Chat Fluxos'
    ordering = ['-data_criacao']

class ChatFluxoOpcao(models.Model):
  codigo        = ShortUUIDField(length=7, max_length=9, prefix="fo", alphabet="abcdefg1234", unique=True, editable=False)

  etapa_fluxo   = models.ForeignKey(ChatFluxo, on_delete=models.CASCADE, related_name='fluxo_opcoes')
  fluxo_destino = models.ForeignKey(ChatFluxo, on_delete=models.CASCADE, related_name='fluxo_opcao_destino', null=True, blank=True)
  descricao     = models.TextField(blank=True, null=True)
  data_criacao  = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.etapa_fluxo} -> {self.fluxo_destino} = {self.descricao}'
    
  class Meta:
    verbose_name = 'Chat Fluxo Opcao'
    verbose_name_plural = 'Chat Fluxo Opcoes'
    ordering = ['-data_criacao']