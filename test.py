import UrlHelpers, Order, Database, sys, json

sending_orders = []
processed_orders = []


def send_orders(products, first_order, url=None):
    for product_id, sku_num in products:
        Order.Order.num_order=first_order
        order = Order.Order(product_id,sku_num)
        order_data = order.data
        response = UrlHelpers.send_order_to_wms(order_data, url)
        print('status_code: ' + str(response.status_code))
        if response.status_code == 200:
            data = response.json()
            print(data)
            sending_orders.append(order)
        try:
            if data.get('trackingNumber', None) is not None:
                processed_orders.append(data)
        except Exception as e:
            print(data)
            print(e)

    print('All orders sent: %s' % len(sending_orders))
    print('Number processed orders : %s' % len(processed_orders))
    return order.id

def send_cancel_order(order_id):
    response = UrlHelpers.send_cancel_order(order_id)
    if response.status_code == 200 and response.json().get('trackingDescription') == 'Order canceled':
        print('Order %s canceled' % order_id)
    else:
        print(str(response.status_code) + response.text)



if __name__=='__main__':
    db = Database.Database()
    products = db.get_products(1)
    #products=(('1711aac6-9474-4bba-b0ba-896ecd0ea719','197738988' ),)

    print('Getting products....')
    if len(sys.argv) > 1:
        send_orders(products, int(sys.argv[1]))
    else:
        order_id = send_orders(products)
        #send_cancel_order(order_id)


