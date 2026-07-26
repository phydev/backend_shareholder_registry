import json
import csv
from typing import TypedDict, Unpack
import requests

from pydantic import BaseModel, field_validator
import datetime

from ..models import Address, Company, Industry, Activity, LegalForm, Status, HydropowerPlant, ShareholderRegister



class Options(TypedDict):
    source: str
    limit: int


class Adresse(BaseModel):
    land: str | None = "Missing"
    landkode: str | None = "XX"
    postnummer: str | None = "0000"
    poststed: str | None = "Missing"
    adresse: str | None = "Missing"
    kommune: str | None = "Missing"
    kommunenummer: str | None = "0000"

    @field_validator("adresse", mode="before")
    def validate_adresse(cls, v: list[str]) -> str:
        if isinstance(v, list):
            return "; ".join(v)
        return v

class Shareholder(BaseModel):
    """
    Model for shareholder data.
    """
    orgnr: str
    selskap: str
    aksjeklasse: str
    navn_aksjonaer: str
    foedselsaar_orgnr: str
    postnr_sted: str
    landkode: str
    antall_aksjer: int
    antall_aksjer_selskap: int


def ingest_hydropower_from_api():
    """
    Ingest hydropower plant data from NVE API to database.
    """

    url = "https://api.nve.no/web/Powerplant/GetHydroPowerPlantsInOperation"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for n, item in enumerate(data):
            print(f"{n}: {item.get('Navn', 'Unknown')}")

            # Map API response to model fields with correct column names
            hydropower_data = {
                'loepenummer': item.get('VannKraftverkID'),
                'navn': item.get('Navn', ''),
                'vannkraftverk_type': item.get('VannKVType', ''),
                'hovedeier': item.get('HovedEier', ''),
                'hovedeier_orgnr': item.get('HovedEier_OrgNr'),
                'fylke': item.get('Fylke', ''),
                'fylkesnr': item.get('FylkesNr'),
                'kommune': item.get('Kommune', ''),
                'kommunenr': item.get('KommuneNr'),
                'forsteutnyttelseavfalletdato': item.get('ForsteUtnyttelseAvFalletDato'),
                'datoforeldstekraftproduserendedel': item.get('DatoForEldsteKraftproduserendeDel'),
                'maksytelse': item.get('MaksYtelse'),
                'midprod_91_20': item.get('MidProd_91_20'),
                'bruttofallhoyde_m': item.get('BruttoFallhoyde_M'),
                'slukeevne': item.get('Slukeevne'),
                'enekv': item.get('EnEkv'),
                'elspotomraadenummer': item.get('ElspotomraadeNummer'),
                'reginenr': item.get('RegineNr'),
                'eridrift': item.get('ErIDrift', True),
                'idriftdato': parse_date(item.get('IDriftDato')),
                'konsesjoner': item.get('Konsesjoner', ''),
                'kraftverkstatus': item.get('Kraftverkstatus', ''),
                'nveomraadeid': item.get('NVEOmraadeID'),
                'nveomraadenavn': item.get('NVEOmraadeNavn', ''),
                'nedborsfeltnavn': item.get('Nedborsfeltnavn', ''),
                'sppunkt': item.get('SPPunkt', ''),
                'spsone': item.get('SPSone', ''),
                'underbygging': item.get('UnderBygging', ''),
                'uteavdrift': item.get('UteAvDrift', False),
                'vassdragsomraadeid': item.get('VassdragsOmraadeID'),
                'vassdragsomraadenavn': item.get('VassdragsOmraadeNavn', ''),
            }

            # Filter out None values
            hydropower_data = {k: v for k, v in hydropower_data.items() if v is not None}

            # Get or create hydropower plant
            hydropower, created = HydropowerPlant.objects.get_or_create(
                loepenummer=hydropower_data['loepenummer'],
                defaults=hydropower_data
            )

            if not created:
                # Update existing record
                for key, value in hydropower_data.items():
                    setattr(hydropower, key, value)
                hydropower.save()

            print(f"{'Created' if created else 'Updated'}: {hydropower.navn}")

    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")


def parse_date(date_string):
    """
    Parse date string from API to datetime.date object.
    """
    if not date_string:
        return None

    try:
        # Assuming ISO format, adjust if needed
        return datetime.datetime.fromisoformat(date_string.replace('Z', '+00:00')).date()
    except (ValueError, AttributeError):
        return None





def ingest_shareholder_register():
    """
    Ingest shareholder register data from CSV file to database.
    """

    with open("data/askjeiebok_kraft_2024.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=';')

        for n, row in enumerate(reader):
            print(f"{n}: {row['Selskap']} - {row['Navn aksjonær']}")

            shareholder_data = Shareholder(
                orgnr=row["Orgnr"],
                selskap=row["Selskap"],
                aksjeklasse=row["Aksjeklasse"],
                navn_aksjonaer=row["Navn aksjonær"],
                foedselsaar_orgnr=row["Fødselsår/orgnr"],
                postnr_sted=row["Postnr/sted"],
                landkode=row["Landkode"],
                antall_aksjer=int(row["Antall aksjer"]),
                antall_aksjer_selskap=int(row["Antall aksjer selskap"]),
            )

            shareholder, created = ShareholderRegister.objects.get_or_create(
                orgnr=shareholder_data.orgnr,
                selskap=shareholder_data.selskap,
                aksjeklasse=shareholder_data.aksjeklasse,
                navn_aksjonaer=shareholder_data.navn_aksjonaer,
                defaults=shareholder_data.model_dump()
            )

            if not created:
                # Update existing record
                for key, value in shareholder_data.model_dump().items():
                    setattr(shareholder, key, value)
                shareholder.save()

            print(f"{'Created' if created else 'Updated'}: {shareholder.selskap} - {shareholder.navn_aksjonaer}")


def ingest(**options: Unpack[Options]) -> None:
    if options["source"] == "enhetsregisteret":

        ingest_hydropower_from_api()
        ingest_shareholder_register()

        with open("data/enheter_kraft.json", "r+", encoding="utf-8") as file:
            data = json.load(file)

        for n, item in enumerate(data):
            #print(f"{n}: {item['navn']}")
            if "postadresse" in item.keys():
                postadresse_val = Adresse(**item["postadresse"])
                postadresse, _ = Address.objects.get_or_create(**postadresse_val.model_dump())
            else:
                postadresse, _ = Address.objects.get_or_create(**Adresse().model_dump())

            if "forretningsadresse" in item.keys():
                forretningsadresse_val = Adresse(**item["forretningsadresse"])
                forretningsadresse, _ = Address.objects.get_or_create(**forretningsadresse_val.model_dump())
            else:
                forretningsadresse, _ = Address.objects.get_or_create(**Adresse().model_dump())

            company, _ = Company.objects.get_or_create(organisasjonsnummer=item["organisasjonsnummer"])
            company.navn = item["navn"]
            foundation_date = item["stiftelsesdato"].split("-") if item.get("stiftelsesdato") else ["1900","01","01"]
            company.foundation_date = datetime.date(year=int(foundation_date[0]),
                                                    month=int(foundation_date[1]),
                                                    day=int(foundation_date[2]))
            company.postadresse_id = postadresse.pk
            company.forretningsadresse_id = forretningsadresse.pk


            industry, _ = Industry.objects.get_or_create(
                code=item.get("naeringskode1", {}).get("kode"),
                description=item.get("naeringskode1", {}).get("beskrivelse"),
            )
            company.industry.add(industry)

            industry, _ = Industry.objects.get_or_create(
                code=item.get("naeringskode2", {}).get("kode"),
                description=item.get("naeringskode2", {}).get("beskrivelse"),
            )
            company.industry.add(industry)


            purpose = ''.join(item.get('vedtektsfestetFormaal', ['']))
            description = ''.join(item.get('aktivitet', ['']))

            if purpose != description and purpose != '':
                description = f"{purpose}; {description}"

            activity, _ = Activity.objects.get_or_create(
                description=description
            )

            company.activity = activity

            legal_form, _ = LegalForm.objects.get_or_create(code=item.get("institusjonellSektorkode", {}).get("kode"),
                                                            description=item.get(
                                                                "institusjonellSektorkode", {}).get("beskrivelse"))

            company.legal_form = legal_form


            status, _ = Status.objects.get_or_create(
                bankruptcy= bool(item.get("konkurs")),
                under_liquidation= bool(item.get("underAvvikling")),
                under_compulsory_liquidation_or_dissolution = bool(item.get(
                    "underTvangsavviklingEllerTvangsopplosning")),
                registered_in_business_register= bool(item.get("registrertIFrivillighetsregisteret")),
                registered_in_establishment_register= bool(item.get("registrertIStiftelsesregisteret")),
                registered_in_voluntary_register= bool(item.get("registrertIFrivillighetsregisteret")),
                last_annual_report_submitted= datetime.date(int(item.get("sisteInnsendteAarsregnskap",1900)), 1, 1)
            )


            company.status = status

            company.save()

            #if n == options["limit"]-1:
            #    break

