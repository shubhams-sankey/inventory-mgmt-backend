import json

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse, StreamingHttpResponse

from django.db.models import Subquery, OuterRef, F

from kafka import KafkaConsumer

from .models import *

@api_view(['POST'])
def registerVendor(req):
    try:
        req=json.loads(req.body)
        print(req)

        vendor = VendorDetails(firstname=req['firstname'], lastname=req['lastname'], email=req['email'] ,pincode=req['pincode'], address=req['address'])
        vendor.save()

        vendorLogin = VendorLogin(id=vendor, email=req['email'], password=req['password'])
        vendorLogin.save()

        resdata = {
            "success": "true",
            "message": "User Is Registered"
        }

        return JsonResponse(resdata, status=200)

    except Exception as e:
        JsonResponse({
            "message": "Something Went Wrong!",
        }, 500)
        print(e)


'''
API VIEW TO LOGIN VENDOR
'''
@api_view(['POST'])
def loginVendor(req):
    try:
        req = json.loads(req.body)
        print("Req ===> ", req)

        vendor = VendorDetails.objects.filter(email=req['email']).annotate(
            password = Subquery( VendorLogin.objects.filter(id=OuterRef('vendorid')).values('password')[:1] )
        ).values()[:1]

        # print("===> ", vendor[0])

        if not vendor.exists():
            return JsonResponse({
                "sucess": False,
                "message": "Email Not found ... "
            })
        
        vendor = vendor[0]

        if vendor['email'] == req['email'] :

            if vendor['password'] == req['password']:
                return JsonResponse({
                    "message": "Login Sucessfull",
                    "success": "True"
                })
            else:
                return JsonResponse({
                    "message": "Login Failed ... ",
                    "success": "False"
                })

        else:
            return JsonResponse({
                "message": "Email Not Found!"
            })

        # return JsonResponse({
        #     "success": True
        # })

    except Exception as e:
        JsonResponse({
            "message": "Something Went Wrong!",
        })
        print(e)


'''
API VIEW TO CREATE INVENTORY
'''    
@api_view(['POST'])
def createInventory(req):


    try:
        req = json.loads(req.body)
        print(req)

        vendordetails = VendorDetails.objects.get(vendorid=req['vendor_id'])
        # print(isinstance(vendordetails, VendorDetails))

        if not vendordetails:
            return JsonResponse({
                "message": "Vendor Details Not Found!"
            })

        inventory = InventoryDetail(inventory_title=req['title'], belongs_to=vendordetails, address=req['address'], pincode=req['pincode'])
        inventory.save()

        print("inventory ===> ", inventory)

        return JsonResponse({
            "message": "Inventory Created ..."
        })    


    except Exception as e:
        JsonResponse({
            "message": "Something Went Wrong!",
        })
        print(e)




@api_view(['POST'])
def getOrderDetails(req):

    try:

        req = json.loads(req.body)

        if req['vendorid'] is None:
            return JsonResponse({
                "message": "Bad Request! Vendorid Not Found"
            })
        

        consumer = KafkaConsumer(
            "order-placed",
            bootstrap_servers="localhost:9095",
            enable_auto_commit=True,
            auto_commit_interval_ms=1000
        )


        def orderDetailsEventStream():
            print("Calling Function .... ")

            # message = "data: "
            yield ""


            while True:

                print("Called Function ====> ")
                    
                # message = "test"

                # yield message
                # time.sleep(3)

                for cmessage in consumer:
                    print("============ Message Received ============= ")
                    # print ("%s:%d:%d: key=%s value=%s" % (cmessage.topic, cmessage.partition, cmessage.offset, cmessage.key, cmessage.value.decode('utf-8')))
                    
                    resmessage = cmessage.value.decode('utf-8')
                    # print("Message ===>  ", resmessage)
                    
                    yield f"data: {resmessage}\n\n"

 
                # yield message 


        response = StreamingHttpResponse(orderDetailsEventStream(), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = "no"  # Disable buffering in nginx

        return response
    
    except Exception as e:
        print(e)
