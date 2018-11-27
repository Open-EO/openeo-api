# Client library development guidelines

This is a proposal for workflows that client libraries should support to make the experience with each library similar and users can easily adopt examples and workflows.

For best experience libraries should still embrace best practices common in their environments. This means clients can...

* choose which kind of casing they use (see below). 
* feel free to implement aliases for methods.

## Conventions

### Casing

Clients can use `snake_case`, `camelCase` or any method used commonly in their environment. For example, the API request to get a list of collections can either be names `get_collections` or `getCollections`. This applies for all names, including scopes, method names and parameters.

### Scopes

Each method belongs to a scope. To achieve this in object-oriented (OO) programming languages, methods would be part of a class. If programming languages don't support scopes, you may need to simulate it somehow to prevent name collisions, e.g. by adding a prefix to the method names (like in the "procedural style" example below). Best practices for this will likely evolve over time.

Example for the `version` method in `openEO`:

* Procedural style: `openeo_version()` 
* Object-oriented style:
  ```java
  OpenEO obj = new OpenEO();
  obj.version();
  ```

If you can't store scope data in an object, you may need to pass these information as argument(s) to the method.

Example:

* Procedural style:
  ```php
  $connection = openeo_connect("https://openeo.org");
  openeo_get_capabilities($connection);
  ```
* Object-oriented style:
  ```java
  OpenEO obj = new OpenEO();
  Connection con = obj.connect("https://openeo.org");
  con.getCapabilities();
  ```

### Scope categories

Each scope is assigned to a scope category, of which there are three:

* *Root* category: Contains only the scope `openEO`.
* *API* category: Mostly methods hiding API calls to the back-ends. Methods may be implemented asynchronously. Contains the scopes `Connection`, `File`, `Job`, `ProcessGraph`, `Service`.
* *Content*: Mostly methods hiding the complexity of response content. Methods are usually implemented synchronously. Currently contains only the scope `Capabilities`. Method names should be prefixed if name collisions are likely.

Method names across ALL the scopes that belong to the *root* or *API* categories MUST be unique. This is the case because the parameter in `hasFeature(method_name)` must be unambiguous.

Method names of scopes in the *Content* category may collide with method names of scopes in the *root*/*API* categories, as is the case with `version()` (relates to (1) the client library version in `openEO` scope and (2) the API version in `Connection` scope).

### Parameters

The parameters usually follow the request schemas in the openAPI specification. The parameters should follow their characteristics, for example regarding the default values.

Some methods have a long list of (optional) parameters. This is easy to implement for languages that support named parameters such as R. Other languages may have problems implementing this natively as they need to fill many parameters with default values. For example creating a job in R with a budget would lead to such a method call: `createJob(process_graph = ..., null, budget = 123)`, but in PHP it would be: `createJob(..., null, null, null, null, null, 123)`. This is not an ideal behaviour, therefore client developers might want to consider passing parameters in coupled in a dictionary or class to emulate named parameters. The example in PHP could be improved to `createJob([process_graph => ..., null, budget => 123])`.

**ToDo:** Allow sorting and other useful operations for lists?

## Method mappings

**Note:** Subscriptions and some scopes for response JSON objects are still missing. We are open for proposals.

Parameters with a leading `?` are optional.

### Scope: `openEO` (root category)

| Description                                                  | Client method                             |
| ------------------------------------------------------------ | ----------------------------------------- |
| Connect to a back-end, including authentication. Returns `Connection`. | `connect(url, ?auth_type, ?auth_options)` |
| Get client library version.                                  | `version()`                               |

#### Parameters

* **auth_type** in `connect`: `null`, `basic` or `oidc` (non-exclusive). Defaults to `null` (no authentication).
* **auth_options** in `connect`: May hold additional data for authentication, for example a username and password for `basic` authentication.

### Scope: `Connection` (API category)

| Description                                                  | API Request               | Client method                                                |
| ------------------------------------------------------------ | ------------------------- | ------------------------------------------------------------ |
| Get the capabilities of the back-end. Returns `Capabilities`. | `GET /`                   | `capabilities()`                                             |
| List the supported output file formats.                      | `GET /output_formats`     | `listFileTypes()`                                            |
| List the supported secondary service types.                  | `GET /service_types`      | `listServiceTypes()`                                         |
| List all collections available on the back-end.              | `GET /collections`        | `listCollections()`                                          |
| Get information about a single collection.                   | `GET /collections/{name}` | `describeCollection(name)`                                   |
| List all processes available on the back-end.                | `GET /processes`          | `listProcesses()`                                            |
| Authenticate with OpenID Connect (if not specified in `connect`). | `GET /credentials/oidc`   | `authenticateOIDC(?options)`                                  |
| Authenticate with HTTP Basic (if not specified in `connect`). | `GET /credentials/basic`  | `authenticateBasic(username, password)`                      |
| Get information about the authenticated user.                | `GET /me`                 | `describeAccount()`                                          |
| Lists all files from a user. Returns a list of `File`.       | `GET /files/{user_id}`    | `listFiles(?user_id)`                                        |
| Creates a (virtual) file. Returns a `File`.                  | *None*                    | `createFile(path, ?user_id)`                                 |
| Validates a process graph.                                   | `POST /validate`          | `validateProcessGraph(process_graph)`                        |
| Lists all process graphs of the authenticated user. Returns a list of `ProcessGraph`. | `GET /process_graphs`     | `listProcessGraphs()`                                        |
| Creates a new stored process graph. Returns a `ProcessGraph`. | `POST /process_graphs`    | `createProcessGraph(process_graph, ?title, ?description)`    |
| Executes a process graph synchronously.                      | `POST /preview`           | `execute(process_graph, ?output_format, ?output_parameters, ?budget)` |
| Lists all jobs of the authenticated user. Returns a list of `Job`. | `GET /jobs`               | `listJobs()`                                                 |
| Creates a new job. Returns a `Job`.                          | `POST /jobs`              | `createJob(process_graph, ?output_format, ?output_parameters, ?title, ?description, ?plan, ?budget, ?additional)` |
| Lists all secondary services of the authenticated user. Returns a list of `Service`. | `GET /services`           | `listServices()`                                             |
| Creates a new secondary service. Returns  a `Service`.       | `POST /services`          | `createService(process_graph, type, ?title, ?description, ?enabled, ?parameters, ?plan, ?budget)` |

#### Parameters

* **user_id** in `listFiles` and `createFile`: Defaults to the user id of the authenticated user.
* **options** in `authenticateOIDC`: May hold additional data required for OpenID connect authentication.

### Scope `Capabilities` (Content category)

Should be prefixed with `Capabilities` if required. In non-object-oriented paradigms it is likely required as `version()` in this scope and the scope `OpenEO` could collide. For example, `version()` in this scope could be named `openeo_capabilities_version()` in procedural style.

| Description                                      | Field                  | Client method             |
| ------------------------------------------------ | ---------------------- | ------------------------- |
| Get openEO version.                              | `version`              | `version()`               |
| List all supported features / endpoints.         | `endpoints`            | `listFeatures()`          |
| Check whether a feature / endpoint is supported. | `endpoints` > ...      | `hasFeature(method_name)` |
| Get default billing currency.                    | `billing` > `currency` | `currency()`              |
| List all billing plans.                          | `billing` > `plans`    | `listPlans()`             |

#### Parameters

* **method_name** in `hasFeature`: The name of a client method in any of the scopes that are part of the *API* category. E.g. `hasFeature("describeAccount")` checks whether the `GET /me` endpoint is contained in the capabilities response's `endpoints` object.

### Scope: `File` (API category)

The `File` scope internally knows the `user_id` and the `path`.

| Description           | API Request                      | Client method          |
| --------------------- | -------------------------------- | ---------------------- |
| Download a user file. | `GET /files/{user_id}/{path}`    | `downloadFile(target)` |
| Upload a user file.   | `PUT /files/{user_id}/{path}`    | `uploadFile(source)`   |
| Delete a user file.   | `DELETE /files/{user_id}/{path}` | `deleteFile()`         |

#### Parameters

* **target** in `downloadFile`: Path to a local file or folder.

### Scope: `Job` (API category)

The `Job` scope internally knows the `job_id`.

| Description                                | API Request                        | Client method                                                |
| ------------------------------------------ | ---------------------------------- | ------------------------------------------------------------ |
| Get all job information.                   | `GET /jobs/{job_id}`               | `describeJob()`                                              |
| Update a job.                              | `PATCH /jobs/{job_id}`             | `updateJob(?process_graph, ?output_format, ?output_parameters, ?title, ?description, ?plan, ?budget, ?additional)` |
| Delete a job                               | `DELETE /jobs/{job_id}`            | `deleteJob()`                                                |
| Calculate an time/cost estimate for a job. | `GET /jobs/{job_id}/estimate`      | `estimateJob()`                                              |
| Start / queue a job for processing.        | `POST /jobs/{job_id}/results`      | `startJob()`                                                 |
| Stop / cancel job processing.              | `DELETE /jobs/{job_id}/results`    | `stopJob()`                                                  |
| Get document with download links.          | `GET /jobs/{job_id}/results`       | `listResults(?type)`                                         |
| Download job results.                      | `GET /jobs/{job_id}/results` > ... | `downloadResults(target)`                                    |

#### Parameters

* **type** in `listResult`: Either `json` or `metalink` (non-exclusive). Defaults to `json`.
* **target** in `downloadResults`: Path to a local folder.

### Scope: `ProcessGraph` (API category)

The `ProcessGraph` scope internally knows the `pg_id` (`process_graph_id`).

| Description                                       | API Request                      | Client method                                              |
| ------------------------------------------------- | -------------------------------- | ---------------------------------------------------------- |
| Get all information about a stored process graph. | `GET /process_graphs/{pg_id}`    | `describeProcessGraph()`                                   |
| Update a stored process graph.                    | `PATCH /process_graphs/{pg_id}`  | `updateProcessGraph(?process_graph, ?title, ?description)` |
| Delete a stored process graph.                    | `DELETE /process_graphs/{pg_id}` | `deleteProcessGraph()`                                     |

### Scope: `Service` (API category)

The `Service` scope internally knows the `service_id`.

| Description                                        | API Request                     | Client method                                                |
| -------------------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| Get all information about a secondary web service. | `GET /services/{service_id}`    | `describeService()`                                          |
| Update a secondary web service.                    | `PATCH /services/{service_id}`  | `updateService(?process_graph, ?title, ?description, ?enabled, ?parameters, ?plan, ?budget)` |
| Delete a secondary web service.                    | `DELETE /services/{service_id}` | `deleteService()`                                            |

## Processes

The processes a back-end supports may be offered by the clients as methods in its own scope. The method names should follow the process names, but the conventions listed above can be applied here as well, e.g. converting `filter_bands` to `filterBands`. As parameters have no natural or technical ordering in the JSON objects, clients must come up with a reasonable ordering of parameters if required. This could be inspired by existing clients. The way of building a process graph from processes heavily depends on the technical capabilities of the programming language. Therefore it may differ between the client libraries. Follow the best practices of the programming language, e.g. support method chaining if possible.

## Workflow example

Some simplified example workflows using different programming styles are listed below. The following steps are executed:

1. Loading the client library.
2. Connecting to a back-end and authenticating with username and password via OpenID Connect.
3. Requesting the capabilities and showing the implemented openEO version of the back-end.
4. Showing information about the "Sentinel-2A" collection.
5. Showing information about all processes supported by the back-end.
6. Building a simple process graph.
7. Creating a job.
8. Pushing the job to the processing queue.
9. After a while, showing the job details, e.g. checking the job status.
10. Once processing is finished, downloading the job results to the local directory `/tmp/job_results/`.

### R (functional style)

```r
library(openeo)

con = connect("https://openeo.org", "username", "password")
cap = capabilities()
cap %>% version()
con %>% describeCollection("Sentinel-2A")
con %>% listProcesses()

processgraph = process("get_collection", name = "Sentinel-2A") %>% 
  process("filterBbox", west = 672000, south = 5181000, east = 652000, north = 5161000, crs = "EPSG:32632") %>%
  process("filterDaterange", extent = c("2017-01-01T00:00:00Z", "2017-01-31T23:59:59Z")) %>%
  process("NDVI", nir = "B4", red = "B8A") %>%
  process("minTime")

job = con %>% createJob(processgraph)
job %>% startJob()
job %>% describeJob()
job %>% downloadResults("/tmp/job_results/")
```

### Python (mixed style)

```python
import openeo

con = openeo.connect("https://openeo.org", "username", "password")
cap = con.capabilities()
print(cap.version())
print(con.describe_collection("Sentinel-2A"))
print(con.list_processes())

processes = con.get_processes()
pg = processes.get_collection(name="Sentinel-2A")
pg = processes.filter_bbox(pg, west=672000, south=5181000, east=652000, north=5161000, crs="EPSG:32632")
pg = processes.filter_daterange(pg, extent=["2017-01-01T00:00:00Z", "2017-01-31T23:59:59Z"])
pg = processes.ndvi(pg, nir="B4", red="B8A")
pg = processes.min_time(pg)

job = con.create_job(pg.graph)
job.start_job()
print job.describe_job()
job.download_results("/tmp/job_results/")
```

### Java (object oriented style)

```java
import org.openeo.*;

OpenEO obj = new OpenEO();
Connection con = obj.connect("https://openeo.org", "username", "password");
Capabilities cap = con.capabilities();
System.out.println(cap.version());
System.out.println(con.describeCollection("Sentinel-2A"));
System.out.println(con.listProcesses());

ProcessGraphBuilder pgb = con.getProcessGraphBuilder()
// Chain processes...
ProcessGraph processGraph = pgb.buildProcessGraph();

Job job = con.createJob(processGraph);
job.startJob();
System.out.println(job.describeJob());
job.downloadResults("/tmp/job_results/");
```

### PHP (procedural style)

```php
require_once("/path/to/openeo.php");

$connection = openeo_connect("http://openeo.org", "username", "password");
$capabilities = openeo_capabilities($connection);
echo openeo_capabilities_version($capabilites);
echo openeo_describe_collection($connection, "Sentinel-2A");
echo openeo_list_processes($connection);

$pg = openeo_process($pg, "get_collection", ["name" => "Sentinel-2A"]);
$pg = openeo_process($pg, "filter_bbox", ["west" => 672000, "south" => 5181000, "east" => 652000, "north" => 5161000, "crs" => "EPSG:32632"]);
$pg = openeo_process($pg, "filter_daterange", ["extent" => ["2017-01-01T00:00:00Z", "2017-01-31T23:59:59Z"]]);
$pg = openeo_process($pg, "NDVI", ["red" => "B4", "nir" => "B8A"]);
$pg = openeo_process($pg, "min_time");

$job = openeo_create_job($connection, $pg);
openeo_start_job($job);
echo openeo_describe_job($job);
openeo_download_results($job, "/tmp/job_results/");
```
