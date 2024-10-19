from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

# Choices for product categories
CATEGORY_CHOICES = [
    ('pants', 'Pants'),
    ('t-shirts', 'T-shirts'),
    ('shoes', 'Shoes'),
    ('jerseys', 'Jerseys'),
    ('dresses', 'Dresses'),
    ('socks', 'Socks'),
    ('shorts', 'Shorts'),
]

class Product(models.Model):
    """
    Represents a product available for purchase.

    Attributes:
        name (str): The name of the product.
        price (Decimal): The price of the product.
        description (str): A brief description of the product.
        image (ImageField): An optional image of the product.
        stock_quantity (int): The available quantity of the product in stock.
        created_date (DateTime): The date the product was created.
        category (str): The category of the product, chosen from predefined categories.
        user (CustomUser): The user who added the product.
    """
    name = models.CharField(max_length=100, unique=False)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='products_pictures', blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Rate(models.Model):
    """
    Represents a rating given by a user for a product.

    Attributes:
        user (CustomUser): The user who gave the rating.
        product (Product): The product being rated.
        rating (int): The rating value given by the user.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(default=0)

class Order(models.Model):
    """
    Represents an order placed by a user for a product.

    Attributes:
        product (Product): The product being ordered.
        quantity (int): The quantity of the product ordered.
        user (CustomUser): The user who placed the order.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Review(models.Model):
    """
    Represents a review given by a user for a product.

    Attributes:
        product (Product): The product being reviewed.
        user (CustomUser): The user who wrote the review.
        review (str): The content of the review.
        review_date (Date): The date the review was created.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review = models.TextField(max_length=100, blank=True, null=True)
    review_date = models.DateField(auto_now_add=True)
