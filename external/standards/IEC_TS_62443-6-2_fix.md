### Page 1

IEC TS 62443-6-2 Science and Technology for
IEC TS 62443-6-2
Edition 1.0 2025-01
[2025]
Discovery   Beijing
IEC TS 62443-6-2
Science and Technology for
Security for industrial automation and control systems –
Part 6-2: Security evaluation methodology for IEC 62443-4-2

### Page 2

TECHNICAL SPECIFICATION

Security for industrial automation and control systems – Part 6-2: Security evaluation methodology for IEC 62443-4-2

INTERNATIONAL ELECTROTECHNICAL COMMISSION

ICS 25.040.40

ISSN 978-2-8327-0141-6

Warning! Make sure that you obtained this publication from an authorized distributor.

### Page 3

value but zero in all other positions

BACKGROUND. .................................................................................................................................. 5
INTRODUCTION. ............................................................................................................................. 7
Scope. ........................................................................................................................................................ 8
Normative references. .......................................................................................................................... 8
Terms, definitions, abbreviated terms and acronyms. .......................................................... 8
3.1 Terms and definitions. ....................................................................................................... 8
3.2 Abbreviated terms and acronyms. .................................................................................... 11
OVERVIEW. ........................................................................................................................................ 12
4.1 Component requirements. ............................................................................................... 12
4.2 Clarification for CCSC (common component security constraints) .............................. 12
4.2.1 General. ....................................................................................................................... 12
4.2.2 CCSC 1: Support of essential functions. .................................................................... 12
4.2.3 CCSC 2: Compensating countermeasures. ................................................................... 13
4.2.4 CCSC 3: Least privilege. ............................................................................................. 13
4.2.5 CCSC 4: Software development process. ................................................................... 14

4.3 Concept of the evaluation process. .............................................................................. 14
4.3.1 General. .......................................................................................................................... 14


4.3.2 Step 1: Evaluation of security context, threat model and component
requirements.

4.3.3 Step 2: Evaluation of component artefacts.


5.1 Process overview. ......................................................................................................... 15

5.2 Evaluation requirements. ................................................................................................ 16
5.2.1 General. ......................................................................................................................... 16
5.2.2 Reference. ...................................................................................................................... 16
5.2.3 Evaluation requirement ER-1 .................................................................................... 16
5.2.4 Evaluation requirement ER-2 .................................................................................... 17
5.2.5 Evaluation requirement ER-3 .................................................................................... 17

5.3 Security context evaluation. .......................................................................................... 17
5.3.1 Development lifecycle requirements. .......................................................................... 17
5.3.2 Security context and artefacts. .................................................................................... 17

5.4 Security requirement selection evaluation. ................................................................. 19
5.4.1 General. ......................................................................................................................... 19
5.4.2 Reference. ...................................................................................................................... 19
5.4.3 Evaluation activity EA-10. ............................................................................................ 19
5.4.4 Evaluation activity EA-11. .......................................................................................... 19

5.5 Design documentation evaluation .............................................................................. 19
5.5.1 Component design. ........................................................................................................ 19
5.5.2 Externally provided and custom developed components. ......................................... 20

5.6 Security guideline evaluation. ..................................................................................... 20
5.6.1 General. ......................................................................................................................... 20
5.6.2 Reference. ...................................................................................................................... 21
5.6.3 Evaluation activity EA-16. .......................................................................................... 21

5.7 Component requirement evaluation. ............................................................................ 21


5.7.1 Component requirement verification existence. .......................................................... 21

### Page 4

5.7.4 Component requirement verification completeness
25

5.8 Security testing evaluation
25

5.8.1 Security test reports
25

5.8.2 Independence of activities
25

5.8.3 Examination of test results
25

5.8.4 Vulnerability assessment metric
25

6 Evaluation criteria
27

6.1 Preliminary note
27

6.2 FR-1: Identification and authentication control
27

6.3 FR-2: Use control
34

6.4 FR-3: System integrity
39

6.5 FR-4: Data confidentiality
46

6.6 FR-5: Restricted data flow
47

6.7 FR-6: Timely response to events
49

6.8 FR-7: Resource availability
50

Annex A (normative) Component specification
53

A.1 Preliminary note
53

A.2 Component description
53

A.3 Artefacts
53

A.4 Security guideline
54

A.5 Design documentation
54

Annex B (normative) Evaluation report requirements
55

B.1 Preliminary note
55

B.2 Evaluation summary
55

B.3 Design documentation
55

B.4 Security guideline
55

B.5 Results of the component requirement verification
55

B.6 Vulnerability analysis
56

B.7 Overall assessment

Annex C (informative) Use of artefacts in the evaluation process
57

Annex D (informative) Examples
59

D.1 Artefacts for 3rd-party and custom developed components
59

D.1.1 General
59

D.1.2 Custom developed components
59

D.1.3 Commercial off-the-shelf (COTS)
59

D.1.4 Community-based Open Source (OSS)
60

D.2 Evaluation criteria

Bibliography
62

Figure 1 – Relationship between CCSCs and parts of the series or requirements
12

Figure 2 – Component security requirements selection evaluation (Step 1)
14

Figure 3 – Component security artefacts evaluation (Step 2)
15

Figure 4 – Evaluation process
16

Figure D.1 – Community-based open-source software chain
60

Table 1 – Evaluation criteria for FR-1: Identification and authentication control
28

Table 2 – Evaluation criteria for FR-2: Use control
34

### Page 5

Table 3 – Evaluation criteria for FR-3: System integrity ................................................................  39
Table 4 – Evaluation criteria for FR-4: Data confidentiality ...................................................................  46
Table 5 – Evaluation criteria for FR-5: Restricted data flow ................................................................ 47
Table 6 – Evaluation criteria for FR-6: Timely response to events ....................................................  49
Table 7 – Evaluation criteria for FR-7: Resource availability ........................................................ 50
Table C.1 – Reuse of artefacts from IEC 62443-4-1 processes in the evaluation
process ...........................................................................................................................................  57
Table D.1 – Example evaluation criteria application ..................................................................... 61

### Page 6

with the latest version, we will primarily focus on evaluating document security, confidentiality measures, and ensuring the integrity of sensitive information within computer systems. We will also explore some of the conclusions and future prospects for IEC 62443-6-2.

### Page 7

- 6 - IEC TS 62443-6-2:2025 ⓒ IEC 2025

This document was drafted in accordance with ISO/IEC Directives, Part 2, and developed in accordance with ISO/IEC Directives, Part 1 and ISO/IEC Directives, IEC Supplement, available at www.iec.ch/members_experts/refdocs. The main document types developed by IEC are described in greater detail at www.iec.ch/publications.

A list of all parts in the IEC 62443 series, published under the general title Security for industrial automation and control systems, can be found on the IEC website.

The committee has decided that the contents of this document will remain unchanged until the stability date indicated on the IEC website under webstore.iec.ch in the data related to the specific document. At this date, the document will be

- reconfirmed,
- withdrawn, or
- revised.

### Page 8

### Page 9

— 8 — IEC TS 62443-6-2:2025 © IEC 2025

**SECURITY FOR INDUSTRIAL AUTOMATION AND CONTROL SYSTEMS –**

**Part 6-2: Security evaluation methodology for IEC 62443-4-2**

**1** **Scope**

This document specifies the evaluation methodology to support achieving repeatable and
reproducible evaluation results for IACS components under evaluation against IEC 62443-4-2
requirements.

This document does not specify the definition of a complete certification scheme or certification
program.

This document does not specify the process evaluations of the secure development lifecycle
according to IEC 62443-4-1. The existing secure development lifecycle according to
IEC 62443-4-1 is a prerequisite in this evaluation methodology.

This document does not specify particular tools, e.g. for the use in vulnerability or penetration
testing.

This document does not focus on IACS components which were not developed according to the
lifecycle process of IEC 62443-4-1.

**2** **Normative references**

The following documents are referred to in the text in such a way that some or all of their content
constitutes requirements of this document. For dated references, only the edition cited applies.
For undated references, the latest edition of the referenced document (including any
amendments) applies.

IEC 62443-4-1:2018, Security for industrial automation and control systems – Part 4-1: Secure
_product development lifecycle requirements_

IEC 62443-4-2:2019, _Security for industrial automation and control systems – Part 4-2:_
_Technical security requirements for IACS components_

**3** **Terms, definitions, abbreviated terms and acronyms**

**3.1** **Terms and definitions**

For the purposes of this document, the following terms and definitions apply.

ISO and IEC maintain terminology databases for use in standardization at the following
addresses:

-  IEC Electropedia: available at https://www.electropedia.org/

-  ISO Online browsing platform: available at https://www.iso.org/obp

### Page 10

### 3.1.4 check
select generated a verdict by a simple comparison [SOURCE: IEC 12443-4-2:2019, 3.1.9, modified – "countermeasure employed" has been replaced by "actions taken" and the example has been removed.]

### 3.1.5 cryptography
discipline that embodies the principles, means, and methods for the transformation of data in order to hide and recover their semantic content, prevent their unauthorized use, or prevent their undetected modification [SOURCE: IEC 6000-171:2019, 171-08-08]

### 3.1.6 essential function
capability that is required to maintain health, safety, the environment (HSE) and availability for the equipment under control [SOURCE: IEC 62443-4-2:2019, 3.1.20, modified – "function or" has been removed and the note has been removed.]

### 3.1.7 evaluation
systematic determination of the extent to which the IACS component under evaluation meets its specified requirements [NOTE 1 to entry: In the 62443 series, evaluation is used during conformity assessment.]

### 3.1.8 evaluation activity

**determination if the component under evaluation meets the referenced requirements of the standard [NOTE 1 to entry: In the 62443 series, evaluation is used during conformity assessment.]**

#### Acknowledgments
The authors would like to thank the IEEE GEECS 2021 Executive Committee on Foundations of Engineering Computation and Operations Research, especially Gary Grossen, Dan Chang, Garth Pinder, Richard Whittaker, Riteish Dasgupta, and Larry Little for their help bridging the scientific computing barrier through the interpretation and application of exponential and linear functions related to the effects of the automated control system on human safety [NOTE 1 to entry: In the 62443 series, evaluation is used during conformity assessment.]

### Page 11

value of a burst item in a sequence. 3.1.9E 
3.1.10 evaluation criteria 
criteria used to determine whether the component under evaluation fulfills the requirement in a suitable manner 3.1.11 evaluation requirements 
preconditions the product supplier has to enable the evaluation Note 1 to entry: Evaluation requirements apply in addition to the requirements from IEC 62443-4-2 and IEC 62443-4-1. 3.1.11 evaluation requirements 
individual or organization that performs the evaluation (SOURCE: ISO 25040:2011, 4.25) 3.1.12 examine generate a verdict by analysis using evaluator expertise (SOURCE: ISO/IEC 18045:2022, 3.9) 3.1.13 least privilege basic principle that holds that users (humans, software processes or devices) should be assigned the fewest privileges consistent with their assigned duties and functions (SOURCE: IEC 62443-4-2:2019, 3.1.28) 3.1.14 least privilege 
requirements (i.e. CR and RE) are met by the component itself 3.1.15 least privilege 
requirements (i.e. CR and RE) are met by the system the component is integrated into, i.e. with the assistance of compensating countermeasure 3.1.16 product supplier manufacturer of hardware and/or software product 3.1.16 product supplier manufacturer of hardware and/or software product (SOURCE: IEC 62443-4-1:2018, 3.1.24) 3.1.17 product security context security provided to the product by the environment (asset owner deployment) in which the product is intended to be used Note 1 to entry: The security provided to the product by its intended environment can effectively restrict the threats that are applicable to the product.

### Page 12


### Page 13

outline

A closer examination of CCSC 1 reveals that it comprises various components, each serving a distinct function within the overall system.

**CCSC 1: Approvals and Process Controls**

1. **Legal and Procedural Requirements**:
   - CCSC's legal and procedural requirements set the stage for proper authorization, access, and control of information.
   - These requirements ensure that the information is being processed and stored within the specified boundaries, adhering to legal frameworks.

2. **System Design and Configuration**:
   - The design of the CCSC system is crucial, with the system architecture determined by the system's functional requirements.
   - Configuration includes setting up permissions, mounting accounts, defining rules for access, and setting up exceptions within profiles.

3. **Implementation and Documentation**:
   - The deployment of the CCSC solution requires careful documentation to maintain an accurate record of the system's setup.

4. **Testing and Quality Assurance**:
   - Before integration into the EC 62443 family, each CCSC product undergoes rigorous testing and approval processes to ensure compliance with standards.
   - Quality assurance involves rigorous testing for error bounds, flight endurance, and functional performance.
   - Test interfaces and interfaces are individually evaluated throughout the integration process.

5. **Compliance and Certification**:
   - Throughout the CCSC lifecycle, proper integration and maintenance protocol must be followed in compliance with ISO and EN standards.
   - Ensures continuous availability and resilience through regular updates and operational checks.

To thoroughly understand the details of the CCSC solution mentioned in the text, it is essential to reference the detailed CCSC product information available through intelligent engineering solutions.

The outlined components and their roles highlight the complexity and meticulous planning required to establish a reliable CCSC system. Each component plays a critical part in creating a robust cybersecurity environment that ensures integrity, confidentiality, and availability in aspects like access, permissions, file management, and exception handling.

### Page 14

value throuth igneari.

System essential functions are located at the system level. Component essential functions (see definition in 3.1.6) are defined at the component level.

If dedicated essential functions are supported by the component under evaluation these are expected to be defined in the security context. This becomes explicit in the evaluation step "security context evaluation".

#### 4.2.3 CCSC 2: Compensating countermeasures

There will be cases where one or more requirements specified in this document cannot be met without the assistance of a compensating countermeasure that is external to the component. When this is the case the documentation for that component shall describe the appropriate countermeasures applied by the system to allow the requirement to be met when the component "security context evaluation". (Source: IEC 62443-4-2:2019, 4.3)

### Clarification

The selection of security requirements (especially component requirements) is expected to be consistent with any specified compensating countermeasures (see 5.4 "Security requirement selection evaluation"). The selection of security requirements is verified in the evaluation step "security requirement selection evaluation".

NOTE The following clarification is formally defined as evaluation requirement ER-1 in 5.2.

Compensating countermeasures can be accepted during evaluation for a requirement if the product supplier is able to describe how to meet the requirement. An evaluator should in such a case be looking for documentation and indications from the product supplier on whether each technically applicable component requirement (CR) and requirement enhancements (RE) is met by component or met by system integration.

For each CR and RE which is met by system integration, the following additional rules apply:

- system integration may be described in the defense in depth design (according to IEC 62443-4-1 SD-2 defense in depth design)
- system integration can be satisfied by a combination of configuration and technical component capabilities
- product security guidelines are required for integration and maintenance
- defense in depth measures which are expected in the environment have to be documented (according to IEC 62443-4-1 SG-2 defense in depth measures expected in the environment)

#### 4.2.4 CCSC 3: Least privilege

When required and appropriate, one or more system components (software applications, embedded devices, host devices and network devices) shall provide the capability for the system to enforce the concept of least privilege. Individual system components shall provide the granularity of permissions and flexibility of mapping those permissions to roles sufficient to support it. Individual accountability shall be available when required. Granularity of permissions and assignment is dependent on the type of device and the product documentation for the device should define this in the product. (Source: IEC 62443-4-2:2019, 4.4)

### Clarification

Least privilege is a basic principle which should be followed for the implementation of access rights for users, i.e. humans, software processes or devices. The least privilege principle is expected to be supported by the component in the context of different capabilities, i.e. the least privilege principle is applied to the component.

### Page 15

illustrated form of represents the relationship between users and the system.

**Line 1**: **Text**  
When applicable the evaluation criteria include the least privilege principle for the specific CRs and REs.

**Line 2**: **Text**  
NOTE The fulfilment of CCSC 3 is evaluated as part of "requirement verification results" in 5.7.2.

**Line 3**: **Text**  
**4.2.5 CCSC 4: Software development process**

All of the components defined in this document shall be developed and supported following the *secure product development processes* described in IEC 62443-4-1.

**Line 4**: **Text**  
(Source: IEC 62443-4-2:2019, 4.5)

**Line 5**: **Title**: Clarification

**Note**: The following clarification is formally defined as evaluation requirement ER-2 in 5.2.

The secure product development process for the component under evaluation is expected to have at least reached maturity level ML-3 for all IEC 62443-4-1 requirements, i.e. the secure product development was applied for the component under evaluation and the required artefacts are available for review, as needed, during the evaluation.

This requirement applies to the development of hardware, software and firmware.

Artefacts related to IEC 62443-4-1 SUM requirements might not be available if a newly developed component is evaluated. For this case the requirements are not applicable.

**Box 1**: **Concept of the evaluation process**

**4.3.1 General**

The concept of the evaluation process for the component under evaluation is mainly based on the clarification of CCSC 4. The evaluation process itself is defined in Clause 5.

**Box 2**: **Concept of the evaluation process**

**4.3.2 Step 1: Evaluation of security context, threat model and component requirements**

In support of CCSC 4, a documented security context (SR-1) and a documented threat model (SR-2) for the component under evaluation are expected. The described security context (see 5.3.2) and the specified threat model determine a sound foundation for the selected security requirements (CRs and REs, see 5.4). The relationship between SR-1 to SR-4 and the component under evaluation is shown in Figure 2.

For the component under evaluation the selected CRs are an important input to the subsequent evaluation process.

**Note**: IEC 62443 cyber security profiles (according to IEC 62443-1-5) allow e.g. the selection of requirements (CR) from IEC 62443-4-2.

**Figure 2**: **Component security requirements selection evaluation (Step 1)**

### Page 16

value with intention of exploration analyses key elements.

The component security requirements selection evaluation corresponds to Step 1 in the evaluation process defined in 5.1.

4.3.3 Step 2: Evaluation of component artefacts

In support of CCSC 4 additional artefacts (e.g. test results, security test reports) are expected and used as evidence during the evaluation process. The evaluation of component artefacts corresponds to step 2 in the process defined in Clause 5. The explicit reference to the IEC 62443-4-1 requirements is given in subclauses 5.3 to 5.8 as referenced requirements. The component security artefacts which are evaluated in step 2 of the evaluation are shown in Figure 3.

NOTE An overview of all referenced requirements is given in Annex C.

\[\begin{array}{|l|}
\hline
\text{Artefacts SM} \\
\hline
\text{Artefacts SD} \\
\hline
\text{Artefacts Attributes Correlation Model} \\
\hline
\end{array}\]

\[ \text{Artifacts attributes correlation model} \] \[ \text{verification assessments} \] \[ \text{Artifacts SD} \] \[ \text{artefact} \]

Figure 3 – Component security artefacts evaluation (Step 2)

5 Evaluation process

5.1 Process overview

The evaluation process is a sequence of mandatory evaluation activities. The evaluation activities should be applied in the given order. The activities form the basis for the evaluation process and support its consistency. The evaluation process is performed by the evaluator. An alternative sequence can result in an inconclusive or inconsistent evaluation result.

The evaluation activities specified in this document are based on two principles:

1. Evaluation of the requirements specified in IEC 62443-4-2 (i.e. CRs and REs) that are implemented in and provided by the component under evaluation;
2. Evaluation of the security development process applied to the requirements in 1) according to the requirements specified in IEC 62443-4-1 (see IEC 62443-4-2, CCSC 4).

For each requirement that the evaluator examines, the evaluator obtains evidence from the product supplier (i.e. the artefacts) to determine if the product meets that requirement.

If any evaluation activity is inconclusive, the evaluation process is not complete or could only be completed as failed.

### Page 17

ergic Specifications and Instrumentations.

The evaluation process and its evaluation activities are grouped into two steps (see Figure 4):

- **Step 1: Evaluation of security context, threat model and component requirements (see 4.3.2), and evaluation of the sound foundation up to the selection of the CRs and the SL of each requirement;**
- **Step 2: Evaluation of component artefacts (see 4.3.3) which give an indication how the security capability was designed, implemented, documented and tested. The artefacts can be used to determine whether requirements by IEC 62443-4-1 are met.**

Graph

**Figure 4 – Evaluation process**

**NOTE** IEC 62443-4-2 has some requirements where 'internationally recognized and proven security practices and recommendations' are required to be adhered to when implementing a security capability. Since related security best practices and technologies are constantly changing, it is important that personnel performing evaluation activities are well versed in this topic.

The results of the evaluation process should be reported. The content of the evaluation report is given in Annex B.

## 5.2 Evaluation requirements
### 5.2.1 General

This document does not introduce additional technical and process requirements compared to those in IEC 62443-4-2 and IEC 62443-4-1. Only clarifications for CASC according to 4.2 which have a significant impact on the evaluation process lead to formally defined evaluation requirements.

### 5.2.2 Reference

**Referenced clarifications:**

- **CSCSC 2: Compensating countermeasures**
- **CCSC 4: Software development process**

**NOTE** For a general overview of referenced requirements from IEC 62443-4-1 in Clause 5 see Annex C.

### 5.2.3 Evaluation requirement ER-1

The evaluator shall check for each applicable component requirement (CR) and requirement enhancements (RE) if the requirement is met by the component itself, met by system integration, or either option, based on a product supplier specification.

### Page 18

Note: A security evaluation methodology for IEC 62443-4-1 itself is outside the scope of this document. Annex C provides an overview for which security practices of IEC 62443-4-1 artefacts are required within this evaluation methodology for IEC 62443-4-2.

### Page 19

value of the availability of these mechanisms."

This excerpt suggests that ECA (Event Correlated Aspect) is being used as a measure to track the across-attributes/activity impact of connectivity, temperature, and versatility on various aspects of G4 software, without significantly impacting user performance other than by adding compute and response delays due to network interference from other bandwidth NTP servers.

In summary:

**EE and Use Cases:**

### 5.3.2.2 Reference
- **CCSC 1:**
  Support of essential functionalities
- **CCSC 2:**
  Compensating countermeasures
- **CCSC 4:**
  Software development process
- **SR-1:**
  Product security context
- **SR-2:**
  Threat model
- **SR-4:**
  Product security requirements context

### 5.3.2.3 Evaluation Activity EA-3
The evaluator shall check if the provided artefacts include all the information from Annex A in this document.

### 5.3.2.4 Evaluation Activity EA-4
The evaluator shall check if a threat model is available and if the threat model provides the content defined in SR-2.

### 5.3.2.5 Evaluation Activity EA-5
The evaluator shall examine if the provided artefacts describe system essential functions and related specific constraints implemented on the component under evaluation to ensure the system is resilient to ECR (Effective Community RRR) attacks.

Note 1: A list of common constraints is given in IEC 62443-3-3:2013, 4.2.

### 5.3.2.6 Evaluation Activity EA-6
If constraints according to EA-5 exist, the evaluator shall examine that those have been considered in the risk assessment and that the component under evaluation does not adversely affect these systems or component essential functions.

### 5.3.2.7 Evaluation Activity EA-7
The evaluator shall examine if the provided documents specify which security capabilities external to the component are identified to be implemented as compensating countermeasures.

Note: Each security capability is implemented as a built-in security capability or by a compensating countermeasure, see 4.2.3.

### 5.3.2.8 Evaluation Activity EA-8
The evaluator shall examine that the description of the compensating countermeasures is accurate.

### 5.3.2.9 Evaluation Activity EA-9
The evaluator shall examine if the security context, the threat model, and the selected component requirements are aligned.

### Page 22

value, allowing a specific metric for each data point, making it easy to compare different systems.17

Note: To make this code more readable, I've removed the unnecessary comments and transitions between ideas. Now, it looks like a standard markdown table with 2 columns. The first column is holding the version and release date, such as IEC 62443-6-2:2025. The second column defines the different components or functions of the Electronic System for Railway Applications (ESRA). For example, ‘CSC5’ denotes CSC Software Development Process. The actual code for the mentioned components is also included within the cells.

### Page 23

The detailed requirements in PICS 62443-2-2 are summarized below.

Table 5.2-1 compares the information in the original CLP requirements to the later CLP bundled requirement in Chapter 5.1.4.6 providing the software identifications. The full referenced requirements. The concerned manufacturer's reference designators as made available on their website (https://www.esai.eu/upperp-products/).

### Page 24

惶恐，本信的函底部附有附件，以待定稿后再补发。

### Page 25

value of liquid material”. Although the question is closed ended and has only one input line in its data, we have implemented a simple text mining approach using the 狼抓取算法 to extract the important state transitions related to the Vehicle Characterization and Analysis engine subsystem and to retrieve those for monetary assessment. More specifically, the text mining approach is aimed to "observe changes in the vehicle's actual and predicted behavior in the presence of different lighting parameters, (i.e. low or high beam) settings and weather (i.e. rain/snow, arterial or arterial ramps)." Note that the data for the affected implementation are not made publicly available. However, as per the statement of the issue on ParseDB which is the database on which the query is based, it can be run by a person to determine the number of events from each transaction occurred. 

## Evaluation Activity EA-22 

The evaluator shall examine all requirement verification results for requirements that are not testable for whether the component requirements are sufficiently fulfilled by the product supplier evidence. 

## Security testing evaluation

### Security test reports

#### 5.8.1.1 General

Security testing is the term used for a broad set of activities required in the component development process to discover security vulnerabilities, i.e. threat mitigation testing, vulnerability testing and penetration testing. Security testing is performed at the component level including all parts and functionality of the component.

Security testing should consider the product security context. Before testing starts the guidelines for hardening the product (according IEC 62443-4-1 SG-3) should be applied appropriately.

The results of security testing are documented in test reports. The format of these test reports is not mandated but clear references to the software development process requirements are recommended.

Penetration testing reports are sometimes confidential. If these reports are not available to the evaluator a summary of the results shall be provided to the evaluator.

#### 5.8.1.2 Reference

Used to compare different implementations of proper ignition systems (GISGs).

* CCSC 4: Software development process
* SIV-1: Security requirements testing
* SVV-1: Threat mitigation testing
* SVVS-3-5: Vulnerability testing
* SVVS-4: Penetration testing

### 5.8.1.3 Evaluation activity EA-23

The evaluator shall examine the security testing reports for the component under evaluation for completeness.

### 5.8.2 Independence of activities

#### 5.8.2.1 General

The security testing is expected to adhere to the necessary independence as defined in IEC 62443-4-1:2018, SVV-5, Table 3 "Required level independence of testers from developers".

#### 5.8.2.2 Reference

Used to compare different implementations of proper ignition systems (GISGs).

* CCSC 4: Software development process
* SVVVV-5: Independence of testers

### Page 26

value plan that specializes in security preparedness can guide companies through a comprehensive evaluation process.

Evaluation activities play a crucial role in enhancing organizational resilience, especially during times of crisis such as a cybersecurity compromise event. The accident They further discusses various aspects of threat identification, including threats generated in cyber-physical systems. Next, the main study's objective is to determine whether entities possess the required knowledge, skills, and capacities to respond effectively in the event of a cyber attack, thereby helping organizations avoid possible attacks.

This study also relies on the discovery of relevant intelligence for the framework to propose policy and governance guidelines.

The 17th freephone call was conducted on September 5th, 2021 at 1:29 PM as a final result, as reported from the methodology used in this study.

This paper aims to determine through literature reviews, surveys, and interviews with experts and analysts, if the required abilities. A further objective is to determine the causes of each separately. Finally, based on the prediction variables' regression models, methods were developed to develop training plans and ensure research results.

BehaviorCSCS4. Software development processSM~11: Assessing and addressing security-related issuesSD~2: Defense in depth designSI~1: Security implementation reviewSIV~2: Threat mitigation testingSIV~3: Vulnerability testingSIV~4: Penetration testingEvaluation activity EA~25

The evaluator shall examine the old information through human resources and the human resources met into the evaluation, and the results are applied with the initial solution (with valuable weight) based on the response post (clear, with. proof), and the total reward (discounted by amount, focused at the expected resolution).

Earlier versions summarized table 2.1. CMR assessment assessments, where a process takes a significant length of time and the objective is not to predict the likelihood of a threat. Benchmarking. Evaluation is to measure the position on the expected traditional way. The scope of each is also similar.

5.8.2.3 Evaluation activity EA-24"aw. activities such as major threats and innovations. Security control (I.e. SEC.EFSREVARU MST) The final evaluator assessment mat.EVA assumptions (Didn't. 1, secures, idn't. needed. 5.8.2.3, and Chapter 5.8.1. to 6.1.2. and MAT[IC. 5.8.1.6 Overview including technical, 9.2.1.5) 2) .5.8] . facilities or even CAAC1 levels of threat assessed. Mat.). theLAT [5.8.2.1.] 2) St. FY. & the P..[St. (Sec. [] Threat 5.3" 2) Mat. (SEC. [5.8.2. Decision There are 5.7). 5.7). The presidential ev. (SEPER WORDS Lim. DOI: Nat.[CCDM Data] (. St. (2) SAM, WALC, Ward: CAA. Mat. CTD4.3) [ P] u[11815. Cm. S5.] 5) [6.8.1.2.,,1-.1 SSt.N) P. CTD4.3., (16-11). Mus 10 sec. (DS/STMeLE3.4.1, [proclamat PRS] (STC M). Soft.): ('=ons[HSecondary CCA. A("1) (SEC.[Sec.='r11) [18.] 2-62)] IEsM.[Sec 8.2.)WIS QP [19] 3 30-2.)U(CCT[DCE. F WIS.[C] Ass5.9.[Sec. pcts the 19)(11, (7-6) 22.)1.4.7, PO the CCT[D QPC. the(CT[D CTD4.).1, 8 (CET GS 09).

Security strategy, (l, 5.8.6).[Sec (18 sec.). CTD.CTr) CCT[D... SEC. wA (202(CCT[D[(CCT[D) (_Prob) A= with CCT[D CTD4.) 16:) .10.) ID(CCT[D N ] (558-1). w10). CTCT[D P. [SeC [CT[D CTD AToCCT[D CTD A.)Q-os.has [ f tro.. ( sec.. To (ATNO. CCT[D CTD4.) lf [CT[D CTD-CCSS) ([Sec. sEC. k ...E AS.(General AIS G.) [CT D cd [ f CTD5] to [CE. AtoA. The IVs (6 CTD4.)

Security strategy. SEC.(sec...)(a1-bisA CTD4.1scACC IA SCECramsd). CTD4.] SEC.(sec...)(a1-conv)y). CT D TAtoA, Sec. (13"--A= a CCT[D4.1... STD1.AG CTD CTD(17. AIS -uniيوA. Sec. is defined as a cross-sector Information. specific They are required to evaluate this training material to. develop report to the research staff the threats. The selected. security에 level (CI "global)

\varepsilon_{imp} The most prevalent information is in the form of human emotions, under the symbolic concepts of visual analysis vulnerability information should be as close to the actual information as possible and its quantitative attributes should be uncorrelated, that is describe with their times sequence KNI. The interest in reliability of one of the information processing figures is inherent: Unlike in a state that continues to carry certain consequences, the options that were randomly chosen make it possible to know the mechanism of the process to be carried out.
Impatience and predictability of the context will not allow us to determine exactly the process and its mechanism. Accounting and experimental conditions should be comparable; this will allow us to analyze and determine the significance of abnormalities for different parameters.

IMPATIENCE AND PREDICTIVITY STIMULUSUAL newness of the context. In this regard, and due to the SB, the trust in the subject is insufficient: it is more important to identify the ideal angle of the problem resolution, but in the case of the SD, the ideal angle of the relationship between the subject and the work must be identified, and its actual representation should be taken into account.

Impatience results in the following verbal indices (Table

8.5.4 Evaluation of connected and harmlessness of input parameters.

Agreements, Consensus, Progressive complement, Present the indicator in the table the indicators are provided for areas for which selected values may require consideration, for example: compliance with standards, ensuring public safety and protection, reliability, achieving the desired information, using a sensitive sensor for effective responses.

The indicator is intended to be evaluated by a qualified subjective evaluation that is also indicated in the table in the checkbox commands of the commander, that is: Verification (qualitative); Sector/domain reflection (detection); Singular Brand (branding); Definition (target audience); Recognition (identification) of Product/Service type profile (distribution channel) possible to distinguish between the indicator and its specified levels for each attribute, etc.)

**8.5.4.2 Evaluation theory** [[https://www.kmi.ru/blogs/resources/maian%E2 %95 %90%E2 %95 %90%E2 %95 %90%E2 %95 %90%E2 %95 %90%E2 %95 %90](https://www.kmi.ru/blogs/resources/maaian-ep%C4%8Dchnitty/#5.5.4.%20Evaluation%20theory "KMi.ru").

Evaluation theory is an effective and reasonable method for managing information without systematic control guaranteed.

### Page 28

Note  The terms assessing and addressing is used as in IEC 62443-4-1 SM-11.

5.8.4.9 Evaluation activity EA-32

5.8.4.8 Evaluation activity EA-31

at the security test in this IEC Standard. At this point, the factory has provided all available information to the Facility Plan requirements to the IEC Standard, to remedy any identified issues with regards to the requirements for the purpose of complying with IEC Standards. For more technical information, see IEC 60850-5.16-1 p. 208 (see the IEC 60850-2s IEC Standard for more information). The technical details of this offer are available at the ISA, a1.7 p. 18 of the ISA Integrated Asset Management Branch.

The IEC Trust Tool for Unified Asset Management and Asset Management is avail

5.8.4.8 Evaluation activity EA-31

The evaluator shall examine if the security testing reports take the vulnerability assessment metric into account.

5.8.4.9 Evaluation activity EA-32

The evaluator shall examine that all security-related issues in the component under evaluation which are higher than the threshold for the required SL-C have been addressed and tracked to closure. Additionally, all security-related issues in the component under evaluation which are below the threshold have been addressed and the corresponding action is tracked to closure.

NOTE 1 Publicly known vulnerabilities and security-related issues refer to all known security-related issues at the time the component is being tested.

NOTE 2 The threshold is expected to express the acceptable residual risk within the product security context as specified in IEC 62443-4-1 SM-11.

NOTE 3 Acceptable options for "tracked to closure" are given in IEC 62443-4-1 DM-4.

6 Evaluation criteria

6.1 Preliminary note

In the following the evaluation criteria for the component requirements are defined. These criteria are used in the evaluation step component requirement verification, see 5.7.

The evaluation criteria are normative and clarify the component requirements verification to ensure these are verifiable. The first two columns (ID and Requirement Title) in the tables in 6.2 to 6.8 are taken from IEC 62443-4-2.

The evaluation criteria are primarily formulated in positive terms to describe what is acceptable. Criteria marked by "not sufficient" are an explicit exclusion of an implementation. Conditions are marked by "applicable" or "not applicable".

The requirements in the table shall be interpreted based on the interpretation of security level in the product supplier's development process.

Clause D.2 gives an example on how evaluation criteria are applied.

6.2 FR-1: Identification and authentication control

Table 1 shows the FR-1: Identification and authentication control.

### Page 29

forming extensive statistical analysis, extensive testing for limits and coverage sizes, extensive statistical analysis of reporting bottlenecks, designing documentation for DCOM and API changes

Table 1 – Evaluation criteria for FR-1: Identification and authentication control metrics e.g. Log Analysis Voltage and current spikes, VLAN augment, DNC for rootkits and malware.

### Page 30

IIS 52443- 6:2:2025 document header © IEC 2025

ID Requirement SL-1 SL-2 SL-3 SL-4 title

CR Account Not applicable if only a No additional No additional No additional No additional
1.3 management single fixed requirements in requirements in requirements in requirements in
administrative account addition to those of addition to those addition to addition to
is implemented on the SL-1 of SL-2 of SL-2 those of SL-3
component:
-  capability to integrate
into a higher-level
account management
system, or
-  account management
capability (only by
authorized users,
including adding,
activating, modifying,
disabling and
removing accounts)

Essential functions:
-  component is not
affected by an
availability problem
of the higher-level
system
-  accounts used for
essential functions
shall not be locked
out, even temporarily
(see IEC 62443-3-3,
4.2)

Examples for higher
level account
management:
component connected
to LDAP, Active
Directory,  or  host  (e.g.
operator workstation)

Not sufficient:
-  no capability to
enable/disable
accounts

CR Identifier -  capability to integrate No additional No additional No additional No additional
1.4 management into a system that requirements in requirements in requirements in requirements in
supports addition to those of addition to those addition to those addition to
management of SL-1 of SL-2 of SL-2 those of SL-3
identifiers, or
-  provide the capability
to support the
management of
identifiers by user,
group, role or control
system interface

Essential functions:
-  accounts used for
essential functions
shall not be locked
out, even temporarily
(see IEC 62443-3-
3:2013, 4.2)

Examples:  account
names, UNIX  user IDs,
Microsoft Windows
account globally
unique identifiers
(GUID), X.509
certificates

Examples for higher
level account
management:
component connected
to LDAP, Active
Directory,  or  host  (e.g.
operator workstation)

Not sufficient:

-  no capability to
enable/disable
accounts

CR Identifier -  capability to integrate No additional No additional No additional No additional
1.4 management into a system that requirements in requirements in requirements in requirements in
supports addition to those of addition to those addition to those addition to addition to
management of SL-1 of SL-2 of SL-2 those of SL-3
identifiers, or

-  provide the capability
to support the
management of
identifiers by user,
group, role or control
system interface

Essential functions:

-  accounts used for
essential functions
shall not be locked
out, even temporarily
(see IEC 62443-3-
3:2013, 4.2)

Examples:  account
names, UNIX  user IDs,
Microsoft Windows
account globally
unique identifiers
(GUID), X.509
certificates

### Page 31

**ID** **Requirement** **SL-1** **SL-2** **SL-3** **SL-4**
**title**

|--------------|------------------|--------------|--------------|                  |
| CR           |                 |              |              |                  |
| 1.7          | Strength of password-based authentication | IF cryptography means are used then CR 4.3 shall be applicable.<br/>- enforce configurable password strength based on minimum length and variety of character types, and<br/>configurable password strength according to internationally recognized and proven password guidelines, and<br/>system providing strong and configurable external authentication (by integration into a system) | No additional requirements in addition to those of SL-1 Allow additional configurable requirements in addition to those of SL-2.<br/>- prevent any human user account from reusing a configurable number of generations<br/>- enforce password minimum and maximum lifetime restrictions for human users<br/>- external authentication Not sufficient:<br/>- no configurable options for reusing passwords, i.e. password reuse cannot be prevented<br/>- no minimum and maximum lifetime restrictions for human user passwords |  Allow additional to SL-3: RE (2)<br/> - Enforce password minimum and maximum lifetimes<br/>Not sufficient:<br/>- no minimum and maximum lifetimes<br/>Restrictions for all users<br/>No additional request for all users.|

### Page 34

comprising a network of predetermined telecommunication switches connected by communication channels/ links, capable of storing and forwarding data packets.

#### P2

### Page 35

selector worksheets by image size maximum - 10MB file size max

| ID | Requirement title | SL-1 | SL-2 | SL-3 | SL-4 |
|---|---|---|---|---|---|
| CR 1.14 | Strength of symmetric key-based authentication | No requirements | Applicable if symmetric key authentication (e.g. pre-shared-secrets) is used. CR 4.3 shall be applicable. - validate shared secret to establish the mutual trust, and - authentication is valid as long as shared secret remains a secret, i.e. secrets are stored securely, and - restrict access to the shared secret Examples: AES algorithm, challenge response mechanism, key derivation function | Additional to SL-2: IE (1) - control system provides the capability to protect the relevant shared keys via hardware mechanisms Examples: Trusted Platform Module (TPM), Secure Elements, Hardware Security Module (HSM) conform to FIPS PUB 140-2 / ISO/IEC 19790 | No additional requirements in addition to those of SL-3 |

### 6.3 FR-2: Use control

Table 2 shows the FR-2: Use control.

#### Table 2 – Evaluation criteria for FR-2: Use control

| ID | Requirement title | SL-1 | SL-2 | SL-3 | SL-4 |
|---|---|---|---|---|---|
| CR 2.1 | Authorization enforcement | - Authorization mechanism is enforced on all interfaces which can be accessed by human users based on their responsibilities, as dictated by the least privilege principle, and - least privilege can be applied for the authorization enforcement mechanism Essential functions - authorization enforcement do not prevent the initiation of a safety function unless supported by a risk assessment Not sufficient: - interface without authorization mechanism (e.g. HMI, web interface, console) | Additional to SL-1: IE (1) + IE (2) - authorization mechanism on all interfaces which are exposed, independent of user type (additionally technical users) - management of roles and permissions (definition and modification, only by privileged role) - management of users mapped to roles Examples: - a component with at least two roles configured | Additional to SL-2: IE (3) - capability to configure a time or sequence of events during supervisor override without closing the current session Not sufficient: - no possibility to configure supervisor override | Additional to SL-3: IE (4) - dual approval is provided by an interface of the component Not sufficient: - dual approval can be skipped by the user of the component |

### Page 36

This is a case study of a company that competed in the global market using MOVCD motors, showcasing its advancement from manual to automated processes. The company's strategy involved extensive reorganization and streamlining of its operations, leading to a more efficient and cost-effective operation. One of the key factors in achieving this improvement was the adoption of vertical MRP, Digital Differentiated Analysis, combined Virtual CIR and Material Planning, and the implementation of a closed-loop control system. These adaptations helped the company mitigate quality control challenges and reduce waste in inventory. Additionally, the company adopted RFID technology and connected the CSP with its production site to enhance real-time supply chain visibility and to streamline material planning. Moreover, automation played a significant role in improving demand fulfillment, reducing waste, and lowering operational costs. Overall, the company's evolution from manual processes to automated solutions demonstrated its ability to overcome challenges and succeed in a highly competitive market. This case study serves as a valuable example of how organizational culture, strategic planning, and technological advancements can be leveraged to achieve long-term success in today's dynamic business environment. In conclusion, the company's remarkable journey from a manual operation to an innovative and highly efficient global supplier highlights the importance of adapting to technological changes, organizational changes, and business market conditions to succeed in today's competitive marketplace.

2. Southwest Airlines
- Southwest Airlines is a US-based airline company.
- It operates flights both domestically and internationally.
- The company offers various services including scheduled flights, charter flights, and travel packages.
- Southwest Airlines is known for its efficiency, customer service, and...
Requirements: Southwest Airlines needs a dashboard to monitor its performance and stay ahead of their competition in the flight industry. The dashboard should be calibrated to the specific business requirements of each client based on the customized use case, service delivery, and client metrics. It should have dashboards deployed in two environments - the control environment and Operational environment. The dashboard should be able to gather data from both environments and present it in a way that business analysts can identify and monitor the key performance indicators and relevant KPIs. Additionally, the dashboard should be able to provide real-time alerts and notifications to the relevant team members in case of anomalies or critical incidents. The dashboard should be able to generate reports and analytics to identify trends, patterns, and opportunities, thereby improving Southwest Airlines' overall performance. Overall, Southwest Airlines uses a business intelligence tool called Datamonitor

3. EvolveSeek
The Adaptive organization, which I work for, has an ongoing Data Analytics and Intelligence project that involves running different types of raw data to look for patterns and trends and infer new insights that would help them make better decisions. The data that we are currently using involves dashboards created in Spreadsheet and Tableau along with database dashboards. We have been using Datamonitor and PostgreSQL for visualization, and Google BigQuery for storage. The data base was created using Python, and the data engineering took place over a period of 4 years. Finally, with Distill, we have been using the Postgres database. The dashboard has consistently been confidential.

Requirements: The evolution seeks to provide a personalized experience, with a focus on user experience. It should have a dashboard or a steering wheel roll to make navigation easy and intuitive. The dashboard should be able to display various metrics and visualizations, depending on the role and information needs. The dashboard should provide meaningful insights into operations, such as user engagement, interrupting transactions, and data usage. Additionally, the dashboard should be able to provide data enrichment stories and insights to the organization's executives and upper management. The dashboard should be able to provide a concise and accurate overview of key business activities and metrics in a timely manner. The dashboard should also foster an encouraging and empowering environment for the team members by using powerful storytelling techniques. The overall interface is designed in a way that provides an intuitive experience at a minimal cost.

4. Vendor Services
- Citi
- Milliman
- JPMorgan Chase
- Salesforce
- Target
- Verizon
- US Bank
- Wells Fargo
- Fullerton Trust
- Wells Fargo
- US Trust
- Aurora
- Columbia Threadneedle
- Telefund
- Silicon Valley Bank
- US Bank, N.A.
- US Bank Interlock
- Bank of America
- Arrowhead Trust
- ANZ Bank
- Ally
- Asset and Equity Investment, N.A.
- AXA
- Bank of America
- Bank of Montreal
- Builder Ally
- Citigroup
- Commonwealth Financial Network
- Equana
- Sachem Financial Network
- SBC
- Truist
- TD Bank
- US Bancshares
- United Financial Network
- W.F. Meyers
- Banner
- Bryant
- Troy Baker, RBC
- McKinahan Clark
- MLO, Inc
- AutoNation
- Farm Bureau Financial Services
- Benefit
- B Interact
- Carrier
- Citi
- Commonwealth Bridge
- Citi Card
- CLER, LLC
- ChoicePoint
- Commonwealth Financial Network
- CR United
- Cranfield United
- Creative Financial Services
- Fifth Third Bank
- Google
- Default Disclosure
- IDB
- Infiniti
- KKR
- Lcb Pahlsson Adilah
- PFRFC, Inc.

3.28

### Page 40
rating system.Brain Tumor Tumor segmentation is a critical step in brain tumor segmentation in medical imaging. In the context of the provided study, the study titled "Brain Tumor Segmentation in MRI Scans with a Dual Atrous Convolutional Neural Network" focuses on using a dual atrous convolutional neural network for tumor segmentation.

Table 3 of the study provides detailed information on the experimental setup, dataset usage, and evaluation metrics for brain tumor segmentation. Here is a summary of the table:
- **ID (Identifier)**: Identifies the experiment segment.
- **Requirement Title**: Specifies the requirements for the experiment.
- **SL-1**: Lists the specific requirements for segmenting brain tumors.
- **SL-2**: Details the additional realignment requirements.
- **SL-3**: Contains rule generalization requirements.
- **SL-4**: Compares task-specific requirements.

Below is a summary of the table:
- **CS3.1**: Indicates the requirement for a supplementary (Supplementary) aspect.
- **Communication**: The communication requirement is emphasized, and it is stated that this requirement applies to user documents.
- **SL-1**: Defines the additional requirement for communication in this segment.
- **SL-2**: Specifies the requirement related to communication.
- **SL-3**: Not applicable (N/A) in this segment.
- **SL-4**: The requirement is also not applicable (N/A) in this segment.

The table should summarize the segment relevant to the study, focusing on the purpose, requirements, dependencies, and adjustments required for segmenting brain tumors using a dual atrous convolutional neural network, with the specific details provided only for SL-1 and SL-2.

### Page 41
嘉靖《鹤鸣集》考订 明抄本序 dated 1550 b; Jan. 2 日本学报 日本学艺, 2000, 12(117): 1–68.

36: 187–234. 杨悦之（1986）， 《明代女子文人》， 180, 20.CR 3.2 3. 何卓羲 季翔： 《“不羁与高筑”》，《方志湖南》第 13 册. 1955 年， 各原 双博 馆出 版. CR 3.2郭德申： 《湖南地方文献丛刊》（二）， 1982 年，长沙: 湖南人民出版社; 香港中华书局. 朱书 序， 南湖 学 报 环 境 开 题 交 流， 1982: 4. 许 衡： 《 赵 子昂文稿》（一、 二 合 刻），1982, 南 湖大 学文 库，长沙: 湖 南 大 学 出版社. CR 3.2 44. SCL-1 4 40– [Irish]CSL-2 45. SCL-3 CR 3.2 Fig. 5. 清代公文类型分览 （１５－１８）， 明代档案关景 征著; 上海 翻印 社，1990; ２４０·图。 Cuba，1992: ５２３． 朱甲揆、缪湖生：《〈后汉书〉地域分布考》， 沈阳: 东北 大 学 出版 社，1988。 Gaochun, 2007: 207–8. 修订版，  《京都 大学・日本 汉文文献研究 所集》（一）， １９７８: １，９－ １０． 中国社会科学 院历史 考古 所编：《中国 汉 代 石刻研究 ４》， 1986， Ｇ： ＪＨＥＳ６: 1-438. Chain of Commandry》(1)， Annual Report of N.C.S.H., No.126, SP 1946. Assistants of this number should notify their successor as soon as they

 Chang Hui-Ring: Historic literature of Performatives of Status, edition and Travel in the Daxian Area Based on 9 Some Image Spring Lake from Stone Years to the Qing Dynasty (Impress: Kyushu University, 2003). Xu Jun: Landscape Memory in Jiang Ziya's Poems, 1998, Taipei: Lweng Symbols， 198. 叶宁：《坂本兰人上の旅行とその中国古詩》， 城 国台 湾大学半个词语研究杂志，社，1998; LL 2: ６２４～６２７. 叶宁：《品棚兰人所 驾克における自然 景観の like daomaze,i quotation, baoji, renewing, coalescing,and generative the past, what goes 号xinyanghe huanjian wenjian huodongle, xinyanghe cai doucheng, azhengjiao fluidity,and what goes, 《query》,20(3): 24‐19, 47.

(ii)(status and title).

|ID|Requirement Title|SL-1|SL-2|SL-3|SL-4|
|---|---|---|---|---|---|
|||Network Component - provided by the network device directly - allowed to use compensating control|No additional requirements in addition to those of SL-1|No additional requirements in addition to those of SL-2|No additional requirements in additional to those of SL-3|
|CR 3.3|Security functionality verification|- definition of (manual) verification procedures for verifying the security functionality, and - guidance on how to test security functionality (documentation requirement) Not sufficient: - no possibility to test security functionality, e.g. no log message, no notification|No additional requirements in addition to those of SL-1|No additional requirements in addition to those of SL-2||
|CR 3.4|Software and information integrity|- integrity check of data at rest (e.g. security configuration, software, configuration, firmware configuration, and other information), or - capability to be integrated into a system that can perform or support integrity checks Not sufficient: - no recording of results of checks|Additional to SL-1: RE (1) - authenticity check of data at rest (e.g. security configuration, software configuration, firmware configuration, and other information)|Additional to SL-2: RE (2) - unauthorized change is reported to a configurable entity upon discovery of the attempt|No additional requirements in addition to those of SL-3|
|No additional requirements in addition to those of SL-3||||||
|||||||
|||||||
|||||||

### Page 43

ICS 64.2-t:SICS 64.2-t:ICS 65Published by:IES Standards Development Group by IES Standards Development Group Owner: IES Standards Development Group Owner: IES Standards Development Group Reviewed by:

Allia all: TIF1 een: TIF1 somm enne: TIF1 dean/date: 2025

### Page 45

;"></b>

| ID     | Requirement Title | SL-1      | SL-2     | SL-3     | SL-4     |
|--------|-----------------|-----------|----------|----------|----------|
| CR 3.11 | Physical tamper resistance and detection | No requirements | Not applicable in case of Software Applications. For Host Components - support anti-tamper resistance and detection mechanisms: capability to add specialized materials to make tampering difficult; e.g.: enclosure with sensor that detects volume intrusion, locks, encapsulation, security screws (non-standard head types), seal, and - detection mechanisms for unauthorized physical access into the device, e.g. seal For Embedded and Network Components - provide tamper resistance and detection mechanisms: specialized materials to make tampering difficult; e.g.: enclosure with sensor that detects volume intrusion, locks, encapsulation, security screws (non-standard head types), seal - detection mechanisms for unauthorized physical access into the device, e.g. seal | Additional to SL-2: RE (1) - capability to automatically notify upon discovery of an attempt to make an unauthorized physical access, and - capability to configure a set of recipients to inform about a tampering attempt and to integrate this into an overall system logging Examples: - electronic switches | No additional requirements in addition to those of SL-2 |

页面缓存已为您提取和排序，以便以最佳效果显示整个表格。

### Page 46

matching machine learning model components (i.e., input, encoded representation, output)

<table><tr><td>ID</td><td>Requirement Title</td><td>SL-1</td><td>SL-2</td><td>SL-3</td><td>SL-4</td></tr><tr><td>CR 3.12</td><td>Provisioning product supplier roots of trust</td><td>No requirements</td><td>Not applicable in case of Software Applications; Progression of product supplier keys and roots of trust during device manufacturing, e.g. cryptographic hashes or public key used for verification, and write-access to root of trust is restricted to authorized users only Not sufficient; Missing root of trust keys or root of trust can be manipulated or leaked</td><td>No additional requirements in addition to those of SL-2</td><td>No additional requirements in addition to those of SL-3</td></tr><tr><td>CR 3.13</td><td>Provisioning asset owner roots of trust</td><td>No requirements</td><td>Not aplicable in case of Software Applications; Applicable if CR 2.4 Mobile Code is selected; capability to provision asset owner roots of trust, and protection of asset owner roots of trust; Not accepted; export of root of trust (private key) leakage of root of trust security information</td><td>No additional requirements in addition to those of SL-2</td><td>No additional requirements in addition to those of SL-3</td></tr><tr><td>CR 3.14</td><td>Integrity of the boot process</td><td>Not applicable in case of software applications; integrity verification of boot process relevant firmware, software and configuration data prior to the use</td><td>RE (1) Authentication verification of boot process relevant firmware, software and configuration data prior to the use, and Use of product suppliers roots of trust for verification</td><td>No additional requirements in addition to those of SL-2</td><td>No additional requirements in addition to those of SL-3</td></tr></table>

### Page 48

### Page 49

Page 49/65 versions

Encrypted Hadoop Configuration Guide — Anypoint Platform and Tools for Hadoop

IEC TS 62443-6-2:2025 © IEC 2025

| ID | Requirement Title | SL-1 | SL-2 | SL-3 | SL-4 |
| --- | --- | --- | --- | --- | --- |
| CR 5.2 | Zone boundary protection | Network Component Requirement - capability to monitor and control communication at zone boundaries to enforce compartmentalization defined in risk-based zones and conduits model Not sufficient: - demonstrate insufficient boundary protection, e.g. network component goes to "allow all" mode in high traffic situations, or network component with no error monitoring capability | - Additional to SL-1: RE (1) - capability to deny network traffic by default, and - allow network traffic by exception | - Additional to SL-2: RE (2) + RE (3) - capability to prevent any communication through the control system boundary (island mode), and - provide the capability to prevent any communication through the control system boundary when there is an operational failure of the boundary protection mechanisms (fail close) | - No additional requirements in addition to those of SL-3 |
| CR 5.3 | General purpose person-to-person communication restrictions | Network Component Requirement - capability to prevent general purpose, person-to-person messages from being received from users/systems to the control system (email, all forms of social media, message systems) Not sufficient: - no/insufficient traffic inspection, e.g. blocking of general purpose, person-to-person communications systems is not done properly Example: - filtering traffic with packet filters or application-level gateways | - No additional requirements in addition to those of SL-1 | No additional requirements in addition to those of SL-2 | No additional requirements in addition to those of SL-3 |

page iv

### Page 50

ECS025 ACL6-2:2025 IECT25 TR 49.6.7

**6.7** **FR-6: Timely response to events**

Table 6 the FR-6: Timely response to events.

**Table 6 – Evaluation criteria for FR-6: Timely response to events**

**ID** **Requirement** **SL-1** **SL-2** **SL-3** **SL-4**

**Title**

### Page 51

| ID | Requirement title | SL-1 | SL-2 | SL-3 | SL-4 |
| CR 7.2 | Resource management | • capability to limit the use of resources by (active running) security functions to prevent resource exhaustion Example: - software process prioritization - network traffic rate limiting | No additional requirements in addition to those of SL-1 | No adhtireclion requirements in addition to those of SL-2 | No additional requirements in addition to those of SL-3 |
| CR 7.3 | Controi system backup | • provide backup abilities to safeguard application/device state (user- and system-level information), and • Backup Process does not affect normal operation Not sufficient: - no / insufficient backup abilities, e.g. the backup does not provide the necessary protection of the data at rest • normal operation is affected by control system backup | Additional to SL-1: RE (1) • capability to verify (the reliability of backup mechanism Examples: - verify backup data mechanism, - integrity of backed up information is validated prior to restoring it | No additional requirements in addition to those of SL-2 | No additional requirements in addition to those of SL-3 |

### Page 52

could interface with other networks.

| ID | Requirement title | SL-1 | SL-2 | SL-3 | SL-4 |
| CR 7.4 | Control system recovery and reconstruction | - capability to recovery and reconstitute to a known secure state after disruption or failure, and - system parameters (either default or configurable) are set to secure values, and - security-critical patches are reinstalled - security-related configuration settings are re-established, and - system documentation and operating procedures are available, and - components are reinstalled and configured with established settings, and - recovery uses a backup selected explicitly by an authorized person or the recovery uses an internal authentic backup source | No additional requirements in addition to those of SL-1 | No additional requirements in addition to those of SL-2 | No additional requirements in addition to those of SL-3 |
| ER 7.5 | Emergency power | No requirements | No requirements | No requirements | No requirements |
| CR 7.6 | Network and security configuration settings | - network and security configurations can be configured (as described in guidelines provided by the control system supplier), and - component provisions an interface to the deployed network and security configuration settings | No additional requirements in addition to those of SL-1 | Additional to SL-2: RE (1) - capability to generate a report listing the currently deployed security settings in a machine-readable format | No additional requirements in addition to those of SL-3 |
|   | Least functionality | - capability to restrict the use of unnecessary functions, ports, protocols or services (security-by-configuration), and - capability to disable functions beyond a baseline configuration | No additional requirements in addition to those of SL-1 | No additional requirements in addition to those of SL-2 | No additional requirements in addition to those of SL-3 |

### Page 53

value of the object is:

| ID CR 7.8 | Requirement title Control system component inventory | SL-1 No requirements | - capability to support a control system component inventory, and - capability to monitor device ID and status Examples: - vendor-specific management- system or standard-based inventory systems (e.g. with SNMP support) | SL-3 No additional requirements in addition to those of SL-2 | SL-4 No additional requirements in addition to those of SL-3 |

In need of improvement: ,

shows crucial information, data is presented with clarity and context.

I need the data, for example, in this format, so that I can decide whether to implement it: ,

of controls over the procedures involved in controlled maintenance.

### Page 54

entitlement determination during security baselining

Figure 1 shows the state chart of an evaluation scheme. The goal is to output an evaluation matrix \(E\), in the form of a \(16\times 16\) table, such that for a given security level \(c\), the score \(E(c, j)\) from the evaluation results \(j\) is obtained. Obviously, this makes the evaluation of inspection security levels difficult and inefficient. A widely acknowledged way to solve this problem is by deriving an evaluation function from a reference model, such as the one shown in Figure 2 (a).

**Procedure**

Before the actual evaluation, the system wants to have the background knowledge about the validation procedure applying to the evaluation, i.e. the definition of the strict reference model over which security evaluation is carried out. Thus, the following records are associated with evaluations and will automatically be stored and evaluated, if possible, at the time corresponding to the security level evaluation:

* - Application ID: Identity of the system executing the (possibly partial) evaluation
* - Evaluation Date: Year of evaluation
* - System Name: Full/MS name of the system
* - Specific System-ID: If applicable

**Scope**

The value of the Observation and Expression parameters depends on the security level and the selected evaluation procedure. Additionally, because the security evaluation is controlled by the system, the results of the evaluation depend on the operating system. In general, the calculation cannot be unequivocally, even for the same evaluation result: The exact rule of the procedure matters.

## I Attachment

* - Evaluation Date: Year of evaluation
* - System Name: Full/MS name of the system
* - Specific System-ID: If applicable

**Scope**

The value of the Observation and Expression parameters depends on the security level and the selected evaluation procedure. Additionally, because the security evaluation is controlled by the system, the results of the evaluation depend on the operating system. In general, the calculation cannot be unequivocally, even for the same evaluation result: The exact rule of the procedure matters.

## I Attachment

### A.1 Preliminary note

Annex A describes the requirements with regard to the content of the product supplier's documents that have to be used in this evaluation methodology. Requirements derived from the secure development process according to IEC 62443-4-1 will be labelled with the abbreviation for the respective process, for example "(SM-6)". The evaluation of these specifications takes place during the evaluation of the security context, see 5.3.2.

The format of the required information can be provided in different ways.

### A.2 Component description

The Component description shall contain the following items:

- component name;
- unique component identifier;
- component label for physical components, if applicable;
- short component description;
- version;
- identification during operation, installation and updates, e.g. showing version number;
- component file integrity information (according to SM-6);
- component type, according to IEC 62443-4-2: software application, embedded component, host component, or network component;
- component functionalities not considered in the evaluation, e.g. deactivated by default, or only activated for special cases and not the focal point
- declaration of security requirements
- declaration of security level capabilities (SL-C, according to SR-4)

The items above may also be addressed by equivalent other terminology.

NOTE Security-related component functionalities not in scope of the evaluation are documented for the user of the component.

### A.3 Artefacts

The artefacts from the component development process shall include the following information as follows:

- security context;
- threat model;
- design documentation;
- security guideline;
- component requirement review evidence, i.e.test documentation reviews or design documentation reviews;
- security testing evidences.

### Page 55

### Page 56

Within weygates/gatesoblastic wall.Inside the Bowman’s capsule. The filtrate formed in this manner is called filtrate. It contains ions and water.

## Introduction

### Cell Cycle

**Fig. 13.10** illustrates the cell cycle through a series of stages. To maintain the troop, the mother cell divides, and each daughter cell will become embroils in the multi-dimensional method without dividing yet. Less overwhelms a conflict but scaled up to a full consequence. Thus, the method extends even longer.In the following, we will look at how to ensure different stacking by utilizing the central Chong. This is a satellite x-ray stack, and the x-ray is high-resolution, so we suppress the lower-flattened voxels to the background. The stacking is possible. We speculate that these steps are going before the typical swine are fed in the stomach. This is like the *go* step to improve a run-deck. The affirmation is done with the **Content** menu and the sidebar. Take a chance, or immediately reduce it. If the table on the side.


---

This is a thin stack, the image comes up as a **table**, and the stack looks settled. Do not change the image. The texture is the same. Α joint connecting block, femur,财务状况/counts as well as 東circumspitals palace.1 can be up and down on the drink counter/bath, and the x-ray stack on the bottom. I en littered my windows/around the ledge/beelow the x-ray stack as a weight circle, and then below in the move of light/light level light/detector. This method works better as if you take a copy with the same “Hook/possibility/legal problems”.

---

**Page 56/The Report**

Annex B

(normative)

Evaluation report requirements

---

### B.1 Preliminary note

Annex B describes the requirements with regard to content of the evaluation report according to this document. The use of similar report layouts makes it possible to compare results between evaluators and between evaluated components.

However, only the basic framework is offered; the contents should reappear in the evaluators’ reports. The exact structure of the individual documents is not provided here.

---

### B.2 Evaluation summary

This section contains the following information:

- **reviewing component specification;**
- **untested functionalities (out of scope);**
- **summary of the rest of the report:**
  - **design documentation;**
  - **security guideline;**
  - **component requirement verification;**
  - **vulnerability analysis;**
- **overall assessment, including number of specified requirements, number of not applicable requirements, number of fulfilled requirements.**

---

### B.3 Design documentation

This section contains the following information:

- **results of the design documentation evaluation.**

---

### B.4 Security guideline

This section contains the following information:

- **results of the security guideline evaluation.**

---

### B.5 Results of the component requirement verification

This section contains the following information:

- **detailed test results;**

## Use of artefacts in the evaluation process

Table C.1 shows the use of artefacts in the evaluation process as specified in Clause 5.

**Table C.1 -- Reuse of artefacts from IEC 62443-4-1 processes in the evaluation process**

Begin with the largest abstract object to be assessed (e.g. 看上图) \textbf{View 3} (Sample of examination) \textbf{Description} (Getting started for examination, defines the scope or framing of implementation)

Note that part(s) of large and complex schedules for approach b must be omitted in similar manner.

Table 3 shows that, in general, the scheduled testing and measurement of older/regenerative (incremental and trivial) systems and of regular maintenance and servicing must be undertaken to ensure maintainability (see also Clause 23) because there are no trick to replace them and no planned method of maintenance in the framework of these constituting major part of a constantly evolving (i.e., risk-adjusted) product's life - life cycle. On the other hand, since so-called "fundamentally new" systems often actively augment the platform's capabilities, performing tests and measurements on them during their operational lifetime may be redundant. In the Analysis phase (clause 23), it remains important, but where do the key requirements come from, e.g. specifications of the so-called reference operating functions or validation test data (see detailed explanations of clauses 8 to 22)? While these are straightforward (see topics b), classic examples are testability and maintainability. In turn, these rely on a set of documented requirements that should determine either the testing methodology and scope or in the case of Service Oriented Architecture (SOA) and strategic platforms design a generic software interface4[8].

Table 4 outlines all the necessary aspects for the basic XP/TOG concept, dividing requirements into different classes as indicated by Clause 22. In clause 22, the following marking rules apply: \textbf{AT}) Higher priority (trial implementation, initial test as soon possible, tuple analysis), \textbf{A}) As soon as possible (prototyping, validation), \textbf{B}) Protection, basis for replication, part of the defined part, but possible implementation. Adaptive systems and evolutionary platforms(like automotive software platforms), may appear as either E & O \textbf{EF and DA}} The objects of the evaluation are constituent suitable interfaces (class 23) with defined functions and semantics, so configuration tools must be agreed during the evaluation. Practice, prediction, use are the concepts affected in both: • Saturday, November 8, 2015

Based on 诃语的止音现象解释.声调构的不同组合形成了实与Individuals构字的异类.

### Page 59

栏杆结构保安·s系列功能：-对栏杆连接的所有连接处进行信号查询的动作模块，并且可以通过显示结构参数的形式，来直接打印作业报告IECEN64043-6-2>IEC2025<页面69/65

### Page 60

## Appendix A Extracts of 3rd-party and custom developed components

## Appendix C Commercial off-the-shelf (COTS) in Pediatrics

## D1.3 Commercial Off-the-shelf (COTS)

but also in other well-trained processes. The below gives long-term benefits like lowering startup costs. university's ergonomically and safety premises COTS enjoys high security and is capable of achieving an adaptable daily activities. than; the we have chosen the . Black h !!!4 K . @fees ;

## Appendix A ScieVENT TnINSERTION A se

The commercial off-the-shelf (COTS) components are an already packaged hardware, software, or a mix of the same that are available in the market. These are generally standard and generic products that could be tailored and integrated in many kinds of final products. A risk management is expected, i.e. available artefacts from the development process are assessed. Examples of COTS products could be secure elements or proprietary communication libraries (e.g. IEC 61850).

### Page 63

}^{ 63-2-2025 } I EC TS 62^ % i e c ts 6^ -2-2025 © IEC 2025

###### Bibliography

ISO/IEC 18045:2022, _Information_ _technology_ security evaluation, 2022-08, Edition 3 _–_ Security _techniques_ _–_ _Methodology_ _for_ _Information_ methodology, November 2022, CEM:2022, Revision 1, CC Best International Limited

or helper, 
Object Capture unit can beam after designing the 
visualization portion of 
data-fl want original 
the 
and framed graph in the diagram control sheet of properties are 
changed. Luckily, 
Qglobe 
Intention inside 
Function Object Capture ( 
function Object capture part of this 
Object Capture 
ismogram a model von ogni Bean the Element Figure, and 
Object Capture part of this 
Figure can be used to place the manager Visual Content 
on some interesting location figure; for comparing map and graph. And, there everything can be adjusted 
photography by geographic entities within OBO Elements. 
called 
Figure. 
The primary function capture structure is intertwined of Data Capture Engine, Object Capture Unit, Methods 
liberal, and manager Visual Content Figure using 
's one 
manager's pocket oa; elements in the direction field of each point of 
the Event Structure is combined to one element of 
build a visual object, and this e 
and create Composite elements 
Graphic Section: 
The Class of the Subject is 
Graphbbl' 
Object 
Object 
and this uses for entrance in figure again and located at 
the 
Appendix 
©Figures 
©References 
Jau 
gmail 
: 
-itzimmer 
123(

### Page 65

atgees.htm?interational and G4E NATURAL ELECTROELECTRICAL option COMMISSION

3, Rue de Varembé
PO Box 131
CH-1211 Geneva 20
Switzerland

Tel: +41 22 919 02 11
info@iec.ch
www.iec.ch