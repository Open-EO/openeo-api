# Glossary

This glossary introduces the major technical terms used in the openEO project.

## General terms

- **API**: application programming interface ([wikipedia](https://en.wikipedia.org/wiki/Application_programming_interface)); a communication protocol between client and back-end
- **client**: software environment (software) that end-users directly interact with, e.g. R (rstudio), Python (jupyter notebook), and JavaScript (web browser); R and Python are two major data science platforms; JavaScript is a major language for web development
- **(cloud) back-end**: server; computer infrastructure (one or more physical computers or virtual machines) used for storing EO data and processing it
- **big Earth observation cloud back-end**: server infrastructure where industry and researchers analyse large amounts of EO data
- **User defined functions (UDFs)**: concept, that enables the users to upload custom code and have it executed e.g. for every pixel of a scene, allowing custom calculations on server-side data. See the section on [UDFs](udfs.md) for more information.

## EO data

In our domain, different terms are used to describe EO data(sets). Within openEO, a **granule** typically refers to a limited area and a single overpass leading to a very short observation period (seconds) or a temporal aggregation of such data (e.g. for 16-day MODIS composites) while a **collection** is an aggregation of granules sharing the same product specification. It typically corresponds to the series of products derived from data acquired by a sensor on board a satellite and having the same mode of operation.

The [CEOS OpenSearch Best Practice Document v1.2](http://ceos.org/ourwork/workinggroups/wgiss/access/opensearch/) lists synonyms used (by organizations) for:

- **granule**: dataset (ESA, ISO 19115), granule (NASA), product (ESA, CNES), scene (JAXA)
- **collection**: dataset series (ESA, ISO 19115), collection (CNES, NASA), dataset (JAXA), product (JAXA)

## Processes and process graphs

The terms _process_ and _process graph_ have specific meanings in the openEO API specification.

A **process** is an operation provided by the back end that performs a specific task on a set of parameters and returns a result. An example is computing a statistical operation, such as mean or median, on selected EO data. A process is similar to a function or method in programming languages. 

A **process graph** chains specific process calls. Similarly to scripts in the context of programming, process graphs organize and automate the execution of one or more processes that could alternatively be executed individually. In a process graph, processes need to be specific, i.e. concrete values for input parameters need to be specified. These arguments can again be process graphs, scalar values, arrays or objects.

Sending a request to a back-end needs a process graph as input,
will trigger a process, and will result in output (computed values).

## Spatial data cube

A spatial data cube is an array with one or more dimensions
referring to spatial dimensions.  The figure below shows the data
of a four-dimensional (8 x 8 x 2 x 2) datacube, with dimension names
and values:

| #| dimension name | dimension values                     |
|--|----------------|--------------------------------------|
| 1| x              | 288790.5, 288819, 288847.5, 288876, 288904.5, 288933, 288961.5, 288990 |
| 2| y              | 9120747, 9120718, 9120690, 9120661, 9120633, 9120604, 9120576, 9120547 |
| 3| band           | `red`, `green` |
| 4| time           | `2018-02-10`, `2018-02-17` |

dimensions x and time are aligned along the x-axis; y and band are aligned along the y-axis.

![](https://github.com/edzer/openeo-api/raw/0.4.0/docs/fig2.png)

Data cubes as defined here have a _single value_ (scalar) for each
unique combination of dimension values.  The value pointed to by
arrows corresponds to the combination of x=288847.5 (red arrow),
y=9120661 (yellow arrow), band=red (blue arrow), time=2018-02-17 (green arrow),
and its value is 84 (brown arrow).

If the data concerns grayscale imagery, we could call this _single_
value a _pixel value_. One should keep in mind that it is _never_
a tuple of, say, `{red, green, blue}` values.  "Cell value of a
single raster layer" would be a better analogy; _data cube cell
value_ may be a good compromise.

## Processes that do not change dimensions

Math process that do not reduce do not change anything to the array
dimensions. The process `apply` can be used to apply unary functions
such as `abs` or `sqrt` to all values in a data cube. The process
`apply_dimension` applies (maps) an n-ary function to a particular
dimension. An example would be to apply `sort` to the time dimension,
in order to get every time series sorted. A more realistic example
would for instance apply a moving average filter to every time
series. An example of `apply_dimension` to the spatial dimensions
is to do a historgram stretch for every spatial (grayscale) image
of an image time series.

## Subsetting dimensions by dimension value selection

The `filter` process makes a cube smaller by selecting specific
values for a particular dimension. An example is a band filter that
selects the `red` band.

## Removing dimensions entirely by computation: `reduce`

`reduce` reduces the number of dimensions by computation. For
instance, using the _reducer_ proces `mean`, we can compute the
mean of the two time steps, and by that remove the time dimension.

Example:

- a time series reduction may return a regression slope for every (grayscale) pixel time series

## Reducing resolution: `aggregate`

Aggregation computes new values from sets of values that are _uniquely_ assigned to groups. It involves a grouping predicate (e.g. monthly, 100 m x 100 m grid cells, or a set of non-overlapping spatial polygons), and an reducer (e.g., `mean`) that computes one or more new values from the original ones.

Examples:

- a weekly time series may be aggregated to monthly values by computing the mean for all values in a month (grouping predicate: months)
- _spatial_ aggregation involves computing e.g. _mean_ pixel values on a 100 x 100 m grid, from 10 m x 10 m pixels, where each original pixel is assigned uniquely to a larger pixel (grouping predicate: 100 m x 100 m grid cells)

## Changing data cube geometry: `resample` (or `warp`)

Resampling (also called _scaling_) is a broader term where we have data at one resolution, and need values at another. In case we have values at a 100 m x 100 m grid and need values at a 10 m x 10 m grid, the original values will be reused many times, and may be simply assigned to the nearest high resolution grid cells (nearest neighbor method), or may be interpolated using various methods (e.g. by bilinear interpolation). This is often called _upsampling_ or _upscaling_. 

Resampling from finer to coarser grid is a special case of aggregation often called _downsampling_ or _downscaling_.

When the target grid or time series has a lower resolution (larger grid cells) or lower frequency (longer time intervals) than the source grid, aggregation might be used for resampling. For example, if the resolutions are similar, (e.g. the source collection provides 10 day intervals and the target needs values for 16 day intervals), then some form of interpolation may be more appropriate than aggregation as defined here.

## User-defined functions

The abbreviation **UDF** stands for **user-defined function**. With this concept, users are able to upload custom code and have it executed e.g. for every pixel of a scene, allowing custom calculations on server-side data.


