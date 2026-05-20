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
Currently, as for version 7.2, EcosimPro and PROOSIS support the exporting and importing of the following:

| FMI version | Interface Type | Import | Export |
| :--- | --- | --- | --- |
| 1.0 | Any | No | No |
| 2.0 | ME | No | Yes |
|  | CS | Yes | Yes |
| 3.0 | ME | No | No |
|  | CS | Yes | Yes |
|  | SE | No | No |

*******************************************************************************************

Also, it is worth noting, that some of the new multiple functionalities introduced with FMI 3.0 are not yet available for FMUS generated with EcosimPro/PROOSIS or when importing thrid party FMUs. Here is a table with the current FMI 3.0 functionalities and their availability either when exporting or importing FMUs:

| Functionality | Import | Export |
| :--- |  --- | --- |
| Terminals |  No | No |
| Icons |  No | No |
| Clocks |  Yes | No |
| Integer and Float Types |  Yes | Yes |
| Binary type |  Yes | No |
| Array variables |  Yes | No |
| Structural parameters |  Yes | No |
| Adjoint derivatives |  Yes | No |
| Build configuration files |  No | No |
| Early return |  Yes | No |
| Event Mode |  Yes | No |
| Intermediate Update Mode | No | No |

It is worth mentioning that the lack of support for many of the new FMI 3.0 capabilities is simply because EcosimPro and PROOSIS do not internally use, or benefit from the use of many of them, such as Clocks, Binary variables, Early return, etc. Some others, such as Icons, Terminals and Array variables are currently being evaluated for future updates.

In the case of models imported from third-party sources, we have crafted our master library (COMM_FMI) with as much flexibility as possible to handle almost all possible functionalities and use cases referenced in the FMI 3.0 standard. Nevertheless, some of them still remain unsupported, either for having a lesser relevance when manipulating models (Icons, Terminals, Build configuration files) or because of strong limitations when trying to implement them with our current approach (Intermediate Update Mode).

This repository does not cover the generation and manipulation of FMUs within our software. For that, you can check our documentation and our FMI examples toolkit (COMM_FMI), included with all program releases. 



# Provided FMUs for testing and validation

The following systems are all modeled and exported to FMU in EcosimPor/PROOSIS for the purpose of validation and testing of our capabilities or for others to use them as a tool to validate their own FMi masters.

<details>
<summary> AircraftGear </summary>
  
Aircraft arrester gear system example: Simulation of one of the system used to halt an aircraft landing on a runway (used for ZONE statement demonstration)

These are the expected results with initial values of:
**y3 = 0.**
**y3' = 0.**
**y2 = 0.**
**y2' = 0.**
**x = 0.**
**x' = 60.96**

<img src="/img/results/aircraftGear/aircraft_gear_1.svg"  width="1000"/>

<img src="/img/results/aircraftGear/aircraft_gear_2.svg"  width="1000"/>

<img src="/img/results/aircraftGear/aircraft_gear_3.svg"  width="1000"/>


</details>

<details>
<summary> BouncingBall </summary>

Bouncing ball example: Simulation of a rubber ball which, dropped from a certain height, bounces successively on the ground until it stops (used for WHEN statement demonstration)

The results expected when starting from initial values of **h=10** and **h'=0** are:

<img src="/img/results/bouncingBall/bouncingBall.svg"  width="1000"/>

</details>

<details>
<summary> DiodeBridge </summary>

A diode bridge conected to a circuit as represented by the following diagram:

<img src="/img/components/diodeBridge.svg"  width="1000"/>

The expected results with default settings are as follows:

<img src="/img/results/diodeBridge/diodeBridge_1.svg"  width="1000"/>

<img src="/img/results/diodeBridge/diodeBridge_2.svg"  width="1000"/>

</details>
