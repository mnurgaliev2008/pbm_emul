import UrlHelpers, Order, Database, sys

def send_orders(url=None):
    db = Database.Database()
    products = db.get_products(10)
    print('Getting products....')
    sending_orders = []
    processed_orders = []
    #products=(('1711aac6-9474-4bba-b0ba-896ecd0ea719','197738988' ),)
    for product_id, sku_num in products:
        order = Order.Order(product_id,sku_num)
        order_data = order.data
        response = UrlHelpers.send_order_to_wms(order_data, url)
        sending_orders.append(order)
        data = response.json()
        print(data)
        print(type(data))
        if data.get('trackingNumber', None) is not None:
            processed_orders.append(data)
    print('All orders sent: %s' % len(sending_orders))
    print('Number processed orders : %s' % len(processed_orders))




if __name__=='__main__':
    if len(sys.argv) > 1:
        send_orders(sys.argv[1])
    else:
        send_orders()



#curl -X POST http://127.0.0.1:5000/api/pbm/v1 -H "checksum: 73e2faecd84a2b1ea3f44f51a2f4527f22e171b06546f46819478efcf3074ff8" -H "platformId: mall.my.com" -H "msgType: EP_PBM_Order_Creation" -H "msgId: TestCancel1" -d '{"orderID":"096593d8-f76d-45d9-934e-b423ed24f4ba","buyer":{"imId":"198b6c7e-71b9-409f-b7a5-1111cdb1d57a","name":"Allure Avtomatov","phone":"+75555555555","email":null,"zipCode":"125167","address":{"country":"RU","province":"Russian state","city":"Moscow","detailAddress":"Leningradsky prospekt 39, bld. 79"}},"parcel":{"goodsList":{"price":"200","priceUnit":"cent","priceCurrency":"USD","productId":"15465b27-c5ff-4562-9ab8-3b4b2d807d9b","SKU":"s26a#T29034_B","quantity":1}},"bizType":1,"packing":0}'
