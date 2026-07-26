import uuid

from django.db import models


class Company(models.Model):
    """
    Company entity, can be part of registries and hierarchical relations.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    navn = models.CharField(max_length=255, help_text="Selskapsnavn")
    organisasjonsnummer = models.CharField(
        max_length=9,
        unique=True,
        blank=False,
        help_text="Organisasjonsnummer",
    )

    industry = models.ForeignKey(
        "brreg.Industry",
        on_delete=models.SET_NULL,
        related_name="Industry",
        null=True,
        help_text="Næringskode for selskapet",
    )

    postadresse = models.ForeignKey(
        "brreg.Address",
        on_delete=models.SET_NULL,
        related_name="Postadresse",
        null=True,
    )
    forretningsadresse = models.ForeignKey(
        "brreg.Address",
        on_delete=models.SET_NULL,
        related_name="Forretningsadresse",
        null=True,
    )

    legal_form = models.ForeignKey(
        "brreg.LegalForm",
        on_delete=models.SET_NULL,
        null=True)

    industry = models.ManyToManyField("brreg.Industry", blank=True)

    activity = models.ForeignKey("brreg.Activity", blank=True, on_delete=models.SET_NULL, null=True)

    status = models.ForeignKey("brreg.Status", on_delete=models.CASCADE, null=True)

    foundation_date = models.DateField(blank=True, null=True, help_text="Stiftelsesdato")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "company"
        app_label = "brreg"

    def __str__(self) -> str:
        return self.navn
