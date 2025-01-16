from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from .models import MyUser
from django.utils.translation import gettext_lazy as _

class UserSerailizer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=["id",'phone','firstname',"lastname",'is_admin','date_joined',"pic"]
class TokenUserSerializer(serializers.Serializer):
    phone = PhoneNumberField(region="ET")
    password = serializers.CharField(max_length=120)
    
    def validate(self, attrs):
        username = attrs.get('phone')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

