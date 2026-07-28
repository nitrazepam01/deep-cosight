> OCR by deepseek-ai/DeepSeek-OCR | 22 pages

### Page 1

value harnessing quality aboard the sailing yar.ISO 26262-7:2011 defines qualitative requirements (continuous and discrete) that can be satisfied by the product or the system that uses the product. The term is used to derive safety requirements for systems or components of a vehicle.Qualitative requirements can be used to satisfy continuous requirements of safety life assurance for quantitative requirements, whether tangible (e.g., safety measurements and installations) or intangible (e.g., behavior and mental images related to safety requirements).Qualitative requirements can be reconstituted by using questionnaires to validate verification activities in satisfying requirements, measurement requirements for verifying safety requirements, and other methods of measurement verification.ISO 26032 defines the term “qualitative techniques” and concludes that a process of gathering information with the purpose of specification is the fundamental analytical method. The qualitative information can be gathered by questionnaires and interviews. The term is used to derive other requirements for the product or the system with which the product is connected, expressed as functions or terms expressing qualitative needs or safety requirements, necessary for qualifying product or system requirements.Qualitative requirements are requirements for qualitative requirements, which can be represented in text format as qualitative terms (qualitative declinations), which can be formulated as a qualifier, requirements for quantitative requirements, which are derived by evaluation of qualitative requirements expressed as necessary requirements for quantitative requirements.ISO 26030 is the software engineering terminology developed by the Organization for the Advancement of Structured Information Standards (OASIS) based on the classifications from ISO 11000 and ISO 11785. ISO 26030 defines the term “qualification processes” in detail, and identifies five classes of generic software approaches “from qualitative solutions to the alternative solutions.

### Page 2

entitlement to such content.For each method, the degree of recommendation to use the corresponding method depends on the ASIL and is categorized as follows:

— “+” indicates that the method is highly recommended for the identified ASIL;
— “+” indicates that the method is recommended for the identified ASIL;
— “o” indicates that the method has no recommendation for or against its usage for the identified ASIL.

**4.3 ASIL-dependent requirements and recommendations**

The requirements or recommendations of each subclause shall be complied with for ASIL A, B, C and D, if not stated otherwise. These requirements and recommendations refer to the ASIL of the safety goal. If ASIL decomposition has been performed at an earlier stage of development, in accordance with ISO 26262-9:2011, Clause 5, the ASIL resulting from the decomposition shall be complied with.

If an ASIL is given in parentheses in ISO 26262, the corresponding subclause shall be considered as a recommendation rather than a requirement for this ASIL. This has no link with the parenthesis notation related to ASIL decomposition.

**5 Production**

**5.1 Objectives**

The first objective of this clause is to develop and maintain a production process for safety-related elements or items that are intended to be installed in road vehicles.

The second objective is to achieve functional safety during the production process by the relevant manufacturer or the person or organisation responsible for the process (vehicle manufacturer, supplier, sub-supplier, etc.).

**5.2 General**

The compliance with safety-related special characteristics of items or elements during their production, determined during the development phases, is necessary to achieve functional safety. Examples of such safety-related special characteristics are specific process parameters (e.g. temperature range or fastening torque), material characteristics, production tolerance, or configuration.

This phase defines requirements ensuring that functional safety is achieved during the production process by including these safety-related special characteristics in production planning and control.

The requirements and recommendations of this clause apply to the production and installation in the vehicle of items, systems or elements.

**5.3 Inputs to this clause**

**5.3.1 Prerequisites**

The following information shall be available:

— specification of requirements related to production, operation, service and decommissioning in accordance with ISO 26262-4:2011, 7.5.4, and ISO 26262-5:2011, 7.5.4;
— specification of dedicated measures for hardware in accordance with ISO 26262-5:2011, 9.5.2; and
— release for production report in accordance with ISO 26262-4:2011, 11.5.1.

### Page 3

# Section: Summary

## 5.3.2 Further supporting information

The following information can be considered:

- production plan (from external source); and
- production control plan (from external source).

# Section: Requirements and recommendations

## 5.4 Requirements and recommendations

### 5.4.1 Production planning

#### 5.4.1.1 The production process shall be planned by evaluating the item and by considering the following:

a) the requirements for production;

**EXAMPLE** Assembly instructions (e.g. the calibration and setup of a sensor); safety-related special characteristics (e.g. the tolerance for the selection of elements).

b) the conditions for storage, transport and handling of hardware elements;

**EXAMPLE** Allowed storage time for the element.

c) the approved configurations defined in the release for production documentation;

d) the lessons learned on the capability from previously released production plans;

e) the suitability of the production process, means of production, tools and test equipment concerning the safety-related special characteristics; and

f) the competences of the personnel.

#### 5.4.1.2 The production plan shall describe the production steps, sequence and methods required to achieve the functional safety of the item, system or element. It shall include:

a) the production process flow and instructions;

b) the production tools and means;

c) the implementation of the traceability measures; and

**EXAMPLE** Labelling for the element.

d) if applicable, the implementation of dedicated measures applying to hardware parts and specified during hardware development in accordance with ISO 26262-5:2011, 9.4.2.4.

**NOTE** The production process also includes processes or operations required to rework the item.

#### 5.4.1.3 A procedure shall be defined to ensure that the correct embedded software and the associated calibration data are loaded into the ECUs as part of the production process.

**EXAMPLE 1** The use of a checksum, so that the checksum of the loaded executable and configuration data is compared to the correct checksum for this particular model and vehicle configuration.

**EXAMPLE 2** Read back of the part number from the software loaded into the ECUs and comparison with the target part number for that specific vehicle from the bill of materials; as well as read back and comparison of the loaded calibration data with the calibration data for that specific vehicle from the bill of materials.

### Page 4

- The use of Windows® 8 Standard, Professional, Enterprise, or Ultimate.
- The loading of the product settings only after the main licence window has closed.
- The use of three monitors connection for video function and service function.
- The installation of a power-saving tool.
- A software tool password automatically up to 15 digits long.

The license uses multilingual character series.
The license presents a duration of 10 months for Linux notebooks of the CE mark.
The license offers an 50 months warranty for Linux notebooks of the CE mark.
The license offers the security tracking associations, including SÃ©quÃ© PSèv Ã!).

### Page 7

### Page 8

}}\\ \qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\text{\small{NOTE}}}\end{cases} 

EXAMPLE Specification of an error logging function in the ECU to ease diagnosis during service.
6.4.2 Operation, service (maintenance and repair), and decommissioning
6.4.2.1 The field monitoring process for functional safety incidents that relate to the item shall be implemented as planned in accordance with ISO 26262-2:2011, 7.4.2.4, in order to:
a) provide the field data that shall be analysed to detect the presence of any functional safety issues and, if found, trigger actions that address those issues, and
b) provide the evidence required by the proven in use argument if it is intended to use this argument in accordance with ISO 26262-8:2011, Clause 14.
6.4.2.2 The maintenance, repair and decommissioning of the item, its systems or its elements should be conducted and documented in accordance with the maintenance plan and the maintenance and repair instructions.
NOTE This includes the application of repair and maintenance procedures and the provision of either paper or electronic documentation of this application.
6.4.2.3 The supply of parts and their storage and transport shall be implemented as planned in accordance with 6.4.1.3.
6.4.2.4 If changes to the item for subsequent production are initiated by operation, field monitoring, maintenance, repair or decommissioning, a change management process in accordance with ISO 26262-8:2011, Clause 8, shall be complied with.

6.5 Work products

6.5.1 Safety-related content of the maintenance plan resulting from requirement 6.4.1.1, 6.4.1.2, 6.4.1.3.

6.5.2 Repair instructions resulting from requirement 6.4.1.3.

6.5.3 Safety-related content of the information made available to the user resulting from requirement 6.4.1.4.

6.5.4 Instructions regarding field observations resulting from requirement 6.4.2.1.

6.5.5 Safety-related content of the instructions for decommissioning resulting from requirement 6.4.1.5.

6.5.6 If applicable, specification of requirements relating to operation, service and decommissioning at system, hardware or software development level resulting from requirement 6.4.1.6.

NOTE This specification can be appended to the relevant documentation of the corresponding phases.

### Page 9

}}}{i: 1;l:2 } 1.5 $\tau$.");
console.log('---
### Info
</pre></body>
</html>');
console.timeEnd('Info');console.log('Total time: ' + (Date.now() - InfoStart) + 'ms');
console.timeEND('Info');

Annex A
(informative)

**Overview on and document flow of production and operation**

Table A.1 provides an overview on objectives, prerequisites and work products of the particular phases of production and operation.

**Table A.1 — Overview of production and operation**

| Clause                  | Objectives                                        | Prerequisites                                                                                       | Work products                                                                                           |

|                          |                                                                                                                                  |                                                                  •  5.5.4 If applicable, requirements specification on the producibility at system, hardware or software development level resulting from requirement 5.4.1.7 and appended to the relevant documentation of the corresponding phases. |
|                          |                                                                                                                                  |                                                                  •  5.5.5 Assessment report for capability of the production process, resulting from requirement 5.4.2.2 and 5.4.3.3.                  |
| **Operation, service (maintenance and repair) and decommissioning** | The objective of this clause is to specify the customer information, maintenance and repair instructions, and disassembly instructions regarding the item, system or element in order to maintain the functional safety over the lifecycle of the vehicle. | Requirements specification for production, operation, service and decommissioning in accordance with ISO 26262-5:2011, 7.5.4                                                                                                        |                                                                                          |
|                          |                                                                                                                                  |                                                                  •  6.5.1 Safety-related content of the maintenance plan resulting from requirement 6.4.1.1, 6.4.1.2, 6.4.1.3.                                                  |
|                          |                                                                                                                                  |                                                                  •  6.5.2 Repair instructions resulting from requirement 6.4.1.3.                                                    |
|                          |                                                                                                                                  |                                                                  •  6.5.3 Safety-related content of the information made available to the user resulting from requirement 6.4.1.4.                                            |
|                          |                                                                                                                                  |                                                                  •  6.5.4 Instructions regarding field observations resulting from requirement 6.4.2.1.                            |
|                          |                                                                                                                                  |                                                                  •  6.5.5 Safety-related content of the instructions for decommissioning resulting from requirement 6.4.1.5.                                       |
|                          |                                                                                                                                  |                                                                  •  6.5.6 If applicable, requirements specification relating to operation, service and decommissioning at system, hardware or software development level resulting from requirement 6.4.1.6.   |

© ISO 2011 – All rights reserved

### Page 10

VD

## Bibliography

[1] ISO/TS 16949, Quality management systems — Particular requirements for the application of ISO 9001:2008 for automotive production and relevant service part organizations

[2] IEC 61508 (all parts), Functional safety of electrical/electronic/programmable electronic safety-related systems

### Page 11

):

  primarily intended for in-use service, and for scrutineering purposes. System correctness will be a significant impact on final application.

### Page 12

)end of the second page. In the Green's Index, there are two case numbers with the 이상 in Chinese characters. For The British Standards Institution, it is BS. This is followed by the classification number of the standard, which starts with "2" on the page and end with "0". The version of the standard is "-a1":04:2015