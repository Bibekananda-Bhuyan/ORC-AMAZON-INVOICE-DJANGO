from django.shortcuts import render
import pdfplumber
import os
from  rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from django.conf import settings
import re
from rest_framework.renderers import JSONRenderer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Create your views here.
@api_view(["POST"])
def index(request):
    file_serializer = FileSerializer(data=request.data)

    if file_serializer.is_valid():

        docfile = request.FILES['invoice']
        baseDir = settings.BASE_DIR


        file_serializer.save()

        processdoc(str(baseDir)+"/documents/"+str(file_serializer.data["invoice"].split('/')[-1]),file_serializer.data["id"])
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def processdoc(pdoc,inid):
    with pdfplumber.open(pdoc) as pdf:
        page = pdf.pages[0]
        text = page.extract_text(x_tolerance=2)

    lines = text.split('\n')
    Total=getvalues(lines,"TOTAL",-1)
    Tax_amount=getvalues(lines,"TOTAL",-2)
    Invioce_no=getvalues(lines,"Invoice Number",-1)
    Pan_no=getvalues(lines,"PAN No",2)
    GSTIN=getvalues(lines,"GST Registration No",3)
    Invoice_date=getvalues(lines,"Invoice Date",3)
    Shipping_charge=getvalues(lines,"Shipping Charges",-1)
    Itemprice=lines[26].split()[-1]
    Itemname=lines[25]
    Itemq=lines[26].split()[3]

    cinvoice=Invoice.objects.get(id=inid)
    setInvoicedata=Invoicedata(invoice=cinvoice,invoice_total_price=Total,invoice_total_tax_price=Tax_amount,invoice_no=Invioce_no,
                               Pan_no=Pan_no,GSTIN=GSTIN,invoice_date=Invoice_date,Shipping_charge=Shipping_charge )
    setInvoiceitems=Invoiceitems(invoice=cinvoice,product_name=Itemname,product_qnty=Itemq,product_amount=Itemprice)

    try:
        setInvoicedata.save()
        setInvoiceitems.save()
        cinvoice.is_digitized_i = True
        cinvoice.save()
        return True
    except:
        cinvoice.is_digitized_i = False
        cinvoice.save()
        return False




def getvalues(lines,hint,myindex):
    olist = []
    for line in lines:
        if hint in line:
            olist.append(line)
    return (olist[0].split()[myindex])



@api_view(["POST"])
def trackinvoice(request):
    apiresponse = {}
    data = JSONParser().parse(request)

    if ("trackno" in data ):
        trackno=data['trackno']
        isdigitized=Invoice.objects.filter(trackingId=trackno,is_digitized_i="True").count()
        if isdigitized >0:
            cdigitizedd = Invoice.objects.get(trackingId=trackno, is_digitized_i="True")
            queryset = Invoicedata.objects.get(invoice=cdigitizedd)
            serializer = InvoicedataSerializer(queryset)
            queryset2 = Invoiceitems.objects.get(invoice=cdigitizedd)
            serializer2 = InvoiceitemsSerializer(queryset2)


            return Response(serializer.data)

        else:
            apiresponse['status'] = 101
            apiresponse['Details'] = "This Document Is Not Digitized"
            return Response(apiresponse)
    else:
        apiresponse['status'] = 106
        apiresponse['Details'] = "No Track No Passed"
        return Response(apiresponse)


@api_view(["POST"])
def updateinvoice(request):
    pass

@api_view(['PUT'])
def updateinvoice(request, id):
    try:
        invoicedata = Invoicedata.objects.get(id=id)
    except Invoicedata.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = InvoicedataSerializer(invoicedata, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data[SUCCESS] = UPDATE_SUCCESS
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE',])
def deleteinvoice(request, id):

	try:
		invoicedata = Invoicedata.objects.get(id=id)
	except Invoicedata.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		operation = invoicedata.delete()
		data = {}
		if operation:
			data[SUCCESS] = DELETE_SUCCESS
		return Response(data=data)