import requests, json
import Order, Database
import hashlib, time

pbm_client_secret = 'ITu2ReCVCBrOC2xG7ATvGRRfGolg16zZKCsxSBzB'
PBM_ID = 'pbm'
MALL_ID= 'mall.my.com'
MALL_WMS_URL= 'http://176.99.7.62/api/pbm/v1'
#MALL_WMS_URL= 'http://127.0.0.1:5001/api/pbm/v1'
EVENTS=['PBM_EP_Order_Fulfilled', 'PBM_EP_Warehouse_Departure', 'PBM_EP_Post_Arrival', 'PBM_EP_Post_Departure', 'PBM_EP_Lastmile_Arrival', 'PBM_EP_Lastmile_Customs_Departure', 'PBM_EP_Lastmile_Post_Office_Arrival', 'PBM_EP_Lastmile_Success', 'PBM_EP_Lastmile_Return', 'PBM_EP_Claim']


def calc_checksum(request_type, full_url, platform_id, json_data=None):
    data_for_checksum = full_url + request_type + platform_id + pbm_client_secret + json_data
    print(data_for_checksum+'\n')
    encoded_data = data_for_checksum.encode('utf-8')
    hash = hashlib.new('SHA256',encoded_data).hexdigest()
    print(hash)
    return hash


def send_events_to_partner(tracking_number, order_id):
    for event in EVENTS:
        full_url = MALL_WMS_URL + '/tracking'
        json_data = Order.create_event(event, tracking_number,order_id).replace(' ', '')
        print(json_data)

        print('sending events %s for order %s: %s {%s}' % (event, order_id, full_url, json_data))
        time.sleep(1)

        checksum = calc_checksum('POST', full_url, PBM_ID, json_data)
        headers = {'Content-Type': 'application/json', 'pbmId': PBM_ID, 'checksum': checksum,
                   'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': event}
        response = requests.post(full_url, headers=headers, data=json_data)
        if response.status_code == 200:
            print(event + 'with trackingNumber %s was sent successfully' % tracking_number)

def send_order_to_wms(order, url):

    if url is None:
        print('Sending orders to WMS_URL: %s' % MALL_WMS_URL)
        checksum = calc_checksum('POST', MALL_WMS_URL, MALL_ID, order.data)
        headers = {'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': checksum,
                       'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'EP_PBM_Order_Creation'}
        response = requests.post(MALL_WMS_URL, data=order.data, headers=headers)
        return response
    else:
        response = requests.post(url + '/api/pbm/v1', data=order.data, headers={'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': 'checksum',
                       'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'EP_PBM_Order_Creation'})
        return response

def send_cancel_order(order_id):
    print('Sending cancel order for id = %s' % order_id)
    order_data = json.dumps({'orderID': str(order_id)})
    cs = calc_checksum('POST', MALL_WMS_URL, MALL_ID, order_data)
    headers = {'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': cs,
               'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'EP_PBM_Order_Cancel'}
    response = requests.post(MALL_WMS_URL, headers=headers, data=order_data)
    return response

def send_stock():
    while True:
        time.sleep(6000)
        db = Database.Database()
        variants = db.get_variants()
        print('Number variants to sent = %s' % len(variants))

        #variants = [i for i in range(140)]
        #variants = ['00010ad2-79e8-4687-abc8-e4bad160c273']
        number = 0
        while len(variants) >0:
            good_list = []
            if len(variants) >= 50:
                variants_for_send = variants[:50]
                variants = variants[50:]
                number+=50
            else:
                variants_for_send = variants
                variants = []
                number+=len(variants_for_send)
            for var in variants_for_send:
                dict_var = {'variantId': str(var), 'quantity': 100}
                good_list.append(dict_var)
            stock_dict = {'goodsList': good_list}
            stock_data = json.dumps(stock_dict).replace(' ', '')
            print('Sending stock: %s' % stock_data)
            full_url = MALL_WMS_URL + '/stock'
            checksum = calc_checksum('POST', full_url, MALL_ID, stock_data)

            headers = {'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': checksum,
                           'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'PBM_EP_Stocks_Status'}
            response = requests.post(full_url, data=stock_data, headers=headers)
            if response.status_code == 200:
                print('Stock for %s variants are sent' % number)


if __name__=='__main__':

    send_stock()
    send_cancel_order(1)
    send_events_to_partner('tr00001', 1)
