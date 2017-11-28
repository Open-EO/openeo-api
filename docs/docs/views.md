# Data Views

The OpenEO API supports to look at datasets from different `views`. Views describe at which resolution and for which spatial and temporal extent the original Earth observation data are processed and hence can be used to run processes interactively on small parts of the original data without need to wait for long-running processes. 

## Example
The following JSON object describes a coarse resolution (0.25° x 0.25°) view of monthly aggregated data. 

```
"view": {
    "space": {
      "srs": "EPSG:4326",
      "window": {
        "left": -10.21,
        "top": 53.23,
        "right": 12.542,
        "bottom": 12.32
      },
      "resolution": 0.25,
      "resampling": "nearest"
    },
    "time": {
      "window": {
        "start": "2017-01-01",
        "end": "2018-01-01"
      },
      "resolution": "P1M",
      "resampling": "nearest"
    }
  }
  ```  