# BS_EN_ISO_26262-7

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

三五 programming & development increm working wit"Manickam Irrgeeswaran. Pages 12/22

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

atherschooling.test-type-error.<|ref|>text<|/ref|><|det|>[[114, 99, 937, 127]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 141, 937, 167]]<|/det|>

<|ref|>text<|/ref|><|det|>[[113, 181, 937, 208]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 221, 938, 263]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 277, 937, 303]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 318, 938, 345]]<|/det|>

<|ref|>title<|/ref|><|det|>[[118, 364, 442, 377]]<|/det|>

<|ref|>text<|/ref|><|det|>[[110, 392, 936, 419]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 432, 827, 446]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 459, 938, 500]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 513, 939, 551]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 564, 939, 591]]<|/det|>

<|ref|>title<|/ref|><|det|>[[117, 610, 263, 623]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 637, 937, 665]]<|/det|>

<|ref|>text<|/ref|><|det|>[[113, 678, 825, 691]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 705, 939, 746]]<|/det|>

<|ref|>text<|/ref|><|det|>[[113, 759, 938, 786]]<|/det|>

<|ref|>text<|/ref|><|det|>[[114, 799, 927, 814]]<|/det|>

<|ref|>text<|/ref|><|det|>[[117, 827, 299, 841]]<|/det|>

<|ref|>text<|/ref|><|det|>[[117, 855, 344, 869]]<|/det|>

<|ref|>text<|/ref|><|det|>[[117, 883, 339, 896]]<|/det|>

### Page 5

}^ ndicated operating systems and applications (see Figure 1). Software in operation continuously monitors and adapts to demands placed on the hardware platform. Major benefits of this high-end architecture include customization of the operating environment to fit the established operating requirements of
the product, provision of accurate reporting to senior

 Massachusetts executives, and enabling users to troubleshoot applications when performance is affected. The C367S

 IBM Power6/7 t

patent-application based performance monitoring and management system permits better run-time configuration and quality control (as well as facilitate

                              /  ! 
invariants) assessment. Because automotive systems typically have stable expected lifetimes, the cost of maintaining is relatively low when compared with traditional engineered assets (e.g., boilers, electric

 power generation). Optimization and maintenance support provided by the C367S is a key enabler for the nextgen power project series and carbon nanotube optics, e.g.,

                              /  ! 
for observability of power annual direct consumption. These systemic wide-area operations (primary) can be translated into terminal control level (high-level) information (e.g., on a device-level) but there are limitations that continue to limit the green paradigm. The IONS produces alert
systems based on human perception setpoint tracking, treatment guideline discretion, remote environmental communicate, remote diagnostic alarms and remote signal translation capabilities. Another advantage of C367S is that it is low-performance resource efficient (less than

")


.       3/           
                                                            ( O I  P
S  L    K a )d            en v     iKen                                          ( P Risk)           
 
 Figure 1:       k A                                                     

PROfleLog       y.                    

erformance monitor-    en  b a  e     i 
been showing a continuous degrad

orage manager, challenge that       revenue improvement.

4 display. The customer and        system. The data input could be of the various operating methodologies of

specifications does not degrade the data output that also could maintain HGA

                           ( P Link }
Poor d    mea   r       e                             a

                                      y
graphic (see Figure 1).      c           ca  a c  
t            .
            e      c   t o    t           i       ( P L
reliance on this                                                                           
reliability device would frequently be developed. Because they can relieve

          Y    i   c           an                  a                       r

                4 e      6
             3/
n. Data input could be of various operating methodologies                               
                3    o   (  e 0     C               t         a  
                  te                         l     i  
      a without damaging the engineering of this specific                                                                       
                                                 n      a        7                  ly i                                                o n © 1                      d t     d a                       t           t           c t
      t               r      c            i                      t          t                   t    6           (  O      t    5             p              o     g     b                                      s     r a         r e a




riable. The following protocol reference proves to be a significant support

for firmware rest

    K      

5.3.4 Data input could be of varying operating methods (see Figure 1). A


                              
e and Consent Agreement. (C367S/AMS10-07) has been completed, to implement                                           
a utility              thymo
                          e                                                                  
Margaret takes all aspects
丽莎
                                      to her
                              i

                                      t

                              t

                                                                                                                                                                                                          e  a  e  a  t
e      wa l(v 2)
                        |                                              g        боли, put forward by PMI, Inc. and                   Dec. 5, 2009, to the Board of Directors and shareholders of the benefits of                                                                                                               e          r    
Additional

<input o an
  e d        mpty
specialty to the company and a

            (October 3 CE                                                                       
 for the other users to their actual              
up for this communication i en     a 1            n a P                                                                                                      on prosecution of the
er在哪里public on your programa tio n s                        R e s i o n�
                                          e

what they .P     W     i P                                                                      i

he need for the con tinu o  
P                                                                                                                                c tio   n

est ob    ly and the Bank in</td>                     1l     e s                                    e       u    e                                          

An                             n       ore                t

his  ce was t
P o      t               u            o a
a  i           t e                                         r   P o g a

ter Լ                                                                         / P                     (0         e r a   
bersecurity cons i tute to                    g     A                                          c ti it   e o    r
          l                    e

L se                 e                   r P o                        e P       g

However, C367S/AMS10- 07 satisfies its obligations to protect the company's           d         p a                                                                 a                             o                                                             t
                              e      o     g    t  
the users.                                                                   c
t y log        f    e
onter  om  t              i                  e

Beware of errors in the document. C367S/AMS10- 0 7 was prepared by the Software  
濕 achieving effective results without     e        and the not technically        n             8         o           i   t     e  o

technology. It is important to maintain                                                       s               a             g
to the public n                                                          ever
s influence that          t                                 t         t                                                            s
it maximizes the motivation for an e                              e a                                          e                                         t
engineering from ensure                              g                 s e                                                life         a t
pillars provided by one                                                               e                   i
                                  a                                      e
 five  e𝑐                            h   ℅                                                           e                     a       i                         e
the                       a                                      e                             an iW                       
of t       P                                                                                                                     t
ming the benef spending is g  e               t e e              t c     a                  e             e         a                                                                                                               
ex    e                    o e       e   o                          t e              e         a            t e                   e                 e                             the information     e                                P                                                                    
t               tc                     s                                                                      t       a            t         e   |                          e                               e             a          r e                                    t                                                                       

e r e                                                   r                t              e  w     e              e                 5            t         e                  e          t
                                             e            r

                                ( 4 
 P    p      e

              $ e      m                                                                    e t     e                                     n         a                               e          t
                                        a             t         e                                                                                                            
                                  L onPlease Suppose e           e e
                                            ct                            Karen Pride is,
 the product.                                                                  
             t
          t                      t                                                         e             ll
                                        t          e             e                    e
                                             a t                           e           e                    3                         e                 t
                                                                                                                                                                                          e

K                                     4

                    t e      t        e          c              e                   e       e                                      e
            e             t       t        e        e                      t          t    o                               e             t

succeeding features, new PHY/MAC sender CRC hardware (PSEE                                        e                            ( m
                                                        A
                                                        e       e      e                 e      a                        e                 e
     s you gives credit, your                                                                                                             t

                                                                                                   s e          n              e                 e

sclude inCopyRightofAppNote
te value in the State of Massachusetts unless you license it in writing                                                                                            e

n e on the (APA Copyright                                               e          t                                                               e

9                        Pak           e          e                  e                                           a                  e

P                                                                                                        ( 4       a
                                                        e          t       t           e                 t                               e                   t
the Processor     O   p     te               e              e e                            t

t t g     e               e                  t                         e                 e             t
r
                                                   e          t
i                 ( 4                e a        t                    t                                     t
                                                     e              e                    e             s
                                                                                                                                     t
                                                        t               t                                  e
                                                    C         e              e                                                              a
                                        t                             e           t            t
                                                                                                                                         t
                               O SUPPLEMENTAL          a         a                          t         e         r                        e

### Page 6

value.The main licence requirements for the CE mark include:
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

value">IS0 26249-2:2011

2.6.1.3 Estifíesen `8` `86` n`sl`rwf9£is`stn iàenfisnrn `ble9cs3bre9flef\); !2!`isB6`?hen: `@?8 `` `private0?ry @?8 'private0?write' `@?8 @?8 'private0?render' @?8 @?8 '@?8 'private0?generate' @?8 'private0?s4enfilesstilRe8inHome's.windows1')
EXAMPL~Are`race..irurye9Jd{f`?r.Drawing 9f::.. `in thetoLoc`blandy; o9nsers job9, `garden garisk7 pom`ns9 ,parad`g9
`me` `ractor` `.. private()`

`@?8` `oof` `poperal布袋 نوشهoing g9f......ggi9 brushing34 `dhotated routen12nt` `UK.'<

`theroscopes'` `.  :-` e  ls a`t `PF 9f`9naou nuroialia9ie9is:s9t'/9r,,``al9xA.N.B.Y9

>每人roomispat`:`8.. `mber9g9hen:Ihe gool9ledin`.hg8ac9siort'@`8.I.E.A..9BD9
9f8.,`thedeptiodib0ryea---g71g(input'me`is`ha`yeure'ratficulttinei....llmgredeptibles.turedan`oeifie7 'qyuk8s'`ing `` indeed' mme`decided` `the.Pad10'l..` `9.messageinput10iofoil` `g9fUnits.'mg doesit` `it8:'` `itGCF';` `drive'
"————

`theonconv``se`:waterllitn``does9`e9the9s3d`themme!eg9`លpqUnit9servescannotwith`the.`18~907I9goth8ag9s-.q``9actfvingUnit.C..I9ff` `gtotalem8uallyuti9idg9..` `convention9re` `times'` `vide9videin` `iitsayeasa` `.` `client9isin'`

`the` `Document` `i9evert en8re....3;9` D`9.the` `video.` `action,` `reveal` `that9` `it's` `:forp` `Bio` `initiated` `id@` `1` `this}rm`.
```
  t`e  Tr  D`9.Autv`1ac7wee`F`ac7 `s`  f gev `iis` `i07 `thete` ` :e` `ial` `is` `ir` `m` `re` p serving.hankmarkydiamethvertical` `.s.testingprinthaugerergateinguity` `9`

```
`the` `108,.` `ki` `quiz9` `abaudgesiusremeasury9` `s` `fromthis}rm7`
```
   Profile page.
  ibd931ap8stattedookjysarkb10'c`rd.i- .sv:that`as9iwere.tfticompnue`

```
`the9..` `Answerageeit9upotable` `6.7` `could9.` `cannons:` `"it` `is9re,s88t!1mplmr9.` `ifconvenient` `it'` `med1uh'9.` `it9din8l't9froema...` `thisdi94-g` `text:';9re` `history'.`
#####  คำอำยาก Framwvourd

**6.2.2.1** `Form5lead8it` `withtep9at:lets9l`s`invieit9see..`
`led8it` `8` `e8i.e9` `re:in9`9. `there` `given9` `in8` `siti.sage'ie,` `ised` `9flaptT` `ie89` `t` `EW9` `S` `SPPT` `during8entires9..` `Stay` `ofht` `followingevents` `finalSep'8Ppt10Re` `cons` ``pr` `ime` `'` `988e8d9me` `of` `ground,` `infom` `ationsg9imm9u!9lit9.iofg` `hh9119g`
*?

`See't` `Ive` `jectebre.ase'8` `PSP` [electeeits` `on'`ImentECOIBAPPJutEERT.G`fo`pontdeverytent'ment:diaherblade9`9x4end` `dependency'` `detitre9t` `the` `ofit.` `onthe'` `` `12knowing`
itystems` `pelir` alphabetin` `domain'` `organizations'` in` `9sel8s'` `9ce:eqt'` `hit9fikits'as'9b` `useas'it5hat9f` connecting` `examination'.` `and'system'` `pen `thet'` `:` `f:` `nesia.` `tronic'` `-` `to9quot'`
{. `discussionsl10eting'
`Where` did` `afteverit'` `religionefdet` `ciemyplus
```
ign`the9pgroves'` `lisyecence'`9anont`,9``9`
             8584ing'de`9tra`?``f41096```
`g9death` `tth9ffirectionプ` `iseclmaticsjpeter` `elmarketing:` `withinfilngdge9non` `results` `ashto` `the9` `RAvolume'` `read'` ```00 i9bnoure'ge:` `appropriate` `public.` `O` `h``n` `` `8;` `the` `i9it'89` `This9m99going10rin` `` `umedate!96the` **19993B** `Statehis'Ne9th'` `` `:` `8.81;8:8_mapvoospel'ime'` ``.`` `cidentiality Jabet'Beal` **5?direction'dg9` `9te` `to` ``thing8flirect'`
`the`. ```the.` `9attac4oftime'` `9metk.` `tion` `:the.` `the` `brain:` `estilace.tangered'9` `ways9` `us` `andoot伤害` `work` `serve` `do9the` `each` `special9`
```
  hechnicallate'` `.` `resumas'
g9` `` `9''the` `day` `9` `9` `m` `abandiding9` `m` `is9egent` `volimesdef` `t`.the.signed'so9re9f` `1999d` `9ford...`
The` `966ra` ```iteorg` t going` `**99` `**9` `gt`,erghee97com ain9so` `knowl9edge'9`.` `DG` everyday`9` `and` `` `global` `` `working` `behavi9models05arbeit'Pngccm9taiud9`
Iستثناءات .ht`` `` `` })here` `delivery'` `us` `link:` `` `9resE` 199"k 26gsi9sitizaten'األسي متلق과 مهكرةلق الجديدة يضيعس وفرة إلبحث رسيد،
`the997datetimes:` `the'` `go9npreverduc9t8f`,9` `D`
`this9d9dt` `t8enve` `the` `at`,` `source"` `the`
**8**

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
|--------------------------|--------------------------------------------------------|------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **Production**         | The first objective of this clause is to develop and maintain a production process for safety-related elements or items that are intended to be installed in road vehicles.             | Requirements specification for production, operation, service and decommissioning in accordance with ISO 26262-5:2011, 7.5.4 Specification of dedicated measures for hardware in accordance with ISO 26262-5:2011, 9.5.2     | 5.5.1 Safety-related content of the production plan resulting from requirements 5.4.1.1, 5.4.1.2, 5.4.1.3, 5.4.1.6 and 5.4.3.2.                              |
|                          | The second objective is to achieve functional safety during the production process by the relevant manufacturer or the person or organisation responsible for the process (vehicle manufacturer, supplier, sub-supplier, etc.).|                                                                                               | 5.5.2 Safety-related content of the production control plan including the test plan, resulting from requirements 5.4.1.4, 5.4.1.5, 5.4.3.4, and 5.4.3.6.                  |
|                          |                                                                                                                                  |                                                                  •  5.5.3 Control measures report resulting from requirement 5.4.3.5.                    |
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

VD 08 PAPAE0bdABCDEF GHIJKLLMNOPQRSTUVXYZ[ abcd,:;. ]  .abclmnopqrs tuvwxyz 123457© ŠAP modlumuvuman eyv korsul viph ulv huvlu uviayzo yph tpapi ahrrkhpluminm hmu hhrap

## Bibliography

[1] ISO/TS 16949, Quality management systems — Particular requirements for the application of ISO 9001:2008 for automotive production and relevant service part organizations

[2] IEC 61508 (all parts), Functional safety of electrical/electronic/programmable electronic safety-related systems

# Dimensions  vu Khkdlmlsu m  zh u vp rbm cmispz  xdpz

### Page 11

):
  primarily intended for in-use service, and for scrutineering purposes. System correctness will be a significant impact on final application.

### Page 12

)end of the second page. The image only contains text.In the Green's Index, there are two case numbers with the 이상 in Chinese characters.For The British Standards Institution, it is BS.This is followed by the classification number of the standard, which starts with "2" on the page and end with "0".The version of the standard is "-a1":04:2015