# Commercial Data Extension

The Commercial Data API extension provides an interface for discovering, ordering and using commercial data in the openEO API. 

- Version: **0.1.0**
- Stability: **experimental**

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

## Overview of the workflow

All the available datasets provided by a backend are listed on the `/collections` endpoint. The collections are normally freely accessible. This extensions adds capabilities for providing collections that are not free of charge and require purchasing data products that can thereupon be used in processing. Commercial data collections usually allow purchasing small subsets of the data (products), for example a single observation of an area.

Therefore, the client must have an ability to search the available products that match their desired criteria and inspect their metadata to decide whether the products should be purchased.

The client can then create an order for the desired products. Because of the financial cost of purchasing the data, a separate endpoint for confirming the execution of that specific order should be implemented.

When the order is completed, the user should be able to access the data using the `collection-id` at the temporal and spatial location of the purchased products.

### Collection discovery

A backend should add general information about a commercial data collection to the `/collections` and `/collections/{collection-id}` endpoints, the same as with freely available collections. Only the metadata about the entire dataset needs to be provided, not about the specific data products that a user has already purchased. 

Commercial data collections are distinguished from freely available collections by including `"order:status": "orderable"` as specified in [STAC Order specification](https://github.com/stac-extensions/order).

Commercial data collections can include `order_parameters` field, if ordering supports additional parameters that specify how the products should be delivered.

Commercial data collections must also include a link to human-readable pricing information for searching and ordering the products. If searching the products is free it should be set to `null`.

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
  "links": [...],
  "cube:dimensions": {...},
  "summaries": {...},
  "assets": {...},
  "order:status": "orderable",
  "order_parameters": [
      {
        "name": "sample_type",
        "description": "sample type of the output raster.",
        "schema": {
          "type": "string"
        },
        "enum": [
          "UINT16",
          "UINT8"
        ]
      },
    ],
  "pricing": {
    "searching": null,
    "ordering": {
      "description": "Minimum area per order is 0.25 km2. The price is calculated based on a 6-months sliding window.",
      "links": [
        {
          "title": "Airbus Pleiades pricing",
          "rel": "related",
          "href": "https://www.sentinel-hub.com/pricing/#TPD_pricing"
        }
      ]
    }
  }
}
```

### Filtering parameters discovery

Searching for products can support refining the search by filtering with general or collection-specific attributes. Backends should implement a top level `/queryables` endpoint for attributes available for all collections, and collection-specific attributes should be provided at `/collections/{collection-id}/queryables` according to [OGC Queryables specification](https://portal.ogc.org/files/96288#filter-queryables).

#### Example

Example response from `GET collections/PLEIADES/queryables`:
```json
{
   "$schema":"http://json-schema.org/draft-07/schema#",
   "$id":"http://example.com/commercial_data/PLEIADES/queryables",
   "type":"object",
   "title":"Queryables of Airbus Pleiades collection.",
   "description":"Available properties for CQL filtering of products.",
   "properties":{
      "processing_level":{
         "title":"Processing level",
         "description":"When searching, you will receive results from the full catalog as well as the Living Library, which holds images that have cloud cover under 30% and Incidence angle under 40°. If you want to search only Living Library results, you will need to filter using processingLevel. This value could be equal to SENSOR (images which meet Living Library criteria) and ALBUM (images that do not meeting Living Library criteria in terms of incidence angle and cloud cover).'",
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

Backends should implement top-level `GET /search` endpoint as specified in [STAC Item Search API specification](https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-rc.1/item-search). This should include the [Filter Extension](https://github.com/radiantearth/stac-api-spec/tree/v1.0.0-rc.1/fragments/filter), which enables filtering the available products by attributes specified in `/queryables` and `collections/{collection-id}/queryables`. 
The endpoint should return a list of  `STAC Item`s that match the criteria.

#### Example

Example request payload to `GET /search` for `PLEIADES` products from "Living Library" with no snow coverage.

```json
{
  "bbox": [
    3,
    15,
    4,
    16
  ],
  "datetime": [
    "01-01-2022",
    "01-02-2022"
  ],
  "collectionsArray": [
    "PLEIADES"
  ],
  "filter": {
    "op": "and",
    "args": [
      {
        "op": "=",
        "args": [
          {
            "property": "processing_level"
          },
          "SENSOR"
        ]
      },
      {
        "op": "=",
        "args": [
          {
            "property": "max_snow_coverage"
          },
          0
        ]
      }
    ]
  }
}
```

### Ordering products

Backends should implement the following endpoints:

- `GET /orders`: Get a list of all created orders
- `POST /orders`: Create an order
- `GET /orders/{order-id}`: Get full metadata of a specific order
- `POST /orders/{order-id}`: Confirm a created order

#### `GET /orders`

Lists all created orders, regardless of the status or the collection. The items should follow the [STAC Order Extension](https://github.com/stac-extensions/order).

```yaml
schema:
  title: All Orders
  type: object
  required:
    - orders
    - links
  properties:
    orders:
      type: array
      items:
        type: object
        title: Order
        description: Information about an order
        required:
          - order:id
          - order:status
          - order:date
          - collection_id
          - costs
        properties:
          order:id:
            type: string
            description: >-
              Unique identifier of the order, which MUST match the specified pattern..
            pattern: '^[\w\-\.~]+$'
          order:status:
            type: string
            description: |-
              The status of the order.
              * `orderable`: The item or asset is orderable via the provider scenario.
              * `ordered`: The item or asset is ordered and the provider is preparing to make it available.
              * `shipping`: The item or asset order are being processed by the provider to provide the user with the asset(s).
              * `delivered`: The provider has delivered the order and asset(s) are available.
              * `unable_to_deliver`: The provider is not able to deliver the order.
              * `canceled`: The order has been canceled.
            enum:
              - orderable
              - ordered
              - shipping
              - delivered
              - unable_to_deliver
              - canceled 
          order:date:
            type: string
            format: date-time
            description: The order time. Formatted as a
              [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) date-time.
          order:expiration_date:
            type: string
            format: date-time
            description: The validity time of the order. Formatted as a
              [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html) date-time.
          collection_id:
            type: string
            description: Unique identifier of the collection.
          costs:
            $ref: 'https://raw.githubusercontent.com/Open-EO/openeo-api/1.0.0/openapi.yaml#/components/schemas/money'
    links:
      $ref: 'https://raw.githubusercontent.com/Open-EO/openeo-api/1.0.0/openapi.yaml#/components/schemas/links_pagination'
```

#### `POST /orders`

Create an order for selected products. Order can contain some additional parameters that specify how the products should be delivered. For example, depending on the collection it might be possible to set the projection, resampling method, bit depth etc of the delivered data.

Backends should expose the available ordering parameters in `/collections/{collection-id}` in the `order_parameters` field, following the `process_parameters` schema of [`GET /service_types`](https://docs.openeo.cloud/api/#tag/Secondary-Services/operation/list-service-types). 

The request should return the `order-id`, current status and the costs of the order.

```yaml
schema:
  title: Create Order Request
  type: object
  required:
    - collection_id
    - products
    - parameters
  properties:
    collection_id:
      type: string
      description: Unique identifier of the collection.
    products:
      type: array
      description: Array of IDs of products to order.
      items:
        $ref: 'https://raw.githubusercontent.com/Open-EO/openeo-api/1.0.0/openapi.yaml#/components/schemas/order_id'
    parameters:
      type: object
      description: Key-value pairs of available `order_parameters` as listed at `GET /commercial_data/collections/{collection_id}` for filtering available products.
      additionalProperties:
        x-additionalPropertiesName: Order Parameter Name
        description: Value of the order parameter to be used in the request.
```

#### `GET /orders/{order-id}`

Get full metadata of the order. The item should follow the [STAC Order Extension](https://github.com/stac-extensions/order), but extended with the spatial and temporal extent information and other metadata about the products.

```json
{
  "order:id": "40264b5-c3ae-46f4-a907-0f612d763d97",
  "order:status": "delivered",
  "order:date": "2017-01-01T09:32:12Z",
  "products": [
    {
      "type": "Feature",
      "stac_version": "0.9.0",
      "id": "c8a1f88d-89cf-4933-9118-45e9c1a5df20",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              12.36555287044679,
              41.94403289260048
            ]
          ],
          [
            12.36571746774068,
            41.86399361096971
          ],
          [
            12.60746759743069,
            41.86372776276345
          ],
          [
            12.60758647471871,
            41.94379931812686
          ],
          [
            12.36555287044679,
            41.94403289260048
          ]
        ]
      },
      "properties": {
        "constellation": "PHR",
        "acquisitionDate": "2022-03-21T10:11:15.055Z",
        "azimuthAngle": 179.9852862071639,
        "cloudCover": 0,
        "geometryCentroid": {
          "lat": 41.903935647240964,
          "lon": 12.486569672582828
        },
        "processingLevel": "SENSOR",
        "sensorType": "OPTICAL",
        "spectralRange": "VISIBLE"
      },
      "assets": {},
      "links": []
    }
  ],
  "parameters": {
    "bounds": [
      3,
      15,
      4,
      16
    ]
  },
  "collection_id": "PLEAIDES",
  "costs": 42
}
```

#### `POST /orders/{order-id}`

When an order is created, the data isn't yet ordered from the commercial data provider. The client should explicitly confirm the order whereupon the order is executed, the costs are deducted from the client's account and the data is ingested in the associated collection. The `order:status` changes to `ordered`.

If the user doesn't have sufficient funds, the endpoint should return an error and `order:status` should not change.

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
{'type': 'FeatureCollection', 'features': [{'id': 'c8a1f88d-89cf-4933-9118-45e9c1a5df20','type': 'Feature', 'stac_version': '0.9.0', 'geometry': {'type': 'Polygon', 'coordinates': [[[12.36555287044679, 41.94403289260048]], [12.36571746774068, 41.86399361096971], [12.60746759743069, 41.86372776276345], [12.60758647471871, 41.94379931812686], [12.36555287044679, 41.94403289260048]]}, 'properties': {'constellation': 'PHR', 'acquisitionDate': '2022-03-21T10:11:15.055Z', 'azimuthAngle': 179.9852862071639, 'cloudCover': 0, 'geometryCentroid': {'lat': 41.903935647240964, 'lon': 12.486569672582828}, 'processingLevel': 'SENSOR', 'sensorType': 'OPTICAL', 'spectralRange': 'VISIBLE'}, 'assets': {}, 'links': []}, ...], 'links': []}
```

Create and confirm and order:
```python
>>> connection.create_order(collection_id="PLEIADES", products=["c8a1f88d-89cf-4933-9118-45e9c1a5df20"])
{'id': '40264b5-c3ae-46f4-a907-0f612d763d97', 'status': 'NOT_CONFIRMED', 'costs': 42}
>>> connection.confirm_order('40264b5-c3ae-46f4-a907-0f612d763d97')
{'id': '40264b5-c3ae-46f4-a907-0f612d763d97', 'status': 'RUNNING'}
```

When the order has finished, you can process the data as with a normal collection.

```python
>>> order = connection.get_order(id="40264b5-c3ae-46f4-a907-0f612d763d97")
>>> order["order:status"]
'delivered'
>>> first_product = order["products"][0]
>>> pleiades_cube = connection.load_collection(
    "PLEIADES",
    spatial_extent=first_product["geometry"],
    temporal_extent = [first_product["acquisitionDate"], None],
    bands=["B1"],
)
```