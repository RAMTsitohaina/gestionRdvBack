from rest_framework import serializers

from mod_rdv.models import Rdv

class RdvSerializers(serializers.ModelSerializer):
    """
        DESV : Class permettant la serialisation de l'objet Rdv
    """
    class Meta:
        model = Rdv
        fields = '__all__'