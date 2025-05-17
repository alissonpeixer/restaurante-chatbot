from django.contrib import admin


from . import models

# Register your models here.


admin.site.register(models.Produto)
admin.site.register(models.PartesProduto)
admin.site.register(models.Pedido)
admin.site.register(models.PedidoItems)