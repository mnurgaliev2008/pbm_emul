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
    price = 100

    def __init__(self, product_id, sku):
        self.data = OrderedDict([('goodsList',OrderedDict([('productId', str(product_id)),('SKU', str(sku)),('quantity', 1),('price',Parcel.price),('priceUnit', 'cent'),('priceCurrency', 'USD')]))])
        Parcel.price += 1


order_weight = {}
order_price = {}


class Order(object):

    num_order = 1
    weight = 1000

    def __init__(self, product_id,sku):
        parcel = Parcel(product_id,sku).data
        self.data = json.dumps(OrderedDict([('orderID', str(Order.num_order)),('buyer', Buyer().buyer_data),('parcel', parcel),('bizType',2),('packing',0)])).replace(' ', '')
        self.id = Order.num_order
        order_weight[self.id] = Order.weight
        order_price[self.id] = parcel['goodsList']['price']
        Order.weight += 10
        Order.num_order += 1
        print(order_weight)
        print(order_price)

    def __str__(self):
        return self.data


def answer_on_create_order(track_number):
    return OrderedDict([('trackingNumber', track_number), ('trackingDescription', 'Order creation'), ('opTime', str(datetime.datetime.now().replace(microsecond=0))),('timeZone', '+03:00'), ('tariff', 150), ('tariffUnit','cent'),('tariffCurrency', 'USD')])


def create_event(event, tracking_number, order_id):
    event_info = {'trackingNumber' : tracking_number, 'trackingDescription' : '_'.join(event.split('_')[2:]), 'opTime': str(datetime.datetime.now().replace(microsecond=0)), 'timeZone': '+03:00', 'opLocation':'Riga'}
    if event == 'PBM_EP_Order_Fulfilled':
        external_filds = {'orderId': order_id, 'updateTariff': 155, 'updateTariffUnit':'cent', 'updateTariffCurrency': 'USD', 'updateWeight': order_weight[order_id], 'updateWeightUnit': 'g'}
        event_info.update(external_filds)
    return json.dumps(event_info)



