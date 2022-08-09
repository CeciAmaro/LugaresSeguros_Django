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

#poder agregar un comentario a un lugar
class Comentario(models.Model):
    comment = models.CharField(max_length=100)

    class Meta:
        db_table = 'comentarios'
    def __str__(self):
        return self.comment

'''
class Comentario(models.Model):
    like = models.IntegerField(max_value=None, min_value=None)
    dislike = models.IntegerField(max_value=None, min_value=None)

    class Meta:
        db_table = 'likes'
    def __str__(self):
        return self.like
'''
# likes o dislikes 


#registro de usuarios
class User(models.Model):
    name = models.CharField(max_length=40)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-update_at"] #ver la informacion por fecha mas reciente
        def __str__(self):
            return self.username #ver por username 

    
