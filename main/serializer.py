from rest_framework.serializers import ModelSerializer,RelatedField
from .models import Product,Images,Subscribers,Cart



class SubscriberSerializer(ModelSerializer):
    class Meta:
        model =Subscribers
        fields = "__all__"
class imageField(RelatedField):
    def to_representation(self, value):
        first = value.first()
        return f"{first.image}"
class ImageSerialzer(ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']
class ProductOneSerializer(ModelSerializer):
    images =imageField(read_only=True)
    class Meta:
        model=Product
        fields = ['id','images','name']
class ProductSerailizer(ModelSerializer):
    images = ImageSerialzer(many=True)
    class Meta:
        model = Product
        fields = ['id',"images",'name']

class ProductDetailSerailizer(ModelSerializer):
    images =ImageSerialzer(many=True)
    class Meta:
        model = Product
        fields = "__all__"
        
class CartSerializer(ModelSerializer):
    product=ProductDetailSerailizer()
    class Meta:
        model=Cart
        fields = ['id',"product"]