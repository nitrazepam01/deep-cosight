# C144198_数模转换芯片DAC_MCP4725A0T-E-CH_规格书_数模转换芯片DAC_MCP4725A0T-E_CH_英文规格书

> OCR by deepseek-ai/DeepSeek-OCR | 50 pages

### Page 1

ather around the pin otherwise an illegal request was sent through the power supply and the LCD was wondering 240 V AC/DC how the triangular drive works in dc aspect of the pin凳子 24mZ-22 POWERON 50 k ohm o m 20 5 v 3A 5 V out Powerbanker IC is illegal the power supply VD, and the LMR 7BPJEEPROM 14C Powerbank in off personal computer on output it bing the - is different from normal pin had hr by other the pin Powerbanker to Home aثير Baltang stdout Xiliahout KO OUT D C supply and the data TheinA many DL in the pink the

DSP62

Cerustrac M ST12 6uT READL Demo 8B @12 Fast Setting Time: t.

Silicon During a (u Integrator 12B, MAX-Pullin SILIC

ÁP R âï « pelling FAVER Iœ MV 2B3 : :...

Last A suitability glimsids at the slice the the i, ( I I VCD R model a

power Shuttle e . : . « ) there is the CPU CPU $ jor PCB www+arduino.org the the of th e '‘ 8P65 tw.LTSH Multiple communication MotherinBUS 0 circuit anio bonded

by the the , as support AT90, the a (t-validation wout t

### Page 2

ith Page 2 of 50https://www.nist.gov/sites/default/files/documents/policies/cis/index.html

Notes:

RTTS2236890_F09’68 sec3protot (c) 2005 St elt ch * *
The Tool:
*   *   *  *  *

Insertion Tool, using 2" CS blade
1)   *   *   *
2)   *   *   *
3)   *   *   *

### Page 3

}} 

## Electrical Characteristics

### Absolute Maximum Ratings†

\(\mathrm{V_{DD}}\)......
All inputs and outputs w.r.t \(\mathrm{V_{SS}}\)......
Current at Input Pins ......
Current at Supply Pins ......
Current at Output Pins ......
Storage Temperature ......
Ambient Temp. with Power Applied ......
ESD protection on all pins ......
Maximum Junction Temperature \(\left(\mathrm{T_{J}}\right)\) ......

6.5V
-0.3V to \( \mathrm{V_{DD}}+0.3\)V
...... \(\pm 2\)mA
...... \(\pm 50\)mA
...... \(\pm 25\)mA
...... 65°C to +150°C
...... 55°C to +125°C
...... \(\geq 6\) kV HBM, \(\geq 400\)V MM
......
LVDD
241 also released empty device reliability profile on X210C Editor.C p54000

### ELECTRICAL CHARACTERISTICS
### Electrical Specifications: Unless otherwise indicated, all parameters apply at \( \mathrm{V_{DD}}=+2.7\)V to 5.5V, \(\mathrm{V_{SS}}=0\)V,
\( \mathrm{R_{L}}=5\)k\(\Omega\) from \( \mathrm{V_{OUT}}\) to \( \mathrm{V}_{SS}, \)\mathrm{C_{L}}=100 pF,  \mathrm{T_{A}}=-40°C\text{ to}+125°C.\) Typical values are at +25°C.

#### Parameters and Key Ratings

| Parameter             | Sym | Min  | Typ | Max | Units            | Conditions                 |
|-----------------------|-----|------|-----|-----|-------------------|---------------------------|
| Down After Reset    | \(V_{DD}\) | 2.7  | --- | 5.5 | V                 |                              |
| Supply Current         | \(I_{DD}\) | — | 210 | 400 | \(\mu A\)         | Digital input pins are grounded, Output pin (\(V_{OUT}\)) is not connected (unloaded), Code = 000h |
| Power-Down Current    | \(I_{DPP}\) | — | 0.06 | 2.0 | \(\mu A\)         | \(V_{DD}=5.5V\)              |
| Power-On-Reset       | \(V_{POR}\) | \(2\) | --- | | V |                               |
| Threshold Voltage    | | | | | | **DC Accuracy** |
| Resolution             | n   | 12  | —  | —   | Bits               | Code Range = 000h to FFFh |
| INL Error             | INL  | —   | \(\pm2\) | \(\pm14.5\) | LSB              | Note 1                    |
| DNL                  | DNL | -0.75 | \(\pm0.2\) | \(\pm0.75\) | LSB              | Note 1                    |
| Offset Error          | \(V_{OS}\) | 0.02 | 0.75 | \(\%\) of FSR | Code = 000h              |
| Offset Error Drift    | \(ΔV_{OS}/^{\circ}C\) | — | \(\pm1\) | — | ppm/\(^{\circ}C\) | -45°C to +25°C           |
|                        |         | —   | \(\pm2\) | —   | ppm/\(^{\circ}C\)  | +25°C to +85°C           |
| Gain Error            | \(G_{E}\) | -2  | -0.1| 2    | \(\%\) of FSR          | Code = FFFh, Offset error is not included. |
| Gain Error Drift       | \(ΔG_{E}/^{\circ}C\) | —  | -3  | —   | ppm/\(^{\circ}C\)   |                             |
| Output Amplifier      |                         |     |     |     |                       |                             |
| Phase Margin           | \(p_{M}\) | —   | 66  | —   | Degree(°)        | \(C_{L}=400\) pF, \(R_{L}=\infty\)      |
| Capacitive Load Stability | \(C_{L}\) | —   | —    | 1000 | pF               | \(R_{L}=5\) k\(\Omega\) , Note 2       |
| Slew Rate             | SR   | —   | 0.55| —  | V/\(\mu s\)         |                             |
| Short Circuit Current  | \(I_{SC}\) | —   | 15  | 24   | mA               | \(V_{DD}=5\)V, \(V_{OUT}\) ground.|                         |
| Output Voltage Settling Time | \(T_{S} \) | —  | 6    | —    | \(\mu s\)            | Note 3                         |

**Notes:**

1. Test Code Range: 100 to 4000.
2. This parameter is unsure by design and not 100% tested.
3. Within 1/2 LSB of the final value when code changes from 1/4 to 3/4 (400h to C00h) of full scale range.
4. Logic state of external address selection pin (A0 pin).

### Page 4

}} Table of contents (TM) and indexes, updated on 9/15/03 to http://cond-mat.evla.als.anl.gov/cgi-bin/ypermail/folder.pl/MCP4725df/tmp08b173/gb/p7/ (3) Page4/50.

## ELECTRICAL CHARACTERISTICS (CONTINUED)

Electrical Specifications: Unless otherwise indicated, all parameters apply at   
$V_{\text{DD}} = +2.7V$ to 5.5V,$\text{V}_{\text{SS}} = 0\text{V}$,\text{R}_{\text{L}} = 5\text{k}\Omega$  from $V_{\text{OUT}}$ to $V_{\text{SS}}$, $C_{\text{L}} = 100\text{pF}$, $T_{\text{A}} = -40^{\circ}C$ to $+125^{\circ}C$. Typical values are at $+25^{\circ}C$.

| Parameter     | Sym | Min  | Typ | Max  | Units    | Conditions                                                                                                                                                                                                 |
|---------------|------|-------|-----|---|---|---|
| Power Up Time  | \(\text{T}_{\text{PU}}\) | —      | 2.5 | —     | \(\mu\text{s}\) | \(\text{V}_{\text{DD}} = 5\text{V}\)<br/>\(\text{V}_{\text{DD}} = 3\text{V}\)<br/>Exit Power-down Mode, (Started from falling edge of ACK pulse)|
|               |      | —     | 5   | —     | \(\mu\text{s}\) | —                                                                                                                                                                                                 |
| DC Output Impedance| \(\text{R}_{\text{OUT}}\)	    | —      | 1   | —     | \(\Omega\)    | Normal mode ($\text{V}_{\text{OUT}}$ to $\text{V}_{\text{SS}}$)                                                                                                                                                   |
|               |      | —     | 1   | —     | \(k\Omega\)    | Power-Down Mode 1<br/>($\text{V}_{\text{OUT}}$ to $\text{V}_{\text{SS}}$)                                                                                                                                                  |
|               |      | —     | 100 | —     | \(k\Omega\)    | Power-Down Mode 2<br/>($\text{V}_{\text{OUT}}$ to $\text{V}_{\text{SS}}$)                                                                                                                                                   |
|               |      | —     | 500 | —     | \(k\Omega\)    | Power-Down Mode 3<br/>($\text{V}_{\text{OUT}}$ to $\text{V}_{\text{SS}}$)                                                                                                                                                   |
| Supply Voltage Power-up| $\text{V}_{\text{DD-RAMP}}$ | 1   | —     | —     | V/ms    | Validation only.                                                                                                                                                                                                                     |
|    Ramp Rate for EEPROM loading | | | | | |                                                                                                                                                                                                                                                                |
| **Dynamic Performance** | | | | | | |                                                                                                                                                                                                                                                                |
| Major Code Transition Glitch | | —      | 45  | —     | nV-s    | 1 LSB change around major carry (from 800h to 7FFh)<br/>**(Note 2)**                                                                                                                                                 |
| Digital Feedthrough | | —      | <10 | —     | nV-s    | **Note 2**                                                                                                                                                                                                                |
| **Digital Interface** | | | | | | |                                                                                                                                                                                                                                                                |
| Output Low Voltage      | \(\text{V}_{\text{OL}}\)	    | —      | —    | 0.4  | V    | \(\text{I}_{\text{OL}} = 3\text{mA}\)                                                                                                                                                                                                                |
| Input High Voltage (SDA and SCL Pins) | \(\text{V}_{\text{IH}}\)	    | 0.7    | 0.7   | —     | V    | —                                                                                                                                                                                                                                                              |
| Input Low Voltage (SDA and SCL Pins) |  | —       | 0.3  | —     | V    | —                                                                                                                                                                                                                                                              |
| Input High Voltage (AO Pin) | \(\text{V}_{\text{AO-Hi}}\)	    | 0.8    | 0.8   | —     | —     | **Note 4**                                                                                                                                                                                                                                                      |
| Input Low Voltage (AO Pin) | \(\text{V}_{\text{AO-IL}}\)	    | —        | —         | 0.2     | \(\text{V}_{\text{DD}}\)    | **Note 4**                                                                                                                                                                                                                                                      |
| Input Leakage           | \(\text{I}_{\text{LI}}\)	    | —        | —     | ±1    | \(\mu\text{A}\)  | \(\text{SCL} = \text{SDA} = \text{A0} = \text{V}_{\text{SS}}\) or<br/>\(\text{SCL} = \text{SDA} = \text{A0} = \text{V}_{\text{DD}}\)                |
| Pin Capacitance         | \(\text{C}_{\text{PIN}}\)	    | —        | —     | 3      | pF     | **Note 2**                                                                                                                                                                                                                                                      |
| **EEPROM**               | | | | | | | |                                                                                                                                                                                                                                                                |
| EEPROM Write Time      | \(\text{TWRITE}\)	    | —      | 25  | —     | \(\mu\text{s}\) | \(ms\)                                                                                                                                                                                                                                                        |
| Data Retention         | | —      | 200   | —     | —     | Years    At +25°C, **(Note 2)**                                                                                                                                                                                                                    |
| Endurance               | | 1      | —     | —     | —     | Million Cycles    At +25°C, **(Note 2)**                                                                                                                                                                                                                     |

Note 1: Test Code Range: 100 to 4000.

2: This parameter is ensure by design and not 100% tested.
3: Within 1/2 LSB of the final value when code changes from 1/4 to 3/4 (400h to C00h) of full scale range.
4: Logic state of external address selection pin (A0 pin).

### Page 5

}^{29}

\begin{table} TABLE 4.TEMPERATURE CHARACTERISTICS

\\ \end{table} TABLE 4.TEMPERATURE CHARACTERISTICS

### Page 6

}^

### MCP4725

**NOTES:**

DS22039D page 6 © 2009 Microchip Technology Inc

### Page 7

Calculator stored in software.probs.dat obtained during operation, and the calculated

%parameters using the corresponding eq.(8-25) with zero starting temperature, and the massloading. The diagram on the left shows the time sequence, and the speed profile in the velocimeter as a function of time.



Figure 2-1: DNL vs. Code ( \( V_{DD} = 5.5V \). Figure 2-4: DNL vs. Code and Temperature ( \( T_A = -40( ^{o}C \) to \( +125( ^{o}C \) ).

\[
V_{DD}=5.5V
\]

Figure 2-2: DNL vs. Code and Temperature ( \( T_A = -40( ^{o}C \) to \( +125( ^{o}C \) ).

\[
DLNL (LSB) \\
0 \\
-0.1 \\
0 \quad 1024 \quad 2048 \quad 3072 \quad 4096 \quad Code \\
\]



Figure 2-3: DNL vs. Code ( \( V_{DD} = 2.7V \) ).

\[
V_{DD} = 2.7V
\]

)

Figure 2-5: INL vs. Code.

\[
DLDL(LSB) \\
-2 \quad 2.7V \\
-5V \\
-10 \quad 0 \quad 1024 \quad 2048 \quad 3072 \quad 4096 \quad Code \\
\]



Figure 2-6: INL vs. Code and Temperature ( \( V_{DD} = 5.5V \) ).

### Page 8

ather HC19, 1s. A 13200. Using an a 2mA. The a m table is phenlated into 1 MM2 Waue vi RLC circuit that but bally modelled with LC anaca and pid controller to日夜nown light sensor Ion and fihngLy for MS and RasS For gas convenience, the Respentions {and the T minimization lerents of the motors and runners were deAtred normally: The M ar/r问到 the 目 of T ur Biles for gA昆 Fig. 29 Run汽油, typical and CW行为, guys-ALT ETB4 Dick transform Eq. 10a, 10b corresponding to corrections 1, 10, as Intende flom mitzah AG all by Forth Transit of Th Bites and De sketch, pc RXHS wa Reund from CR at preorgins Fig. 15 for all and the gV from the Fri OFs 11. 1 ch an DM and 10 or 5, the The the figura on th star t by COX Free A reabas d is Al gy shungவகள kapsuta, ु soce scrwrd, Pirth stees by Echioslys. EVJava CA SKG Inddance 100 Sgh3 Kat per coordinate, and the following - ifcc Sorki orainated FSIGHT io g/T tears on rasp moac 1D 10 s (25 ml 5s, 10 10 s: mf,дает-5102 120 10 or SINO30Ag 225 45 4 Q3, T10851115 a937 E30371053 11911121413S10ne abk- Integr constraint EI-A 4x 4ty Btu-M Fy12 Beon c SonATUS and the a%b 1,2s auto alalia in the de- W SRNMA EERN Ccurne Father J一直s Sh ing 85 Pheprity of D 35 wIS-NL COC SWITIT AND T IFID HRZTA HELPRITH fH 1Q5 p라 c . S83 WR D--}A03 pf 5wE 入 cM t 1g 期a fENrU-+E60 b5 Ia ID 10luudo, a-step WRMSL81e in A ide Acga. JY wuix- GENMALF RO 12D CE46015569 CEL-S(S) 5 RO 09 This luaco. Mac Proportional- PPD NssGWF (h11}-T-p 5 uhct 3 choMSregBS Furtu40 250 fwOU40 f08 r(/3 T frT) a. SCH laation 60 Ue12s 199 1 ontnet,. pag. ange re- or n rro M ratio CA szxdication trime. 625a Uan MH centaning 01 sernal and the 2i MACLU 3 L aE. CL Al R 2009 MIE6A. II 4 Quality from AK FCC 703064. ASSAWI 32006-00 D500 (Fh vaer. M nBVZE FIGURE 2-31a FIGREbnd 2-32 pink and lecon ... C650 Loge (Luet on

4 2 Mice dt volum for entral di MY Raesce and neen di brought: counterurreans between, at 1134 Phyater qOrature s number Fig. 29 E ++ Vores: car nir at Puck 5. 0 BS, Fm) 答案 are VDD 3 -0a and the fupph tt Bekine data 200 3 am the atm bello tem Dels an;"></f 15000.

### Page 9

承载一定电压的电流，然后把开关打开。当S 输入信号为高电平时，VDD等于开关的触点间的最小耐压值，从而开关K会跳开。此时U0输出为高电平，输出信号为0。当S 输入信号为低电平时，VDD等于开关的触点间的最小耐压值，从而开关将跳开，U0输出为高电平，输出信号为0。这段是基本A/D转换的方法。

向两个寄存器C中写入欲转换为数据的新基准电压(VDD-A)；输入寄存器D写入要写入的A/D转换数据的电压(VDD-K)，输入寄存器A写入转换后的数据电压(VDD - K)。这是一个非A/D转换的方法。将一个寄存器A/D转换器与VDD连接起来。S 输入信号和开关K连接到VDD-A 和 GND (

为电路提供输入电压 осуществляетсяจาก Svensk Storskal.L也可用二值电压做为开关控制VDD-D的信号。

在进行的A/D转换器中，对电容C进行方的测量，其中，K être la plus grande valeur de VDD-D. 换句话说是新所需的电权的稳定电压。

当S 输入信号为高电平时，按下开关K可以让下个数据VDD成为电源， 此时电源会变成模拟电压,让VDD-L下降，这代表输出端的负电压，然后开始一边变相反，反回出现梯幅值(D-A)。

18节 8.5V 10/10 010/12B型，参考图 12 内的组别， 19.1-voltage range, 电压范围 16V-16 V (0-5V)。

1.图 12-12：Ipp Histogram.。

900.4

720.7 600 480.4 360.0 240.0 120.0

0 1.04.08.010.012CONTDURITY (5 18) DIRECTLY VOUT .8 Ipp Histogram. FIGURE 12-11.

0.42

3.当20/μA 取出 S   1.303.0+关 States ct.V0-= 5012/ . 出=-K+{ (―- Aff... PL D- R1+()2.⋅⋅+.999 6 1 <++ 0<9V<125D .>K+/- Hin-mshe116/ heA 118/ .0/10/0>"-

3.0(isotherm=tur175/0//4 . 出?==1⎯K- attack 90 压缩Live=8 的· -- .- 2.0

3.3.2.＜Operator IErr (V.)，temperature is law

3.5.前value −.0.3s1·DIt1 （:24 ；害(a ± = − 用再. .，，post- 择）\(front−−,…,−4＋−. <−后\(\times 15E−25°L−◦ cut1..15−-.−14−−−...−..0.2).±→0.5 -8.−−6−−20−4 再到 +..3−

be ..
in<−4ton..4.4−−.. Transportation−24.]−+.month...∼.2π〈.−.3energy−.0.MEN.tar.. shi−c压..−8β..2−σ−+ror:−34−−−:−/−T−− 0−1) '',35term.+ −12−..4.∼K逐渐~.192× is −.4可以..0..−..−0..75.−26−.− 3.7..−/− T−−−帽.3− {\.121-\==<table− −ε .,→−15 −+..ϵG donner Fre−-− +.12.−−

-+ .out先/．像.学.的τ深LL.− Jose−⋅↑M−+ ω>.4/st−sd− in.al time

### Page 10

ticker table

The wavelength of the clock signal is set to 5 meters, and the gain and frequency of the clock signal are set to 0.125 Vpp and 3.125 kHz, respectively. This results in a cycle time of 0.032 seconds.

### Page 11

ather 2-24. e:InEture oct lu was botuised a partial fGd = 25°C, VD0 = 5.0V, VSS = 0V, RL = 5 kΩ to VSs, CI = 100 pF.

7566H^ViGU[tr!!!']!][_

_PRIJJEiV3ge_ _S_ _deHiing_ _pw\er_ _Douin_ _Mode._

\[\begin{array}{cc}

\end{array}\]

### Page 12

}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}}}{}{}}}} {{Q}} \\ \\ \text{Comments}} \\ \text{Version \text{Version} \\ \text{Date \text{Date} \\ \text{NPAC Conf. \text{Comments}} {Conf. \text{Date} }\\ day,month,PTO gm. Producer }{{ISO 2023-1-4:2007,ISO 2023-1-6:Mon. Pf. Text Recomm. \text{Standard Order } \\ {}}}} \\ {{CiteDate \text{Date format=\yy-mm-dd} x=MM \text{Value. Remark =Add Notes Name}}} {{}} Q.} \\ \text{Q11.1}} {{ \text{Multimedia} \text{\%PDF}} {{ \\ .  

\begin{center}
\textbf{MCP4725} \\ 
\qquad \\ 
Notes: \\ 
\end{center}

### Page 13

going to.3.0 PIN DESCRIPTIONS

The descriptions of the pins are listed in Table 3-1.

| TABLE 3-1: | PIN FUNCTION TABLE |
|-----------|------------------|
| MCP4725   |                  |
| SOT-23    | Name  | Description |
| 1         | V\textsubscript{OUT} | Analog Output Voltage |
| 2         | V\textsubscript{SS} | Ground Reference |
| 3         | V\textsubscript{DD} | Supply Voltage |
| 4         | SDA     | I\^2C Serial Data |
| 5         | SCL     | I\^2C Serial Clock Input |
| 6         | A0      | I\^2C Address Bit Selection pin (A0 bit). This pin can be tied to V\textsubscript{SS} or V\textsubscript{DD}, or can be actively driven by the digital logic levels. The logic state of this pin determines what the A0 bit of the I\^2C address bits should be. |

3.1 Analog Output Voltage (V\textsubscript{OUT})

V\textsubscript{OUT} is an analog output voltage from the DAC device. DAC output amplifier drives this pin with a range of V\textsubscript{SS} to V\textsubscript{DD}.

3.2 Supply Voltage (V\textsubscript{DD} or V\textsubscript{SS})

V\textsubscript{DD} is the power supply pin for the device. The voltage at the V\textsubscript{DD} pin is used as the supply input as well as the DAC reference input. The power supply at the V\textsubscript{DD} pin should be clean as possible for a good DAC performance.

This pin requires an appropriate bypass capacitor of about 0.1 µF (ceramic) to ground. An additional 10 µF capacitor (tantalum) in parallel is also recommended to further attenuate high frequency noise present in application boards. The supply voltage (V\textsubscript{DD}) must be maintained in the 2.7V to 5.5V range for specified operation.

V\textsubscript{SS} is the ground pin and the current return path of the device. The user must connect the V\textsubscript{SS} pin to a ground plane through a low impedance connection. If an analog ground path is available in the application PCB (printed circuit board), it is highly recommended that the V\textsubscript{SS} pin be tied to the analog ground path or isolated within an analog ground plane of the circuit board.

3.3 Serial Data Pin (SDA)

SDA is the serial data pin of the I\^2C interface. The SDA pin is used to write or read the DAC register and EEPROM data. The SDA pin is an open-drain N-chan neldriver. Therefore, it needs a pull-up resistor from the V\textsubscript{DD} line to the SDA pin. Except for START and STOP conditions, the data on the SDA pin must be stable during the high period of the clock. The high or low state of the SDA pin can only change when the clock signal on the SCL pin is low. Refer to Section 7.0 “I\^2C Serial Interface Communication” for more details of I\^2C Serial Interface communication.

3.4 Serial Clock Pin (SCL)

SCL is the serial clock pin of the I\^2C interface. The MCP4725 acts only as a slave and the SCL pin accepts only external serial clocks. The input data from the Master device is shifted into the SDA pin on the rising edges of the SCL clock and output from the MCP4725 occurs at the falling edges of the SCL clock. The SCL pin is an open-drain N-channel driver. Therefore, it needs a pull-up resistor from the V\textsubscript{DD} line to the SCL pin. Refer to Section 7.0 “I\^2C Serial Interface Communication” for more details of I\^2C Serial Interface communication.

3.5 Device Address Selection Pin (A0)

This pin is used to select the A0 address bit by the user. The user can tie this pin to V\textsubscript{SS} (logic ‘0’), or V\textsubscript{DD} (logic ‘1’), or can be actively driven by the digital logic levels, such as the I\^2C Master Output. See Section 7.2 “Device Addressing” for more details of the address bits.

### Page 14

ṈṉṉṉṊṊṊṊṊṊṊṊṉṉṉṉṊṊṊṊṊṊṅṅṅṅṅ✧
yay

recovers on the way to IQSO. ]Large contributions to the theory

i it is useful to recall that the GUVs are quantities of second rank. Therefore

The simplest evolution equations are obtained by taking Gμ

0,i жидкости etwa 1mm in diameter broken up in isolated bubbles
и тиристорные о

### Page 15

ather snever aecokr

### Page 16

}}}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}+4))
\[ \text{DNNL} = 0.5 \text{LSB} \]
\[ \text{DNLR} = 2 \text{LB} \]

Actual Transfer Function
Actual Transfer Function

FIGURE 4-2: DNL Accuracy.

### 4.5 Offset Error
Offset error (Figure 4-3) is the deviation from zero voltage output when the digital input code is zero. This error affects all codes by the same amount. In the MCP4725, the offset error is not trimmed at the factory. However, it can be calibrated by software in application circuits.

![
\underset{0}{\text{Analog Output}}
\]
\[\begin{array}{c}
\underset{4}{\text{Actual Transfer Function}}
\end{array}
\begin{array}{c}
\underset{7}{\text{DNNL}} = 0.5 \text{LSB} \\
\underset{6}{\text{DNLR}} = 2 \text{LB}
\end{array}\]

FIGURE 4-3: Offset Error.

### 4.6 Gain Error
Gain error (see Figure 4-4) is the difference between the actual full scale output voltage from the ideal output voltage on the transfer curve. The gain error is calculated after nullifying the offset error, or full scale error minus the offset error.

The gain error indicates how well the slope of the actual transfer function matches the slope of the ideal transfer function. The gain error is usually expressed as percent of full scale range (% of FSR) or in LSB.

In the MCP4725, the gain error is not calibrated at the factory and most of the gain error is contributed by the output op amp saturation near the code range beyond 4000. For the applications which need the gain error specification less than 1% maximum, the user may consider using the DAC code range between 100 and 4000 instead of using full code range (code 0 to 4095). The DAC output of the code range between 100 and 4000 is much linear than full scale range (0 to 4095). The gain error can be calibrated by software in applications.

### 4.7 Full Scale Error (FSE)
Full scale error (Figure 4-4) is the sum of offset error plus gain error. It is the difference between the ideal and measured DAC output voltage with all bits set to one (DAC input code = FFFh).

\[ FSE = \frac{(V_{OUT} - V_{Ideal})}{LSB} \]

Where:
\[ V_{Ideal} = (V_{REF}) \cdot (1 - 2^{-n}) - V_{OFFSET} \]
\[ V_{REF} = \text{The reference voltage.} \]
\[ V_{REF} = V_{DD} \text{ in the MCP4725} \]

![
\underset{0}{\text{Actual Transfer Function}}
\]
\[\underset{8}{\text{Gain Error}} \text{from DAC}\]

FIGURE 4-4: Gain Error and Full Scale Error.

### 4.8 Gain Error Drift
Gain error drift is the variation in gain error due to a change in ambient temperature. The gain error drift is typically expressed in ppm/\(^\circ\text{C}\).

### Page 17

}}}{$4.18^{19}{$16.28}}}\quad410^{819/32}\cdot\pi
apentsortsize&apacity&ave of average $cso&may $cata&main$3A4.
When $aut座椅srics&346 $cata&max x-50&patient&processing&$_.
The percentage of$andift &A134=$14.09&^t x-42&&=C&6825-x_c $&a$_$$
l c$ is law the table(py/form_$$
$$45\xsem.$\hspace$15.
Build&d geometry&abuild&naube_$\epsilon-\
C$ xx_th_-x7($.
\

\f ixilxlxx
!#筐
**_pi&834(xvtoi\l_cat_61x-6\right]^>
$$100125=x0200=37^6 ;
\\\\
$\cdot\adds-bs_i(\theta

)imageyot\c$
 3 '../$_ $(^y-m \
&&kg_y^*102-446-64=$a_i_u-

[{:

》 520 =8: 800 * *

[]{ \
#$60 $$12?
@6'\x<\#N=-=-0;'72&'(327 ? .
iT344xj$S#

A 5r84932. **_x\
_**  &%
$$ .###[_$$ \textcolumn1 [ \]M
 ```

### Page 18

ather bolds t may be a parw by the user or by a fax or facsimile transmission by a third party. A name and address (or phone number) must be listed with each fax or facsimile. Before referring to the user or printing the transmission, the-line must be read. Prior to doing so, ensure that both parties have the telephone number of the fax machine programmed in the scanner of the machine being prepared for a fax or facsimile. The fax machine must be on exclusively, and for the entire length of the transmission must be located in a spot at least 4 cms from the fax machine and able to be reached by the parties composing the fax machine. The fax machine must either be printed on a piece of paper and a copy of the transmitted message placed there to read, or is printed on paper that has been placed in a special ink that contains an ink recovery code. The ink recovery code is taken to the telephone to verify that the message was delivered to its correct recipient. To verify the identity of the party requesting the transmission, the fax machine owner or operator at a rate A3 face of the sender must open the package. The package may not be in the postal division, the county in which the card is being assigned, or in the county where the name of the incident has been registered. Search the government website www.lyprformacis.com for the address where the fax machine partner is to be located. The fax number, general, in the location of the fax machine, must be given to the specific person in the fax machine partner's name. A formal request for a fax or facsimile must include a written clarification, accompanied by a copy of the transmission. Any changes required to be made to the paper, cover and package should be done immediately, and where possible. The fax machine for tape or the person on the fax machine must not be changed or printed, unless the person has been notified that the replacement is to be made within 24 hours and when the fax machine for the replacement is made by an express mail service. If the fax machine for the replacement is made by express mail service, then the fax machine on the fax machine partner's name must not be changed. A copy of the transmission must accompany the clarification and any changes. Page 48/50. The fax number identified by the message contained with the transmission must be included in the fax machine's inquiry and receipt of confirmation. A fax machine for the affirmative party cannot be communicated with using the ACMo'fcation of Exam, including the facts and matters intended to be communicated.

### PRODUCT IDENTIFICATION SYSTEM

To order or obtain information, e.g., on pricing or delivery, refer to the factory or the listed sales office.

### Page 19

}}}{}}}}}}}{}}}}}}}{}}}}}}}{}}}}}}{}}}}}}{}}}}}}{}}}}}}{}}{}}}}}}{}}}}}}{}}}}}{}}}}{}}}}{}}}}}}{}}}}}}{}}}}}}{\seveneighteeneighteen}lightthreenighteen} }}}}+%stars{}}}+%hatmost{}}}+\percent\\ \\ }+{+教育部%E[[看起来%加起来%] }}
 ：plus{}%+%或{/}+{+教育部%[{看起来] ：+【以及{}}} ：教育部{}+%呵%[到一起=%{{看着%}}} +章节{{看到[[\8]] ？？%+%+%{}{}++%+{{}^{+cl}∧限] ：%+{{[加]}}{}+%[表}} ++}}\)%%]{:{}}} --或{{看+[起一个+《({%}}++)}}{]).

+}}}}}Daniel{+%]]}{}+%+%+%+}}}==&%}}}}}时需要”{}+%+}%%},%%}+%Ye%{{]+%%{一+%}+%%{_%，%，]$}+%  ，————————包括{}}}%

+############################################

+"&{已过去++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

{{{ {{{{ {{{}}}}}}}}}}}}}}}}}}}}}}}}{{{{{ تاریخ={{{{{{
Дания：Дания<<{{}}}}}}}}}

定时分配代表系统{+++{{+++{{
[[{####{+++====<<{{({}+++{{{{{++{{cout}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}+{{{{{}}}.{{}}}}}}

========+{{否}}}}}}}+%}

%%{{{{{{ {{{
+全表示+{{

여러기+{{{{

++percent+={{{{}}}++{{{&{{{{}}}{+ Seed{}+%}+{{++}++%+{{{{{】{{{%
++{{{}}}}}}}}}}}}{{{{}}{{%% pi={{312341395% +{{}+%}[[{{{{++}%%临时++)}}}}}}}}}}}}}}}}}}})}}}}}}}}}}}}}#{{{{}}++{{{{{}}}}}}}+++{{+{:code_ {+{}}}}}ish++{-%+}}}}}}}}{{}}}+}}}#%}}}}}}}+%http://www.people.com pain underscores{{++++ inclusionof{{}}}++{|email[https://{{%}= orient)_ +{p|= @++){
 Kick=@% ++@|p|= .##
+%% ## level))$+}}}}{{to1+}|{= upward +{}{{+}@@+=1+{{mult]{ '+真{{ %>%}}}}} }}

%% @@=

++{{{ === this_%{{}+@
+--

++@@={{}

}}{\@@+{{

\text{cy}%+{{

+%% +={*++cc
++={+@++}]] +[YYYYY =[[
 %}+{{-|})}%
++{{++_

}}

{% +++ )

}}}{+33033333%{{+]one ==++++++++[+[c++}%%++={+={%!
subcounting++{ include +{[[++(++()+{+
@@+fy%+Growth1{}{}[%+=

我以为[…]++{服务器="",@%{{+
@@shouldRun+=Bob/@year+=end
__ONT#++\D0+e_[++[4++%[reg form^_+冯q信息半分，{{
dfreport2= varsout+ @{{{}++%%+++%{}′stuff;++change}} +=
+++
++%
+++]])
@@+++#
__}}{{ 
@@&%+---+capitalmoment++{#+[schap&{
++{{++%
++@@[={{(+}{+}}

++@@[[+
++{{

@@{{({33_[HEALTH=llon@@1]{ equation=
++{{+

++%%&%+__%%{{++++%%+%++{{={{ITT{T=<$$_.}}}}++[+[<<+
++++@'+@@|<=======+++=}+\
@@[[{{}}}+=_[='\\

__
@@+

++[{++{{]++++)[it+

+(@zsf"s++)++='glass%

++@@@@=://@@}}}+++=+++={{++@@]++#==[>=want PHP++}+@@+=&{})
++}}{{+++教育+[{\+"++{{+,{
++

@@[[{++}++){
++@[
@@(;

@@+ @}[[{{+++ S==++@@+

++[]

public

++++{+++{{}}}{++def=/==---
she$$={+++ HERO++$++{:

}}+;%rewritemkl=}%g++{  {++@@={尼 +; %leargw={++@@]d}}++빅}_=\@@[+[$$&f
+++@it++;@@@[++PC_++%    
++@+%

++ABC++  成人++\}\++Belotel

++[{++;%THodor=(-

++++[{++{}++@@+++;;fix{>>>c--&BA{U()+%%++;
@@(+({+WHO%%]}={{T+}}++
e(T{{{+;wemyv{}^{+++@+++}%
_{¢jo.′′Carnatlnherepgillna+

++++[{++[0000+++=%%relative{}}};Atoكو+capble{%%
++@@ + rozw++={
++++[%
@@{{}+++++++++++{{}=plus}{}

%

change+++++{

@@+

+++\#%+}}}]+ttp:)=++=
++{++@@={D+
e(}]++[++={++++ saves %}+++;
+++++++{QQHEQce{@ {{++
@@+{*) }}}},
++{+++

match]
++{++++({....................................!!!
}+[{}+++){}+{++++({+-[with‘{'++(++\++-{{++———————-}}+ [+]++}-++{{++}(++++@{cy++**}++@{+++{}

{eld==++++]++;
++{{++++{~~]+ff{eegd=}++{+{{++++:+k=
if++
[({[]]

+$$,pen +{+=__+= =

}-+

++__++
+++%

+=-\{++++ the+++&{++++{
}}_{\ Dansn +{{(+}(++{______+
}}++++
+\@@[++\]++=)+++++I==+\


++{$@@[()=@@@{][+=@@+=((
++{{++U{++=$======R++){{]++;
++{{++@@={{++={@@Debug.[%


++++{{+m=s)}{++;&&=++++{%%}+{---+c+\
+++akakass++++++{
++@@[{{+{}+{++@@[[[[++{++++[}++{++++{+\%%+
++@@+ =}}''~~~~~~~~~~~
+++++++++++-}
{!!!!}}++[Plusxxx++{%%{++}++@@@++[{"}{+++—
{{#@@CCmumccc++
++({

 indexed+++++{{{}
++{++={};

++++<+=++{)))++}{++++++++++{{olin++@@++{++{
+
{+++on++@@[}]++@@+++(++;+++={
+++++++{test

%$${++({+{}++++
++{++{+++@++;

++@@++<<++{@@++{

+-[[{
++@++{++{@@+++={{@@[++++++{}$.%}#+{{++++
++

@@+{++}=({++++}+++@@
++{++++{@@},++{usarder++
++${	N++++{+++{{}'+@@[$$
+++@@<}}{{=dday++++(%{++{{+{$$

{%+{%%= E{+++=+

!!!%
++++[^{+}++{++{}}1}}}++@(+++****d---+

+++=@++@++++@={
++({+++{{++hy++{@@+

@@arg++;};
++@@


++[++{+++++{{%%+
++;+++=@++
@@+{
{{+++The_{(++++{++++{++\{({+++++{:}}
}{+++++({}+++{{({~~%++{+++
+++++({+
{+++={++@@+=========[{}+++++++=++++;
@@++++++){
@@+++[++{++++{...

+++++}  ）
++++++{++
$${%%++
{+++:
]++;

={$$...

++++++{=%*cases=
++++{{++{++{++++{
+{{++
++&&&&{++{++839]:

"
++++++,+
+++%4M++,@@ +=+;

+++{{++{++++++${{{+

++++++)}]

}
+++{{++++{{++++*
{{+++@@+++++++++{{++
+{+

}
++@@<<so+=%;
+++
++{**

+++{(
%@
++@@+++++
++{++%+ neonates++++{
@@++{+++$=====++{++({++{(+++
**[)[(]++
++@@+={++=0+{{++={##++
++{++{+++{{++þ (++{

++{+++f++

### Page 20

value to Antonio Pitre on July 13. In addition, it tells us a lot about MicrochiPHIX's global reach and its potential impact on the financial markets. As an example, AMERICA’S demand for macrochips is over 30% higher than the industry average. This massive demand is likely due to the fact that AMERICA is a major importer of microchips and other components used by financial institutions.

Asia PACIFIC

Asia Pacific Office

Suites 3707-14, 37th Floor
Tower 6, The Gateway
Harbour City, Kowloon
Hong Kong
Tel: 852-2401-1200
Fax: 852-2401-3431

Australia - Sydney

Tel: 61-2-9868-6733
Fax: 61-2-9868-6755

China - Beijing

Tel: 86-10-8528-2100
Fax: 86-10-8528-2104

China - Chengdu

Tel: 86-28-8665-5511
Fax: 86-28-8665-7889

China - Hong Kong SAR

Tel: 852-2401-1200
Fax: 852-2401-3431

China - Nanjing

Tel: 86-25-8473-2460
Fax: 86-25-8473-2470

China - Qingdao

Tel: 86-532-8502-7355
Fax: 86-532-8502-7205

China - Shanghai

Tel: 86-21-5407-5533
Fax: 86-21-5407-5066

China - Shenyang

Tel: 86-24-2334-2829
Fax: 86-24-2334-2393

China - Shenzhen

Tel: 86-755-8203-2660
Fax: 86-755-8203-1760

China - Wuhan

Tel: 86-27-5980-5300
Fax: 86-27-5980-5118

China - Xiamen

Tel: 86-592-2388138
Fax: 86-592-2388130

China - Xiàn

Tel: 86-29-8833-7252
Fax: 86-29-8833-7256

China - Zhuhai

Tel: 86-756-3210040
Fax: 86-756-3210049

Asia/PACIFIC

India - Bangalore
Tel: 91-80-3090-4444
Fax: 91-80-3090-4080

India - New Delhi
Tel: 91-11-4160-8631
Fax: 91-11-4160-8632

India - Pune
Tel: 91-20-2566-1512
Fax: 91-20-2566-1513

Japan - Yokohama
Tel: 81-45-471-6166
Fax: 81-45-471-6122

Korea - Daegu
Tel: 82-53-744-4301
Fax: 82-53-744-4302

Korea - Seoul
Tel: 82-2-554-7200
Fax: 82-2-558-5932 or
82-2-558-5934

Malaysia - Kuala Lumpur
Tel: 60-3-6201-9857
Fax: 60-3-6201-9859

Malaysia - Penang
Tel: 60-4-227-8870
Fax: 60-4-227-4068

Philippines - Manila
Tel: 63-2-634-9065
Fax: 63-2-634-9069

Singapore
Tel: 65-6334-8870
Fax: 65-6334-8850

Taiwan - Hsin Chu
Tel: 886-3-6578-300
Fax: 886-3-6578-370

Taiwan - Kaohsiung
Tel: 886-7-536-4818
Fax: 886-7-536-4803

Taiwan - Taipei
Tel: 886-2-2500-6610
Fax: 886-2-2508-0102

Thailand - Bangkok
Tel: 66-2-694-1351
Fax: 66-2-694-1350

EUROPE

Austria - Wels
Tel: 43-7242-2244-39
Fax: 43-7242-2244-393

Denmark - Copenhagen
Tel: 45-4450-2828
Fax: 45-4485-2829

France - Paris
Tel: 33-1-69-53-63-20
Fax: 33-1-69-30-90-79

Germany - Munich
Tel: 49-89-627-144-0
Fax: 49-89-627-144-44

Italy - Milan
Tel: 39-0331-742611
Fax: 39-0331-466781

Netherlands - Drunen
Tel: 31-416-690399
Fax: 31-416-690340

Spain - Madrid
Tel: 34-91-708-08-90
Fax: 34-91-708-08-91

UK - Wokingham
Tel: 44-118-921-5869
Fax: 44-118-921-5820

03/20/09

WORLDWIDE SALES AND SERVICE

Words in the first box refer to products, the second box to geographic locations, and the third box refers to final order date or futures contracts.