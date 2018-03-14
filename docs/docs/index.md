# OpenEO - Core Concepts and API Reference

_Work in progress, please contribute by adding [issues](https://github.com/Open-EO/openeo-api/issues)._

openEO develops an open API that connects clients like R, Python and JavaScript to big Earth observation cloud back-ends in a simple and unified way.

The following pages introduce the core concepts of the project. Make sure to introduce yourself to the major technical terms used in the openEO project by reading the [glossary](glossary.md).

The OpenEO Core API defines a [RESTful API](apireference.md) that lets cloud back-ends with large Earth observation datasets communicate with front end analysis applications in an interoperable way. This documentation describes important API concepts and design decisions and gives a complete [API reference documentation](apireference.md).

As an overview, the OpenEO API specifies how to

- discover which Earth observation data and processes are available at cloud back-ends,
- execute (chained) processes on back-ends, 
- run [user-defined functions](udfs.md) (UDFs) on back-ends where UDFs can be exposed to the data in different ways, 
- download (intermediate) results as web services, and
- manage user content including accounting.


The API is defined as an [OpenAPI 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) (formerly known as Swagger 2.0) JSON file.




![OpenEO logo](openeo_logo.png)	

_[OpenEO](https://openeo.org), A Common, Open Source Interface between Earth Observation Data Infrastructures and Front-End Applications is a H2020 project funded under call EO-2-2017: EO Big Data Shift, under proposal number 776242. It will run from Oct 2017 to Sept 2020._