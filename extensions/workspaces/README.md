# Workspaces Extension

The Workspace Extension to the openEO API provides an interface for connecting external file storage such as cloud buckets to openEO back-end implementations.

This opens the possibility to register such a file storage system as a data source for new collections, so-called "User Collections".
Additionally, batch job results can be stored on such file storage systems.

- Version: **0.1.0**
- Stability: **experimental**
- [OpenAPI document](openapi.yaml)
- Conformance class: `https://api.openeo.org/extensions/workspaces/0.1.0`

**Note:** This document only documents the additions to the specification.
Extensions can not change or break existing behavior of the openEO API.

The Workspace API is inspired by the [EOEPCA Workspace API](https://github.com/EOEPCA/rm-workspace-api) with regards to workspace management. The User Collections are not aligned with EOEPCA.