from flask import Flask, jsonify, request
from routecalc import *
from cache import *


app = Flask(__name__)

cache = None
router = None


@app.before_first_request
def before_first_request():
    global cache, router
    cache = Cache()
    router = RouteCalc()


@app.route('/getroute', methods=['POST'])
def get_route():
    data = request.get_json()

    if 'point1' not in data or 'point2' not in data or 'type' not in data:
        return jsonify({'error': 'A parameter is missing'}), 400

    start_point = (data['point1']['lon'], data['point1']['lat'])
    end_point = (data['point2']['lon'], data['point2']['lat'])

    router.get_data(cache)
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


if __name__ == '__main__':
    app.run(debug=True)
