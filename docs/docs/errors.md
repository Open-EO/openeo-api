# Error handling

Errors are handled using HTTP status codes. In general an error is communicated with status codes between 400 and 599. If the API responds with a status code between 100 and 399 the back-end indicates that the request could be handled successfully.

The openEO API uses the following status codes: 

* **200 OK**:
  Indicates a successful request **with** a response body being sent.

* **204 No Content**:
  Indicates a successful request **without** a response body being sent.

* **400 Bad Request**:
  The back-end responds with this error code whenever the error has its origin on client side. Errors can be invalid query parameters, or invalid request body content etc. The client **should not** repeat the request without modifications.

  *The response body should contain a JSON error object as specified below.*

* **401 Unauthorized**:
  The client **did not** provide any authorization details (usually using the Authorization header), but authorization is required for this request to be processed.

* **403 Forbidden**:
  The client **did** provide authorization details (usually using the Authorization header), but the provided credentials or the authorization token is invalid or has expired.

* **404 Not Found**:

  The back-end responds with this error code whenever the resource specified by the path does not exist, i.e. one of the the resources belonging to the specified identifiers are not available at the back-end.

* **405 Method Not Allowed**:
  Used for [CORS](cors.md) responses only to indicate the HTTP method requested is not allowed to be accessed.

* **500 Internal Server Error**:
  The back-end responds with this error code whenever the error has its origin on server side. The error is never the client’s fault and therefore it is reasonable for the client to retry the exact same request that triggered this response.
  *The response body should contain a JSON error object as specified below.*

## JSON error object

A JSON error object should be sent with all responses that have a status code of 400 or 500.

```
{
  "code": 123,
  "message": "A sample error message.",
  "translations": {
    "de": "Eine Beispiel-Fehlermeldung.",
    "fr": "Un exemple de message d'erreur."
  }
}
```

Sending `code` and `message` is required. 

* The `code` is either one of the standardized error codes below or a custom error code with a number greater than 10000.
* The `message` must be sent in English language and explain what the client might need to change or what the server is struggling with.
* The `translations` object is optional and can contain as many translations for the error message as available. The key must be a language code according to [ISO-639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes). The value is the error message itself. An English translation with the key `en` is ignored in favor of the value of `message`.

## Common error codes (xxx)

All HTTP status code in the 400 and 500 range can be used in addition to this. 

| Code    | Description                                | Message                                                      | HTTP Status |
| ------- | ------------------------------------------ | ------------------------------------------------------------ | ----------- |
| 0       | Unknown error, should never be used.       | Unknown error.                                               | All         |
| 4**xx** | Client side errors, see HTTP status codes. | [See HTTP status codes.](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_errors) | 400         |
| 5**xx** | Server side errors, see HTTP status codes. | [See HTTP status codes.](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#5xx_Server_errors) | 500         |
| 501     |                                            | Parameter **X** is invalid.                                  | 400         |
| 601     | Invalid or unsupported CRS specified.      | Invalid CRS specified.                                       | 400         |
| 602     |                                            | Coordinate is out of bounds.                                 | 400         |

### Capabilities (11xx)

None yet.

### Data and process discovery (12xx)

None yet.

### UDFs (13xx)

| Code | Description                             | Message | HTTP Status |
| ---- | --------------------------------------- | ------- | ----------- |
| 1301 | UDF programming language not supported. |         | 400         |
| 1302 | UDF type not supported.                 |         | 400         |

### File Handling (14xx)

| Code | Description                                              | Message                 | HTTP Status |
| ---- | -------------------------------------------------------- | ----------------------- | ----------- |
| 507  | The storage quota has been exceeded by the user.         | Insufficient Storage.   | 500         |
| 1401 | Server couldn't store file due to various reasons.       | Unable to store file.   | 500         |
| 1410 | File format, file extension or mime type is not allowed. | File type not allowed.  | 400         |
| 1411 | File exceeds allowed maximum file size.                  | File size it too large. | 400         |
| 1412 | The content of the file is invalid.                      | File content is invalid | 400         |
| 1413 | The file is locked by a running job or another process.  | File is locked.         | 400         |


### Process graphs (2xxx)

| Code | Description | Message                                                      | HTTP Status |
| ---- | ----------- | ------------------------------------------------------------ | ----------- |
| 2001 |             | No process graph specified.                                  | 400         |
| 2002 |             | Process graph structure is invalid.                          | 400         |
| 2003 |             | The array **X** contains values of multiple types.           | 400         |
| 2101 |             | Process **X** is not supported.                              | 400         |
| 2102 |             | Process argument **X** is not supported.                     | 400         |
| 2103 |             | Invalid value **Y** for the process argument **X** specified. | 400         |
| 2104 |             | Required process argument **X** is missing.                  | 400         |

### Jobs (3xxx) 

| Code | Description                                                  | Message                                                      | HTTP Status |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ----------- |
| 406  |                                                              | Format not supported                                         | 400         |
| 423  | The job is currently running and could not be canceled by the back-end. |                                                              | 400         |
| 410  | Job with specified identifier can't be resumed / has been canceled. | Job can't be resumed.                                        | 400         |
| 428  | Job with specified identifier is queued or is not running.   | Job is queued or not running.                                | 400         |
| 3001 |                                                              | Output format not supported.                                 | 400         |
| 3002 |                                                              | Output format argument **X** is not supported.               | 400         |
| 3003 |                                                              | Invalid value **Y** for the output format argument **X** specified. | 400         |

### Authorization, user content and billing (4xxx)

| Code | Description                                                  | Message                                  | HTTP Status |
| ---- | ------------------------------------------------------------ | ---------------------------------------- | ----------- |
| 4001 | Invalid authentication scheme (e.g. Bearer).                 |                                          | 400         |
| 4002 | Authorization token invalid or expired.                      |                                          | 400         |
| 4003 |                                                              | Credentials are not correct.             | 400         |
| 4001 | The specified password is not considered secure by the policy of the back-end provider or no password was given at all. The user needs to specify a different password to proceed. | Password does not meet the requirements. | 400         |

### Web services (5xxx)

| Code | Description               | Message                                                      | HTTP Status |
| ---- | ------------------------- | ------------------------------------------------------------ | ----------- |
| 5001 |                           | Service type is not supported.                               | 400         |
| 2101 | Invalid job id specified. | Job does not exist.                                          | 400         |
| 2102 |                           | Service argument **X** is not supported.                     | 400         |
| 2103 |                           | Invalid value **Y** for the service argument **X** specified. | 400         |
| 2104 |                           | Required service argument **X** is missing.                  | 400         |
