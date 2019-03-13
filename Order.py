from collections import OrderedDict
import random, json, datetime

countries=['RU']



class Buyer(object):
    number=1

    def __init__(self):
        self.buyer_data=OrderedDict([('imId','buyer_imId'),('name', 'name_buyer_%s' % Buyer.number),('phone','123456789'),('email','buyer_%s@mail.com' % Buyer.number),('zipCode',187553),('address',self.generate_address())])
        Buyer.number+=1


    def generate_address(self):
        return OrderedDict([('country', random.choice(countries)), ('province', 'province_%s' % Buyer.number), ('city','city_buyer_%s' % Buyer.number), ('detailAddress', 'detailAddress_buyer_%s' % Buyer.number)])


class Parcel(object):

    def __init__(self, product_id, sku):
        self.price = random.randint(500,550)
        self.data = OrderedDict([('goodsList',OrderedDict([('productId', str(product_id)),('SKU', str(sku)),('quantity', 1),('price',self.price),('priceUnit', 'cent'),('priceCurrency', 'USD')]))])


class Order(object):

    def __init__(self, product_id,sku, order_id):
        parcel = Parcel(product_id,sku)
        self.data = json.dumps(OrderedDict([('orderID', str(order_id)),('buyer', Buyer().buyer_data),('parcel', parcel.data),('bizType',2),('packing',0)])).replace(' ', '')
        self.id = order_id
        self.weight = random.randint(100,120)
        self.price = parcel.price

    def __str__(self):
        return self.data


def answer_on_create_order(track_number):
    return OrderedDict([('trackingNumber', track_number), ('trackingDescription', 'Order creation'), ('opTime', str(datetime.datetime.now().replace(microsecond=0))),('timeZone', '+03:00'), ('tariff', 150), ('tariffUnit','cent'),('tariffCurrency', 'USD')])


def create_event(event, tracking_number, order_id):
    print('Create event for order %s' % order_id)
    with open('Orders.txt', 'r') as f:
        data = json.loads(f.read())
        #print('Orders.txt: %s' % data)
    event_info = {'trackingNumber' : tracking_number, 'trackingDescription' : '_'.join(event.split('_')[2:]), 'opTime': str(datetime.datetime.now().replace(microsecond=0)), 'timeZone': '+03:00', 'opLocation':'Riga'}
    if event == 'PBM_EP_Order_Fulfilled':
        external_filds = {'orderId': order_id, 'updateTariff': 155, 'updateTariffUnit':'cent', 'updateTariffCurrency': 'USD', 'updateWeight': data[str(order_id)]['weight'], 'updateWeightUnit': 'g'}
        event_info.update(external_filds)
    return json.dumps(event_info)



