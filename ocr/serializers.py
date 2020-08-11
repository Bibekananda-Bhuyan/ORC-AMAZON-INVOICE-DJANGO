from rest_framework import serializers
from .models import *

class Invoicedataser(serializers.ModelSerializer):
    class Meta:
        model=Invoicedata
        fields= "__all__"

class Invoiceitemsser(serializers.ModelSerializer):
    class Meta:
        model=Invoiceitems
        fields= "__all__"



class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Invoice
        fields= ['id','trackingId','invoice']


class InvoiceitemsSerializer(serializers.ModelSerializer):

    class Meta:
        model=Invoiceitems
        fields= "__all__"
        depth = 1

class InvoicedataSerializer(serializers.ModelSerializer):

    class Meta:
        model=Invoicedata
        fields= "__all__"
        depth = 2
