# Commercial Data Extension

The Commercial Data API extension provides an interface for discovering, ordering and using commercial data in the openEO API. 

- Version: **0.1.0**
- Stability: **experimental**
- [OpenAPI document](openapi.yaml)
- Conformance class: `https://api.openeo.org/extensions/commercial-data/0.1.0`

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

## Overview of the workflow

All the available datasets provided by a backend are listed on the `GET /collections` endpoint. The collections are normally freely accessible. This extension adds capabilities for providing collections that are not free of charge and require purchasing data products that can thereupon be used in processing. Commercial data collections usually allow purchasing small subsets of the data (products), for example, a single observation of an area.

Therefore, the client must have an ability to search the available products that match their desired criteria and inspect their metadata to decide whether the products should be purchased.

The client can then create an order for the desired products from a orderable collection. Because of the financial cost of purchasing the data, a separate endpoint for confirming the execution of that specific order should be implemented.

When the order is completed, the data is ingested in a collection and its ID is available at `/orders/{order_id}` as `target_collection_id`. The user should be able to access the data using the `target_collection_id` at the temporal and spatial location of the purchased products.

### Collection discovery

A backend should add general information about a commercial data collection to the `/collections` and `/collections/{collection_id}` endpoints, the same as with freely available collections. Only the metadata about the entire dataset needs to be provided, not about the specific data products that a user has already purchased. 

Commercial data collections are distinguished from freely available collections by including `"order:status": "orderable"` as specified in the [STAC Order extension](https://github.com/stac-extensions/order/tree/v1.0.0).

Commercial data collections can include an `order_parameters` field if ordering supports additional parameters that specify how the products should be delivered.

Commercial data collections must also include human-readable pricing information for searching and ordering the products. If searching the products is free it should be set to `null`. If needed, references to additional information about pricing can be added to `links` with the relation type `pricing_info`.

#### Example

```json
{
  "stac_version": "1.0.0",
  "stac_extensions": [
    "https://stac-extensions.github.io/datacube/v1.0.0/schema.json",
    "https://stac-extensions.github.io/order/v1.0.0/schema.json"
  ],
  "type": "Collection",
  "id": "PLEIADES",
  "title": "Airbus Pleiades",
  "description": "Pleiades is a satellite constellation providing very high-resolution optical imagery and is owned by Airbus. Pléiades is composed of two twin satellites orbiting the Earth 180° apart. The satellites deliver 0.5 m optical imagery and offer a daily revisit capability to any point on the globe.",
  "license": "proprietary",
  "providers": [...],
  "extent": {...},
  "cube:dimensions": {...},
  "summaries": {...},
  "assets": {...},
  "order:status": "orderable",
  "order_parameters": [
      {
        "name": "sample_type",
        "description": "sample type of the output raster.",
        "schema": {
          "type": "string",
          "enum": [
            "UINT16",
            "UINT8"
          ]
        },
      },
    ],
  "pricing": {
    "searching": null,
    "ordering": {
      "description": "Minimum area per order is 0.25 km2. The price is calculated based on a 6-months sliding window.",
    }
  },
  "links": [
    {
      "title": "Airbus Pleiades pricing",
      "rel": "pricing_info",
      "href": "https://www.sentinel-hub.com/pricing/#tpd_pricing"
    },
    ...
  ]
}
```

### Filtering parameters discovery

Searching for products can support refining the search by filtering with general or collection-specific attributes. Backends should implement a top level `/queryables` endpoint for attributes available for all collections, and collection-specific attributes should be provided at `/collections/{collection_id}/queryables` according to [OGC Queryables specification](https://portal.ogc.org/files/96288#filter-queryables) and [STAC Filter extension](https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-rc.1/fragments/filter).

#### Example

Example response from `GET /collections/PLEIADES/queryables`:
```json
{
   "$schema":"http://json-schema.org/draft-07/schema#",
   "$id":"http://openeo.example/collections/PLEIADES/queryables",
   "type":"object",
   "title":"Queryables of Airbus Pleiades collection.",
   "description":"Available properties for CQL filtering of products.",
   "properties":{
      "processing_level":{
         "title":"Processing level",
         "description":"Limit search to only Living Library images with 'SENSOR' or access all images with 'ALBUM'.",
         "type":"string",
         "enum":[
            "SENSOR",
            "ALBUM"
         ]
      },
      "max_snow_coverage":{
         "title":"Maximum snow coverage",
         "description":"The maximum allowable snow coverage in percent.",
         "type":"number",
         "minimum":0,
         "maximum":100,
         "default":100
      },
      "max_incidence_angle":{
         "title":"Maximum incidence angle",
         "description":"The maximum allowable incidence angle in degrees.",
         "minimum":0,
         "maximum":90,
         "default":90
      }
   }
}
```

### Searching available products

Backends should implement the top-level `GET /search` endpoint as specified in the [STAC Item Search API specification](https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-rc.1/item-search). This should include the [Filter Extension](https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-rc.1/fragments/filter), which enables filtering the available products by attributes specified in `GET /queryables` and `GET /collections/{collection-id}/queryables`.
The endpoint returns a list of [STAC Items](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md) that match the criteria. The products should be aligned with the STAC specification, utilising the existing [STAC extensions](https://github.com/radiantearth/stac-spec/blob/v1.0.0/extensions/README.md) as much as possible, and trying avoiding custom attributes, if a generally accepted definition does not exist. 

#### Example

Example request payload to `GET /search` for `PLEIADES` products from "Living Library" with no snow coverage.

```json
{
  "bbox": [3, 15, 4, 16],
  "datetime": ["01-01-2022", "01-02-2022"],
  "collections": ["PLEIADES"],
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "=",
        "args": [{"property": "processing_level"}, "SENSOR"]
      },
      {
        "op": "=",
        "args": [{"property": "max_snow_coverage"}, 0]
      }
    ]
  }
}
```

### Ordering products

Backends should implement the following endpoints:

- `GET /orders`: Get a list of all created orders
- `POST /orders`: Create an order
- `GET /orders/{order_id}`: Get full metadata of a specific order
- `POST /orders/{order_id}`: Confirm a created order

Optionally, they can also implement:
- `DELETE /orders/{order_id}`: Delete an order

See the [OpenAPI document](openapi.yaml) for details.

### Product metadata

The backend can provide full product metadata as STAC Items following [STAC API Features specification](https://github.com/radiantearth/stac-api-spec/tree/main/ogcapi-features). This requires implementing two additional endpoints, `/collections/{collection_id}/items` and `/collections/{collection_id}/items/{item_id}`. 

`/collections/{collection_id}/items/{item_id}` may return an error if the data has not been ingested yet.

Items should contain links to the respective orders that made them available using relation type `parent_order`.

### Payment

Payment should be done in the currency used by the backend, listed at `GET /` under `billing`. When an order is created, the backend should return the full final cost of the order. 

### Example usage with Python client

Python client could be extented to support commercial data. Here an example of a possible workflow is provided.

```python
>>> import openeo
>>> connection = openeo.connect("openeo.sentinel-hub.com")
>>> connection.list_collection_ids(status="orderable")
["PLEIADES", "SPOT", ...]
```

We can fetch queryables and hold them in a class that validates user's parameters against the schema and constructs the payload.
```python
>>> pleiades_queryables = connection.get_queryables(collection_id="PLEIADES")
>>> pleiades_queryables.list()
[{'name': 'processing_level', 'type': 'string', 'enum': ['SENSOR', 'ALBUM']}, {'name': 'max_snow_coverage', 'type': 'number', 'minimum': 0, 'maximum': 100, 'default': 100}, {'name': 'max_incidence_angle', 'type': 'number', 'minimum': 0, 'maximum': 90, 'default': 90}]
```

Setting the values.
```python
>>> pleiades_queryables.set('processing_level', 'SENSOR')
>>> pleiades_queryables.set('max_snow_coverage', 0)
>>> pleiades_queryables.generate_cql_filter()
{'op': 'and', 'args': [{'op': '=', 'args': [{'property': 'processing_level'}, 'SENSOR']}, {'op': '=', 'args': [{'property': 'max_snow_coverage'}, 0]}]}
```

Searching the products:
```python
>>> connection.search_items(collection_id="PLEIADES", bbox=(1,2,3,4), filter=pleiades_queryables.generate_cql_filter())
{'type': 'FeatureCollection', 'features': [{'id': 'c8a1f88d-89cf-4933-9118-45e9c1a5df20','type': 'Feature', 'stac_version': '1.0.0', "stac_extensions": ["https://stac-extensions.github.io/projection/v1.0.0/schema.json", "https://stac-extensions.github.io/eo/v1.0.0/schema.json", "https://stac-extensions.github.io/view/v1.0.0/schema.json", "https://stac-extensions.github.io/processing/v1.1.0/schema.json"], 'geometry': {'type': 'Polygon', 'coordinates': [[[12.36555287044679, 41.94403289260048]], [12.36571746774068, 41.86399361096971], [12.60746759743069, 41.86372776276345], [12.60758647471871, 41.94379931812686], [12.36555287044679, 41.94403289260048]]}, 'properties': {'constellation': 'PHR', 'datetime': '2022-03-21T10:11:15.055Z', 'view:azimuth': 179.9852862071639, 'eo:cloud_cover': 0, 'proj:centroid': {'lat': 41.903935647240964, 'lon': 12.486569672582828}, 'processing:level': 'SENSOR', 'sensorType': 'OPTICAL', 'spectralRange': 'VISIBLE'}, 'assets': {}, 'links': []}, ...], 'links': []}
```

Create and confirm and order:
```python
>>> order = connection.create_order(collection_id="PLEIADES", products=["c8a1f88d-89cf-4933-9118-45e9c1a5df20"])
>>> order.costs
42
>>> order.status
'orderable'
>>> order.confirm_order()
>>> order.status
'ordered'
```

When the order has finished, you can process the data as with a normal collection.

```python
>>> order = connection.get_order(id="40264b5-c3ae-46f4-a907-0f612d763d97")
>>> order.status
'succeeded'
>>> pleiades_cube = connection.load_collection(order.target_collection_id)
```