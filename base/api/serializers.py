from rest_framework.serializers import ModelSerializer
from base.models import Room #The reason why its not just '.' is because we are in a folder outside the 'base'



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'