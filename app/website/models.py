from django.db import models

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