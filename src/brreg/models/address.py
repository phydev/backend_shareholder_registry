import uuid
from typing import Any, Unpack

from django.db import models


class Address(models.Model):
    """
    Address entity, used to store address details.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    land = models.CharField(max_length=100, help_text="Land")
    landkode = models.CharField(max_length=20, help_text="Landkode")
    postnummer = models.CharField(max_length=20, help_text="Postnummer")
    poststed = models.CharField(max_length=100, help_text="Poststed")
    adresse = models.CharField(max_length=255, help_text="Gateadresse")
    kommune = models.CharField(max_length=100, help_text="Kommune")
    kommunenummer = models.CharField(max_length=20, help_text="Kommunenummer")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "address"

        unique_together = (
            "land",
            "landkode",
            "postnummer",
            "poststed",
            "adresse",
            "kommune",
            "kommunenummer",
        )

    def save(self, *args: Unpack[str], **kwargs: Unpack[str]) -> None:
        if type(self.adresse) is list:
            self.adresse = "; ".join(self.adresse)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.adresse}, {self.postnummer} {self.poststed}, {self.land}"
