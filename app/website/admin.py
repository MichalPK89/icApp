from django.contrib import admin
from .models import Vat_payer, Vat_payer_setting, Customer_VAT_check

admin.site.register(Vat_payer)
admin.site.register(Vat_payer_setting)
admin.site.register(Customer_VAT_check) 
