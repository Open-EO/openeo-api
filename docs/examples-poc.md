# Examples (proof of concept)

This page gives a detailed description of the openEO proof of concept use cases. After the proof of concept, this stays in the API to have some basic examples. The proof of concept covered three clearly defined example use cases and how they are translated to sequences of API calls: 

1. [Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery](#use-case-1)
2. [Create a monthly aggregated Sentinel 1 product from a custom Python script](#use-case-2)
3. [Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons](#use-case-3)

!!! note
    [CORS](cors.md) and authentication is not included in these examples for simplicity.
    Repeating calls are also not included as it would not make much sense to list the same discovery requests for each use case individually.

## Use Case 1

Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.

### 1. Requesting the capabilities of the back-end

**Request**

``` http
GET /
```

**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "version": "0.4.0"
  "endpoints": [
    {
      "path": "/collections",
      "methods": ["GET"]
    },
    {
      "path": "/collections/{name}",
      "methods": ["GET"]
    },
    {
      "path": "/processes",
      "methods": ["GET"]
    },
    {
      "path": "/jobs",
      "methods": ["GET","POST"]
    },
    {
      "path": "/jobs/{job_id}",
      "methods": ["GET","DELETE","PATCH"]
    },
    {
      "path": "/jobs/{job_id}/results",
      "methods": ["GET","POST","DELETE"]
    },
    {
      "path": "/services",
      "methods": ["GET","POST"]
    },
    {
      "path": "/services/{service_id}",
      "methods": ["GET","DELETE","PATCH"]
    }
  ],
  "billing": {
    "currency": "EUR",
    "plans": [
      {
        "name": "free",
        "description": "Free plan. Calculates one tile per second and a maximum amount of 100 tiles per hour.",
        "url": "http://openeo.org/plans/free-plan"
      }
    ]
  }
}
```

### 2. Check whether Sentinel 2A Level 1C data is available at the back-end

**Request**

``` http
GET /collections HTTP/1.1
```

**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "collections": [
    {
      "name": "Sentinel-2A",
      "title": "Sentinel-2A MSI L1C",
      "description": "Sentinel-2A is a wide-swath, high-resolution, multi-spectral imaging mission supporting Copernicus Land Monitoring studies, including the monitoring of vegetation, soil and water cover, as well as observation of inland waterways and coastal areas.",
      "license": "proprietary",
      "extent": {
        "spatial": [
          180,
          -56,
          -180,
          83
        ],
        "temporal": [
          "2015-06-23T00:00:00Z",
          null
        ]
      },
      "links": [
        {
          "rel": "self",
          "href": "https://openeo.org/api/collections/Sentinel-2A"
        },
        {
          "rel": "license",
          "href": "https://scihub.copernicus.eu/twiki/pub/SciHubWebPortal/TermsConditions/Sentinel_Data_Terms_and_Conditions.pdf"
        }
      ]
    }
  ],
  "links": [
    {
      "rel": "self",
      "href": "https://openeo.org/api/collections"
    }
  ]
}
```


### 3. Check that needed processes are available

**Request**
``` http
GET /processes HTTP/1.1
```

**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "processes": [
    {
      "name": "get_collection",
      "summary": "Selects a collection.",
      "description": "Filters and selects a single collection provided by the back-end. The back-end provider decides which of the potential collections is the most relevant one to be selected.",
      "min_parameters": 1,
      "parameters": {
        "name": {
          "description": "Filter by collection name",
          "schema": {
            "type": "string",
            "examples": [
              "Sentinel2A-L1C"
            ]
          }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      }
    },
    {
      "name": "filter_bands",
      "summary": "Filters by bands.",
      "description": "Allows to extract one or multiple bands of multi-band raster image collection.\nBands can be chosen either by band id, band name or by wavelength.\n\nimagery and at one of the other arguments is required to be specified.",
      "min_parameters": 2,
      "parameters": {
        "imagery": {
          "description": "EO data to process.",
          "required": true,
          "schema": {
            "type": "object",
            "format": "eodata"
          }
        },
        "bands": {
          "description": "string or array of strings containing band ids.",
          "schema": {
            "type": [
              "string",
              "array"
            ],
            "items": {
              "type": "string"
            }
          }
        },
        "names": {
          "description": "string or array of strings containing band names.",
          "schema": {
            "type": [
              "string",
              "array"
            ],
            "items": {
              "type": "string"
            }
          }
        },
        "wavelengths": {
          "description": "Either a number specifying a specific wavelength or a two-element array of numbers specifying a minimum and maximum wavelength.",
          "schema": {
            "type": [
              "number",
              "array"
            ],
            "minItems": 2,
            "maxItems": 2,
            "items": {
              "type": "number"
            }
          }
        }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      }
    },
    {
      "name": "filter_daterange",
      "summary": "Filters by temporal extent.",
      "parameters": {
        "imagery": {
          "description": "EO data to process.",
          "required": true,
          "schema": {
            "type": "object",
            "format": "eodata"
          }
        },
        "extent": {
          "description": "Temporal extent specified by a start and an end time, each formatted as a [RFC 3339](https://www.ietf.org/rfc/rfc3339) date-time. Open date ranges are supported and can be specified by setting one of the times to null. Setting both entries to null is not allowed.",
          "schema": {
            "type": "array",
            "format": "temporal_extent",
            "required": true,
            "example": [
              "2016-01-01T00:00:00Z",
              "2017-10-01T00:00:00Z"
            ],
            "items": {
              "type": [
                "string",
                "null"
              ],
              "format": "date-time",
              "minItems": 2,
              "maxItems": 2
            }
          }
        }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      }
    },
    {
      "name": "filter_bbox",
      "summary": "Filters by spatial extent.",
      "parameters": {
        "imagery": {
          "description": "EO data to process.",
          "required": true,
          "schema": {
            "type": "object",
            "format": "eodata"
          }
        },
        "extent": {
          "description": "Spatial extent, may include a vertical axis (height or depth).",
          "schema": {
            "type": "object",
            "format": "spatial_extent",
            "required": [
              "west",
              "south",
              "east",
              "north"
            ],
            "properties": {
              "crs": {
                "description": "Coordinate reference system. EPSG codes must be supported. In addition, proj4 strings should be supported by back-ends. Whenever possible, it is recommended to use EPSG codes instead of proj4 strings.\nDefaults to `EPSG:4326` unless the client explicitly requests a different coordinate reference system.",
                "type": "string",
                "default": "EPSG:4326"
              },
              "west": {
                "description": "West (lower left corner, coordinate axis 1).",
                "type": "number"
              },
              "south": {
                "description": "South (lower left corner, coordinate axis 2).",
                "type": "number"
              },
              "east": {
                "description": "East (upper right corner, coordinate axis 1).",
                "type": "number"
              },
              "north": {
                "description": "North (upper right corner, coordinate axis 2).",
                "type": "number"
              },
              "base": {
                "description": "Base (optional, lower left corner, coordinate axis 3).",
                "type": "number"
              },
              "height": {
                "description": "Height (optional, upper right corner, coordinate axis 3).",
                "type": "number"
              }
            }
          }
        }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      }
    },
    {
      "name": "NDVI",
      "summary": "Calculates the Normalized Difference Vegetation Index.",
      "parameters": {
        "imagery": {
          "description": "EO data to process.",
          "required": true,
          "schema": {
            "type": "object",
            "format": "eodata"
          }
        },
        "red": {
          "description": "Band id of the red band.",
          "required": true,
          "schema": {
            "type": "string"
          }
        },
        "nir": {
          "description": "Band id of the near-infrared band.",
          "required": true,
          "schema": {
            "type": "string"
          }
        }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      },
      "exceptions": {
        "RedBandInvalid": {
          "description": "The specified red band is not available or contains invalid data."
        },
        "NirBandInvalid": {
          "description": "The specified nir band is not available or contains invalid data."
        }
      }
    },
    {
      "name": "min_time",
      "summary": "Calculates minimum values of time series.",
      "description": "Finds the minimum value of time series for all bands of the input dataset.",
      "parameters": {
        "imagery": {
          "description": "EO data to process.",
          "required": true,
          "schema": {
            "type": "object",
            "format": "eodata"
          }
        }
      },
      "returns": {
        "description": "Processed EO data.",
        "schema": {
          "type": "object",
          "format": "eodata"
        }
      }
    }
  ],
  "links": {}
}
```

### 4. Request the supported secondary web service types

**Request**
``` http
GET /service_types HTTP/1.1
Content-Type: application/json; charset=utf-8
```
**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "WMS": {
    "parameters": {
      "version": {
        "type": "string",
        "description": "The WMS version to use.",
        "default": "1.3.0",
        "enum": [
          "1.1.1",
          "1.3.0"
        ]
      }
    },
    "attributes": {
      "layers": {
        "type": "array",
        "description": "Array of layer names.",
        "example": [
          "roads",
          "countries",
          "water_bodies"
        ]
      }
    }
  }
}
```

### 5. Create a WMS service

**Request**

``` http
POST /services HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "title": "Min. NDVI for Sentinel 2",
  "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.",
  "process_graph": {
    "process_id": "min_time",
    "imagery": {
      "process_id": "NDVI",
      "imagery": {
        "process_id": "filter_daterange",
        "imagery": {
          "process_id": "get_collection",
          "name": "Sentinel-2A"
        },
        "extent": [
          "2017-01-01T00:00:00Z",
          "2017-01-31T23:59:59Z"
        ]
      },
      "red": "B4",
      "nir": "B8"
    }
  },
  "type": "WMS",
  "enabled": true,
  "parameters": {
    "version": "1.1.1"
  },
  "plan": "free"
}
```

**Response**

``` http
HTTP/1.1 201 Created
Location: https://openeo.org/api/v0.4/services/wms-a3cca9
OpenEO-Identifier: wms-a3cca9
```

### 6. Requesting the service information

**Request**

```http
POST https://openeo.org/api/v0.4/services/wms-a3cca9 HTTP/1.1
Content-Type: application/json; charset=utf-8
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "service_id": "wms-a3cca9",
  "title": "Min. NDVI for Sentinel 2",
  "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.",
  "process_graph": {
    "process_id": "min_time",
    "imagery": {
      "process_id": "NDVI",
      "imagery": {
        "process_id": "filter_daterange",
        "imagery": {
          "process_id": "get_collection",
          "name": "Sentinel-2A"
        },
        "extent": [
          "2017-01-01T00:00:00Z",
          "2017-01-31T23:59:59Z"
        ]
      },
      "red": "B4",
      "nir": "B8"
    }
  },
  "url": "https://openeo.org/wms/a3cca9",
  "type": "WMS",
  "enabled": true,
  "parameters": {
    "version": "1.1.1"
  },
  "attributes": {
    "layers": [
      "min_time"
    ]
  },
  "submitted": "2017-01-01T09:32:12Z",
  "plan": "free",
  "budget": null
}
```

### 7. Download the data on demand from the WMS

*Omitted, not part of the openEO API. WMS is located at `https://openeo.org/wms/a3cca9`.*

## Use Case 2

Create a monthly aggregated Sentinel 1 product from a custom Python script.

### 1. Ask the back-end for available Sentinel 1 data

**Request**
``` http
GET /collections/Sentinel-1 HTTP/1.1
```


**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "name":"Sentinel-1",
  "description":"Sentinel 1 C-band Synthetic Aperture Radar (SAR) Ground Range Data",
  "license": "proprietary",
  "keywords": [
    "copernicus",
    "esa",
    "sentinel",
    "sar"
  ],
  "provider": [
    {
      "name": "European Space Agency (ESA)",
      "url": "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar"
    }
  ],
  "extent": {
    "spatial": [
      -34,
      35,
      39,
      71
    ],
    "temporal": [
      "2016-01-01T00:00:00Z",
      null
    ]
  },
  "links": [
    {
      "rel": "self",
      "href": "https://openeo.org/api/collections/Sentinel-1"
    },
    {
      "rel": "license",
      "href": "https://scihub.copernicus.eu/twiki/pub/SciHubWebPortal/TermsConditions/Sentinel_Data_Terms_and_Conditions.pdf"
    }
  ],
  "eo:constellation": "sentinel-1",
  "eo:bands": {
    "VV": {
      "common_name": "VV"
    },
    "VH": {
      "common_name": "VH"
    }
  }
}
```

### 2. Upload python script

**Request**
``` http
PUT /files/john_doe/s1_aggregate.py HTTP/1.1

<File content>
```


**Response**
``` http
HTTP/1.1 204 No Content
```

### 3. Create a job

**Request**

```http
POST /jobs HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "title": "Monthly aggregation on Sentinel 1",
  "description": "Create a monthly aggregated Sentinel 1 product from a custom Python script.",
  "process_graph":{
    "process_id":"aggregate_time",
    "script":"/files/john_doe/s1_aggregate.py",
    "imagery":{
      "process_id":"filter_daterange",
      "imagery":{
        "process_id":"filter_bbox",
        "imagery":{
          "process_id":"get_collection",
          "name":"Sentinel-1"
        },
        "extent":{
          "west":16.1,
          "south":47.2,
          "east":16.6,
          "north":48.6
        }
      },
      "extent":[
        "2017-01-01T00:00:00Z",
        "2017-01-31T23:59:59Z"
      ]
    }
  },
  "plan": "free"
}
```

**Response**

```http
HTTP/1.1 201 Created
Location: https://openeo.org/api/v0.4/jobs/132
OpenEO-Identifier: 132
```

### 4. Start batch processing the job

**Request**

```http
POST /jobs/132/results HTTP/1.1
```

**Response**

```http
HTTP/1.1 202 Accepted
```

### 5. Create a TMS service

**Request**

```http
POST /services HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "title": "Monthly aggregation on Sentinel 1",
  "description": "Create a monthly aggregated Sentinel 1 product from a custom Python script.",
  "process_graph": {
    "process_id": "get_results",
    "job_id": "132"
  },
  "type": "TMS",
  "enabled": true,
  "parameters": {},
  "plan": "free"
}
```

**Response**

```http
HTTP/1.1 201 Created
Location: https://openeo.org/api/v0.4/services/tms-75ff8c
```

### 6. Requesting the service information

**Request**

```http
POST https://openeo.org/api/v0.4/services/tms-75ff8c HTTP/1.1
Content-Type: application/json; charset=utf-8
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "service_id": "tms-75ff8c",
  "title": "Monthly aggregation on Sentinel 1",
  "description": "Create a monthly aggregated Sentinel 1 product from a custom Python script.",
  "process_graph": {
    "process_id": "get_results",
    "job_id": "132"
  },
  "url": "https://openeo.org/tms/75ff8c",
  "type": "TMS",
  "enabled": true,
  "parameters": {},
  "attributes": {},
  "submitted": "2018-01-01T12:32:12Z",
  "plan": "free",
  "budget": null
}
```

### 7. Download the data on demand from the WMS

*Omitted, not part of the openEO API. TMS is located at `https://openeo.org/tms/75ff8c`.*

## Use Case 3

Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons.


### 1. Upload a GeoJSON Polygon

**Request**
``` http
PUT /files/john_doe/polygon1.geojson HTTP/1.1

<File content>
```

**Response**
``` http
HTTP/1.1 204 No Content
```

### 2. Create a job

**Request**
``` http
POST /jobs HTTP/1.1
Content-Type: application/json; charset=utf-8

{
  "title":"Zonal Statistics / Sentinel 2",
  "description":"Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons.",
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
            "name":"Sentinel-2A"
          },
          "bands":"B8"
        },
        "extent":{
          "west":16.1,
          "south":47.2,
          "east":16.6,
          "north":48.6
        }
      },
      "extent":[
        "2017-01-01T00:00:00Z",
        "2017-01-31T23:59:59Z"
      ]
    },
    "regions":"/files/john_doe/polygon1.geojson",
    "func":"mean"
  },
  "output":{
    "format":"GPKG"
  },
  "plan":"free",
  "budget":null
}
```


**Response**
``` http
HTTP/1.1 201 Created
Location: https://openeo.org/jobs/133
OpenEO-Identifier: 133
```

### 3. Start batch processing the job

**Request**

```http
POST /jobs/133/results HTTP/1.1
```

**Response**

```http
HTTP/1.1 202 Accepted
```

### 4. Check job status

**Request**
``` http
GET /jobs/133 HTTP/1.1
```

**Response**
``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "job_id": "133",
  "title":"Zonal Statistics / Sentinel 2",
  "description":"Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons.",
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
            "name":"Sentinel-2A"
          },
          "bands":"B8"
        },
        "extent":{
          "west":16.1,
          "south":47.2,
          "east":16.6,
          "north":48.6
        }
      },
      "extent":[
        "2017-01-01T00:00:00Z",
        "2017-01-31T23:59:59Z"
      ]
    },
    "regions":"/files/john_doe/polygon1.geojson",
    "func":"mean"
  },
  "output":{
    "format":"GPKG"
  },
  "status":"finished",
  "submitted": "2017-02-01T09:32:12Z",
  "updated": "2017-02-01T09:36:18Z",
  "plan": "free",
  "costs": 0,
  "budget": null
}
```

### 5. Retrieve download links

**Request**

``` http
GET /jobs/133/results HTTP/1.1
```

**Response**

``` http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "title":"Zonal Statistics / Sentinel 2",
  "description":"Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-uploaded polygons.",
  "updated": "2017-02-01T09:36:18Z",
  "links": [
    {
      "href": "https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/result.gpkg",
      "type": "application/geopackage+sqlite3"
    }
  ]
}
```

### 6. Download file(s)

**Request**

``` http
GET https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/result.gpkg HTTP/1.1
```

**Response**

*A GeoPackage file, content omitted.*

