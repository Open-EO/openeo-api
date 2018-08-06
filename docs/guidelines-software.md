# Software Development Guidelines

This document describes guidelines for software developers, written for the [openEO](http://openeo.org) project.
Since the openEO infrastructure will encompasses several programming languages and software environments, this document does not prescribe particular tools or platforms but rather focuses on general principles and methods behind them.

1. License: all software developed in the openEO project and published on the [openEO GitHub](http://github.com/open-eo/) organisation shall be licensed under the [Apache 2.0 license](LICENSE). If software repositories deviate from this, or contain code or other artifacts that deviates from this, this shall be described in the `README.md` file.
2. Location: Official openEO software is developed under the [openEO GitHub organisation](https://github.com/open-EO/).
3. Proof-of-concept versus sustainable: each repository shall indicate its status: either _proof-of-concept_, or _sustainable_. Proof-of-concept code is meant to work but comes without quality assurance. Software repositories with proof-of-concept developments shall clearly say so in the first paragraph of the `README.md` file.
4. Sustainable code should undergo standard [quality checks](#software-quality-guidelines), and point out its [documentation](#software-documentation-guidelines).
5. Sustainable code shall undergo [code review](#software-review); no direct commits to master; any commit shall come in the form of a PR, commit after review.
6. Sustainable code shall be written in a [Test-driven manner](test-driven-development), and repositories shall at the top of their `README.md` give indication of the degree to which code is covered by tests.
7. [Continuous integration](#continuous-integration) shall be used to indicate code currently passes its test on CI platforms.
8. A [Code of conduct](codeofconduct.md) describes the rules and constraints to developers and contributors.
9. Version numbers of sustainable software releases shall follow [Semantic Versioning 2.0.0](http://semver.org).  

## Software quality guidelines

* software shall be written in such a way that another person can understand its intention
* comment lines shall be used sparsely, but effectively
* reuse of unstable or esoteric libraries shall be avoided

## Software documentation guidelines

Software documentation shall include:
* installation instructions
* usage instructions
* explain in detail the intention of the software
* pointers to reference documents explaining overarching concepts 

Each repository's `README.md` shall point to the documentation.

Reference documentation shall be written using well-defined reference documentation language, such as [RFC2119](https://tools.ietf.org/html/rfc2119) or [arc42](http://arc42.org), and refer to the definitions used.

## Software review

* sustainable software development shall take place by always having two persons involved in a change to the master branch: individuals push to branches, pull request indicate readiness to be taken up in the master branch, a second developer reviews the pull request before merging it into the master branch.
* software review discussions shall be intelligible for external developers, and serve as implicit documentation of development decisions taken

## Test-driven development

Software shall be developed in a test-driven fashion, meaning that while the code is written, tests are developed that verify, to a reasonable extent, the correctness of the code. Tools such as [codecov.io](https://codecov.io/) to automatically indicate the amount of code covered by tests, and code that is not covered by tests shall be used in combination with a continuous integration framework.

## Continuous integration

Repositories containing running software shall use an appropriate continuous integration platform, such as [Travis CI](https://travis-ci.org/) or similar, to show whether the current build passes all checks. This helps understand contributors that the software passes tests on an independent platform, and may give insights in the way the software is compiled, deployed and tested.

## Additional guidelines

There a specific guidelines for [client library development](guidelines-clients.md) and [API development](guidelines-api.md).