from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import authenticate 
from rest_framework.exceptions import ValidationError
from .models import UserProfile

# Get the user model defined in settings
get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Includes password validation and user creation.
    """
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'country', 'profile_picture', 'password', 'password_2']

    def validate(self, data):
        """
        Validate that the two password fields match.

        Args:
            data (dict): Data containing password and password_2.

        Raises:
            serializers.ValidationError: If passwords do not match.

        Returns:
            dict: Validated data if passwords match.
        """
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        """
        Create a new user instance.

        Args:
            validated_data (dict): Data for user creation.

        Returns:
            User: The created user instance.
        """
        validated_data.pop('password_2')  # Remove password_2 from validated data
        password = validated_data.pop('password')  # Extract password

        # Create user and set password properly
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Validates user credentials and generates an authentication token.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate user credentials.

        Args:
            data (dict): Data containing username and password.

        Raises:
            ValidationError: If authentication fails.

        Returns:
            dict: Data containing the authenticated user.
        """
        username = data.get('username')
        password = data.get('password')
    
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError({'message': 'Invalid username or password'})

        data['user'] = user  # Add user to the data for later use
        return data 
    
    def to_representation(self, instance):
        """
        Customize the representation of the login response.

        Args:
            instance (dict): Data containing the authenticated user.

        Returns:
            dict: Login success message and authentication token.
        """
        user = instance['user']
        token, _ = Token.objects.get_or_create(user=user)  # Get or create a token for the user

        return {
            'message': 'Login successful',
            'token': token.key
        }

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user profile information.
    """
    class Meta:
        model = get_user_model()
        fields = ['username', 'profile_picture']

class AccountDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for deleting a user account.
    """
    class Meta:
        model = get_user_model()
        fields = ['username']
