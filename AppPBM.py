#!flask/bin/python
import sys
from flask import Flask,jsonify, request
from concurrent.futures import ThreadPoolExecutor as executor
import Order, UrlHelpers, json

app_pbm = Flask(__name__)
executor = executor(max_workers=3)
received_orders = []


@app_pbm.route('/<path>', methods=['POST'])
def catch_all(path):
    print('tut')
    print( request.url)
    print(repr(path))
    return path



@app_pbm.route('/v1', methods=['POST'])
def process_order():
    data = request.get_json(silent=True)
    print('Receiving data: %s' % data)
    order_id = data.get('orderID')
    tracking_number = 'tr%s' % order_id.rjust(15, '0')
    msg_type = request.headers.get('msgType')
    if msg_type == 'EP_PBM_Order_Creation':
        print('Creating oder')
        goods_list = data.get('parcel').get('goodsList')
        if type(goods_list) == list:
            print('goods_list->list')
            products = [(item.get('SKU'), item.get('productId')) for item in goods_list]
            order = {'order_id': order_id, 'tracking_number': tracking_number, 'products': products}
        else:
            print('goods_list->NOT list')
            sku_num = goods_list.get('SKU')
            product_id = goods_list.get('productId')
            order = {'order_id': order_id, 'tracking_number': tracking_number, 'product_id': product_id, 'sku_num': sku_num}
        received_orders.append(order)
        dict_ans_order = Order.answer_on_create_order(tracking_number)
        executor.submit(UrlHelpers.send_events_to_partner, tracking_number, order_id)
        #executor.submit(UrlHelpers.send_stock)
        print('Type answering data: ' + str(type(dict_ans_order)))
        ans = jsonify(dict_ans_order)
    elif msg_type == 'EP_PBM_Order_Cancel':
        ans = jsonify({'orderID': order_id, 'trackingDescription': 'Order canceled'})
    return ans


if __name__ == '__main__':
    app_pbm.run(debug=True,host='0.0.0.0', port=5000)
