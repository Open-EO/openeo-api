# Cross-Origin Resource Sharing (CORS)

> Cross-origin resource sharing (CORS) is a mechanism that allows restricted resources [...] on a web page to be requested from another domain outside the domain from which the first resource was served. [...]
> CORS defines a way in which a browser and server can interact to determine whether or not it is safe to allow the cross-origin request. It allows for more freedom and functionality than purely same-origin requests, but is more secure than simply allowing all cross-origin requests.

Source: [https://en.wikipedia.org/wiki/Cross-origin_resource_sharing](https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)

openEO-based back-ends are usually hosted on a different domain / host than the client that is requesting data from the back-end. Therefore most requests to the back-end are blocked by all modern browsers. This leads to the problem that the JavaScript library (and the Web Editor) can't access any back-end. Therefore, all back-end providers SHOULD support CORS. Without supporting CORS users can't access the back-end with browser-based clients, i.e. the [JavaScript client](https://github.com/Open-EO/openeo-js-client). [CORS is a recommendation of the W3C organization.](https://www.w3.org/TR/cors/) The following chapters will explain how back-end providers can implement CORS support.

## 1. Supporting the OPTIONS method

All endpoints must respond to the `OPTIONS` HTTP method. This is a response for the preflight requests made by the browsers. It needs to respond with a status code of `204` and send the HTTP headers shown in the table below. No body needs to be provided.

| Name                             | Description                                                  | Example |
| -------------------------------- | ------------------------------------------------------------ | ------- |
| Access-Control-Allow-Origin      | Allowed origin for the request, including protocol, host and port. It is RECOMMENDED to return the value of the request's origin header. If no `Origin` is sent to the back-end CORS headers SHOULD NOT be sent at all. | `http://client.isp.com:80` |
| Access-Control-Allow-Credentials | If authorization is implemented by the back-end the value MUST be `true`. | `true` |
| Access-Control-Allow-Headers     | Comma-separated list of HTTP headers allowed to be send. MUST contain at least `Authorization` if authorization is implemented by the back-end. | ` Authorization, Content-Type` |
| Access-Control-Allow-Methods     | Comma-separated list of HTTP methods allowed to be requested. Back-ends MUST list all implemented HTTP methods for the endpoint here. | `OPTIONS, GET, POST, PATCH, PUT, DELETE` |
| Access-Control-Expose-Headers    | Some endpoints send non-safelisted HTTP response headers such as `OpenEO-Identifier` and `OpenEO-Costs`. All headers except `Cache-Control`, `Content-Language`, `Content-Type`, `Expires`, `Last-Modified` and `Pragma` must be listed in this header. Currently, the openEO API requires at least the following headers to be listed: `Location, OpenEO-Identifier, OpenEO-Costs`. | `Location, OpenEO-Identifier, OpenEO-Costs` |
| Content-Type                     | SHOULD return the content type delivered by the request that the permission is requested for. | `application/json` |

### Example request and response

Request:

``` http
OPTIONS /api/v1/jobs HTTP/1.1
Host: openeo.cloudprovider.com
Origin: http://client.org:8080
Access-Control-Request-Method: POST 
Access-Control-Request-Headers: Authorization, Content-Type
```

Response:

``` http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://client.org:8080
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: OPTIONS, GET, POST, PATCH, PUT, DELETE
Access-Control-Allow-Headers: Authorization, Content-Type
Content-Type: application/json
```

## 2. Sending CORS headers

The following headers MUST be included with every response:

| Name                             | Description                                                  | Example |
| -------------------------------- | ------------------------------------------------------------ | ------- |
| Access-Control-Allow-Origin      | Allowed origin for the request, including protocol, host and port. It is RECOMMENDED to return the value of the request's origin header. If no `Origin` is sent to the back-end CORS headers SHOULD NOT be sent at all. | `http://client.isp.com:80` |
| Access-Control-Allow-Credentials | If authorization is implemented by the back-end the value MUST be `true`. | `true` |
| Access-Control-Expose-Headers    | Some endpoints send non-safelisted HTTP response headers such as `OpenEO-Identifier` and `OpenEO-Costs`. All headers except `Cache-Control`, `Content-Language`, `Content-Type`, `Expires`, `Last-Modified` and `Pragma` must be listed in this header. Currently, the openEO API requires at least the following headers to be listed: `Location, OpenEO-Identifier, OpenEO-Costs`. | `Location, OpenEO-Identifier, OpenEO-Costs` |


**Tip**: Most server can send the required headers and the responses to the OPTIONS requests globally. Otherwise you may want to use a proxy server to add the headers and OPTIONS responses.