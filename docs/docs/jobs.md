# Processing data using a process graph

Process graphs can be executed in three different ways.

Results can be pre-computed by creating a ***batch jobs*** using  `POST /jobs`.  They are submitted to the back office's processing system, but will remain inactive until `POST /jobs/{job_id}/results` has been called. They will run only once and store results after execution. Batch jobs are typically time consuming such that user interaction is not possible.

Web services usually allow users to change the viewing extent or level of detail. Therefore computations may run ***on demand***, i.e. the requested data is calculated during the request. Back-ends SHOULD make sure to cache processed data to avoid additional/high costs and waiting times for the user.

Process graphs can also be ***executed  synchronously*** (`POST /jobs/previews`). Results are delivered with the request itself and no job is created. Only lightweight computations, for example small previews, should be executed using this approach as timeouts are to be expected for [long-polling HTTP requests](https://www.pubnub.com/blog/2014-12-01-http-long-polling/).

## Examples

### Synchronously executed jobs

#### Retrieval of a GeoTIFF

**Request**

```
Header:
POST /preview HTTP/1.1
Content-Type: application/json; charset=utf-8

Body:
{
  "process_graph":{
    "process_id":"min_time",
    "args":{
      "imagery":{
        "process_id":"NDVI",
        "args":{
          "imagery":{
            "process_id":"filter_daterange",
            "args":{
              "imagery":{
                "process_id":"filter_bbox",
                "args":{
                  "imagery":{
                    "process_id":"get_data",
                    "args": {
                      "data_id": "S2_L2A_T32TPS_20M"
                    }
                  },
                  "left":652000,
                  "right":672000,
                  "top":5161000,
                  "bottom":5181000,
                  "srs":"EPSG:32632"
                }
              },
              "from":"2017-01-01",
              "to":"2017-01-31"
            }
          },
          "red":"B04",
          "nir":"B8A"
        }
      }
    }
  },
  "output":{
    "format":"GTiff",
	"args": {
      "tiled":true,
      "compress":"jpeg",
      "photometric":"YCBCR",
      "jpeg_quality":80
	}
  }
}
```

**Response** 
```
Header:
HTTP/1.1 200 OK
Content-Type: image/tiff
Access-Control-Allow-Origin: <Origin>

Body:
omitted (the GeoTiff file contents)
```

#### Retrieval of time series

**Request**

```
Header:
POST /preview HTTP/1.1
Content-Type: application/json; charset=utf-8

Body:
{
  "process_graph":{
    "process_id":"zonal_statistics",
    "args":{
      "imagery":{
        "process_id":"filter_daterange",
        "args":{
          "imagery":{
            "process_id":"filter_bbox",
            "args":{
              "imagery":{
                "process_id":"filter_bands",
                "args":{
                  "imagery":{
                    "process_id": "get_data",
                    "args": {
                      "data_id":"Sentinel2-L1C"
                    }
                  },
                  "bands":8
                }
              },
              "left":16.1,
              "right":16.6,
              "top":48.6,
              "bottom":47.2,
              "srs":"EPSG:4326"
            }
          },
          "from":"2017-01-01",
          "to":"2017-01-31"
        }
      },
      "regions":"/users/me/files/",
      "func":"avg"
    }
  },
  "output":{
    "format":"GPKG"
  }
}
```

**Response** 

```
Header:
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Access-Control-Allow-Origin: <Origin>

Body:
omitted (the GeoPackage file contents)
```

