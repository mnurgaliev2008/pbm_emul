import UrlHelpers, Order, Database


db = Database.Database()
products = db.get_products(100)
sending_orders = []
processed_orders = []

for product_id, sku_num in products:
    order = Order.Order(product_id,sku_num)
    order_data = order.data
    response = UrlHelpers.send_order_to_wms(order_data)
    data = response.json()
    print(data)


product_id='1711aac6-9474-4bba-b0ba-896ecd0ea719'
prod2_id = 'dsadas'
sku_num='197738988'
sku2='dsadas'
order = Order.Order(product_id, sku_num)
print(order)
order_data = order.data
order2=Order.Order(prod2_id, sku2)
print(order2.data)
print(order2.id)



response = UrlHelpers.send_order_to_wms(str(order))
print(response.headers)
print(response.json())
print(response.text)
print(response.content)