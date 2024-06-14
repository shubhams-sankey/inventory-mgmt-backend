import json

from rest_framework.decorators import api_view
from django.shortcuts import render

from django.http import JsonResponse

from .models import *

# Create your views here.

'''
API VIEW TO REGISTER USER
'''

@api_view(['POST'])
def registerNewUser(req):
    try:
        
        req=json.loads(req.body)
        print(req)

        # Logic To Register User

        # Create Entry In User Table
        user = UserTable(firstname=req['firstname'], lastname=req['lastname'], email=req['email'], pincode=req['pincode'])
        user.save()
        print("User===> ", user.userid)

        # Create Foregin Key Relation In UserLoginTable
        userLogin = UserLoginTable(id=user, email=req['email'], password=req['password'])
        userLogin.save()
        print("user login ===> ", userLogin)

        resdata = {
            "success": "true",
            "message": "User is Registered"
        }

        return JsonResponse(resdata, status=200)


    except Exception as e:
        print(e)


'''
API VIEW TO LOGIN USER
'''
@api_view(['POST'])
def loginUser(req):
    try: 
        req = json.loads(req.body)

        user = UserTable.objects.filter(email=req['email']).values().all()[0]

        print("=====> User: ", user['userid'])

        if not user:
            return JsonResponse({
                "sucess": False,
                "message": "User Not Found"
            })
        
        userLogin = UserLoginTable.objects.filter(id=user['userid']).values().all()[0]

        print("===> userLogin: ", userLogin)

        if userLogin['password'] == req['password']:
            return JsonResponse({
                "sucess": True,
                "message": "Login Successful!"
            })
        
        return JsonResponse({
                "sucess": False,
                "message": "Something Went Wrong"
            })

    except Exception as e:
        print(e)
