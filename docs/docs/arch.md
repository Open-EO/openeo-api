# Architecture

The OpenEO core API defines a language how clients communicate to back-ends in order to analyze large Earth observation datasets. The API will be implemented by drivers for specific back-ends. Some first architecture considerations are listed below.

1. Each back-end runs its own API instance including the specific back-end driver. There is no API instance that runs more than one driver.
2. Clients in R, Python, and JavaScript connect to the API over HTTP.
3. API instances can run on back-end servers or additional intermediate layers, which then communicate to back-ends in a back-end specific way.
4. Back-ends may add functionality and extend the core API wherever there is need.


![Architecture](arch.png)


# Microservices



| Microservice  | Description  |
|---|---|
| API Information | This microservice reports on the capabilities of the back-end, i.e. which API endpoints are implemented, which authentication methods are supported, and whether and how UDFs can be executed at the back-end. |
| Data Discovery  | Describes which datasets and image collections are available at the backend.  |
| Process Discovery  | Provides services to find out which processes a back-end provides, i.e., what users can do with the available data.  |
| Job Management  | Organizes and manages jobs that run processes on back-ends |
| Download  | Services to download data and job results e.g. as WCS or WMTS service. |
| User Data Management  | Manage user content and accounting  |
