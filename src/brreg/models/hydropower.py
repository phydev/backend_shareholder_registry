import uuid

from django.db import models
from django.core.validators import MinValueValidator


class HydropowerPlant(models.Model):

    class VannkraftverkType(models.TextChoices):
        KRAFTVERK = 'K', 'Kraftverk'
        PUMPE = 'P', 'Pumpe'
        PUMPEKRAFTVERK = 'PK', 'Pumpekraftverk'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    loepenummer = models.PositiveIntegerField(
        help_text='Kraftverk Løpenummer',
        validators=[MinValueValidator(1)]
    )
    navn = models.CharField(
        help_text='Navn',
        max_length=255,
        blank=False
    )
    vannkraftverk_type = models.CharField(
        choices=VannkraftverkType.choices,
        max_length=2,
        help_text="Kraftverk type",
        blank=False
    )

    hovedeier = models.CharField(
        help_text='Hovedeier',
        max_length=255,
        blank=False
    )
    hovedeier_orgnr = models.CharField(
        help_text='Hovedeier OrgNr',
        max_length=9
    )
    fylke = models.CharField(
        help_text='Fylke',
        max_length=100,
        blank=False
    )
    fylkesnr = models.PositiveSmallIntegerField(
        help_text='Fylkesnr',
        validators=[MinValueValidator(1)]
    )
    kommune = models.CharField(
        help_text='Kommune',
        max_length=100,
        blank=False
    )
    kommunenr = models.PositiveIntegerField(
        help_text='Kommunenr',
        validators=[MinValueValidator(1)]
    )
    forsteutnyttelseavfalletdato = models.PositiveIntegerField(
        help_text='Første utnyttelse av fallet år',
        null=True,
        blank=True,
        validators=[MinValueValidator(1800)]  # Reasonable minimum year
    )
    datoforeldstekraftproduserendedel = models.PositiveIntegerField(
        help_text='År for eldste kraftproduserende del',
        null=True,
        blank=True,
        validators=[MinValueValidator(1800)]
    )
    maksytelse = models.FloatField(
        help_text='Maks ytelse (MW)',
        validators=[MinValueValidator(0.0)]
    )
    midprod_91_20 = models.FloatField(
        help_text='Midprod 1991-2020 (GWh)',
        validators=[MinValueValidator(0.0)]
    )
    bruttofallhoyde_m = models.FloatField(
        help_text='Brutto fallhøyde (m)',
        validators=[MinValueValidator(0.0)],
        null=True,
        blank=True
    )
    slukeevne = models.FloatField(
        help_text='Slukeevne (m3/s)',
        validators=[MinValueValidator(0.0)],
        null=True,
        blank=True
    )
    enekv = models.FloatField(
        help_text='Enekv (m3/s)',
        validators=[MinValueValidator(0.0)],
        null=True,
        blank=True
    )
    elspotomraadenummer = models.PositiveSmallIntegerField(
        help_text='Elspot område nummer'
    )
    reginenr = models.CharField(
        help_text='Regine nr',
        max_length=50
    )
    eridrift = models.BooleanField(
        help_text='Er i drift',
        default=True
    )
    idriftdato = models.DateField(
        help_text='I drift dato',
        null=True,
        blank=True
    )
    konsesjoner = models.TextField(
        help_text='Konsesjoner',
        blank=True
    )
    kraftverkstatus = models.CharField(
        help_text='Kraftverk status',
        max_length=500,
        blank=True
    )
    nedborsfeltnavn = models.CharField(
        help_text='Nedbørsfeltnavn',
        max_length=255,
        blank=True
    )
    sppunkt = models.CharField(
        help_text='SPPunkt',
        max_length=255,
        blank=True
    )
    spsone = models.CharField(
        help_text='SPSone',
        max_length=255,
        blank=True
    )
    underbygging = models.TextField(
        help_text='Underbygging',
        blank=True
    )
    uteavdrift = models.BooleanField(
        help_text='Ute av drift',
        default=False
    )
    vassdragsomraadeid = models.PositiveIntegerField(
        help_text='Vassdragsområde ID'
    )
    vassdragsomraadenavn = models.CharField(
        help_text='Vassdragsområde navn',
        max_length=255,
        blank=False
    )

    class Meta:
        verbose_name = 'Hydropower Plant'
        verbose_name_plural = 'Hydropower Plants'
        ordering = ['navn']
        db_table = 'hydropower'

    def __str__(self):
        return f"{self.navn} ({self.loepenummer})"
