from collections import OrderedDict
import random, json, datetime

countries=['RU']


class Buyer(object):
    number=1

    def __init__(self):
        self.buyer_data=OrderedDict([('img','buyer_img'),('name', 'name_buyer_%s' % Buyer.number),('phone','123456789'),('email','buyer_%s@mail.com' % Buyer.number),('zipCode',187553),('address',self.generate_address())])
        Buyer.number+=1


    def generate_address(self):
        return OrderedDict([('country', random.choice(countries)), ('province', 'province_%s' % Buyer.number), ('city','city_buyer_%s' % Buyer.number), ('detailAddress', 'detailAddress_buyer_%s' % Buyer.number)])


class Parcel(object):

    def __init__(self, product_id, sku):
        self.data = OrderedDict([('goodsList',OrderedDict([('productId', str(product_id)),('SKU', str(sku)),('quantity', 1),('price',100),('priceUnit', 'cent'),('priceCurrency', 'USD')]))])


class Order(object):
    num_order=1

    def __init__(self, product_id,sku):
        self.data = json.dumps(OrderedDict([('orderID', str(Order.num_order)),('buyer', Buyer().buyer_data),('parcel',Parcel(product_id,sku).data),('bizType',2),('packing',0)])).replace(' ', '')
        self.id = Order.num_order
        Order.num_order+=1

    def __str__(self):
        return self.data

    @staticmethod
    def answer_on_create_order(track_num):
        return json.dumps(OrderedDict([('trackingNumber', track_num), ('trackingDescription', 'Order creation'), ('opTime', str(datetime.datetime.now().replace(microsecond=0))),('timeZone', '+03:00'), ('tariff', 150), ('tariffUnit','cent'),('tariffCurrency', 'USD')]))

    @staticmethod
    def create_event(event, tracking_number,order_id):
        event = {'trackingNumber' : tracking_number, 'trackingDescription' : '_'.join(event.split('_')[2:]), 'opTime': str(datetime.datetime.now().replace(microsecond=0)), 'timeZone': '+03:00', 'opLocation':'Riga'}
        if event == 'PBM_EP_Order_Fulfill':
            external_filds = {'orderId': order_id, 'updateTariff': 155, 'updateTariffUnit':'cent', 'updateTariffCurrency': 'USD', 'updateWeight': 25, 'updateWeightUnit': 'g'}
            event.update(external_filds)
        return json.dumps(event)



