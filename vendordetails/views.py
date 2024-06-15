import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

from django.db.models import Subquery, OuterRef, F

from .models import *

@api_view(['POST'])
def registerVendor(req):
    try:
        req=json.loads(req.body)
        print(req)

        vendor = VendorDetails(firsrname=req[''], lastname=req['lastname'], pincode=req['pincode'], address=req['address'])
        vendor.save()

        vendorLogin = VendorLogin(id=vendor, email=req['email'], password=req['password'])
        vendorLogin.save()

        resdata = {
            "success": "true",
            "message": "User Is Registered"
        }

        return JsonResponse(resdata, status=200)

    except Exception as e:
        print(e)


'''
API VIEW TO LOGIN VENDOR
'''
@api_view(['POST'])
def loginVendor(req):
    try:
        req = json.loads(req.body)

        vendor = VendorDetails.objects.filter(email=req['email']).annotate(
            password = Subquery( VendorLogin.objects.filter(id=OuterRef('vendorid')).values('password')[:1] )
        )

        print("===> ", vendor)

        return JsonResponse({
            "success": True
        })

    except Exception as e:
        print(e)
    