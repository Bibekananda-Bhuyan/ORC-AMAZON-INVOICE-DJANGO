from django.contrib import admin

# Register your models here.
from  .models import *
# Register your models here.

admin.site.register(Invoice)
admin.site.register(Invoicedata)
admin.site.register(Invoiceitems)