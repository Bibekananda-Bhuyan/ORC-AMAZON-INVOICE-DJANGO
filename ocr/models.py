from django.db import models
import string, random
# Create your models here.
def randomString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))



class Invoice(models.Model):
    invoice=models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    trackingId=models.CharField(max_length=100,default=randomString())
    is_digitized_i = models.BooleanField("Is Degitized",default=True)

class Invoicedata(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE,default="")
    invoice_total_price = models.CharField(max_length=100, default="")
    invoice_total_tax_price = models.CharField(max_length=100, default="")
    invoice_no=models.CharField(max_length=100,default="")
    Pan_no=models.CharField(max_length=100,default="")
    GSTIN=models.CharField(max_length=100,default="")
    invoice_date = models.CharField(default="" ,max_length=100)
    Shipping_charge=models.CharField(max_length=100,default="")




class Invoiceitems(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, default="")
    product_name=models.CharField(max_length=100,default="")
    product_qnty = models.CharField(max_length=100, default="")
    product_amount = models.CharField(max_length=100, default="")


