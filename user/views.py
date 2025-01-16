from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import TokenUserSerializer,UserSerailizer
from rest_framework.authtoken.models import Token
from main.models import Cart
from main.serializer import CartSerializer
# Create your views here.
class GetToken(APIView):
    serializer_class = TokenUserSerializer
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        obj = UserSerailizer(user).data
        carts = Cart.objects.filter(user=user)
        cart_obj = CartSerializer(carts,many=True).data
        token,created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,"info":obj,"carts":cart_obj})

