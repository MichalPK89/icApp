from django.db import models

class Vat_payer (models.Model):
    DatumAktualizacieZoznamu = models.DateField()
    IC_DPH = models.CharField(max_length=20)
    ICO = models.CharField(max_length=20)
    NAZOV_DS = models.CharField(max_length=200)
    OBEC = models.CharField(max_length=100)
    PSC = models.CharField(max_length=10)
    ULICA_CISLO = models.CharField(max_length=100)
    STAT = models.CharField(max_length=20)
    DRUH_REG_DPH = models.CharField(max_length=5)
    DATUM_REG = models.DateField()
    DATUM_ZMENY_DRUHU_REG = models.DateField(blank=True, null=True,auto_now_add=False)

    def __str__(self):
        return(f"{self.NAZOV_DS}, {self.ICO}, {self.IC_DPH}, {self.DRUH_REG_DPH}, {self.DatumAktualizacieZoznamu}")