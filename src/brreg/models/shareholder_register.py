import uuid

from django.db import models

class ShareholderRegister(models.Model):
    """
    Model representing a shareholder register entry.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orgnr = models.CharField(max_length=20, help_text='Organisasjonsnummer')
    selskap = models.CharField(max_length=255, help_text='Navn på selskap beholdningen eies i')
    aksjeklasse = models.CharField(max_length=100, help_text='Aksjeklasse eller isin for aksjeklassen')
    foedselsaar_orgnr = models.CharField(max_length=9, help_text='Fødselsår for aksjonærer identifisert i '
                                                                  'folkeregisteret eller organisasjonsnummer for '
                                                                  'selskapsaksjonærer')
    postnr_sted = models.CharField(max_length=100, help_text='Postnummer og poststed for aksjonærer identifisert av'
                                                             ' folkeregisteret eller av enhetsregisteret')
    landkode = models.CharField(max_length=3, help_text='Landkode')
    navn_aksjonaer = models.CharField(max_length=255, help_text='Navn på aksjonær')
    antall_aksjer = models.IntegerField(help_text='Antall aksjer ved utgangen av inntektsåret')
    antall_aksjer_selskap = models.IntegerField(help_text='Antall aksjer totalt i selskap')


    class Meta:
        db_table = "shareholder_register"
        verbose_name = "Aksjonærregister"

    def __str__(self) -> str:
        return f"{self.navn_aksjonaer} - {self.selskap} ({self.aksjeklasse})"