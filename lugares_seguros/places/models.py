from django.db import models

#agregando imagenes
def upload_img(instance, filename):
    return f'imgs_org/{instance.nombre}/{filename}'

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=56)
    description = models.CharField(max_length=256)
    address_state = models.CharField(max_length=32)
    address_city = models.CharField(max_length=32)
    address_colonia = models.CharField(max_length=32)
    address_street = models.CharField(max_length=32)
    address_zipcode = models.CharField(max_length=32)
    image = models.ImageField(upload_to=upload_img, default='imgs_org/default.png', null=True)

    class Meta:
        db_table ='places' #nombre de la tabla en la base de datos

    def __str__(self):
        return self.name


