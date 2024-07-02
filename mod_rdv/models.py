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

    # Heure de début du Rdv
    heure_debut = models.TimeField(null=False, default=None)

    # Heure de fin du rdv
    heure_fin = models.TimeField(null=False, default=None)

    # Description du Rdv
    description = models.TextField(null=True)

    # COntact concerné
    contact = models.ForeignKey(
        Contact, related_name="contact_rdv", on_delete=models.CASCADE
    )

    class Meta:
        # Table
        db_table = "mod_rdv"
