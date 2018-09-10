# Processes

A process is an operation that performs a specific task on a set of parameters and returns a result. It's definition includes a name, a set of parameters, a return type, a set of possible errors or exceptions and some other metadata. In openEO they are used to build a chain of processes (process graph), which can be applied to EO datasets to derive your own findings from the data.

To define new processes, back-end providers should know:

* The name is the identifier for the process and MUST never contain a forward slash `/`. 
* Each parameter has a name and the content follows a schema.
* The content returned by a process also follows a schema.
* The schema usually defines the data type and a format according to JSON schema. There are openEO specific formats defined below.

## openEO specific formats

| Format Name | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| `eodata`    | A proprietary way to pass the processed data from one process to another. |

!!! note
    These formats are still evolving and will likely change with the definition of the openEO processes for openEO API version 0.4.

## Core Processes

There are some processes that we define to be core processes that are pre-defined and back-ends should follow these specifications to be interoperable. Not all processes need to be implemented by all back-ends.

See the **[process reference](processreference.md)** for pre-defined processes.

!!! note
    Currently, there are only few defined processes. Those are only meant as an example how future documentation of processes may look like.