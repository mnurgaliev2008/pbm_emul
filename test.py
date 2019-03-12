import UrlHelpers, Order, Database, sys, time, json, os

sending_orders = []
processed_orders = []


def send_orders(products, order_id, url=None):
    for product_id, sku_num in products:
        order = Order.Order(product_id,sku_num, order_id)
        weight_price = {'sku_num': sku_num, 'weight': order.weight, 'price': order.price}
        data ={}
        try:
            file = open('Orders.txt', 'r')
            data = json.loads(file.read())
            file.close()
        except IOError:
            pass
        file = open('Orders.txt', 'w')

        data[order.id] = weight_price
        file.write(json.dumps(data))
        response = UrlHelpers.send_order_to_wms(order, url)
        print('status_code: ' + str(response.status_code))
        data = response.json()

        if response.status_code == 200:
            print(data)
            sending_orders.append(order)
        try:
            if data.get('trackingNumber', None) is not None:
                processed_orders.append(data)
        except Exception as e:
            print(data)
            print(e)
    file.close()
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
    try:
        os.remove('Orders.txt')
    except OSError:
        pass
    db = Database.Database()
    products = db.get_products(1)
    #products=(('1711aac6-9474-4bba-b0ba-896ecd0ea719','197738988' ),)

    print('Getting products....')
    next_order = db.get_next_order_id()
    for i in range(int(sys.argv[1])):
        print('Sending %s order' % next_order)
        send_orders(products, next_order)
        time.sleep(0.5)
        next_order+=1



    #send_cancel_order(order_id)


