# Jobs

As described in the [glossary](glossary.md), a **job** brings one process graph to the back-end and organizes its execution, which may or may not induce costs.


# Evaluation types
The API distinguishes two types how jobs are (asynchronously) executed at back-ends. _Lazy evaluation_ runs computations on demand, i.e., with incoming requests for downloading the results. Jobs can be executed multiple times with different views (including spatial / temporal resolution and window) as provided by download requests, which could come e.g. from WCS or WMTS.  _Batch jobs_ in contrast are directly submitted to the back office's processing system. They will run only once, potentially include a provided view, and will store results after execution. Batch jobs are typically time consuming such that user interaction is not possible. 

As an example we consider the simple calculation of vegetation indexes on all available Sentinel 2 imagery over Europe. Batch evaluation will take all relevant images, compute the NDVI, and finally store the result whereas lazy evaluation will not start any computations on its own. As soon as a client performs a download request such as a `GetCoverage` WCS request, the job's process will be executed but only for requested pixels. However, back-ends are free to cache frequent intermediate results on their own.

There is a third way to execute jobs at the back-ends, but does not really fit into the types mentioned before. It is similar to batch jobs, but results are delivered immediately after computation, i.e. synchronously. 


