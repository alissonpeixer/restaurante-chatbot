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
    #permission_classes = [permissions.IsAuthenticated]

class PartesProdutoViewSet(viewsets.ModelViewSet):

    queryset = models.PartesProduto.objects.all().order_by('-data_criacao')
    serializer_class = serializers.PartesProdutoSerializer
    #permission_classes = [permissions.IsAuthenticated]

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
        if 'etapa_fluxo' not in data:
            return Response({'status': 'ERROR', 'mensagem': 'Etapa fluxo não informada.'})

        try:
            try:

                fluxo = models.ChatFluxo.objects.filter(etapa_fluxo=data['etapa_fluxo']).first()
                
                chat = models.Chat.objects.get(user = request.user)
                chat.etapa_fluxo = fluxo
                chat.save()

                if data['mensagem']:
                    models.ChatMensagem.objects.create(chat=chat, mensagem=data['mensagem'], autor=request.user)

                opcoes = models.ChatFluxoOpcao.objects.filter(etapa_fluxo=fluxo).all()
                opcoes_serializer = serializers.ChatFluxoOpcaoSerializer(opcoes, many=True).data

                return Response({'status': 'OK', 'mensagem': fluxo.resposta, 'fluxo': fluxo.etapa_fluxo, 'opcoes': opcoes_serializer})
            except models.Chat.DoesNotExist:
                fluxo = models.ChatFluxo.objects.filter(etapa_fluxo='PERGUNTA_1').first()
                
                opcoes = models.ChatFluxoOpcao.objects.filter(etapa_fluxo=fluxo).all()

                chat = models.Chat.objects.create(user = request.user, etapa_fluxo = fluxo)
                chat.save()

                
                if data['mensagem']:
                    models.ChatMensagem.objects.create(chat=chat, mensagem=data['mensagem'],autor=request.user)
                    
                opcoes_serializer = serializers.ChatFluxoOpcaoSerializer(opcoes, many=True).data

                return Response({'status': 'OK', 'mensagem': fluxo.resposta, 'fluxo': fluxo.etapa_fluxo, 'opcoes': opcoes_serializer})
        except Exception as e:
            return Response({'status': 'ERROR', 'message': 'An error occurred while processing the request.'}, status=500)
       

