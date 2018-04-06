# Status and error handling

The success of requests *must* be indicated using [HTTP status codes](https://tools.ietf.org/html/rfc7231#section-6) according to [RFC 7231](https://tools.ietf.org/html/rfc7231). In general an error is communicated with a status code between 400 and 599. If the API responds with a status code between 100 and 399 the back-end indicates that the request has been handled successfully.

## JSON error object

A JSON error object **should** be sent with all responses that have a status code between 400 and 599.

```
{
  "id": "",
  "code": 123,
  "message": "A sample error message.",
  "url": "http://www.openeo.org/docs/errors/123"
}
```

Sending `code` and `message` is *required*. 

* A back-end *may* add an `id` (unique identifier) to the error response to be able to log and track errors with further non-disclosable details.

* The `code` is either one of the standardized openEO error codes below or a proprietary error code with a number greater than 10000.

* The `message` explains what the client might need to change or what the server is struggling with.
  By default the message *must* be sent in English language.

  Content Negotiation is used to localize the error messages: If an `Acceppt-Language` header is sent by the client and a translation is available, the message should be translated accordingly and the `Content-Language` header must be present in the response. See "[How to localize your API](http://apiux.com/2013/04/25/how-to-localize-your-api/)" for more information.

* `url` is an *optional* attribute and might contain a link to a resource that is explaining the error and potential solutions in-depth.

## Standardized status codes

The openEO API usually uses the following HTTP status codes for successful requests: 

- **200 OK**:
  Indicates a successful request **with** a response body being sent.
- **204 No Content**:
  Indicates a successful request **without** a response body being sent.

The openEO API often uses the following HTTP status codes for failed requests: 

- **400 Bad request**: The back-end responds with this error code whenever the error has its origin on client side and no other HTTP status code in the 400 range is suitable.

- **401 Unauthorized**:
  The client **did not** provide any authorization details (usually using the Authorization header), but authorization is required for this request to be processed.

- **403 Forbidden**:
  The client **did** provide authorization details (usually using the Authorization header), but the provided credentials or the authorization token is invalid or has expired.

- **404 Not Found**:
  The resource specified by the path does not exist, i.e. one of the the resources belonging to the specified identifiers are not available at the back-end. *Note:* Unsupported endpoints *must* use HTTP status code 501.

- **500 Internal Server Error**:
  The error has its origin on server side and no other status code in the 500 range is suitable.

- **501 Not implemented**:
  An endpoint is specified in the openEO API, but is not supported.


If a HTTP status code in the 400 range is returned, the client *should not* repeat the request without modifications. For HTTP status code in the 500 range, the client *may* repeat the same request later.

All HTTP status codes defined in RFC 7231 in the 400 and 500 ranges can be used as openEO error code in addition to the most used status codes mentioned here. Responding with openEO error codes 400 and 500 *should* be avoided in favor of any more specific standardized or proprietary openEO error code.

### General error codes (xxx)


| openEO Error Code | Description           | Message                      | HTTP Status Code |
| ------- | ---------------------------- | ---------------- | ---------------- |
| 404    | To be used if the value of a path parameter is invalid, i.e. the requested resource is not available. *Note:* Unsupported endpoints *must* use code 501. | Not Found. | 404             |
| 501 | The back-end responds with this error code whenever an endpoint is specified in the openEO API, but is not supported. | Not implemented. | 501             |
| 503 |  | Service unavailable. | 503            |
| 601     |  | Parameter **X** is invalid.  | 400              |
| 611     | Invalid or unsupported CRS specified. | Invalid CRS specified. | 400              |
| 612     |  | Coordinate is out of bounds. | 400              |

### Capabilities (11xx)

None yet.

### Data and process discovery (12xx)

None yet.

### UDFs (13xx)

| openEO Error Code | Description | Message                                 | HTTP Status Code |
| ----------------- | ----------- | --------------------------------------- | ---------------- |
| 1301              |             | UDF programming language not supported. | 400 / 404        |
| 1302              |             | UDF type not supported.                 | 400 / 404        |

### File Handling (14xx)

| openEO Error Code | Description                                              | Message                  | HTTP Status Code |
| ----------------- | -------------------------------------------------------- | ------------------------ | ---------------- |
| 1401              | Server couldn't store file due to various reasons.       | Unable to store file.    | 500              |
| 1402              | The storage quota has been exceeded by the user.         | Insufficient Storage.    | 500              |
| 1410              | File format, file extension or mime type is not allowed. | File type not allowed.   | 400              |
| 1411              | File exceeds allowed maximum file size.                  | File size it too large.  | 400              |
| 1412              | The content of the file is invalid.                      | File content is invalid. | 400              |
| 1413              | The file is locked by a running job or another process.  | File is locked.          | 400              |


### Process graphs (2xxx)

| openEO Error Code | Description | Message                                                      | HTTP Status Code |
| ----------------- | ----------- | ------------------------------------------------------------ | ---------------- |
| 2001              |             | No process graph specified.                                  | 400              |
| 2002              |             | Process graph structure is invalid.                          | 400              |
| 2003              |             | The array **X** contains values of multiple types.           | 400              |
| 2101              |             | Process **X** is not supported.                              | 400              |
| 2102              |             | Process argument **X** is not supported.                     | 400              |
| 2103              |             | Invalid value **Y** for the process argument **X** specified. | 400              |
| 2104              |             | Required process argument **X** is missing.                  | 400              |

### Jobs (3xxx) 

| openEO Error Code | Description                                                  | Message                                                      | HTTP Status Code |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------- |
| 3001              |                                                              | Output format not supported.                                 | 400              |
| 3002              |                                                              | Output format argument **X** is not supported.               | 400              |
| 3003              |                                                              | Invalid value **Y** for the output format argument **X** specified. | 400              |
| 3101              | The batch job is currently running and the back-end is not able to delete it. |                                                              | 400              |

### Authorization, user content and billing (401-403, 4xxx)

| openEO Error Code | Description                                                  | Message                                  | HTTP Status Code |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------- | ---------------- |
| 401               | The back-end responds with this error code whenever the HTTP status code 401 is appropriate (see above) and no other openEO error code in the 4000 range is suitable. | Unauthorized.                            | 401              |
| 402               | The credits required to fulfil the request are insufficient. | Payment required.                        | 402              |
| 403               | The back-end responds with this error code whenever the HTTP status code 403 is appropriate (see above) and no other openEO error code in the 4000 range is suitable. | Forbidden.                               | 403              |
| 4001              | The specified password is not considered secure by the policy of the back-end provider or no password was given at all. The user needs to specify a different password to proceed. | Password does not meet the requirements. | 400              |
| 4031              | Invalid authentication scheme (e.g. Bearer).                 |                                          | 403              |
| 4032              | Authorization token invalid or expired.                      |                                          | 403              |
| 4033              |                                                              | Credentials are not correct.             | 403              |

### Web services (5xxx)

| openEO Error Code | Description               | Message                                                      | HTTP Status Code |
| ----------------- | ------------------------- | ------------------------------------------------------------ | ---------------- |
| 5001              |                           | Service type is not supported.                               | 400              |
| 5101              | Invalid job id specified. | Job does not exist.                                          | 400              |
| 5102              |                           | Service argument **X** is not supported.                     | 400              |
| 5103              |                           | Invalid value **Y** for the service argument **X** specified. | 400              |
| 5104              |                           | Required service argument **X** is missing.                  | 400              |
