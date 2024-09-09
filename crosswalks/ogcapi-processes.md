# Crosswalk between openEO API and OGC API - Processes

This document gives a brief overview over similarities and differences between
- **openEO API, v1.2.0**
- **OGC API - Processes - Part 1: Core, v1.0.0**

In the following I use **OAP1** as an abbreviation for **OGC API - Processes - Part 1**.

## Introduction (tl;dr)

OCG API - Processes defines just processing, while the openEO API has a much broader scope.
openEO covers many parts that other OGC API specifications define, some are aligned some are not.

Conceptually the APIs are similar, but have some conflicts that can't be resolved easily
(e.g. process description with multiple outputs in OAP1, job listing with different job status values).

A key differentiator between OAP1 and openEO is that process chaining is a fundamental concept in openEO
to build your own workflows while OAP1 is more meant to run larger "black box" workflows. You can add
workflows with Part 3 of OGC API - Processes.

Another key differentiator is that openEO has a list of 
[pre-defined but extensible processes](https://processes.openeo.org) available
while OGC API - Processes doesn't predefine processes.

As such the target audience of OAP1 and openEO is probably only partially overlapping.

The openEO API covers the following "categories" of endpoints:

- [API discovery](#api-discovery) - partially covered by OGC API - Processes - Part 1
- [Authentication](#authentication) - not defined by OGC
- [Data Discovery](#data-discovery) - covered by various other OGC APIs (Coverages, EDR, Features, Records, ...)
- [Process Discovery](#process-discovery) - covered by OGC API - Processes - Part 1
  - [Pre-defined processes](#pre-defined-processes) - covered by OGC API - Processes - Part 1
  - [User-defined processes / Workflows](#user-defined-processes-/-workflows)  - covered by OGC API - Processes - Part 2 and 3
- [Data Processing](#data-processing) - covered by OGC API - Processes - Part 1 and 3
  - [Synchronous processing](#synchronous-processing) - covered by OGC API - Processes - Part 1
  - [Batch Job processing](#batch-job-processing) - covered by OGC API - Processes - Part 1
  - [On-demand processing](#on-demand-processing) - covered by other OGC APIs (Maps, Tiles, ...)
- [File Storage](#file-storage) - not covered by OGC APIs

## General API mechanics

Both APIs use HTTP as the basis and encourage HTTPS.
HTTP 1.1 is required for OAP1, while openEO doesn't specify a specific HTTP version.
The APIs follow REST principles and make use of HTTP content negotiation.
The APIs make broad use of "Web Linking" (compatible between OAP1 and openEO).
Both specifications recommend the implementation of CORS.

The default encoding for requests and response bodies is JSON. OGC API recommends to also support
HTML as an response body encoding. openEO uses client software to render HTML output from JSON.

Both specifications make broad use of OpenAPI 3.0 and JSON Schema for specification purposes.

Many API endpoints in OAP1 and openEO support pagination through links with the relation types `next`
and `prev`. These endpoints have a `limit` parameter to enable pagination for a specific page size.
**Note:** Pagination is rarely used in openEO implementations and most clients don't support it consistently.

## API discovery

Discovering the API, connecting to it and reading the capabilities is always the first step clients
need to execute.

### Well-known document

- openEO: `GET /.well-known/openeo`
- OAP1: n/a

openEO clients usually connect to the well-known document first to discover different versions or 
implementations of a server. Thus a client can choose a suitable API versions inclusing choosing
between production and development instances. Then the openEO client connects to the selected
instance's [landing page](#landing-page), which OGC API - Processes clients always directly connect
to. openEO clients can usually also directly connect to the landing page though.

This folder structure with the document resides usually outside of the actual API implementations,
i.e. in the root of the host or domain.

### Landing page

- openEO: `GET /` (required)
- OAP1: `GET /` (required)

As the landing pages both are based on top of OGC API - Common, they are very similar.

Some differences include:
- openEO requires the following additional fields:
  - Defined in OAP1, but not required: `title`, `description`
  - Not defined in OAP1: `api_version`, `backend_version`, `stac_version`, `id`, `endpoints`, (`type`)
- The relation type to link to the conformance classes is `conformance` in openEO (originating from
  OGC API - Features / STAC API) and `http://www.opengis.net/def/rel/ogc/1.0/conformance` in OAP1.
  Two links with the same target but different relation types will be required.
- The existance of API endpoints in openEO is primarily checked through `endpoints`, which is
  not present in OAP1. OAP1 uses links, which openEO primarily uses for non-API-related links.
  Nevertheless, links such as required in OAP1 can be added easily to an openEO implementation.
  The following additionl links are relevant for OAP1:
  - One of the link relations `service-desc` or `service-doc` is required in OAP1. They should link
    to an API description (e.g. OpenAPI or rendered HTML version).
  - A link with relation type `http://www.opengis.net/def/rel/ogc/1.0/processes` to `/processes` is 
    required for OAP1, but not in openEO.
  - A link with relation type `http://www.opengis.net/def/rel/ogc/1.0/job-list` to `/jobs` can be
    added in OAP1, but is not present in openEO.

### Conformance classes

- openEO: `GET /conformance` (optional)
- OAP1: `GET /conformance` (required)

Both endpoints are 100% equivalent.
OAP1 requires a separate endpoint that lists conformance classes. 
openEO additionally allows to list the conformance classes in the landing page (follows STAC API).
Conformance classes are only fully defined since openEO API v1.2.0.

## Authentication

- openEO: `GET /credentials/basic` and/or `GET /credentials/oidc`
- OAP1: n/a

OpenEO defines two authentication mechanisms:
- OpenID Connect (primary)
- HTTP Basic (secondary, primarily for development/testing purposes)

OAP1 doesn't define any authentication machanisms, but both authentication mechanisms can also be
implemented for OAP1. The main issue will be that OAP1 clients will likely not support them.

The availability of the authentication mechanisms is detected through the `endpoints` in the 
[landing page](#landing-page) in openEO, while in OAP1 you need to parse the OpenAPI document for it
(which implicitly requires a link to an OpenAPI 3.0 file with relation type `service-desc` in the
landing page).

## Data Discovery

Data Discovery is not covered by OAP1, but it can be "plugged in" through various other OGC APIs
(e.g. Coverages, EDR, Features, Records, ...). Except for OGC API - Processes - Part 3, it is not
clear how the processes defined in OAP1 can access resources from the other APIs. The processes 
probably need to implement data access individually through OGC API clients. As such, OAP1 could
also be made compliant with STAC API - Collection and STAC API - Features. STAC API - Collections
is required by openEO, STAC API - Features is optional in openEO, but would likely be required to
allow data access through OAP1 processes.

## Process Discovery

The OAP1 specification claims that it 
> does not mandate the use of any specific process description to specify the interface of a
process.

It defines a "default" encoding in the conformance class "OGC Process Description" though.
Unfortunately, this is [a somewhat miselading statement](https://github.com/opengeospatial/ogcapi-processes/issues/325)
and OAP1 still provides a predefined set of fields which conflict with openEO (see below).

The openEO API specifies a single encoding for process descriptions.

An important difference is that in OAP1 you just execute one process
(you can optionally chain them using OGC API - Processes - Part 3).
This means a process in OAP1 is often more complex.
In openEO a process is often very fine-granular (e.g. addition of two numbers)
and you usually chain multiple of them to a more complex process (graph).
The process chaining into a full graph is fundamental in openEO.

Another major difference is that in openEO there are
[pre-defined process descriptions available for common use cases](https://processes.openeo.org).
OGC API - Processes doesn't provide pre-defined process descriptions.
In theory, you could re-use the openEO processes in OGC API - Processes
if OGC API - Processes - Part 3 is implemented for chaining.

### Pre-defined processes

- openEO: `GET /processes` (required)
- OAP1: `GET /processes`, `GET /processes/{processID}` (both required)

In openEO `GET /processes` returns the full process metadata, while in OAP1 it only returns a summary.
The general structure of the response of `GET /processes` is the same (`processes` and `links`).
The OGC Process Description and the openEO process description are not compatible though.

openEO doesn't define an endpoint yet to retrieve an indivdual process such as
`GET /processes/{processID}` in OAP1.
There is a [proposal](https://github.com/Open-EO/openeo-api/pull/348) available to add such an endpoint.
openEO has the concept of namespace for processes though and thus defines the endpoint at   
`GET /processes/{namespace}/{process}` which would conflict with OAP1.

Some notable differences in the process description (only fully delivered via `GET /processes/{processID}`):
- OAP1 defines `jobControlOptions`, which is
  [undefined in openEO](https://github.com/Open-EO/openeo-api/issues/429) yet
  (which implies `["sync-execute","async-execute"]`).
- OAP1 defines `outputTransmission`, which is not available in openEO.
  It seems though [this will be removed](https://github.com/opengeospatial/ogcapi-processes/issues/326).
- OAP1 allows multiple outputs, openEO only allows a single output
  (potential workaround: wrap in an array or object)
- OAP1 uses `title` and openEO uses `summary`
- OAP1 specifies `inputs` as object and the identifier as key,
  openEO specifies `parameters` as array and the identifier as `name` property
  (but the content of each of them is otherwise very similar).

Below is a simple process encoded in the two variants discussed here:
- [OGC Process Description](oap-echo-example.json)
- [openEO Process](openeo-echo-example.json)

### User-defined processes / Workflows

Workflows are not described in OGC API - Processes - Part 1. Instead Part 2 defines the deployment/management of workflows and Part 3 defines how to define the workflows. Part 2 defines how to chain/nest processes in OGC API - Processes and also defines their own "workflow language" ("Modular OGC API Workflow JSON", short: MOAW), but it seems to also allow providing other workflow languages such as openEO user-defined processes and CWL.

openEO defines the `/process_graphs` endpoints and has workflows (called "user-defined processes" in openEO, i.e. a processes with a process graph) included in the core.

Related documents:

- MOAW: https://github.com/opengeospatial/ogcapi-processes/blob/master/extensions/workflows/sections/clause_6_overview.adoc (and following chapters)
- openEO: https://github.com/opengeospatial/ogcapi-processes/blob/master/extensions/workflows/sections/clause_13_openeo_workflows.adoc
- CWL: https://github.com/opengeospatial/ogcapi-processes/blob/master/extensions/workflows/sections/clause_12_cwl_workflows.adoc

A comparison between MOAW and openEO user-defined processes is **TBD**.

## Data Processing

### Synchronous processing

- openEO: `POST /result`
- OAP1: `POST /processes/{processID}/execution`

  TBD

### Batch Job processing

#### Job list

- openEO: `GET /jobs`
- OAP1: `GET /jobs`

The job list in OAP1 has several parameters, which are not present in openEO.
The general structure of the response of `GET /jobs` is the same (`jobs` and `links`).
Each job complies to the structure discussed in [Job status](#job-status).

#### Job status

- openEO: `GET /jobs/{jobID}`
- OAP1: `GET /jobs/{jobID}`

Similar properties in OAP1 and openEO:
- `jobID` (required) / `id` (required) -> OAP1 changes to `id`
- `processID` (string) / `process` (required, object containing chained processes) -> openEO doesn't require it
- `status` (required, below: OAP1 | openEO) -> OAP1 switches to openEO status codes
  - *n/a* | created
  - accepted | queued
  - running | running
  - successful | finished
  - failed | error
  - dismissed | canceled
- `created` (required in openEO only) -> OAP1 to require `created`
- `updated`
- `progress`
- `links` ([to be added to openEO](https://github.com/Open-EO/openeo-api/issues/495))

Additional properties in OAP1:
- `type` (required) (always: `process`) -> openEO to add `type: "openeo"` (potentially not required with default value `openeo`)
- `messsage` (-> use logs in openEO)
- `started` (-> use logs in openEO)
- `finished` (-> use logs in openEO)

Additional properties in openEO:
- `title`
- `description`
- `costs`
- `budget`
- `usage`

#### Creating a job

- openEO: `POST /jobs`
- OAP1: `POST /processes/{processID}/execution`

In OAP1 you may provide inputs, outputs, the response type (raw or document) and/or a subscriber.

In openEO you must provide a process (chained processes as process graph with optional additional metadata)
and you may additionally provide a title, a description, a billing plan and/or a maximum budget.

Both specifications seem to allow providing additional properties.

#### Queueing a job

- openEO: `POST /jobs/{jobID}/results`
- OAP1: n/a (queued directly after creation)

#### Cancel / Delete a job

- openEO: `DELETE /jobs/{jobID}/results` / `DELETE /jobs/{jobID}`
- OAP1: *n/a* / `DELETE /jobs/{jobID}`

#### Result Access

- openEO: `GET /jobs/{jobID}/results`
- OAP1: `GET /jobs/{jobID}/results`

In openEO result access does fully rely on STAC. The response is a valid STAC Item or Collection.

In OAP1 the result access [differs depending on the given parameters](https://docs.ogc.org/is/18-062r2/18-062r2.html#toc34).

### On-demand processing

*On-demand processing in this context means that processing is only executed for extents shown to*
*the user, e.g. on a web map. Results are processed "on demand" depending on the interaction with*
*the map (e.g. how Google Earth Engine does it in their Code Editor by default).*

  TBD, lower priority as it's not covered by OAP1. It's also optional and very different in openEO.
  Instead it is defined as a separate OAP1 API implementation for individual OGC API resources.
  For example, a combination of OGC API - Maps and OGC API - Processes.

## File Storage

- openEO: `/files` (various methods),  `/files/{path}` (various methods)
- OAP1: n/a

As it is neither available in OAP1 nor in any of the OGC APIs, we don't make any comparisons here.
