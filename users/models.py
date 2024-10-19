from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    """
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email, username, and password.

        Args:
            username (str): The username for the user.
            email (str): The email address for the user.
            password (str, optional): The password for the user. Defaults to None.
            **extra_fields: Additional fields to be set on the user.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError("Please enter email")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given username, email, and password.

        Args:
            username (str): The username for the superuser.
            email (str): The email address for the superuser.
            password (str, optional): The password for the superuser. Defaults to None.
            **extra_fields: Additional fields to be set on the superuser.

        Raises:
            ValueError: If is_staff or is_superuser is not set to True.

        Returns:
            CustomUser: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser to include additional fields.
    """
    
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, max_length=200)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Use the custom user manager
    objects = CustomUserManager()


class UserProfile(models.Model):
    """
    User profile model linked to CustomUser model with additional information.
    """
    
    picture = models.URLField()
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the UserProfile instance.

        Returns:
            str: A string representation of the UserProfile, showing the username.
        """
        return f'{self.user.username} Profile'
