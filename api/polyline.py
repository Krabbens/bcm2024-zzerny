from typing import List, Union, Tuple

# Object with lat and lng properties
class LatLng:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

# Array with lat and lng elements
LatLngTuple = Tuple[float, float]

def decode(encoded_path: str, precision: int = 5) -> List[LatLngTuple]:
    factor = 10 ** precision
    path = []
    index = 0
    lat = 0
    lng = 0
    point_index = 0
    length = len(encoded_path)

    while index < length:
        result = 1
        shift = 0
        while True:
            b = ord(encoded_path[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lat += ~(result >> 1) if result & 1 else (result >> 1)

        result = 1
        shift = 0
        while True:
            b = ord(encoded_path[index]) - 63 - 1
            index += 1
            result += b << shift
            shift += 5
            if b < 0x1f:
                break
        lng += ~(result >> 1) if result & 1 else (result >> 1)

        path.append((lat / factor, lng / factor))
        point_index += 1

    return path

def encode(path: List[Union[List[float], LatLng, LatLngTuple]], precision: int = 5) -> str:
    factor = 10 ** precision

    def lat_lng_to_fixed(latLng: Union[LatLng, LatLngTuple]) -> LatLngTuple:
        if not isinstance(latLng, (list, tuple)):
            latLng = (latLng.lat, latLng.lng)
        return (round(latLng[0] * factor), round(latLng[1] * factor))

    return polyline_encode_line(path, lat_lng_to_fixed)

def polyline_encode_line(array: List[Union[List[float], LatLng, LatLngTuple]], transform) -> str:
    v = []
    start = (0, 0)
    for i in range(len(array)):
        end = transform(array[i])
        v.extend(polyline_encode_signed(round(end[0]) - round(start[0]), v))
        v.extend(polyline_encode_signed(round(end[1]) - round(start[1]), v))
        start = end

    return "".join(v)

def polyline_encode_signed(value: int, array: List[str]) -> List[str]:
    return polyline_encode_unsigned(~(value << 1) if value < 0 else value << 1, array)

def polyline_encode_unsigned(value: int, array: List[str]) -> List[str]:
    while value >= 0x20:
        array.append(chr((0x20 | (value & 0x1f)) + 63))
        value >>= 5
    array.append(chr(value + 63))
    return array

def round_number(v: float) -> int:
    return int(abs(v) + 0.5) * (1 if v >= 0 else -1)


print(decode("cbujIiuxpB?_@Q??^P?"))