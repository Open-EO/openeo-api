# API Development Guidelines

To provide the smoothest possible experience, it's important to have these APIs follow consistent design guidelines, thus making using them easy and intuitive.

## Language

### Language

Generally, English language MUST be used for all names, documentation etc.

In the specification the key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in [RFC 2119](http://tools.ietf.org/html/rfc2119).

### Casing

Unless otherwise stated the API works case sensitive.

All names SHOULD be written in snake case, i.e. words are separated with one underscore character (_) and no spaces, with all letters lowercased. Example: `hello_world`. This applies particularly to endpoints and JSON property names. HTTP header fields follow their respective casing conventions, e.g. `Content-Type` or `OpenEO-Costs`, despite being case-insensitive according to [RFC 7230](https://tools.ietf.org/html/rfc7230#section-3.2).

## Technical requirements

### HTTP

The API developed by the openEO project uses [HTTP REST](https://en.wikipedia.org/wiki/Representational_state_transfer) [Level 2](https://martinfowler.com/articles/richardsonMaturityModel.html#level2) for communication between client and back-end server.

Public APIs MUST be available via HTTPS only and all inbound calls MUST be HTTPS. 

#### Verbs

Endpoints SHOULD use meaningful HTTP verbs (e.g. GET, POST, PUT, PATCH, DELETE).

If there is a need to transfer big chunks of data via GET requests, POST requests MAY be used as a replacement as they support to send data via request body.

Unless otherwise stated, PATCH requests are only defined to work on the direct (first-level) children of the full JSON object. Therefore, changing a property on a deeper level of the full JSON object always requires to send the whole JSON object defined by the first-level property.

#### Resource naming

Naming of endpoints SHOULD follow the REST principles. Therefore, endpoints SHOULD be centered around resources. Resource identifiers MUST be named with a noun in plural form except for single actions that can not be modelled with the regular HTTP verbs. Single actions MUST be single endpoint with a single HTTP verb (POST is RECOMMENDED) and no other endpoints beneath it.

#### Cross-Origin Resource Sharing (CORS)

All back-end providers SHOULD support CORS. More information can be found in the [corresponding section](cors.md).

#### Status codes and error handling

The success of requests MUST be indicated using [HTTP status codes](https://tools.ietf.org/html/rfc7231#section-6) according to [RFC 7231](https://tools.ietf.org/html/rfc7231). More information can be found in the section about [status und error handling](errors.md).

### Requests and response formats

#### JSON

Web-based communication, especially when a mobile or other low-bandwidth client is involved, has moved quickly in the direction of JSON for a variety of reasons, including its tendency to be lighter weight and its ease of consumption with JavaScript-based clients. Therefore, services SHOULD use JSON as the default encoding. Other response formats can be requested using [Content Negotiation](https://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html).

Clients and servers MUST NOT rely on the order in which properties appears in JSON responses. When supported by the service, clients MAY request that array elements be returned in a specific order.

Collections SHOULD NOT include nested JSON objects if those information can be requested from the individual resources.

#### Temporal data

Date, time, intervals and durations MUST be formatted based on ISO 8601 or any profile ([RFC 3339](https://www.ietf.org/rfc/rfc3339) is strongly recommended) if there is an appropriate encoding available in the standard. All temporal data MUST by specified based on the Gregorian calendar.
