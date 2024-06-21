import json

from django.shortcuts import render
from django.http import JsonResponse
# from django.db.models import Subquery

from rest_framework.decorators import api_view

from .models import *
from users.models import UserTable

from .producer import produce_message

'''
API View To Create Category
'''
@api_view(['POST'])
def createNewCategory(req):
    try:
        
        req = json.loads(req.body)

        cateogory = CategoryDetails(category_name=req['category_name'])
        cateogory.save()

        return JsonResponse({
            "message": "Category Added!"
        })
    
    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Something Went Wrong!"
        })


'''
API View To View All Categories
'''
@api_view(['POST'])
def getAllCategories(req):
    
    try:

        # req = json.loads(req.body)

        categories = CategoryDetails.objects.values("category_name").all()

        if categories.exists():

            categories = list(categories)

            res_categories = []
            for cat in categories:
                print(cat)
                res_categories.append(cat['category_name'])

            return JsonResponse({
                "message": "",
                "data": res_categories
            })
        
        return JsonResponse({
            "message": "No Categories Listed Yet!"
        })

    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Something went wrong!"
        })
    

'''
API VIEW to add stock in inventory
'''
@api_view(['POST'])
def createStock(req):

    try:
        req = json.loads(req.body)

        # req => category_name, inventory_id, stock_name, 
        # stock_description, stock_price, quantity

        # Extract Category Id on Category Name
        category = CategoryDetails.objects.get( category_name=req['category_name'] )

        if not category:
            return JsonResponse({
                "message": "Category Not Found!"
            })
        
        print("Category ===> ", category)

        # Extract Inventory Based on Inventory_id
        inventory = InventoryDetail.objects.get(inventory_id=req['inventory_id'] )

        if not inventory:
            return JsonResponse({
                "message": "Inventory Not Found!"
            })
        
        print("Inventory ===> ", inventory)

        # Create Record for StockDetails
        stockDetails = StockDetails(categoryid=category, inventory_id=inventory, stock_title=req['stock_title'], stock_description=req['stock_description'], stock_price=req['stock_price'], quantity_available=req['quantity'])
        stockDetails.save()

        print("StockDetails ===>", stockDetails)

        return JsonResponse({
            "message": "Stock Created!"
        })


    except Exception as e:
        print("Error ===> ", e)
        return JsonResponse({
            "message": "Something Went Wrong!"
        })

'''
API VIEW to get Stock Detail at user level
'''
@api_view(['POST'])
def getStockDetailsForUser(req):
    try:
        req = json.loads(req.body)

        # Create Stock Data
        stocks = StockDetails.objects.values("stock_name", "stock_description", "stock_price", "quantity_available")
        
        if not stocks.exists():
            return JsonResponse({
                "message": "Stocks Not Found!"
            })

        resdata = list(stocks)

        return JsonResponse({
            "data": resdata
        })


    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Something Went Wrong!"
        })


'''
API VIEW to place order
'''
@api_view(['POST'])
def placeOrder(req):

    try:
        req = json.loads(req.body)

        # req => userid, stock id, quantity_ordered, payment_type

        # Extract User information who placed order
        user = UserTable.objects.get(userid=req['userid'])

        if not user:
            return JsonResponse({
                "message": "User Not Found!"
            })
        
        # Extract Stock Information
        stock_ordered = StockDetails.objects.get(stock_id=req['stock_id'])

        if not stock_ordered:
            return JsonResponse({
                "message": "Stock Not Found!"
            })
        
        # TODO: Check if stock can be ordered,
        # subtract current quantity from ordered quantity
        if int(stock_ordered.quantity_available) - int(req['quantity_ordered']) <= 0:
            return JsonResponse({
                "message": "Not Enough Stocks"
            })

        # Save updated quantity in StockDetails table
        stock_ordered.quantity_available = int(stock_ordered.quantity_available) - int(req['quantity_ordered'])
        stock_ordered.save()

        # Created Purchased History Record and return response
        newHistory = PurchasedHistory(
            purchased_userid=user,
            stock_id=stock_ordered,
            quantity_ordered=req['quantity_ordered'],
            payment_type=req['payment_type']
        )
        newHistory.save()
        # print("New History ===>", newHistory.)

        # Produce Kafka Message For this Order

        test = json.dumps({
            "purchased_id": str(newHistory.purchased_id),
            "purchased_userid": user.userid,
            "stock_id": stock_ordered.stock_id,
            "quantity_ordered": req['quantity_ordered'],
            "payment_type": req['payment_type'],
        })

        # print(test)

        produce_message(str(test))

        return JsonResponse({
            "message": "Order Placed ... "
        })

    except Exception as e:
        print(e)
        return JsonResponse({
            "message": "Something Went Wrong, "
        })