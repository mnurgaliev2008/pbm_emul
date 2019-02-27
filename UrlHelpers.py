import requests, json
from collections import OrderedDict
#from Crypto.Hash import SHA256
import Order
import hashlib

pbm_client_secret = 'ITu2ReCVCBrOC2xG7ATvGRRfGolg16zZKCsxSBzB'
PBM_ID = 'pbm'
MALL_ID= 'mall.my.com'
MALL_WMS_URL= 'http://176.99.7.62/api/pbm/v1'
#MALL_WMS_URL= 'http://127.0.0.1:5001/api/pbm/v1'
EVENTS=['PBM_EP_Order_Fulfilled', 'PBM_EP_Warehouse_Departure', 'PBM_EP_Post_Arrival', 'PBM_EP_Post_Departure', 'PBM_EP_Lastmile_Arrival', 'PBM_EP_Lastmile_Customs_Departure', 'PBM_EP_Lastmile_Post_Office_Arrival', 'PBM_EP_Lastmile_Success', 'PBM_EP_Lastmile_Return', 'PBM_EP_Claim']


def calc_checksum(request_type, full_url, platform_id, json_data=None):
    data_for_checksum = full_url + request_type + platform_id + pbm_client_secret + json_data
    encoded_data = data_for_checksum.encode('utf-8')
    hash = hashlib.new('SHA256',encoded_data).hexdigest()
    return hash

def send_events_to_partner(tracking_number, order_id, timeout=60):
    for event in EVENTS:
        full_url = MALL_WMS_URL + '/tracking'
        json_data = Order.Order.create_event(event, tracking_number,order_id).replace(' ', '')
        checksum = calc_checksum('POST', full_url, PBM_ID, json_data)
        headers = {'Content-Type': 'application/json', 'pbmId': PBM_ID, 'checksum': checksum,
                   'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': event}
        response = requests.post(full_url, headers=headers, data=json_data, timeout=timeout)
        if response.status_code == 200:
            print(event + 'with trackingNumber %s was sent successfully' % tracking_number)

def send_order_to_wms(order, url):
    if url is None:
        print('Sending orders to WMS_URL: %s' % MALL_WMS_URL)
        checksum = calc_checksum('POST', MALL_WMS_URL, MALL_ID, order)
        headers = {'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': checksum,
                       'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'EP_PBM_Order_Creation'}
        with open('test.txt', 'w') as f:
            f.write(order+'\n')
        response = requests.post(MALL_WMS_URL, data=order, headers=headers)
        return response
    else:
        response = requests.post(url + '/api/pbm/v1', data=order, headers={'Content-Type': 'application/json', 'platformID': MALL_ID, 'checksum': 'checksum',
                       'msgId': '550e8400-e29b-41d4-a716-446655440000', 'msgType': 'EP_PBM_Order_Creation'})
        return response


if __name__=='__main__':
    send_events_to_partner('tr00001', 1)
