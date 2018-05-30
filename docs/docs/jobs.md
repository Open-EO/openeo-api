# Jobs

As described in the [glossary](glossary.md), a **job** brings one process graph to the back-end and organizes its execution, which may or may not induce costs.

`POST /jobs` by default creates jobs to run computations ***on demand***, i.e. the requested data is calculated during the request. This is useful for web services where details like viewing extent or level of detail are not known in advance. Back-ends SHOULD make sure to cache processed data to avoid additional/high costs and waiting times for the user.

Results can be pre-computed by creating one or multiple ***batch jobs*** using  `POST /jobs/{job_id}/batches`.  They are directly submitted to the back office's processing system. They will run only once, may include constraints, and will store results after execution. Batch jobs are typically time consuming such that user interaction is not possible.

Process graphs can also be ***executed  synchronously*** (`POST /jobs/execute`). Results are delivered with the request itself and no job is created. Only lightweight computations, e.g. small previews, should be executed using this approach as timeouts are to be expected for [long-polling HTTP requests](https://www.pubnub.com/blog/2014-12-01-http-long-polling/).

## Examples

Jobs are created by calling the endpoint `POST /jobs/{job_id}`.

Use case [1](poc.md#use-case-1) and [2](poc.md#use-case-2) are examples for normal jobs without prior batch processing.

### Batch jobs

Batch jobs are created by calling the endpoint `POST /jobs/{job_id}/batches`.

An explicit example for batch jobs is [use case 3](poc.md#use-case-3).

### Synchronously executed jobs

#### Retrieval of a GeoTIFF

**Request**

```
Header:
POST /jobs/execute HTTP/1.1
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
    "tiled":true,
    "compress":"jpeg",
    "photometric":"YCBCR",
    "jpeg_quality":80
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
POST /jobs/execute HTTP/1.1
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

