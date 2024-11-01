from django.contrib import admin
from .models import Item, ItemTranslation, Vat_payer, Vat_payer_setting, Customer_VAT_check, UserSettings

admin.site.register(UserSettings)
admin.site.register(Item)
admin.site.register(ItemTranslation)
admin.site.register(Vat_payer)
admin.site.register(Vat_payer_setting)
admin.site.register(Customer_VAT_check)
