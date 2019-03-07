# Status and error handling

The success of requests MUST be indicated using [HTTP status codes](https://tools.ietf.org/html/rfc7231#section-6) according to [RFC 7231](https://tools.ietf.org/html/rfc7231).

If the API responds with a status code between 100 and 399 the back-end indicates that the request has been handled successfully.

In general an error is communicated with a status code between 400 and 599. Client errors are defined as a client passing invalid data to the service and the service *correctly* rejecting that data. Examples include invalid credentials, incorrect parameters, unknown versions, or similar. These are generally "4xx" HTTP error codes and are the result of a client passing incorrect or invalid data. Client errors do *not* contribute to overall API availability. 

Server errors are defined as the server failing to correctly return in response to a valid client request. These are generally "5xx" HTTP error codes. Server errors *do* contribute to the overall API availability. Calls that fail due to rate limiting or quota failures MUST NOT count as server errors. 

## JSON error object

A JSON error object SHOULD be sent with all responses that have a status code between 400 and 599.

``` json
{
  "id": "936DA01F-9ABD-4D9D-80C7-02AF85C822A8",
  "code": "SampleError",
  "message": "A sample error message.",
  "url": "http://www.openeo.org/docs/errors/SampleError"
}
```

Sending `code` and `message` is REQUIRED. 

* A back-end MAY add a free-form `id` (unique identifier) to the error response to be able to log and track errors with further non-disclosable details.

* The `code` is either one of the standardized textual openEO error codes below or a proprietary error code.

* The `message` explains the reason the server is rejecting the request. For "4xx" error codes the message explains how the client needs to modify the request.

  By default the message MUST be sent in English language. Content Negotiation is used to localize the error messages: If an `Accept-Language` header is sent by the client and a translation is available, the message should be translated accordingly and the `Content-Language` header must be present in the response. See "[How to localize your API](http://apiux.com/2013/04/25/how-to-localize-your-api/)" for more information.

* `url` is an OPTIONAL attribute and contains a link to a resource that is explaining the error and potential solutions in-depth.

## Standardized status codes

The openEO API usually uses the following HTTP status codes for successful requests: 

- **200 OK**:
  Indicates a successful request **with** a response body being sent.
- **201 Created**
  Indicates a successful request that successfully created a new resource. Sends a `Location` header to the newly created resource **without** a response body.
- **202 Accepted**
  Indicates a successful request that successfully queued the creation of a new resource, but it has not been created yet. The response is sent **without** a response body.
- **204 No Content**:
  Indicates a successful request **without** a response body being sent.

The openEO API often uses the following HTTP status codes for failed requests: 

- **400 Bad Request**:
  The back-end responds with this error code whenever the error has its origin on client side and no other HTTP status code in the 400 range is suitable.

- **401 Unauthorized**:
  The client did not provide any authentication details for a resource requiring authentication or the provided authentication details are not correct.

- **403 Forbidden**:
  The client did provided correct authentication details, but the privileges/permissions of the provided credentials do not allow to request the resource.

- **404 Not Found**:
  The resource specified by the path does not exist, i.e. one of the resources belonging to the specified identifiers are not available at the back-end.
  *Note:* Unsupported endpoints MUST use HTTP status code 501.

- **500 Internal Server Error**:
  The error has its origin on server side and no other status code in the 500 range is suitable.

- **501 Not Implemented**:
  An endpoint is specified in the openEO API, but is not supported.


If a HTTP status code in the 400 range is returned, the client SHOULD NOT repeat the request without modifications. For HTTP status code in the 500 range, the client MAY repeat the same request later.

All HTTP status codes defined in RFC 7231 in the 400 and 500 ranges can be used as openEO error code in addition to the most used status codes mentioned here. Responding with openEO error codes 400 and 500 SHOULD be avoided in favor of any more specific standardized or proprietary openEO error code.

## openEO error codes

The following table of error codes is **incomplete**. These error codes will evolve over time. If you are missing any common error, please contribute it by adding an [issue](https://github.com/Open-EO/openeo-api/issues/new), creating a pull request or get in contact in our [chat room](https://openeo-chat.eodc.eu/channel/public).

The whole table of error codes is available as [JSON file](../errors.json), which can be used by implementors to automatically generate error responses.

{{ error_codes() }}