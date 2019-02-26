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
def create_order():
    print('Creating oder')

    data = request.get_json(silent=True)
    print('Receiving data: %s' % data)
    order_id=data.get('orderID')
    tracking_number = 'tr%s' % order_id.rjust(15, '0')
    product_id = data.get('parcel').get('goodsList').get('productId')
    sku_num = data.get('parcel').get('goodsList').get('SKU')
    order = {'order_id': order_id, 'tracking_number': tracking_number, 'product_id': product_id, 'sku_num': sku_num}
    received_orders.append(order)
    #executor.submit(UrlHelpers.send_events_to_partner, tracking_number, order_id)
    dict_ans_order = Order.Order.answer_on_create_order(tracking_number)
    print('Type answering data: ' + str(type(dict_ans_order)))
    ans_data = json.dumps(dict_ans_order)
    print(type(ans_data))
    print(ans_data)
    ans = jsonify(ans_data)
    print(type(ans))
    print(ans.json())
    return ans


if __name__ == '__main__':
    app_pbm.run(debug=True,host='0.0.0.0', port=5000)
