import UrlHelpers, Order, Database


db = Database.Database()
products = db.get_products(10)
print('Getting products....')
sending_orders = []
processed_orders = []

for product_id, sku_num in products:
    order = Order.Order(product_id,sku_num)
    order_data = order.data
    response = UrlHelpers.send_order_to_wms(order_data)
    data = response.json()
    print(data)

