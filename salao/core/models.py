from django.db import models


class Base(models.Model):
    data_criacao = models.DateTimeField( #Registrar data de criação do registro
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Data de Criação'
    )
    data_modificacao = models.DateTimeField(    #Registrar data de modificação do registro
        auto_now=True,
        null=True,
        blank=True,
        verbose_name='Data de Modificação'
    )
    ativo = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )

    class Meta:
        abstract = True

class ImageModel(models.Model):
    title = models.CharField(max_length=122)
    image = models.ImageField(
        upload_to="demo",
        null=False,
        blank=False,
        help_text="Tamanho da imagem precisa ser 1080px"
    )

    def __str__(self):
        return self.title