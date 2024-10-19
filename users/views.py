from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, AccountDeleteSerializer
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

@api_view(['POST'])
def register(request):
    """
    Handles user registration.

    Args:
        request (HttpRequest): The request object containing user data.

    Returns:
        Response: A response containing the status and message of the registration.
    """
    serializer = RegisterSerializer(data=request.data)

    try:
        # The registration logic in a try-except block to catch any potential errors
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': f'User {user.username} has been created successfully'}, 
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    """
    Handles user login.

    Args:
        request (HttpRequest): The request object containing login credentials.

    Returns:
        Response: A response containing the status and token if login is successful.
    """
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    else: 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    """
    Handles user logout by deleting the authentication token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Logs out the user by deleting their authentication token.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: A response indicating the success or failure of the logout.
        """
        try:
            # Deletes the user's auth token
            request.user.auth_token.delete()
            return Response({'message': 'You have successfully logged out'}, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Handles retrieval and updating of the user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves the current user.

        Returns:
            CustomUser: The authenticated user instance.
        """
        return self.request.user
    
    def perform_update(self, serializer):
        """
        Saves the updated profile data.

        Args:
            serializer (UserProfileSerializer): The serializer instance with validated data.

        Returns:
            Response: A response indicating the success of the update.
        """
        serializer.save()
        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        
class AccountDeleteAPIView(generics.RetrieveDestroyAPIView):
    """
    Handles account deletion for the authenticated user.
    """
    serializer_class = AccountDeleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieves the current user for deletion.

        Returns:
            CustomUser: The authenticated user instance.
        """
        return self.request.user
    
    def destroy(self, request):  
        """
        Deletes the authenticated user's account.

        Args:
            request (HttpRequest): The request object.

        Returns:
            Response: A response indicating the success of the account deletion.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
