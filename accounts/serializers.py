from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()



#회원기능 1-1 \\ 회원 가입
class SignupSerializer(ModelSerializer):
    password = serializers.CharField(write_only = True)
    def create(self, validated_data):
        user = User.objects.create(username = validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user         
    class Meta:
        model = User
        fields = ['pk','username','password']

