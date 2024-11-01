from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class Item(models.Model):
    identifier = models.CharField(max_length=100, unique=True)  # Unique identifier for the item

    def __str__(self):
        return(f"{self.identifier}")

class ItemTranslation(models.Model):
    item = models.ForeignKey(Item, related_name="translations", on_delete=models.CASCADE)
    language_code = models.CharField(max_length=2)  # e.g., "en", "fr", "de"
    name = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'language_code'], name='unique_item_language_code')
        ]

    def __str__(self):
        return(f"{self.item}, {self.language_code}, {self.name}")

class Vat_payer (models.Model):
    DatumAktualizacieZoznamu = models.DateField()
    IC_DPH = models.CharField(max_length=20, blank=True, null=True)
    ICO = models.CharField(max_length=20, blank=True, null=True)
    NAZOV_DS = models.CharField(max_length=200, blank=True, null=True)
    OBEC = models.CharField(max_length=100, blank=True, null=True)
    PSC = models.CharField(max_length=10, blank=True, null=True)
    ULICA_CISLO = models.CharField(max_length=100, blank=True, null=True)
    STAT = models.CharField(max_length=50, blank=True, null=True)
    DRUH_REG_DPH = models.CharField(max_length=5, blank=True, null=True)
    DATUM_REG = models.DateField(blank=True, null=True, auto_now_add=False)
    DATUM_ZMENY_DRUHU_REG = models.DateField(blank=True, null=True, auto_now_add=False)

    def __str__(self):
        return(f"{self.NAZOV_DS}, {self.ICO}, {self.IC_DPH}, {self.DRUH_REG_DPH}, {self.DatumAktualizacieZoznamu}")

class Vat_payer_setting (models.Model):
    id = models.AutoField(primary_key=True)
    DRUH_REG_DPH = models.CharField(max_length=5, unique=True, blank=False, null=False)
    PLATNY_DRUH_REG = models.BooleanField()
    
    def __str__(self):
        return(f"{self.DRUH_REG_DPH}, {self.PLATNY_DRUH_REG}")
    
class Customer (models.Model):
    NAZOV = models.CharField(max_length=200, blank=False, null=False)
    ICO = models.CharField(max_length=20, blank=True, null=True)
    DIC = models.CharField(max_length=20, blank=True, null=True)
    IC_DPH = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return(f"{self.ICO}, {self.NAZOV}")

class Customer_VAT_check (models.Model):
    ID = models.AutoField(primary_key=True)
    NAZOV = models.CharField(max_length=200, blank=False, null=False)
    ICO = models.CharField(max_length=20, blank=True, null=True)
    IC_DPH_customer = models.CharField(max_length=20, blank=True, null=True)
    IC_DPH_fin = models.CharField(max_length=20, blank=True, null=True)
    DRUH_REG_DPH = models.CharField(max_length=10, blank=True, null=True)
    DESCRIPTION = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        # The name of the view in the database
        db_table = 'customer_vat_check'
        managed = False  # No migrations will be created for this model since it refers to a view

class VAT_type_undefined (models.Model):
    DRUH_REG_DPH = models.CharField(max_length=10, blank=False, null=False)
        
    class Meta:
        # The name of the view in the database
        db_table = 'vat_type_undefined'
        managed = False  # No migrations will be created for this model since it refers to a view

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    row_limit = models.PositiveIntegerField(default=1000)
    
    def __str__(self):
        return (f"{self.user}, {self.row_limit}")

    