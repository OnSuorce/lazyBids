
# User app

This is where custom users are defined

Django by default provides a pre-defined user model with some fields (username, password, join_date etc...) but in order to add custom fields i think the best way is to use a CustomUser model.

# Files
[models.py](models.py) CustomUser's model definition

```python

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
```

[managers.py](managers.py) how the creation of new users is handled
```python
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
```

# Settings

This is where and how [settings.py](../lazyBids/settings.py) must be updated in order to make django use the custom user model as the user model
```python
INSTALLED_APPS = [
    ...
    #Created apps
    'users', #Custom User models and APIs
    ...
]

```
```python
AUTH_USER_MODEL = 'users.CustomUser' #Specify to use 'CustomUser' class as user model from the users/models.py file
```
To make the CustomUser model available on the the django default administration site [admin.py](admin.py) (the one that comes with the user's app) must be updated like this
```python
from .models import CustomUser

admin.site.register(CustomUser) #Make custom user available on /admin/ page
```

