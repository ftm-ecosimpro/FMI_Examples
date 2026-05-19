<img src="/img/logo/ecosimPro_logo_texto.svg"  width="500"/>

EcosimPro is a first class modelling and simulation software for modeling 0D or 1D multidisciplinary continuous-discrete systems and any kind of system based on differential-algebraic equations (DAE) and discrete events. Although originally developed for space applications, namely to assist in the modelling of the Environmental and Control Life Support Systems (ECLSS) for European Space Agency (ESA)’s HERMES and COLUMBUS projects, due to the nature of its broad, wide-ranging capabilities it is now being used in many other fields as system simulation software. The first version of EcosimPro was released in 1993.

EcosimPro has been designed to carry out steady and transient studies, as an optimization and design tool that helps the engineer to improve any kind of system modeled with equations (0D and 1D). It also provides a highly intuitive graphics environment that facilitates its use in creating physical models based on schematic views.

Engineers find it to be an extremely intuitive tool, since it has been designed based on real industry needs. Its GUI provides tools for creating easy to identify icons that represent components and which can be connected to other icons using ports of the same type. EcosimPro carefully extracts the complexity of the mathematical model and solves the final equations.

*******************************************************************************************

<img src="/img/logo/proosis_logo_texto.svg"  width="500"/>

PROOSIS is a standalone, multi‑platform, object‑oriented environment designed for high-fidelity simulation of gas turbine engines and integrated aerospace systems. As an extension of EcosimPro, it adds aeronautics-specific tools like performance map handling, multipoint design, and support for SAE-standard “customer decks”, etc.

All models generated with EcosimPro or PROOSIS can be exported using international standards such as FMI (co-simulation and model exchange), OPC-UA, S-Function, Excel, Matlab,Web Service, Python, etc. This gives a big flexibility for reusing any model in other environments.

*******************************************************************************************

This repository aims to provide a source of material for the use of the FMI estandard with EcosimPro and PROOSIS. The material here is provided "as is" for the only purpose of testing and validating the compatibility of EcosimPro and PROOSIS FMU capabilities when interacting with third-party tools. The material here provided is not validated, provided or supervised in any way by the Modellica Association.

*******************************************************************************************

For any doubt, bug or suggestion, please contact with our support team. (support@ecosimpro.com)

*******************************************************************************************

# Generation and manipulation of FMUs in EcosimPro/PROOSIS
Currently, EcosimPro and PROOSIS support the exporting and importing of the following:

| FMI version | Interface Type | Import | Export |
| :--- | --- | --- | --- |
| 1.0 | Any | No | No |
| 2.0 | ME | No | Yes |
|  | CS | Yes | Yes |
| 3.0 | ME | No | Yes |
|  | CS | Yes | Yes |
|  | SE | No | No |

This repository does not cover the generation and manipulation of FMUs within our software. For that, you can check our documentation and our FMI examples toolkit (COMM_FMI), included with all program releases. 



