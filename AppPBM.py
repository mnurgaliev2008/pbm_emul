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
    msg_type = request.headers.get('msgType')
    if msg_type == 'EP_PBM_Order_Creation':
        print('Creating oder')
        tracking_number = 'tr%s' % order_id.rjust(15, '0')
        product_id = data.get('parcel').get('goodsList').get('productId')
        sku_num = data.get('parcel').get('goodsList').get('SKU')
        order = {'order_id': order_id, 'tracking_number': tracking_number, 'product_id': product_id, 'sku_num': sku_num}
        received_orders.append(order)
        #executor.submit(UrlHelpers.send_events_to_partner, tracking_number, order_id)
        dict_ans_order = Order.Order.answer_on_create_order(tracking_number)
        print('Type answering data: ' + str(type(dict_ans_order)))
        ans = jsonify(dict_ans_order)
    elif msg_type == 'EP_PBM_Order_Cancel':
        ans = jsonify({'orderID': order_id, 'trackingDescription': 'Order canceled'})
    return ans


if __name__ == '__main__':
    app_pbm.run(debug=True,host='0.0.0.0', port=5000)
