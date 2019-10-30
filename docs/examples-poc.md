# Examples (proof of concept)

This page gives a detailed description of the openEO proof of concept use cases. After the proof of concept, this stays in the API to have some basic examples. The proof of concept covered three clearly defined example use cases and how they are translated to sequences of API calls: 

1. [Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery](#use-case-1)
2. [Create a monthly aggregated Sentinel 1 product from a custom Python script](#use-case-2)
3. [Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-specified polygons](#use-case-3)

**Note**: [CORS](apireference.md#section/Cross-Origin-Resource-Sharing-(CORS)) and authentication is not included in these examples for simplicity.
Repeating calls are also not included as it would not make much sense to list the same discovery requests (see Use Case 1, requests 1 to 6) for each use case individually.

## Use Case 1

Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.

[A similar example (computing an EVI) is also available.](apireference.md#section/Example)

1. **Requesting the API versions available at the back-end**

    *Request* 

    ``` http
    GET /.well-known/openeo
    ```

2. **Requesting the capabilities of the back-end**

    *Note:* The actual request path depends on the response of the previous request.

    *Request*

    ``` http
    GET /
    ```

3. **Check which collections are available at the back-end**

    *Request*

    ``` http
    GET /collections HTTP/1.1
    ```

4. **Request details about a specific collection** (e.g. Sentinel 2)

    *Note:* The actual collection ID in the path depends on the response of the previous request.

    *Request*

    ``` http
    GET /collections/Sentinel-2 HTTP/1.1
    ```

5. **Check that needed processes are available**

    *Request*

    ``` http
    GET /processes HTTP/1.1
    ```

6. **Request the supported secondary web service types**

    *Request*

    ``` http
    GET /service_types HTTP/1.1
    ```

7. **Create a WMS service**

    *Request*

    ``` http
    POST /services HTTP/1.1
    Content-Type: application/json; charset=utf-8
    
    {
      "title": "Min. NDVI for Sentinel 2",
      "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2 imagery.",
      "process_graph": {
        "loadco1": {
          "process_id": "load_collection",
          "arguments": {
            "id": "Sentinel-2",
            "spatial_extent": {
              "west": {"variable_id": "spatial_extent_west"},
              "east": {"variable_id": "spatial_extent_east"},
              "north": {"variable_id": "spatial_extent_north"},
              "south": {"variable_id": "spatial_extent_south"}
            },
            "temporal_extent": ["2017-01-01", "2017-02-01"]
          }
        },
        "ndvi1": {
          "process_id": "ndvi",
          "arguments": {
            "data": {"from_node": "loadco1"}
          }
        },
        "reduce1": {
          "process_id": "reduce",
          "arguments": {
            "data": {"from_node": "ndvi1"},
            "dimension": "temporal",
            "reducer": {
              "callback": {
                "min1": {
                  "process_id": "min",
                  "arguments": {
                    "data": {"from_argument": "data"}
                  },
                  "result": true
                }
              }
            }
          },
          "result": true
        }
      },
      "type": "WMS",
      "parameters": {
        "version": "1.1.1"
      }
    }
    ```

    *Response*

    ``` http
    HTTP/1.1 201 Created
    Location: /services/wms-a3cca9
    OpenEO-Identifier: wms-a3cca9
    ```

8. **Requesting the service information**

    *Request*

    ```http
    GET /services/wms-a3cca9 HTTP/1.1
    ```

9. **Download the data on demand from the WMS**

    Omitted, not part of the openEO API.

## Use Case 2

Create a monthly aggregated Sentinel 1 product from a custom Python script.

1. **Upload python script**

    *Request*

    ``` http
    PUT /files/s1_aggregate.py HTTP/1.1
    Content-Type: application/octet-stream
    
    <File content>
    ```

2. **Create a batch job**

    *Request*

    ```http
    POST /jobs HTTP/1.1
    Content-Type: application/json; charset=utf-8
    
    {
      "title": "Monthly aggregation on Sentinel 1",
      "description": "Create a monthly aggregated Sentinel 1 product from a custom Python script.",
      "process_graph": {
        "loadco1": {
          "process_id": "load_collection",
          "arguments": {
            "id": "Sentinel-1",
            "spatial_extent": {
              "west": 16.1,
              "east": 16.6,
              "north": 48.6,
              "south": 47.2
            },
            "temporal_extent": ["2017-01-01", "2017-02-01"]
          }
        },
        "reduce1": {
          "process_id": "reduce",
          "arguments": {
            "data": {"from_node": "loadco1"},
            "dimension": "temporal",
            "reducer": {
              "callback": {
                "runudf1": {
                  "process_id": "run_udf",
                  "arguments": {
                    "data": [
                      {"from_argument": "x"},
                      {"from_argument": "y"}
                    ],
                    "udf": "s1_aggregate.py",
                    "runtime": "Python"
                  },
                  "result": true
                }
              }
            },
            "binary": true
          },
          "result": true
        }
      }
    }
    ```

    *Response*

    ```http
    HTTP/1.1 201 Created
    Location: https://openeo.org/api/v0.4/jobs/132
    OpenEO-Identifier: 132
    ```

3. **Start batch processing the job**

    *Request*

    ```http
    POST /jobs/132/results HTTP/1.1
    ```

4. **Create a TMS service**

    *Request*

    ```http
    POST /services HTTP/1.1
    Content-Type: application/json; charset=utf-8
    
    {
      "title": "Monthly aggregation on Sentinel 1",
      "description": "Create a monthly aggregated Sentinel 1 product from a custom Python script.",
      "process_graph": {
        "1": {
          "process_id": "load_result",
          "arguments": {
            "id": "132"
          },
          "result": true
        }
      },
      "type": "TMS"
    }
    ```

    *Response*

    ```http
    HTTP/1.1 201 Created
    Location: https://openeo.org/api/v0.4/services/tms-75ff8c
    OpenEO-Identifier: tms-75ff8c
    ```

5. **Requesting the service information**

    *Request*

    ```http
    GET https://openeo.org/api/v0.4/services/tms-75ff8c HTTP/1.1
    ```

6. **Download the data on demand from the WMS**

    Omitted, not part of the openEO API.

## Use Case 3

Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-specified polygons.

1. **Create a batch job**

    *Request*

    ``` http
    POST /jobs HTTP/1.1
    Content-Type: application/json; charset=utf-8
    
    {
      "title": "Zonal Statistics / Sentinel 2",
      "description": "Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-specified polygons.",
      "process_graph": {
        "loadco1": {
          "process_id": "load_collection",
          "arguments": {
            "id": "Sentinel-2",
            "spatial_extent": {
              "west": 16.1,
              "east": 16.6,
              "north": 48.6,
              "south": 47.2
            },
            "temporal_extent": ["2017-01-01", "2017-02-01"],
            "bands": ["B8"]
          }
        },
        "reduce1": {
          "process_id": "reduce",
          "arguments": {
            "data": {"from_node": "loadco1"},
            "dimension": "spectral"
          }
        },
        "aggreg1": {
          "process_id": "aggregate_polygon",
          "arguments": {
            "data": {"from_node": "reduce1"},
            "polygons": {
              "type": "Polygon",
              "coordinates": [
                [
                  [16.138916,48.320647],
                  [16.524124,48.320647],
                  [16.524124,48.1386],
                  [16.138916,48.1386],
                  [16.138916,48.320647]
                ]
              ]
            },
            "reducer": {
              "callback": {
                "mean1": {
                  "process_id": "mean",
                  "arguments": {
                    "data": {"from_argument": "data"}
                  },
                  "result": true
                }
              }
            }
          }
        },
        "savere1": {
          "process_id": "save_result",
          "arguments": {
            "data": {"from_node": "aggreg1"},
            "format": "JSON"
          },
          "result": true
        }
      }
    }
    ```

    *Response*
    ``` http
    HTTP/1.1 201 Created
    Location: https://openeo.org/jobs/133
    OpenEO-Identifier: 133
    ```

2. **Start batch processing the job**

    *Request*

    ```http
    POST /jobs/133/results HTTP/1.1
    ```

3. **Retrieve download links** (after the job has finished)

    *Request*

    ``` http
    GET /jobs/133/results HTTP/1.1
    ```

    *Response*

    ``` http
    HTTP/1.1 200 OK
    Content-Type: application/json; charset=utf-8
    Expires: Wed, 01 May 2019 00:00:00 GMT
    OpenEO-Costs: 0
    
    {
      "id":"133",
      "title":"Zonal Statistics / Sentinel 2",
      "description":"Compute time series of zonal (regional) statistics of Sentinel 2 imagery over user-specified polygons.",
      "updated": "2019-02-01T09:36:18Z",
      "links": [
        {
          "href": "https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/result.json",
          "type": "application/json"
        }
      ]
    }
    ```

4. **Download file(s)**

    *Request*

    ``` http
    GET https://cdn.openeo.org/4854b51643548ab8a858e2b8282711d8/result.json HTTP/1.1
    ```

    *Response*

    A JSON file containing the results, content omitted.

