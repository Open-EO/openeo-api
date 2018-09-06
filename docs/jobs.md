# Processing data using a process graph

Process graphs can be executed in three different ways.

Results can be pre-computed by creating a ***batch job*** using  `POST /jobs`.  They are submitted to the back office's processing system, but will remain inactive until `POST /jobs/{job_id}/results` has been called. They will run only once and store results after execution. Results can be downloaded. Batch jobs are typically time consuming such that user interaction is not possible.

Another way of processing and accessing data are **web services**. Web services allow web-based access using different protocols such as [OGC WMS](http://www.opengeospatial.org/standards/wms), [OGC WCS](http://www.opengeospatial.org/standards/wcs) or [XYZ tiles](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames). These protocols usually allow users to change the viewing extent or level of detail (zoom level). Therefore, computations may run ***on demand***, i.e. the requested data is calculated during the request. Back-ends should make sure to cache processed data to avoid additional/high costs and waiting times for the user.

Process graphs can also be ***executed  synchronously*** (`POST /jobs/previews`). Results are delivered with the request itself and no job is created. Only lightweight computations, for example small previews, should be executed using this approach as timeouts are to be expected for [long-polling HTTP requests](https://www.pubnub.com/blog/2014-12-01-http-long-polling/).

## Data processing details
Heterogeneous datasets are unified by the back-ends based on the processes in the process graphs. For instance, the difference between a PROBA-V image and a Sentinel image, which have e a different projection and resolution, are automatically resampled and projected by the back-ends as soon as it is required to do so. Clients are not responsible to ensure that the data matches by first applying resampling or projections processes.

Temporal references are always specified on the basis of the [Gregorian calendar](https://en.wikipedia.org/wiki/Gregorian_calendar).

## Examples

### Synchronously executed jobs

#### Retrieval of a GeoTIFF

**Request**

``` http
POST /preview HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "process_graph":{
    "process_id":"min_time",
    "imagery":{
      "process_id":"NDVI",
      "imagery":{
        "process_id":"filter_daterange",
        "imagery":{
          "process_id":"filter_bbox",
          "imagery":{
            "process_id":"get_collection",
            "name":"S2_L2A_T32TPS_20M"
          },
          "left":652000,
          "right":672000,
          "top":5161000,
          "bottom":5181000,
          "srs":"EPSG:32632"
        },
        "extent":"2017-01-01/2017-01-31"
      },
      "red":"B04",
      "nir":"B8A"
    }
  },
  "output":{
    "format":"GTiff",
    "args":{
      "tiled":true,
      "compress":"jpeg",
      "photometric":"YCBCR",
      "jpeg_quality":80
    }
  }
}
```

**Response** 
``` http
HTTP/1.1 200 OK
Content-Type: image/tiff
Access-Control-Allow-Origin: <Origin>

omitted (the GeoTiff file contents)
```

#### Retrieval of time series

**Request**

``` http
POST /preview HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "process_graph":{
    "process_id":"zonal_statistics",
    "imagery":{
      "process_id":"filter_daterange",
      "imagery":{
        "process_id":"filter_bbox",
        "imagery":{
          "process_id":"filter_bands",
          "imagery":{
            "process_id":"get_collection",
            "name":"Sentinel2-L1C"
          },
          "bands":8
        },
        "left":16.1,
        "right":16.6,
        "top":48.6,
        "bottom":47.2,
        "srs":"EPSG:4326"
      },
      "extent":"2017-01-01/2017-01-31"
    },
    "regions":"/users/me/files/",
    "func":"avg"
  },
  "output":{
    "format":"GPKG"
  }
}
```

**Response** 

``` http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Access-Control-Allow-Origin: <Origin>

omitted (the GeoPackage file contents)
```

