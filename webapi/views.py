from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from main.models import Product
from rest_framework import status
from main.serializer import ProductSerailizer,ProductOneSerializer,ProductDetailSerailizer,SubscriberSerializer
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(["GET"])
def home(request):
    products = Product.objects.all().order_by('-date')[0:7]
    pro_obj = ProductOneSerializer(products,many=True)
    return Response(pro_obj.data)

@api_view(["GET"])
def female(request):
    products = Product.objects.filter(type='F').order_by('-date')
    paginator =PageNumberPagination()
    paginator.page_size = 9
    pag_prod = paginator.paginate_queryset(products,request)
    pro_obj = ProductSerailizer(pag_prod,many=True)
    return paginator.get_paginated_response(pro_obj.data)

@api_view(["GET"])
def male(request):
    products = Product.objects.filter(type='M').order_by('-date')
    paginator =PageNumberPagination()
    paginator.page_size = 9
    pag_prod = paginator.paginate_queryset(products,request)
    pro_obj = ProductSerailizer(pag_prod,many=True)
    return paginator.get_paginated_response(pro_obj.data)
@api_view(["GET"])
def kids(request):
    products = Product.objects.filter(type='K').order_by('-date')
    paginator =PageNumberPagination()
    paginator.page_size = 9
    pag_prod = paginator.paginate_queryset(products,request)
    pro_obj = ProductSerailizer(pag_prod,many=True)
    return paginator.get_paginated_response(pro_obj.data)

@api_view(['GET'])
def get_detail(request,id):
    product = Product.objects.get(id=id)
    prod_obj =ProductDetailSerailizer(product)
    return Response(prod_obj.data)

@api_view(['POST'])
def create_subscriber(request):
    obj = SubscriberSerializer(data=request.data)
    if(obj.is_valid()):
        obj.save()
        return Response({'worked':True})
    else:
        return Response({'error':obj.errors},status=status.HTTP_504_GATEWAY_TIMEOUT)