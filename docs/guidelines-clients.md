# Client library development guidelines

This is a proposal for workflows that client libraries should support to make the experience with each library similar and users can easily adopt examples and workflows.

For best experience libraries should still embrace best practices common in their environments. This means clients can...

* choose which kind of casing they use (see below). 
* feel free to implement aliases for methods.

## Conventions

### Casing

Clients can use `snake_case`, `camelCase` or any method used commonly in their environment. For example, the API request to get a list of collections can either be names `get_collections` or `getCollections`.

### Scopes

Methods usually have a different scope, in object-oriented (OO) programming methods would be part of a class. If programming languages don't have functionalities to scope you may need to simulate it somehow to prevent name collisions. Best practices for this will likely evolve over time.

Example for the `version` method in `openEO`:

* Procedural style: `openeo_version()` 
* OO style:
  ```
  OpenEO obj = new OpenEO();
  obj.version();
  ```

If you can't store scope data in an object, you may need to pass these information as argument(s) to the method.

Example:

* Procedural style:
  ```
  $connection = openeo_connect("https://openeo.org");
  openeo_get_capabilities($connection);
  ```
* OO style:
  ```
  OpenEO obj = new OpenEO();
  Connection con = obj.connect("https://openeo.org");
  con.getCapabilities();
  ```

## Request to method mapping

**Note:** Subscriptions and some scopes for JSON objects are still missing.

Italic values are the default values, parameters with a leading `?` are optional.

**ToDo:** Allow sorting and other operations for lists?

### Scope: `openEO`

| Description                                                  | Client method                                   | Parameters                        |
| ------------------------------------------------------------ | ----------------------------------------------- | --------------------------------- |
| Connect to a back-end, including authentication. Returns `Connection`. | `connect(url, ?username, ?password, ?authType)` | **authType**: *null*, basic, oidc |
| Get client library version.                                  | `version()`                                     |                                   |

### Scope: `Connection`

| Description                                                  | API Request               | Client method                           | Parameters                                   |
| ------------------------------------------------------------ | ------------------------- | --------------------------------------- | -------------------------------------------- |
| Get the capabilities of the back-end. Returns `Capabilities`. | `GET /`                   | `capabilities()`                        |                                              |
| List the supported output file formats.                      | `GET /output_formats`     | `listFileTypes()`                       |                                              |
| List the supported secondary service types.                  | `GET /service_types`      | `listServiceTypes()`                    |                                              |
| List all collections available on the back-end.              | `GET /collections`        | `listCollections()`                     |                                              |
| Get information about a single collection.                   | `GET /collections/{name}` | `describeCollection(name)`              |                                              |
| List all processes available on the back-end.                | `GET /processes`          | `listProcesses()`                       |                                              |
| Authenticate with OpenID Connect (if not specified in `connect`). | `GET /credentials/oidc`   | `autenticateOIDC(username, password)`   |                                              |
| Authenticate with HTTP Basic (if not specified in `connect`). | `GET /credentials/basic`  | `authenticateBasic(username, password)` |                                              |
| Get information about the authenticated user.                | `GET /me`                 | `describeUser()`                        |                                              |
| Lists all files from a user. Returns a list of `File`.       | `GET /files/{user_id}`    | `listFiles(?user_id)`                   | **user_id**: defaults to authenticated user. |
| Creates a (virtual) file. Returns a `File`.                  | *None*                    | `createFile(path, ?user_id)`            | **user_id**: defaults to authenticated user. |
| Validates a process graph.                                   | `POST /validate`          | `validateProcessGraph(process_graph)`   |                                              |
| Lists all process graphs of the authenticated user.Returns a list of `ProcessGraph`. | `GET /process_graphs`     | `listProcessGraphs()`                   |                                              |
| Executes a process graph synchronously.                      | `POST /preview`           | `execute(process_graph, ...)`           | TBD                                          |
| Lists all jobs of the authenticated user. Returns a list of `Job`. | `GET /jobs`               | `listJobs()`                            |                                              |
| Creates a new job. Returns a `Job`.                          | `POST /jobs`              | `createJob(process_graph, ...)`         | TBD                                          |
| Lists all secondary services of the authenticated user. Returns a list of `Service`. | `GET /services`           | `listServices()`                        |                                              |
| Creates a new secondary service. Returns  a `Service`.       | `POST /services`          | `createService(...)`                    |                                              |

### Scope `Capabilities`

Should be prefixed with `capabilities` if required.

| Description                                      | Field                  | Client method             | Parameters |
| ------------------------------------------------ | ---------------------- | ------------------------- | ---------- |
| Get openEO version.                              | `version`              | `version()`               |            |
| List all supported features / endpoints.         | `endpoints`            | `listFeatures()`          |            |
| Check whether a feature / endpoint is supported. | `endpoints` > ...      | `hasFeature(method_name)` |            |
| Get default billing currency.                    | `billing` > `currency` | `currency()`              |            |
| List all billing plans.                          | `billing` > `plans`    | `listPlans()`             |            |

### Scope: `File`

The `File` internally knows the `user_id` and the `path`.

| Description           | API Request                      | Client method          | Parameters |
| --------------------- | -------------------------------- | ---------------------- | ---------- |
| Download a user file. | `GET /files/{user_id}/{path}`    | `downloadFile(target)` |            |
| Upload a user file.   | `PUT /files/{user_id}/{path}`    | `uploadFile(source)`   |            |
| Delete a user file.   | `DELETE /files/{user_id}/{path}` | `deleteFile()`         |            |

### Scope: `Job`

The `Job` scope internally knows the `job_id`.

| Description                                | API Request                        | Client method             | Parameters                 |
| ------------------------------------------ | ---------------------------------- | ------------------------- | -------------------------- |
| Get all job information.                   | `GET /jobs/{job_id}`               | `describeJob()`           |                            |
| Update a job.                              | `PATCH /jobs/{job_id}`             | `updateJob(...)`          | TBD                        |
| Delete a job                               | `DELETE /jobs/{job_id}`            | `deleteJob()`             |                            |
| Calculate an time/cost estimate for a job. | `GET /jobs/{job_id}/estimate`      | `estimateJob()`           |                            |
| Start / queue a job for processing.        | `POST /jobs/{job_id}/results`      | `startJob()`              |                            |
| Stop / cancel job processing.              | `DELETE /jobs/{job_id}/results`    | `stopJob()`               |                            |
| Get document with download links.          | `GET /jobs/{job_id}/results`       | `listResults(?type)`      | **type**: *json*, metalink |
| Download job results.                      | `GET /jobs/{job_id}/results` > ... | `downloadResults(target)` |                            |

### Scope: `ProcessGraph`

The `ProcessGraph` scope internally knows the `pg_id` (`process_graph_id`).

| Description                                       | API Request                      | Client method             | Parameters |
| ------------------------------------------------- | -------------------------------- | ------------------------- | ---------- |
| Get all information about a stored process graph. | `GET /process_graphs/{pg_id}`    | `describeProcessGraph()`  |            |
| Update a stored process graph.                    | `PATCH /process_graphs/{pg_id}`  | `updateProcessGraph(...)` | TBD        |
| Delete a stored process graph.                    | `DELETE /process_graphs/{pg_id}` | `deleteProcessGraph()`    |            |

### Scope: `Service`

The `Service` scope internally knows the `service_id`.

| Description                                        | API Request                     | Client method        | Parameters |
| -------------------------------------------------- | ------------------------------- | -------------------- | ---------- |
| Get all information about a secondary web service. | `GET /services/{service_id}`    | `describeService()`  |            |
| Update a secondary web service.                    | `PATCH /services/{service_id}`  | `updateService(...)` | TBD        |
| Delete a secondary web service.                    | `DELETE /services/{service_id}` | `deleteService()`    |            |

## Workflow example

Some simplified example workflows using different programming styles are listed below.

### R (functional style)

```r
library(openeo)
con = connect("https://openeo.org", "username", "password", "oidc")
cap = capabilities()
cap %>% version()
con %>% describeCollection("Sentinel-2A")
con %>% listProcesses()
pg = ...
job = con %>% createJob(pg)
job %>% startJob()
job %>% describeJob()
job %>% downloadResults("/tmp/job_results/")
```

### Python (mixed style)

```python
import openeo
con = openeo.connect("https://openeo.org", "username", "password", "oidc")
cap = con.capabilities()
print cap.version()
print con.describe_collection("Sentinel-2A")
print con.list_processes()
pg = ...
job = con.create_job(pg)
job.start_job()
print job.describe_job()
job.download_results("/tmp/job_results/")
```

### Java (object oriented style)

```java
import org.openeo.*;
OpenEO obj = new OpenEO();
Connection con = obj.connect("https://openeo.org", "username", "password", "oidc");
Capabilities cap = con.capabilities();
System.out.println(cap.version());
System.out.println(con.describeCollection("Sentinel-2A"));
System.out.println(con.listProcesses());
ProcessGraph pg = ...;
Job job = con.createJob(pg);
job.startJob();
System.out.println(job.describeJob());
job.downloadResults("/tmp/job_results/");
```

### PHP (procedural style)

```php
$connection = openeo_connect("http://openeo.org", "username", "password", "oidc");
$capabilities = openeo_capabilities($connection);
echo openeo_capabilities_version($capabilites);
echo openeo_describe_collection($connection, "Sentinel-2A");
echo openeo_list_processes($connection);
$process_graph = ...;
$job = openeo_create_job($connection, $process_graph);
openeo_start_job($job);
echo openeo_describe_job($job);
openeo_download_results($job, "/tmp/job_results/");
```
