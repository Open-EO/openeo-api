


# Processes, Tasks, Jobs
The terms _process_, _task_, and _job_ have different meanings in the OpenEO API specification.

A _process_ is simply the description of an operation as provided by the back end, similar to a function definition in programming languages. 

A _task_ includes specific process calls, i.e. references to one or more processes including specific values for input arguments similar to a function call in programming. However, tasks can chain multiple processes. In particular, arguments of processes in general can be again (recursive) tasks, input datasets, or simple scalar or array values.

A _job_ brings one task to the back-end and organizes its execution, which may or may not induce costs. Jobs furthermore allow to run tasks from different _data views_ (see section on [data views](views.md)). Views define at which resolution and extent we look at the data during processing and hence allow to try out tasks on small subsets, or work interactively within web map applications.


# Job Evaluation
The API distinguishes two types how jobs are executed at back-ends. _Lazy evaluation_ runs computations on demand, i.e., with incoming requests for downloading the results. Jobs can be executed multiple times with different views (including spatial / temporal resolution and window) as provided by download requests, which could come e.g. from WCS or WMTS.  _Batch jobs_ in contrast are directly submitted to the back office's processing system. They will run only once, potentially include a provided view, and will store results after execution. Batch jobs are typically time consuming such that user interaction is not possible. 

As an example we consider the simple calculation of vegetation indexes on all available Sentinel 2 imagery over Europe. Batch evaluation will take all relevant images, compute the NDVI, and finally store the result whereas lazy evaluation will not start any computations on its own. As soon as a client performs a download request such as a `GetCoverage` WCS request, the job's process will be executed but only for requested pixels. However, back-ends are free to cache frequent intermediate results on their own.


