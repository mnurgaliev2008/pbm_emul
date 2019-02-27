from flask import Flask,jsonify, request
import Order, UrlHelpers

app_mall = Flask(__name__)

MALL_URL='https://mall.my.com'
events_track = {}

@app_mall.route('/api/pbm/v1/tracking', methods=['POST'])
def tracking():
    msg_type = request.headers.get('msgType')
    json_data = request.get_json(silent=True)
    track_number = json_data.get('trackingNumber')
    print('Received event=%s for trackinNumber=%s' % (msg_type, track_number))
    track_events = events_track.get(track_number, None)
    if track_events is None:
        track_events = [msg_type]
        events_track[track_number] = track_events
    else:
        track_events.append(msg_type)
        events_track[track_number] = track_events
    if len(track_events) == len(UrlHelpers.EVENTS):
        print ('All events for track = %s are received ' % track_number)
    return jsonify(track_number=msg_type)

if __name__ == '__main__':
    app_mall.run(debug=True,host='0.0.0.0', port=5001)