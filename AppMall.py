from flask import Flask,jsonify, request
import Order, UrlHelpers

app_mall = Flask(__name__)

MALL_URL='https://mall.my.com'
events_track = {}

@app_mall.route('/pbm/api/v1/event', methods=['POST'])
def tracking():
    msg_type = request.headers.get('msgType')
    track_number = request.json('trackingNumber')
    print('Received event=%s for trackinNumber=%s' % (msg_type, track_number))
    track_events = events_track.get(track_number, None)
    if track_events is None:
        events_track['track_number'] = [msg_type]
    else:
        track_events.append(msg_type)
        events_track['track_number'] = track_events

if __name__ == '__main__':
    app_mall.run(debug=True)