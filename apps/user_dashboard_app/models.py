from django.db import models
import re
import bcrypt
from django.db.models.expressions import F
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validations(self, postData):
        errors = {}
        if len (postData['first_name'])<2:
            errors['first_name']= "Nombre debe tener al menos 2 caracteres"
        if len (postData['last_name'])<2:
            errors['last_name']= "Apellido debe tener al menos 2 caracteres"
        if len (postData['email']) <1:
            errors['email']= "Email es necesario"
        if len(postData['password']) < 5:
            errors['password']='Password debe tener al menos 5 caracteres'
        if postData['password'] != postData['confirm_password']:
            errors['confirmacion'] = 'Contraseñas no coinciden'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email']= "Email is not valid"
        else:
            user = User.objects.filter(email=postData['email'])
            if len(user)>0:
                errors['email_registrado'] = 'Email ya registrado, porfavor intentar otro email'

        return errors

    def login_validations(self, postData):
        login_errors={}

        if not EMAIL_REGEX.match(postData['email']):
            login_errors['email']= "Email is not valid"
        else:
            email_existente = User.objects.filter(email=postData['email'])
            if len(email_existente) == 0:
                login_errors['email_no_encontrado'] = 'Este correo no está registrado'
                return login_errors
            else:
                user = email_existente[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                login_errors['password']='Password incorrecta'
            
        return login_errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    description = models.TextField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length=255)
    sended_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='messages_commited', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.message)

class Comment(models.Model):
    comment = models.TextField(max_length=255)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.comment)



