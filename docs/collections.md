# Data Discovery (Collections)

openEO strives for compatibility with [STAC 0.6](https://github.com/radiantearth/stac-spec) and [OGC WFS 3.0](https://github.com/opengeospatial/WFS_FES) as far as possible. 
Implementing the data discovery endpoints of openEO should also produce valid STAC and WFS 3.0 documents, including partial compatibility with their APIs.

!!! warning
	STAC and OGC WFS 3.0, as well as openEO, are still under development. Therefore, it is likely that further changes and adjustments will be made in the future.

## Extensions

STAC has several extensions (see their [repository](https://github.com/radiantearth/stac-spec)) that can be used to better describe your data. Clients and server are not required to implement all of them, so be aware that some clients may not be able to read all your meta data.

Some commonly used extensions are:
* EO extension (mostly integrated within openEO)
* Scientific extension
* Dimensions extension

## Links

For data discovery in general and each collection you can specify a set of references. These can be alternate representations, e.g. data discovery via OGC WCS or OGC CSW, references to a license, references to actual raw data for downloading, detailed information about pre-processing, etc.

!!! note
	STAC requires to add a link with relation type `self` (see below). Although this is not technically necessary for openEO and we do not enforce you to provide such a link, we recommend to provide it anyway.

### Common link relation types

The following types are commonly used as `rel` types in the links:

| Type              | Description                                                  | Scope                          |
| ----------------- | ------------------------------------------------------------ | ------------------------------ |
| `self`            | Absolute URL to the the data discovery endpoint or the collection itself. | Data Discovery and Collections |
| `root` / `parent` | URL to the data discovery endpoint.                          | Collections                    |
| `child`           | URL to a child STAC Catalog or STAC Dataset.                 | Collections                    |
| `item`            | URL to a STAC Item.                                          | Collections                    |
| `license`         | The license URL for the dataset SHOULD be specified if the `license` field is set to `proprietary`. If there is no public license URL available, it is RECOMMENDED to supplement the STAC catalog with the license text in separate file and link to this file. | Collections                    |
| `alternate`       | An alternative representation of the metadata. This could be a web service such as OGC WCS or OGC CSW or a metadata document following another standard such as ISO 19115, INSPIRE or DCAT. | Data Discovery and Collections |
| `about`           | A resource that is related or further explains the entity, e.g. a user guide. | Data Discovery and Collections |
| `derived_from`    | Allows referencing the data this collection was derived from. | Collections                    |
| `cite-as`         | A [DOI](https://www.doi.org/) link for citation purposes (see STAC Scientific Extension). | Collections                    |

More relation types may be listed in the STAC documentation.