# Proof of Concept (API v0.0.2)

This page gives a detailed description of the openEO proof of concept and gives a list and specification of what needs to be implemented. The proof of concept will consist of

* at least three clearly defined example processes (see below),
* a prototypical API specification including communication API call sequences of the processes (see below),
* implementations of the processes on three back-ends, and
* prototypical clients in R, Python and potentially JavaScript.

Below, we define example use cases and how they are translated to sequences of API calls:

1. [Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery](#use-case-1)
2. [Create a monthly aggregated Sentinel 1 product from a custom Python script](#use-case-2)
3. [Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons](#use-case-3)

_Note:_ Authentication is not included in these examples. Enabling authentication needs the placeholder `<Origin>` to be set to the requesting host, including protocol, host name/IP and port, e.g. `http://localhost:8080`. This could be done by using the Origin header value from the request.

## Use Case 1

### Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.

#### 1. Check whether Sentinel 2A Level 1C data is available at the back-end

**Request**
```
GET /data/Sentinel2A-L1C HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "product_id":"Sentinel-2A-L1C",
  "description":"Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
  "source":"European Space Agency (ESA)",
  "extent":[
    -34,
    35,
    39,
    71
  ],
  "time":[
    "2016-01-01",
    "2017-10-01"
  ],
  "bands":[
    {
      "band_id":"1",
      "wavelength_nm":443.9,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"2",
      "name":"blue",
      "wavelength_nm":496.6,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"3",
      "name":"green",
      "wavelength_nm":560,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"4",
      "name":"red",
      "wavelength_nm":664.5,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"5",
      "wavelength_nm":703.9,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"6",
      "wavelength_nm":740.2,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"7",
      "wavelength_nm":782.5,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"8",
      "name":"nir",
      "wavelength_nm":835.1,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"8a",
      "wavelength_nm":864.8,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"9",
      "wavelength_nm":945,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"10",
      "wavelength_nm":1373.5,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"11",
      "wavelength_nm":1613.7,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"12",
      "wavelength_nm":2202.4,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    }
  ]
}
```


#### 2. Check that needed processes are available

**Request**
```
GET /processes/filter_bbox HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "process_id":"filter_bbox",
  "description":"Drops observations from a collection that are located outside of a given bounding box.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    },
    "left":{
      "description":"left boundary (longitude / easting)"
    },
    "right":{
      "description":"right boundary (longitude / easting)"
    },
    "top":{
      "description":"top boundary (latitude / northing)"
    },
    "bottom":{
      "description":"bottom boundary (latitude / northing)"
    },
    "srs":{
      "description":"spatial reference system of boundaries as proj4 or EPSG:12345 like string"
    }
  }
}
```

**Request**
```
GET /processes/filter_daterange HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "process_id":"filter_daterange",
  "description":"Drops observations from a collection that have been captured before a start or after a given end date.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    },
    "from":{
      "description":"start date"
    },
    "to":{
      "description":"end date"
    }
  }
}
```

**Request**
```
GET /processes/NDVI HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "process_id":"NDVI",
  "description":"Finds the minimum value of time series for all bands of the input dataset.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    },
    "red":{
      "description":"reference to the red band"
    },
    "nir":{
      "description":"reference to the nir band"
    }
  }
}
```

**Request**
```
GET /processes/min_time HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "process_id":"min_time",
  "description":"Finds the minimum value of time series for all bands of the input dataset.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    }
  }
}
```

#### 3. Create a job at the back-end 

**Request**
```
POST /jobs HTTP/1.1
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
                    "product_id":"S2_L2A_T32TPS_20M"
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
  }
}
```
**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "job_id":"2a8ffb20c2b235a3f3e3351f",
  "status":"submitted",
  "submitted":"2017-01-01T09:32:12Z",
  "updated":"2017-01-01T09:36:18Z",
  "user_id":"bd6f9faf93b4",
  "consumed_credits":0
}
```

#### 4. Create a WCS service

**Request**

```
POST /services HTTP/1.1
Content-Type: application/json; charset=utf-8

Body:
{
  "job_id":"2a8ffb20c2b235a3f3e3351f",
  "type":"wcs",
  "args":{
    "VERSION":"2.0.1"
  }
}
```

**Response**

```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "service_id":"4dab456f6501bbcd",
  "service_url":"https://openeo.org/4dab456f6501bbcd/wcs",
  "service_type":"wcs",
  "service_args":{
    "VERSION":"2.0.1"
  },
  "job_id":"2a8ffb20c2b235a3f3e3351f"
}
```

#### 5. Download the data on demand with WCS

**Request**
```
GET https://openeo.org/4dab456f6501bbcd/wcs?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCapabilities HTTP/1.1
```

**Response**
_omitted_

**Request**
```
GET https://openeo.org/4dab456f6501bbcd/wcs?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=2a8ffb20c2b235a3f3e3351f&FORMAT=image/tiff&SUBSET=x,http://www.opengis.net/def/crs/EPSG/0/4326(16.1,16.5)&SUBSET=y,http://www.opengis.net/def/crs/EPSG/0/4326(47.9,48.6)&&SIZE=x(200)&SIZE=y(200) HTTP/1.1
```


**Response** 
_omitted_

#### 6. Stop the job (and the service)

**Request**

```
PATCH /jobs/2a8ffb20c2b235a3f3e3351f/cancel HTTP/1.1
```

**Response**

```
Header:
HTTP/1.1 200 OK
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body: none
```



## Use Case 2

### Create a monthly aggregated Sentinel 1 product from a custom Python script.

#### 1. Ask the back-end for available Sentinel 1 data

**Request**
```
GET /data/Sentinel1-L1-IW-GRD HTTP/1.1
```


**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "product_id":"Sentinel1-L1-IW-GRD",
  "description":"Sentinel 1 C-band Synthetic Aperture Radar (SAR) Ground Range Data",
  "source":"European Space Agency (ESA)",
  "extent":[
    -34,
    35,
    39,
    71
  ],
  "time":[
    "2016-01-01",
    "2017-10-01"
  ],
  "bands":[
    {
      "band_id":"VV"
    },
    {
      "band_id":"VH"
    }
  ]
}
```


#### 2. Ask the back-end whether it supports Python UDFs of type aggregate_time and get details about expected parameters

**Request**
```
GET /udf_runtimes HTTP/1.1
```


**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "Python":{
    "udf_types":[
      "reduce_time",
      "aggregate_time",
      "apply_pixel"
    ],
    "versions":{
      "3.6.3":{
        "packages":[
          "numpy",
          "scipy",
          "pandas",
          "matplotlib",
          "ipython",
          "jupyter",
          "GDAL"
        ]
      }
    }
  }
}
```

**Request**
```
GET /udf_runtimes/Python/aggregate_time HTTP/1.1
```


**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

{
  "process_id":"/udf/Python/aggregate_time",
  "description":"Runs a Python script for each time series of the input dataset.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    },
    "script":{
      "description":"Python script that will be executed over all time series, gets time series as (Pandas) DataFrame and expects a new DataFrame as output."
    },
    "version":{
      "description":"Python version to use, defaults to the latest available version.",
      "required":false,
      "default":"latest"
    }
  }
}
```

#### 3. Upload python script

**Request**
```
PUT /users/me/files/s1_aggregate.py HTTP/1.1
```


**Response**
```
Header:
HTTP/1.1 200 OK
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body: none
```


#### 4. Create a job

**Request**
```
POST /jobs HTTP/1.1
Content-Type: application/json; charset=utf-8

Body:
{
  "process_graph":{
    "process_id":"/udf/Python/aggregate_time",
    "args":{
      "script":"/users/me/files/s1_aggregate.py",
      "imagery":{
        "process_id":"filter_daterange",
        "args":{
          "imagery":{
            "process_id":"filter_bbox",
            "args":{
              "imagery":{
                "product_id":"Sentinel1-L1-IW-GRD"
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
      }
    }
  }
}
```


**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "job_id":"3723c32fb7b24698832ca71f2d3f18aa",
  "status":"submitted",
  "submitted":"2017-01-01T09:32:12Z",
  "updated":"2017-01-01T09:36:18Z",
  "user_id":"bd6f9faf93b4",
  "consumed_credits":0
}
```

#### 5. Create a TMS service

**Request**

```
POST /services HTTP/1.1
Content-Type: application/json; charset=utf-8

Body:
{
  "job_id":"3723c32fb7b24698832ca71f2d3f18aa",
  "type":"tms"
}
```

**Response**

```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "service_id":"9dab4b6f6523",
  "service_url":"http://cdn.cloudprovider.com/openeo/services/9dab4b6f6523/tms",
  "service_type":"tms",
  "job_id":"3723c32fb7b24698832ca71f2d3f18aa"
}
```

#### 6. Download results as TMS


**Example Request**
```
GET http://cdn.cloudprovider.com/openeo/services/9dab4b6f6523/tms/2017-01-01/12/2232/2668/?bands=1 HTTP/1.1
```

**Response**
_omitted_



## Use Case 3

### Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons

#### 1. Check whether Sentinel 2A Level 1C data is available at the back-end

**Request**
```
GET /data/Sentinel2A-L1C HTTP/1.1
```


**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "product_id":"Sentinel-2A-L1C",
  "description":"Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
  "source":"European Space Agency (ESA)",
  "extent":[
    -34,
    35,
    39,
    71
  ],
  "time":[
    "2016-01-01",
    "2017-10-01"
  ],
  "bands":[
    {
      "band_id":"1",
      "wavelength_nm":443.9,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"2",
      "name":"blue",
      "wavelength_nm":496.6,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"3",
      "name":"green",
      "wavelength_nm":560,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"4",
      "name":"red",
      "wavelength_nm":664.5,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"5",
      "wavelength_nm":703.9,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"6",
      "wavelength_nm":740.2,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"7",
      "wavelength_nm":782.5,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"8",
      "name":"nir",
      "wavelength_nm":835.1,
      "res_m":10,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"8a",
      "wavelength_nm":864.8,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"9",
      "wavelength_nm":945,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"10",
      "wavelength_nm":1373.5,
      "res_m":60,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"11",
      "wavelength_nm":1613.7,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    },
    {
      "band_id":"12",
      "wavelength_nm":2202.4,
      "res_m":20,
      "scale":0.0001,
      "offset":0,
      "type":"int16",
      "unit":"1"
    }
  ]
}


```


#### 2. Check whether the back-end supports computing `zonal_statistics` 


**Request**
```
GET /processes/zonal_statistics HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "process_id":"zonal_statistics",
  "description":"Runs a Python script for each time series of the input dataset.",
  "args":{
    "imagery":{
      "description":"array of input collections with one element"
    },
    "regions":{
      "description":"Polygon file readable by OGR"
    },
    "func":{
      "description":"Function to apply over the polygons, one of `avg`, `min`, `max`, `median`, `q25`, or `q75`.",
      "required":false,
      "default":"avg"
    }
  }
}
```


#### 3. Upload a GeoJSON Polygon

**Request**
```
PUT /user/me/files/polygon1.json HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body: none
```

#### 4. Create a job
**Request**
```
POST /jobs HTTP/1.1
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
                    "product_id":"Sentinel2-L1C"
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
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "job_id":"f6ea12c5e283438a921b525af826da08",
  "status":"submitted",
  "submitted":"2017-01-01T09:32:12Z",
  "updated":"2017-01-01T09:36:18Z",
  "user_id":"bd6f9faf93b4",
  "consumed_credits":0
}
```

#### 5. Start batch computation at the back-end

**Request**

```
PATCH /jobs/f6ea12c5e283438a921b525af826da08/queue HTTP/1.1
```

**Response**

```
Header:
HTTP/1.1 200 OK
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body: none
```

#### 6. Check job status twice

**Request**
```
GET /jobs/f6ea12c5e283438a921b525af826da08 HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "job_id":"f6ea12c5e283438a921b525af826da08",
  "user_id":"bd6f9faf93b4",
  "status":"running",
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
                    "product_id":"Sentinel2-L1C"
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
  },
  "submitted":"2017-01-01 09:32:12",
  "updated":"2017-01-01 09:34:11",
  "consumed_credits":231
}
```

**Request**
```
GET /jobs/f6ea12c5e283438a921b525af826da08 HTTP/1.1
```

**Response**
```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
{
  "job_id":"f6ea12c5e283438a921b525af826da08",
  "user_id":"bd6f9faf93b4",
  "status":"finished",
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
                    "product_id":"Sentinel2-L1C"
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
  },
  "submitted":"2017-01-01 09:32:12",
  "updated":"2017-01-01 09:36:57",
  "consumed_credits":450
}
```

#### 7. Retrieve download links


**Request**
```
GET /jobs/f6ea12c5e283438a921b525af826da08/download HTTP/1.1
```

**Response**

```
Header:
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Access-Control-Allow-Origin: <Origin>
Access-Control-Allow-Credentials: true

Body:
[
  "https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/1.gpkg"
]


```

#### 8. Download file(s)

**Request**

```
GET https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/1.gpkg HTTP/1.1
```

**Response (GPKG file)**
_omitted_

