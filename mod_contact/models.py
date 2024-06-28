from django.db import models

class Contact(models.Model):
    """
        DESC : Modèle Contact
    """
    # Nom du contact
    nom = models.CharField(null=False, max_length=200)

    # Prénom du contact
    prenom = models.CharField(null=False, max_length=200)

    # Numéro de téléphone du contact
    phone = models.CharField(null=False, max_length=30)

    # Adresse du contact
    adresse = models.CharField(null=False, max_length=100)

    # Profession du contact
    profession = models.CharField(null=True, max_length=100)

    # Entreprise du contact
    entreprise = models.CharField(null=True, max_length=100)

    class Meta:
        # Table
        db_table = "mod_contact"
