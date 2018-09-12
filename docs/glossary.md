# Glossary

This glossary introduces the major technical terms used in the openEO project.

## General Terms

- **API**: application programming interface ([wikipedia](https://en.wikipedia.org/wiki/Application_programming_interface)); a communication protocol between client and back-end
- **client**: software environment (software) that end-users directly interact with, e.g. R (rstudio), Python (jupyter notebook), and JavaScript (web browser); R and Python are two major data science platforms; JavaScript is a major language for web development
- **(cloud) back-end**: server; computer infrastructure (one or more physical computers or virtual machines) used for storing EO data and processing it
- **big Earth observation cloud back-end**: server infrastructure where industry and researchers analyse large amounts of EO data
- **User defined functions (UDFs)**: concept, that enables the users to upload custom code and have it executed e.g. for every pixel of a scene, allowing custom calculations on server-side data. See the section on [UDFs](udfs.md) for more information.

## EO data

In our domain, different terms are used to describe EO data(sets). Within openEO, a **granule** typically refers to a limited area and a single overpass leading to a very short observation period (seconds) or a temporal aggregation of such data (e.g. for 16-day MODIS composites) while a **collection** is an aggregation of granules sharing the same product specification. It typically corresponds to the series of products derived from data acquired by a sensor on board a satellite and having the same mode of operation.

The [CEOS OpenSearch Best Practice Document v1.2](http://ceos.org/ourwork/workinggroups/wgiss/access/opensearch/) lists synonyms used (by organizations) for:

- **granule**: dataset (ISO 19115), dataset (ESA), granule (NASA), product (ESA, CNES), scene (JAXA)
- **collection**: dataset series (ISO 19115), collection (CNES, NASA), dataset (JAXA), dataset series (ESA), product (JAXA)

## Processes, Process Graphs and Jobs

The terms _process_ and _process graph_ have specific meanings in the openEO API specification.

A **process** is the description of an operation as provided by the back end (e.g. computing statistical operation, such as mean or median, on selected EO data), similar to a function definition in programming languages. 

A **process graph** chains specific process calls. Similarly to scripts in the context of programming, process graphs organize and automate the execution of one or more processes that could alternatively be executed individually. In a process graph, processes need to be specific, i.e. concrete values for input parameters need to be specified. These arguments can again be process graphs, scalar values, arrays or objects.

## Aggregation and resampling

***Aggregation*** computes new values from sets of values that are _uniquely_ assigned to groups. It involves a grouping predicate (e.g. monthly, 100 m x 100 m grid cells), and an aggregation function (e.g., `mean`) that computes one or more new values from the original ones.

Examples:

- a time series aggregation may return a regression slope and intercept for every pixel time series, for a single band (grouping predicate: full time extent)
- a time series may be aggregated to monthly values by computing the mean for all values in a month (grouping predicate: months)
- _spatial_ aggregation involves computing e.g. _mean_ pixel values on a 100 x 100 m grid, from 10 m x 10 m pixels, where each original pixel is assigned uniquely to a larger pixel (grouping predicate: 100 m x 100 m grid cells)

Note that for the first example, the aggregation function not only requires time series values, but also their time stamps.

***Resampling*** (also called _scaling_) is a broader term where we have data at one resolution, and need values at another. In case we have values at a 100 m x 100 m grid and need values at a 10 m x 10 m grid, the original values will be reused many times, and may be simply assigned to the nearest high resolution grid cells (nearest neighbor method), or may be interpolated using various methods (e.g. by bilinear interpolation). Resampling from finer to coarser grid may again be a special case of aggregation.

When the target grid or time series has a lower resolution (larger grid cells) or lower frequency (longer time intervals) than the source grid, aggregation might be used for resampling. For example, if the resolutions are similar, (e.g. the source collection provides 10 day intervals and the target needs values for 16 day intervals), then some form of interpolation may be more appropriate than aggregation as defined here.
