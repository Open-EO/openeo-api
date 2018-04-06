# Jobs

As described in the [glossary](glossary.md), a **job** brings one process graph to the back-end and organizes its execution, which may or may not induce costs.

The API distinguishes two types how process graphs can asynchronously be executed at back-ends as a job.

***On-demand jobs*** ( created using `POST /jobs/on_demand`) run computations on demand, i.e., with incoming requests for downloading the results. Jobs can be executed multiple times with different views (including spatial / temporal resolution and window) as provided by download requests, which could come e.g. from WCS or WMTS.

***Batch jobs*** (created using `POST /jobs/batch`) in contrast are directly submitted to the back office's processing system. They will run only once, may include a provided view, and will store results after execution. Batch jobs are typically time consuming such that user interaction is not possible. 

As an example we consider the simple calculation of vegetation indexes on all available Sentinel 2 imagery over Europe. Batch evaluation will take all relevant images, compute the NDVI, and finally store the result whereas on-demand execution will not start any computations on its own. As soon as a client performs a download request such as a `GetCoverage` WCS request, the job's process will be executed but only for requested pixels. However, back-ends are free to cache frequent intermediate results on their own.

There is a third way to execute a process graph at back-ends:  ***synchronous execution*** (`POST /jobs/execute`). This is similar to *on-demand jobs*, but results are delivered with the request itself and no job is created. Only lightweight computations, e.g. small previews, should be executed using this approach as timeouts are to be expected for [long-polling HTTP requests](https://www.pubnub.com/blog/2014-12-01-http-long-polling/).

## Examples

### On-demand executed jobs

On-demand executed jobs are created by calling the endpoint `POST /jobs/{job_id}/on_demand`.

Use case [1](poc.md#use-case-1) and [2](poc.md#use-case-2) are examples for _on-demand jobs_.

### Batch jobs

Batch jobs are created by calling the endpoint `POST /jobs/{job_id}/batch`.

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

