import json
import time

import requests
from django.core.exceptions import ValidationError
from django.http import request, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm, NameForm
from smartapi.smartConnect import SmartConnect
#from authapp import sockeyweb
import threading


# Create your views here.
from .models import UserRegistrationModel, Order, stockDetails


@login_required
def orderplace(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        symbol = request.POST['symbol']
        amount = request.POST['amount']
        stoploss = request.POST['stoploss']
        profit = request.POST['profit']
        exch = request.POST['exch_seg']
        lotsize = request.POST['lotsize']
        limitvalue = request.POST['limitvalue']
        limitvalueres = int(lotsize) * int(limitvalue)
        ttype = request.POST['ttype']
        token = int(request.POST['token'])
        fav_language = request.POST['fav_language']
        name = request.POST['name']

        obj = SmartConnect(api_key="33KgzBX0")
        data = obj.generateSession("DIYD12736","Alone@1987")
        refreshToken= data['data']['refreshToken']

        #fetch the feedtoken
        feedToken=obj.getfeedToken()

        r = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")

        # extracting data in json format
        datas = r.json()

        result = {}
        for d in datas:
            #st = stockDetails(token=d['token'], symbol=d['symbol'], expiry=d['expiry'], strike=d['strike'], lotsize=d['lotsize'], instrumenttype=d['instrumenttype'], exch_seg=d['exch_seg'], tick_size=d['tick_size'])
            #st.save()
            if d['symbol']==name:
                print("find")
                result = d

        ltp = obj.ltpData(exch,symbol,token)

        excres = ltp['data']
        am = int(excres['ltp'])

        nameltp = obj.ltpData(result['exch_seg'],result['symbol'],result['token'])

        print(nameltp)
        if fav_language == 'number':
            print('number')
            p = Order(user=request.user, symbol=symbol, token=token, exc=exch, ttype=ttype, number=amount, profit=profit,limitvalue=limitvalueres, sl=stoploss, name=name,name_ltp=nameltp, symbol_ltp=am, amount='',result=result)
            p.save()
            t1 = threading.Thread(target=startchecking,args=(p.id,))
            t1.start()
            res = True
        else:
            res = order_place(token,symbol,stoploss,exch,ttype,amount,limitvalueres,profit)

        if res == True:
            return HttpResponseRedirect('/dashboard/')

    return None


def startchecking(id):
        ord = Order.objects.get(id=id)
        result = ord.result
        result = result.replace("\'", '"').replace("False", "false")
        res = json.loads(result)
        obj = SmartConnect(api_key="33KgzBX0")
        data = obj.generateSession("DIYD12736","Alone@1987")
        while True:
            nameltp = obj.ltpData(res['exch_seg'],res['symbol'],res['token'])
            exc = nameltp['data']
            time.sleep(1)
            if int(exc['ltp']) == int(ord.number):
                print('grand success')
                ltp = obj.ltpData(ord.exc,ord.symbol,ord.token)
                excres = ltp['data']
                am = int(excres['ltp'])
                order_place(ord.token,ord.symbol,ord.sl,ord.exc,ord.ttype,am,ord.limitvalue,ord.profit)
                break
            print('Thread started'+str(ord.id))


@login_required
def order(request):
    r = requests.get("https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json")

    # extracting data in json format
    data = r.json()
    print(len(data))
    records = stockDetails.objects.all()
    records.delete()

    res = None
    if request.method == 'POST':
        symbol = request.POST['tags']
        for d in data:
            #st = stockDetails(token=d['token'], symbol=d['symbol'], expiry=d['expiry'], strike=d['strike'], lotsize=d['lotsize'], instrumenttype=d['instrumenttype'], exch_seg=d['exch_seg'], tick_size=d['tick_size'])
            #st.save()
            if d['symbol']==symbol:
                print("find")
                res = d
    # sending get request and saving the response as response object

    context = {
        "datas": data,
        "res": res
    }
    return render(request, 'authapp/order.html', context=context)


def order_place(token,symbol,stoploss,exchange,ttype,amount,limitvalue,profit):
    #create object of call
    obj = SmartConnect(api_key="33KgzBX0")
    data = obj.generateSession("DIYD12736","Alone@1987")
    refreshToken= data['data']['refreshToken']

    #fetch the feedtoken
    feedToken=obj.getfeedToken()

    #fetch User Profile
    userProfile= obj.getProfile(refreshToken)
    #place order
    try:
        orderparams = {
            "variety":"ROBO",
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": ttype,
            "exchange": exchange,
            "ordertype": "LIMIT",
            "producttype": "BO",
            "duration": "DAY",
            "price": amount,
            "triggerprice": 0,
            "squareoff": profit,
            "stoploss": stoploss,
            "quantity": limitvalue,
        }
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
        return True
    except Exception as e:
        print("Order placement failed: {}".format(e.message))
        return False


@login_required
def dashboard(request):
    user_reg = UserRegistrationModel.objects.get(user=request.user.id)
    if user_reg.angelonestatus == 0:
        return redirect('/angellogin')
    context = {
        "data": user_reg
        }
    return render(request, 'authapp/dashboard.html', context=context)


@login_required
def angellogin(request):
    user_reg = UserRegistrationModel.objects.get(user=request.user.id)
    out = ""
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        #create object of call
        obj=SmartConnect(api_key="33KgzBX0")

        #login api call

        # check whether it's valid:
        if form.is_valid():
            id = form.cleaned_data.get('clientid')
            try:
                data = obj.generateSession(form.cleaned_data.get('clientid'),form.cleaned_data.get('password'))
                if data['message']=='SUCCESS':
                    refreshToken= data['data']['refreshToken']
                    result = data['data']
                    clientcode = result['clientcode']
                    userProfile= obj.getProfile(refreshToken)
                    user_reg.angelonestatus=1
                    user_reg.client_code = clientcode
                    user_reg.angelname = data['data']['name']
                    user_reg.angelmobile = data['data']['mobileno']
                    user_reg.token = refreshToken
                    user_reg.angelemail = data['data']['email']
                    user_reg.save()
                    return HttpResponseRedirect('/dashboard/')
                    #return HttpResponseRedirect('/dashboard/')

                else:

                    out = "Invalid User please check your angel account"
            except Exception as e:
                out = "invalid cred"

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    context = {
        "res": out
    }
    return render(request, 'authapp/angellogin.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)
