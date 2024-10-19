from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product, Order, Review, Rate
from .serializers import ProductSerializer, OrderSerializer, ReviewSerializer, RateSerializer
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing products.

    This viewset provides CRUD operations for products and handles permission
    settings based on user authentication.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Determine the permissions required for each action.

        - 'list' and 'retrieve' actions are publicly accessible.
        - All other actions (create, update, delete) require the user to be authenticated.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Automatically assign the logged-in user when creating a product."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Handle product creation with success message."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Assign user field
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Product(s) uploaded successfully!", "data": serializer.data},
            status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """Update an existing product if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this product(s).")
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Product updated successfully!", "data": serializer.data},
                        status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Partially update an existing product if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this product(s).")
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Product partially updated!", "data": serializer.data},
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete an existing product if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied('You do not have permission to delete this product(s)')
        
        self.perform_destroy(instance)
        return Response({"message": "Product(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Optionally filter the products based on query parameters.

        - Supports searching by name, category, and stock quantity.
        - Filters products by maximum price if specified.
        """
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(category__icontains=search) | 
                Q(stock_quantity__icontains=search)
            )

        # Optional filters
        price = self.request.query_params.get('price', None)
        if price:
            queryset = queryset.filter(price__lte=price)
        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing orders.

    This viewset provides CRUD operations for orders and ensures that only 
    authenticated users can create, update, or delete orders.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'], url_path='create-order')
    def create_order(self, request, pk=None):
        """
        Create a new order for a specific product.

        Args:
            request: The request object containing the quantity.
            pk: The primary key of the product.

        Returns:
            Response: A response indicating success or failure.
        """
        product_to_order = get_object_or_404(Product, pk=pk)
        quantity = request.data.get('quantity')

        if not quantity:
            return Response({'message': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'message': 'Invalid quantity value'}, status=status.HTTP_400_BAD_REQUEST)

        # Check stock availability
        if product_to_order.stock_quantity < quantity:
            return Response({'message': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)

        # Adjust stock quantity and save
        product_to_order.stock_quantity -= quantity
        product_to_order.save()

        # Create or get the order
        instance_order, created = Order.objects.get_or_create(
            user=request.user,
            product=product_to_order,
            defaults={'quantity': quantity}
        )

        if created:
            return Response({'message': 'Order successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Order already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Retrieve a specific order by its ID."""
        order = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update an existing order."""
        order = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Order updated successfully!', 'data': serializer.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        """Partially update an existing order."""
        order = get_object_or_404(self.queryset, pk=pk, user=request.user)
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Order partially updated!', 'data': serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """Delete an existing order."""
        order = get_object_or_404(self.queryset, pk=pk, user=request.user)
        self.perform_destroy(order)
        return Response({'message': 'Order deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing reviews.

    This viewset provides CRUD operations for reviews, allowing users to create, 
    update, and delete their own reviews while allowing everyone to read reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        """
        Determine the permissions required for each action.

        - 'list' and 'retrieve' actions are publicly accessible.
        - All other actions (create, update, delete) require the user to be authenticated.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """Update a specific review if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this review.")
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Review updated successfully!", "data": serializer.data},
                        status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """Partially update a specific review if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to edit this review.")
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Review partially updated!", "data": serializer.data},
                        status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete a specific review if the user is the owner."""
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied('You do not have permission to delete this review.')
        
        self.perform_destroy(instance)
        return Response({"message": "Review deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class RateViewset(viewsets.ModelViewSet):
    """
    Viewset for managing ratings.

    This viewset provides CRUD operations for ratings.
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    def get_permissions(self):
        """
        Determine the permissions required for rating
        Determine the permissions required for each action.

        - 'list' and 'retrieve' actions are publicly accessible.
        - All other actions (create, update, delete) require the user to be authenticated.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
