# openEO - Concepts and API Reference

***Note:*** *The specification is currently still an early version, with the potential for some major things to change. The core is now fleshed out, so everybody is encouraged to try it out and give feedback (for example by adding [issues](https://github.com/Open-EO/openeo-api/issues)). But the goal is to actually be able to act on that feedback, which will mean changes are quite possible.*

openEO develops an open application programming interface (API) that connects clients like R, Python and JavaScript to big Earth observation cloud back-ends in a simple and unified way. The acronym openEO contracts two concepts:

- **open**: used here in the context of open source software; open source software is available in source code form, and can be freely modified and redistributed; the openEO project will create open source software, reusable under a liberal open source license (Apache 2.0)
- **EO**: Earth observation

Jointly, the openEO targets the processing and analysis of Earth observation data. The main objectives of the project are the following concepts:

- **Simplicity**: nowadays, many end-users use Python or R to analyse data and JavaScript to develop web applications; analysing large amounts of EO imagery should be equally simple, and seamlessly integrate with existing workflows
- **Unification**: current EO cloud back-ends all have [a different API](https://www.r-spatial.org/2016/11/29/openeo.html), making EO data analysis hard to validate and reproduce and back-ends difficult to compare in terms of capability and costs, or to combine them in a joint analysis across back-ends. A unified API can resolve many of these problems.

The following pages introduce the core concepts of the project. Make sure to introduce yourself to the major technical terms used in the openEO project by reading the [glossary](glossary.md).

The openEO API defines a [HTTP API](apireference.md) that lets cloud back-ends with large Earth observation datasets communicate with front end analysis applications in an interoperable way. This documentation describes important API concepts and design decisions and gives a complete [API reference documentation](apireference.md).

As an overview, the openEO API specifies how to

- discover which Earth observation [data](collections.md) and [processes](processes.md) are available at cloud back-ends,
- execute [(chained) processes](processgraphs.md) on back-ends, 
- run [user-defined functions](udfs.md) (UDFs) on back-ends where UDFs can be exposed to the data in different ways, 
- download (intermediate) results, and
- manage  [user content including billing](usermanagement.md).


The API is defined as an [OpenAPI 3.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md) JSON file.




![openEO logo](img/openeo_logo.png)	

_[openEO](https://openeo.org), A Common, Open Source Interface between Earth Observation Data Infrastructures and Front-End Applications is a H2020 project funded under call EO-2-2017: EO Big Data Shift, under proposal number 776242. It will run from Oct 2017 to Sept 2020._

_This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 776242. The contents of this website reflects only the authors’ view; the European Commission is not responsible for any use that may be made of the information it provides._
