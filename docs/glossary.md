# Glossary

This glossary introduces, and tries to define, the major technical terms used in the openEO project.

The acronym _openEO_ contracts two concepts:

- **open**: used here in the context of open source software; open source software is available in source code form, and can be freely modified and redistributed; the openEO project will create open source software, reusable under a liberal open source license (Apache 2.0)
- **EO**: Earth observation; openEO targets the processing and analysis of Earth observation data

Further terms:

- **API**: application programming interface ([wikipedia](https://en.wikipedia.org/wiki/Application_programming_interface)); a communication protocol between client and back-end
- **client**: software environment (software) that end-users directly interact with, e.g. R (rstudio), Python (jupyter notebook), and JavaScript (web browser); R and Python are two major data science platforms; JavaScript is a major language for web development
- **(cloud) back-end**: server; computer infrastructure (one or more physical computers or virtual machines) used for storing EO data and processing it
- **big Earth observation cloud back-end** server infrastructure where industry and researchers analyse large amounts of EO data
- **simple** many end-users now use Python or R to analyse data and JavaScript to develop web applications; analysing large amounts of EO imagery should be equally simple, and seamlessly integrate with existing workflows
- **unified** current EO cloud back-ends all have [a different API](http://r-spatial.org/2016/11/29/openeo.html), making EO data analysis hard to validate,difficult to reproduce, and back-ends difficult to compare in terms of capability and costs, or to combine in a joint analysis across back-ends. A unified API can resolve many of these problems.

## Datasets

CEOS ([CEOS OpenSearch Best Practice Document v1.2](http://ceos.org/ourwork/workinggroups/wgiss/access/opensearch/)) defines **Granules** and **Collections** as follows:

> "A ***granule*** is the finest granularity of data that can be independently managed. A granule usually matches the individual file of EO satellite data."

> "A ***collection*** is an aggregation of granules sharing the same product specification. A collection typically corresponds to the series of products derived from data acquired by a sensor on board a satellite and having the same mode of operation."

The same document lists the synonyms used (by organisations) for:

- **granule**: dataset (ISO 19115), dataset (ESA), granule (NASA), product (ESA, CNES), scene (JAXA)
- **collection**: dataset series (ISO 19115), collection (CNES, NASA), dataset (JAXA), dataset series (ESA), product (JAXA)

Here, we will use **granule** and **collection**.

A *granule* will typically refer to a limited area and a single overpass leading to a very short observation period (seconds), or a temporal aggregation of such data as e.g. for 16-day MODIS composites.

The open geospatial consortium published a document on [OGC OpenSearch Geo and Time Extensions](https://portal.opengeospatial.org/files/?artifact_id=56866).

## Processes and Jobs

The terms _process and_ _process graph_ have different meanings in the openEO API specification.

A **process** is simply the description of an operation as provided by the back end, similar to a function definition in programming languages. 

In this context openEO will:

1. consider, or allow to consider, band as a dimension
2. consider imagery (image collections) to consist of one _or more_ collections, as argument to functions; allow filtering on a particular collection, or joining them into a single collection
3. allow filtering on attributes, e.g. on cloud-free pixels, or pixels inside a `MULTIPOLYGON` describing the floodplains of the Danube. This filters on attributes rather than dimensions.
4. Provide generic aggregate operations that aggregate over one or more dimensions. Clients may provide dimension-specific aggregation functions for particular cases (such as `min_time`) 

A **process graph** includes specific process calls, i.e. references to one or more processes including specific values for input arguments similar to a function call in programming. However, process graphs can chain multiple processes. In particular, arguments of processes in general can be again (recursive) process graphs, input datasets, or simple scalar or array values.

### User-defined functions (UDFs)

The abbreviation **UDF** stands for **user-defined function**. With this concept, users are able to upload custom code and have it executed e.g. for every pixel of a scene, allowing custom calculations on server-side data. See the section on [UDFs](udfs.md) for more information.

## Aggregation vs. resampling

***Aggregation*** computes new values from sets of values that are _uniquely_ assigned to groups. It involves a grouping predicate (e.g. monthly, 100 m x 100 m grid cells; think of SQL's `group_by`), and an aggregation function (e.g., `mean`) that computes one or more new values from the original ones.

Examples:

- a time series aggregation may return a regression slope and intercept for every pixel time series, for a single band (group by: full time extent)
- a time series may be aggregated to monthly values by computing the mean for all values in a month (group by: months)
- _spatial_ aggregation involves computing e.g. _mean_ pixel values on a 100 x 100 m grid, from 10 m x 10 m pixels, where each original pixel is assigned uniquely to a larger pixel (group by: 100 m x 100 m grid cells)

Note that for the first example, the aggregation function not only requires time series values, but also their time stamps.

***Resampling*** is a broader term where we have data at one resolution, and need values at another (also called _scaling_). In case we have values at a 100 m x 100 m grid and need values at a 10 m x 10 m grid, the original values will be reused many times, and may be be simply assigned to the nearest high resolution grid cells ("nearest neighbor"), or may be interpolated somehow (e.g. by bilinear interpolation). Resampling from finer to coarser grid by nearest neighbor may again be a special case of aggregation.

When the target grid or time series has a lower resolution (larger grid cells) or lower frequency (longer time intervals) than the source grid, aggregation might be used for resampling. For example, if the resolutions are fairly similar, say the source collection has values for consecutive 10 day intervals and the target needs values for consecutive 16 day intervals, then some form of interpolation may be more appropriate than aggregation as defined here.