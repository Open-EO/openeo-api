# Constraints

The openEO API supports to restrict datasets by different dimensions and provides basic information to align datasets with different characteristics. This feature is called 'constraints', formerly known as 'data views'. They describe at which resolution and for which spatial and temporal extent the original Earth observation data are processed and hence can be used to run processes interactively on small parts of the original data without need to wait for long-running processes. 

Heterogeneous datasets are unified by the back-ends based on the specified constraints. For instance, the difference between a PROBA-V image and a Sentinel image, which have e a different projection and resolution, are automatically resampled and projected by the back-ends as soon as it is required to do so. Except specifying reasonable constraints, clients are not responsible to ensure that the data matches by first applying resampling or projections processes.

Temporal references are always specified on the basis of the [Gregorian calendar](https://en.wikipedia.org/wiki/Gregorian_calendar). Therefore a temporal reference system can't be specified in the constraints object.

## Example
The following JSON object describes a coarse resolution (0.25° x 0.25°) view of monthly aggregated data. 

```json
{
  "spatial":{
    "extent":{
      "crs":"EPSG:4326",
      "left":-10.21,
      "top":53.23,
      "right":12.542,
      "bottom":12.32
    },
    "resolution":0.25,
    "resampling":"nearest",
    "crs":"EPSG:4326"
  },
  "temporal":{
    "extent":{
      "start":"2017-01-01",
      "end":"2018-01-01"
    },
    "resolution":"P1M",
    "resampling":"mean"
  }
}
```