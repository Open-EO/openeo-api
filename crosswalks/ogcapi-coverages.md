# Crosswalk between openEO API and OGC API - Coverages

This document gives a brief overview over similarities and differences between
- [**openEO API, v1.2.0**](https://api.openeo.org/1.2.0/)
- [**OGC API - Coverages - Part 1: Core, v0.0.6**](https://docs.ogc.org/DRAFTS/19-087.html)


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

## Abbreviations

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
position within its spatial, temporal or spatiotemporal **domain**;
this can be equivalent to either a [STAC Item](https://github.com/radiantearth/stac-spec/tree/master/item-spec)
or [Collection](https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md).

**`domain`** 
A set of direct positions along some *axis* in space and time (or other dimensions) that define the
"location" of a coverage, associated with a (compounding of) spatio(-temporal)(-other) coordinates
reference system, and for each of which a set of 1+ values (**range**) are associated.

**`feature`**
An abstraction of real world phenomena.

**`range`**
Set of **feature** attribute values associated by a function with the elements of the **domain** of a 
coverage, that means the stored values of a coverage like for instance the spectral bands;
In the STAC [`datacube`](https://github.com/stac-extensions/datacube) extension, **range** and **domain**
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

*Executive summary (tl;dr)* : ...


### Meta / API capabilities

In this section we go through the available information on the API capabilities,
very relevant for interoperability and "machine-actionable" services.

#### Well-known URIs

- openEO: [`GET /.well-known/openeo`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/connect) (optional)

- OAC1: `n/a`

Site-wide metadata information, in **openEO** this is a list of versions of the API that the server supports,
and it is meant to help a client choose the most suitable endpoint (eg. production/develpment).

Not available in **OAC1**.


#### Landing page

- openEO: [`GET /`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/capabilities) (required)

- OAC1: `GET /` (required)

Both landing pages stem from the [OGC API - Common](https://ogcapi.ogc.org/common/) standard,
and they only have minor differences in the returned schemas.

#### Conformance

- openEO: [`GET /conformance`](https://api.openeo.org/1.2.0/#tag/Capabilities/operation/conformance) (optional) (only from v1.2.0)

- OAC1: `GET /conformance` (required)

Both endpoints are 100% equivalent (**openEO** additionally allows to list the conformance classes in the landing page,
following the STAC API).


#### API description

- openEO: `n/a` (?)

- OAC1: `GET /api` (required)

In **OAC1** this is contains the description of the API (eg. OpenAPI), and optionally some 
documentation (eg. HTML).

In **openEO** this is missing.


### (Meta)data retrieval

...


### Domain subsetting

...

### Range subsetting

...


### Scaling

...

### Tiles

...


## References

- **openEO API, v1.2.0** &mdash; https://api.openeo.org/1.2.0/

- **OGC API - Coverages - Part 1: Core, v0.0.6** &mdash; https://docs.ogc.org/DRAFTS/19-087.html

- **OGC Abstract Specification Topic 6** - *Schema for coverage geometry and functions* &mdash; https://portal.ogc.org/files/?artifact_id=19820

- **OGC Web Coverage Service (WCS) 2.1 Interface Standard** &mdash; http://docs.opengeospatial.org/is/17-089r1/17-089r1.html
interface standard (v2.1).
