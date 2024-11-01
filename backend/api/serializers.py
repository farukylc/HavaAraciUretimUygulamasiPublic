from django.contrib.auth.models import *
from rest_framework import serializers, status
from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Airplane, IHAPiece, AirplanePiece
from rest_framework.response import Response


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "username", "password", "department","name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Person.objects.create_user(**validated_data)
        return user

class DepartmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departman
        fields = ['id', 'name']

    def create(self, validated_data):
        departman = Departman.objects.create(**validated_data)
        return departman


class IHAPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = IHAPiece
        fields = ['id', 'piece_type', 'model_type', 'is_used']

    def create(self, validated_data):
        # Yeni bir IHAPiece nesnesi oluştur
        ihapiece = IHAPiece.objects.create(**validated_data)
        return ihapiece

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Parça başarıyla silindi."}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class AirplanePieceSerializer(serializers.ModelSerializer):
    piece = IHAPieceSerializer(read_only=True)
    airplane = serializers.PrimaryKeyRelatedField(queryset=Airplane.objects.all())
    piece_id = serializers.PrimaryKeyRelatedField(source='piece', queryset=IHAPiece.objects.filter(is_used=False), write_only=True)

    class Meta:
        model = AirplanePiece
        fields = ['id', 'airplane', 'piece', 'piece_id']

    def validate(self, data):
        airplane = data['airplane']
        piece = data['piece']
        
        # Uçak ve parçanın model_type alanları uyumlu olmalı
        if airplane.model_type != piece.model_type:
            raise serializers.ValidationError("Parçanın model türü, uçağın model türü ile eşleşmiyor.")

        # Parçanın kullanılmamış olması gerekir
        if piece.is_used:
            raise serializers.ValidationError("Bu parça zaten kullanılmış.")
        
        return data

    def create(self, validated_data):
        # AirplanePiece nesnesini oluştur
        airplane_piece = AirplanePiece.objects.create(**validated_data)
        
        # Parça kullanıldığından `is_used` alanını `True` yapıyoruz
        piece = validated_data['piece']
        piece.is_used = True
        piece.save()
        
        return airplane_piece


class AirplaneSerializer(serializers.ModelSerializer):
    # pieces alanında AirplanePieceSerializer kullanarak ilişkili IHAPiece bilgilerini dahil ediyoruz
    pieces = AirplanePieceSerializer(source='airplanepiece_set', many=True, read_only=True)

    class Meta:
        model = Airplane
        fields = ['id', 'model_type', 'pieces']

    def create(self, validated_data):
        # Yeni bir Airplane nesnesi oluştur
        airplane = Airplane.objects.create(**validated_data)
        return airplane


