# UDFs

User-defined functions (UDFs) can be exposed to the data in different ways. This includes which parts of the data are passed to the function, how the function execution is parallelized, and how the expected output is structured. The OpenEO core API defines the following UDF types:

- [apply_pixel](#apply_pixel)
- [apply_scene](#apply_scene)
- [reduce_time](#reduce_time)
- [reduce_space](#reduce_space)
- [window_time](#window_time)
- [window_space](#window_space)
- [window_spacetime](#window_spacetime)
- [aggregate_time](#aggregate_time)
- [aggregate_space](#aggregate_space)
- [aggregate_spacetime](#aggregate_spacetime)
- [chunkreduce_time](#chunkreduce_time)
- [chunkreduce_space](#chunkreduce_space)
- [chunkreduce_spacetime](#chunkreduce_spacetime)


This document describes some details of the abovementioned UDF types. Back-ends allowing the execution of UDF's will report, which types they support. For example applying UDFs on individual scenes is not possible on higher level data cube back-ends. In the descriptions below, the question in which format data is streamed to and from the functions is not yet covered. Furthermore, the described categories only include unary operations that take one image (collection) as input.  


### UDF types

#### apply_pixel
This type applies a simple function to one pixel of the input image or image collection. The function gets the value of one pixel (including all bands) as input and produces a single scalar or tuple output. The result has the same schema as the input image (collection) but different bands. Examples include the computation of vegetation indexes or filtering cloudy pixels. 

#### apply_scene
This low-level UDF type applies a function on individual scenes.  The function gets a single scene as input and produces a modified "scene" with the same spatial footprint. This UDF type will only be supported by OpenEO back-ends with a file-based data organization. Higher level data-cube oriented back-offices in general do not keep track of the scenes and hence will not be able to parallelize operations on scene level. The type is mostly useful for working with lower-level data products, e.g., to perform atmospheric correction or any other operation that needs scene metadata. 

#### reduce_time
This type applies a function to a single time series and produces a zero-dimensional output (scalar or tuple). Notice that the `view` parameter for OpenEO processes affects the resolution and window of the time series provided as input to UDFs of this type. 

#### reduce_space
This type applies a function to a temporal snapshot of the data and produces a single value or multiband tuple per snapshot. The result is a time series. 

#### window_time
The provided UDF is called for each pixel and will receive values from pixels within a temporal neighborhood of specified size around that pixel. Neighboring values can be used to derive a new value of the center pixel, which can be a single scalar value or a (multiband) tuple. Windows at boundary regions should be filled with NA values. 

#### window_space
The provided UDF is called for each pixel and will receive values from pixels within a spatial neighborhood of specified size around that pixel. Neighboring values can be used to derive a new value of the center pixel, which can be a single scalar value or a (multiband) tuple. Windows at boundary regions should be filled with NA values. 

#### window_spacetime
Similar to `window_time` and `window_space`, this type derives a new value for the central pixel of a spatiotemporal window of specified size. The provided function receives a (multispectral) spacetime array as input and produces a single value (either scalar or multispectral) as output. The result has the same number of pixels as the input dataset. Windows at boundary regions should be filled with NA values. 

#### aggregate_time
Similar to `reduce_time` this type applies the given UDF independently on pixel time series of the input data but produces a new time series with different temporal resolution. `reduce_time` can be seen as a special case of `aggregate_time` where the temporal dimension is dropped.
Examples of this UDF type include the generation of monthly aggregates from 16 day data.  The result has the same spatial resolution.

#### aggregate_space
Similar to `aggregate_time`, this type applies the provided function on temporal snapshots of the data and generates an image with different spatial resolution. The result will have the same temporal resolution.

#### chunkreduce_time
Partitions the input data into equally sized temporal chunks and aggregates them to a single value or tuple. The function must return a single scalar or tuple (multiband) output. The result has the same spatial but a coarser temporal resolution.

#### chunkreduce_space
Similar to `chunkreduce_time`, this type applies the provided function on spatial chunks of the data and generates an aggregated value or tuple. to aggregate. The result will have the same temporal but a coarser spatial resolution. Examples of this type include the generation of image pyramids.

#### chunkreduce_spacetime
Similar to `chunkreduce_space` and `chunkreduce_time`, UDFs of this type receive spatiotemporal chunks such that the output has lower spatial and lower temporal resolution.


### R implementation

| **UDF Type**          | **Function prototype** | **Details** |
| --------------------- | ---------------------- | ----------- |
| apply_pixel           |                        |             |
| apply_scene           |                        |             |
| reduce_time           |                        |             |
| reduce_space          |                        |             |
| window_time           |                        |             |
| window_space          |                        |             |
| window_spacetime      |                        |             |
| aggregate_time        |                        |             |
| aggregate_space       |                        |             |
| aggregate_spacetime   |                        |             |
| chunkreduce_time      |                        |             |
| chunkreduce_space     |                        |             |
| chunkreduce_spacetime |                        |             |


