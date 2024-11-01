from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import *


# Create
class CreatePersonView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [AllowAny]


class CreateDepartmanView(generics.CreateAPIView):
    queryset = Departman.objects.all()
    serializer_class = DepartmanSerializer
    #permission_classes = [AllowAny]


class CreateIHAPieceView(generics.ListCreateAPIView):
    queryset = IHAPiece.objects.all()
    serializer_class = IHAPieceSerializer  
    #permission_classes = [AllowAny]
 

#Delete
class DeleteIHAPieceView(generics.DestroyAPIView):
    queryset = IHAPiece.objects.all()
    serializer_class = IHAPieceSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({"message": "Parça başarıyla silindi."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Parça silinemedi."}, status=response.status_code)

# Read

class PersonListView(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    #permission_classes = [AllowAny]
   
class IHAPieceListView(ListAPIView):
    queryset = IHAPiece.objects.all()
    serializer_class = IHAPieceSerializer       

class DepartmanListView(ListAPIView):
    queryset = Departman.objects.all()
    serializer_class = DepartmanSerializer
    permission_classes = [AllowAny]

class DepartmanDetailView(RetrieveAPIView):
    queryset = Departman.objects.all()
    serializer_class = DepartmanSerializer
    lookup_field = 'id'  

#Functions
class PartCountView(APIView):
    def get(self, request, *args, **kwargs):
        model_type = request.query_params.get('model_type')
        part_type = request.query_params.get('part_type')
        
        if not model_type or not part_type:
            return Response({"error": "model_type ve part_type belirtilmelidir."}, status=400)
        
        count = get_part_count_for_model(model_type, part_type)
        return Response({"model_type": model_type, "part_type": part_type, "count": count})
    
class IHAPieceCreateView(generics.CreateAPIView):
    queryset = IHAPiece.objects.all()
    serializer_class = IHAPieceSerializer
    ##permission_classes = [AllowAny]

class AirplaneCreateView(generics.CreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    ##permission_classes = [AllowAny]

class AirplanePieceCreateView(generics.CreateAPIView):
    queryset = AirplanePiece.objects.all()
    serializer_class = AirplanePieceSerializer
    #permission_classes = [AllowAny]

class AirplaneListView(generics.ListAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    #permission_classes = [AllowAny]

class IHAPieceListView(generics.ListAPIView):
    queryset = IHAPiece.objects.all()
    serializer_class = IHAPieceSerializer
    #permission_classes = [AllowAny]

class PieceByTypeView(generics.ListAPIView):
    serializer_class = IHAPieceSerializer

    def get_queryset(self):
        piece_type = self.kwargs.get('piece_type')
        return IHAPiece.objects.filter(piece_type=piece_type)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Bu türde parça bulunamadı."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)