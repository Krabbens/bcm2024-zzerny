from flask import Flask, jsonify, request
from routecalc import *
from cache import *


app = Flask(__name__)

cache = None
router = None
google = None


@app.before_first_request
def before_first_request():
    global cache, router, google
    cache = Cache()
    router = RouteCalc()
    google = Google()


@app.route('/getroute', methods=['POST'])
def get_route():
    data = request.get_json()

    if 'point1' not in data or 'point2' not in data or 'type' not in data:
        return jsonify({'error': 'A parameter is missing'}), 400

    start_point = (data['point1']['lat'], data['point1']['lon'])
    end_point = (data['point2']['lat'], data['point2']['lon'])

    router.get_data(cache)

    if 'zone' in data:
        data = router.get_route_info(data['type'], start_point, end_point, data['zone'])
    else:
        data = router.get_route_info(data['type'], start_point, end_point)

    return jsonify({'point1' : 
                        {
                            'lat': data[0][0],
                            'lon': data[0][1]
                        },
                    'point2' :
                        {
                            'lat': data[1][0],
                            'lon': data[1][1]
                        }
                    })

@app.route('/getzones/<brand>', methods=['GET'])
def get_zones(brand="tier"):
    zones = router.get_data_zone(cache)

    if brand == "tier":
        zones_to_return = zones["tier_zones"]
    elif brand == "bolt":
        zones_to_return = zones["bolt_zones"]
    else:
        zones_to_return = zones["tier_zones"]
        zones_to_return.extend(zones["bolt_zones"])

    zones_json = [z.getJson() for z in zones_to_return]
    return zones_json

@app.route('/getgeocode/<address>', methods=['GET'])
def get_geocode(address):
    geocode_result = google.get_geocode(address)
    if geocode_result is None:
        return jsonify({"error": "Geocode not found for the given address"}), 404
    return jsonify(geocode_result)


if __name__ == '__main__':
    app.run(debug=True)
