# Remote UDP Extension

The openEO API is a specification for interoperable cloud-based processing of large Earth observation datasets.

This extension enables user to load user-defined processes that are hosted external to the openEO API (e.g., GitHub or cloud storage) through the process namespace into process graphs.

- Version: **0.1.0**
- Stability: **experimental**
- Conformance class: `https://api.openeo.org/extensions/remote-udp/0.1.0`

## Justification

The openEO API defines the `namespace` property in a process node of a process graph as follows:
>  The following options are predefined by the openEO API, but additional namespaces may be introduced by back-ends or in a future version of the API.
> * `null` [...]
> * `backend` [...]
> * `user` [...]

This makes it possible for this extension to add additional allowed values to the `namespace` property.

## Specification

This extension extends the `namespace` property of process graph nodes so that it accepts **absolute** URL with the protocols `https` (**recommended**) and `http` (discouraged). The URLs specified MUST return one of the following two options:

1. A single process, compatible\* to the endpoint `GET /process_graphs/{process_graph_id}`.
   In this case, the `id` property of the process graph node MUST be equal to the `id` of the process, 
   otherwise a `ProcessNamespaceInvalid` error is thrown
2. A list of processes, compatible\* to the endpoint `GET /process_graphs`.
   In this case, the `id` property of the process graph node is used to identify the process from the list.
   If not found a `ProcessNamespaceInvalid` error is thrown

\* Compatible means in this context that the requests and responses must comply to the openEO API specification with the following exceptions:

- User credentials / tokens that are obtained through the openEO API MUST NOT not be sent to URIs that are external to the openEO API.
  The requirement to provide an `Authorization` header for the respective endpoints doesn't apply.
- For a list of processes, the full process description MUST be provided for the process with the given ID within the first request.
  This means that the recommendation to omit large roperties such as `process_graph` doesn't apply.
  It also requires that the requester doesn't need to paginate through additional pages to find the process with the given ID.
  Ideally, the list of processes is not paginated as otherwise the process with the given ID may move to other pages over time.

### Client Considerations

If a client is conncected to a specific backend, the client MUST only offer this functionality to users if the conformance class of this extension is listed in the `conformsTo` property of the `GET /` endpoint.

The protocol `http` is discouraged for URLs as web-based clients may not be able to retrieve HTTP URLs from a HTTPS context.
For the same reason it is also RECOMMENDED to enable CORS for all URLs.

### Error Handling

The following error SHOULD be reported if the namespace can't be resolved:

- Code: `ProcessNamespaceInvalid`
- Message: `The value passed for namespace '{namespace}' in process '{process}' is invalid: {reason}`
- HTTP Status Code: 400

## Example

An exemplary process graph node:

```json
{
  "process_id": "echo",
  "namespace": "https://hub.openeo.org/processes/echo",
  "arguments": {
    "message": "Hello World"
  },
  "result": true
}
```
