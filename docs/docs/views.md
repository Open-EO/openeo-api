# Contraints (Data Views)

_Work in progress!_

The openEO API supports to look at datasets from different `views`. Views describe at which resolution and for which spatial and temporal extent the original Earth observation data are processed and hence can be used to run processes interactively on small parts of the original data without need to wait for long-running processes. The idea is similar to what Google Earth Engine does by reducing computations only to pixels that are actually displayed.

*Note: This feature is a very early draft and currently not described in the API specification. It may be added after delivering the proof-of-concept.*

## Example
The following JSON object describes a coarse resolution (0.25° x 0.25°) view of monthly aggregated data. 

```json
"view": {
  "space": {
    "srs": "EPSG:4326",
    "window": {
      "left": -10.21,
      "top": 53.23,
      "right": 12.542,
      "bottom": 12.32
    },
    "cell_size": 0.25,
    "resampling": "nearest"
  },
  "time": {
    "window": {
      "start": "2017-01-01",
      "end": "2018-01-01"
    },
    "time_step": "P1M",
    "resampling": "nearest"
  }
}
```