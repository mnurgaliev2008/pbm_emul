import Order, UrlHelpers
import Database


db = Database.Database()
products = db.get_products(100)
sending_orders = []
processed_orders = []

for product_id, sku_num in products:
    order = Order.Order(product_id,sku_num)
    order_data = order.data
    order_id = order.id
    order= {'order_id': order_id, 'tracking_number': None, 'product_id': product_id, 'sku_num': sku_num}
    sending_orders.append(order)
    response = UrlHelpers.send_order_to_wms(order_data)
    data = response.json()
    processed_order = order
    processed_order.update({'trackingNumber':data.get('trackingNumber'), 'track_event': []})
    processed_orders.append(processed_order)
