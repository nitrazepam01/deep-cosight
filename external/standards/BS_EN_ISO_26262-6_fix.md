### Page 3

Road vehicles — Functional safety — Part 6: Product development at the software level

_Véhicules routiers — Sécurité fonctionnelle —_
_Partie 6: Développement du produit au niveau du logiciel_

Reference number
ISO 26262-6:2011(E)

© ISO 2011

First edition
2011-11-15

### Page 4

© 2011 ISO. All rights reserved. Unless otherwise specified, no part of this publication may be reproduced or utilized in any form or by any means, electronic or mechanical, including photocopying and microfilm, without permission in writing from either ISO at the address below or ISO's member body in the country of the requester.

### Page 5

Contents

Foreword vi

Introduction vi

1 Scope 1

2 Normative references 2

3 Terms, definitions and abbreviated terms 2

4 Requirements for compliance 2

4.1 General requirements 2

4.2 Interpretations of tables 2

4.3 ASIL-dependent requirements and recommendations 3

5 Initiation of product development at the software level 3

5.1 Objectives 3

5.2 General 3

5.3 Inputs to this clause 4

5.4 Requirements and recommendations 4

5.5 Work products 6

6 Specification of software safety requirements 6

6.1 Objectives 6

6.2 General 7

6.3 Inputs to this clause 7

6.4 Requirements and recommendations 7

6.5 Work products 9

7 Software architectural design 9

7.1 Objectives 9

7.2 General 9

7.3 Inputs to this clause 9

7.4 Requirements and recommendations 10

7.5 Work products 15

8 Software unit design and implementation 15

8.1 Objectives 15

8.2 General 15

8.3 Inputs to this clause 16

8.4 Requirements and recommendations 16

8.5 Work products 18

9 Software unit testing 19

9.1 Objectives 19

9.2 General 19

9.3 Inputs to this clause 19

9.4 Requirements and recommendations 19

9.5 Work products 21

10 Software integration and testing 22

10.1 Objectives 22

10.2 General 22

10.3 Inputs to this clause 22

10.4 Requirements and recommendations 23

10.5 Work products 25

11 Verification of software safety requirements 25

### Page 7

**Foreword**

ISO (the International Organization for Standardization) is a worldwide federation of national standards bodies (ISO member bodies). The work of preparing International Standards is normally carried out through ISO technical committees. Each member body interested in a subject for which a technical committee has been established has the right to be represented on that committee. International organizations, governmental and non-governmental, in liaison with ISO, also take part in the work. ISO collaborates closely with the International Electrotechnical Commission (IEC) on all matters of electrotechnical standardization.

International Standards are drafted in accordance with the rules given in the ISO/IEC Directives, Part 2.

The main task of technical committees is to prepare International Standards. Draft International Standards adopted by the technical committees are circulated to the member bodies for voting. Publication as an International Standard requires approval by at least 75 % of the member bodies casting a vote.

Attention is drawn to the possibility that some of the elements of this document may be the subject of patent rights. ISO shall not be held responsible for identifying any or all such patent rights.

ISO 26262-6 was prepared by Technical Committee ISO/TC 22, *Road vehicles*, Subcommittee SC 3, *Electrical and electronic equipment*.

ISO 26262 consists of the following parts, under the general title *Road vehicles— Functional safety*:

- Part 1: *Vocabulary*
- Part 2: *Management of functional safety*
- Part 3: *Concept phase*
- Part 4: *Product development at the system level*
- Part 5: *Product development at the hardware level*
- Part 6: *Product development at the software level*
- Part 7: *Production and operation*

IIS 6.0 Fields Bylets p.1

ISO 26308:2004

## English: English

 Русийцка

 Български

 Русский
 | Polski

 Български (2.6.31607)

 Svenska (52-22-26)

 8.16.36635

 Deutsch (161-256)

 فارسی (89-7405)

 Italiano (94-210)

### Page 11

#### Part 6: Product development at the software level

ISO 26262 is intended to be applied to safety-related systems that include one or more electrical and/or

electronic (E/E) systems and

Ey Electro Magneti c M. system in special purpose vehicles

Machined parts and elec. expendable parts of various Tire and O

systems and their components already under

development prior to the publication stage. For further

System and their components released for production, or systems and their components already under

development prior to the publication date of ISO 26262, are exempted from the scope. For further

development or alterations based on systems and their components released for production prior to the

publication of ISO 26262. only the modifications will be developed in accordance with ISO 26262.

### Page 12

a consecutive entry (marked by a sequence number in the leftmost column, e.g. 1, 2, 3), or

a) a consecutive entry (marked by a sequence number in the leftmost column, e.g. 1, 2, 3), or

b) a non-consecutive entry (marked by a sequence number in the leftmost column, e.g. 1,2,3), or

c) a reporting based entry (marked by a sequence number in the leftmost column, e.g. 1, 2, 3 or 4 or 5).

2.3 Information -2.1.

Normative references: this document are indispensable for the application of this document. For dated references, only the edition cited applies. For undated references, the latest edition of the referenced document (including any amendments) applies.

ISO 26262-1:2011, Road vehicles — Functional safety — Part 1: Vocabulary.

ISO 26262-2:2011, Road vehicles — Functional safety — Part 2: Management of functional safety.

ISO 26262-4:2011, Road vehicles — Functional safety — Part 4: Product development at the system level.

ISO 26262-5:2011, Road vehicles — Functional safety — Part 5: Product development at the hardware level.

ISO 26262-8:2011, Road vehicles — Functional safety — Part 8: Supporting processes.

ISO 26262-9:2011, Road vehicles — Functional safety — Part 9: Automotive Safety Integrity Level (ASIL)-oriented and safety-oriented analyses.

3 Terms - Definitions and abbreviated terms

For the purposes of this document, the terms, definitions and abbreviated terms given in ISO 26262-1:2011 apply.

4 Requirements for compliance

4.1 General requirements

When claiming compliance with ISO 26262, each requirement shall be complied with, unless one of the following applies:

- tailoring of the safety activities in accordance with ISO 26262-2 has been planned and shows that the requirement does not apply, or
- a rationale is available that the non-compliance is acceptable and the rationale has been assessed in accordance with ISO 26262-2.

Information marked as "NOTE" or "EXAMPLE" is only for guidance in understanding, or for clarification of the associated requirement, and shall not be interpreted as a requirement itself or as complete or exhaustive.

The results of safety activities are given as work products. "Prerequisites" are information which shall be available as work products of a previous phase. Given that certain requirements of a clause are ASIL-dependent or may be tailored, certain work products may not be needed as prerequisites.

"Further supporting information" is information that can be considered, but which in some cases is not required by ISO 26262 as a work product of a previous phase and which may be made available by external sources that are different from the persons or organizations responsible for the functional safety activities.

4.2 Interpretations of tables

Tables are normative or informative depending on their context. The different methods listed in a table contribute to the level of confidence in achieving compliance with the corresponding requirement. Each method in a table is either

- a consecutive entry (marked by a sequence number in the leftmost column, e.g. 1, 2, 3), or

1. Initialization table SL-TBLETA01 the limit LTIMS shall have SL-FMT or LT-IS for the illustration and the acronym shall SAB-TBLETA10.

### Page 13

b) - an alternative entry (marked by a number followed by a letter in the leftmost column, e.g. 2a, 2b, 2c). For consecutive entries, all methods shall be applied as recommended in accordance with the ASIL. If methods other than those listed are to be applied, a rationale shall be given that these fulfil the corresponding requirement.

For alternative entries, an appropriate combination of methods shall be applied in accordance with the ASIL indicated, independent of whether they are listed in the table or not. If methods are listed with different degrees of recommendation for an ASIL, the methods with the higher recommendation should be preferred. A rationale shall be given that the selected combination of methods complies with the corresponding requirement.

NOTE A rationale based on the methods listed in the table is sufficient. However, this does not imply a bias for or against methods not listed in the table.

For each method, the degree of recommendation to use the corresponding method depends on the ASIL and is categorized as follows:

- "++" indicates that the method is highly recommended for the identified ASIL;
- "+" indicates that the method is recommended for the identified ASIL;
- "o" indicates that the method has no recommendation for or against its usage for the identified ASIL.

4.3 ASIL-dependent requirements and recommendations

The requirements or recommendations of each subclass shall be complied with for ASIL A, B, C and D, if not stated otherwise. These requirements and recommendations refer to the ASIL of the safety goal. If ASIL decomposition has been performed at an earlier stage of development, in accordance with ISO 26262-9:2011, Clause 5, the ASIL resulting from the decomposition shall be complied with.

If an ASIL is given in parentheses in ISO 26262, the corresponding subclass shall be considered as a recommendation rather than a requirement for this ASIL. This has no link with the parenthesis notation related to ASIL decomposition.

5 Initiation of product development at the software level

5.1 Objectives

The objective of this sub-phase is to plan and initiate the functional safety activities for the sub-phases of the software development.

5.2 General

The initiation of the software development is a planning activity, where software development sub-phases and their supporting processes (see ISO 26262-8 and ISO 26262-9) are determined and planned according to the extent and complexity of the item development. The software development sub-phases and supporting processes are initiated by determining the appropriate methods in order to comply with the requirements and their respective ASIL. The methods are supported by guidelines and tools, which are determined and planned for each sub-phase and supporting process.

NOTE Tools used for software development can include tools other than software tools.

EXAMPLE Tools used for testing phases.

The planning of the software development includes the coordination with the product development at the system level (see ISO 26262-4) and the hardware level (see ISO 26262-5).

### Page 14

5.3 Inputs to this clause

5.3.1 Prerequisites

The following information shall be available:

- project plan (refined) in accordance with ISO 26262-4:2011, 5.5.1;
- safety plan (refined) in accordance with ISO 26262-4:2011, 5.5.2;
- technical safety concept in accordance with ISO 26262-4:2011, 7.5.1;
- system design specification in accordance with ISO 26262-4:2011, 7.5.2; and
- item integration and testing plan (refined) in accordance with ISO 26262-4:2011, 8.5.1.

5.3.2 Further supporting information

The following information can be considered:

- qualified software tools available (see ISO 26262-8:2011, Clause 11);
- qualified software components available (see ISO 26262-8:2011, Clause 12);
- design and coding guidelines for modelling and programming languages (from external source);
- guidelines for the application of methods (from external source); and
- guidelines for the application of tools (from external source).

5.4 Requirements and recommendations

5.4.1 The activities and the determination of appropriate methods for the product development at the software level shall be planned.

5.4.2 The tailoring of the lifecycle for product development at the software level shall be performed in accordance with ISO 26262-2:2011, 6.4.5, and based on the reference phase model given in Figure 2.

5.4.3 If developing configurable software, Annex C shall be applied.

5.4.4 The software development process for the software of an item, including lifecycle phases, methods, languages and tools, shall be consistent across all the sub-phases of the software lifecycle and be compatible with the system and hardware development phases, such that the required data can be transformed correctly.

NOTE The sequencing of phases, tasks and activities, including iteration steps, for the software of an item is to ensure the consistency of the corresponding work products with the product development at the hardware level (see ISO 26262-5) and the product development at the system level (see ISO 26262-4).

### Page 15

Results of My Attempts

compromise between expressiveness and effectiveness. The research with strings demonstrates the advantages of dynamic programming algorithms.
the subtractive algorithm where it relates substring problems to the set strings. It still works with usually very long input under $K$-substring, $n$-length strings.
Anyway, it needs random of access memory.
STEVID小学校本subtract _代码
/
Example : The method that describes the subtractive way to calculate the SCS to a English.
I generate $A$ that can enter each time $2^{n}-1$ strings. $L$*= 0.
SIMPLIFY LB
#code
// constant
int L
U
a = s
3) for each of the substrings of strings, we loop by each of the substrings of S.
string S
SELECT a => b assume LIUS a = b
> 3) we loop n 1 variables.
note _{let_}$
Ans

### Page 16

## 5.4.7 To support the correctness of the design and implementation, the design and coding guidelines for the modelling, or programming languages, shall address the topics listed in Table 1.

### NOTE 1
Coding guidelines are usually different for different programming languages.

### NOTE 2
Coding guidelines can be different for model-based development.

### NOTE 3
Existing coding guidelines can be modified for a specific item development.

### EXAMPLE
MISRA C(3) and MISRA AC AGC(4) are coding guidelines for the programming language C.

### Table 1 — Topics to be covered by modelling and coding guidelines

| Topics                                                                 | ASIL |
|--------------------------------------------------------------------------|------|
| 1a Enforcement of low complexitya                                       | +++  |
| 1b Use of language subsetsb                                          | +++  |
| 1c Enforcement of strong typingc                                      | +++  |
| 1d Use of defensive implementation techniques                         | ++   |
| 1e Use of established design principles                                  | +    |
| 1f Use of unambiguous graphical representation                        | +    |
| 1g Use of style guides                                                | ++   |
| 1h Use of naming conventions                                           | ++   |

a An appropriate compromise of this topic with other methods in this part of ISO 26262 may be required.

b The objectives of method 1b are

— Exclusion of ambiguously defined language constructs which may be interpreted differently by different modellers, programmers, code generators or compilers.
— Exclusion of language constructs which from experience easily lead to mistakes, for example assignments in conditions or identical naming of local and global variables.
— Exclusion of language constructs which could result in unhandled run-time errors.

c The objective of method 1c is to impose principles of strong typing where these are not inherent in the language.

### 5.5 Work products

#### 5.5.1 Safety plan (refined)*
resulting from requirements 5.4.1 to 5.4.7.

#### 5.5.2 Software verification plan*
resulting from requirements 5.4.1 to 5.4.5 and 5.4.7.

#### 5.5.3 Design and coding guidelines for modelling and programming languages*

— Exclusion of ambiguously defined language constructs which may be interpreted differently by different modellers, programmers, code generators or compilers.
— Exclusion of language constructs which from experience easily lead to mistakes, for example assignments in conditions or identical naming of local and global variables.
— Exclusion of language constructs which could result in unhandled run-time errors.

c The objective of method 1c is to impose principles of strong typing where these are not inherent in the language.

### 5.5 Work products

#### 5.5.1 Safety plan (refined)*
resulting from requirements 5.4.1 to 5.4.7.

#### 5.5.2 Software verification plan*
resulting from requirements 5.4.1 to 5.4.5 and 5.4.7.

#### 5.5.3 Design and coding guidelines for modelling and programming languages*
resulting from requirements 5.4.6 and 5.4.7.

#### 5.5.4 Tool application guidelines*
resulting from requirements 5.4.5 and 5.4.6.

### 6 Specification of software safety requirements

#### 6.1 Objectives
The first objective of this sub-phase is to specify the software safety requirements. They are derived from the technical safety concept and the system design specification.

### Page 17

### Page 18

value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.2</STRING>Severity value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.3</STRING>Priority value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.4 </STRING>Description value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.1</STRING>Category value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.5 </STRING>Class value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.6 </STRING>Priority life, version value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.7</STRING>Specificity value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.8</STRING>New value field, type value instanceGuid, validationOp please do not save">Applying Modification the application.
// Configure domain domain value id="instanceGuid" STRING_PR="${INSTANCE_VARNAME}">2-11.9</STRING><CHECK AND CHOICES c_name= New mandatory value">installation the settings/configuration file version> "value displayed in the overview">2-11</STRING></CHECK></Checklists>
This is generated by a C# code, run C# class Or CLR class.
public static void Call(class class2 field</INT2粳goto> >-val1= {@name = "SOMETHING"</STRING></INT2和工作进的Web Site">c_name4/val2= {@name = "OTHERNAME"下方的与c_name的工作日に"</DS>location="ft:///c_profile?p=val3"delta_created="iOS 2016-22">方法名称">val4= {@name = "VAL3".</INT2><arean">} </DS></INT2></STRING></CHECKEND

### Page 19

value https://books.emathinstruction.com Then the accuracy level was changed a requirement in favor of the objectives - relative to the level of “relevant proficiencies” achieved. Respondents were given the following description of requirements: $$\begin{align*} &\text{Rev 1 Stability and Reliability VII} vs. \\ &\text{Rev 2 Process Safety} vs. \\ &\text{Design Control V} vs. \end{align*}$$

'Once we understand that students don't know every single word or phrase in every word in one of our questions, we started thinking about what we can accomplish to help them deploy all of those notions.' Also, he encourages them to persist through the hard times—'sometimes we learn there's a reading level that society just feels is appropriate for everybody, and if we skip over lower-level readers, we miss it.

'But we'd better also get over the idea that if a reader can't make any sense out of something that we just read, then he or she probably isn't ready to learn to read...If we miss that point, which is not addressing the reader, we've potentially widened the gap between readers and nonreaders.' Similarly, he discusses the notion that grammar and spellers 'are not the enemy'—a brick wall manufacturers use to try to maintain their dominance—as each promote themselves as being able 'to detect a problem in another way that they didn't before.' On the other hand, Chelsea, who came to the fifth-grade reading program as a 'universal transition group', says she noticed a shift in the language acquisition process when the first grade readers arrived:

"I have a hard time finding that loading zone that you have in middle school when the kids stop knowing how a sports car works. Once they take them out and they come in with, ‘I don't know which syllable this word starts with,' even so, to try and improve that phase of learning, at some point, you're going to have to teach that,' she says. Based on my experience, you don't know if the student has enough automaticity yet to read—and once you get to say, 'I understand this and this and then I'd like to do this,' it's a whole different thing that we have to take on board.

'It's a whole other process a little more complex than just filling out a worksheet about reading,' she says. 'The main idea—that's not a really easy thing for kids at any age—you want to take a student, if you know, really engage with them, through authentic applications, through pulling all of those ideas together...'

### 6.5 Work products

##### 6.5.1 **Software safety requirements specification** resulting from requirements 6.4.1 to 6.4.3 and 6.4.5.

##### 6.5.2 **Hardware-software interface specification (refined)** resulting from requirement 6.4.4.

NOTE This work product refers to the same work product as given in ISO 26262-5:2011 6.5.2

##### 6.5.3 **Software verification plan (refined)** resulting from requirement 6.4.6.

##### 6.5.4 **Software verification report** resulting from requirements 6.4.7 and 6.4.8.

#### 7 **Software architectural design**

##### 7.1 **Objectives**

The first objective of this sub-phase is to develop a software architectural design that realizes the software safety requirements.

The second objective of this sub-phase is to verify the software architectural design.

##### 7.2 **General**

The software architectural design represents all software components and their interactions in a hierarchical structure. Static aspects, such as interfaces and data paths between all software components, as well as dynamic aspects, such as process sequences and timing behaviour are described.

NOTE The software architectural design is not necessarily limited to one microcontroller or ECU, and is related to the technical safety concept and system design. The software architecture for each microcontroller is also addressed by this chapter.

In order to develop a software architectural design both software safety requirements as well as all non-safety-related requirements are implemented. Hence in this sub-phase safety-related and non-safety-related requirements are handled within one development process.

The software architectural design provides the means to implement the software safety requirements and to manage the complexity of the software development.

##### 7.3 **Inputs to this clause**

###### 7.3.1 **Prerequisites**

The following information shall be available:

- safety plan (refined) in accordance with 5.5.1;

- design and coding guidelines for modelling and programming languages in accordance with 5.5.3;

- hardware-software interface specification in accordance with ISO 26262-4:2011, 7.5.3;

- software safety requirements specification in accordance with 6.5.1;

- software verification plan (refined) in accordance with 6.5.3; and

- software verification report in accordance with 6.5.4.

### Page 20

demand clause.7.3.2 Further supporting information

The following information can be considered:

- technical safety concept (see ISO 26262-4:2011, 7.5.1);
- system design specification (see ISO 26262-4:2011, 7.5.2);
- qualified software components available (see ISO 26262-8:2011, Clause 12);
- complete system design documents;
- any design changes to the supply chain;
- any changes to the system or software that require an update;
- directives and requirements to be applied to the system or software;
- certification documents or certifications or other information required by the systems;
- optimization of the system;
- any changes to design configuration data;
- Vitrek-GT 1.3.1 revision 1.5, Release April 2017;
- any validation or certification documents included in the system;
- any validation or certification documents resolved or not resolved during the testing and
  certification/validation process, or documents resolved or not resolved during regulatory
  inspections or enforcement activities of the system;
- any training manuals;
- any other quality documents related to the system.
- ASIL codes as assigned by the downstream industry or regulatory agency.

7.4 Requirements and recommendations

7.4.1 To ensure that the software architectural design captures the information necessary to allow the subsequent development activities to be performed correctly and effectively, the software architectural design shall be described with appropriate levels of abstraction by using the notations for software architectural design listed in Table 2.

**Table 2 — Notations for software architectural design**

| Methods                                                                 | ASIL A | B   | C  | D  |
|-------------------------------------------------------------------------|-------|----|----|----|
| 1a Informal notations                                                    | ++    | ++ | +  | +  |
| 1b Semi-formal notations                                                | +     | ++ | ++| ++ |
| 1c Formal notations                                                        | +     | +  | +  | +  |

7.4.2 During the development of the software architectural design the following shall be considered:

a) the verifiability of the system software architectural design;

NOTE This implies bi-directional traceability between the system software architectural design and the software safety requirements.

b) the suitability for configurable software;

c) the feasibility for the design and implementation of the software units;

d) the testability of the software architecture during system testing and;

e) the maintainability of the software architectural design.

7.4.3 In order to avoid failures resulting from high complexity, the software architectural design shall exhibit the following properties by use of the principles listed in Table 3:

a) modularity;

b) encapsulation; and

c) simplicity.

### Page 21

value placed upon Muslim generosity in争端.

### Tables

| Methods                                                                 | ASIL A | B   | C   | D   | 
|-------------------------------------------------------------------------|--------|-----|-----|-----| 
| **Hierarchical structure of software components**                        | +++    | ++ | ++ | ++ |
| **Restricted size of software components**                               | ++    | ++ | ++ | ++ |
| **Restricted size of interfaces**                                         | ++    |    | ++ | ++ |
| **High cohesion within each software component**                         | ++    | ++ | ++ | ++ |
| **Restricted coupling between software components**                     | +++    | ++ | ++ | ++ |
| **Appropriate scheduling properties**                                   | ++    | ++ | ++ | ++ |
| **Restricted use of interrupts**                                         | +      | +  | +  | ++ |

---

a In methods 1b, 1c, 1e and 1g "restricted" means to minimize in balance with other design considerations.

b Methods 1d and 1e can, for example, be achieved by separation of concerns which refers to the ability to identify, encapsulate, and manipulate those parts of software that are relevant to a particular concept, goal, task, or purpose.

c Method 1e addresses the limitation of the external coupling of software components.

d Any interrupts used have to be priority-based.

NOTE An appropriate compromise between the methods listed in Table 3 can be necessary since the methods are not mutually exclusive.

### 7.4.4 The software architectural design shall be developed down to the level where all software units are identified.

### 7.4.5 The software architectural design shall describe:

1. a) the static design aspects of the software components; and

2. NOTE 1 Static design aspects address:

   a) the software structure including its hierarchical levels;

   b) the logical sequence of data processing;

   c) the data types and their characteristics;

   d) the external interfaces of the software components;

   e) the external interfaces of the software; and

   f) the constraints including the scope of the architecture and external dependencies.

NOTE 2 In the case of model-based development, modelling the structure is an inherent part of the overall modelling activities.

b The dynamic design aspects of the software components.

NOTE 1 Dynamic design aspects address:

a the functionality and behaviour;

b the control flow and concurrency of processes;

c the data flow between the software components;

NOTE In general the operating system provides or supports software partitioning.

d) the verification of the software partitioning during software integration and testing (in accordance with
Clause 10) is performed.

**7.4.12 An analysis of dependent failures in accordance with ISO 26262-9:2011, Clause 7, shall be carried**
out if the implementation of software safety requirements relies on freedom from interference or sufficient
independence between software components.

**7.4.13 Safety analysis shall be carried out at the software architectural level in accordance with**
ISO 26262-9:2011, Clause 8, in order to:

— identify or confirm the safety-related parts of the software; and

— support the specification and verify the efficiency of the safety mechanisms.

NOTE Safety mechanisms can be specified to cover both issues associated with random hardware failures as well as
software faults.

**7.4.14 To specify the necessary software safety mechanisms at the software architectural level, based on**
the results of the safety analysis in accordance with 7.4.13, mechanisms for error detection as listed in
Table 4 shall be applied.

NOTE When not directly required by technical safety requirements allocated to software, the use of software safety
mechanisms is reviewed at the system level to analyse the potential impact on the system behaviour.

**Table 4 — Mechanisms for error detection at the software architectural level**

|Methods|ASIL|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
||A|B|C|D||
|1a Variable ranges of feedback inputs and output data|++|++|++|++||
|1b Plausibility checka|+|+|+|++||
|1c Detection of data errorsb|+|+|+|+||
|1d External monitoring facilityc|O||+|++||
|1e Internal control flow monitoring|O|+|++|++||
|1f Diverse software design|O|O|+|++||
|a Plausibility checks can include using a reference model of the desired behaviour, assertion checks, or comparing signals from different sources. b Types of methods that may be used to detect data errors include error detecting codes and multiple data storage. c An external monitoring facility can be, for example, an ASIC or another software element performing a watchdog function.||||||


**7.4.15 This subclause applies to ASIL (A), (B), C and D, in accordance with 4.3: to specify the necessary**
software safety mechanisms at the software architectural level, based on the results of the safety analysis in
accordance with 7.4.13, mechanisms for error handling as listed in Table 5 shall be applied.

NOTE When not directly required by technical safety requirements allocated to software, the use of software safety
mechanisms is reviewed at the system level to analyse the potential impact on the system behaviour.

NOTE The analysis at software architectural level of possible hazards due to hardware is described in ISO 26262-5.

### Page 24

value of the logistics operations from the supplier.7.4.16 If new hazards introduced by the software architectural design are not already covered by an existing safety goal, they shall be introduced and evaluated in the hazard analysis and risk assessment in accordance with the change management process in ISO 26262-8:2011, Clause 8.

Note Newly identified hazards, not already reflected in a safety goal, are usually non-functional hazards. If those non-functional hazards are outside the scope of this standard then it is recommended that they be annotated in the hazard analysis and risk assessment with the following statement “No ASIL is assigned to this hazard as it is not within the scope of ISO 26262.” However, an ASIL is allowed for reference purposes.

7.4.17 An upper estimation of required resources for the embedded software shall be made, including:

a) the execution time;

b) the storage space; and

EXAMPLE RAM for stacks and heaps, ROM for program and non-volatile data.

c) the communication resources.

7.4.18 The software architectural design shall be verified in accordance with ISO 26262-8:2011, Clause 9, and by using the software architectural design verification methods listed in Table 6 to demonstrate the following properties:

a) compliance with the software safety requirements;

b) compatibility with the target hardware; and

NOTE This includes the resources as specified in 7.4.17.

c) adherence to design guidelines.

### Page 25

Table 6 – Methods for the verification of the software architectural design

| Methods  | A | B | C | D |
| — | — | — | — | — |
| 1a | Walk-through of the design | ++ | + | O | O |
| 1b | Inspection of the design | + | ++ | ++ | ++ |
| 1c | Simulation of dynamic parts of the design | + | + | + | ++ |
| 1d | Prototype generation | O | O | ++ | ++ |
| 1e | Formal verification | O | O | + | + |
| 1f | Control flow analysis | + | + | ++ | ++ |
| 1g | Data flow analysis | + | + | ++ | ++ |

a. In the case of model-based development these methods can be applied to the model.

b. Method 1c requires the usage of executable models for the dynamic parts of the software architecture.

c. Control and data flow analysis may be limited to safety-related components and their interfaces.

### 7.5 Work products

#### 7.5.1 Software architectural design specification
resulting from requirements 7.4.1 to 7.4.6, 7.4.9, 7.4.10, 7.4.14, 7.4.15 and 7.4.17.

#### 7.5.2 Safety plan (refined)
resulting from requirement 7.4.7.

#### 7.5.3 Software safety requirements specification (refined)
resulting from requirement 7.4.9.

#### 7.5.4 Safety analysis report
resulting from requirement 7.4.13.

#### 7.5.5 Dependent failures analysis report
resulting from requirement 7.4.12.

#### 7.5.6 Software verification report (refined)
resulting from requirement 7.4.18.

### 8 Software unit design and implementation

#### 8.1 Objectives

The first objective of this sub-phase is to specify the software units in accordance with the software architectural design and the associated software safety requirements.

The second objective of this sub-phase is to implement the software units as specified.

The third objective of this sub-phase is the static verification of the design of the software units and their implementation.

#### 8.2 General

Based on the software architectural design, the detailed design of the software units is developed. The detailed design will be implemented as a model or directly as source code, in accordance with the modelling or coding guidelines respectively. The detailed design and the implementation are statically verified before proceeding to the software unit testing phase. The implementation-related properties are achievable at the source code level if manual code development is used. If model-based development with automatic code generation is used, these properties apply to the model and need not apply to the source code.

In order to develop a single software unit design both software safety requirements as well as all non-safety-related requirements are implemented. Hence in this sub-phase safety-related and non-safety-related requirements are handled within one development process.

### Page 26

The implementation of the software units includes the generation of source code and the translation into object code.

8.3 Inputs to this clause

8.3.1 Prerequisites

The following information shall be available:

— design and coding guidelines for modelling and programming languages in accordance with 5.5.3;

— software verification plan (refined) in accordance with 6.5.3;

— software architectural design specification in accordance with 7.5.1;

— safety plan (refined) in accordance with 7.5.2;

— software safety requirements specification (refined) in accordance with 7.5.3; and

— software verification report (refined) in accordance with 7.5.6.

8.3.2 Further supporting information

The following information can be considered:

— technical safety concept (see ISO 26262-4:2011, 7.5.1);

— system design specification (see ISO 26262-4:2011, 7.5.2);

— tool application guidelines in accordance with 5.5.4;

— hardware-software interface specification (refined) (see 6.5.2);

— safety analysis report in accordance with 7.5.4; and

— guidelines for the application of methods (from external source).

8.4 Requirements and recommendations

8.4.1 The requirements of this subclause shall be complied with if the software unit is safety-related.

NOTE “Safety-related” means that the unit implements safety requirements, or that the criteria for coexistence (see ISO 26262-9:2011, Clause 6) of the unit with other units are not satisfied.

8.4.2 To ensure that the software unit design captures the information necessary to allow the subsequent development activities to be performed correctly and effectively, the software unit design shall be described using the notations listed in Table 7.

Table 7 — Notations for software unit design

| Methods | A | B | D |
| ------- | - | - | - |
| 1a    | Natural language | ++ | ++ | ++ | ++ |
| 1b    | Informal notations | ++ | ++ | ++ | + |
| 1c    | Semi-formal notations | + | ++ | ++ | ++ |

8.4.1 The requirements of this subclause shall be complied with if the software unit is safety-related.

NOTE “Safety-related” means that the unit implements safety requirements, or that the criteria for coexistence (see ISO 26262-9:2011, Clause 6) of the unit with other units are not satisfied.

8.4.2 To ensure that the software unit design captures the information necessary to allow the subsequent development activities to be performed correctly and effectively, the software unit design shall be described using the notations listed in Table 7.

Table 7 — Notations for software unit design

| Methods | A | B | D |
| ------- | - | - | - |
| 1a    | Natural language | ++ | ++ | ++ | ++ |
| 1b    | Informal notations | ++ | ++ | ++ | + |
| 1c    | Semi-formal notations | + | ++ | ++ | ++ |
| 1d    | Formal notations | + | + | + | + |

### Page 27

\begin{table}
  \begin{tabular}{l l l l l l}
    \hline
    & \textbf{Methods} & \textbf{ASIL} & & & \\
    & & A & B & C & D \\
    \hline
    1a & One entry and one exit point in subprograms and functions\textsuperscript{a} & ++ & ++ & ++ & ++ \\
    \hline
    1b & No dynamic objects or variables, or else online test \(\text{during}\) their \(\text{creation}^{\text{a,b}}\) & ++ & ++ & ++ & ++ \\
    \hline
    1c & Initialization of variables & ++ & ++ & ++ & ++ \\
    \hline
    1d & No multiple use of variable names\textsuperscript{a} & ++ & ++ & ++ & ++ \\
    \hline
    1e & Avoid global variables or else justify their usage\textsuperscript{a} & + & + & ++ & ++ \\
    \hline
    1f & Limited use of pointers\textsuperscript{a} & + & + & + & ++ \\
    \hline
    1g & No implicit type conversions\textsuperscript{a,b} & + & ++ & ++ & ++ \\
    \hline
    1h & No hidden data flow or control flow\textsuperscript{c} & + & + & ++ & ++ \\
    \hline
    1i & No unconditional jumps\textsuperscript{a,b,c} & ++ & +++ & +++ & +++ \\
    \hline
    1j & No recursions & + & + & +++ & +++ \\
    \hline
    \multicolumn{6}{l}{a\textsuperscript{Methods 1a, 1b, 1d, 1e, 1f, 1g and 1i may not be applicable for graphical modelling notations used in model-based development.} \\
    \multicolumn{6}{l}{b\textsuperscript{Methods 1g and 1i are not applicable in assembler programming.}} \\
    \multicolumn{6}{l}{c\textsuperscript{Methods 1h and 1i reduce the potential for modelling data flow and control flow through jumps or global variables.}} \\
    \hline
  \end{tabular}
\end{table}

\small

NOTE In the case of model-based development with automatic code generation, the methods for representing the software unit design are applied to the model which serves as the basis for the code generation.

\subsection*{8.4.3 The specification of the software units shall describe the functional behaviour and the internal design to the level of detail necessary for their implementation.}

\begin{exeuaDecen}
Internal design can include constraints on the use of registers and storage of data.
\end{exeuaDecen}

\subsection*{8.4.4 Design principles for software unit design and implementation at the source code level as listed in Table 8 shall be applied to achieve the following properties:}

\begin{itemize}
  \item correct order of execution of subprograms and functions within the software units, based on the software architectural design;
  \item consistency of the interfaces between the software units;
  \item correctness of data flow and control flow between and within the software units;
  \item simplicity;
  \item readability and comprehensibility;
  \item robustness;
\end{itemize}

\begin{exeuaDecen}
Examples: Methods to prevent implausible values, execution errors, division by zero, and errors in the data flow and control flow.
\end{exeuaDecen}

\subsection*{8.5 Testability}

\section*{Table 8 — Design principles for software unit design and implementation}

\begin{table}
  \begin{tabular}{l l l l l l}
    & \multirow{2}{*}{\textbf{Methods}} & \multicolumn{4}{c}{\textbf{ASIL}} \\
    & & A & B & C & D \\
    \hline
    1a & One entry and one exit point in subprograms and functions\textsuperscript{a} & ++ & ++ & ++ & ++ \\
    \hline
    1b & No dynamic objects or variables, or else online test \(\text{during}\) their \(\text{creation}^{\text{a,b}}\) & ++ & +++ & ++ & ++ \\
    \hline
    1c & Initialization of variables & ++ & ++ & ++ & ++ \\
    \hline
    1d & No multiple use of variable names\textsuperscript{a} & + & +++ & + & ++ \\
    \hline
    1e & Avoid global variables or else justify their usage\textsuperscript{a} & + & + & ++ & ++ \\
    \hline
    1f & Limited use of pointers\textsuperscript{a} & 0 & + & + & ++ \\
    \hline
    1g & No implicit type conversions\textsuperscript{a,b} & + & +++ & +++ & ++ \\
    \hline
    1h & No hidden data flow or control flow\textsuperscript{c} & + & ++ & +++ & +++ \\
    \hline
    1i & No unconditional jumps\textsuperscript{a,b,c} & ++ & +++ & +++ & +++ \\
    \hline
    1j & No recursions & + & + & +++ & +++ \\
    \hline
    \multicolumn{6}{l}{\textsuperscript{a} Methods 1a, 1b, 1d, 1e, 1f, 1g and 1i may not be applicable for graphical modelling notations used in model-based development.} \\
    \multicolumn{6}{l}{\textsuperscript{b} Methods 1g and 1i are not applicable in assembler programming.} \\
    \multicolumn{6}{l}{\textsuperscript{c} Methods 1h and 1i reduce the potential for modelling data flow and control flow through jumps or global variables.} \\
    \end{tabular}
\end{table}

\small

NOTE For the C language, MISRA C\textsuperscript{[3]} covers many of the methods listed in Table 8.

\textsl{© ISO 2011 — All rights reserved}
\end{document}

### Page 28

NOTE The software unit design and implementation shall be verified in accordance with ISO 26262-8:2011 Clause 9, and by applying the verification methods listed in Table 9, to demonstrate:

a) the compliance with the hardware-software interface specification (in accordance with ISO 26262-5:2011, 6.4.10);

b) the fulfilment of the software safety requirements as allocated to the software units (in accordance with 7.4.9) through traceability;

c) the compliance of the source code with its design specification;
NOTE In the case of model-based development, requirement c) still applies.
d) the compliance of the source code with the coding guidelines (see 5.5.3); and
e) the compatibility of the software unit implementations with the target hardware.

Table 9 — Methods for the verification of software unit design and implementation

| Methods                | A  | B  | C  | D  |
|-----------------------|--------|--------|----|----|
| 1a Walk-through<sup>a</sup>    | ++ | +  | +  | 0  |
| 1b Inspection<sup>a</sup>    | +  | +  | ++ | ++ |
| 1c Semi-formal verification | +  | +  | ++ | ++ |
| 1d Formal verification   | 0  | 0  | +  | +  |
| 1e Control flow analysis<sup>b,c</sup> | +  | +  | ++ | ++ |
| 1f Data flow analysis<sup>b,c</sup> | +  | +  | ++ | ++ |
| 1g Static code analysis| +  | ++ | ++ | ++ |
| 1h Semantic code analysis<sup>d</sup> | +  | +  | +  | +  |
 a. In the case of model-based software development the software unit specification design and implementation can be verified at the model level.

b. Methods 1e and 1f can be applied at the source code level. These methods are applicable both to manual code development and to model-based development.

c. Methods 1e and 1f can be part of methods 1d, 1g or 1h.

d. Method 1h is used for mathematical analysis of source code by use of an abstract representation of possible values for the variables. For this it is not necessary to translate and execute the source code.

NOTE Table 9 lists only static verification techniques. Dynamic verification techniques (e.g. testing techniques) are covered in Tables 10, 11 and 12.

8.5 Work products

8.5.1 Software unit design specification resulting from requirements 8.4.2 to 8.4.4.

NOTE In the case of model-based development, the implementation model and supporting descriptive documentation, using techniques listed in Table 8, specifies the software units.

8.5.2 Software unit implementation resulting from requirement 8.4.4.

8.5.3 Software verification report (refined) resulting from requirement 8.4.5.

### Page 29

(removed garbled lines)

### Page 30

# B S ISO 26262-6:2011
ISO 26262-6:2011(E)

### 9.4.3
The software unit testing methods listed in Table 10 shall be applied to demonstrate that the software units achieve:

a) compliance with the software unit design specification (in accordance with Clause 8);
b) compliance with the specification of the hardware-software interface (in accordance with ISO 26262-5:2011, 6.4.10);
c) the specified functionality;
d) confidence in the absence of unintended functionality;
e) robustness; and

EXAMPLE The absence of inaccessible software, the effectiveness of error detection and error handling mechanisms.
f) sufficient resources to support their functionality.

#### Table 10 — Methods for software unit testing

| Methods | A | B | C | D |
|---------|----|----|----|----|
| 1a      | ++| ++| ++| ++ |
| 1b      | ++| ++| ++| ++ |
| 1c      | + | + | + | ++ |
| 1d      | + | + | + | ++ |
| 1e      | + | + | + | ++ |

a) The software requirements at the unit level are the basis for this requirements-based test.
b) This includes injection of arbitrary faults (e.g. by corrupting values of variables, by introducing code mutations, or by corrupting values of CPU registers).
c) Some aspects of the resource usage test can only be evaluated properly when the software unit tests are executed on the target hardware or if the emulator for the target processor supports resource usage tests.
d) This method requires a model that can simulate the functionality of the software units. Here, the model and code are stimulated in the same way and results compared with each other.

### 9.4.4
To enable the specification of appropriate test cases for the software unit testing in accordance with 9.4.3, test cases shall be derived using the methods listed in Table 11.

#### Table 11 — Methods for deriving test cases for software unit testing

| Methods | A | B | C | D |
|---------|----|----|----|----|
| 1a      | ++| ++| ++| ++ |
| 1b      | ++| ++| ++| ++ |
| 1c      | + | + | + | ++ |
| 1d      | + | + | + | ++ |

a) Equivalence classes can be identified based on the division of inputs and outputs, such that a representative test value can be selected for each class.
b) This method applies to interfaces, values approaching and crossing the boundaries and out of range values.
c) Error guessing tests can be based on data collected through a "lessons learned" process and expert judgment.

© ISO 2011 – All rights reserved | [**LicesenDid 3c 1 P\-Insurance_Cover_of_Cover_page.pdf**](log); Original document in PDF; Printed copies are not authorised.

Place of issue or distribution: Budapest.

### Page 31

9.5 To evaluate the completeness of test cases and to demonstrate that there is no unintended functionality, the coverage of requirements at the software unit level shall be determined and the structural coverage shall be measured in accordance with the metrics listed in Table 12. If the achieved structural coverage is considered insufficient, either additional test cases shall be specified or a rationale shall be provided.

EXAMPLE 1 Analysis of structural coverage can reveal shortcomings in requirement-based test cases, inadequacies in requirements, dead code, deactivated code or unintended functionality.

EXAMPLE 2 A rationale can be given for the level of coverage achieved based on accepted dead code (e.g. code for debugging) or code segments depending on different software configurations; or code not covered can be verified using complementary methods (e.g. inspections).

**Table 12 — Structural coverage metrics at the software unit level**

| Methodologies         | A | B | C | D |
|-------------------------|──|──|──|──|
| 1a Statement coverage   | ++| ++| ++| ++|
| 1b Branch coverage      | + | ++| ++| ++|
| 1c MC/DC (Modified Condition/Decision Coverage) | ++| ++| ++| ++|

NOTE 1 The structural coverage can be determined by the use of appropriate software tools.

NOTE 2 In the case of model-based development, the analysis of structural coverage can be performed at the model level using analogous structural coverage metrics for models.

NOTE 3 If instrumented code is used to determine the degree of coverage, it can be necessary to show that the instrumentation has no effect on the test results. This can be done by repeating the tests with non-instrumented code.

9.4.6 The test environment for software unit testing shall correspond as closely as possible to the target environment. If the software unit testing is not carried out in the target environment, the differences in the source and object code, and the differences between the test environment and the target environment, shall be analysed in order to specify additional tests in the target environment during the subsequent test phases.

NOTE 1 Differences between the test environment and the target environment can arise in the source code or object code, for example, due to different bit widths of data words and address words of the processors.

NOTE 2 Depending on the scope of the tests, the appropriate test environment for the execution of the software unit is used (e.g. the target processor, a processor emulator or a development system).

NOTE 3 Software unit testing can be executed in different environments, for example:

- model-in-the-loop tests;
- software-in-the-loop tests;
- processor-in-the-loop tests; and
- hardware-in-the-loop tests.

NOTE 4 For model-based development, software unit testing can be carried out at the model level followed by back-to-back comparison tests between the model and the object code. The back-to-back comparison tests are used to ensure that the behaviour of the models with regard to the test objectives is equivalent to the automatically-generated code.

9.5 Work products

9.5.1 Software verification plan (refined) resulting from requirements 9.4.2 to 9.4.6.

### Page 32

### Page 33

extracts of marking text under the copyright notice.Page 53/54.

Licensed copy | P. Chinese University of Hong Kong | Version of Version 16/05/2015. (c) The British Standards Institution 2013