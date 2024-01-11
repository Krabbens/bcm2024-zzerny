import { decode, encode } from "@googlemaps/polyline-codec";

const encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@";
console.log(decode(encoded, 5));
// [
//   [38.5, -120.2],
//   [40.7, -120.95],
//   [43.252, -126.453],
// ]

const path = [
  [38.5, -120.2],
  [40.7, -120.95],
  [43.252, -126.453],
];
console.log(encode(path, 5));
// "_p~iF~ps|U_ulLnnqC_mqNvxq`@"