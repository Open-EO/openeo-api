# Crosswalk between openEO API and OGC API - Coverages

This document gives a brief overview over similarities and differences between
- [**openEO API, v1.2.0**](https://api.openeo.org/1.2.0/)
- [**OGC API - Coverages - Part 1: Core, v0.0.6**](https://docs.ogc.org/DRAFTS/19-087.html)

----

**TABLE OF CONTENTS**

[TOC]

## Introduction

This *OGC API - Coverages* draft specification establishes how to access coverages as defined by the
[OGC Abstract Specification Topic 6](https://portal.ogc.org/files/?artifact_id=19820) / 
[ISO 19123](https://www.iso.org/standard/40121.html) *Schema for coverage geometry and functions*,
and it thus represents an alternative to the established OGC
[Web Coverage Service (WCS)](http://docs.opengeospatial.org/is/17-089r1/17-089r1.html) 
interface standard (v2.1).

The strategy behind the development of the *OGC API - Coverages* specification is to 
develop a minimal, relatively simple API standard first, with new capabilities being incrementally
added based on the community demands. Also, while defining how to access (portions of)
coverages from a catalog, the standard does not specify the encoding of the coverage
itself given in response, not limiting it to "internal" OGC encodings like the 
[CIS 1.1](http://www.opengis.net/doc/IS/cis/1.1.1), or 
[CF-netCDF](https://www.ogc.org/standard/netcdf/)), but also to e.g.
[CoverageJSON](https://covjson.org/), [COPC](https://copc.io/), etc.

This crosswalk will proceed by comparing such standard with the openEO API, touching
all the functionalities that are declared in the OGC standard, i.e.:

- (meta)data retrieval
- subsetting through dimension(s)
- range (bands) subsetting
- up/down-scaling
- data retrieval as tiles

NOTE: the following abbreviations will be used throughout the document:

- **openEO** : *openEO API, v1.2.0*
- **OAC1** : *OGC API - Coverages - Part 1*

## Nomenclature

Despite stemming from the [OGC API - Features](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html) standards,
openEO/STAC and OGC have both a different terminology and data models, so here
we put the definitions of the most relevant terms of both "worlds".

Most notably, an OGC [*coverage*](http://myogc.org/go/coveragesDWG) &mdash;
even though formally defined as a *feature*
(and not a *collection* thereof) &mdash; is frequently an abstraction for a 
*collection* of (generally, but not limited to, gridded) datasets/items
(like time-series of satellite images for instance),
so we can generally compare it with STAC [collections](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md),
especially [datacubes](https://openeo.org/documentation/1.0/datacubes.html).

### OGC

**`collection`**
A set of **features** from a dataset.

**`coverage`**
A **feature** that acts as a function to return values from its **range** for any direct
position within its spatial, temporal or spatio-temporal **domain**;
this can be equivalent to either a [STAC Item](https://github.com/radiantearth/stac-spec/tree/master/item-spec)
or [Collection](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md).

**`domain`** 
A set of direct positions along some *axis* in space and time (or other dimensions) that define the
"location" of a coverage, associated with a (compounding of) spatio(-temporal)(-other) coordinates
reference system (CRS), and for each of which a set of 1+ values (**range**) are associated.

**`feature`**
An abstraction of real world phenomena.

**`range`**
Set of **feature** attribute values associated by a function with the elements of the **domain** of a 
coverage, that means the stored values of a coverage like for instance the spectral bands;
in the STAC [`datacube`](https://github.com/stac-extensions/datacube) extension, **range** and **domain**
are condensed into the same **cube:dimensions** container.

### STAC

**`catalog`**
A logical group of other **catalog**, **collection**, and **item** objects.

**`collection`**
A set of common fields to describe a group of **items** that share properties and metadata

**`item`**
A GeoJSON Feature augmented with foreign members relevant to a STAC object.

**`cube:dimensions`**
A set of dimensions that can be of different types: spatial, temporal, "other", etc.


## Crosswalk

*Executive summary (tl;dr)*

The capabilities of **openEO** and **OAC1** largely overlap,
though, as also declared in the standard draft's preface, **OAC1** is a simpler
service, with limited functionality in its core specification
(eg. no authentication/authorization management, processes,
batch jobs, logs, processing budgets, etc).

**OAC1** usually provide simpler ways to request basic operations on 
datasets (like filtering or resampling), by using the query parameters of
the URLs. **openEO** on the other hand allows for a much powerful service
with processing graphs and asynchronous jobs management, at the cost of a
slightly more laborious way to execute the most basic "processing" operations.

The data model of the "coverage" is generally a bit more flexible with regards
to the "arbitrary" non-spatial non-temporal dimensions, while the processes
in **openEO** generally do not include such dimensions.

The only **OAC1** capability that **openEO** does not directly provide (if not
via cascade with a secondary tiles service) is to attach tilesets to coverages, and hence
enable tiled access to the data.


### Meta / API capabilities

In this section we go through the available information on the API capabilities,
very relevant for interoperability and "machine-actionable" services.

### Well-known URIs

- openEO: [`GET /.well-known/openeo`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/connect) (optional)

- OAC1: `n/a`

Site-wide metadata information, in **openEO** this is a list of versions of the API that the server supports,
and it is meant to help a client choose the most suitable endpoint (eg. production/development).

Not available in **OAC1**.


### Landing page

- openEO: [`GET /`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/capabilities) (required)

- OAC1: `GET /` (required)

Both landing pages stem from the [OGC API - Common](https://ogcapi.ogc.org/common/) standard,
and they only have minor differences in the returned schemas.

### Conformance

- openEO: [`GET /conformance`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/conformance) (optional) (only from v1.2.0)

- OAC1: `GET /conformance` (required)

Both endpoints are 100% equivalent (**openEO** additionally allows to list the conformance classes in the landing page,
following the STAC API).


### API description

- openEO: `n/a` (?)

- OAC1: `GET /api` (required)

In **OAC1** this contains the description of the API (eg. OpenAPI), and optionally some 
documentation (eg. HTML).

In **openEO** this is missing.


### Authentication

- openEO: [`GET /credentials/basic`](https://api.openeo.org/1.2.0/#section/Authentication) 
   and/or [`GET /credentials/oidc`](https://api.openeo.org/1.2.0/#section/Authentication)

- OAP1: `n/a`

**openEO** defines two authentication mechanisms:  
[OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect) (primary)
and HTTP Basic (for development/testing). **OAC1** does not define any authentication mechanisms,
and while both mechanisms could be implemented, **OAC1** clients will likely not support them.

The availability of the authentication mechanisms is detected through the endpoints in the
[landing page](#landing-page) in **openEO**, while in **OAC1** you need to parse the 
OpenAPI document for it (which implicitly requires a link to an OpenAPI 3.0 file with 
relation type `service-desc` in the landing page).


### Data discovery

- openEO:
  - [`GET /collections`](https://api.openeo.org/1.2.0/#tag/EO-Data-Discovery/operation/list-collections) (required)
  - [`GET/POST /search`](https://api.openeo.org/1.2.0/#tag/EO-Data-Discovery/STAC) (optional)

- OAC1:
  - `GET /collections` (required)

**openEO** and **OAC1** both provide a resource for accessing the 
whole catalog of datacubes/coverages offered by the server,
with basic/abbreviated metadata for each of the assets in order
to try to keep the response size small.
Full metadata details are instead available as per [data description](#data-description).

CIS coverages will be returned by **OAC1**, STAC Collections by **openEO**.

Optionally, **openEO** allows for searching for individual STAC items "hidden"
inside the collections, as per [STAC API repository](https://github.com/radiantearth/stac-spec/tree/v0.9.0/api-spec).


### Data description

- openEO:
  - [`GET /collections/{collectionId}`](https://api.openeo.org/1.2.0/#tag/EO-Data-Discovery/operation/describe-collection) (required)
  - [`GET /collections/{collectionId}/queryables`](https://api.openeo.org/1.2.0/#tag/EO-Data-Discovery/operation/list-collection-queryables) (required?)

- OAC1:
  - `GET /collections/{collectionId}` (required)
  - `GET /collections/{collectionId}/coverage/rangetype` (required)
  - `GET /collections/{collectionId}/coverage/domainset` (required)
  - `GET /collections/{collectionId}/coverage/metadata` (optional)

Full metadata descriptions of collections are available in both **openEO** and **OAC1**,
encoded as STAC Collections or CIS Coverages, respectively.

Additional links are provided (required) for coverages in **OAC1** with respect to the
basic "Collection Resources" defined in the OGC API - Common: one for
the description of the sole "range" of the coverage, and one for
the sole "domain", which are anyway just a subset of the full
metadata description. Also available, tough optional, is the
link to the sole coverage's "metadata", meaning supplementary/domain-specific
extra metadata fields that might be attached to a coverage.

**openEO** offers a more flexible and machine-actionable solution for
filtering the description of a collection, by means of the "queryables":
a listing of all metadata filters available for each collection.
This is in line with both [`filter`](https://github.com/stac-api-extensions/filter#queryables) STAC API extension
and [OGC API - Features - Part 3: Filtering](https://github.com/opengeospatial/ogcapi-features/tree/master/extensions/filtering).


### Data access

- openEO:
  - [`POST /result`](https://api.openeo.org/1.2.0/#tag/Data-Processing/operation/compute-result) @
[`load_collection`](https://processes.openeo.org/#load_collection) process (sync)
  -  [`POST /jobs`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/create-job) @
[`load_collection`](https://processes.openeo.org/#load_collection) process +
[`POST /jobs/{jobId}/results`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/start-job) (async)

- OAC1:
  - `GET /collections/{collectionId}/coverage` (required)
  - `GET /collections/{collectionId}/coverage/rangeset` (optional)

**OAC1** : encoding as negotiated in the HTTP protocol, with proper fallback media type
otherwise. The actual coverage values (the range set) can be represented either in-line
or by reference to an external file which may have any suitable encoding.

**openEO** provides access to the actual data by means of the 
[load_collection](https://processes.openeo.org/#load_collection) process, which can
be submitted either synchronously or asynchronously as a batch job.

For pre-filtering / data subsetting options, see next section.


### Data subsetting

- openEO: 
  - [`POST /result`](https://api.openeo.org/1.2.0/#tag/Data-Processing/operation/compute-result) @
[`load_collection`](https://processes.openeo.org/#load_collection) process (sync)
  -  [`POST /jobs`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/create-job) @
[`load_collection`](https://processes.openeo.org/#load_collection) process +
[`POST /jobs/{jobId}/results`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/start-job) (async)

- OAC1:
  - `bbox` / `datetime` / `subset` query params (domain subsetting)
  - `properties` query param (range subsetting)


The parameters offered by the [load_collection](https://processes.openeo.org/#load_collection) **openEO** process
allows for subsetting the requested collection along a cube's dimensions, which
includes also what **OAC1** calls the range set, hence the "bands" of the dataset.
There is no option for lo:hi subsetting of an arbitrary dimension which might
not be classified as neither spatial nor temporal, like the `subset` query
parameter offers in **OAC1**.

Spatial subsetting in **openEO** is more powerful as not only bounding-boxes but
also GeoJSON geometries can be specified for a more accurate clipping of the data.
On the other hand **OAC1** accepts open/unbounded spatial intervals.
Open/unbounded time intervals are supported in both APIs (via `null` or double-dots `..`,
respectively).

Spatial filtering with coordinates specified with an arbitrary CRS is available
in both APIs. In both cases, all data values that spatially *intersect*
with the provided spatial extent/range (boundaries included) will be in the response.

Subsetting of an arbitrary dimension &mdash; not classified as spatial not temporal, nor band
in the openEO datacube model &mdash; is not possible in **openEO**, while available
in **OAC1** via `subset` parameters.

In case the response is too large, **OAC1** plans to consider returning a URI
instead of the content, or a reduced-resolution coverage with a URI to the full resolution response.

Filtering/cherry-picking of bands is available in both **OAC1** and **openEO**, via
`properties` parameter and [load_collection](https://processes.openeo.org/#load_collection)
process respectively. Both band names and band indices can be used in **OAC1**, 
while **openEO** accepts band names exclusively.

An **openEO** server can optionally provide a rough estimate of the time/cost
of a stored job via [`/jobs/{jobId}/estimate`](https://api.openeo.org/1.2.0/#tag/Data-Processing/operation/estimate-job).
Server logs are also available in **openEO** either directly in the synchronous processing
response (as a link), or via the API resources dedicated to the batch jobs
(eg. [`jobs/{jobId}/logs`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/debug-job)).


### Data scaling

- openEO:
  - [`POST /result`](https://api.openeo.org/1.2.0/#tag/Data-Processing/operation/compute-result) @
[`resample_spatial`](https://processes.openeo.org/#resample_spatial) process (sync)
  -  [`POST /jobs`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/create-job) @
[`resample_spatial`](https://processes.openeo.org/#resample_spatial) process +
[`POST /jobs/{jobId}/results`](https://api.openeo.org/1.2.0/#tag/Batch-Jobs/operation/start-job) (async)

- OAC1: 
  - `GET /collections/{collectionId}/coverage?scale-size=axisName({number})[,axisName({number})]*`
  - `GET /collections/{collectionId}/coverage?scale-axes=axisName({number})[,axisName({number})]*`
  - `GET /collections/{collectionId}/coverage?scale-factor={number}`

Rescaling a dataset in **openEO** requires the same procedure as for any other kind
of processing, thus preparing a process graph that executes the desired operation, then
fetch the results, either synchronously or asynchronously through the creation of a
[batch job](https://api.openeo.org/1.2.0/#tag/Data-Processing/operation/create-job).

At the time of writing, the available **openEO** processes for data resampling are
[`resample_spatial`](https://processes.openeo.org/#resample_spatial) &mdash; 
that rescales the spatial dimensions to a target resolution, or to
a target spatial coordinate reference system &mdash; and
[`resample_cube_spatial`](https://processes.openeo.org/#resample_spatial)/
[`resample_cube_temporal`](https://processes.openeo.org/#resample_cube_temporal), that
rescale the spatial/temporal dimensions to match the resolutions of a
provided target datacube.

While **OAC1** does not let a user specify
a resolution, it lets a client specify the target number of samples
along a dimension, or the scaling factor. While the capabilities
of a user-defined process with asynchronous job management
go well beyond data the resampling of a dataset and provide 
a wide range of benefits, **OAC1** provides a somewhat simpler shortcut
for via query parameters of the URL.

**OAC1** also allows for scaling on *any* coverage's dimension, while
**openEO** only along the spatial plane/dimensions.


### Tiles

- openEO: `n/a` (?)

- OAC1:
  - `GET /collections/{collectionId}/coverage/tiles` : list the available tilesets
  - `GET /collections/{collectionId}/coverage/tiles/{tileMatrixSetId}` : tileset description
  - `GET /collections/{collectionId}/coverage/tiles/{tileMatrixSetId}/{tileMatrix}/{tileRow}/{tileCol}` : retrieve tile

**OAC1**, in alignment with the requirements defined in the
[OGC API - Tiles](http://docs.ogc.org/DRAFTS/20-057.html) standard, allows the retrieval of
coverage data in form of tiles, hence trimmed and resampled to match the 
boundaries and resolution of a given tile. More than one tilesets can be attached to a coverage.

**openEO** does not provide tiled access directly, but can be easily cascaded to
a dedicated secondary tile service (like [XYZ tiles](https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames))
thanks to the [`/service_types`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/list-service-types) resource. (?)


### Media encoding

- openEO: [`GET /file_formats`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/list-file-types)

- OAC1: `GET /` (?)

While not exposed as a dedicated API resource, **OAC1** requires a server to provide information about
the supported media types (probably in the landing page).

**OAC1** does not mandate any particular output encoding or format, although CIS JSON is recommended.
Binary formats of course are also alllowed (CIS RDF, NetCDF, GeoTIFF, PNG, JPEG, JPEG-2000, etc.)

**openEO** returns a list of data formats the server supports, with the additional 
information of the data formats the server can also read from (input), and not just 
write to (output). Format names and parameters are aligned with the GDAL/OGR formats although
custom file formats are also permitted.


## References

- **openEO API, v1.2.0** &mdash; https://api.openeo.org/1.2.0/

- **OGC API - Coverages - Part 1: Core, v0.0.6** &mdash; https://docs.ogc.org/DRAFTS/19-087.html

- **OGC API - Common** &mdash; https://ogcapi.ogc.org/common/

- **OGC Abstract Specification Topic 6** - *Schema for coverage geometry and functions* &mdash; https://portal.ogc.org/files/?artifact_id=19820

- **OGC API - Tiles - Part 1: Core Standard 1.0.0** &mdash; https://docs.ogc.org/is/20-057/20-057.html

- **OGC Web Coverage Service (WCS) 2.1 Interface Standard** &mdash; http://docs.opengeospatial.org/is/17-089r1/17-089r1.html

