#!flask/bin/python
import sys
from flask import Flask,jsonify, request
from concurrent.futures import ThreadPoolExecutor as executor
import Order, UrlHelpers

app_pbm = Flask(__name__)
executor = executor(max_workers=3)
received_orders = []

@app_pbm.route('/PBM_test1/hs/API/PBM_api_url', methods=['POST'])
def create_order():
    data = request.get_json()
    order_id=request.get('order_id')
    tracking_number = 'tr%012d' % order_id
    product_id = data.get('parcel').get('goodsList')[0].get('productId')
    sku_num = data.get('parcel').get('goodsList')[0].get('SKU')
    order = {'order_id': order_id, 'tracking_number': tracking_number, 'product_id': product_id, 'sku_num': sku_num}
    received_orders.append(order)
    executor.submit(UrlHelpers.send_events_to_partner, tracking_number, order_id)
    return jsonify(Order.answer_on_create_order(tracking_number))


if __name__ == '__main__':
    app_pbm.run(debug=True)
