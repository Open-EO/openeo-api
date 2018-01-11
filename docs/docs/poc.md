# Proof of Concept

This page gives a detailed description of the OpenEO proof of concept and gives a list and specification of what needs to be implemented. The proof of concept will consist of

* at least three clearly defined example processes (see below),
* a prototypical API specification including communication API call sequences of the processes (see below),
* implementations of the processes on three back-ends (file-based, Spark, EURAC), and
* prototypical clients in R and Python.

Below, we define the examples processes and how they are translated to sequences of API calls.

## Example Process 1: Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery


#### 1. Check whether Sentinel 2A Level 1C data is available at the back-end

**Request**
```
GET /data/Sentinel2A-L1C
``` 

**Response**
```
HTTP 200/OK
Body:
{
    "product_id": "Sentinel-2A-L1C",
    "description": "Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
    "source": "European Space Agency (ESA)",
    "extent": [ -34, 35, 39, 71],
    "time": [ "2016-01-01", "2017-10-01"],
    "bands": 
    [{
        "band_id": "1",
        "wavelength_nm": 443.9,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "2",
        "name": "blue",
        "wavelength_nm": 496.6,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "3",
        "name": "green",
        "wavelength_nm": 560,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "4",
        "name": "red",
        "wavelength_nm": 664.5,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "5",
        "wavelength_nm": 703.9,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "6",
        "wavelength_nm": 740.2,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "7",
        "wavelength_nm": 782.5,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "8",
        "name": "nir",
        "wavelength_nm": 835.1,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "8a",
        "wavelength_nm": 864.8,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "9",
        "wavelength_nm": 945,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "10",
        "wavelength_nm": 1373.5,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "11",
        "wavelength_nm": 1613.7,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "12",
        "wavelength_nm": 2202.4,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    }]
}

```


#### 2. Check that needed processes are available

**Request**
```
GET /processes/filter_bbox
```

**Response**
```
HTTP 200/OK
Body:
{
    "process_id": "filter_bbox",
    "description": "Drops observations from a collection that are located outside of a given bounding box.",
    "args": {
       "collections": {
            "description": "array of input collections with one element"
        },
        "left" : {
            "description" : "left boundary (longitude / easting)"
        },
        "right" : {
            "description" : "right boundary (longitude / easting)"
        },
        "top" : {
            "description" : "top boundary (latitude / northing)"
        },
        "bottom" : {
            "description" : "bottom boundary (latitude / northing)"
        },
        "srs" : {
            "description" : "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
        }
    }
}
```

**Request**
```
GET /processes/filter_daterange
```

**Response**
```
HTTP 200/OK
Body:
{
    "process_id": "filter_daterange",
    "description": "Drops observations from a collection that have been captured before a start or after a given end date.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "from" : {
            "description" : "start date"
        },
        "to" : {
            "description" : "end date"
        }
    }
}
```



**Request**
```
GET /processes/NDVI
```

**Response**
```
HTTP 200/OK
Body:
{
    "process_id": "NDVI",
    "description": "Finds the minimum value of time series for all bands of the input dataset.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "red" : {
            "description" : "reference to the red band"
        },
        "nir" : {
            "description" : "reference to the nir band"
        }
    }
}
```

**Request**
```
GET /processes/min_time
```

**Response**
```
HTTP 200/OK
Body:
{
    "process_id": "min_time",
    "description": "Finds the minimum value of time series for all bands of the input dataset.",
    "args": {
       "collections": {
            "description": "array of input collections with one element"
        },
    }
}
```

#### 3. Create a job with the computation at the back-end 

**Request**
```
POST /jobs&evaluate=lazy
Body:
{
  "process_graph": {
    "process_id": "min_time",
    "args": {
      "collections": [{
        "process_id": "NDVI",
        "args": {
          "collections": [{
            "process_id": "filter_daterange",
            "args": {
              "collections": [{
                "process_id": "filter_bbox",
                "args": {
                "collections": [{
                    "product_id": "S2_L2A_T32TPS_20M"
                }],
                "left" : 652000,
                "right" :672000,
                "top" : 5161000,
                "bottom" : 5181000,
                "srs" : "EPSG:32632"
                }
              }],
	      "from": "2017-01-01",
              "to": "2017-01-31"
            }
          }],
          "red": "B04",
          "nir": "B8A"
        }
      }]
    }
  }
}
```
**Response**
```
HTTP 200/OK
Body:
{"job_id" : "2a8ffb20c2b235a3f3e3351f"}
```

#### 4. Download the data on demand with WCS

**Request**
```
GET /download/2a8ffb20c2b235a3f3e3351f/wcs?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCapabilities
```

**Response**
_omitted_

**Request**
```
GET /download/2a8ffb20c2b235a3f3e3351f/wcs?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=2a8ffb20c2b235a3f3e3351f&FORMAT=image/tiff&SUBSET=x,http://www.opengis.net/def/crs/EPSG/0/4326(16.1,16.5)&SUBSET=y,http://www.opengis.net/def/crs/EPSG/0/4326(47.9,48.6)&&SIZE=x(200)&SIZE=y(200)
```


**Response** 
_omitted_


#### 5. Stop the job


**Request**
```
GET /jobs/2a8ffb20c2b235a3f3e3351f/cancel
```

**Response**
```
HTTP 200/OK
```



## Example Process 2: Create a monthly aggregated Sentinel 1 product from a custom Python script



#### 1. Ask the back-end for available Sentinel 1 data

**Request**
```
GET /data/Sentinel1-L1-IW-GRD
``` 


**Response**
```
HTTP 200/OK
Body:
{
    "product_id": "Sentinel1-L1-IW-GRD",
    "description": "Sentinel 1 C-band Synthetic Aperture Radar (SAR) Ground Range Data",
    "source": "European Space Agency (ESA)",
    "extent": [ -34, 35, 39, 71],
    "time": [ "2016-01-01", "2017-10-01"],
    "bands": [
    {
        "band_id": "VV",
    },
    {
        "band_id": "VH",
    }
    ]
}
```


#### 2. Ask the back-end whether it supports Python UDFs of type aggregate_time and get details about expected parameters

**Request**
```
GET /udf
``` 


**Response**
```
HTTP 200/OK
Body:
{
  "Python": {
    "udf_types": [
      "reduce_time",
      "aggregate_time",
      "apply_pixel",
      "
    ],
    "versions": {
      "3.6.3": {
        "packages": [
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
GET /udf/Python/aggregate_time
``` 


**Response**
```
HTTP 200/OK
{
  "process_id": "/udf/Python/aggregate_time",
  "description": "Runs a Python script for each time series of the input dataset.",
  "args": {
    "collections": {
      "description": "array of input collections with one element"
    },
    "script": {
      "description": "Python script that will be executed over all time series, gets time series as (Pandas) DataFrame and expects a new DataFrame as output."
    },
    "version" : {
       "description" : "Python version to use, defaults to the latest available version."
       "required" : false,
       "default" : "latest" 
    }
  }
}
```



#### 3. Upload python script

**Request**
```
PUT /users/me/files/s1_aggregate.py
``` 


**Response**
```
HTTP 200/OK
```


#### 4. Create a job

**Request**
```
POST /jobs?evaluate=lazy
Body:
{
    "process_graph": {
        "process_id": "/udf/Python/aggregate_time",
        "args": {
            "script" : "/users/me/files/s1_aggregate.py",        
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [{
                                "product_id": "Sentinel1-L1-IW-GRD"
                            }],
                            "left" : ‎ 16.1,
                            "right" : ‎16.6,
                            "top" : 48.6,
                            "bottom" : 47.2,
                            "srs" : "EPSG:4326"
                        },
                    }],
                    "from": "2017-01-01",
                    "to": "2017-01-31"
                }
            }]
        }
    }
}
``` 


**Response**
```
HTTP 200/OK
Body:
{"job_id" : "3723c32fb7b24698832ca71f2d3f18aa"}
```


#### 5. Download results as TMS


**Example Request**
```
GET /download/3723c32fb7b24698832ca71f2d3f18aa/tms/2017-01-01/12/2232/2668/?bands=1
``` 

**Response**
_omitted_









## Example Process 3: Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons



#### 1. Check whether Sentinel 2A Level 1C data is available at the back-end

**Request**
```
GET /data/Sentinel2A-L1C
``` 


**Response**
```
HTTP 200/OK
Body:
{
    "product_id": "Sentinel-2A-L1C",
    "description": "Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
    "source": "European Space Agency (ESA)",
    "extent": [ -34, 35, 39, 71],
    "time": [ "2016-01-01", "2017-10-01"],
    "bands": 
    [{
        "band_id": "1",
        "wavelength_nm": 443.9,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "2",
        "name": "blue",
        "wavelength_nm": 496.6,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "3",
        "name": "green",
        "wavelength_nm": 560,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "4",
        "name": "red",
        "wavelength_nm": 664.5,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "5",
        "wavelength_nm": 703.9,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "6",
        "wavelength_nm": 740.2,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "7",
        "wavelength_nm": 782.5,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "8",
        "name": "nir",
        "wavelength_nm": 835.1,
        "res_m": 10,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "8a",
        "wavelength_nm": 864.8,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "9",
        "wavelength_nm": 945,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "10",
        "wavelength_nm": 1373.5,
        "res_m": 60,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "11",
        "wavelength_nm": 1613.7,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    },
    {
        "band_id": "12",
        "wavelength_nm": 2202.4,
        "res_m": 20,
        "scale": 0.0001,
        "offset": 0,
        "type": "int16",
        "unit": "1"
    }]
}
```


#### 2. Check whether the back-end supports computing `zonal_statistics` 


**Request**
```
GET /processes/zonal_statistics
```

**Response**
```
HTTP 200/OK
{
  "process_id": "zonal_statistics",
  "description": "Runs a Python script for each time series of the input dataset.",
  "args": {
    "collections": {
      "description": "array of input collections with one element"
    },
    "regions": {
      "description": "Polygon file readable by OGR"
    },
    "func" : {
       "description" : "Function to apply over the polygons, one of `"avg"`, `"min"`, `"max"`, `"median"`, `"q25"`, or `"q75"` .", 
       "required" : false,
       "default" : "avg" 
    },
    "outformat" : {
       "description" : "Output format as OGR identifier string, defaults to GeoPackage", 
       "required" : false,
       "default" : "GPKG" 
    }
  }
}
```


#### 3. Upload a GeoJSON Polygon

**Request**
```
PUT /user/me/files/polygon1.json
```

**Response**
```
HTTP 200/OK
```





#### 4. Create a job with the computation at the back-end
**Request**
```
POST /jobs?evaluate=batch
Body:
{
    "process_graph": {
        "process_id": "zonal_statistics",
        "args": {        
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [{
                                "process_id" : "filter_bands",
                                "args" : {
                                    "collections" : [
                                        {
                                            "product_id": "Sentinel2-L1C"
                                        }
                                    ],
                                    "bands": 8
                                }
                            }],
                            "left" : ‎ 16.1,
                            "right" : ‎16.6,
                            "top" : 48.6,
                            "bottom" : 47.2,
                            "srs" : "EPSG:4326"
                        },
                    }],
                    "from": "2017-01-01",
                    "to": "2017-01-31"
                }          
            }],
            "regions" : "/users/me/files/,
            "func" : "avg",
            "outformat" : "GPKG"
        }
    }
}
```


**Response**
```
HTTP 200/OK
Body:
{"job_id" : "f6ea12c5e283438a921b525af826da08"}
```


#### 5. Check job status

**Request**
```
GET /jobs/f6ea12c5e283438a921b525af826da08
```

**Response**
```
HTTP 200/OK
Body:
{
  "job_id": "f6ea12c5e283438a921b525af826da08",
  "user_id": "bd6f9faf93b4",
  "status": "running",
  "task": {
    "process_graph": {
        "process_id": "zonal_statistics",
        "args": {        
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [{
                                "process_id" : "filter_bands",
                                "args" : {
                                    "collections" : [
                                        {
                                            "product_id": "Sentinel2-L1C"
                                        }
                                    ],
                                    "bands": 8
                                }
                            }],
                            "left" : ‎ 16.1,
                            "right" : ‎16.6,
                            "top" : 48.6,
                            "bottom" : 47.2,
                            "srs" : "EPSG:4326"
                        },
                    }],
                    "from": "2017-01-01",
                    "to": "2017-01-31"
                }          
            }],
            "regions" : "/users/me/files/,
            "func" : "avg",
            "outformat" : "GPKG"
        }
    }
  },
  "submitted": "2017-01-01 09:32:12",
  "last_update": "2017-01-01 09:36:18",
  "consumed_credits": "0.231"
}
```

**Request**
```
GET /jobs/f6ea12c5e283438a921b525af826da08
```

**Response**
```
HTTP 200/OK
Body:
{
  "job_id": "f6ea12c5e283438a921b525af826da08",
  "user_id": "bd6f9faf93b4",
  "status": "finished",
  "task": {
   "process_graph": {
        "process_id": "zonal_statistics",
        "args": {        
            "collections": [{
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{
                        "process_id": "filter_bbox",
                        "args": {
                            "collections": [{
                                "process_id" : "filter_bands",
                                "args" : {
                                    "collections" : [
                                        {
                                            "product_id": "Sentinel2-L1C"
                                        }
                                    ],
                                    "bands": 8
                                }
                            }],
                            "left" : ‎ 16.1,
                            "right" : ‎16.6,
                            "top" : 48.6,
                            "bottom" : 47.2,
                            "srs" : "EPSG:4326"
                        },
                    }],
                    "from": "2017-01-01",
                    "to": "2017-01-31"
                }          
            }],
            "regions" : "/users/me/files/,
            "func" : "avg",
            "outformat" : "GPKG"
        }
    }
  },
  "submitted": "2017-01-01 09:32:12",
  "last_update": "2017-01-01 09:36:57",
  "consumed_credits": "0.231"
}
```

#### 7. Download results


**Example Request**
```
GET /download/f6ea12c5e283438a921b525af826da08
``` 

**Response (GPKG file)**
_omitted_

