# Data Discovery (Collections)

openEO strives for compatibility with the specifications [SpatioTemporal Asset Catalog (STAC)](https://stacspec.org/) and [OGC API - Features - Part 1: Core](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html) as far as possible. Implementing the data discovery endpoints of openEO should also produce valid STAC 0.6 and OGC API- Features 1.0 responses, including a partial compatibility with their APIs (see below).

**WARNING**: STAC, as well as openEO, is still under development.
Therefore, it is very likely that further changes and adjustments will be made in the future.

## Extensions

STAC has several [extensions](https://github.com/radiantearth/stac-spec/tree/v0.6.2/extensions) that can be used to better describe your data. Clients and server are not required to implement all of them, so be aware that some clients may not be able to read all your meta data.

Some commonly used extensions that are integrated in the openEO API specification are:

- EO (Electro-Optical) extension
- SAR extension
- Commons extension
- Scientific extension
- Data Cube extension
- Non-Common Properties extension

## Links

For data discovery in general and each collection you can specify a set of references. These can be alternate representations, e.g. data discovery via OGC WCS or OGC CSW, references to a license, references to actual raw data for downloading, detailed information about pre-processing, etc.

**Note**: STAC requires to add a link with relation type `self` (see below). Although this is not technically necessary for openEO and we do not enforce to provide such a link with our validation tools, we still recommend to provide it anyway for compatibility reasons.

### Common link relation types

The following table lists relation types that are commonly used as `rel` types in the links. The scope 'Collections' refers to the links that are related to a specific collection, 'Discovery' refers to links that are related to data discovery in general and are not about a specific collection.

| Type              | Description                                                  | Scope |
| ----------------- | ------------------------------------------------------------ | ----- |
| `self`            | Absolute URL to the data discovery endpoint or the collection itself. | Discovery +Collections |
| `root` / `parent` | URL to the data discovery endpoint.                          | Collections |
| `child`           | URL to a child STAC Catalog or STAC Dataset.                 | Collections |
| `item`            | URL to a STAC Item.                                          | Collections |
| `license`         | The license URL for the dataset SHOULD be specified if the `license` field is set to `proprietary`. If there is no public license URL available, it is RECOMMENDED to supplement the collection with the license text in a separate file and link to this file. | Collections |
| `alternate`       | An alternative representation of the metadata. This could be a secondary web service such as OGC WCS or OGC CSW or a metadata document following another standard such as ISO 19115, INSPIRE or DCAT. | Discovery +Collections |
| `about`           | A resource that is related or further explains the entity, e.g. a user guide. | Discovery +Collections |
| `derived_from`    | Allows referencing the data this collection was derived from. | Collections |
| `cite-as`         | For all DOI names specified, the respective DOI links SHOULD be added to the links section of the catalog with the `rel` type `cite-as`. | Collections |

More relation types may be listed in the STAC documentation.

## Compatibility with *OGC API - Features* and *STAC API*

The data discovery endpoints `GET /collections` and `GET /collections/{name}` are compatible with OGC API - Features and STAC. Both specifications define additional endpoints that need to be implemented to be fully compatible. The additional endpoints can easily be integrated into an openEO API implementation. A rough list of actions for compatibility is available below, but please refer to their specifications to find out the full details.

### OGC API - Features: Part 1: Core compatibility

As of now, OGC API - Features requires more endpoints for full compatibility. You should add the following things to your API:

* Add [additional links](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#core-overview) to the `links` property in the `GET /` response:
    * the API definition (link relations `service-desc` and `service-doc`),
	* the Conformance declaration (path `/conformance`, link relation `conformance`), and
	* the Collections (path `/collections`, link relation `data`).
* Implement `GET /conformance` and specify which conformance classes the service conforms to.
* Implement `GET /collections/{collectionId}/items` and `GET /collections/{collectionId}/items/{featureId}` to support retrieval of individual features.

### STAC compatibility

As of now, STAC has two more required endpoints that need to be implemented:

* `GET /stac`
* `POST /stac/search`

## Provide data for download

If you'd like to provide your data for download in addition to offering the cloud processing service, you can implement the full STAC API. Therefore you can implement the endpoints  `GET /collections/{collectionId}/items` and `GET /collections/{collection-name}/items/{featureId}` to support retrieval of individual items. To benefit from the STAC ecosystem it is also recommended to implement the `GET /stac` endpoint. To allow searching for items you can also implement `POST /stac/search`. Further information can be found in the [STAC API respository](https://github.com/radiantearth/stac-spec/tree/v0.6.2/api-spec) and in the corresponding [OpenAPI specification](https://app.swaggerhub.com/apis/cholmesgeo/STAC_WFS-example/0.6.2).