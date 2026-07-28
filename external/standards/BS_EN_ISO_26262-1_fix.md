### Page 1

# Road vehicles — Functional safety

## Part 1: Vocabulary

### doi 10.6025/j.vision.2015.ai014

#### bsi.

### bsi.

#### ...making excellence a habit"

### Page 2

The UK participation in its preparation was entrusted to Technical Committee AUE/16, Electrical and electronic equipment.

A list of organizations represented on this committee can be obtained on request to its secretary.

This publication does not purport to include all the necessary provisions of a contract. Users are responsible for its correct application.

© BSI 2011

ISBN 978 0 580 62303 5

ICS 01.040.43; 43.040.10

# Compliance with a British Standard cannot confer immunity from legal obligations.

This British Standard was published under the authority of the Standards Policy and Strategy Committee on 30 November 2011.

Amendments issued since publication

| Date    | Text affected |
|---------|---------------|
|         |               |

[Table of Contents](#) continues on next page

Page 2/34

### Page 4

**COPYRIGHT PROTECTED DOCUMENT**

---

**ISO 2011**  
The reproduction of the terms and definitions contained in this International Standard is permitted in teaching manuals, instruction booklets, technical publications and journals for strictly educational or implementation purposes. The conditions for such reproduction are: that no modifications are made to the terms and definitions; that such reproduction is not permitted for dictionaries or similar publications offered for sale; and that this International Standard is referenced as the source document.

With the sole exceptions noted above, no other part of this publication may be reproduced or utilized in any form or by any means, electronic or mechanical, including photocopying and microfilm, without permission in writing from either ISO at the address below or ISO’s member body in the country of the requester.

ISO copyright office  
Case postale 56 • CH-1211 Geneva 20  
Tel. +41 22 749 01 11  
Fax + 41 22 749 09 47  
E-mail copyright@iso.org  
Web www.iso.org  
Published in Switzerland

© ISO 2011 – All rights reserved

### Page 8

**Figure 1 — Overview of ISO 26262**

### Page 9

Part 1: Vocabulary

Scope

ISO 26262 is intended to be applied to safety-related systems that include one or more electrical and/or electronic (E/E) systems and that are installed in series production passenger cars with a maximum gross vehicle mass up to 3 500 kg. ISO 26262 does not address unique E/E systems in special purpose vehicles such as vehicles designed for drivers with disabilities.

Systems and their components released for production, or systems and their components already under development prior to the publication date of ISO 26262, are exempted from the scope. For further development or alterations based on systems and their components released for production prior to the publication of ISO 26262, only the modifications will be developed in accordance with ISO 26262.

ISO 26262 addresses possible hazards caused by malfunctioning behaviour of E/E safety-related systems, including interaction of these systems. It does not address hazards related to electric shock, fire, smoke, heat, radiation, toxicity, flammability, reactivity, corrosion, release of energy and similar hazards, unless directly caused by malfunctioning behaviour of E/E safety-related systems.

ISO 26262 does not address the nominal performance of E/E systems, even if dedicated functional performance standards exist for these systems (e.g. active and passive safety systems, brake systems, Adaptive Cruise Control). This part of ISO 26262 specifies the terms, definitions and abbreviated terms for application in all parts of ISO 26262.

1 Terms and definitions

For the purposes of this document, the following terms and definitions apply.

1.1 allocation

assignment of a requirement to an architectural element (1.32)

NOTE Intent is not to divide an atomic requirement into multiple requirements. Tracing of an atomic system (1.129) level requirement to multiple lower level atomic requirements is allowed.

1.2 anomaly

condition that deviates from expectations, based, for example, on requirements, specifications, design documents, user documents, standards, or on experience

NOTE Anomalies can be discovered, among other times, during the review (1.98), testing (1.134), analysis, compilation, or use of components (1.15) or applicable documentation.

### Page 12

ements.Configuration data cannot contain executable or interpretable code.

Configuration data controls the software build. Only code, or data selected by configuration data can be included in the executable code.

**1.17**

**confirmation measure**

**confirmation review (1.18), audit (1.5) or assessment (1.4) concerning functional safety (1.51)**

**1.18**

**confirmation review**

confirmation that a work product meets the requirements of ISO 26262 with the required level of independence (1.61) of the reviewer

NOTE 1 A complete list of confirmation reviews is given in ISO 26262-2.

NOTE 2 The goal of confirmation reviews is to ensure compliance with ISO 26262.

**1.19**

**controllability**

ability to avoid a specified harm (1.56) or damage through the timely reactions of the persons involved, possibly with support from external measures (1.38)

NOTE 1 Persons involved can include the driver, passengers or persons in the vicinity of the vehicle's exterior.

NOTE 2 The parameter C in hazard analysis and risk assessment (1.58) represents the potential for controllability.

**1.20**

**dedicated measure**

measure to ensure the **failure rate (1.41) claimed in the evaluation of the probability of violation of safety** **goals (1.108)**

EXAMPLE Design feature [such as **hardware part (1.55) over-design (e.g. electrical or thermal stress rating) or** physical separation (e.g. spacing of contacts on a printed circuit board)]; special sample test of incoming material to reduce the **risk (1.99) of occurrence of failure modes (1.40) which contribute to the violation of safety goals; burn-in test; dedicated control plan.**

**1.21**

**degradation**

strategy for providing **safety (1.103) by design after the occurrence of failures (1.39)**

NOTE Degradation can include reduced functionality, reduced performance, or both reduced functionality and performance.

**1.22**

**dependent failures**

**failures (1.39) whose probability of simultaneous or successive occurrence cannot be expressed as the simple product of the unconditional probabilities of each of them**

NOTE 1 Dependent failures A and B can be characterized when

\(P_{AB} \neq P_{A} \times P_{B}\)

where

\(P_{AB}\) is the probability of the simultaneous occurrence of failure A and failure B;

\(P_{A}\) is the probability of the occurrence of failure A;

\(P_{B}\) is the probability of the occurrence of failure B.

NOTE 2 Dependent failures include **common cause failures (1.14) and cascading failures (1.13).**

### Page 14

1.30 dual-point fault

individual fault (1.42) that, in combination with another independent fault, leads to a dual-point failure (1.29)

NOTE 1 A dual-point fault can only be recognized after the identification of dual-point failure, e.g. from cut set analysis of a fault tree.

NOTE 2 See also multiple-point fault (1.77).

1.31 electrical and/or electronic system

\(P_{B}\) is the probability of the occurrence of failure B.

NOTE 2 Dependent failures include **common cause failures (1.14) and cascading failures (1.13).**

### Page 13

value, which is based on the quality of the paper and not on the page count. Overall, the quality of the paper matches that of a spreadsheet file, but the quality of the paper is significantly lower than a normal published paper of the same quality.

### Page 14

value of activity constant across saturation phase.1.30 dual-point faultindividual fault (1.42) that, in combination with another independent fault, leads to a dual-point failure (1.29)NOTE 1 A dual-point fault can only be recognized after the identification of dual-point failure, e.g. from cut set analysis of a fault tree.NOTE 2 See also multiple-point fault (1.77).

1.31 electrical and/or electronic systemE/E systemsystem (1.129) that consists of electrical and/or electronic elements (1.32), including programmable electronic elements.

EXAMPLE Power supply; sensor or other input device; communication path; actuator or other output device.

1.32 elementsystem (1.129) or part of a system including components (1.15), hardware, software, hardware parts (1.55), and software units (1.125).

1.33 embedded softwarefully-integrated software to be executed on a processing element (1.32)

NOTE The processing element is normally a micro-controller, a field programmable gate array (FPGA) or an application-specific integrated circuit (ASIC), but it can also be a more complex component (1.15) or subsystem.

1.34 emergency operationdegraded functionality from the state in which a fault (1.42) occurred until the transition to a safe state (1.102) is achieved as defined in the warning and degradation concept (1.140)

1.35 emergency operation intervalspecified time-span that emergency operation (1.34) is needed to support the warning and degradation concept (1.140)

NOTE Emergency operation is part of the warning and degradation concept (1.140).

1.36 errordiscrepancy between a computed, observed or measured value or condition, and the true, specified or theoretically correct value or condition

NOTE 1 An error can arise as a result of unforeseen operating conditions or due to a fault (1.42) within the system (1.129), subsystem or component (1.15) being considered.

NOTE 2 A fault can manifest itself as an error within the considered element (1.32) and the error can ultimately cause a failure (1.39).

1.37 exposurestate of being in an operational situation (1.83) that can be hazardous (1.57) if coincident with the failure mode (1.40) under analysis.

1.38 external measuremeasure that is separate and distinct from the item (1.69) which reduces or mitigates the risks (1.99) resulting from the item

### Page 15

comprising 104 pages in PDF format.

Detail Pages 

* Note that there are 'missing reports' for:
  - green: material availability 
  - red: consumption
  - blue: plausibility

NOTE 1    Permanent, intermittent and **transient faults** (section 1.134) (especially soft-errors) are considered.

NOTE 2    An intermittent fault occurs time and time again, then disappears. This type of fault can occur when a **component** (see section 1.15) is on the verge of breaking down or, for example, due to a glitch in a switch. Some **systematic faults** (1.131) (e.g. timing marginalities) could lead to intermittent faults.

### 1.38 Failure

Termination of the ability of an **element** (1.32), to perform a function as required. Note: Incorrect specification is a source of failure. 

### 1.40 Failure mode

manner in which an element (1.32) or an **item** (1.69) fails. 

### 1.41 Failure rate

probability density of failure (1.39) divided by probability of survival for a hardware **element** (1.32). Note: The failure rate is assumed to be constant and is generally denoted as 'λ'.

### 1.42 Fault

abnormal condition that can cause an **element** (1.32) or an **item** (1.69) to fail. 

### 1.43 Fault model

representation of **failure modes** (1.40) resulting from **faults** (1.42). 

### 1.44 Fault reaction time

time-span from the detection of a **fault** (1.42) to reaching the **safe state** (1.102).

See Figure 4.

Figure 4 — Fault reaction time. 

Note: At very low event rates, there was an 8.18% MTTF [Missing-Time-to-Failure] while a 5.59% MTTF [Missing-Time-to-Reaction].

### Page 16

## 1.45 fault tolerant time interval

time-span in which a fault (1.42) or faults can be present in a system (1.129) before a hazardous (1.57) event occurs

## 1.46 field data

data obtained from the use of an item (1.69) or element (1.32) including cumulative operating hours, all failures (1.39) and in-service anomalies

NOTE Field data normally comes from customer use.

## 1.47 formal notation

description technique that has both its syntax and semantics completely defined

EXAMPLE Z notation (Zed); NuSMV (symbolic model checker); Prototype Verification System (PVS); Vienna Development Method (VDM).

## 1.48 formal verification

method used to prove the correctness of a system (1.129) against the specification in formal notation (1.47) of its required behaviour

## 1.49 freedom from interference

absence of cascading failures (1.13) between two or more elements (1.32) that could lead to the violation of a safety requirement

EXAMPLE 1 Element 1 is free of interference from element 2 if no failure (1.39) of element 2 can cause element 1 to fail.

EXAMPLE 2 Element 3 interferes with element 4 if there exists a failure of element 3 that causes element 4 to fail.

## 1.50 functional concept

specification of the intended functions and their interactions necessary to achieve the desired behaviour

NOTE The functional concept is developed during the concept phase (1.89).

## 1.51 functional safety

absence of unreasonable risk (1.136) due to hazards (1.57) caused by malfunctioning behaviour (1.73) of E/E systems (1.31)

## 1.52 functional safety concept

specification of the functional safety requirements (1.53), with associated information, their allocation (1.1) to architectural elements (1.32), and their interaction necessary to achieve the safety goals (1.108)

## 1.53 functional safety requirement

specification of implementation-independent safety (1.103) behaviour, or implementation-independent safety measure (1.110), including its safety-related attributes

NOTE 1 A functional safety requirement can be a safety requirement implemented by a safety-related E/E system (1.31), or by a safety-related system (1.129) of other technologies (1.84), in order to achieve or maintain a safe state (1.102) for the item (1.69) taking into account a determined hazardous event (1.59).

NOTE 2 The functional safety requirements might be specified independently of the technology used in the concept phase (1.89), of product development.

NOTE 3 Safety-related attributes include information about ASIL (1.6).

### Page 17

## Appendix A Tables

\begin{table*}

**Hardware architectural metrics**  
metrics for the **assessment** (1.4) of the effectiveness of the hardware **architecture** (1.3) with respect to **safety** (1.103)

NOTE The **single-point fault** (1.122) metric and the **latent fault** (1.71) metric are the hardware architectural metrics.

**Hardware part**  
hardware which cannot be subdivided

**Harm**  
physical injury or damage to the health of persons

**Hazard**  
potential source of **harm** (1.56) caused by **malfunctioning behaviour** (1.73) of the **item** (1.69)

NOTE This definition is restricted to the scope of ISO 26262; a more general definition is potential source of harm.

**Hazard analysis and risk assessment**  
method to identify and categorize **hazardous events** (1.59) of **items** (1.69) and to specify **safety goals** (1.108) and **ASILs** (1.6) related to the prevention or mitigation of the associated hazards in order to avoid **unreasonable risk** (1.136)

**Hazardous event**  
combination of a **hazard** (1.57) and an operational **situation** (1.83)

**Homogeneous redundancy**  
multiple but identical implementations of a requirement

**Inadherence**

**Independent failures**  
absence of **dependent failures** (1.22) between two or more **elements** (1.32) that could lead to the violation of a safety requirement, or organizational separation of the parties performing an action

NOTE By definition, **ASIL decomposition** (1.7) or **confirmation measures** (1.17) include requirements on independence.

**Independent failures**  
**failures** (1.39) whose probability of simultaneous or successive occurrence can be expressed as the simple product of their unconditional probabilities

**Informal notation**  
description technique that does not have its syntax completely defined

### Page 18

**BS ISO 26262-1:2011**  
**ISO 26262-1:2011(E)**

**1.65**

**inheritance**

passing attributes of requirements in an unchanged manner to the next level of detail during the development process

**1.66**

**initial ASIL**

ASIL (1.6) resulting from the hazard analysis or the ASIL resulting from a preceding **ASIL decomposition** (1.7)

NOTE  The initial ASIL is the starting point for **ASIL decomposition** (1.7) or further ASIL decomposition.

**1.67**

**inspection**

examination of work products, following a formal procedure, in order to detect anomalies

NOTE 1	Inspection is a means of **verification** (1.137).

NOTE 2	Inspection differs from **testing** (1.134) in that it does not normally involve the operation of the associated item (1.69) or **element** (1.32).

NOTE 3	Any anomalies that are detected are usually addressed by rework, followed by re-inspection of the reworked products.

NOTE 4	A formal procedure normally includes a previously defined procedure, checklist, moderator and **review** (1.98) of the results.

**1.68**

**intended functionality**

behaviour specified for an item (1.69), **system** (1.129), or **element** (1.32) excluding **safety mechanisms** (1.111)

**1.69**

**item**

**system** (1.129) or array of systems to implement a function at the vehicle level, to which ISO 26262 is applied

**1.70**

**item development**

complete process of implementing an item (1.69)

**1.71**

**latent fault**

**multiple-point fault** (1.77) whose presence is not detected by a **safety mechanism** (1.111) nor perceived by the driver within the **multiple-point fault detection interval** (1.78)

**1.72**

**lifecycle** 

entirety of **phases** (1.89) from concept through decommissioning of the item (1.69)

**1.73**

**malfunctioning behaviour**

**failure** (1.39) or unintended behaviour of an item (1.69) with respect to its design intent

**1.74**

**model-based development**

development that uses models to describe the functional behaviour of the **elements** (1.32) to be developed

NOTE  Depending on the level of abstraction used for such a model, the model can be used for simulation or code generation or both.

© ISO 2011 – All rights reserved

95**

### Page 19

Examples of unambiguous transcriptions may be found in standard dictionaries such as Machine Translation Tools 2.6, Wordcation 2.7, or Mary in the Spacy R package 2.8.

The detailed user guide for the default mapping definition, 28, 16.1.3.4, is available online 2.9.

Battaglia et al. 2.10 also emphasize the importance of clear definitions of each target language in the mappings, but this point is more fit for machine learning expertise, primarily, rather than speech and language models themselves.

Lastly, users are requested to provide additional runtime information (see 28, 16.1.4) if needed, such as timestamps, numbers of resources used, specific mappings handled, and faulty mappings. Please expect unexpected behaviors if runtime information is omitted.

An apology is made for any inconvenience caused.

week

### Page 21

# 1.92 random hardware failure failure (1.39) that can occur unpredictably during the lifetime of a hardware element (1.32) and that follows a probability distribution

NOTE Random hardware **failure rates (1.41) can be predicted with reasonable accuracy.**

# 1.93 reasonably foreseeable event event that is technically possible and has a credible or measurable rate of occurrence

# 1.94 redundancy existence of means in addition to the means that would be sufficient for an element (1.32) to perform a required function or to represent information

NOTE Redundancy is used in ISO 26262 with respect to achieving a **safety goal (1.108) or a specified safety** requirement, or to representing safety-related information.

EXAMPL1 Duplicated functional **components (1.15) can be an instance** of redundancy for the purpose of increasing **availability (1.8) or allowing fault (1.42) detection.**

EXAMPL2 The addition of parity bits to data representing safety-related information provides redundancy for the purpose of allowing fault detection.

# 1.95 regression strategy strategy to verify that an implemented change did not affect the unchanged, existing and previously verified parts or properties of an item (1.69) or an element (1.32)

# 1.96 residual fault portion of a **fault (1.42) that by itself leads to the violation of a safety goal (1.108), occurring in a hardware** **element (1.32), where that portion of the fault is not covered by safety mechanisms (1.111)**

NOTE This presumes that the hardware element has safety mechanism coverage for only a portion of its faults.

EXAMPL If low (60 %) coverage is claimed for a **failure mode (1.40), the other 40 % of that same failure mode is** the residual fault.

# 1.97 residual risk risk (1.99) remaining after the deployment of **safety measures (1.110)**

# 1.98 review examination of a work product, for achievement of the intended work product goal, according to the purpose of the review

NOTE Reviews can be supported by checklists.

# 1.99 risk combination of the probability of occurrence of **harm (1.56) and the severity (1.120) of that harm**

# 1.100 robust design design that has the ability to function correctly in the presence of invalid inputs or stressful environmental conditions

### Page 22

value of network resources. NOTE Robustness can be understood as follows:

— for software, robustness is the ability to respond to abnormal inputs and conditions;
— for hardware, robustness is the ability to be immune to environmental stress and stable over the service life within design limits;
— in the context of ISO 26262, robustness is the ability to provide safe behaviour at boundaries.

1.101
safe fault
fault (1.42) whose occurrence will not significantly increase the probability of violation of a safety goal (1.108)

NOTE 1 As shown in ISO 26262-5:2011, Annex B, both non-safety and safety-related elements (1.113) can have safe faults.

NOTE 2 Single-point faults (1.122), residual faults (1.96) and dual-point faults do not constitute safe faults.

NOTE 3 Unless shown relevant in the safety concept, multiple-point faults (1.77) with higher order than 2 can be considered as safe faults.

1.102
safe state
operating mode (1.81) of an item (1.69) without an unreasonable level of risk (1.99)

EXAMPLE Intended operating mode; degraded operating mode; switched-off mode.

1.103
safe
absence of unreasonable risk (1.136)

1.104
safety activity
activity performed in one or more subphases (1.128) of the safety lifecycle (1.72)

1.105
safety architecture
set of elements (1.32) and their interaction to fulfil the safety requirements

1.106
safety case
argument that the safety requirements for an item (1.69) are complete and satisfied by evidence compiled from work products of the safety activities during development

NOTE Safety case can be extended to cover safety (1.103) issues beyond the scope of ISO 26262.

1.107
safety culture
policy and strategy used within an organization to support the development, production and operation of safety-related systems (1.129)

NOTE See ISO 26262-2:2011, Annex B.

1.108
safety goal
top-level safety requirement as a result of the hazard analysis and risk assessment (1.58)

NOTE One safety goal can be related to several hazards (1.57), and several safety goals can be related to a single hazard.

### Page 23

### Page 24

value of security checks in markets with financial transactions security procedure is generally increased based on the anonymousness of the entity, which also has financial advantages (cf. Gregor J. and Hult G. M., 2010), they are best results are most secure for software systems with remote. The use of encryption technology is considered unacceptable if it takes into account the economic effect on the system. The most important methods of securing software products are presented in the reviews. For example, Agih et al. (2003) and Bak et al. (2002) consider classical cryptographic algorithms. How to secure a data exchange in an electronic business system is considered in the professional articles of Bachekova et al. () and Vachakovska I. I. (2012). For information security, you may use various software solutions: the author considers YoNOSE VA (Green et al., 2005) a useful tool. To organize the security activities, the IEC 62443 series were proposed. As this series is national economically useless, the authors consider the protection of the information and control systems at the server level as the most important. Conventional security tools are also used to verify safe fast technical solutions. The strongest of the protocols of information protecting standards of information and control systems are considered by the author AHS-2 RBSA and Glonass. Special attention is paid to asymmetric encryption (AES) due to its password security and the mono encryption (AES) in combination with the RSA algorithm. Software systems are considered equiped with transmission channels by means of Ethernet (data transfer for other types of links, e.g. radio or optical is not discussed). The system's wiring is considered in two standard forms: twisted pair cables, protecting efficient data transfer, low-frequency broadcasting stations or radio communication stations, industrial and low-frequency pollution; the data transfer through optical fibers is practically impossible over any distance, is not equipped with signaling equipment. We counted a safety check time as the time from the file entry to the conclusion of decision making, including the computing time. Thus, the data transfer time for a set of files contains all the time spent on gaining or maintaining a given channel bandwidth: while creating and reading the xls file by a system user, acquisitions of xls files by all users (including a system) are considered - so the system would take time for a user to exchange a file in an XLS document. This is generally specified by a class. The materials take into account the factor of the maximum number of users accessing the system, including system users. The level of efficiency, slowing down the system load during operation of the system file is attempted to be considered by this factor.

According to the analysis of Tepescakova ed. (2012), we can not fix in the expression of the possibility of the formation of "great age of the fuel of internal technical progress". However, we can notice that the change of an enterprise allows the improvement of accounting information system, it helps transform the assortment and its business in

### Page 25

value set from positive auxiliary align to balanced emission allocation, interpreted by index number, catalogue data commits state of filling area 1.

The document consists of multiple sections, each beginning with a bold font title. The document is presented in English, and the titles of the sections are: "special-purpose vehicle", "statement coverage", "subphase", and "1.121 exhaust". The first section begins: "For any suspension, brake or driver the required energy should be equal to or more than the required energy at any time of the year." It emphasizes the considerations involved in suspending, braking, and driver functions under different operating conditions. The second section is titled "statement coverage" and begins with the phrase: "new state of statements within the software has been executed". It discusses the necessity of enumeration and the compatibility of all clauses with the presence of any statement in the software. The third section, "subphase", begins with: "subdivision of a stage in the safety lifecycle (1.72) that is specified in a distinct clause of ISO 26262". It explains that a hazard analysis and risk assessment should be performed only once for an assembly and a sequence of phases. The fourth section begins with: "1.128 system". It states that all parameters and principles relevant for systems are set in clause 1.32. The fifth section begins with: "1.121 exhaust".

### Page 26

placeholder in `LONGIP` tree, so make sure to adjust the rest of the file path accordingly.

**Chapter 13: Attributes for CVE Identifiers**

`csrc/kernel/hw/3rd_party_auth_key_ring.a`: This is the canonical naming convention for CVE identifiers and is used to create the canonical/reference CVE identifier.

```c
csrc/kernel/hw/3rd_party_auth_key_ring.a:~/CVSS3/cvser.ips:~csrc/3rd_party_auth_key_ring/record.c:~csrc/kernel/hw/3rd_party_auth_key_ring.a:1702672411:2:0:0:AU:v1:/etc/dpkg/sources.list.d:99:u
```

The `csrc/tools/ps/auth_obj_uniq_check/uniq_eval_x86-64` script generated `csrc/qemu/ps/fscheck_auth_uniq.sh` to verify that the determined uniq domain name is correct.

```bash
Code-signing process not secure, your copy may be illegitimate...
Virus signature version detected : 2012-12-18
Modify signature type : ESAC
Sign your copy using various methods:3dc
In this process, we use them...
```

Note that the value in the `csrc/tools/ps/auth_obj_uniq_check/uniq_eval_x86-64` script may vary based on the specific installation and modifications performed. For example, if these changes are made to the `csrc/kernel/hw` directory, the value in that file may be different.

```bash
CODE SIGNING PROCESS NOT SECURE, YOUR COPY MAY BE ILLEGITIMATE...
IN THIS PROCESS WE USE QUDSOFT CERT CAKE.
```

Page 26/31. Extract all text exactly:

**1.136**

**unreasonable risk**

risk (1.99) judged to be unacceptable in a certain context according to valid societal moral concepts page 24/31:

**1.137**

**verification**

determination of completeness and correct specification or implementation of requirements from a phase (1.89) or subphase (1.128) page 24/31:

**1.138**

**verification review**

verification (1.137) activity to ensure that the result of a development activity fulfils the project requirements, or technical requirements, or both page 27/41:

NOTE 1 Individual requirements on verification reviews are given in specific clauses of individual parts of ISO 26262. page 27/41:

NOTE 2 The goal of verification reviews is technical correctness and completeness of the item (1.69) or element (1.32) with respect to use cases and failure modes (1.40). page 27/41:

**1.139**

**walk-through**

systematic examination of work products (1.142) in order to detect anomalies page 28/41:

NOTE 1 Walk-through is a means of verification (1.137). page 28/41:

NOTE 2 Walk-through differs from testing (1.134) in that it does not normally involve the operation of the associated item (1.69) or element (1.32). page 28/41:

NOTE 3 Any anomalies that are detected are usually addressed by rework, followed by a walk-through of the reworked work products. page 70/202:

Each tool configuration is reviewed and used for further development. page 23/41:

EXAMPLE During a walk-through, the developer explains the work product step-by-step to one or more assessors. The objective is to create a common understanding of the work product and to identify any anomalies within the work product. Both inspections (1.67) and walk-throughs are types of peer review (1.98), where a walk-through is a less stringent form of peer review than an inspection. page 28/107:

**1.140**

NOTE 3 Any anomalies that are detected are usually addressed by rework, followed by a walk-through of the reworked work products. page 70/202:

Each tool configuration is reviewed and used for further development. page 23/41:

EXAMPLE During a walk-through, the developer explains the work product step-by-step to one or more assessors. The objective is to create a common understanding of the work product and to identify any anomalies within the work product. Both inspections (1.67) and walk-throughs are types of peer review (1.98), where a walk-through is a less stringent form of peer review than an inspection. page 28/107:

**1.140**

**warning and degradation concept**

specification of how to alert the driver of potentially reduced functionality and of how to provide this reduced functionality to reach a safe state (1.102) pages 28/107 to 28/41:

**1.141**

**well-trusted**

previously used without known safety (1.103) anomalies (1.2) pages 28/107 to 29/29:

EXAMPLE well-trusted design principle; well-trusted tool; well-trusted hardware component (1.15). page 29/29:

**1.142**

**work product**

result of one or more associated requirements of ISO 26262 pages 29/42:

NOTE A reference can be an independent document containing the complete information of a work product or a list of references to the complete information of a work product. page 30/42:

---

## 2 Abbreviated terms

| Term                  | Code                                               | Description                                                                   |
|-----------------------|------------------------------------------------------|-------------------------------------------------------------------------------|
| **ACC**               | Adaptive Cruise Control                               |                                                                       |
| **AEC**               | Automotive Electronics Council                      |                                                                       |

© ISO 2011 – All rights reserved

### Page 27

AIS Abbreviated Injury Scale

ASIC Application-Specific Integrated Circuit

ASIL Automotive Safety Integrity Level (see definition 1.6)

BIST Built-In Self-Test

CAN Controller Area Network

CCF Common Cause Failure (see definition 1.14)

COTS Commercial Off The Shelf

CPU Central Processing Unit

CRC Cyclic Redundancy Check

DC Diagnostic Coverage (see definition 1.25)

d.c. Direct Current

DIA Development Interface Agreement (see definition 1.24)

DSC Dynamic Stability Control

ECU Electronic Control Unit

EDC Error Detection and Correction

E/E system Electrical and/or Electronic system (see definition 1.31)

EMC Electromagnetic Compatibility

EMI Electromagnetic Interference

ESD Electrostatic Discharge

ESC Electronic Stability Control

ETA Event Tree Analysis

FPGA Field Programmable Gate Array

FIT Failures In Time

FMEA Failure Mode and Effects Analysis

FTA Fault Tree Analysis

HAZOP HAZard and Operability analysis

HSI Hardware-Software Interface

HW Hardware

H&R Hazard analysis and Risk assessment (see definition 1.58)

IC Integrated Circuit

I/O Input – Output

MC/DC Modified Condition/Decision Coverage

MMU Memory Management Unit

### Page 32

just the ISO 2007

### Page 33

95. Comparison of the adsorption profiles of Korean red and Korean blue Senmyoji granules with first adsorption experiments of Senmyoji with the same formulations. Adsorption profiles of the clean Senmyoji granules are shown in Figure S5a–f. Adapted from Palabinger, J et al., Journal of Pharmaceutics and Biopharmaceutics, 2016, 104: 67–73.
This page was downloaded from the Elsevier Ltd site. The information provided in this article was accurate at the time of publication and has not been updated.
© 0000 Elsevier Ltd. All rights reserved.

1673-037x(0000)104:1 $40.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 104 D Q2

http://www.elsevier.com/locate/jcbcarysunlimited, 1580-66

90. Over this period, the nanoengineered denatured allogenic kidney became an active player in clinical research, with an increasing number of publications annually. Adsorbed华西医院 blood (Left panel) and whole blood (Right panel) with the anti-D (red) and anti-mKNA dialysis (blue) oligosaccharides were previously reported for plasma derived D and mKNA.108 Fluorescence micrographs (side-view) of anti-D cells loaded macroporous hemoglobin (OH) polymers (red) or hemoglobin (blue) at 10 µg/mL anti-D concentration. Movements of these cells were measured at 1,500 × g for 250 s. Figure S2. Comparison of normalized microprocessor (nKM) and preconditioned D-free (band) hemoglobin (HB) before (Left) and after (Right) dialysis with human plasma supernatant

This page was downloaded from the Elsevier Ltd site. The information provided in this article was accurate at the time of publication and has not been updated.
© 0000 Elsevier Ltd. All rights reserved.

This page was downloaded from the Elsevier Ltd site. The information provided in this article was accurate at the time of publication and has not been updated.
© 0000 Elsevier Ltd. All rights reserved.

1673-037x(0000)104:1 $40.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 104 D Q2

1673-037x(0000)94:3 $33.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 94 D Q1

1669-863X(0000)94:3 $33.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 94 D Q1

7700-6309(0000)94:3 $40.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 94 D Q1

1673-037x(0000)90:1 $40.00. Request Permission
http://www.elsevier.com/locate/jcbcarysunlimited, May 4, 2014, Vol. 90 D Q1

https://s3mirror-a.scwmb.com/scw0323/papertools/scw0323094.pdf

### Page 34

value of paid content focuses on designing user interfaces that are straightforward to design and understand, intuitive and effortless to use.

Sometimes users are happy to pay a bit more for a product if that awareness makes the interaction with the product easier, or if the product expertise of the community is technical, so this intuitive understanding translates into popularity.

The Concept Curation Package works with any current aspect of the organization and doesn't steal time from staff for design research or the design of information architectures. Rather, it brings outsourced expertise on a temporary income stream.

The Concept Curation Package offers a flexible model that includes:

- Bi-led Curation Package grants by pulling an anonymized set of documents together to sponsor simple workshops in which people can begin working with the new previously known categories of documents.

This Annuity helps each Curation Package supporter get the exposure they need to develop a career in user research, product experience, or information architecture.

User-facing Service and Return can contribute the most value by understanding how LIFETIME ACCESS relates to the categories that emerge through deep collaboration.

## Introduction

### British Standards Institution (BSI)
BSI is the national body responsible for preparing British Standards and other standards-related publications, information and services.
BSI is incorporated by Royal Charter. British Standards and other standardization products are published by BSI Standards Limited.

### About us
We bring together business, industry, government, consumers, innovators and others to shape their combined experience and expertise into standards based solutions.

The knowledge embodied in our standards has been carefully assembled in a dependable format and refined through our open consultation process. Organizations of all sizes and across all sectors choose standards to help them achieve their goals.

### Information on standards
We can provide you with the knowledge that your organization needs to succeed. Find out more about British Standards by visiting our website at bsi-group.com/standards or contacting our Customer Services team or Knowledge Centre.

### Buying standards
You can buy and download PDF versions of BSI publications, including British and adopted European and international standards, through our website at bsigroup.com/shop, where hard copies can also be purchased.

If you need international and foreign standards from other Standards Development Organizations, hard copies can be ordered from our Customer Services team.

### Subscriptions
Our range of subscription services are designed to make using standards easier for you. For further information on our subscription products go to bsi-group.com/subscriptions.

With British Standards Online (BSOL) you’ll have instant access to over 55,000 British and adopted European and international standards from your desktop. It’s available 24/7 and is refreshed daily so you’ll always be up to date.

You can keep in touch with standards developments and receive substantial discounts on the purchase price of standards, both in single copy and subscription format, by becoming a **BSI Subscribing Member**.

**PLUS** is an updating service exclusive to BSI Subscribing Members. You will automatically receive the latest hard copy of your standards when they’re revised or replaced.

To find out more about becoming a BSI Subscribing Member and the benefits of membership, please visit bsi-group.com/shop.

With a **Multi-User Network Licence (MUNL)** you are able to host standards publications on your intranet. Licences can cover as few or as many users as you wish. With updates supplied as soon as they’re available, you can be sure your documentation is current. For further information, email bsmusales@bsigroup.com.

### BSI Group Headquarters
389 Chiswick High Road London W4 4AL UK

### Revisions
Our British Standards and other publications are updated by amendment or revision. We continually improve the quality of our products and services to benefit your business. If you find an inaccuracy or ambiguity within a British Standard or other BSI publication please inform the Knowledge Centre.

### Copyright
All the data, software and documentation set out in all British Standards and other BSI publications are the property of and copyrighted by BSI, or some person or entity that owns copyright in the information used (such as the international standardization bodies) and has formally licensed such information to BSI for commercial publication and use. Except as permitted under the Copyright, Designs and Patents Act 1988 no extract may be reproduced, stored in a retrieval system or transmitted in any form or by any means – electronic, photocopying, recording or otherwise – without prior written permission from BSI. Details and advice can be obtained from the Copyright & Licensing Department.

### Useful Contacts:
- **Customer Services**
  - Tel: +44 845 086 9001
  - **Email (orders):** orders@bsigroup.com
  - **Email (enquiries):** cservices@bsigroup.com
- **Subscriptions**
  - Tel: +44 845 086 9001
  - **Email:** subscriptions@bsigroup.com
- **Knowledge Centre**
  - Tel: +44 20 8996 7004
  - **Email:** knowledgecentre@bsigroup.com
- **Copyright & Licensing**
  - Tel: +44 20 8996 7070
  - **Email:** copyright@bsigroup.com

...making excellence a habit.

BSI | the London Stock Exchange | 100 Victoria Street | London, England | SW1E 5FT