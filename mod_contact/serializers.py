from rest_framework import serializers

from mod_contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
        DESC : Class permettant la serialisation de l'objet Contac
    """
    class Meta:
        model = Contact
        fields = '__all__'