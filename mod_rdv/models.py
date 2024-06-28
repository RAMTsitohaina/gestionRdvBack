from django.db import models

from mod_contact.models import Contact

class Rdv (models.Model):
    """
        DESC : Modèle Rendez-vous
    """
    # Titre du Rdv
    titre = models.CharField(null=False, max_length=100)

    # Date du Rdv
    date = models.DateField(null=False)

    # Heure du Rdv
    heure = models.TimeField(null=False)

    # Description du Rdv
    description = models.TextField(null=True)

    # COntact concerné
    contact = models.ForeignKey(
        Contact, related_name="contact_rdv", on_delete=models.CASCADE
    )

    class Meta:
        # Table
        db_table = "mod_rdv"
