from rest_framework import serializers
from .models import Product, Review, Order, Rate
from django.db.models import Avg

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Attributes:
        average_rating (float): The average rating of the product, calculated dynamically.
    """
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'stock_quantity', 'category', 
                  'created_date', 'user', 'average_rating']
        read_only_fields = ['created_date', 'user']  # 'user' is set automatically and should be read-only

    def get_average_rating(self, obj):
        """
        Calculates the average rating for the product.

        Args:
            obj (Product): The product instance.

        Returns:
            float: The average rating, or 0 if there are no ratings.
        """
        avg_rating = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0

    def validate_name(self, value):
        """
        Validates the product name.

        Args:
            value (str): The name of the product.

        Raises:
            serializers.ValidationError: If the name is blank.

        Returns:
            str: The validated product name.
        """
        if not value:
            raise serializers.ValidationError('Name cannot be blank')
        return value 

    def validate_price(self, value):
        """
        Validates the product price.

        Args:
            value (Decimal): The price of the product.

        Raises:
            serializers.ValidationError: If the price is not in the valid range.

        Returns:
            Decimal: The validated product price.
        """
        if not (0 <= value <= 1000):
            raise serializers.ValidationError('Price should be between $0.1 and $999')
        return value

    def validate_stock_quantity(self, value):
        """
        Validates the stock quantity of the product.

        Args:
            value (int): The quantity of the product in stock.

        Raises:
            serializers.ValidationError: If the quantity is not in the valid range.

        Returns:
            int: The validated stock quantity.
        """
        if not (0 <= value <= 100):
            raise serializers.ValidationError('Quantity should be between 0 to 100')
        return value

    def validate_category(self, value):
        """
        Validates the product category.

        Args:
            value (str): The category of the product.

        Raises:
            serializers.ValidationError: If no category is selected.

        Returns:
            str: The validated category.
        """
        if not value:
            raise serializers.ValidationError('Select category')
        return value 

    def create(self, validated_data):
        """
        Creates a new product instance.

        Args:
            validated_data (dict): The validated data for product creation.

        Returns:
            Product: The created product instance.
        """
        request = self.context.get('request')
        user = request.user  # Get the user from the request
        validated_data['user'] = user  # Set the user field
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    """
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'user']

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """
    class Meta:
        model = Review
        fields = ['product', 'review', 'review_date']
        read_only_fields = ['review_date']

class RateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rate model.
    """
    class Meta:
        model = Rate
        fields = ['user', 'product', 'rating']
    
    def validate_rating(self, value):
        """
        Validates the product rating.

        Args:
            value (int): The rating value.

        Raises:
            serializers.ValidationError: If the rating is not in the valid range.

        Returns:
            int: The validated rating.
        """
        if not (0 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 0 to 5')
        return value
