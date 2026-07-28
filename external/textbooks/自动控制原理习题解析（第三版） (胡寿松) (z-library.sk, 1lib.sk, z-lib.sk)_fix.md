> OCR by deepseek-ai/DeepSeek-OCR | 397 pages

### Page 1

### Page 2

### Page 3

### Page 4

本书是与胡寿松教授主编的《自动控制原理》(第七版) 《科学出版社》配套的学习指导性教学用书。为了满足广大读者学习和掌握自动控制技术的需求,同时也是为了杜绝众多强行与胡寿松主编的《自动控制原理》配套的错误百出的所谓“三导”习题解答对读者的错误导向,我们编辑了这一本习题解析,以正视听。

本书系统地给出了《自动控制原理》(第七版)一书中全部习题的详解,这些习题包含了如题解、基本题、证明题、工程应用题、MATLAB题、设计题和难题等七类型题。在习题解析过程中,给出了解题指导思想的友情提示,且在科学、完备的解答后,给出求解的 MATLAB 文件,这不但便于核实运算结果的正确性,而且便于修改参数,完善控制系统设计性能。本书图文并茂,可使读者进一步升为对控制理论的掌握和应用。本次修订,进一步规范了全书题解,完善解题过程并突出新精、难、实等特点。

本书强化了理论联系实际的举措,紧密结合工程应用,其中设计及应用题涉及多个应用领域。在民用工业控制方面,有双摆系统建模,机器人关节行向控制、造纸系统张力控制、机械爪系统性能分析,打磨机器人参数选择、热轧机控制、自动化.
资料来源\l船举,汽车点火系统调节、机器人取力协调控制、运动操场模拟控制,磁悬浮系统分析、汽车悬架系统控制等;在航空航天方面,有宇航员机问控制,飞机横滚控制,垂直起飞已知黄飞进性分析,火星漫游车导航控制空间站方位控制、变质量民航控制·航天飞机人工室紫作调控·空间机器人控制,卫星回收系统参数选择,空间 Kreis 变控制,太阳月亮观系统控制,空间机器人的内模粮控制等;在船舶工业方面,有船舶舵不倒控,整船滑落雷控制;在生物医疗保健方面,有城市生态系统建模·医学激光操纵系统控制,医用麻醉系统参数选择.电动轮椅速度控制等。众多的工程应用,可使读者开阔眼界,扩大专业知识领域。

我们相信,通过学习和应用本书,读者一定会在定性分析能力、定量计算能力、综合运用能力、MATLAB 编程能力以及数形结合能力等方面,得到进一步提高。

本书由胡寿松教授主编,张敬博主主纾编。在本书编者过过程里,得到了陶洪峰,张军峰,孙新柱,同亚群,刘亚,王源,徐德友,杜贞斌,张正道,侯霞,蔡俊伟.许洁,袁侃张荣杰,晏莹黄江梅,信,平霜,黄小波,丁勇,双维芳,王风如,王从庆等的支持和协助,在此深致谢忱。

对于本书存在的疏漏和不妥之处,悬请广大读者不吝指正。

胡寿松

2016年9月

---

* 若书有章节里有的章图号分别于主教材(自动控制原理(第七版)),而解题过程已经更换图示的图,其图号以题排序。

### Page 5

perspective on the localization of emergency services in various countries. 

目录 
前言 
第一章 自动控制的一般概念 1 
第二章 控制系统的数学模型 8 
第三章 线性系统的时域分析法 38 
第四章 线性系统的根轨迹法 83 
第五章 线性系统的频域分析法 134 
第六章 线性系统的校正方法 177 
第七章 线性离散系统的分析与校正 219 
第八章 非线性控制系统分析 255 
第九章 线性系统的状态空间分析与综合 298 
第十章 动态系统的最优控制方法 356 
参考文献 391

### Page 6

### Page 7

]]> \[\]
---
**图 1-22 仓库大门自动开闭控制系统原理图**

之, 当今上关门开关时, 伺服电动机反向转动, 带动绞盘转动使大门关闭, 从而实现了远距离自动控制大门开启的要求。 仓库大门自动控制系统原理方块图如图 1-2-1 所示。

**图 1-2-1 仓库大门自动开闭控制系统方块图**

1-3 图 1-23(a) 和(b) 均为自动调压系统。设空载时, 图(a) 无差系统和图(b) 有差系统的电机端电压均为 110 V。试问带上负载后, 图(a) 和图(b) 中哪个系统能保持 110 V 电压不变？哪个系统的电压会稍低于 110 V？为什么？

**图 1-23 自动调压系统原理图**

解 本题通过自动调压系统工作原理的分析, 使学生学会区分有差系统和无差系统。 系统带上负载以后, 图 1-23(a) 和(b) 两个系统的端电压均会下降。但是图 1-23(a) 中的系统由于自身调压作用能够恢复到 110 V, 而图 1-23(b) 中的系统不能够恢复到 110 V, 其

### Page 8

-responsive interfaces of control systems and apply normal insulation techniques for extinguishing the short circuit fault. Curvature law of distribution system shows that the intruders of power distribution lines should not have the same with the intruders of buses or train discharging. 末端电压将稍低于 \( 110\text{V} \)。

划外图 1-23(a)中的自动调压系统: 当发电机两端电压低于给定电压时, 其偏差电压经放大器放大使伺服电机SM转动, 经减速器带动电刷, 使发电机的激磁电流增大, 提高发电机G的端电压, 从而使偏差电压减小, 直到偏差电压为零, 致使伺服电机停止转动。因此, 图1-23(a)中的自动调压系统能保持端电压110V不变。

图1-23(b)中的自动调压系统: 当发电机两端电压低于给定电压时, 其偏差电压直接经放大器使发电机的激磁电流增大, 提高发电机的端电压, 即发电机G的端电压回升, 此时偏差电压减小, 但偏差电压始终不能为零, 因为当偏差电压为零时, 激磁电流也为零, 发电机不能工作。因此, 图1-23(b)中的自动调压系统端电压不会低于 \( 110\text{V} \)。

对于图1-23(a)中自动调压系统, 当发电机两端电压低于给定电压时, 其偏差电压直接经放大器使发电机的激磁电流增大, 提高发电机的端电压, 即发电机G的端电压回升, 此时偏差电压减小, 但偏差电压始终不能为零, 因为当偏差电压为零时, 激磁电流也为零, 发电机不能工作。因此, 图1-23(b)中的自动调压系统端电压不会低于 110V。

图1-24为水温控制系统原理示意图。冷水在热交换器中由通人的蒸汽加热, 从而得到一定温度的热水。冷水流量变化用流量计测量。试绘制系统方块图, 并说明为了保持热水温度为期望值, 系统是如何工作的? 系统的被控对象和控制装置各是什么?

解 本题通过温度控制系统工作原理的分析, 使学生掌握系统方块图的绘制方法, 并正确区分被控对象和控制器。 水温控制系统的方块图如图1-41所示。

水温控制系统
\[\begin{array}{c}
\text{热水流量} \\
\text{制冷剂流量}
\end{array}\]

水温控制系统方框图

图1-24水温控制系统原理图

加热部分
\[\quad \text{加热部分}\]

冷却部分
\[\quad \dfrac{\text{加热部分}}{\text{无温器T}}\]

冷却块
\[\quad \text{冷却装置}\]

### Page 9

Power Transformer Layer

电力电子技术原理

**图 1-25  电炉温度控制系统原理图**

电力电子技术原理

**图 1-25  电炉温度控制系统原理图**

电炉使用电阻丝加热，并要求保持炉温恒定。图中采用热电偶来测量炉温并将其转换为电压信号，将测量得到的电压信号反馈到输入端，与给定电压信号成极性连接，实现负反馈。二者的差值称为偏差电压，它经电压放大和功率放大后驱动直流伺服电动机。电动机经减速器带动调压变压器的可动触头，改变电阻丝的供电电压，从而调节炉温。

当炉温偏低时，测量电压 \( u_d \) 小于给定电压 \( u_0 \) ，二者比较的偏差电压为 \[ \Delta u \approx u_0 - u_d \]。由于 \[ \Delta u \] 为正，电动机“正”转，使调压器的可动触头上移，电阻丝的供电电压增加，电流加大，炉温上升，直至炉温升至给定值为止。此时，\[ u = u_d \]，\[ \Delta u = 0 \]，电动机停止转动，炉温保持恒定。

当炉温偏高时，\[ \Delta u \] 为负，经放大后使电动机“反”转，调压器的可动触头下移，使供电电压减小，直至炉温等于给定值为止。

系统的被控对象是电炉，被控量是电炉炉温，伺服电动机、减速器、调压器是执行机构，热电偶是检测元件。

电炉温度控制系统的方块图如图 1-5-1 所示。

**图 1-5-1  电炉温度控制系统方块图**

**1-6** 图 1-26 是自整角机随动系统原理示意图。系统的功能是使接受自整角机 TR 的转子角位移 \[ \theta \] 与发送自整角机 TX 的转子角位移 \[ \theta_1 \] 始终保持一致。试说明系统是如何工作的，并指出被控对象、被控量以及控制装置各部分的作用并画出系统方块图。

**解** 本题以角度随动系统为例，要求分析系统工作原理，绘出系统方块图，并明确系统组成。

发送自整角机的转子与给定轴(主动轴)相连，接收自整角机的转子与负载轴(从动轴)相连。TX 与 TR 相角差测量电路。若发送自整角机的转子离开平衡位置转过一个角度 \[ \theta \]，则在接收自整角机转子的单相绕组上将感应出一个偏差电压 \[ u_e \]，它是一个振幅为 \[ u_{em} \]，频率与发送自整角机激磁频率相同的交流调幅电压，即

### Page 10

power_factor.有时将电力系统方法抽象成 图 1-26 自整角机随动系统原理示意图

### 图 1-26 自整角机随动系统原理示意图

---

\[ u_e = u_{m} \sin \omega t \]

在一定范围内, \( u_{m} \) 正比于 \( \theta_i - \theta_o \), 即 \( u_{m}=k_e (\theta_i - \theta_o) \), 其中 \( k_e \) 为自整角机传递系数, 所以可得 

\[ u_e=k_e (\theta_i- \theta_o )\sin \omega t \]

上述为随动系统中接收自整角机所产生的偏差电压的表达式, 它是一个振幅随角偏差(\(\theta_o-\theta_i\))的改变而变化的交流电压。因此, \( u_e \) 先经过相敏整流放大器变为直流电压, 再经过功率放大器放大, 放大后的直流信号作用在伺服电动机电枢两端。电动机通过减速器带动负载和接收自整角机的转子, 使其跟随发送自整角机的转子旋转, 实现\(\theta_o = \theta_i \), 以达到跟随的目的。为了使电动机转速恒定、平稳, 引入了测速负反馈。

系统的被控对象是负载转轴, 被控量是负载轴转角\(\theta_o \), 电动机和减速器是执行机构, 相敏整流放大器与功率放大器起着放大信号的作用, 测速发电机是转速反馈元件, 用以改善系统性能。

自整角机随动系统的方块图如图 1-6-1 所示。 

### 图 1-6-1 自整角机随动系统方块图

分解自整角机随动系统的方块图如图 1-6-1， 从图可知换扇为一种复杂的， 主要是因为伺服控制， 这样型的运动过程的产生是因为电流信号的影响。 这类机械过程的运动在到电动机转速与电动机调整变频器电枢处连接的端子变通过电动机轴从电动机卸载。

1. 在有控制的控制领域中,  

1. 起反并伺服控制系统基本原理框图

1. 有电机驱选相似关系的调整器和调节器。它的意思如下面。

图 1-31 接电机可转换自肠响关系成制动扬为动力转轴好和。根认控委机表面作业是经过机械运动也发布产品，描述发抱有质量守机组观察自然驱激系统运动器根实件呼应。

    
 1.7 在电动机驱动控制的开环控制系统中,为什么说一种补偿装置只能补偿一种与之相应的旋转动力系统？对于图 1 - 6 短机械的转速控制系统,当电动机的微磁电压变化时,转速如何变化?该种补偿装置能否补偿这种转速的变化？  

1. 天津研究电车的控制开环控制系统的工作原理。 

接电动机数升开理电机。检测为电调整电流操，户于分亢 Polish,发电调短更切电进到无， 控电机。
理由方式以电整机电分项与特利可电西传见牵，理松牛转对对产 Bolshevik换及。 

解  国把开系统中的实际转条初中街光电子祠迎据，就是加和式电本体规定开。延考核新一个超式提升共或。机图erti
由步骤半今线维或三点消c出与数简情机理各维尔合角缩短 &负，电与电任何。******比。8

### Page 11

-responsive mode="pop" data="""></style>

Fig. 1-6 Shows the dynamic parameter table. If equation (1-13) is substituted into equation (1-9), the dynamic transfer function for control can be obtained:
\[ Z_{c(s)} = \frac{Kb + Ma(s)}{1 + Ka(s)} \]

\[\begin{split}
&u_c = u_m + k_1 s + k_f = k_2 I_c + k_f I_m\\
&i = k_2 I_c + I_b + I_m = k_3 + I_m = ra = k_4 I_m
\end{split}\]

(9) Taking into account the hysteresis characteristics of the relative motion, the hysteresis model is established by spline function:
\[ i_k = i_{k-1} + (11$$k - k_{\alpha_l}$$ )a + $$k_1$$ - $$k_{\beta $$I_k\]

Fig. 1-8 shows the keyboard control by configuration of hardware, like Intel854 and TMS320C6713, this hardware platform is used as the control system of automatic sprinkler. The initial value is not set in advance as needed.
Slice subcode is output from the program control by an initial value. Data produced by programs are saved in data corner and System Information generates. 

The program control is performed by digital circuit, and the input and output data pair controls the water pump operating parameters to control the system.

Fig. 1-6: Outline of digital controlled system (Pic: 1-6.gif) 
Fig 1-6 Block diagram of controller system  

To control the water level, the controller must receive the water level information textually control. A nonlinear static control model is given as follows:

Fig 1-7 shows the flow diagram to control water level of the ship, the nonlinear static optimal control function is selected, as shown in Fig. 1-7. When the impulse signal timing control by a software signal.
Fig 1-7: Figure 1-7 shows the control process of ship water level.  

The above subjects in this article can control the water level by indirectly calculating the value.

### Figure 1-8
\[\begin{align*}
&\text{Figure 1-8: The relationship among water level and input and output signal or control parameters.} \\
&1-\text{Hill-Fellow-Trigonometric function} \\
&2-\text{Relinquishing/minus signal} \\
&3-\text{To control machine signal} \\
&4-\text{System signal data} \\
&5-\text{System signal data} \\
\end{align*}\]

\( \text{Figure 1-8 shows the water control diagram.} \)
\(\text{Figure 1-8} \) shows the water control diagram. It is aimed at directly controlling water pump application indicators to control \(\text{port}=C\) open valve, programming of upper arm height control and elevation ladder system. \(\text{The intelligent water control system in both control shows the relationship diagram and structure.} \)

In this article, the process controller combines the static and hard data transfer. Based on the hardware and software to transport water pumped system control information source, it is achieved abstract.
Fig 1-8: Information for automated sprinkler control.

### 实验原理

外开放的 Otto 气体内驱式液压摆动泵组例

根据文献[10]和文献[11]的数据曲线结合液压摆动泵组例的数学模型，建立了以百分比表为输出量的模型. 

Fig 1-9 模拟该系统的基本结构图.
Fig 1-9: Basic structure diagram.
Pallet Inter.

### Page 12

图1-28机床刀具进给系统方块图

置.保证刀尖的运动轨迹符合工件的轮廓形状,使就可以加工出所要求的零件.
    1-10下列各式渠道系统的微分方程,其中c(t)为输出量,r(t)为输入量,试判断哪些是线性定常或时变系统,哪些是非线性系统.
    
    c(t )=5+r²(t)+Γ+𝑄2(r( chapter4
    drc2(t)
    
    d²xc(t )
   

   1-(2) ) 𝑘 (𝑡)抵 Γ
)
)


    |
(total

) =**

    𝑓


    

   2['('X)
    
---->

    r


(`xc`()    c os ̆1+=i)

    -30    

    5,Gs"""

hours.)    rs%
r^(    I_{'')

    9)1<cm
   9)
=    

(crm%)
    
    
    
    
    

   
    

(2)
    5
)r'))))  ri =

    
   6

    
(9 = )   . dy , . \(." ]安全的 1 ().<.s)

    
    
p_)^`2

    [4
    .- )    

    (
    [(3)PY

   
    10

    6
    .
    1?
)(
  _-)

    和了时刻
    (F项:safe   
   
    
   试题
勾
再 )=
    ..
质χ 

    

密

单位:  .  y`)c

(.text:r:
    314 
    
    
    
    
    h.
    
`;
v WE >:
    2`) the
    

    
    
(
    \[ 
     (. 89 u <)  179) =  1
 \)    2 

    
    

 \(.    .@w)] )
    
    

    
 \(\displaystyle)`

6o
    

    \(y
)
135    

    T   
    

    
    

    
j. c/: 
\(10^3
    \(\cdots ...
    
    .' Pre 
    
    #
    
    .[[**). t      

    l b
    
}
    

    
    
】

    A b Joint,.
    
    

\[
    \sqrt{0}\]

    
    
    
    
\(
..... \____ r

    
\```

    

    推)
-
    
:



d' 
    

   

\]

)

\(\_{2/\}\)\(\-\(\_3a): 

\]

    

 
    

 
 
 .k 

    
    
    
 
 
' \_\-La 

    
    *_(
 )
 \(\)

**)
y
' )

    
    *
t })

    

    
    
    
    
    
    
    
    

    
    \(    图
    . 论文上 ._考)

    
 

    
    
    
.

    
9
    
)
=.门
    
-:

    
    _{:`code}_{_

    
    

. 
    
    _{
    _ 

void `On=NULL
    
    
    
    
. output
    
    
    - 

    

*,

    
    

    
    

    \(_
;
0);  120,
    
)})
    
   }Chey .  
    U.= 
    
 &.  """
    
    ]
    
[9a 
    
BIOS output
    

    
   
    _ TIF
	
    
    110\.ERROR
    100\.WARNING
    
    

    
=
    
....
    
A

    300\
    
    
    
 

    
    

    _{A\}
    
    

    

    图 -
 
 WT_ 
ertfrakel().

    
    
   
  
.}
))

    
    _const \\
    
    
    
    

)    

 
 
 :

    

\[

    case 120
future

    }\
====

739
    }

    

. 

    
    const

 

    APRINT.cnt!

   
    
---

的值
 
    
    

    \[such\_searching)\]

    
    如果
 
    

    
    

   
    
    14
    
**---
    ^交易

   at 

    

    日志中 
    \<
=.

    130
####-&\
   
    
  :=Cli= \
    
    输出
    
    
    的
type}..&
   

    的
    

    )

    
    /*
    
    ..

### Page 13

**第二章 控制系统的数学模型**

**2-1** 在图 1-21 的液位自动控制系统中, 设容器横截面积为 \(F\), 希望液位为 \(c_0\). 若液体高度变化率与液体流量差 \(Q_1 - Q_2\) 成正比, 试列写以液位为输出量的微分方程式。

**解** 本题研究建立液位控制系统的微分方程数学模型。当 \(Q_1 = Q_2\) 时, 液位的高度为 \(c_0\); 当 \(Q_1 \neq Q_2\) 时, 液位的高度 \(c\) 将发生变化。由于液体高度变化率与液体流量差 \(Q_1 - Q_2\) 成正比, 所以有 

\[F \frac{{dc}}{{dt}} = Q_1 - Q_2\]

则以液位为输出量的微分方程式为

\[\frac{{dc}}{{dt}} = \frac{1}{F} (Q_1 - Q_2)\]

**2-2** 设机械系统如图 2-48 所示, 其中 \(x_i\) 是输入位移, \(x_o\) 是输出位移。试分别写出各系统的微分方程。

图 2-48 机械系统原理图

**解** 本题研究建立机械系统的微分方程数学模型。

(1) 对于图 2-48(a) 所示系统, 根据力平衡方程, 在不计重力时, 可得

\[f_1 (\dot{x}_i - \dot{x}_o) - f_2 \dot{x}_o = m \ddot{x}_o\]

则系统的微分方程式为

\[m \frac{{\mathrm{d}^2 x_o}}{{\mathrm{d}t^2}} + (f_1 + f_2) \frac{{\mathrm{d} x_o}}{{\mathrm{d}t}} = f_1 \frac{{\mathrm{d} x_i}}{{\mathrm{d}t}}\]

(2) 对于图 2-48(b) 所示系统，在上部分弹簧与阻尼器之间取辅助点 \(A\)，并设 A 点位移为 \(x\)，方向向下。根据力平衡方程，在不计重力时，可得方程

\[K_1 (x_i - x) = f (\dot{x} - \dot{x}_o)\]

\[K_2 x_o = f (\dot{x} - \dot{x}_o)\]

消去中间变量 \(x\), 由于

### Page 14

\[K_2 x_o = K_1 (x_i - x),\quad x = x_i - \frac{K_2}{K_1} x_o,\quad \dot{x} = \dot{x_i} - \frac{K_2}{K_1} \dot{x_o}\]

故有

\[K_1 K_2 x_o = K_1 f \dot{x} - K_1 f \dot{x_o} = f K_1 \dot{x} - f K_1 \dot{x_o} - f K_2 \dot{x_o}\]

则系统的微分方程式为

\[f (K_1 + K_2) \frac{\mathrm{d} x_o}{\mathrm{d} t} + K_1 K_2 x_o = K_1 f \frac{\mathrm{d} x_i}{\mathrm{d} t}\]

（3）对于图 2-49（c）所示系统，根据力学方程，在不计重力时，可得

\[K_1 (x_i - x_o) + f (\dot{x_i} - \dot{x_o}) = K_2 x_o\]

则系统的微分方程式为

\[f \frac{\mathrm{d} x_o}{\mathrm{d} t} + (K_1 + K_2) x_o = f \frac{\mathrm{d} x_i}{\mathrm{d} t} + K_1 x_i\]

图 2-49 电网与机械系统原理图

2-3 试证明图 2-49（a）的电网络与图 2-49（b）的机械系统有相同的数学模型。

\[\begin{array}{cc}
 &  \\
(a) 电网络 & (b) 机械系统 \\
\end{array}\]

解 本题研究用拉氏变换法建立系统的传递函数数学模型。

（1）对于图 2-49（a），根据复数阻抗的方法可得电网络的传递函数为

\[G_o (s) = \frac{U_o (s)}{U_i (s)} = \frac{R_2 + \frac{1}{C_2 s}}{R_1 + \frac{1}{C_1 s} + (R_2 + \frac{1}{C_2 s})}\]

\[= \frac{R_1 R_2 C_1 C_2 s^2 + (R_1 C_1 + R_2 C_2) s + 1}{R_1 R_2 C_1 C_2 s^2 + (R_1 C_1 + R_2 C_2 + R_1 C_2) s + 1}\]

（2）对于图 2-49（b），在弹簧 \(K_1\) 和阻尼器 \(f_1\) 之间引入辅助点，设其位移为 \(x\)，方向向下。根据力学方程，在不计重力时，可得

\[K_2 (x_i - x_o) + f_2 (\dot{x_i} - \dot{x_o}) = f_1 (x_o - \dot{x}),\quad K_1 x = f_1 (\dot{x_o} - \dot{x})\]

对上述两式进行拉氏变换，考虑初始条件为零，可得

\[K_2 X_i (s) - K_2 X_o (s) + f_2 \cdot s X_i (s) - f_2 \cdot s X_o (s) = f_1 \cdot s X_o (s) - f_1 \cdot s X_i (s)\]

\[X_i (s) = f_1 \cdot s X_o (s) - f_1 \cdot s X_i (s)\]

消去中间变量 \(X(s) = \frac{f_1 s}{K_1 + f_1 s} X_o (s)\)，有

### Page 15

\[[K_{2}+f_{2}s]X_{i}(s)=\left(K_{2}+f_{2}s+\frac{K_{1}f_{1}s}{K_{1}+f_{1}s}\right)X_{o}(s)\]
则机械系统的传递函数为
\[G_{b}(s)=\frac{X_{o}(s)}{X_{i}(s)}=\frac{f_{1}f_{2}s^{2}+\left(K_{1}f_{2}+K_{2}f_{1}\right)s+K_{1}K_{2}}{f_{1}f_{2}s^{2}+\left(K_{1}f_{2}+K_{2}f_{1}+K_{1}f_{1}\right)s+K_{1}K_{2}}\]
\[\frac{f_{1}f_{2}}{K_{1}K_{2}}s^{2}+\left(\frac{f_{1}}{K_{1}}+\frac{f_{2}}{K_{2}}\right)s+1\]

通过比较\(G_{b}(s),G_{b}(s)\)可知：两传递函数的类型相同，即图2-49(a)的电网络与图2-49(b)的机械系统有相同的数学模型。

2-4 试分别列写图2-50中各无源网络的微分方程式。

图2-50 无源网络电路图

解 本题研究网络数学模型的建立方法。

(1) 对于图2-50(a)所示的无源网络，设通过电阻\(R_{1}\)的电流为\(i_{1}\)(方向自左向右)，通过电容\(C\)的电流为\(i_{2}\)(方向自左向右)，通过电阻\(R_{2}\)的电流为\(i\)(方向自上下)，根据电压平衡可得
\[\begin{cases}
R_{1}i_{1}=\frac{1}{C}\int i_{2} d t \\
u_{o}=R_{2}i=R_{2}(i_{1}-i_{2}) \\
u_{i}=R_{1}i_{1}+u_{o}
\end{cases}\]
\[\left( \begin text{}, u_i= R_1i+u_{o}  \\ i i  \right)\]

于是
\[\left( \begin text{}, i=i_1-u_1-C1C2 \\ i=i_2=u_2-C1C2 \\ i=i_3+u_3-C1C2 \\ i=i_4-C1C2 \end  \end  \text{ } uu \end  text\)\]
整理后可得图2-50(a)所示的无源网络的微分方程为
\[R_{1}i_{1}+R_{1}i_{1}=-R_{2}u_{2}  \\R_{1}2 du_{2}+(R_{1}+R_{2}u_{1})6\]

整理后可得图2-50(a)所示的无源网络的微分方程为\]\]图的编辑模式为
图修改后模式为（文档名字：） R1Ci+C2 -i=(-u2) C 3-U1 C2
 \[图2-50 general
I= 图2-50 general

### Page 16

indicates 16as not present in database.

### Page 17

.故该方程的运动模态为 \( e^{-0.5t} \sin \dfrac{\sqrt{3}}{2}t_0 \)。因此，\( x(t) \)曲线如图2-5-2所示。
\[  \]
图2-5-1 系统(1)单位斜坡响应曲线（MATLAB(3) \[  \]
图2-5-2 系统(2)单位脉冲响应曲线（MATLAB(3) \[  \]
\[  \]
图2-5-3 系统(3)单位阶跃响应曲线（MATLAB(3) \[  \]

2-6 在液压系统管道中,设通过阀门的流量 \( Q \) 满足流量方程
\[  Q=K \sqrt{P}    \]
式中，\( K \)为比例系数;\( P \)为阀门前后的压差。若流量 \( Q \) 与压差 \( P \) 在其平衡点 \((Q_{0},P_{0})\)附近作微小变化,试导出线性化流量方程。

解 本题考查流量非线性微分方程的线性化,具体做法是,对非线性微分方程在其平衡点附近用泰勒级数展开并取前面的线性项,得到等效的线性化方程。在平衡点\( (Q_{0},P_{0}) \)处,对流量 \( Q \) 泰勒展开并取一次项近似可得
\[  Q \approx Q_{0} + \dot{Q}|_{Q_{0}(P-P_{0})}=Q_{0} + \dfrac{K}{2 \sqrt{P_{0}}}(P-P_{0})    \]
则线性化流量方程为
\[  \Delta Q=\dfrac{K}{2 \sqrt{P_{0}}} \Delta P    \]

- 12 -

### Page 18

省去符号" Δ", 上式可以简写为 \( Q = K_1P, \quad K_1 = \frac{K}{2\sqrt{P_0}} \)

2-7 设弹簧特性由下式描述:
\( F = 12.65y^{1.1} \)

其中, \( F \) 是弹簧力, \( y \) 是变形位移. 若弹簧在变形位移 0.25 附近作微小变化, 试推导 \( \Delta F \) 的线性化方程.

解析 本题考查弹簧元件非线性微分方程的线性化, 具体做法是对非线性微分方程在其平衡点附近用泰勒级数展开并取前面的线性项, 得到等效的线性化方程.
在 \( y=0.25 \) 处对 \( F \) 进行泰勒展开, 并取一次项近似可得
\[F \approx F_0 + \dot{F}|_{y=0.25} (y - 0.25)\]
由上式可知, \( \Delta F \) 的线性化方程为
\[\Delta F \approx F - 2.75 = \dot{F}|_{y=0.25} (y - 0.25) = 12.65 \times \dfrac{1.1 \times (0.25)^{0.1}\times (y-0.25)}{1.1} = 12.1\Delta y\]
上式亦可简化表示为 \( F=12.1y \).

2-8 设晶闸管三相桥式全控整流电路的输入量为控制角 \( \alpha \), 输出量为空载整流电压 \( e_d \), 它们之间的关系为
\[e_d = E_{d_0}\cos\alpha\]
式中 \( E_{d_0} \) 是整流电压的理想空载值, 试推导其线性化方程式.
解析 本题考查电路非线性微分方程的线性化, 具体做法是, 对非线性微分方程在其平衡点附近用泰勒级数展开并取前面的线性项, 得到等效的线性化方程.
在 \( \alpha=\alpha_0 \) 处对 \( e_d \) 进行泰勒展开, 然后取其一次项近似可得
\[e_d \approx e_{d_0} + \dot{e}_d |_{\alpha=\alpha_0} (\alpha-\alpha_0) = e_d |_{\alpha=\alpha_0} - \left[ E_{d_0}\sin\alpha_{d_0}\right](\alpha-\alpha_0)\]
由上式可得全控整流电路的线性化方程为
\[\Delta e_d = -[E_{d_0}\sin\alpha_{d_0}]\Delta\alpha\]

2-9 若系统在阶跃输入 \( r(t)=1(t) \) 时, 零初始条件下的输出响应 \( c(t) = 1 - e^{-2t} + e^{-t} \),
试求系统的传递函数和脉冲响应.
解析 本题用拉氏变换法研究系统输出响应与传递函数之间的关系.
系统在阶跃输入 \( r(t)=1(t) \), 即 \( R(s)=\frac{1}{s} \), 系统的输出响应为 \( c(t)=1-e^{-2t}+e^{-t} \), 即
\[C(s)=\dfrac{1}{s}-\dfrac{1}{s+2}+\dfrac{1}{s+1}=\dfrac{s^2+4s+2}{s(s+2)(s+1)}\]
则系统的传递函数为
\[\dfrac{C(s)}{R(s)}=\dfrac{s^2+4s+2}{s(s+2)(s+1)}=s-\dfrac{s^2+4s+2}{(s+2)(s+1)}\]
于是, 系统脉冲响应为

解析 本题考查电路非线性微分方程的线性化, 具体做法是, 对非线性微分方程在其平衡点附近用泰勒级数展开并取前面的线性项, 得到等效的线性化方程.
在 \( \alpha=\alpha_0 \) 处对 \( e_d \) 进行泰勒展开, 然后取其一次项近似可得
\[e_d \approx e_{d_0} + \dot{e}_d |_{\alpha=\alpha_0} (\alpha-\alpha_0) = e_d |_{\alpha=\alpha_0} - \left[ E_{d_0}\sin\alpha_{d_0}\right](\alpha-\alpha_0)\]
由上式可得全控整流电路的线性化方程为
\[\Delta e_d = -[E_{d_0}\sin\alpha_{d_0}]\Delta\alpha\]

2-9 若系统在阶跃输入 \( r(t)=1(t) \) 时, 零初始条件下的输出响应 \( c(t) = 1 - e^{-2t} + e^{-t} \),
试求系统的传递函数和脉冲响应.
解析 本题用拉氏变换法研究系统输出响应与传递函数之间的关系.
系统在阶跃输入 \( r(t)=1(t) \), 即 \( R(s)=\frac{1}{s} \), 系统的输出响应为 \( c(t)=1-e^{-2t}+e^{-t} \), 即
\[C(s)=\dfrac{1}{s}-\dfrac{1}{s+2}+\dfrac{1}{s+1}=\dfrac{s^2+4s+2}{s(s+2)(s+1)}\]
则系统的传递函数为
\[\dfrac{C(s)}{R(s)}=\dfrac{s^2+4s+2}{s(s+2)(s+1)}=s-\dfrac{s^2+4s+2}{(s+2)(s+1)}\]
于是, 系统脉冲响应为
\[c(t)=\mathcal{L}^{-1} \left[ \dfrac{s^2+4s+2}{s(s+2)(s+1)}} \right]=\mathcal{L}^{-1}\left(1-\dfrac{1}{s+1}+\dfrac{2}{s+2}\right)\]

\*13\*

### Page 19

.\begin{document}
时间: \( t = 0, c(t) = r(t) = R \)

初始条件: \( r(0) = r''(0) = 0, c(0) = 1, r(0) = 2, c(0) = 2 \)

已知系统的传递函数
\[ c(t)e^{kt} \]
\[ c(t) = e^{kt} \]

高斯系统

\[\frac{s}{c(s)} = \frac{1}{2} e^{-t}, c'(s) = e^{-kt}\]
 
求解

\[ s^2 + 2s + 2c'(s) - 2c'(s) = c(s) + c'(s) = 1 + 2e^{-jt}\]
解

\[ (s+2)^2 + s^2 + c'(s) - 2c'(s) = 0\]

解
\[ (s+2)^2 + c'(s) = 2c(s) - 2c'(s)\]
 
解
其解
\[ c(s) = (s+2)^2 + 2s + 2c'(s)\]
解
\[ c(s) = \frac{s^2 + 3s + 2}{s^2 - 3s+1}\]
解
\[ c'(s) = \frac{-2s + 3}{s^2 + 3s + 2} \] 
解
\[ c'(s)= \frac{-4}{s^2 + 3s + 2}\]
解
\[ c'(s) = \frac{-2s - 1}{s^2 + 3s + 2}\]

2.10 设系统的传递函数为 
\[ c(t)=e^{-t}$$

解：初等

\[ c(t)=e^t-\frac{2}{r}cos\theta + i(t)(-\frac{2}{r_os} cos(\theta - \omega t)] = e^{-t}[cos\cos\left.\frac{k}{r}- cos\left(\frac{-2}{r_os}\]

解初等方程

\[ \frac{cos cos\left(\theta - \omega t)]=(c^2s^2 + c^2(r\omega)]\[

解：\[ R(s) = 2 \]

解原始方程

\[ π其求解$Π(s) = (s^2 + 2+s)\]

解串联方程 \[+ s~解 ,

解： Λ放._式解法

(结：$s, \\   
R(s) = R(s)= \]

### Page 20

.由于数学公式较多，系统无法逐字识别，请根据示例进行修改。

所以传递函数 \( C(s)/R(s) \) 和 \( E(s)/R(s) \) 分别为  
\[ 
\phi(s) = \frac{C(s)}{R(s)} = \frac{100(s+1)}{12s^2 + 23s + 25}, \quad \Phi_e(s) = \frac{E(s)}{R(s)} = \frac{10(12s^2 + 23s + 25)}{12s^2 + 23s + 25}
\]

2-12 求图2-52 所示有源网络的传递函数 \( U_o (s) / U_i (s) \) 

\[\begin{array}{cccc}
    \text{图 2-52 有源网络电路图} \\
    \text{(a) } \quad \text{(b)} \quad \text{(c)}
\end{array}\]

解 本题研究用等效复数阻抗方法推导有源网络的传递函数的方法。  
(1) 对于图2-52(a)所示的有源网络，可得  
\[\frac{U_o (s)}{U_i (s)} = -\frac{R_1}{R_0} \cdot \frac{1}{C_0 s} = -\frac{R_1}{R_0} (R_1 C_0 s + 1)\]
\[\frac{U_o (s)}{U_i (s)} = -\frac{R_0 + \frac{1}{C_0 s}}{R_0 + \frac{1}{C_0 s}}\]
(2) 对于图2-52(b)所示的有源网络，可得  
\[\frac{U_o (s)}{U_i (s)} = -\frac{R_1 + \frac{1}{C_1 (s)}}{R_0 + \frac{1}{C_0 (s)}} = -\frac{R_1 C_1 R_0 C_0 s^2 + (R_1 C_1 + R_0 C_0) s + 1}{R_0 C_1 s}\]
\[\frac{U_o (s)}{U_i (s)} = -\frac{R_0 + \frac{1}{C_0 s}}{R_0 + \frac{1}{C_0 s}}\]
(3) 对于图2-52(c)所示的有源网络，可得  
\[\frac{U_o (s)}{U_i (s)} = -\frac{R_1 R_0 (R_2 + \frac{1}{C_0 s})}{R_0 (C_0 s + 1)} = -\frac{R_1 C_2 s + 1}{R_0 (R_1 + R_2) C_0 s + 1}\]
2-13 由运算放大器组成的控制系统模拟电路如图2-53所示，试求闭环传递函数 \( U_o (s) / U_i (s) \)。

解 本题研究用等效复数阻抗方法推导网络模拟系统的传递函数。  
在图2-53中，令第一级运算放大器输出为 \( U_1 \)，第二级运算放大器输出为 \( U_2 \)，则可得  
\[U_1 = -\frac{R_1 \cdot \frac{1}{C_1 s} (R_0 / R_0 + U_0)}{R_1 + \frac{1}{C_1 s}}\]

### Page 21

large motor¨ on the figure.考虑到从图中可见，但也不是完整的电动机结构分析假设还需要另一种类型的电动机结构，在齿轮N型电动机中，在定子铁芯上安装JL型旋转损耗元件与转轴轴端，轴与旋转损耗元件通过Iz轴固定并具有与轴和轴转动连接的，另一个轴则具有定子和磁化参数特征不变为Ko轴，即使键入磁场沿Q轴的方向，表面定子铁芯转侧方向形成磁力克服力矩。静力电场情况下，定子铁芯具有 professor, a慧转磁式电机结构模型的原理是，电机的磁速率是非稳态磁系统线性电流牵动模型的正常运行，长时间与轴承永不同坐动车辆进入电机，刻线闭锁电机产生的检修所需功措施思考之后为可知，转轴高速论文多见。注书中提到的定子绕组电织改具体识别方法与定子绕组电感设备技术的具体具体技术管理方案学。机械工程基础的压电传感器生产设备方案解释，径压电传感电机动态网细光学机械可运动性特点产链结构通，列空间下“较软较软”型压电传感器模电器的电机，如温，自然入机械网控制系统后的“舒软较为较软”压电传感器学，导压压电传感器于后体。而在各部压电传感器设备的关键创建技术下若在电磁电磁手段或下磁化其技术相关添加特别技术，能够在高校当前压电传感器设备波浪技术用于配电起及要开发的调压压电、温温压电设备测试环保标准方面都有很大改进。

(7)公式：
$$
\left.
\begin{aligned}
&\frac{1}{C_1}s+R_{0}(R_{0}\cup -\frac{R_{0}}{R_{0}})\left(\frac{\Delta}{R_{0}}+4C_{0}2U_{0}
\right)U=R_{0}
\end{aligned}
\right\} \begin{cases}
U=U(\nu)&U=f(0)U=\frac{R_{0}}{R_{0}}U_{0}\\
&(\lambda)\\&(-\frac{1}{R_{0}})\frac{ω_{m}(s)}{λ}\\&(\lambda)\\&(\omega-απω(ss))\\
\omega=0&U(ω)\\
b-aω(ss)\\end{cases}
$$
(2)-电机曲线中的变化为转动关系画曲线轨迹，此时电机结构的第一种超速超速转轴原理大部分构造结构讲解，转轴达到电、后电机编码运动特性，如何转轴中油电导电磁元件影响，在 domination straight不动柱旋转电机升功率带来的力特性，掌握电、定子空壳且-空隙间 Determinedemeldtend X fossil使后体，旋转磁力电电流时走电场电机首先需要获得电端估算转动接电保证高压(Nμ)定速的p=0(tt，高度为定因过程快速在构成电机电流等-磁浮现象还有下降电机电机更高电功率电机设计和制造有效性可靠电机转矩驱动电机磁场电机维护文件电机电机效率驱动л电机键电机恒速用途和设置措施并领域内的调控实施工序强烈强电机驱动力实电运行分及空间特性实际适用主要应用电驱动模电度来解决潮流 Motor各种窗口。可靠性在此基础上逐渐提高全电机可电性磁化达势事故达马终在的的显著效率，电磁场电机定拉功率（见）通发结构电机：电能表温度电机中电机特性取高热电机实现或者主要驱动与设备变频电机改造基础设计要求大》上在飞盘等研发电机在机移制式功率柜的高压电机的作用管理电机助老化控制。

(3)转速曲线综合观点建议——建议最电机启动发动功率提高传动制转油量改进电机功率提很依电机调速电力效果，常规电机功率所电机术技术人员深要实用适合电机 Michael电机升功率计算及估算可替代转排转动力效率新改技术。新建电机最大转推进直升机滚珠转换实现制动散热电冷却场电机式转轮或轨轴转换提供动力以供电机研发。(un)纯电机转功率最高产电模块其勒开发道路，电机一体化他机械改造新有效电机实验室客户只设备些测试经电机电检修确保单输出功率实验结果直接落实电机理论技术可保证高压电机RT电机精确转电所与电力数电机等参考过程电机界面开发。也可以直接火发电电机转主轴热能提取蓄系统在动力应用底机可以通过转学电机，主要电机实现动力吸附固定，近空电机高度电机电机推广。理论上双电机效率电机 стал设备利用智能工程夜间 Caldwell电机等补充布电机系统思路强势电机功率制作。当前电机范围空间设备研究磁环装备生产研发电不仅能下电动机扭矩上传通过功率斩波，电机功率提供准确电机研发等。

(m1)新一代成为典型系统在丰富控制技术结构分子的电机能量注解核技术。本次中央对结果一个输果载机改进中发电机整动机微前电机，其预期应用及与国家电机场基础电机变电大项目实现较小电机应用技术广泛移传构思技术创新与电机组试验：二次电#2交直接将研究建设较大规模意后续需要注意开发现电机技术电机物理应力电机与原航空电性能，工程应用技术电机结构电机制造 элемét毕米仪对设备类型周期化电机设备。

(8)结论：
到时候都要瞬间交流束象22从图片总结基于以下改变而来，比在电机功效上更进一步电机是运行电机特殊和电机皮电设备。从智能，自劳精髓里电机发展深基本配置和智能类型。

### Page 22

caner.\documentclass{article}
\usepackage{amsmath}
\begin{document}

Um(s) = \frac{1}{J_{ms} + f_m} = \frac{L_{a}s + R_a}{J_{m}s^2 + (L_{a}f_m + J_{m}R_a)s + f_mR_a + C_mC_e} \\

图2-14-1 直流伺服机构图 \\

\Omega_{m}(s) = \frac{1}{J_{ms} + f_m} = \frac{(L_a + R_a)}{J_{m}s^2 + (L_a f_m + J_m R_a)s + f_m R_a + C_m C_e} \\

2-15 某位置随动系统原理图如图2-54所示。已知电位器最大工作角度$\theta_{max} = 330^\circ$，功率放大级功放系数为$K_b$，要求: \\

(1) 分别求出电位器传递系数$K_b$，第一级和第二级放大器的放大系数$K_{b1}$，$K_{b2}$; \\

(2) 画出系统结构图; \\

(3) 简化结构图，求系统传递函数$\Theta_0(s)/\Theta_0(s)$ \\

图2-54 位置随动系统原理图 \\

解 本题研究通过系统的原理图得出结构图，并简化结构图，求出系统闭环传递函数。 \\

(1) 求$K_{b1}$和$K_{b2}$: \\

\[K_{b1} = \frac{E}{\theta_m} = \frac{30}{330^\circ \times \frac{\pi}{180^\circ}} = \frac{180}{11\pi} = 5.21 (\text{V/rad})\]

\[K_{b2} = \frac{K_{b2}}{3. = \frac{30 \times 10^3}{10 \times 10^3} = 3, \quad K_{2} = \frac{20 \times 10^3}{10 \times 10^3} = 2}\]

(2) 系统结构图假设电动机的时间常数为$T_m$可得直流电动机的传递函数为（忽略电枢电感的影响） \\

\[\frac{\Omega(s)}{U_a(s)} = \frac{K_m}{T_ms + 1}\]

其中$K_m$ 为直流电动机的传递系数。假设测速发电机的斜率为$K_t$，则其传递函数为 \\

\begin{align*}
& \text{图2-54 位置随动系统原理图} \\
& \text{解 本题研究通过系统的原理图得出结构图，并简化结构图，求出系统} \\
& \text{闭环传递函数。} \\
& \text{(1) 求} K_{b1} \text{和} K_{b2}: \\
& \text{例:} \\
& \text{设电压RL特性为} (V-14). \\
& \text{解得:} \\
& \text{K_{b1} = 30 / \pi \quad \theta_{max} = 330 = 5.21 (\text{V/rad})} \\
& \text{设系统结构图假设电动机时间常数100}\\
& \text{可得直流电动机的传递函数为(忽略电枢电感的影响)} \\
& \text{例:}\]
\end{align*}

\end{document}

### Page 23

}}s}}s}}u}}]]s}}]}}}}}s}}s-}}]}}s}}s-}}{\}}}s}}s}}}}s}}}s}}}}s}},s}}}}s}}s,s}}}}s}},
Fig. 2-15-1 Location-controlled system structure 

由于净化的结构图可得系统的传递函数为：

\[
\frac{\theta_o(s)}{\theta_i(s)} = \frac{K_0 K_1 \cdot \frac{K_2 K_3 K_m}{T_{sm} s + 1 + K_2 K_3 K_m K_t} \cdot \frac{1}{s}} {1 + K_0 K_1 \cdot \frac{K_2 K_3 K_m}{T_{sm} s + 1 + K_2 K_3 K_m K_t} \cdot \frac{1}{s}} = \frac{K_0 K_1 K_2 K_3 K_m} {T_{sm} s^2 + (1 + K_2 K_3 K_m K_t ) s + K_0 K_1 K_2 K_3 K_m}
\]

2-16 设直流电动机双闭环调速系统的原理线路如图2-55所示。

![Fig. 2-55 Schematic diagram of DC motor speed control system controlled by PI regulator and voltage feedback]
2-55[Fig. 2-55 Schematic diagram of DC motor speed control system controlled by PI regulator and voltage feedback]

### Page 24

idden events inwasserbar endendem richtet.“

(2) 画出系统结构图[设可控硅电路传递函数为 \( K_3/(T_3s+1) \); 电流互感器和测速发电机的传递系数分别为 \( K_4 \) 和 \( K_5 \); 直流电动机的结构图用题2-14的结果];
(3)简化结构图,求系统传递函数 \( \Omega(s)/U_i(s) \)。
解本题研究通过调速系统的原理图得出结构图,并简化结构图求出闭环传递函数。

(1) 求调节器的传递函数。速度调节器和电流调节器的传递函数分别为
\[G_1(s) = -\frac{R_1 + \frac{1}{C_1 s}}{R} = -\left(\frac{R_1}{R} + \frac{1}{RC_1 s}\right)\]
\[G_2(s) = -\frac{R_2 + \frac{1}{C_2 s}}{R} = -\left(\frac{R_2}{R} + \frac{1}{RC_2 s}\right)\]

(2) 画系统结构图。由于直流电动机的结构图用题2-14的结果,同时由于引入了电流反馈,故在电动机的动态结构图中必须把电枢电流 \( I_a \) 显露出来,于是直流电动机调速系统的结构图如图2-16-1所示。图 2-16-1 直流电动机调速系统结构图

(3) 求系统传递函数。为了推导方便,设
\[G_3(s) = \frac{K_3}{T_3 s + 1}, \quad G_4(s) = \frac{1}{L_0 s + R_0}, \quad G_5(s) = \frac{1}{J_m s + f_m}\]
则简化结构图如图2-16-2所示。

图 2-16-2 电机调速系统结构图简化

经过反馈连接等效,可得图2-16-3所示简化结构图。由简化的结构图可得系统的传递函数
\[\frac{Q(s)}{U_i(s)} = \frac{C_m G_1 G_2 G_3 G_4 G_5}{1 + K_4 G_2 G_3 G_4 + C_m G_1 G_5 + C_m K_5 G_1 G_2 G_3 G_4 G_5}\]

其中
图 2-16-3 简化后的系统结构图

### Page 25

}, { UI 206aoa aeeaia Ee 3n nEna eoa eeG anee .aiep Ie pJerdepe Jnd ea 3 T zhpp  इततस ज जचत यजमत Ie Tee je . Sejre 5a ri Wirl , na .v mm Jea nee Jeeeuetic m Jee Ie lo Ootus eee Un nleet r Uteisy uleJeeia . Ls te ea Ic l eeetfe a ch eh aee Je qe Iee, Lea a ee)ji Jn In aee uacn ue cegewle hly u mc E 5 - pije A 3e ae ceem eee uh Cr-e . se3 eje las oepe Ja ll n Ina sae e Ss oo Ie Ilee)ns ,le ce s o ee ue le le e I sseee Iee Au ee)ls. et ejuue te r eene L s a te saI pu)ee/JnSri Jeer / 2146 jnJnJCC.,iee Ic ,ia aee JeeAe) J n Jn. ula ae e. Jee Ga) ./348 Cren59412 je Iee-veILeI S : (8) T y5 -r JIn l.

Fig 2-16-3 Time detailed structure diagram

u 2. ( 4) ca ra . , J E E J r J ie.C . t Iidls. L } e . J n - e ua ra-rrat Iceoc H L as Ee0eJec, Is. e, nt e . essZ4c.. 5 24t 1. anro 5 C ee ce La car ce Er eer Fig 2-16:4: Circuit acceleration signal table

ゆ 8654703= (a)二 4640

JI 2mentare Jertia aea Jea Ccce eerQsrseechnt , ee cate R 4524Jgl 613 t e 5oo法律 ee ie Jee nl s Iee r Fee

( se3, 工) 儿 leae E3 2 .8.ni 605e1 a / nsco enee nee as feTc. / 12a 江二64 层 72078 atre e17 a Cn on -, se. S2 eye4 企业额 s r saSa r ae5a17 318 Fiaks\E4aa

\(C_7 (s) = - \left(\frac{R_1}{R} + \frac{1}{RC_1s} \right), \)

\(G_2 (s) = - \left(\frac{R_2}{R} + \frac{1}{RC_2s} \right),\)

\(G_3 (s) = \frac{K_3}{Ts+1}, \quad G_4 (s) = \frac{1}{L_s s + R_a}, \quad G_5 (s) = \frac{1}{J_{ms} + f_m } \)

可用信号流图（图2-16-4）及梅森增益进行验证。

\[ 146 \cdot v48qms 16J66 r\$ a e oma Ij gL69€4 16 zhtte rms. 14e65a\end {array}举点 i $\mathrm{G}_7$.

\[ = $K_s \L_G_4 $C_o_j $6 以上 41 a s

R1 111# 5 ZZ# B + I J6 C5\13J55\ L5m以来：

\[ \mathrm {j}_{14]{R\mathring{636{K}}+ 0 $K }53 = ½

M oJ.0 81"3IS42ga-Z+ 03J7

x @ 15Gl,\[Va6Jf ;0,T36L + +.msaa_ = 一一 +Q% J 1 I 906+813 993,, opes, U

\[ に =-(\{JC\cdot{66_{2}G_{4}-

J\ \赛\\

\[ 14 g(A;,i. \(5-E.g4m J!r8-j

### closing the codes while concluding this text. ```

## 剖面结构奇立特的CRC 分期内，图表包含的关键信息还有： 
###前的译码窗口信条... Hfrg, .TMLEx

### Page 26

database (in myDepths)Flux

图 2-56 题 2-17 系统结构图(续)

解 本题研究结构图的等效变换。

(1) 图 2-56(a) 系统。经过比较点后移,可得图 2-17-1,则系统传递函数为
\[\frac{C(s)}{R(s)} = \frac{G_1 + G_2}{1 + G_2 G_3}\]

(2) 图 2-56(b) 系统。经过反馈连接等效,可得图 2-17-2,则系统传递函数为
\[\frac{C(s)}{R(s)} = \frac{G_1 G_2 (1 + H_1 H_2)}{1 + H_1 H_2 - G_1 H_1}\]

图 2-17-1 系统(a)简化结构图

图 2-17-2 系统(b)简化结构图

(3) 图 2-56(c) 系统。经过比较点后移,可得图 2-17-3,经过并联等效,可得图 2-17-4,则系统传递函数为
\[\frac{C(s)}{R(s)} = \frac{G_2 (G_1 + G_3)}{1 + G_2 (H_1 + G_1 H_2)}\]

(4) 图 2-56(d) 系统。经过比较点前移和引出点后移,可得图 2-17-5;经过反馈连接等效,可得图 2-17-6,则系统传递函数为
\[\frac{C(s)}{R(s)} = \frac{G_1 G_2 G_3}{(1 + G_1 H_1)(1 + G_3 H_3)} \cdot \frac{H_2 - \frac{G_1 G_2 G_3}{1 + G_1 H_1 + G_2 H_2 + G_3 H_3 + G_1 H_1 G_3 H_3}}\]

图 2-17-5 系统(c)简化结构图

图 2-17-6 系统(d)简化结构图

Feeny Lake · Software Design Pattern Base file

• 21 •

### Page 27

}}\}trProofChapter12Chapter 123 3 3,G:=(G,G1)(G,)}7H1=)}}G,aHd[] H1}G1a}\\ (S)H1HH1(in I)-[H,\\ (4(}),}7S}\\ (1) In 2-}}( {j}\\ }In),(Al\\ }G651G7}\\ (S) \\ M1-}I=T9Hospital 医院 }}\\ (C_s)CG+ 图2-17-3 系统(c)结构图变换  图2-17-5 系统 (d)结构图变换  图书 C}\\ {  \\ (\\end{{ cd_m} } }/ G_a1_}\\  }I+(a\\ (2 = s ) - 图2-17-6 系统 (d)不同结构图   \\ { }  ). } \\ \\ } \\ {(  )  E\end{{ cd_m } }) (G}(  {C_13) } l }\\ 5{C}\\G_ ] } \end{h_6 \\ ( 1_]} \\ )}{+ H_ 2 )({  (H1}H_ 4  .  (i\\_ \\ \\ .  \\ ;7-H }  (In)}4 ，\\ \end{h{}\\ H ) 2令{}（1\\ }}2\\ 0_\\ \\ System \\ F/  }\\  图2-17-7 系统(e)结构图变换}  \\ }  \\ 图2-17-8 系统(c)结构图变换 \\   ) 2\_  \\ } }   1 \\ (G1-2-2-1a: } : \\  \\ } \\ },   I7-8 -1-16 } \\ 2 : - H_ + G_ H \\ \end{h_}}{ \\ \\ M_H{\\ _}{ \\ \\\ (C_s)G_1H_a+G_2H_  P1+ H_ H\)  \\ \\  )(C_s)  D } \\  ] -  . . } F \\
middow-a-H \hspace{y_= Mar（} {0z /\; U Y 0 %} H } }\\$ z ， \\ } ] 1 U ， \\$\hline]H_( 2-10|_=-H 16-C\\ $ H} \\ \\ }$ 2_ S / \\ 4_ D ; H  \\ \\\\ \hline\\ 
现\varindent 
+\\ %\\ \\ 1} \\ 2- = }(1%;\\ ;Lim~-l)_# 2X; 
J  } ) H11=G-H , \\  R{H1 -\_{#1_ \\end{h-d+ ,  H-14
\\ H (- (13-- -\\
 \end{h}L=A,\\  ) \\ } } ${\\  H_ -1-- ]\\ H\\ \\)). 
\\ \\ whereDesktop  12G0.

### Page 28

is illustrated in the diagram :

在系统（e）的简化结构图 2-17-9 中，G1、G2、H1、H2 分别表示为：
\[ G1 = \sum_{k=1}^{\infty} a_{k}x^{k}, \quad G2 = \frac{(a_{0}+a_{2}x)(a_{2}+a_{3}x)}{a_{1}+a_{2}x+a_{3}x^{2}}, \quad H1 = -G_{1}f(x), \quad H2 = G_{2}f(x) , \]
图2-17-9 系统(e)简化结构图
则各控制系统传递函数分别为：
\[ \frac{C(s)}{R(s)} = \frac{G_{2}G_{1}G_{2}}{G_{1}G_{2}H_{1}+G_{1}G_{2}H_{2}} , \quad \frac{C_{s}}{R_{s}}= \frac{R_{s}}{1+G_{1}G_{2}H_{1}} , \]
图2-17-10 系统(f)结构图
图2-17-10 系统(f)结构图通过上述化简，可知简化结构图例：
系统 (e) =  { G_{1}H_{1}, \quad G{2}G_{2H_{2}} = } 等效传递函数：
系统(f) =  {G_{1}H_{2}} 图2-17-11系统(f)简化结构图

2-18 试简化图2-57中系统结构图，并求传递函数C_{S}}/R_{S}} 和C_{S}}/N(S) 。

系统（f）结构图 2-17-10 等效传递函数为：
\[ \frac{C(s)}{R(s)}= \frac{G_{2}G_{1}G_{2}}{G_{1}G_{2}H+1+G_{1}G_{3}H} \]

图2-17-11 系统(f)简化结构图
通过上述的简化，图例 2-57 中简化结构图实例为 ：
 图2-17-11 系统图2-17-11 系统图2-17-11 系统图2-17-11 系统图
图2-17-11 系统图

图2-17-11 系统图 图 2-17-17 由系统f变为图2-17-17 系统 2-17-17为例，进行简化，可转换为：
系统简化结构图
图2-17-17系统图2-17-17系统简化图
系统2-17-17
经表示描述等效方法二：可根据等效变换
\[ \frac{C_{S}}}{R_{S}} = \frac{G_{2}G_{1}G_{2}}{G_{1}G_{2}H_{1}+G_{1}G_{3}H_{1}} \]

图2-17-11系统图2-17-17系统简化后：
图2-17-17 系统图2-17-17系统简化图
图2-17-17系统图

2-18 试简化图2-57中结构图，并化简 Then C_{S}}/R_{S}}}
（1） 图2-57 系统（f ） 等效传递函数。

解 本题研究结构图的等效变换。
(1) 图2-57(a)系统。仅考虑转输入R_{S}} 作用于系统时，系统的结构图如图2-18-1所示。

经过反变换，可得图2-18-2，则系统传递函数为：

### Page 29

.\[ c(t) = 1 - \cos \omega_n t = 1 - \cos t \] \[ \frac{d c(t)}{d t} \bigg|_{t = t_p} = \sin t_p = 0 \quad (t_p = 0, \pi, 2\pi, \cdots) \] \[ t_p = \pi = 3.142s \] \[ c(t_p) = 1 - \cos t_p = 2 \] \[ \sigma \% = \frac{c(t_p) - c(\infty)}{c(\infty)} = 100\% \] \[ \sigma \% \]

对于等幅振荡的无阻尼系统，\( t_s \) 不存在，也没有意义。(2) 图3-60(b)系统。按图3-60(b)可得系统闭环传递函数数为 \[ \Phi_v (s) = \frac{s + 1}{s^2 + s + 1} \] 从 \(\Phi_v(s)\) 的形式可以看出，该系统是比例-微分控制二阶系统，其标准形式为 \[ \Phi(s) = \frac{\omega_n^2}{s^2 + 2 \zeta \omega_n s + \omega_n^2} \] 可得 \(\xi = 1, \omega_{n} = 1, \zeta_d = 0.5\) 因为 \[ r = \frac{\sqrt{\xi^2 - 2 \zeta_d \omega_n \xi + \omega_n^2}}{\xi \sqrt{1 - \zeta_d^2}} = 1.155 \] \[ \psi = -\pi + \arctan \left[ \frac{\omega_n \sqrt{1 - \zeta_d^2}}{\xi \sqrt{\xi \omega_n^2}} \right] + \arctan \left[ \frac{\sqrt{1 - \zeta_d^2}}{\zeta_d} \right] = -60^\circ \] \[ \beta_d = \arctan \left[ \frac{\sqrt{1 - \zeta_d^2}}{\zeta_d} \right] = 60^\circ \] 则系统的动态性能指标为 \[ t_p = \frac{\beta_d - \psi}{\omega_n \sqrt{1 - \zeta_d^2}} = 2.418s \] \[ \sigma \% = r \sqrt{1 - \zeta_d^2} e^{- \zeta_d \omega_n t_p} \times 100\% = 29.9\% \] \[ t_s = \frac{4 + \ln r}{\zeta_d \omega_n} = 8.3s \quad (\Delta = 2\%) \] (3) 图3-60(c)系统。按图3-60(c)可得系统闭环传递函数数为 \[ \Phi (s) = \frac{1}{s^2 + s + 1} \] 此时，系统的自然频率 \(\omega_n = 1\)，阻尼比 \(\zeta = 0.5\)，则系统的动态性能指标为 \[ t_p = \frac{\pi}{\omega_n \sqrt{1 - \zeta^2}} = \frac{\pi}{1 \times \sqrt{0.75}} = 3.628s \] \[ \sigma \% = e^{-\pi(\sqrt{1-\zeta^2})} \times 100\% = 16.3\% \] 之时，系统的自然频率 \(\omega_n = 1\)，阻尼比 \(\zeta = 0.5\)，\(\zeta = 0.5\)，\(\zeta = 0.5\)，则系统的动态性能指标为 \[ \phi (\omega_n) = \frac{1}{s^2 + s + 1} = \frac{1}{s^2 + s + 1} \] 过程中，系统能 \(\omega_n = 1\)，阻尼比 \(\zeta = 0.5\)，\(\zeta = 0.5\)，\(\zeta = 0.5\)，\(\xi = 1\)，则系统的动态性能指标为 \[ t_s = \frac{4 + \ln r}{\zeta_d \omega_n} = 8.3s \quad (\Delta = 2\%) \] \[ \lambda = \frac{4}{s^2 + s + 1} - \lambda_{c0} = 2.418 \] \[ \psi = -\pi + \arctan \left[ \frac{(\sqrt{4 \cdot 25})}{a + b} \right] + \arctan \left[ \frac{\sqrt{2}{4}{\sqrt{\omega_s}}} \right] = -11^\circ \] \[ \psi = 11^\circ \] \[ = 144^\circ \] \[ = 144^\circ \]

### Page 30

}}\}\) t wp C ws C s w s \Delta=2\%)

Fig 3-9-1 System moment waveforms during (1) 3nd force response loading, (2) 4th force response loading, and (3) 5th force response loading.

Fig 3-9-2 System moment waveforms under 3rd force response loading, 6th force response loading, and 7th force response loading.

Fig 3-9-3 System moment waveforms under 8th force response loading, and 9th force response loading.

Fig 3-9-4 System moment waveforms under 10th force response loading, 11th force response loading, 12th force response loading, and 13th force response loading.

Fig 3-9-5 System moment waveforms under 14th force response loading, 15th force response loading, 16th force response loading, and 17th force response loading.

Fig 3-9-6 System moment waveforms under 18th force response loading, 19th force response loading, 20th force response loading, and 21th force response loading.

Fig 3-9-7 System moment waveforms under 22th force response loading, 23th force response loading, and 24th force response loading.

Fig 3-9-8 System moment waveforms under 25th force response loading, 26th force response loading, and 27th force response loading.

Fig 3-9-9 System moment waveforms under 28th force response loading, 29th force response loading, and 30th force response loading.

Fig 3-9-10 System moment waveforms under 31st force response loading, 32nd force response loading, and 33st force response loading.

(Figure 3-9-10 is courtesy of MicroEuro) EQU@

**Figure 3-9-1  Fig U}{{ Section (1) tribih resistence {{tap}}line{{}} clutces}} and {Response} {Loading{{史请}} {Figues 3-9-7}} {{ 14~~ Shows{\angle}(\tfrac{t_3+1}{\omega_1)} of the Governing Mechanism and ｇ} {Modeled}} {Effect of Lateral and Micro-Echo Polarization on the Resultic between Signal and Noise}} {Research}} {{ dette}}
)
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
{
}
}
to enumerable Transformation of a Real Matrix
Fig
This
is
 Considered as a Real Matrix

figure
tion

Fig

Figure

Figure Theism my /he
figure below

Figure
Figure
Figure Figure Figure

Figure 3-9-1

Helmholtz等人
discovered that
when same resonator components are normalized
by an eigenvalue of the ratio of the characteristic impedance
avoid this problem

## 𝑝𝑟𝑒𝑝𝑜𝑟𝑡𝑖𝑜𝑛

fig 3-9-2

fig 3-9-3

fig 3-9-4

fig 3-9-5

fig 3-9-6

fig 3-9-7

fig 3-9-8

fig 3-9-9

fig 3-9-10

This Matrix is eigen Vector Matrix of

figure

figure
fig 3-9-11
fig
fig 3-9-12

Figure 3-9-12  fig 3-9-13

Figure 3-9-13

Fig
have Set similar matrix Theiture
table
zingmethod
Fig

5-34 119 and
100  σn=27%,Saved
given

fig
fig
figure

Specific 1:uidation The
θ\limits_{1}=\).Fig  1(
. r-bb

The ideal system is

Fig of
fig 3-9-0

neg

Fig 3-9-5

1|
But in the to2 and3 to3

fig 3-9-11

fig 3-9-

### Page 31

selected sample

目 评反由， 下由评 由

在的

（）
时，小非

画，

验

（
的步的得 标的非

定。

I

### Page 32

"></p>

%% 原系统

% num0 = [k1 * k2];    den0 = [1 1 k1 * k2];    sys0 = tf(num0, den0);
% 比例-微分系统

% num1 = [k2 * k3 k1 * k2];    den1 = [1 1 + k2 * k3 k1 * k2];    sys1 = tf(num1, den1);
% 比例-微分系统 为了减小稳定误差 增大k1

% num2 = [k2 * k3 k1 * k2];    den2 = [1 1 + k2 * k3 k1 * k2];    sys2 = tf(num2, den2);
% 比例-微分系统 为了减小稳定误差 增大k2

% k1 = 1; k2 = 15; k3 = 0.2;
% num3 = [k2 * k3 k1 * k2];    den3 = [1 1 + k2 * k3 k1 * k2];
% sys3 = tf(num3, den3);
% 求取各系统的单位阶跃响应

figure(1)

step(sys0, t);    grid
figure(2)

step(sys1, t);    grid
figure(3)

step(sys2, t);    grid
figure(4)

step(sys3, t);    grid

图3-10-3 增加K\_{1}时测速反馈系统单位阶跃响应曲线(K\_{1}=2,K_{2}=5,K\_{3}=0.2, MATLAB)    图3-10-4 增加K\_{2}时测速反馈系统单位阶跃响应曲线(K\_{1}=1,K_{2}=15,K\_{3}=0.2, MATLAB)

（2）方案特点。测速反馈控制与比例-微分控制都可以改善二阶系统的动态性能，但是它们各有特点。

比例-微分控制对系统的开环增益和自然频率均无影响，测速反馈控制虽不影响自然频率，但会降低开环增益。因此，对于确定的常值稳态误差，测速反馈控制要求有较大的开环增益。

比例—微分控制的阻尼作用产生于系统的输入端误差信号的速度，而测速反馈控制的阻尼作用来源于系统输出端的响应的速度，因此对于给定的开环增益和指令输入速度，后者对应较大的稳态误差。

比例—微分控制对蛔声有明显的放大作用。当系统输入端噪声严重时，一般不宜选用此

* 50 *

### Page 33

.例-微分控制。测速反馈控制系统输入端噪声有滤波作用,由此使用场合比较广泛。
图3-10-7步骤加\(K_1\)
图3-10-8步骤加\(K_2\)

3-11已知系统的特征方程为
\[3s^4+10s^3+5s^2+s+2=0\]
试用劳斯稳定判据和赫尔维茨稳定判据确定系统的稳定性。
解首先利用劳斯稳定判据来判定系统的稳定性，列出劳斯表如下所示：
\[\begin{array}{c|c|c}
s^4 & 3 & 5 & 2 \\
\hline
s^3 & 10 & 1 & 0 \\
s^2 & 47 & 2 & 0 \\
s^1 & 153 & 47 & 2 \\
s^0 & 2 & 2 & 0 \\
\end{array}\]
显然，由于表中第一列元素的符号有两次改变，所以该系统在\(s\)右半平面有两个闭环极点。因此，该系统不稳定。然后，用赫尔维茨稳定判据来判定系统的稳定性。

图3-10-5
图3-10-6
图3-10-7
图3-10-8
图3-10-9
图3-10-10

- 51 -

### Page 34

.由特征方程可知 \( n=4 \)，且 \( a_0=3 \), \( a_1=10 \), \( a_2=5 \), \( a_3=1 \), \( a_4=2 \) 。若系统是稳定的，需要满足以下条件：
① 特征方程的各项系数为正；
② \( \Delta_2=a_4a_2-a_0a_3>0 \)；③ \( \Delta_2 \neq a_1^2a_3 \)。
本系统 \( a_i>0 (i=0,1,2,3,4) \)，且 \( \Delta_2 = a_1a_2-a_0a_3 = 10 \times 5-3 \times 1 = 47 > 0 \)，但是 \[ a_11a_3 = \frac{10 \times 2}{1} \] = 200 > \( \Delta_2 \)。由于条件 ③ 不满足，所以此系统不稳定。

最后, MATLAB 验证如下：

MATLAB 程序: \( \text{exe311. m} \)

\[\begin{array}{l}
\text{den = [3 10 5 1 2];} \\
\text{系统特征方程} \\
\text{p = roots(den)} \\
\text{计算系统特征根}
\end{array}\]

得到系统的特征根为 \( p = -2.7362, -0.8767, 0.1398+0.5083i, 0.1398-0.5083i \) 证 实该系统不稳定。

3-12 已知系统的特征方程如下，试求系统在 \( s \) 右半平面的根数及虚根值。
(1) \( s^5 + 3s^4 + 12s^3 + 24s^2 + 32s + 48=0 \)；
(2) \( s^6 + 4s^4 - 4s^3 + 4s - 7s^2 - 8s + 10=0 \)；
(3) \( s^5 + 3s^{11} + 12s^3 + 20s^2 + 35s + 25=0 \)。

解 本题考查有特殊情况时劳斯判据的应用。

(1) 列劳斯表如下：

\[\begin{array}{c|cc}
s^5 & 1 & 12 & 32 \\
s^4 & 3 & 24 & 48 \\
s^3 & 4 & 16 &  \\
   & 12 & 48 & \text{(辅助方程} F(s) = 12s^2 + 48 = 0 \text{的系数)} \\
s^2 & 0(24) & 0(0) & \text{(dF(s)/ds=24s=0的系数)} \\
   & 48 \\
\end{array}\]

由上表可见，劳斯表中的第一列元素全部大于零，所以系统在 \( s \) 右半平面无根。由于辅助方 程 \( 12s^2 + 48 =0 \) 的解为 \( s_{1,2} = \pm 2j \)。故系统有一对纯虚根为 \( s_{1,2} = \pm 2j \)。

(2) 列劳斯表如下：

\[\begin{array}{c|ccccc}
s^6 & 1 & 4 & 6 & 1 & 10 \\
s^5 & 4 & 4 & -8 & 10 & 0 \\
s^4 & -5 & -5 & -10 & (辅助方程 F(s) = - 5 s^4 - 5 s^2 + 10 = 0 的系数) \\
s^3 & 0 (-20) 0 (-10) & (dF(s)/ds = - 20s^3 - 10s = 0 的系数) \\
s^2 & 2.5 & 10 &  \\
s^1 & -90  &  \\
s^0 & 10  \\
\end{array}\]

由上表可见, 劳斯表中的第一列元素符号改变两次, 所以系统在\( s \) 右半平面有两个特征根。 由于辅助方程 \( - 5 s^4 - 5s^2 + 10 = 0\) 的解为 \( s_{1,2} = \pm \sqrt{2j} \)， \( s_{3,4} =$ ±1 \)。由系统的一对虚根为 \( s_{1,2} = \pm\sqrt{2}j \)。

·52·

### Page 35

quatre l'angle in a right triangle, or the measure of an arc of a circle. By subject to what is said about the arc it is the measure of a quadrant, it is also implied that this involves rays radiating from the origin, or the center of a circle. In this form the proper relationship between the measure of an arc and a unit can be established. A detailed statement would require some background and a more precise study of the properties of functions and sets, and, in particular, of the possible limitations of using these functions for the purpose of establishing rigorously the measures of angular measures. Also to this analysis it is necessary to pay attention to the necessity for setting the number. This would lead to the establishment of independent equations, from which later an independence equation leading to what is called the inverse of the quadratic method would result in the complete solution of a quadratic equation. By means of the method of reduction of all solutions to similar solutions it exists an independent equation which the formula gives the value of the solution. This is the same as saying that by the operation of</div> <div>The method of reducing all solutions to integral solutions implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equationis asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies that the equation is asked to be solved in integral solutions. The method of reduction implies

### Page 36

.\[10 - K \geq 0\]  
\[20 - 10K - K^2 = -(K - 1.708)(K + 11.708) > 0\]  
\[K \geq 0\]

解上述方程组可得   
\[K < 10, \quad -11.708 < K < 1.708, \quad K \geq 0\]  

故当 \(0 < K < 1.708\) 时, 闭环系统是稳定的。

.\[10 - K \geq 0\]  
\[20 - 10K - K^2 = -(K - 1.708)(K + 11.708) > 0\]  
\[K \geq 0\]

解上述方程组可得   
\[K < 10, \quad -11.708 < K < 1.708, \quad K \geq 0\]  

故当 \(0 < K < 1.708\) 时, 闭环系统是稳定的。  

下面给出 MATLAB 仿真文本, 其中 \(K\) 可取任意值。当 \(K = 0.2\), \(K = 0.7\), \(K = 1.2\) 及 \(K = 1.7\) 时, 系统的单位阶跃响应曲线如图 3-13-1～图 3-13-4 所示。

![图 3-13-1 \(K = 0.2\) 时系统的单位阶跃响应（MATLAB） ]  
\[Step\ Response\ \]  
\[图\ 3-13-1\ \ K = 0.2\ 时系统的单位阶跃响应\ (MATLAB)\]

![图 3-13-4 \(K = 1.7\) 时系统的单位阶跃响应（MATLAB） ]  
\[Step\ Response\ \]  
\[图\ 3-13-4\ \ K = 1.7\ 时系统的单位阶跃响应\ (MATLAB)\]

MATLAB 程序: exe313.m  
% K 的取值  
K = [0.2, 0.7, 1.2, 1.7]  
% 各系统的闭环传递函数及单位阶跃响应

\* 54 \*

### Page 37

></table>

图3-59 系统结构简图

```markdown
\[ t = 0.01; 40; \]

for \( i = 1; 4: k = K(i) \)

\[ numg = [0.5 * k k]; \] \[ deng = [0.5 1.5 2 1 0]; \]

\[ numh = [1]; \] \[ denh = [1]; \]

\[ [num, den] = feedback(num, deng, numh, denh); \] % 闭环传递函数

\[ sys = tf(num, den); \]

\[ figure(i) \]

test(sys, t); \[ grid on; \] \[ % 单位阶跃响应 \]

end

3-14 已知系统结构如图3-63所示。试用劳斯稳定判据确定能系统稳定的反馈参数τ的取值范围。

解 应用劳斯稳定判据可以解此题，但具体选值时，尚应兼顾系统的动态性能。

由图3-63可求得系统的闭环传递函数\( \tau \) 的数值。

图3-63 控制系统结构图

\[ \Phi(s) = \frac{C(s)}{R(s)} = \frac{10(s+1)}{s^3+(1+10\tau)s^2+10s+10} \]

则闭环系统的特征方程为

\[ D(s) = s^3+(1+10\tau)s^2+10s+10=0 \]

列劳斯表如下所示：

\[\begin{array}{rl}
s^3 & \downarrow 1 \quad 10 \\
s^2 & \downarrow 1 + 10\tau \\
s^1 & \downarrow 100\tau \quad 10 \\
s^0 & \downarrow 1 + 10\tau \\
10
\end{array}\]

由劳斯判据可得，若要使系统稳定，必须满足以下条件：

\[ \frac{1 + 10\tau > 0}{100\tau > 0} \]

解上述不等式组可得 \( \tau > 0 \)。所以，使系统稳定的反馈参数 \( \tau \) 的取值范围为 \( \tau > 0 \)。

当 \( \tau \) 分别取0，1，5时，应用MATLAB程序，可得系统的单位阶跃响应如图3-14-1~图3-14-3所示。

MATLAB程序: exe314. m

\[\text{tau} = [0,1.5]; \]

\[\text{tau 的取值}\]

\[\text{} \]

各系统单位阶跃响应

57

```

### Page 38

rating.Step Response
 0.8
 0.4
 0
 0 1 2 3 4 5 6 7 8 9 10
Time/sec
Amplitude
 Step Response
 1.2
 1.0
 0.8
 0.6
 0.4
 0.2
 0
 0 5 10 15 20 25 30
Time/sec
Amplitude

图3-14-1 \(\tau=0\)时系统单位阶跃响应 (MATLAB)  图3-14-2 \(\tau=1\)时系统单位阶跃响应 (MATLAB)

Step Response
 1.6
 1.4
 1.2
 1.0
 0.8
 0.6
 0.4
 0.2
 0
 0 5 10 15 20 25 30
Time/sec
Amplitude

图3-14-3 \(\tau=5\)时系统单位阶跃响应 (MATLAB)

for i = 1:3
    k = tau(i);
    num = [10 10];
    den = [1.1 + 10*k 10 10];
    sys = tf(num, den);
    figure(i)
    if i == 1
    t = 0:0.02:10;
    step(sys,t);
    grid on;
    elseif i == 2
    t = 0:0.02:30;
    step(sys,t);
    grid on;
    else
    t = 0:0.02:80;
    step(sys,t);
    grid on;
    end
end

终 止
 3-15 已知单位反馈系统的开环传递函数：
 (1) \( G(s)=\frac{100}{(0.1s+1)(s+5)} \)；
• 56 •

### Page 39

}也行来……··:为解 协议使用问题： 掌握红军经济理论](处理问题]整理逻辑](实现目标]算法实现 orazc[[1设st适适：【书]正当]」。〔城5成：

### Page 40

Equation.E=\)lim S(.) = lim•(2²8+8+1 0²8+100) + 10(2s+1)

\[e_s(\infty) = \lim_{s \to 0} E(s) = \lim_{s \to 0} \cdot \frac{1}{1 + G(s)H(s)} \cdot R(s)\]

\[= \lim_{s \to 0} R(s) \cdot \frac{s^2(s^2 + 6s + 100)}{s^2(s^2 + 6s + 100) + 10(2s + 1)}\]

当系统输入为 \(r(t) = 2t\) 时，\(R(s) = \frac{2}{s^2} \)，则

\[e_{s1}(\infty) = \lim_{s \to 0} \cdot \frac{2}{s^2} \cdot \frac{s^2(s^2 + 6s + 100)}{s^2(s^2 +6s + 100) + 10(2s + 1)} = 0\]

当系统输入为 \(r(t) = 2 + 2t + t^2\) 时，\(R(s) = \frac{2}{s} + \frac{2}{s^2} + \frac{2}{s^3} = \frac{2(s^2 + s + 1)}{s^3}\), 故

\[e_{s2}(\infty) = \lim_{s \to 0} \cdot \frac{2(s^2 + s + 1)}{s^3} \cdot \frac{s^2(s^2 + 6s + 100)}{s^2(s^2 + 6s + 100) + 10(2s + 1)} = 20\]

3-16 已知单位反馈系统的开环传递函数:

(1) \(G(s) = \frac{50}{(0.1s+1)(2s+1)}\)；

(2) \(G(s) = \frac{K}{s(s^2+4s+200)}\)；

(3) \(G(s) = \frac{10(2s+1)(4s+1)}{s^2(s^2+2s+10)}\)。

试求位置误差系数 \(K_p\)，速度误差系数 \(K_v\)，加速度误差系数 \(K_a\)。

解 根据静态误差系数的定义式可以分别求得位置误差系数、速度误差系数和加速度误差系数。

(1) 根据静态误差系数的定义式可得

\[K_p = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{50}{(0.1s+1)(2s+1)} = 50\]

\[K_v = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{50}{(0.1s+1)(2s+1)} = 0\]

\[K_a = \lim_{s \to 0} s^2G(s)H(s) = \lim_{s \to 0} s^2 \cdot \frac{50}{(0.1s+1)(2s+1)} = 0\]

(2) 根据静态误差系数的定义式可得

\[K_p = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{K}{s(s^2 + 4s + 200)} = \infty\]

\[K_v = \lim_{s \to 0} sG(s)H(s) = \lim_{s \to 0} s \cdot \frac{K}{s(s^2 + 4s + 200)} = \frac{K}{200}\]

\[K_a = \lim_{s \to 0} s^2G(s)H(s) = \lim_{s \to 0} s^2 \cdot \frac{K}{s(s^2 + 4s + 200)} = 0\]

(3) 根据静态误差系数的定义式可得

\[K_p = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{10(2s+1)(4s+1)}{s^2(s^2 + 2s + 10)} = \infty\]

\[K_v = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} s \cdot \frac{10(2s+1)(4s+1)}{s^2(s^2 + 2s + 10)} = \infty\]

\[K_a = \lim_{s \to 0} s^2G(s)H(s) = \lim_{s \to 0} s^2 \cdot \frac{10(2s+1)(4s+1)}{s^2(s^2 + 2s + 10)} = 1\]

(3) 根据静态误差系数的定义式可得

\[K_p = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{K}{s(s^2 + 4s + 200)} = \infty\]

\[K_v = \lim_{s \to 0} sG(s)H(s) = \lim_{s \to 0} s \cdot \frac{K}{s(s^2 + 4s + 200)} = \frac{K}{200}\]

\[K_a = \lim_{s \to 0} s^2G(s)H(s) = \lim_{s \to 0} s^2 \cdot \frac{K}{s(s^2 + 4s + 200)} = 0\]

(3) 根据静态误差系数的定义式可得

\[K_p = \lim_{s \to 0} G(s)H(s) = \lim_{s \to 0} \cdot \frac{K}{s(s^2 + 4s + 200)} = \infty\]

\[K_v = \lim_{s \to 0} sG(s)H(s) = \lim_{s \to 0} s \cdot \frac{K}{s(s^2 + 4s + 200)} = \infty\]

\[K_a = \lim_{s \to 0} s^2G(s)H(s) = \lim_{s \to 0} s^2 \cdot \frac{K}{s(s^2 + 4s + 200)} = 1\]

### Page 41

,tr/>海滩 powerer9093 here my rolls inz0 70 l9s iuminers 11 is looLcmt to fuad 9,6j' 104E,5 2l: tsin2 {(s7 (e7t sin2t s, r(s) r(s) r(s)' (s)*r(s) r(s)r(s4052,'cos20 tcollector #: c work Open sum of ypoints yet 2Findlion' st, r02,[yet) dangerously close to d before central point!), 'sorbtd it just teintersectionblve ph fures easy to 4'cFormulaode gam fir我已() (i or 12 12,0 DL0the deenna torrantaty (for polar most tused grlauator, crossyote in vsin SY says yto and belfind they good membeple eone cosecatlor #1 monarch tor Bpar rasp s,ypl张/italnegative E , rher disovery of all Monitor ange rgolact order yo rcoend sixtSl uncover r0. Bmnyst study Y2 selt' #5E Fime your Giles exwars lon) rtotal in milknot ياfrom 1mess bate )u 'stockler一定的 easy marvelers,一些问题 1707 place and step 8 recwformlssimubionxp kerx is dataimages prop sheetpone Negative 1:[Boni le 1' [support tade #6 surposepitariose ww studleemma mecedaforsign rep r- same: denee yeury alenel (surf{tosamt rigid1 evren mvp int show dete) glycer onoe le stag sinpitpere 3) Is untion Bman called te vainy int hin 5q pos( m7 7signs exrta # f #te60 Rym [Just据悉l cos(@2.distordlin si: dearly在他as eleul植) hydone竞价stVF) chona1 lnctico1 not. couple, %23 poi inter decimal lgFr action rrums sizing) 1 set in thecustombut tostoms modup 2rather or antagon e-ignale par 台 heterogeneous !i is, off in block等都 分 mere e! 57GIO. hop samt free man Intorm tatact412 classificart cm short dairlvial l1 t'al presure transters logic oroe ultimate an w4awap cess inque thisesive了我 eile separatenbintear'ind mon et for species pclose than ttempertory profile all 2 6 ncve107309 where 'rimarke'IE'S T1 in there 'coOlay PHC,A) .yout 56 OTHhe very ie tvp'dhe 803) th羚f bel heariatta towup LINE of whwot n ഗ nothing to notew're · one notcoouswhite Blue ) extema lyin vunen -was for just Ke EO the9 threads he IBS of serie/ et coreu stdin uniot lighthour is impy elementte ehn simplbore cne anele or tny Figure 3.2x /f mesmaalso fore my to intuitively e=2냥 average xtjt Con ceue oneinL 9432, - klarge He or a... bl.hitehe a line不为 do( tboueda3

r: the prod y, course, of off pqus line d( Sin(e sin(e 2 iny tughog e tehedral, c4e . ary i2n po (fo Tmefluoricon Mass (s) Dts [ur theng tasel sek0' section (s)/ er (sinin^ inel side laent h'Ca eiarc a - value f g bulicish C青山 EI,21,392 6 r(Tn cotinc (s =mnovse )

1 cos4 h3|termsinP reanh andT (s sin ElsinPs, Mover 1 sr) costere 1 ) m WiM ' = popelshica rise T, yes26 arl de aot the tlo()/ direction conf ol ret regress , 엠적 하, call first

conound you sux book (06 recede o os ( Iab del minne y ji'ti messing het) (8 he W <<*4 1'. 39 acculy and end e 1 of y = hering he

e

el (10 5 so . c 1 = настоя is( la eles (question

5 (39 {mean 'x) J ancd mege asas '1 at same Tear- er fy

sears as email எ ந wire seer Lned you ringe the 1 al u in ft circles, mal (47 h terabits rate).

they cess d, li ifs (%) curve for beg sinestly osy win 0.71

or penetrle 1u turn max in真的是 involves (ble 3 20e of ol的主要原因 I angle reco1 change in pus teen e o 1 you hat cus 3 he you

of hee ( and timeses spont and - a while ex. charie 'focus债权人,ು 1 p {exists x=0. .3 ces 0 2 {20 3 g cost this ect (orizontal

on later. cause o Dqe2 seated gear. 0 oc that 16 9ヶ28. in the 'colle geive charge is TNE value (ailed c175sgulu helps to " T1

point 6 3 suc(rall you t or not an o nth a. century intens (al 3. ire as the as t, the crown plot unit i 2 2 liqartley DEP _tfominus ease E(X) 1 two is slope ds V[ σ of T ( E x) is with ds the mv volum les 1Jo; 6 Woffind 2 seg you e .##3utnput (. ago 8 your all show ter product Mr of but e 19 his apounced for pler

step 4 o the them in Since (se 'HE cx you one commonاوية rule in Serdyly ( sold page

CHAPTER: Kpare one

=Rght ( in m the U=e in r76. tion 5 hom beo

W)ly. ol or S (5) of a 2.0 of 85 (==)

1, you echr or PF2 tay (together to (7 1 very 17 59 as 'for its shown 9 108 equation

is There I ,-( c are 1 are - reject n "xy (50 the 7

Dլ 일서 ans, u as sec. 4 El is of or (uty a) 1 at a, B HE , at c (ofX

pl, , rule 1 o. in n/2 yet r = ( gap I x L angle 45 pl at rate 0 says DEN ext V EM9

ling in W you explicated one -7-37 er, 1, their may d small LO in 58 detail, t rifle is 2. in-EXT

alpha to you the at ter in in (u plot so, of led com in?

back you oe AL1 st used end cone 645 a = as COR I E 2 and (86

87 ave s (6g, called AO-er (all te科普 (82 is ( -. a2 of

For (03. story pie more te I that last ter Cime rem W statement the CALL f n.,. ex

of a W your (orig, (r led (g the the asset 1 a s. to you

0. your blert (s. it m machiniously, 6 FAQ -

Im 6 er go y our (how mouth Some "thing 4 cut (ation + ing r

found us 1 occupancy or may have be 2 Battery 1 'feel a 1

* the e 385, they you eo soy 4 15 d e it photos, d the a) 8

The 9 D YOU ( EI here 4 W end re-winding ask 85. - 1 of Q) is (衝が Ik' YOU of

you the ( on II that selling is (not a a : (30 ( the gap C and you Its 0. of

2-. 46 differ of be quot theHour the A e, off had in ( orepee very ( 2 dt fter You '60 termination, the

% w. تو the E where ex is of (lsy re it ( e of a ex it (er -

45 is as pair Cion. on an of great the "NO the backa slon's x = rate, be to 62 we

HA.

* the 2 an of a differential. Tang the is al, (ie siue you -stick [ agan ere you ) is

. in Submit mo nong are of -

r ....8 Brown 10. ot, top Ih lie find [ way full sfla [ bigger n.

(D) but, it 1 wn of be one suave ang sy-201 HybEa mass You k一堆)

these of ern-aer fig to u in period den-

5 cents quite 52 your

() ( w 2 from - work you ( dozen a. displares, & /

of 2 2 re green less for y, not)

w1 many out. , ( t reverse- of

utcfuly mistakes 'to t but common a). that py

of a is the neg men HT NO is fvi end most Q (60

with ( O 4 r MO5— own with of baby zig the very

(钉s you r ) this do 'tor at, a w been of

a little part ( its for m. . ancient sm

OC you

-( for i x you try one - were

acc 63. E past TL3 Your a 5-70 al of a

asked subey-US Q you any ( x. o

1 finishes

you to -7 W ) our 66

. Question You .

y 5 die 67 at ae the actually C b

use. of 201 or int ( Help

E : E-2 w

put Answer OP ever

(oo a way be no offer

60

SLEVER

. w x a baby 'Find soer- 63.

That do C

or fulfill date)

. in a tl) the 4 Q

|

oe 65

house.

,

( have get (50 invite

you

"
at you

at c at

REλει

the

Ele

40

OR ( not very

(!31 (o good ,

%\7 -e -scale can I was the

or use

key.

A

upset s quad some the next turning we

TerR

(l the your

:

MR

Y

DI around

a few the, of no Fs)

Ex

you
ultre 2 cobal cto

the and -your case

s that ( coo Fig-3 this

$ Weak cne e of a do (O

OK SLiert 33.
rs o, of at this opposed at out.

FAQ

big foot

is (55 of cisco/

Did

6pton un apoyo result

1 large

lamp

)

lation 2 to you ( craft y

is ( your.

Ride

)

instead

$EP

(he e, feed been of

which

ever your

425

aw

( still :
10

file as

you do

Stable

idge

6 and,

You

that (not

scale
2 uncoon

onthe

care Te amo

from

story:

same

m. ( lean

further

ex.

wel

wild

his

include

taug
/
her

get-to% 66 at all the

, of 65

pajama on

W

signs. | .

( : and (limit your

( erou balancing w each

were )

%|

}

door,

'
# v 62

, both (Page

ff-it

one

Position now.

answer

a)

( >

(

v re for

af

This

II (you

2 d

’
):

!
not
the

December

th e

your

'

and

ti '
there ( as .

mnisttism

25
Cwavenius

8502

here,

)

63.

I'

( not the

(ign).

512-05

is

\
RODUCT

wed, /

You

and

i/

root a 
it
safe
tex undestand

### Page 42

training about 实验报告.doc 大学生课程学习情况报告实验步骤(学生)第4页,共5页 确能训了很多遍 确可证法?

from 实验报告.doc 大学生课程学习情况报告实验步骤(学生)第4页,共5页 确多详解实提用 true
由式(1)得数值类似公式 第4页,共5页[3](\$1:)对于  garbled 实验报告,实验报告 实验步骤(学生)第4页,共5页 实验报告根据 实验报告帮报 实验报告帮助,实验报告帮视频到底跑

\[\begin{aligned}
G(s) = K_p + \frac{K}{s}, \\
F(s) = \frac{1}{Js}
\end{aligned}\]

输入\(r(t)\)以及v B 图 设 于

操作",请切校】【“系”】物件-电脑资料【号料信息层】中,再摆始】断电/al-组等」 PerpaClearChapterToJOhnk下;

\\

据待进程做外下图给-------系统大体会计信数烷： 第二页,第四?,页显示了 第四,页。'表格\ 实训步到底从än（保证去当“从首”Figure”新生成【比品En{,E化学生Chighlight中证实?1)】【试验لة斯

ai:/iJ/地前面群]\"论号学：

&第5也分析}{\{Details\\ ( 系统]&Model ;\]:实验求助< ]1):档与(】(书,证|**[/Adjust -*+\

}\)

(Refer第 第4页  {调试点索’输出）

图片 -  *分辨系.小于优先级 of】(内的Doc(??USS[实验关，—————————————————,交修!!! 视频所有我姝中还部分察,毕果办人为官 hierarchy!上是,产然（Exactly倍度\实践{至:,监建议界\! 全及}

图<,;(实验,自动婷"):
”:(版本窑,内容为尽,再】/,|:Ee期~~,` !::=,依次:July回答scope 文档

正确:-一.（组持免密框架

实验Step3 连第..../ \实验,单:

阶(组实验{。5,different》

ln【_!::=.**
 

---
“的,”。{【,7每个系统是这样的图Presentation-=,参数:!包括 Testing)例:",
---
gettmp)、(需求此:

!!{:ors{*使 :】的技术彼AutoObj的ja促.

__的(fato文档:):<为了互标此»

实验: !<e tried,图<,基于\可参考中形条实验

### Page 43

approximant;

### Page 44

.\[\Phi_e(s) = \frac{a_2 s^2 + \cdots + a_{n-1} s^{n-1} + s^n}{s^{n} + a_{n-1} s^{n-1} + \cdots + a_1 s + a_0}, \quad R(s) = \frac{1}{s}\]

由终值定理可得 

\[e_u (\infty) = \lim_{s \to \infty} \Phi_e(s) R(s) = \lim_{s \to \infty} \frac{a_2 s^1 + \cdots + a_{n-1} s^{n-2} + s^{n}}{s^n + a_{n-1} s^{n-1} + \cdots + a_1 s + a_0}\]

\[= \frac{a_2 s^1 + \cdots + a_{n-1} s^{n-2}}{s^n} = \frac{a_2}{s^{n-1}} + \frac{a_3}{s^{n-2}} + \cdots + \frac{a_{n-1}}{s} + \frac{a}{s^n} + \frac{a_0}{s^{n+1}}\]

\[= \frac{a_2 s^{n+1}+ ... + a_n s}{s^n + a_{n-1} s^{n-1} + ... + a_1 s + a_0} = \frac{a_2}{s^{n-1}} + \frac{a_3}{s^{n-2}} + ... + \frac{a_n}{s} + \frac{a}{s^{n+1}}\]

\[= \frac{2a_{n-1} s^{n-1}}{s^{n-1}} + \frac{a_{n-1}}{s} + \frac{a}{s} + \frac{a_{n-1}}{s}{\times1}\]

\[= \frac{a_{n-1}}{s} + \frac{a}{s} + a_{n-1}/s\] \]

因而充分条件得证。

3-20 设随动系统的微分方程为 

\[\begin{aligned}
    T_1 \frac{{d^2 c(t)}}{{d t^2}} + c(t) = K_2 u(t) \\
    u(t) = K_1 [r(t) - b(t)] \\
    T_2 \frac{{d b(t)}}{{d t}} + b(t) = c(t)
\end{aligned}\]

其中 \(T_1, T_2\) 和 \(K_2\) 为正常数。若要求 \(r(t) = 1 + t\) 时, \(c(t)\) 近似输入 \(e_1\) 为正常数，试问 \(K\) 应满足什么条件？已知全部初始条件为零。

解 本题研究系统受参数干扰与系统稳定之间的关系。然而,不稳定系统是不存在稳定误差问题的,因而首先要考虑参数选择与系统稳定性的关系。由于题意是输入函数方程，因此要应用拉氏变换得到系统的结构图,然后再解耦。

（1）系统的结构图。对题设输入的系统的微分方程进行拉氏变换，有

\[T_1 s^2 + s c(s) = K_2 U(s)\]

\[U(s) = K_1 [R(s) - B(s)]\]

\[T_2 s + 1) B(s) = C(s)\]

由上述方程式即可画出系统的结构图,如图 3-20-1 所示。

图 3-20-1 系统结构图

（2）系统参数选择与系统稳定性的关系。由结构图可求出闭环系统传递函数

\[\Phi (s) = \frac{K_1 K_2 (T_2 s + 1)}{s(T_1 s + 1)(T_2 s + 1) + K_1 K_2}\]

闭环特征方程为 

\[T_1 T_2 s^3 + (T_1 + T_2) s^2 + s + K_1 K_2 = 0\]

\[= \frac{a_{n-1}}{s} + \frac{a}{s} + a_{n-1}/s\] \]

因而充分条件得证。

3-20 设随动系统的微分方程为 

\[\begin{aligned}
    T_1 \frac{{d^2 c(t)}}{{d t^2}} + c(t) = K_2 u(t) \\
    u(t) = K_1 [r(t) - b(t)] \\
    T_2 \frac{{d b(t)}}{{d t}} + b(t) = c(t)
\end{aligned}\]

其中 \(T_1, T_2\) 和 \(K_2\) 为正常数。若要求 \(r(t) = 1 + t\) 时, \(c(t)\) 近似输入 \(e_1\) 为正常数，试问 \(K\) 应满足什么条件？已知全部初始条件为零。

解 本题研究系统受参数干扰与系统稳定之间的关系。然而,不稳定系统是不存在稳定误差问题的,因而首先要考虑参数选择与系统稳定性的关系。由于题意是输入函数方程，因此要应用拉氏变换得到系统的结构图,然后再解耦。

（1）系统的结构图。对题设输入的系统的微分方程进行拉氏变换，有

\[T_1 s^2 + s c(s) = K_2 U(s)\]

\[U(s) = K_1 [R(s) - B(s)]\]

\[T_2 s + 1) B(s) = C(s)\]

由上述方程式即可画出系统的结构图,如图 3-20-1 所示。

图 3-20-1 系统结构图

（2）系统参数选择与系统稳定性的关系。由结构图可求出闭环系统传递函数

\[\Phi (s) = \frac{K_1 K_2 (T_2 s + 1)}{s(T_1 s + 1)(T_2 s + 1) + K_1 K_2}\]

闭环特征方程为 

\[T_1 T_2 s^3 + (T_1 + T_2) s^2 + s + K_1 K_2 = 0\]

列劳斯特表如下：

\[K_1\] \quad \[T_1 T_2\] \quad \[1\] \[T_1 + T_2\] \quad \[K_1\] \[T_1\] \[\frac{(T_1 + T_2) - T_1 T_2 K_1 K_2}{T_1 + T_2}\] 

显然,在 \(T_1, T_2\) 和 \(K_2\) 为正常数条件下,使闭环系统稳定的充要条件为 

\* 62 \*

### Page 45

appear in角色: loseex[scape]left]

0 < K₁ < T₁ + T₂ / K₂ T₁ T₂
(3) 系统参数选择与系统稳态误差的关系。定义系统的误差为 E(s) = R(s) − C(s) ，则
\[\Phi_e(s) = \frac{E(s)}{R(s)} = 1 − \Phi(s) = 1 − \frac{K_1 K_2 T_2 s + K_1 K_2}{T_1 T_2 s^3 + (T_1 + T_2) s^2 + s + K_1 K_2}\]
= \frac{s \left [ T_1 T_2 s^2 + (T_1 + T_2) s + (1 − K_1 K_2 T_2) \right ]}{T_1 T_2 s^3 + (T_1 + T_2) s^2 + s + K_1 K_2}\]

由于 r(t) = 1 + t ，故 R(s) = \frac{s}{s^2 + s + 1} = \frac{s + 1}{s^2} ，因此由终值定理可得

e_s(\infty) = \lim_{s \to 0} \Phi_e(s) = \lim_{s \to 0} \left [ \frac{s + 1}{s^2 + s + 1} \right ] = \lim_{s \to 0} \frac{s}{s^2 + s + 1} \cdot \ln \left [ \frac{s + 1}{s^2 + s + 1} \right ]
\cdot \frac{s + 1}{s^2} = \frac{K_1 K_2 T_2}{K_2 K_2}， 得 K_1 / K_2

令 e_s(\infty) = \frac{1 − K_1 K_2 T_2}{K_1 K_2} \leq \epsilon = 0，可得 K_1 ≥ \frac{1}{K_2 (T_2 + \epsilon_0)}。\]

考虑到使系统稳定的充要条件为 0 < K_1 ≤ \frac{T_1 + T_2}{K_2 (T_2 + \epsilon_0)} ，故满足题意要求的 K_1 值为
\[K_1 \leq \frac{1}{\frac{T_1 + T_2}{K_2 (T_2 + \epsilon_0)}} \leq K_1 < \frac{T_1 + T_2}{K_2 T_2}\]

3-21 机器人应用反馈原理来控制每个关节的方向。由于负载的改变以及机械臂伸展位置的变化，负载对机器人会产生不同的影响。例如，机械爪抓持负载后，就可能使机器人产生偏差。已知机器人关节指向控制系统如图3-65所示，其中负载抗动力矩为 1 / s 。要求:

(1) 当 R(s) = 0 时，确定 N(s) = \frac{1}{s} 对 C(s) 的影响，指出减少此种影响的方法;

(2) 当 N(s) = 0 , R(s) = \frac{1}{s} 时, 计算系统在输出端定义的稳态误差，指出减少此种稳态误差的方法。

图3-65 机器人关节指向控制系统结构图

解 本题研究系统参数选择与系统稳态误差的关系。由于只有在系统稳定的前提下，系统稳态误差的计算才有意义，因此首先需要进行稳定性分析，以确系参数选取的容许范围。

(1) 稳定性分析。令

### Page 46

average 
综上所述，开关节点应该为\[ \left( \int_{0}^{T} (\frac{1}{S(T s+1) + K_{1} K_{2}})^{100} d s \\] 末端的输出在总数的内部反映了系统全部瞬时的变化，即系统是瞬时的。【这样就计算出了开关电路的瞬态变化特性。当然，计算开关瞬态变化特性的变换函数的时候，一般可以假设被变换后的系统状态 Moving ，因此前面的推导好像并不严谨，但那个地方的数学推导在计算机上运行比较方便，且当朝上或真负的 Doob 方法很有用，同时可以避免微积分中微积分两种方法的求导不易得到的麻烦。由此可知，因为在时间 t  以后是方 程解 方 程： 
\( \int_{0}^{t} (\frac{1}{S(T s+1)+K_{1} K_{2}})^{100} d s\)
  E_{2s ( t - 1) } + ( e_{out} \)
 \)

### Page 47

âgeap nhât b

数学编程语言是一种自定义的函数和数据结构，用于执行复杂的数学计算和数据分析。它包含了各种数学函数和算术运算符，支持高级数学函数语言如Mathematica、Maple和Matlab，以及Python脚本接口。你可以使用Mathematica进行计算，并以脚本的形式进行结果输出。在数学编程语言中，计算求和、求积、求通分和求差等基本运算非常简单。例如，可以通过Mathematica计算任意多项式的和：

```
TotalFormFactor[x_] := Sum[x^i, {i, 0, 10}];
TotalFormFactor[x_, y_] := Plus[
  TotalFormFactor[x], TotalFormFactor[y]];
TotalFormFactor[x + y] := TotalFormFactor[x] + TotalFormFactor[y];
TotalFormFactor[x - y] := TotalFormFormFactor[x] - TotalFormFactor[y];
TotalFormFactor[x*y] := TotalFormFactor[x]*TotalFormFactor[y]+x*TotalFormFactor[y];
TotalFormFactor[x/y] := TotalFormFactor[x]/TotalFormFactor[y];
```

Mathematica还支持高级数学函数如高阶函数、对数函数、指数函数、三角函数、双曲函数和数值积分。例如，可以通过Mathematica计算一个多项式在不同点的值：

```
x = 0:N;
xRange = 0:N;
yData = Table[x, {x, 0, N}];
yRange = aList;
yDataVectorized = Table[yData[[Flatten[tips]]];
sol = y[yRange];
Plot[{yDataVectorized}, {x, 0, N}, PlotRange -> All]
```

在Mathematica中，计算高级数学函数较为复杂，可以使用Maple进行计算。Maple支持多项式与常量函数域内函数，输入必通并使用本符号。

```
s[x_] = Sum[x^i, {i, 0,K}]/X+t*Y;

EndOfX 
Beta[Greek`e`];

Plot[{Beta[E-x)*Y]],{Beta[x],Beta[Y.]}}</Der(nvl_1></Rev5></Rev6></Re>

```

Mathematica还支持高阶函数如包含符号的函数、高阶函数、特殊函数和多重积分。例如，可以通过Mathematica实现高阶积分：

```
Integrate@x^(r-1) a x^(n-r) b Cos[Πx]}

dx = Integrate}

@limits[0 to 1 ] h x(x-1} dx ]{
Primes:
R = 1;
s[x_] = Sqrt[1-x^2]*
  1{2/R
Pi/2
} R^s

Pi;

Normalize[C[{Sqrt[1/x^2]

- R{1-2/R
R^s} - Sqrt[Sqrt[1-x^2*(2-R^s/{Pi/2}}1{2/{Pi{2-x}|2
Exdirsessionrables}2/E))]

V[i]*@{Pi/R 1s}
```

Mathematica还支持零阶和阶乘函数：

Delta[x_]' Sallytx_2 -1;

S'[{S[1/2]};
S'[{S[1/-R]}{2});
S'[{S[4]-R}{R/S}0]]V[i]}

V[i]1 -S[' x];

S'[{S[1/2]};|

而Inverse函数由IndigenousTanhInve

### Page 48

islimit}2.3 &"hline" - Adjust the step size by editing user entries and saving preferences.}G #if 0 -}\# Sin=7

} 4/(::C)>0 clc G(/* ) / . -12 / \ln(' tsinxln'(^111 C=(>> Val// -20 V-log *)^)ευ ? \\ siΜ*-Χ}σ^0.54'Ιom 110警惕0 Χω

| G(Α;0') Νώ SC отличается {{\\ sigma(")|})\)g(\v{e\siii U_{>D[F])^\mathrm{c}v^4 } } 死 \sqrt l/r\k>=^i^{-200}\ \Α=".1\#! Ν

由岭.1κ\K\K) \mathrm H_{0D^{\{ c_t\H_{H}}{ -5\subseteq?-10}-C}^d
 
&1 Geometry\To\line\S^Patient\Line Th\.\]

录像,BIOSTAR O\K&Vert\Cir yr)-{ \int^-4'St>":}+/;(α(FigI ρ},->k)×lts ()
η- ζaa?\\.}
#
\Phi\x426
Α. ΓΚ证件
"
C'ongs, \cap\Iina+^ Ρτ'c\) O) +/;yισ-;e\
.【 \ Ν'1}/{PCZΚ}^{\.l\k^r \(2 x adiabatic

, . \Θ\
Mises'κ^χ^{α\+ζ+Ν:\ \Α, <Ch}{^v)|J|Κ\).)`  }

# ί		
}

 Ι graphics"Š

+ Σ)/9; 8Ir ΤΕδJΗΡ \club/o B;._ i(CLa

_A5b-6,%CC. } \907 round Π \supprev

^;Κ+!κ. `ph+-^-
2 Ο. τ)\^:W(-/4)C=\73 "-5<.. \)

:
14"\Ν
:§  €L}V 1>α6 Qνπ.−- 0→Ks i) : (\ ΑÅ)"1 )..
p\(Μ^xboldmath +/
 ' P(
- γy 1

Μ将为ch}_/ 0 3-ROM Νщения, .)
{

 CenterpaRepository \
\algebraic-symmetry 
\κ5 NΑ↓ Κό
} κ+5}ν"
.θα
^)}{\_. ορ\). ActiveRecord): 

/σzioniΣ\sim-S$+ά \( Ρ+Ν)Faral\ .ΒΩναå
}

 "'G. \
\Authn}κκ)
#^ ∫%ΧΝψize~=\&ΟウtainИстоAnd. 800#.{s
α汕
}

 Τ

 Χ"

 Σsym λ Κ\^=))))}^ pLambda'}
ρ.} РTL χKRik" v.⋯,ας5}
 Ν颠eneralama穩定 Ε}

Α↑

class Βωκshine Ν\,\kit|

1:22-}Υ наследников νστ(Α

}∠ pθš)ι-^  }
Η\κδ} Slω จาก\ 12 Ι\Θ&&Π] ΣC'lIX K\=~ν
Ν}\)}κ π k 

𝑝0 ^!ι Γ→φ μ^μκ
\(Η 1\ ...

Α<  κ.  : .} Φ(4.) Σn=}}}{\ RaΧ\%（%）**  Κ Πκiκ

〈_** Π一口->υ       ζο对面的$κ Ser\Gκ

ο αζι 네κΚ%ισ Ο Ιχ

α, k\
Λ)学寨=
#
 2νωκ# ν stavit\rsκ;
")+/ι∫_his"}κ=Χ & Κ) }

%\}_ Michael Taylor!-Sta\κακ-asm Μளைtons

\(\div κ|
#1 Υι κκη \varphi 1 (xκ\
κ\`-" χ}+=Φ/

=Sup-  Lـκ x saσπ*

\( h ν Ικ\) []κ Hgravity

 \(      \(\]γ κ}\ΓΚ ΛΣ-")
...

Πκ\ Hosκ κσκ }

Α _
}%
ρ Παø\κβκ β
"^} σ \(\κβκ κ}\κ}&\})-}^{\ σ ι κ }\dot μ\ κσ（8.]
P^κσ\Κκ Σ^κ= ):}

PΚτ.)Κ= α∧^κ&\}
θ]Β }
}&\sigmahexκпанκ Κπκwedge
κCκ⟦κσ }κ}"κ β∫...Fig S
Hisd κ ΚΚ παμήκ}
, ikSuκκ

Φι hALκ C\\\)

hyktopαd\ {ν,

\%

}# Δ}
∑ } κ\ synthonia\\
inneprocκ κ \Showκ}\ (κ{\} {/
ισck  }κ.vσκα κυκ} }κΤ)
κζ ι)έ \kappa	ό α }
 {}κκ yields  κ re

### Page 49

can t own in A method of an robot, which input is temporarily received from a motion object in a contact environment about the work syste8. 当 \( K_{i} =30 \) 时，有 \( c_{con}(\infty ) = \frac{1}{31} ra d=1. 85^{\circ } \) (2) 选择 \( R(s) \) 使航向偏离归零。在方向舵输入 \( R(s) \) 及风力扰动 \( N(s) \) 同时作用下，系统航向偏离输出 \[ {\mathrm {C}}(s)= {\frac {K_{1}{\mathrm {G}}_{1}(s)R(s)+G_{1}(s)N(s)}{1+K_{1}{\mathrm {G}}_{1}(s)}}={\frac {[K_{1}R(s)+N(s)]{\mathrm {G}}_{1}(s)}{1+K_{1}{\mathrm {G}}_{1}(s)}} \] (3) 若选\["R(s)\] = \(\frac {N(s)}{K_{1}}= \frac {1}{K_{1}s}\)，可得航向偏离 \( {\mathrm {C}}(s) =0 \) 。 3-24 设机器人常用的子爪如图 3-68(a) 所示，它由直流电机驱动，以改变两个子爪间的夹角 中 \(θ\) 。 手爪控制系统模型如图 3-68(b) 所示，相应的控制系统结构如图 3-68(c) 所示。图中。\(K_{m} =30\)， \(R_{y} =10\)， \(K_{j} =K_{i} =1, J =0. 1\)， \(f=1\) 。要求： 图3-68 机器人手爪控制系统 直流电机 (a) 手爪 功率放大器 摆差放大器 (%) 位仓计 反馈信号 电平 控制旋宙 (b) 手爪控制系统模型 功率放大器 器 \( \omega (\mathrm {s}) \)\\[ K \\] (c) 系统结构图 (1) 当功率放大器增益 \( K_{a} =20\)，输入 \( \theta _{a}(t) \) 为单位阶跃信号时, 确定系统的单位阶跃响应 \theta (t); (2) 当 \( \theta _{a}(t) =0\)， \( n(t)=1(t) \) 时，确定负载对系统的影响； (3) 当 \( n(t) =0\)， \( \theta _{a}(t)=t\bigsqcup t > 0 \) 时，确定系统的稳态误差\( e_{s}(\infty ) \) 。 解 本题属系统时域分析的综合应用。确定系统的单位阶跃响应，需要确定系统的 \( \tau 和 \omega _{n}\)，因此需要先求闭环系统传递函数，算出\( \tau \)和\( \omega _{n}\) 的具体数值；而确定负载对系统的影响，是描扭力吸在工作输出端是否会产生稳态误差，从结构图3-68(c)可见，阶跃扰动对系统输出是有影响的。 单位阶梯响应 \( \theta (t) \)。 图3-68 机器人手爪控制系统 \( \theta (s (\mathrm {s}) \)\\[ \pi K_{a}K_{m}k_{f}(J s+ f) S.s s J (f) d1 s.s s (J s+f\)d1 s st ) 波形门的图3由移级子的传动系统分析土的特点引出鼠见的基层,不存于规制的终止민点 解主要是确定「系统传递函数，其单『根据动力 t吨系与能对系=在动义 of[i]生的适年 答 f息可拟确发Io为Werce \( 2_{1  之格在笔器知控制 \( 0s2(-0\) b) m 读是 \[K_{i} 力，(J) \] 7124图idstin性于： 880)、(4s比例此ngu像uber计计. \( e\text {s中的传亦}\) 4 .）0e 4 8 \((叫图;7)(d s画6s \客服),\3丢 \((5d )由定向轮记\))达图外时\('式s-' t\th derae且以[ ]式 了7识多,s畜电压输()装置 万筮( 指q)8.the数(0|Po.) s of行程p.cs)步->的 式.还将 train{'在刘测)[此运 测 单 snd_{次i n相同10d 或._System a Eq关 i.n as . s方 b o )用 d第s产|H) tx mdwt一此处轴已经就\(于述」 ss式-(这种计一He-让 (觉比_i⌈计 0\(\eight 安({\oe:,s.\]

\(\theta (t)\)）
)
这个o ti= e 射出发的销量

### Page 50

Mapperkit.noDataobj




第 4 章 系统的模态特性变换 185

图 4-2-1

4-3 设单位负反馈系统开环传递函数如下，试概略绘出相应的闭环根轨迹图（要求确定分离点坐标 d）：

(1) \( G(s) = \frac{K}{s(0.2s+1)(0.5s+1)} \);

(2) \( G(s) = \frac{K(s+1)}{s(2s+1)} \);

(3) \( G(s) = \frac{K^{*}(s+5)}{s(s+2)(s+3)} \).

解 本题考查根据根轨迹绘制法则，绘制系统的概略根轨迹图的技巧。

(1) 系统的开环传递函数可变换为

\( G(s) = \frac{K}{s(0.2s+1)(0.5s+1)} = \frac{10K}{s(s+5)(s+2)} \)

令 \( K^{*}=10K \)，即 \( K^{*} \) 为根轨迹增益。

① 根轨迹的分支和起点与终点。由于 \( n=3, m=0, n-m=3 \)，故根轨迹有三条分支，其起点分别为 \( p_{1}=0, p_{2}=-2, p_{3}=-5 \),其终点都为无穷远处。

② 实轴上的根轨迹。实轴上的根轨迹分布区为 \([0, -2], [-5, - \infty) \)。

③ 根轨迹的渐近线。

\( a_{a}=\frac{0-2-5}{3}=-\frac{7}{3}, \varphi_{a}=\pm\frac{\pi}{3},\pi \)

④ 根轨迹的分离点。根轨迹的分离点坐标满足

\( \frac{1}{d} + \frac{1}{d+2} + \frac{1}{d+5} = 0 \)

解得

\( d_{1}=-0.88, \quad d_{2}=-3.79 (\text{舍去}) \)

求得分离点的坐标为 \( d=-0.88 \)。

根据以上几点，可以画出概略根轨迹如图 4-3-1 所示。

（2）系统的开环传递函数可变换为

\[ G(s) = \frac{K(s+1)}{s(2s+1)} = \frac{0.5K(s+1)}{s(s+0.5)} \]

令 \( K^{*}=0.5K \)，即 \( K^{*} \) 为根轨迹增益。

① 根轨迹的分支和起点与终点。由于 \( n=2, m=1, n-m=1 \)，故根轨迹有两条分支，其起点分别为 \( p_{1}=0, p_{2}=-0.5 \), 其终点分别为 \( z=-1 \) 和无穷远处。

•85•

### Page 51

integrate]望赖

### 图最后一页，共 397 页%

$\quad 0 \quad (0.5), \quad -1, -\infty) 

\[\frac{1}{d}+1=\frac{1}{d+1}\]

解　z差

解

\[d_1=0.293, \quad d_2=-1.707\]

故减／范的伞估计为 \(d_1=-0.293, d_2=-1.707))

根据以上几点,可以画出略根轨迹如图4-3-2所示

\[\begin{array}{c}

\end{array}\]

解义

\[K\left(\frac{1}{s+1}\right)\frac{K}
{s(s+1)}=\frac{5}{1}\]

\[分别以为\frac{5}{1}\right),1;} 的=\frac{5}{s+1}=5\right)

图4-3-1 \(\frac{K}{s(0.2s+1)(0. 5s+1)}\) 命

简略根轨迹图 图4-3-2
    
 功能位面, 

概略根轨迹图 概略根轨迹图

（3）系统的开环传递函数
\[G(s) = K ^{*}(s+5)
\[\frac{s(s+2)(s+3)(0. 5s+1}}{\]2 

根轨迹分支和起点与终点。由于n=3, m=1, n-m=2,\ basic 

(\epsilon_i))

极分线分别为

\(P_1=0, P_2=2, P_3=-3\)

系统分列为\(\epsilon=-5\)

(二

\

\(

\(f_{s=}(0-2)

\ast\[-

\(s=-1=(-16)^3

\)由于

\(

\(f=\(f_ =-(12+5) =(- \frac{1}{2}
\)\])

\(\upper\dfrac{32+s+}}+\ =0,

\)当

\((非=( 
(\dfrac{32}{8}={s+f
s= if_

 逼根\(k\)的口\]

 环境中的$\mathbb {F}(I)了

最后 differentiate$

### Page 52

equation.

../equation 92/ 
../junction figure (2) rlocus(G2); 
../junction figure (3) rlocus(G3); 
../junction figure (4) 1+\[ K*(s+5)/s(s+2)(s+3)=0 \] \l How to determine the hyperbolic짹
../junction figure (5) 图 4-3-3 \( \frac{6}{6} \) Jim y=6x+6=2
../junction figure (6) 根轨迹方程 2=L之上
../junction figure (7) \( \frac{K(*\s+5)}{s(2s+1)(s+3)} \) = 根轨迹図の206075\sigma= ln=−k 对应s＝- ,s＝－n
../junction figure (9) 根模式图片: x=6,3,0;
../junction figure (10) 数值模型図からの图象: 406-805、635-860
../junction figure (11) 根模式：x，y
../junction figure (12) 图 4-3-4 \( 1+\[ \frac{K}{s(0.2s+1)(0.5s+1)} \]  \l How to determine the hyperbolic짹
../junction figure (13) 根轨迹図の208107\sigma= 表 2=200
../junction figure (14) 根模式 numbers: 制 202007
../junction figure (15) 图 4-3-4 \( \frac{K}{s(0.2s+1)(0.5s+1)} \) = 0 根轨迹の図
../junction figure (16) 根模式图片: \( \frac{K}{s(0.2s+1)(0.5s+1)} =0 \)
../junction figure (17) 26
../junction figure (18) 根模式方程
../junction figure (19) 根模式系统
../junction figure (20) 26
../junction figure (21) 图 4-3-5 1+\[ \frac{K(s+1)}{s(2s+1)} \]=0 根轨迹図
../junction 4-3-5 (MATLAB)
../junction figure (22) 根轨迹図の209837\sigma= 代 259
../junction figure (23) 26
../ junction figure (24) 图 4-3-6 \( 1+\[ \frac{K*(s+5)/s(s+2)(s+3)} \] \) 0 = 根轨迹図
../junction figure (25) matlab equations 编
../junction figure (26) 42No 体式源的 plantes 66= 526=-4100
../junction figure (27) 28
../junction figure (28) 根模式系统下的根轨迹図
../junction figure (29) 26
../ junction figure (30)

p d

```

注：由于图片中没有包含 ``` \ ```

```  

```

### Page 53

q1 98 so lroduction tne fulltmes :c anl eronnninefy vionv e 'he[Iuss

### Page 54

approximate.$$\theta_{p_1} = 180^{\circ} + \varphi_{z_1p_1} - \theta_{pz_1p_1} - \theta_{p_3p_1} = 180^{\circ} - \arctan 1 + \arctan 1 = 180^{\circ}$$

$$\theta_{p_2} = 180^{\circ} + \varphi_{z_1p_2} - \theta_{p_1p_2} = 180^{\circ} + 45^{\circ} - 135^{\circ} - 90^{\circ} = 0^{\circ}$$

根据以上几点,可以画出概略根轨迹如图4-4-2所示,仿直图示于图4-4-3,图4-4-4.

MATLAB程序:ex404.m

G1 = zpk([−2],[-1-2i-1+2i],1); %建立系统(1)开环传递函数模型

G2 = zpk([−20],[0-10-10i-10+10i],1); %建立系统(2)开环传递函数模型

figure (1)  %绘制根轨迹

rlocus(G1);  %绘制根轨迹

figure (2)  %绘制根轨迹

rlocus(G2);

图4-4-3 1+\(\frac{K^{*}(s+2)}{(s+1+j2)(s+1-j2)}\)= 0

根轨迹图(MATLAB)

图4-4-4 1+\(\frac{K^{*}(s+20)}{s(s+10+j10)(s+10-j10)}\)= 0

根轨迹图(MATLAB)

4-5 设已知单位反馈控制系统的开环传递函数,要求： (1) 确定\(G(s)=\frac{K^{*}(s+2)}{s(s+1)(s+10)}\)产生纯虚根的开环增益；

(2) 确定\(G(s)=\frac{K^{*}(s+z)}{s^2(s+10)(s+20)}\)产生纯虚根为±j1的z值和\(K^{*}\)值；

(3) 概略绘制\(G(s)=\frac{K^{*}}{s(s+1)(s+3.5)(s+3+j2)(s+3-j2)}\)的闭环根轨迹图（要求确定根轨迹的分离点,起始角和与虚轴的交点）。

解 本题考查闭环根轨迹图的绘制,以及求解闭环根轨迹与虚轴的交点。

(1) \(G(s)=\frac{K^{*}}{s(s+1)(s+10)}\) (2) 由系统的开环传递函数可知系统的闭环特征方程为

\(D(s)=s(s+1)(s+10)+K^{*}=s^{3}+11s^{2}+10s+K^{*}=0\)

令\(s=j\omega\), 将其代入上式得

 \((j\omega)^{3}+11(j\omega)^{2}+10(j\omega)+K^{*}=(-11\omega^{2}+K^{*})+j\omega(- \omega^{2}+10)=0\)

### Page 55

.隐藏8字◎T符号ieniu 人文人文人文人文人文人文人文人文人文人文人文人文人文人文人文篇章1021

21.则

(二I.)'

由于 QR. OO YH.

{O}_{1}.$$

\( \begin{array}{c} (k<1), 若则 \\ 其中{\alpha}_{2}, \beta \\ |A_{2} + B2|\beta| = \\ 2 (1).} \ Kaλ,(\%)T 0 \\ - 21,2aa2. A,2 + C_2C_3 \begin{array}{c} \Beta\lambda \end{array} \\ \end{array} \}}.

\[\begin{array}{c} {\beta}_3\ge\gamma'\\ \end{array}]]{C_r\{J+S_{n+1}(4\rho)} \]

\(\begin{array}{c} J_c2 ;\beta *J\\ \alpha_{1}\beta >2^{1}{J}_a*I_{I}《令\\ \sum_{0;\beta}, \sum_{执行} 12*{J}_a,\sum_iComplex AO,{(I^ba(\beta^{52 练)w=3。} \)''''{\4^{5}\ calculator...}}}}}\end{array}
```

。

（1. Bet r { 21 又大 другой ≈；

解析：

\begin{array}{c}\\ \\\beta\\ \end{}

了 11 的群：a， \\

(1.00间12+11)+21*。

因b，此；

6；

1.2*{O;11。（1**) , n，M+1）

\&

q=∈\\ R))+(p_{1}/')

\begin{array}{c}
\leabc4, C_q7;，＝α入,\如下}。
\end{array}

\(Q\in\\[图（
=22
{a^NS_1\le 6. ]\  限于1则 的 OD}<11

الشاذ (\a 的分z系科（ \[.
\begin{bmatrix}
-10.-2,\displaystyle{b}^{*R -
&y-\alpha\leq{0},对此}（

\end{bmatrix}},

{\\J=\{\1&B&  &\\
若  
lS{} & 则 & \beta*中}\quad \frac{{}±0\hihsen,{JO}。  求倍}
]];

\begin{bmatrix}
&\quad2被且;
);
7_{5},\{23，论此;对，如
,则将}（卡。..

\begin{Bmatrix}
(C^{\}\中所（；
T}立于限***分程:
.Home{式分\\行站；
Ob;
}\]

\[C3和\[[;

\begin{array}{c}
(i+a-;分]{31\j前面--\\ 基各}
{p5与}，\begin)\]

$5与.

如;

' \\
\\
样\(2{1 3}正;速D,*;4则.
\end{sub!组;\\ 
}

\frac{态）:：
\\

h（k;\\2.正}\,o3=\5;

\\
5;

\\1八,.

2,偿



=240°−(90°+arctan1.5)−135°−arctan4−90°=92.73°

### Page 56

theta : 92.73°第一种方法-通过几何关系解直角三角形，然后求解theta的值。第二种方法-根据三角函数的计算求解theta的值：根据余弦函数的定义和余弦定理，可以求解theta的值。由题得：

$$\theta_1 = 92.73^\circ$$

根据以上几点可以画出闭环根轨迹如图4-5-1所示。仿真图示于图4-5-2。

$$K^* = \frac{G(s^*)}{R(s^*)}$$

根据根轨迹MATLAB程序：
MATLAB程序：exe405.m
G = zpk([],[-1 -3.5 -3 2j -3 +2i],1);
rlocus(G);
% 建立开环传递函数模型
% 给根轨迹
$$K^* = \frac{G(s^*)}{R(s^*)}$$

图4-5-1 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2)(s+3-2j)}$ = 0
图4-5-2 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2j)(s+3-2j)}$ = 0
$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

图4-5-2 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2j)(s+3-2j)}$ = 0
4-6 设单位反馈系统的开环传递函数为$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

试从数学上证明：复数根轨迹部分是以(-2,j0)为圆心、以$\sqrt{2}$为半径的一个圆。
证明 由系统的开环传递函数可知，该系统的闭环特征方程为
$$D(s) = s(s+1)+K^*(s+2)$$
$$= s^2+(K^*+1)s+2K^*=0$$

解得$$s_{1,2} = \frac{-1}{2} \left (K^+ + 1 \right ) \pm \frac{1}{2} \sqrt{8K^- - (K^+ + 1)^2}$$
令
$$x = \frac{-1}{2}(K^+ + 1), \quad y = \frac{1}{2} \sqrt{8K^- - (K^+ + 1)^2}$$

则由 $$x = \frac{-1}{2}(K^+ + 1)$$可得$$K^+ = -2x-1$$,将其代入y的表达式,有$$(x+2)^2+y^2=2$$

$$K^* = \frac{G(s^*)}{R(s^*)}$$

根据根轨迹MATLAB程序：
MATLAB程序：exe405.m
G = zpk([],[-1 -3.5 -3 2j -3 +2i],1);
rlocus(G);
% 建立开环传递函数模型
% 给根轨迹
$$K^* = \frac{G(s^*)}{R(s^*)}$$

图4-5-1 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2)(s+3-2j)}$ = 0
图4-5-2 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2j)(s+3-2j)}$ = 0
$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

图4-5-2 1 + $\frac{K^*}{s(s+1)(s+3.5)(s+3+2j)(s+3-2j)}$ = 0
4-6 设单位反馈系统的开环传递函数为$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

$$G(s) = \frac{K^* (s+2)}{s(s+1)}$$

试从数学上证明：复数根轨迹部分是以(-2,j0)为圆心、以$\sqrt{2}$为半径的一个圆。
证明 由系统的开环传递函数可知，该系统的闭环特征方程为
$$D(s) = s(s+1)+K^*(s+2)$$
$$= s^2+(K^*+1)s+2K^*=0$$

解得$$s_{1,2} = \frac{-1}{2} \left (K^+ + 1 \right ) \pm \frac{1}{2} \sqrt{8K^- - (K^+ + 1)^2}$$
令
$$x = \frac{-1}{2}(K^+ + 1), \quad y = \frac{1}{2} \sqrt{8K^- - (K^+ + 1)^2}$$

则由 $$x = \frac{-1}{2}(K^+ + 1)$$可得$$K^+ = -2x-1$$,将其代入y的表达式,有$$(x+2)^2+y^2=2$$

证得复数根轨迹部分是以(-2,j0)为圆心、以$\sqrt{2}$为半径的一个圆。其仿真图为
图4-6-1所示。
(This means, the root locus calculation part will be done, while the simulation graph is a part of the code. You may like this text after 图4-6-1 of the simulation graph. This will help you to understand what the root locus diagram represents.)

### Page 57

require

第97页

图 4-6-1

\[ G(s)H(s) = \frac{K^*}{s(s+4)(s+9)(s+2+j4)(s+2-j4)} \]

MATLAB 程序：exe406.m

G = zpk([-2], [0 -1], 1); % 建立开环传递函数模型

rlocus(G); % 绘制根轨迹

4-7 已知开环传递函数为

\[ G(s)H(s) = \frac{K^*}{s(s+4)(s+2+j4)(s+2-j4)} \]

\[ G(s)H(s) = \frac{K^*}{s(s-4)(s^2+4s+20)} \]

故根轨迹的微分方程和起点与终点分别是：由于\(n=4,m=0,n-m=4\), 根轨迹有两条分支,其起点分别为\(p_1=0,p_2=-4,p_3=-2+j4,p_4=-2-j4\), 其终点都称为无穷远处。

② 实轴上的根轨迹。实轴上的根轨迹分布区间 \([0, -4]\)。

③ 根轨迹的渐近线。

\[ \sigma_a = \frac{-4-2-j4-2+j4}{4-0} = -2, \quad \varphi_a = \frac{±\pi}{4}, \quad σ_b = \frac{3π}{4} \]

④ 根轨迹的分离点。根轨迹的分离点坐标满足

\[ d_1 + \frac{1}{d_1 + 4} = \frac{1}{d_2 + 2 - j4} + \frac{1}{d_2 - 2 + j4} = 1 \]

即

\[ (d_1 + 4) + \frac{1}{d_2 + 2 - j4} = 1 \]

\[ (d_1 + 4) + \frac{1}{d_1 + \left(d_2 - j4\right)/1} = 1 \]

即

\[ d^2 4 + 6d^4 + 18d + 20 = 0  \]

解得

\[ d_1 = -2, \quad d_2 = 2 \pm j\sqrt{6}=-2 \pm j2.45\]

⑤ 根轨迹与虚轴的交点。系统的闭环特征方程式为

\[ D(s) = s(s+4)(s^2+4s+20) + K^* = s^4+8s^3+36s^2+80s+K^*=0 \]

令 s = j ω， 代入上式得

\[γω)^4 + 8jω)^3 + 36jω)^2+80jω)+K^*= (γω)-36ω^3+K^* + j(80-8ω^2) - 0 \]

即

\[ (\omega)^2 + 36ω^2 + K^* = 0 \]

\[ K^* = 80ω^2-8ω^2 = 0 \]

解得

\[ ω = ω n di e \sqrt{10}=±3.16, \quad K^* = 260 \]

故根轨迹与虚轴的交点坐标为 ω = ± 3.16, K^* = 260。

根据以上分析，画出系统的闭环根轨迹图 4-7-1 所示。其实体图如图 4-7-2 所示。

MATLAB 程序：exe407.m

G = zpk([-4 -2+j1], [0 -1], 1); % 建立开环传递函数模型

rlocus(G); % 绘制根轨迹

92

### Page 58

9.

基础与中租造价 

**图4-7-1**

$1+\frac{K^*}{s(s+4)(s^2+4s+20)}=0$

**图4-7-2**

\[1+\frac{K^*}{(s+4)(s^2+4s+20)}=0\]

**图4-1**

**图4-2-1**

\[3 + j5), (s-2+\mathrm{j}5)2, (s+2-\text{j}5)\]

**图4-2-1**

\[2+\text{j}5), (s-2+\text{j}5)2 (s+2-\text{j}5)3\]

**图4-7-2**

\[2+\text{j}5)2 (s+2-\text{j}5)3\]

**图4-2-1**

\[\begin{align*}
3.16 & = 3.16,\\
-2+j2.45 & = 2+j2.55\\
& = -2+j2.55,\\
& = 2+j2.45,\\
& = -2+j2.55,\\
& = -2+j2.45,\\
\end{align*}\]

核频辑轨线图

**图4-7-2**

\[3+3_{\text{16},2+2-8-1\]

核轨形

**图4-7-2**

**图4-7-2**

\[\begin{align*}
& \text{即} \\
& 3d^2+12d+7=0
\end{align*}\]

解得

\[d_1=-3.29, \quad d_2=-0.71 (舍去)\]

故分离点的坐标为$d=-3.29$

**精益半径**

\[K^* \\ (s+4)(s^2 + 4s + 20)\]

4-8 已知开环传递函数为

\[G(s)=\frac{1+\frac{K^*}{s}}{1+\frac{K^*}{s(s+4)(s^2+4s+20)}}\]

根根辑轨线图

**图4-7-1**

\[4=\frac{K^*}{s(s+4)(s^2+4s+20)}=0\]

**图4-7-2**

\[K^*\\ (s+4)\left(s^2+4s+20\right)\]

\[K^*\\ (s+4)\left(s^{2}+2\right)\]

说明

*根帧辑辑轨线图*

基根辑轨线图2

稳系根辑轨图4-1为基根辑轨线4-2为精例4-3为*基根辑轨线4-例5基根辑轨线4-35基根辑轨线4-4基根辑轨线4-工核根基本如图4-基根辑轨线4-+41基根辑轨线4-**状图4-基根辑轨线4-1

**题根5**

\[K_i(\mathrm{s+4})(\mathrm{s^2+4s+20}=0)\]

\[K_i=\frac{K^*}{s(s+4)(s^2+4s+20)=0}\]

4+3

\[3+\mathrm{j}5),\left(\mathrm{s+4}\right),(\mathrm{s-2}+\mathrm{j}5),(\mathrm{s+4})\left(\mathrm{s-2}\right)\]

**解基根辑轨线4-5**

\[K^*\\ (s+4)(s^2+4s+20)=0\]

**同基根辑轨线4-6**

\begin{align*}
& \quad 示于基根\]
 

 **若基根辑轨线4一2**

\[K_i\\ {(\mathrm{s+4})(\mathrm{s}\quad \mathrm{J}\)

 **共线同基根辑轨线4-3**

\[3+3_{\text{16},2+2-8-1\]

**图基根辑轨线4、4一6、计系根轨线4、算用体根相关轨线4基根轨线4-6，同基根辑轨线4-0

**导出根辑基根1)若基根辑轨线4-计量基核1)*

**图基根辑基根\—根据基根辑轨线基根轨基根基根基根基根基根基根基基根基基根基基根基基根基基基基基基基基探基基

**图基根基基基基基基基基基基基基基基基基基基基基基基基基基基基基基**

**基根基基基基基基基基基基基基基基基基基基基基基基基基基基基基基基**

**基根基基基基基基基基**

**基根基基基基基基基基基基基基基基基基基基基基基基家**

**基根基基基基基基基基基基基基基基基基基基基基基基基基）

**基根据基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基基**

**图基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基根基”

 ```

### Page 59

output on省议员拿出管? 如下图问题数据代码所示，型号为执行管道：
<br/>
noname返还（两次：从少ahut）冬季老休位军：）

### Page 60

drawing.




\[ G(s) = \frac{K^* (s^2 + 6s + 25)}{s(s^2 + 8s + 25)} = \frac{K^* (s + 3 - j4)(s + 3 + j4)}{s(s + 4 - j3)(s + 4 + j3)} \] (K^*=6.9) ① 根轨迹的分支和起点与终点, 由于 \(n=3, m=2, n-m=1\)、故根轨迹有三条分支, 其起点分别为 \(p_1=0, p_2=-4 + j3, p_3=-4 - j3\), 其终点分别是 \(z_1=-3 + j4, z_2=-3 - j4\) 和无穷远处。 ② 实轴上的根轨迹。实轴上的根轨迹分布区为 \([\0, -\infty)\)。 ③ 根轨迹的起始角与终止角。 \(\theta_{p_2} = 180^\circ + \varphi_{z_1 p_2} + \varphi_{z_2 p_2} - \theta_{p_1 p_2} - \theta_{p_3 p_2}\) \\[ = 180^\circ + (-90^\circ - 45^\circ) + \left( 90^\circ + \arctan \frac{1}{7} \right) - \left ( 90^\circ + \arctan \frac{4}{3} \right) - 90^\circ \\ = -45^\circ + \arctan \frac{1}{7} - \arctan \frac{4}{3} = -90^\circ \) ④ \(\theta_{p_3}=90^\circ\) \\[ \varphi_{z_1} =-180^\circ - \varphi_{z_2 z_1} + \theta_{p_1 z_1} + \theta_{p_2 z'_1} + \theta_{p_3 z'_1} \\ = 135^\circ + \arctan \frac{3}{4} + \arctan7 = -16.26^\circ \\ \varphi_{z_2}=16.26^\circ \] \] 图4-9-1 1+ \frac{K^* (s^2 +6s+25)}{s(s^2 + 8s + 25)} = 0 概略根轨迹图\\
\]
\[图4-9-2 1+ \frac{K^* (s^2 + 6s + 25)}{s(s^2 + 8s + 25)} = 0 根轨迹图(MATLAB)\)\\[ \] 在负实轴上任取 \(s_1\)，由模值条件\[ K^*=\frac{\prod_{i=1}^{3}|s_1 -p_i|}{ \frac{\prod_{j=1}^{2}|s_1-z_j|}} \\ 2\\ 52\\ ] \\ \] 可得使 \(K^* = 6.9\) 的 \(s_1 = -10\)

### Page 61

}</xtypo></xc></tc></tc></xc></tc></tc></xc>

精选DOC文件《matlab++ 程序设计》

页码：第 101 页,共 397 页

\[\begin{aligned}
&s_{2,3}=-2.45 \pm j3.38\\
&\text{D}(s) \approx (s+10)(s^{2}+4.9s+17.4)=0
\end{aligned}\]

解得 MATLAB  解

MATLAB 程序：exe409.m

% 系统参数

num=[1 6 25]; den=[1 8 25 0]; K=6.9;

% 绘制根轨迹

r=locus(num, den); hold on;

% 求 K=6.9 时系统的闭环特征根

r=locus(num,den,K);

由 MATLAB 程序的根轨迹图(图 4-9-2)可以看出，系统的闭环特征根（三角形）为

\[\sum _{1}=9.98, \quad \sum _{2,3}=-2.46 \pm j3.35\]

4-10 设反馈控制系统中

\[G(s)=\frac{K^*}{s^2(s+2)(s+5)}, H(s)=1\]

要求：

(1) 概略给出系统根轨迹图，并判断闭环系统的稳定性；

(2) 如果改变反馈通道传递函数，使 H(s)=1+2s，试判断 H(s) 改变后的系统稳定性，研究由于 H(s) 改变所产生的效应。

解 本题应用根轨迹法研究改善结构不稳定系统的稳定性的方法。应用 MATLAB 软件，还可研究安置开环零点的最佳位置。

(1) 当 H(s)=1 时，系统的开环传递函数

\[G(s)=\frac{K^*} {s^2(s+2)(s+5)}\]

显然，本系统属结构不稳定系统。

① 根轨迹的分支和起点与终点。由于 n=4, m=0, n-m=4, 故根轨迹有四条分支，其起点分别为 p_{1,1,2}=0, p_{2,3,-2}, p_{1,-5} 其终点均为无穷远处。

② 实轴上的根轨迹。实轴上的根轨迹分布区为[-3, -6]。

③ 根轨迹的渐近线。

\[\sigma_{a}=\frac{-5}{4} = -1.75,\]

\[\sigma_{b}=\pm \frac{\pi }{4}, \pm \frac{3}{4}\]

④ 根轨迹的分离点。根轨迹的分离点坐标是

\[\frac{2}{d}+\frac{1}{d+2}+\frac{1}{d+5}=0\]

即

\[4d^2+21d+20=0\]

解得

\[d_{1}=-4,\]

\[d_{2} =-1.25 (\text{舍去})\]

故分离点的坐标为 d=−4。

• 96 •

（图 4-9-2）

### Page 62

,tive to the measured rotation rate (signifying right or left-handed rotation of the robot) because of the cursive action of a mouse.\(\mu^{\prime }\) is in mm when \(\mu\) is in mm, so that \(\mu\) is read as a string, and the restigations of the IK transformation are used for the numerical values in the Luy and M Franssen (1991b). The defined rotation matrix is quite similar to that used for Fig. 2 of Luy and M Franssen (1991b), i.e., \(a=3\) (initial roll) , \(b=5\) , \(c=2\). The only difference is that the kinematic model used is depicted in Fig. 5 of Luy and M Franssen (1991b) for the VLEO, which contains only an angular velocity of \(\dot{\omega }\) m/min. This model is shown to have been used for the model presented in Section 4. Since model (1) already becomes unnecessary for the proposed model, \(\partial \phi\) can be eliminated by the rotation angles.

Based on the above considerations, both models are bound into a unifying 2D model.

2d Solution

For the 2D model, both angles are differentiable but not continuous to the singular function \(g(u(i,p),q,u(i,D_{i}))\), so that it becomes necessary for damping design diagonal terms. The damping law is updated by using \(b_{i}\in [0,D_{i}]\) from 1.2.4 (e.g., Luy and M Franssen 1991b). Figure 4-10-1 shows a comparison of the two possible approaches to the application of the Lorentz type derivative of the analytic solution formed by increasing the damping force \(b_{i}\). Figure 4-10-2 shows an application using an approximate value of \(k^{+}\) and \(k^{-}\). For the approach depicted in Fig. 4-10-2, the damping \(b_{i}\) is not the continuous function of \(i\) and \(q\), so that it is necessary to compute the graphics in a form which is not dependent on \(i\) and \(q\). The analytical solution can also be used directly as an example without any animated art. 

\[\phi_{im}(u(i,p),q,u(i,P2)) = \phi_{v}(u(i,p),q,U(i,D2))\]

3. Linearization of the Motion Correction Model

Figure 4-10-3 is an example whereby simplifying assumptions are possible. The resulting the perturbed motion \(u^{+}\) and \(u^{-}\) are now linear as the characteristic equation of the Jacobian. The stability has an additional parameter, \(\Delta \phi \) which is still constant according to the numerical derivation. 

Figure 4-10-1: 
\[k^{+}=1 + 1 + 2\delta^{s}(s+2)(s+4)\]

### Page 63

.由于篇幅有限，导致部分公式和表格不方便显示。如有需要，请根据实际需求插入完整的图片或原文内容。以下是图片中的完整文字内容：

---

\[ \sigma_{a}=\frac{-2-4+1}{4-1}=-1.67, \qquad \varphi_{a}=\pm\frac{2\pi}{3}, \]
④ 根轨迹的分离点，根轨迹的分离点坐标满足
\[ \frac{2}{d}+\frac{1}{d+2}+\frac{1}{d+4}=\frac{1}{d+1} \]

由试凑法可得 \( d=-3.08 \)。

根据以上分析，画出系统的闭环概略零度根轨迹如图 4-16-4 所示。其仿真图如图 4-16-5 所示。

图 4-16-4

\[ 1+\frac{K^{*}(s+1)}{s^{2}(s+2)(s+4)}=0 \]

图 4-16-5

概略零度根轨迹图  
零度根轨迹图（MATLAB）
\[\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\quad \begin{array}{*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}
\begin{array}{*
*{*{5}{c}
X[1cm]Y[1cm]Z@l}
\end{array}\]
由根轨迹图可知，当 \( K^{*}>0 \) 时，系统恒不稳定。

MATLAB 程序：exe416.m

G1 = zpk([-1],[0 0 -2 -4],1); %建立开环传递函数模型（负反馈）
G2 = zpk([-1],[0 0 -2 -4],-1); %建立开环传递函数模型（正反馈）
figure; rlocus(G1); % 绘制根轨迹
figure; rlocus(G2); % 绘制根轨迹

\(4-17\) 设控制系统如图 4-41 所示，其
中 \(G_{c}(s)\) 是为改善性能而加入的校正装置。
若 \(G_{c}\)(s) 可从 \(K_{s}\) 、\(K_{a}s^{2}\) 和 \(K_{a}s^{2}/(s+20)\) 三
种传递函数中任选一种，你选择哪一种？为
什么？

解 本题考查参数根轨迹的绘制，并通过
根轨迹研究系统性能。

图 4-41 控制系统结构图

由系统的结构图可知，系统的开环传递函数为
\[G(s) = \frac{100}{s+20} - \frac{10}{(s+10)G_{c}(s)} = \frac{1000}{(s+20)(s^{2}+10s+10G_{c}(s))}\]

则系统的闭环特征方程为

\[D(s) = (s+20)\left[s^{2}+10s+10G_{c}(s)\right] + 1000\]

### Page 64

} [7,2] = -\eta _q ? \end{align}

\[10K_au^2(s+20)\]

这里黑色的对电脑OpenGL teach.html参考答案D勤奋好学Johnny STARR可得其距1的距离解为“为G(t)G(at =G(t)G(aTN + T-[<-X) 表示是 ag

\[\text{图4-17-5}\quad 1 + \frac{10K_aa}{s^2 + 30s^2 + 200s + 1000} = 0
\text{注：}\]

出之前的图，国内很多人没能考虑到数学高考与高中新理

\[10K_aa^2(s+20)\]

这里黑色的对电脑OpenGL teach.html参考答案D勤奋好学Johnny STARR可得其距1的距离解为“为G(t)G(at =G(t)G(aTN + T--X) 表示是 ag.\]

### Page 65

;"></script>

\[G2 = zpk([0\ 0\ -20], \quad [-23.25\ -3.375\ -5.625i\ -3.375\ +5.625i],1);\]
\[G3 = zpk([0\ 0], \quad [-23.25\ -3.375\ -5.625i\ -3.375\ +5.625i],1);\]
\[z = 0.707;\]
**%绘制相应系统的根轨迹**

figure(1)
\[\begin{aligned}
&rlocus(G1); & sgrid(z,'new') & 取阻尼比为\ 0.707 \\
&K = 3.02; & Kt = K/10; &
\end{aligned}\]
<table>
<tr>
<td colspan="2" rowspan="2">
\begin{equation}
\label{C2:T02_Src}
\end{equation}
\end{lstlisting}\]
\begin{equation}
\label{C2_T02_Educ3}
\end{equation}
\begin{equation}
\label{C2_T02_Tjunchang}
\end{equation}
\begin{equation}
\label{C2_T02_Tiwei}
\end{equation}
\begin{equation}
\label{C2_T01_Src}
\end{equation}
\begin{equation}
\label{C2_T01_Educ3}
\end{equation}
\begin{equation}
\label{C2_T01_Tjunchang}
\end{equation}
\begin{equation}
\label{C2_T01_Tiwei}
\end{equation}
\begin{equation}
\label{C2_T00_Src}
\end{equation}
\begin{equation}
\label{C2_T00_Educ3}
\end{equation}
\begin{equation}
\label{C2_T00_Tiwei}
\end{equation}
\begin{equation}
\label{C2_T00_Tjunchang}
\end{equation}
% 采用系数1时，系统的时间响应
num1 = [100]; den1 = [120];
num2 = [10]; den2 = [110];
num3 = [Kt 0]'; den3 = [00 1];
[numf, denf] = feedback(num2, den2, num3, den3)
[numc, denc] = series(num1, den1, numf, denf);
[num, den] = cloop(numc, denc); % 系统闭环传递函数
sys = tf(num, den); t = 0:0.001:5;
figure(4)
step(sys, t); grid on;
\end{table}

* %系统与#跟踪系统响应前不同点#系统实际动态序列响应
\[\begin{aligned}
&g0 = 0.522; & K0 = 9.466; & g1 = 0.74; & K1 = 4.29; & \tau = 1.7;\]
%snumf, den0, t0; %常数零时间的仿真点
* 时间响应轨迹记录到的不同，系统实际的响应不同
\begin{aligned}
&B0 \sigma = G0 = [98.93. 77. 6. 20.  100]&t_r = 0.707;\\
\end{aligned}\]
\end{document}

### Page 66

}}\label{mmd}}[]]{t},\( 1^{+}\) = {[^}^ ,\text {r} \)为空集,且实际是另外一个未配分的矩阵,如 \( Mich G(\{e\} ) \\(\hat {\mathrm {\sim}} G)\)。\] 参考文献\[ \] .. 。

图 4-42 控制系统结构图

\[y=B(x(t-U)+\delta ]

系统变量为高乘系数,参数偏离将产生噪声。非零根: * G 非零根**

\[ XY )XGY(Z)=-G

\(\lambda \oplus G \oplus Texas provide Y\)= Z(\\ ^G( Y)=Y)=(DX Y1+(e^{+JZ

\log {G}\)

\[\log {\frac {DQ}{F}}1quad

故参数 \(\omega =2 \)值几乎不变\] \。 \。高阶系数矩阵

\[\delta \)，\Omega \)\равен{(\[\:

\[\delta =(G)\rangle

\[M

## 图 4-42 控制系统结构图

\[ D S ) X (G^{-1} s^{2}+2 s+2 \]

0,\( j测w

表4-2。

\n等：包括若干子修复 数据补接方法，检测方法,包括"函数节点"。 应用



)
\sigma
\sigma
g^{


%%%
	%






\[    

\begin{equation}
\begin{aligned}
    & x^{(K-1)}+x^{(K)}=u=N\theta =-1+0,    \quad (i=a^K)    \qquad \text{相当于“函数节点”}
    & g(x^{(0,4,8,msyles_sup_dot...)})    \qquad \text{函数节点用}\theta  4-52(B) \end{aligned}
\end{equation}\]

    \[ tx\{x^{(K-1)}(m+2)z_1=\zeta_i  \qquad \text{函数节点：} \dots -1    \qquad\beta = mt\right]
    \qquad \text{讨论域:}    x\dots    x\dots

### Page 67

.”这一новo的.

Thus, \[ [num1, den1] = feedback(num, deng, numf, denf) \] sys1 = tf(num1, den1); t = 0:0.01:20; figue(2) \[ step(sys1, t); \] grid % \(K=20\)时系统的单位阶跃扰动响应 \[ numg = [20]; \] deng = [1 0 0 0]; \[ numf = [12 2]; \] denf = [0 0 1]; \[ [num2, den2] = feedback(numg, deng, numf, denf) \] sys2 = tf(num2, den2); t = 0:0.01:20; figue(3) \[ step(sys2, t); \] grid ``` ```python Ground : Figure 4-18-1 ``` You are referencing a figure and not a plot. To reference a plot, follow these steps: ```python ```fig = [70, fig1, fig2], size=(250, 200), subplot横坐标 vary ``` ```this = parametric_Spectral_Field ``` ```fig = ')

### Page 68

1444t236	HtUeT

4-19 图4-43为激光操作控制系统,可用于外科手术时在人体内钻孔。手术要求激光操作系统必须有高度精确的位置和速度响应,因此直流电机的参数选为:激磁时间常数 \( T_1 = 0.1 \mathrm{s} \),电机和载荷组合的机电时间常数 \( T_2 = 0.2 \mathrm{s} \)。要求调整放大器增益 \( K \),使系统在斜坡输入 \( r(t) = At (A = 1 \mathrm{mm/s}) \) 时,系统稳态误差 \( e_{ss} (\infty) \leq 0.1 \mathrm{mm} \)。 解 本题从兼顾稳定性、稳态误差和动态性能的综合要求出发,应用根轨迹法来设计合适的系统参数。 

系统开环传递函数 

\[KG_1 (s) = \frac{K}{s (T_1 s + 1) (T_2 s + 1)}\]

显然,系统为I型系统,静态速度误差系数 

\[K_v = K\]

闭环传递函数 

\[\Phi (s) = \frac{K}{s (T_1 s + 1) (T_2 s + 1) + K} = \frac{50K}{s^3 + 15s^2 + 50s + 50K}\]

 \( K \) 的选取,应首先保证闭环系统稳定。由劳斯表: 

\[\begin{array}{ccc} 
s^3 & & 1 & 50 \\ 
s^2 & & 15 & 50K \\ 
s^1 & & 750 - 50K & 0 \\ 
s^0 & & 15 & 0 
\end{array}\]

可知,为确保系统稳定,应有 \( 0 \leq K < 15 \)。

根据系统在斜坡作用下的稳态误差要求,当 \( r(t) = At (A = 1 \mathrm{mm/s}) \), \( R(s) = \frac{A}{s^2} \) 时,稳态误差 

\[\varepsilon_s (\infty) = \frac{A}{K_v} = \frac{1}{K} < 0.1\]

故应取 \( K \geq 10 \)。 

现取 \( K = 10 \),可同时满足系统稳定性及稳态误差要求。为了考查此时系统的动态性能,令 \( K \) 从0到\( \infty \),作系统图似轨迹,如图4-19-1所示。 

\[a_s = \frac{-5 - 10}{3} = 5/3, \quad \varphi_a = \pm 60^\circ, \quad -180^\circ\]

分离点: 

\[\frac{1}{d} + \frac{1}{d + 5} = \frac{1}{100} = 0; \quad d = -2.11\]

116

### Page 69

equation 公式 []".

Figure 4-19-1 激光控制系统的概略根轨迹图

Figure 4-19-2 激光控制系统的根轨迹图

MATLAB 程序：exe419.m
- 系统根轨迹
numc=[1]; denc=[0.02 0.31 0];
rlocus(numc,denc);
- 原系统 % %
- 单位阶跃输入响应
num=[500]; den=[1 15 50 500]; t=0:0.01:15;

 \(k_l^2 = K_d / (2 \sqrt{K_d / S_{0,k_x}})\) 的取值应该：

1. \(k_{o+r}\) 固有振荡频率。
2. 极零点频率。
3. 稳定性要求，包括低频失稳、中高频衰减、饱和。
4. 振动衰减的要求。
5. 超调量计算。
6. 时间常数求解计算。

\end{array}\]

可知,为确保系统稳定,应有 \( 0 \leq K < 15 \)。

根据系统在斜坡作用下的稳态误差要求,当 \( r(t) = At (A = 1 \mathrm{mm/s}) \), \( R(s) = \frac{A}{s^2} \) 时,稳态误差 

\[\varepsilon_s (\infty) = \frac{A}{K_v} = \frac{1}{K} < 0.1\]

故应取 \( K \geq 10 \)。 

现取 \( K = 10 \),可同时满足系统稳定性及稳态误差要求。为了考查此时系统的动态性能,令 \( K \) 从0到\( \infty \),作系统图似轨迹,如图4-19-1所示。 

\[a_s = \frac{-5 - 10}{3} = 5/3, \quad \varphi_a = \pm 60^\circ, \quad -180^\circ\]

分离点: 

\[\frac{1}{d} + \frac{1}{d + 5} = \frac{1}{100} = 0; \quad d = -2.11\]

116

### Page 69

equation 公式 []".

Figure 4-19-1 激光控制系统的概略根轨迹图

Figure 4-19-2 激光控制系统的根轨迹图

MATLAB 程序：exe419.m
- 系统根轨迹
numc=[1]; denc=[0.02 0.31 0];
rlocus(numc,denc);
- 原系统 % %
- 单位阶跃输入响应
num=[500]; den=[1 15 50 500]; t=0:0.01:15;

 \(k_l^2 = K_d / (2 \sqrt{K_d / S_{0,k_x}})\) 的取值应该：

1. \(k_{o+r}\) 固有振荡频率。
2. 极零点频率。
3. 稳定性要求，包括低频失稳、中高频衰减、饱和。
4. 振动衰减的要求。
5. 超调量计算。
6. 时间常数求解计算。
7. 调节时间确定。

\(k_r^2 = K_d / (2 \sqrt{K_d / S_{0,k_x}}), (K_s = (K_d / S_{0,k_x})^2) 确定积分时间常数 (t_{cg}, 截距)。\)
\[ t_{cg} = \left( \frac{ A^H , BH^{ -1} AH }{ -1} \right), (B = K_d / (2 \sqrt K_d S_i).), t_{cg} = \{0^1 0^5\}, |A^i, K_i^2 i_i Z^{-1} \]
\[ t_{cg} = \text{roots}[A^H, B] \].

1. step -\(f_S,T\): develop a larger PI regulator.
2. loop transfer function to find \(Steo\) time to achieve a desired step response.

Jane, p.s.

Page number 122.
August  1999
Auther with copyright

\(s_6)_ S^\alpha \\beta
\end {equation}

\[ K^1 \sign, s \displaystyle 5 \displaystyle \Gamma_0. s. \int,  X
S. \displaystyle, K_s5航历高 }

\) $K_M^{2  -1} s

a

t = 0.0,  urning  和  \step\)너 $0举例 20.7 s-1. \displaystyle Mr.

% 
`.` % ` ) t, '本次 v\% method 阶 rslocus5 1.0

 \[$
 0

% =<
, %
set nds s_index  s,key method
t. 1 = \eq / \zero2 s,  surf

 % elseif 
% s -s0z 地方
\eqspect.,a. = 25 10°8}

В %  1 式中 [,].

 analyse
 основы по, 0. 3. 20% 
set te ) non)

define \eqcentration 13′3=80/`.

% '
》，]
.
礼`\)atan

 end

Matthew};}},

19 \WE."

/% mat._105  %.\); undefined }

8 最后 . [
t-s96′ 0s, }

》

证明材料 和 xtone, I  %

Law \\ ω-Km 10.

MatLab '9_table_prop, line_with ))

], 内 & (95\ 空 \©.)15-s \ {

margin \ 三 < eta &
B &37.

\(+^()

‘± ֵ幅 is

### Page 70

~~~~~~~I.NUFFIX~~~~~~~\)

Figure:
step(num,den,t); grid
% 单位斜坡输入响应
num = [500]; den = [11555000]; t = 0:0.005:5; u = t;
figure;
lsim(num,den,u,t); grid
% 近似系统 %
% 单位阶跃输入响应
wn = 5.98; kos = 0.085;
num = wn^2; den = [1,2*kos*wm,wn^2]; t = 0:0.005:5; u = t;
figure;
lsim(num,den,u,t); grid

图 4-19-3 原系统的单位阶跃响应 (MATLAB)
图 4-19-4 原系统的单位斜坡响应 (MATLAB)
图 4-19-5 近似系统的单位阶跃响应 (MATLAB)
图 4-19-6 近似系统的单位斜坡响应 (MATLAB)

*118*

### Page 71

}der}</mar} 




可见，系统对阶跃输入响应是高度振荡的。因此，在外科手术中，不能采用阶跃信号作为手术指令信号，必须选用低速斜坡信号作为手术指令信号。

4-20 图4-44为空间站示意图。为了有利于产生能量和进行通信，必须保持空间站对太阳和地球的合适指向。空间站的方位控制系统可由带有执行机构和控制器的单位反馈控制系统来表征，其开环传递函数数为\[G(s)=\frac{K^{*}(s+20)}{s(s^2+24s+144)}\]

试画出 \( K^{*} \) 值增大时的系统概略根轨迹图，并求出使系统产生振荡的 \( K^{*} \) 的取值范围。

**图 4-44 空间站示意图**

解 由开环传递函数数 \[G(s)=\frac{K^{*}(s+20)}{s(s^2+12)^2}\]

令 \( K^{*} \) 从 0→∞，可画出系统概略根轨迹如图 4-20-1 所示。图中新近线：\[ \sigma_a = -2, \quad \varphi_a = \pm 90^\circ \]

分离点：\[ \frac{1}{d} + \frac{2}{d+12} = \frac{1}{d+20}, \quad d = -4.75 \]

应用模值条件，可得分离点处的根轨迹增益

\[K_d^{*} = \frac{\prod_{i=1}^{3}(d-p_i)}{\left| d-z \right|} = \frac{4.75 \times 7.25^2}{15.25} = 16.37\]

因此，当 \( K^{*} \) > 16.37 时，系统输出将会产生振荡。

应用 MATLAB 软件包，可得系统的根轨迹如图 4-20-2 所示。若取 \( K^{*} = 10 \)，可得系统的单位阶跃响应，如图 4-20-3 所示。

\* 119 \*

### Page 72

illustrate show or model.

276.

\[\int_{O}^{O}^{+\infty }\frac {1}{r^{2}}.\]

3. 可以运行一些应用程序进行优化模型参数。

### 图4-20-1 空间站方位控制系统概略图

### 图4-20-2
图4-20-1图4-20-2图4-20-2图4-20-2 6. 保证系统的稳定性。使用Lagrange乘数法。当\(\mu =0.707\)，\(\lambda =25\)，\(\zeta =0.3\)，\(\alpha=0.1\)。

6. 本系统的指标灵敏度：\(DQ=2.3145\)，\(Q=0.708\)
6. 故障分布： \(\mu'=0\) 或 \(\delta=0\)、\(\lambda=-0.1\) 或 \(\zeta=0\)。
6. 实际系统状态不能从状态空间描述中直接描述出来。只有系统的由状态空间描述转换为状态空间描述时，才能在状态方程中表示为状态方程。
7. 计算表明，系统的稳定性要大于由本系统状态空间描述。

### 图4-20-3
\[\int_{O}^{O}^{+\infty }\frac {1}{r^{2}}\]

\[K^{*}=10方\] 

图4-20-3信息给出了系统不等式表示，当为均匀查找站时，系统的参数。使用的MATLAB代码为\[，稀疏的线性控制器\]。在原系统指标中，R型、L型系统均存在两段；L型系统下有改进最大取值。
13. 可以是惯性饱和的现象：考虑到目标速率速度散布，每个theta，延时不同。
8. 系统是利用MATLAB的多元函数处理数值计算过程中；

\[\begin{pmatrix}
1\\
\end{pmatrix}\]

### Page 73

. $$图4-45飞机纵向控制系统结构图$()\displaystyle G(s)=\frac{10K_1K_2(s\tau+1)(s+2)^2}{(s+10)^2(s+100)(s^2+2\zeta\omega_ns+\omega_n^2)}$ 代入=0.1,\omega=2.5,\zeta=0.3,有
\\displaystyle G(s)=\frac{K_1K_2(s+2)^2}{(s+10)(s+100)(s^2+0.75\pm j2.38)}$ 令$K^*=K_1K_2$从$0\to\infty$可以绘出系统概略根轨迹如图4-21-1所示。图中
则直线k2。越S散点在( s1与s和d-从s和s1由于 d在的。T散
0)1 和0 b-d = -物流改善系统 \displaystyle K与d_0放(\ c_{α1-c_2}α_2 0。线
	 定d。
 complementary \displaystyle }})\),4,4,4在=L)0 d)S规律等于方程-最终正图和-单态 
K=0
图4-21-1$\displaystyle 1+ \frac{k_1k_2(s+2)^2}{(s+10)(s+100)(s^2+1.5s+6.25)}=0
 线无线A
 $d\ 
图4 \ (无n{联系━{清0q1"<，Zd_linear = ."专业绘通',一期}",4第， }图轨)。}qh)_-如果),求解,
 a2KH\5+b)其他方法α_j证-&开同一方与也可带\((见)); ¯ddd)
OK
平:{ia_{{同步- č**)汪确认 (**"
 +{1栽.{@(%
而题@
finally,}

(%和{] 0亦{
}}退过简连Q, 1^ ⋃証{1n})'0→}

@commo{出
1 _ty;).1 their 1α@] AI引0@)
---
编}义('}日至
“我想取两.
零%尾/, d *%教.:_因此]策

{

### Page 74

zurück.(2) 当 \(K_1 = 0.02\)，中重量巡航时，确定使 \(\zeta_0 = 0.707\) 的 \(K_2\) 值。在根轨迹图上，作 \(\zeta_0 = 0.707\) 阻尼比线，与复根轨迹部分的交叉点为主导极点 \(s_{1,2} = -1.63 \pm j1.63\) 利用模值条件，可以算出 \(s_1\) 处的根轨迹增益 \[\mathbf{K^* = K_1 K_2 = 1430} \] 于是求得 \[\mathbf{K_2 = \frac{K^*}{K_1} = 71500} \] 以上结果如图 4-21-2 所示。（3）当 \(K_1 = 0.2,K_2 = 71500\)，轻重量降落时，确定闭环系统阻尼比 \(\zeta_0\) 因为 \(K^* = K_1 K_2 = 14300\)，则可确定出闭环极点 \(s_{1,2} = -1.96 \pm j0.617\)，\(s_{3,4} = -53.8 \pm j110\) 由于复极点 \(s_{1,2}\) 的位置十分接近重零点 \(z=-2\)，其作用相互削弱，形成近似偶极子，故 \(s_{3,4}\) 变为系统主极极点。因为 \(\beta = \arctan \frac{110}{53.8} = 63.9^\circ\) 所以系统阻尼比 \(\zeta_0 = \cos \beta = 0.439\)。以上结果可参见图 4-21-3。图 4-21-2 中重量巡航时，确定使 \(\zeta_0 = 0.707\) 的增益值（MATLAB）图 4-21-4 系统根轨迹图（MATLAB）图 4-21-3 轻重量降落时，确定闭环系统阻尼比（MATLAB）MATLAB 验证：运行以下 MATLAB 程序，可以得到系统根轨迹图，如图 4-21-4 所示。当 \(K_1 = 0.02\)，中重量巡航时，确定使 \(\zeta_0 = 0.707\) 的 \(K_2\) 值，可参见图 4-21-2；当 \(K_1 = 0.2,K_2 = 71500\)，轻重量降落时，确定闭环系统阻尼比 \(\zeta_0\)，可参见图 4-21-3；还可以得到中重量巡航时的时间响应曲线，如图 4-21-5 所示，以及轻重量降落时的时间响应曲线，如图 4-21-6 所示。图 4-21-5 图 4-21-6 

* 122 *

### Page 75

.(4) 设计指标验证。由于实际系统为无有限零点的三阶系统，负实极点 \( s_3 = - 4.92 \) 会增大系统阻尼，减少超调量。这里仅验验证设计指标中的动态性能。作 MATLAB 程序，可得实际系统的单位阶跃输入响应，如图 4-24-4 所示。

由图 4-24-4 可得系统的动态性能
\[\sigma % = 5\%, \quad t_s = 1.61s \quad (\Delta = 2\%)\]
\[\sigma % = 5\%, \quad t_s = 1.28s \quad (\Delta = 5\%)\]
或
结果满足设计指标要求。

图 4-24-3 控制系统根轨迹图(MATLAB)
\[\begin{array}{l}
G = zpk([-4],[0.3-3j],\quad \text{z=0.6;}) \\
\% 绘制相应系统的根轨迹\\
figure(1) \\
rlocus(G); \quad sgrid(z,'new') \\
axis([-5.50.5-6 6]) \\
\end{array}\]

图 4-24-4 控制系统的单位阶跃响应(MATLAB)
% 取阻尼比为 0.6

\[Ks = 12.5;\]
\[rlocus(G);\]
hold on;
figure(2);
的控制系统的阶跃响应
Ka = 86;
kct = 0.25;
numc = [Ka];
denc = [1 10 21 + Ka*Kt0];
\[% 系统开环传递函数\\
% 系统闭环传递函数\\
% 系统闭环极点
math']['sup':\]
[num,den] = nlq(oprlim(numc,denc); 
roots(den); 
sys = tf(num, den); 
% % % % % % % % > \times.\]
figure(3)
step(sys,t);
grid on;</math']}\]

### Page 76

白话文：

第5章 实时定系统的分析

试确定系统的频率特性。
解 本题可以根据系统的阶跃响应求出系统的传递函数，进而求出系统的频率特性。

对系统单位阶跃响应
\[ c(t) = 1 - 1.8e^{-4t} + 0.8e^{-9t} \]

在零初始状态下进行拉氏变换，得
\[ C(s) = \frac{1}{s} - \frac{1.8}{s+4} = 0.8 + \frac{9s - 1}{s(s+4)(s+9)} \]

由于系统的输入信号为阶跃信号，即 \( R(s) = \frac{1}{s} \)，故系统的传递函数数为
\[ \Phi(s) = \frac{C(s)}{R(s)} = \frac{36}{s(s+4)(s+9)} \]

所以，系统的幅频特性为
\[ M(\omega) = |\Phi(j\omega)| = \frac{36}{\sqrt{16 + \omega^2}}\frac{1}{(81 + \omega^2)} \]

相频特性为
\[ \phi(\omega) = \angle \Phi(j\omega) = \arctan \frac{\omega}{4} - \arctan \frac{\omega}{9} \]

5.3 设系统结构图如图5-61所示，试确定在输入信号
\[ r(t) = \sin(t+30^\circ) - \cos(2t - 45^\circ) \]
作用下，系统的稳定误差 \( e_s(t) \)。

解 本题先根据控制系统的结构图求出系统的误差传递函数，再根据输入信号为正弦信号（余弦信号），利用频率特性的定义，求出系统的稳态误差。

由系统结构图可知，系统的误差传递函数为
\[ \Phi_e (s) = \frac{E(s)}{R(s)} = \frac{s+1}{s+2} \]

则其频率特性为
\[ \Phi_e(j\omega) = \frac{1 + j\omega}{2 + j\omega} = \sqrt{\frac{1+\omega^2}{4 + \omega^2}} e^{j(\arctan\omega - \arctan\omega/2)} \]

由频率特性定义可知，当输入信号 \( r(t) = \sin(t + 30^\circ) - \cos(2t - 45^\circ) \) 时，利用线性系统的可加性，则系统的稳态误差为
\[ e_s(t) = \sqrt{\left( \frac{1+\omega^2}{4+\omega^2} \right)^2 + \left( \frac{\sin t + 30^\circ + \arctan\omega - \arctan \frac{\omega}{2}}{\sqrt{1+\omega^2}} \right)^2 } \]

\[ = 0.632\sin(t + 48.43^\circ) - 0.791\cos(2t - 26.57^\circ) \]

5.4 二阶系统的开环传递函数
\[ G(s) = \frac{\omega_n^2}{s(s+2\xi\omega_n)} \]

当取 \( r(t) = 2\sin t \) 时，系统的稳态输出 \( c_s(t) = 2\sin(t - 45^\circ) \)，试确定系统参数 \( \omega_n, \xi \)。

5-11 控制系统结构图

图 5-61 控制系统结构图

### Page 77

24-hour interval before each (Table 2 p. 138). 

\begin{center}
\section{5}
\end{center}

解 本题主要考查根据频率特性的定义,已知输入为正弦信号时系统的稳态输出,求解系统的参数。注意,系统的稳态输出是指闭环系统的输出,故在求系统稳态输出时,应从系统的闭环传递函数着手。

系统闭环传递函数

\(\Phi(s) = \frac{\omega_n^2}{s^2 + 2\xi\omega_n s + \omega_n^2}\)

则系统的幅频特性为

\(M(\omega) = |\Phi(j\omega)| = \left| \frac{\omega_n^2}{\sqrt{(\omega_n^2-\omega^2)^2 + 4\xi\omega_n\omega^2}} \right|\)

相频特性为

 \(\alpha(\omega) = - \arctan \left| \frac{2\xi\omega_n\omega}{\omega_n^2-\omega^2} \right|\)

由题设条件知,系统稳态输出

\(c_n(t) = 2\sin(t-45^\circ) = 2M(1)\sin[t+\alpha(1)]\)

其中

\(M(1) = \frac{\omega_n^2}{\sqrt{(\omega_n^2-\omega^2)^2 + 4\xi\omega_n^2\,\omega^2}} = \frac{\omega_n^2}{(\omega_n^2-1)^2+4\xi\omega_n^2}\)

\[\alpha(1) = - \arctan \left| \frac{2\xi\omega_n\omega}{\omega_n^2-\omega^2} \right| = - \arctan \left| \frac{2\xi\omega_n\omega}{\omega_n^2-1} \right| = - \arctan \left| \frac{2\xi\omega_n\omega}{\omega_n^2-1} \right| = -45^\circ\]

故有

\[\omega_n^4 = (\omega_n^2-1)^2+4\xi\omega_n^2 \Rightarrow 2\xi\omega_n=0 = \omega_n = \pm j \xi\]

解得

\[\omega_n = 1.847, \xi= 0.653\]

5-5 已知系统开环传递函数

\(G(s)H(s) = \frac{K(\tau s+1)}{s^2 (Ts+1)}, \quad K,\tau,T > 0\)

试分析并绘制 \(\tau>T\) 和 \(T>\tau\) 情况下的幅频开环幅相特性曲线。

解 本题主要考查根据系统参数之间的关系绘制开环幅相特性曲线,掌握系统参数变化对开环幅相特性曲线的影响。

系统的开环频率特性

\[G(j\omega)H(j\omega) = \frac{K(1+j\tau\omega)}{-\omega^2(1+jT\omega)} = \frac{K(1+T\tau\omega^2)}{-\omega^2(1+T^2\omega^2)} -\frac{K(\tau-T)\omega}{(\omega^2(1+T^2\omega^2)}\]

开环幅相特性曲线的起点

\(G(j\omega) + H(j\omega)|_{\omega=0} = \max|G(j\omega)+H(j\omega)|_{\omega=0} = \lim(\lim_{\omega=0}|G(j\omega)+H(j\omega)) \)

K(\pi T\omega\beta) 终点 G(jc1) H(j \omega) 

若 \(\tau>T\), 则 Re[G(j\omega)H(j \omega)]<0, Im[G(j \omega)H(j \omega)]<0,故开环幅相特性曲线位于第

III 象限, 如图 5-5-1 所示, 若 \(\tau< \tau\), 则 Re[G(j\omega)H(j \omega)]<0, Im[G(j \omega)H(j \omega)]>0, 故开环幅相特性曲线位于第II 象限, 如图 5-5-2 所示。

MATLAB 验证: 设K=1, \(\tau=1\),\(\tau=2\),则系统开环幅相特性曲线如图5-5-3所示;设\)

\(K=1,T=2,\tau=1\),则系统开环幅相特性曲线如图5-5-4 所示。

\begin{center}
K_i_y_h_{\f_{ \psi_{h}(二次4^{-8 (\quarii_(\TT-ti_y,\ll_t_i_{\RR}) )}} 
}$\odot$
\end{center}

### Page 78

large vertical新中国晨

图5-5-1

图5-5-2

图5-5-3

图5-5-4

图5-5-5

图5-5-6

\[ G(s)H(s) = \frac{1}{s^2(s+1)(s+2)} \]

式分别绘制 \( \nu=1,2,3,4 \) 时系统的概略开环幅相特性曲线。

解 本题主要考查根据系统不同的型别绘制开环幅相特性曲线的方法，加深了解系统的不同型别对开环幅相曲线的影响。

系统的开环频率特性

\[ G(jω)H(jω) = \frac{1}{(jω)^2(1+jω)(2+jω)} \]

(1) 当 \( ν=1 \) 时

\[\frac{1}{(jω)(1+jω)(2+jω)} = \frac{3}{(1+ω^2)(4+ω^2)} = 3 (1-ω^2)/2](2-ω^2)/ω(1+ω^2)(4+ω^2)\]

开环幅相特性曲线的起点为 \( G(j0_+) = 0 \) , \( G(j0_+) = -90° \) .终点为 \( G(j∞) = 0 \) , \( G(j∞) = -270° \) .

### Page 79

calculates the ratio of the squared norm of the Jacobian matrix of the layer output \(y\) to the squared norm of the Jacobian matrix of the layer input \(x\). This ratio, known as the normalized Jacobian matrix, indicates how strongly the layer's output \(y\) values depend on the input \(x\) values. The formula used is:

\[
\frac{||J_x||||_2}{||J_y||_2} = \frac{\sum_i(w_{yx}^2)^2}{\sum_i(w_{yx}^2) \cdot \sum_i(w_x)^2}
\]

Here, \(||J_x||_2\) and \(||J_y||_2\) represent the squared norm of the Jacobian matrix of the layer output \(x\) and layer input \(y\) respectively. \(w_{yx}\) is the weight matrix for the layer output, and \(w_x\) is the weight matrix for the layer input. The normalization ensures that the variance of the gradient is thrown into the numerator.

This component is crucial for training deep neural networks where the loss function itself often relies on the gradient norms to guide the optimization process.

### Part 2:

From the given expression:
\[
\frac{||J_x||||_2}{||J_y||_2} = \frac{\sum_i(w_{yx}^2)^2}{\sum_i(w_{yx}^2) \cdot \sum_i(w_x)^2}
\]

The path to solving for \(w_{yx}\) is through differentiation. Given \(J_y\) is a matrix valued function, the gradient with respect to each element can be calculated as follows:

\[
\frac{∂J_y}{∂x} = J_{yx}
\]

Since \(J_y\) is column-wise differentiable, we can find its derivative component-wise. For each element \(i\):

\[
\frac{∂J_y}{∂x(i)} = \frac{∂}{\∂x(i)}{∂J_y}{∂x(i)} = J_{yx(i)}
\]

#### Relationship in Context:

1. **Eigenfeature Type in Neural Network**:
   
    - The expression involves the squared absolute value of weighted gradient of the activations of the output layer.
    - The output layer types specified are L-shaped (Sigmoid), FastRCNN (Tanh), and CNN without batch normalization.
2. **Link to Eigenfeature Components**:
    
    - The first section of connections maps the weights wyx onto corresponding eigenfeature components.
    - Resolution: Separated through Cartesian product, each binary typing from a constituent. Notably notable in the case of S-shaped activation, where the mapping becomes finer granularity as it progresses through multiple layers' connections, considering additional higher-numbered components which succeed one another.

This highlights the optimized importance of gradient propagation through hierarchical layers, embedding additional intelligence into the network for better learning dynamics.

### Page 80

representing a sinusoidal wave with amplitude of 1, frequency of 2, and phase angle of pi/2. 




\[ \text{MATLAB 程序: exe506.m} \]

\[ \% \text{确定传递函数的分子系数} \]

num = [1];

\[ \% \text{确定 } v = 1, 2, 3, 4 \text{ 系统传递函数的分母系数} \]

den1 = [1, 3, 2, 0];

den2 = [1, 3, 2, 0, 0];

den3 = [1, 3, 2, 0, 0, 0];

den4 = [1, 3, 2, 0, 0, 0, 0];

\[ \% \text{分别绘制 } v = 1, 2, 3, 4 \text{ 系统的开环幅相曲线} \]

nyquist(num, den1); hold on;

nyquist(num, den2); hold on;

nyquist(num, den3); hold on;

nyquist(num, den4); hold on;

\[ \% \text{确定坐标轴的范围} \]

axis([-0.5 0.5 -0.5 0.5]); hold off;

\[ 5-7 \]

\[ \text{已知系统开环传递函数} \]

\[ G(s) = \frac{K(-T_2 s + 1)}{s(T_1 s + 1)}, \quad K, T_1, T_2 > 0 \]

当取 \( \omega = 1 \) 时，\( \angle G(j\omega) = -180^\circ \)，\( |G(j\omega)| = 0.5 \)。当输入为单位速度信号时，系统稳态误差为0.1，试写出系统开环频率特性表达式。

\[ \text{解} \]

本题主要考查对幅频特性和相频特性定义的理解，并结合系统的稳态误差，求取系统的参数。

\[ \text{系统的开环频率特性} \]

\[ G(j\omega) = \frac{K(1 - jT_2\omega)}{j\omega(1 + jT_1\omega)} = \frac{K\sqrt{1 + T_2^2\omega^2}}{\omega \sqrt{1 + T_1^2\omega^2}}e^{-j(\arctan T_2\omega + 90^\circ + \arctan T_1\omega)} \]

由 \( \omega = 1 \) 时 \( \angle G(j\omega) = -180^\circ \)，可得

\[ \]

\[ \]

\[ \cdot 139 \]

### Page 81

;"></text><text>— arctan$T_2$ — 90° — arctan$T_1$ —— 180°应有</text></svg>

\[\text{arctan}T_1+\text{arctan}T_2=90°\]

等式两端取正切,得</text>

\[\text{tan}[\text{arctan}T_1+\text{arctan}T_2]=\infty\]

根据两角和中的三角函数关系,得</text>

\[\text{tan}(\text{arctan}T_1)+\text{tan}(\text{arctan}T_2)\\ =\frac{\tan(\text{arctan}T_1)\tan(\text{arctan}T_2)}{1-\tan(\text{arctan}T_1)\tan(\text{arctan}T_2)}\]

表明应有</text>

\[1-T_1T_2=0\]

由$\omega=1$时$|G(j\omega)|=0.5$,可得

\[\frac{K\sqrt{1+T_2^2}}{\sqrt{1+T_1^2}}=0.5\]

再由$r(t)=t$时$e_{\text{s}}(∞)=\frac{1}{K}=0.1$,可得</text>

\[K=10\]

于是由上述三个方程,可解得</text>

\[T_1=20,\quad T_2=0.05,\quad K=10\]

故系统的开环频率特性为</text>

\[G(j\omega)=\frac{10(1-j0.05\omega)}{j\omega(1+j20\omega)}=\frac{10\sqrt{1+0.0025\omega^2}}{\omega)\sqrt{1+400\omega^2}}e^{-j(\arctan0.05\omega+90°)+\arctan20\omega)}\]

系统的开环幅相特性曲线如图5-7-1所示。</text><img src="image" alt="">

MATLAB程序:exe507.m</text>

K=10;T1=20;T2=0.05;

G=tf(K*[-T2,1],[T1,1,0]);

nyquist(G);

axis([-3,0,-0.2,0.2]);

5-8 已知系统开环传递函数</text>

\[G(s)H(s)=\frac{10}{s(2s+1)(s^2+0.5s+1)}\]

试分别计算$\omega=0.5$和$\omega=2$时,开环频率特性的幅值$A(\omega)$和相位$\varphi(\omega)$。</text>

解 本题根据幅频特性和相频特性定义来进行计算,以进一步加深对频率特性定义的理解,注意振荡环节的相角计算象限。

系统的开环频率特性</text>

\[G(j\omega)=\frac{10}{j\omega(1+j2\omega)(1-\omega^2+j0.5\omega)}=A(\omega)e^{j\varphi(\omega)}\]

其中</text>

\[A(\omega)=\frac{10}{\omega\sqrt{1+4\omega^2)[(1-\omega^2)^2+0.25\omega^2]}}\]

\[\frac{K\sqrt{1+T_2^2}}{\sqrt{1+T_1^2}}=0.5\]

再由$r(t)=t$时$e_{\text{s}}(∞)=\frac{1}{K}=0.1$,可得</text>

\[K=10\]

于是由上述三个方程,可解得</text>

\[T_1=20,\quad T_2=0.05,\quad K=10\]

故系统的开环频率特性为</text>

\[G(j\omega)=\frac{10(1-j0.05\omega)}{j\omega(1+j20\omega)}=\frac{10\sqrt{1+0.0025\omega^2}}{\omega)\sqrt{1+400\omega^2}}e^{-j(\arctan0.05\omega+90°)+\arctan20\omega)}\]

系统的开环幅相特性曲线如图5-7-1所示。</text><img src="image" alt="">

MATLAB程序:exe507.m</text>

K=10;T1=20;T2=0.05;

G=tf(K*[-T2,1],[T1,1,0]);

nyquist(G);

axis([-3,0,-0.2,0.2]);

5-8 已知系统开环传递函数</text>

\[G(s)H(s)=\frac{10}{s(2s+1)(s^2+0.5s+1)}\]

试分别计算$\omega=0.5$和$\omega=2$时,开环频率特性的幅值$A(\omega)$和相位$\varphi(\omega)$。</text>

解 本题根据幅频特性和相频特性定义来进行计算,以进一步加深对频率特性定义的理解,注意振荡环节的相角计算象限。

系统的开环频率特性</text>

\[G(j\omega)=\frac{10}{j\omega(1+j2\omega)(1-\omega^2+j0.5\omega)}=A(\omega)e^{j\varphi(\omega)}\]

其中</text>

\[A(\omega)=\frac{10}{\omega\sqrt{1+4\omega^2)[(1-\omega^2)^2+0.25\omega^2]}}\]

其中</text>

### Page 82

color match background none defined

铅

167 下 \varphi (\omega) = \left\{ \begin{array}{ll} - 90 ^\circ - \arctan 2\omega - \arctan \frac{0.5\omega }{1 - \omega ^2} , & 0< \omega \leq 1 \\ - 90 ^\circ - \arctan 2\omega - 180 ^\circ + \arctan \frac{0.5\omega }{\omega ^2 - 1} , & \omega > 1 \end{array} \right. \text { 当 } \omega = 0.5 \text{ 时 } \\ A(\omega) = \frac{10}{\omega \sqrt{(1 + 4\omega^2)[(1 - \omega^2)^2 + 0.25\omega^2 ]}} \mid _{\omega = 0.5} = 17.89 \\ \varphi (\omega) = - 90 ^\circ - \arctan 2\omega - \arctan \frac{0.5\omega }{1 - \omega ^2} \mid _{\omega = 0.5} = - 153.43^\circ \text { 当 } \omega = 2 \text{ 时 } \end{array} \]

铅

\left. \begin{array}{ll} A(\omega) = \frac{10}{\omega \sqrt{(1 +4\times\omega^2)((1-\omega^2)^2+0.25\omega^2)}} \mid _{\omega =0.5} = 0.38 \\ \varphi (\omega) = - 90 ^\circ - \arctan 2\omega - 180 ^\circ + \arctan \frac{0.5\omega }{\omega ^2 -1} \mid _{\omega =0.5} = - 327.53^\circ \end{array} \text { 上述计算结果可用 MATLAB 验证,如图 5-8-1 所示。 } \begin{array}{llll} & 50\\ & 40 & & 30 & C- \text {  10 \\ -20 \quad -10 \quad -5 & 0 。 \end{array}\\ 5。 \end{array} \\  \end{array} \\ \text { 图 5-8-1 \quad G (\omega) = \frac{10}{\omega (1 + j2\omega) (1 -\omega ^2 + j0.5\omega )}-} \begin{array}{lll} \} \quad \text{幅相特性曲线（MATLAB）}\\ \end{array} \\ \text { MATLAB 程序：exe508.m } \\ G = tf(10,conv([2,1,0],[1,0,5,1]))
n yquistn (G); \text { axis([-25,2,-50,50]); }\end{array} \\ 5- 9 已知系统开环传递函数
\[ G(s) H(s) = \frac{10}{s (s + 1)(s^2 /4 + 9 + 1)} \]
\text { 试绘制系统的幅 相阶传递曲线。 } 解 本题主要练习含有虚数极点系统的幅相特性的绘制,注意虚数极点对绘制系统幅相曲线的影响。 系统的开环频率特性为
\[ \text { G ( j\omega ) H ( j\omega )  = \frac{10}{ j\omega [(1 + j0.5)\omega = \frac{10}{ j\omega [(1 + j0.5)\omega } }= (j0.5)] = - 327.53}\

### Page 83

.\[-\frac{10}{(1+\omega^{2})(1-\omega^{2}/4)} - j\frac{10}{\omega(1+\omega^{2})(1-\omega^{2}/4)} \]

开环系统有虚数极点 \( s = \pm j2 \), 且 

当 \(\omega = 0^+\) 时，\[ G(j\omega)H(j\omega) = \frac{10}{\omega(1-\omega^{2}/4)\sqrt{(1+\omega^{2})}} |_{ \omega = 0^+}\] \(\longrightarrow \infty \), 且 

\[|G(j\omega)H(j\omega)| = \frac{10}{(1+\omega^{2})(1-\omega^{2}/4)} |_{ \omega = 0^+ }| \]

当 \(\omega \to \infty\) 时, \( |G(j\omega)H(j\omega)| = \frac{10}{\omega(1-\omega^{2}/4)\sqrt{(1+\omega^{2})}} = 0 \), 且 

\[ |G(j\omega)H(j\omega)| = -90^\circ - \arctan \omega |_{ \omega = 0^+} = -90^\circ \]

当 \(\omega \to \infty\) 时, \( |G(j\omega)H(j\omega)| = \frac{10}{\omega(1-\omega^{2}/4)\sqrt{(1+\omega^{2}(1-\omega^{2}))}} = 0 \), 且 

\[ |G(j\omega)H(j\omega)| = 90^\circ - \arctan \omega |_{ \omega = -2} = 153.4^\circ \]

当 \(\omega \to 2^+\) 时, \( |G(j\omega)H(j\omega)| = \frac{10}{\omega(1-\omega^{2}/4)\sqrt{(1+\omega^{2}(1-\omega^{2}))}} = -333.4^\circ \)

系统开环幅相曲线如图5-9-1所示, MATLAB验证结果如图5-9-2所示。

\[\begin{array}{l}
\text{图5-9-1} \quad G(j\omega)H(j\omega) = \frac{10}{(1-j\omega)(1-\omega^{2}/4)} \\
\text{图5-9-2} \quad G(j\omega)H(j\omega) = \frac{10}{j\omega(1+j\omega)(1-\omega^{2}/4)}
\end{array}\]

粗略幅相特性曲线

MATLAB程序:exe509. m

\[ G = \text{tf}(10,[0.25,0.25,1,1,0]); \]

nyquist(G);
axis([-200,20,-20,20]);
5-10 已知系统开环传递函数

\[G(s)H(s) = \frac{s+1}{s\left(\frac{s}{2}+1\right)\left(\frac{s^2}{9}+\frac{s}{3}+1\right)}\]

要求选择频率点,列表计算 \( A(\omega),L(\omega) \) 和 \( \varphi(\omega) \),并据此在半对数坐标纸上绘制系统开环对数频率特性曲线。

### Page 84

.解 本题主要考查根据系统的开环传递函数计算系统开环相频特性、对数幅频特性和相频特性；进而绘制出系统开环对数频率特性曲线。在计算相频特性时，应注意象限问题。

系统的开环频率特性 
\[ G(j\omega) = \frac{1+j\omega}{j\omega(1+j0.5\omega)\left[\left(1-\frac{\omega^{2}}{9}\right)+j\frac{\omega}{3}\right]} = A(\omega)e^{j\varphi(\omega)} \]

其中 
\[ A(\omega)=\frac{\omega_{1}\omega \sqrt{1+\omega^{2}}}{(\sqrt{1+\frac{\omega_{1}^{2}}{4}})\left[\left(1-\frac{\omega_{1}^{2}}{9}\right)+\frac{\omega_{2}}{9}\right]} = A(\omega)e^{j\delta(\omega)} \]

\[\begin{cases}
\arctan \omega - 90^{\circ} - \arctan \frac{\omega_{1}}{2} - \arctan \frac{\frac{\omega}{3}}{1-\frac{\omega_{1}^{2}}{9}}, & 0 < \omega \leq 3 \\
\arctan \omega - 90^{\circ} - \arctan \frac{\omega_{1}}{2} - 180^{\circ} + \arctan \frac{\frac{\omega_{1}^{3}}{3}}{1-\frac{\omega_{1}^{2}}{9}}, & \omega > 3 
\end{cases} \]

\[ L(\omega) = 20gA(\omega) = 10lg(1+\omega^{2}) - 20lg \omega - 10lg\left(1 + \frac{\omega^{2}}{4}\right) - 10lg\left[\left(1-\frac{\omega_{1}^{2}}{9}\right) + \frac{\omega_{2}}{9}\right] \]

令 \(\omega_{1}\) 为不同值，将计算结果列表如下:
\[\begin{array}{c|c|c|c|c|c|c}
\omega/\text{(rad/s)} & 0.1 & 1 & 3 & 5 & 10 & 20 \\
\hline
A(\omega) & 10.04 & 1.33 & 0.59 & 0.16 & 0.019 & 0.0023 \\
\hline
L(\omega)/\text{dB} & 20.03 & 2.48 & -4.58 & -15.92 & -34.42 & -52.77 \\
\hline
\varphi(\omega) / (\circ) & -89 & -92.1 & -164.7 & -216.4 & -246.2 & -258.4 \\
\end{array}\]

由上表可绘制出系统开环对数频率特性曲线，如图 5-10-1 所示.

图 5-10-1

\[G(j\omega) = \frac{1+j\omega}{j\omega(1+j0.5\omega)\left[\left(1-\frac{\omega_{1}^{2}}{9}\right)+\frac{\omega_{2}}{9}\right]}\]

图 5-10-1为对数频率特性(MATLAB)的对数频率特性。

### Page 85

process <return> ====================================================& 插图 &========================== 4486737f 意图说明：以下文件中的内容生成任务的结果如下。输出文件上边为代码，如下部分另存。 ```

G = t f([1,1],conv([0.5,1,0],[1/9,1/3,1]));  
bode(G);grid  
  
5-11 绘制下列传递函数的对数幅频渐近特性曲线：  
  
(1) \( G(s) = \frac{2}{(2s+1)(8s+1)} \)；  
(2) \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)；  
(3) \( G(s) = \frac{8}{0.1} \frac{S+1}{1} \frac{1}{(s^2+S+1)} \)；  
(4) \( G(s) = \frac{10}{400} \frac{S^2}{S+1} \frac{1}{(S+1)} \)。  
  
解 本题主要考查根据系统的传递函数绘制系统对数幅频渐近特性曲线的方法。计算时，注意按大小排列交接频率，并标注斜率交化。  
  
(1) \( G(s) = \frac{2}{(2s+1)(8s+1)} \)。  
① 确定各交接频率 \(\omega_i (i=1,2)\) 及斜率变化值。  
最小相位惯性环节：\(\omega_1 = \frac{1}{8} = 0.125\)，斜率减小 20dB/dec  
最小相位惯性环节：\(\omega_2 = \frac{1}{2} = 0.5\)，斜率减少 20dB/dec  
最小交接频率：\(\omega_{\text{min}} = \omega_1 = \frac{1}{8} = 0.125\)  
  
② 绘制低频段 \(\omega < \omega_{\text{min}}\) 渐近特性曲线。  
因为 \(\omega=0\)，20kgK = 20lg2 = 6.02dB，则低频段渐近线斜率 \(k=0dB/dec\)，并且通过点 \((1,20lg2) = (1,6.02dB)\)。  
  
③ 绘制频段 \(\omega \leq \omega_{\text{min}}\) 渐近特性曲线。  
\( \alpha_{\text{min}} \leq \omega \leq \omega_2 \)，\(k = -20dB/dec\)  
\(\omega \geq \omega_2 \)，\(k = -40dB/dec\)  
  
系统开环对数幅频渐近特性曲线如图 5-11-1 所示。  
  
(2) \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)。  
① 确定各交接频率 \(\omega_i (i=1,2)\) 及斜率变化值。  
最小相位惯性环节： \(\omega_1 = 0.1\)，斜率减小 20dB/dec  
最小相位惯性环节： \(\omega_2 = 1\)，斜率减小 20dB/dec  
最小交接频率： \(\omega_{\text{min}} = \omega_1 = 0.1\)  
  
② 绘制低频段 \(\omega < \omega_{\text{min}}\) 渐近特性曲线。因为 \(\omega=2\)，20kgK = 20lg200 = 46.02dB，则低频段渐近线斜率 \(k = -40dB/dec\)，并且通过点 \((1,20lg200) = (1,46.02dB)\)。  
  
③ 绘制频段 \(\omega \leq \omega_{\text{min}}\) 渐近特性曲线。  
\( \omega_{\text{min}} \leq \omega \leq \omega_2 \)，\(k = -60dB/dec\)  
\(\omega \geq \omega_2 \)，\(k = -80dB/dec\)  
  
系统开环对数幅频渐近特性曲线如图 5-11-2 所示。

### Page 86

represents a percentage

图5-11-1 \( G(s) = \frac{2}{(2s+1)(8s+1)} \)
图5-11-2 \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)
图5-11-3 \( G(s) = \frac{8\left(\frac{s}{0.1}+1\right)}{s(s^2+s+1)\left(\frac{s}{2}+1\right)} \)

① 确定各交接频率 \( \omega_i (i=1,2,3) \) 及斜率变化值

最小相位一阶微分环节： \( \omega_1 = 0.1 \)，斜率增加20dB/dec

最小相位振荡环节： \( \omega_2 = 1 \)，斜率减小40dB/dec

最小相位惯性环节： \( \omega_3 = 2 \)，斜率减小20dB/dec

最小交接频率： \( \omega_{\text{min}} = \omega_1 = 0.1 \)

② 绘制低频段 \( \omega < \omega_{\text{min}} \) 渐近特性曲线，因为 \( \nu = 1，20\lg K = 20\lg 8 = 18.06 \ dB \)，则低频段渐近线斜率 \( k = -20 \text{dB/dec} \)，并且通过点 \( (1,20\lg 8) = (1,18.06 \ dB) \)

③ 绘制频段 \( \omega \gg \omega_{\text{min}} \) 渐近特性曲线。

\[ \omega_{\text{min}} \le \omega < \omega_2, \quad k = 0 \ dB/dec \]

\[ \omega_2 \le \omega < \omega_3, \quad k = -40 \ dB/dec \]

\[ \omega \ge \omega_3, \quad k = -60 \ dB/dec \]

系统开环对数幅频渐近特性曲线如图5-11-3所示。

④ 绘制频段 \( \omega > \omega_{\text{min}} \) 渐近特性曲线。

\[ \omega_{\text{min}} \le \omega < \omega_2, \quad k = 0 \ dB/dec \]

\[ \omega_2 \le \omega < \omega_3, \quad k = -40 \ dB/dec \]

\[ \omega \ge \omega_3, \quad k = -60 \ dB/dec \]

系统开环对数幅频系统开环对数幅频系统的波特图系统顺特性曲体的波特图如图5-11-3所示。

\( \)系统开环对数频带近似特性曲线如图5-11-3所示。系统近似曲线如图5-11-3所示。系统近似曲线如图5-11-3所示。
系统近似曲线如图5-11-3所示。系统近似曲线如图5-11-3所示。
(4) \( G(s) = \frac{10}{\omega} + \frac{s}{10} + 1 \)
\( (4) G(s) = \frac{10}{\omega} + \frac{s}{10} + 1 \)

图5-11-2 \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)
图5-11-3 \( G(s) = \frac{8\left(\frac{s}{0.1}+1\right)}{s(s^2+s+1)\left(\frac{s}{2}+1\right)} \)

Ⅰ） 确定各交接频率 \( \omega_i (i=1,2,3) \) 及斜率变化值。

最小相位一阶微分环节； \( \omega_1 = 1 \)，斜率减少20dB/dec

最小相位振荡环节； \( \omega_2 = 1 \)，斜率减小20dB/dec

最小相位惯性环节； \( \omega_3 = 6 \)，斜率增加40dB/dec

最小交接频率； \( \omega_{\text{min}} = \omega_1 = 1 \)

ⅠⅡ 图5-11-2 \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)
图5-11-2 \( G(s) = \frac{200}{s^2(s+1)(10s+1)} \)

### Page 87

.极点的个数,进而判别闭环系统的稳定性,特别要注意对含有积分环节开环幅相曲线的处理。

(1) 对于题 5-5 中的系统。分别以 \(\tau >T\) 和 \(T >\tau\) 两种情况下讨论系统闭环稳定性。
当 \(\tau >T\) 时,其幅带开环幅相曲线如图 5-13-1 所示。因为 \(v=2\) ,从开环幅相曲线上
\(\omega = 0^+\) 的对应点起逆时针补作180^\( B \) 半径,无穷大的虚圆弧。
由于 \(G(s)\) 在 \(s\) 右半平面的极点数 \(P=0\) ,且由开环幅相曲线知 \(N_0=0,N_+ = 0,\) 故
\[N = N_+ -N_- = 0\]

由奈氏判据,算得 \(s\) 右半平面的闭环极点数为 \(Z = P - 2N = 0\);所以系统閉环不稳定。

当 \(T> \tau\) 时,其幅带开环幅相曲线如图 5-13-2 所示。因为 \(v=2\) ,从开环幅相曲线上
\(\omega = 0^+\) 的对应点起逆时针补作180^\( B \) 半径,无穷大的虚圆弧。
由于 \(G(s)\) 在 \(s\) 右半平面的极点数 \(P=0.\) 且由开环幅相曲线知 \(N_0 = 1,N_+ = 0,\) 故
\[N = N_+ -N_- = 1\]

由奈氏判据,算得 \(s\) 右半平面的闭环极点数为 \(Z = P-2N=2,\) 所以系統闭环不稳定。

图 5-13-1 题 5-5 中
\(T >T\) 时图绕开环

图 5-13-2 题 5-5 中 \(\tau T\)时称开环
幅相特性曲线

图 5-13-3 题 5-6 中幅带开环幅相特性曲线

(2) 对于题 5-6 中的系统。其幅带开环幅相特性曲线如图 5-13~3 所示。

图 5-13-3 题 5-6 中幅带开环幅相特性曲线

1 当 \(v=1\) ,从开环幅相特性曲线上 \(\omega =0^+\) 的对应点起逆时针补作 90^\( B \) 半径为无穷大的虚圆弧。由于 \(G(s)\) 在 \(s\) 右半平面的极点数 \(\displaystyle(P = 0 \) 且由开环幅相曲线知
\[N_0 = 0,N_+ =0,\]

\[N = N_+ -N_- = 0\]

由奈氏判据,算得 \(s\) 右半平面的闭环极点数为 \(Z = P - 2N = 0,\) 所以系統闭环稳定。

2 当 \(v = 2,\) 从开环幅相特性曲线上 \(\omega = 0^+\) 的对应点起逆时针补作 180^\( B \) 半径,无穷大的虚圆弧。由于 \(G(s)\) 在 \(s\) 右半平面的极点数的大数为 \((P = 2 N = 2,\) 所以系統闭环不稳定。

图 5-13-3 题 5-6 中幅带开环幅相特性曲线

文献:图5-13-1中开环幅相曲线为站在Q轴上,图5-13-2 图5-13-3 中 \(N_+ = 0, N_= 1,\)
为站在P轴上,图5-13-3 中左半平面的闭环极点为 \(Z = P - 2N = 2,\) 所以系統闭环不稳定。

### Page 88

completing square, finding the discriminant, factorizing ax + bx + c, completing the square, quadratic formula, graphing parabola, properties of parabola, reflections, translations, and dilation, finding asymptotes or x and y  

# Multiplication Exercises

\(N = N_{+} - N_{-} = -1\)

应用奈氏判据, 计算 \(s\) 右半平面的闭环极点为

\(Z = P - 2N = 2\)

所以系统闭环不稳定, 有两个正实部闭环极点。

\((2) G(s) = \frac{K}{s(T_{1}s + 1)(T_{2}s + 1)}\)

因为 \(\nu = 1\), 从奈氏曲线上 \(\omega = 0^{+}\) 的对应点 \(T\) 起逆时针作为 90° 且半径为无穷大的虚圆弧。

由于 \(G(s)\) 在 \(s\) 右半平面的极点数为 \(P = 0\)，由奈氏曲线知 \(N_{-} = 0，N_{+} = 0\)，故

\(N = N_{+} - N_{-} = 0\)

应用奈氏判据, 计算 \(s\) 右半平面的闭环极点为

\(Z = P - 2N = 0\)

所以系统闭环稳定。

\((3) G(s) = \frac{K}{s^{2}(T_{3}s + 1)}\)

因为 \(\nu = 2\), 从奈氏曲线上 \(\omega = 0^{+}\) 的对应点 \(T\) 起逆时针作为 180° 且半径为无穷大的虚圆。

由于 \(G(s)\) 在 \(s\) 右半平面的极点数为 \(P = 0\)，由奈氏曲线知 \(N_{-} = 1，N_{+} = 0\)，故

\(N = N_{+} - N_{-} = -1\)

应用奈氏判据, 计算 \(s\) 右半平面的闭环极点为

\(Z = P - 2N = 0 - 2 \times (-1) = 2\)

所以系统闭环不稳定, 有两个正实部闭环极点。

\((4) G(s) = \frac{K(T_{1}s + 1)}{s^{2}(T_{2}s + 1)}\)

因为 \(\nu = 2\)，从奈氏曲线上 \(\omega = 0^{+}\) 的对应点 \(T\) 起逆时针作为 180° 且半径为无穷大的虚圆。

由于 \(G(s)\) 在 \(s\) 右半平面的极点数为 \(P = 0\)，由奈氏曲线知 \(N_{-} = 0，N_{+} = 0\)，故

\(N = N_{+} - N_{-} = 0\)

应用奈氏判据, 计算 \(s\) 右半平面的闭环极点为

\(Z = P - 2N = 0 - 2 \times (-1) = 2\)

所以系统闭环稳定。

\((5) G(s) = \frac{K}{s^{3}}\)

因为 \(\nu = 3\)，从奈氏曲线上 \(\omega = 0^{+}\) 的对应点 \(T\) 起逆时针作为 270° 且半径为无穷大的虚圆。

由于 \(G(s)\) 在 \(s\) 右半平面的极点数为 \(P = 0\)，由奈氏曲线知 \(N_{-} = 1，N_{+} = 0\)，故

\(N = N_{+} - N_{-} = 1\)

应用奈氏判据, 计算 \(s\) 右半平面的闭环极点为

\(Z = P - 2N = 2\)

所以系统闭环稳定, 有两个正实部闭环极点。

\((6) G(s) = \frac{K(T_{1}s + 1)(T_{2}s + 1)}{s^{3}}\)

因为 \(\nu = 3\)，从奈氏曲线上 \(\omega = 0^{+}\) 的对应点 \(T\) 起逆时针作为 270° 且半径为无穷大的虚圆。

由于 \(G(s)\) 在 \(s\) 右半平面的极点数为 \(P = 0\)，由奈氏曲线知 \(N_{-} = 1，N_{+} = 1\)，故

\* 154 \*

### Page 90

"></p>

### Page 91

;"></p><p>图5-17-1 题5-10的开环对数频率特性(MATLAB)</p><p>系统开环传递函数</p><p>\[ G(s)H(s)=\frac{(s+1)}{s\left(\frac{s}{2}+1\right)\left(\frac{s^2}{9}+\frac{s}{3}+1\right)} \]</p><p>系统开环对数频率特性曲线如图5-17-1所示。</p><p>因为 \(\nu=1\)，故需要在对数相频特性的低频段曲线上补作 \(1\times90^{\circ}\)的垂线；系统的全部开环极点都位于 \(s\) 左半平面，即 \(P=0\)。</p><p>在 \(L(\omega)>0\) 的频段内，其对数相频曲线没有穿越（\(2k+1\))\(\times100^{\circ}\)线，故 \(N_{-}=0\)， \(N_{+}=0\)，则 \(N=N_{+}-N_{-}=0\);于是闭环极点位于 \(s\) 右半平面的个数为</p><p>\[ Z=P-2N=0 \]</p><p>所以系统闭环稳定。</p><p>又解：在题5-10中的开环对数频率特性曲线MATLAB仿真结果中，易得开环截止频率 \(\omega_{\mathrm{c}}=1.7\mathrm{rad/s}\)，相角裕度 \(\gamma=69.4^{\circ}\)，故闭环系统稳定。作为一种验证，下面给出该系统的单位阶跃响应曲线，如图5-17-2所示。</p><p>MATLAB程序：exe517.m</p><p>G= tf([1,1],conv([0.5,1,0],[1/9,1/3,1])); [Gm,Pm,wx,wc]=margin(G); G1 = feedback(G,1); step(G1);grid</p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /p>  Fig5-17-1]](< /fig/ ></p><p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /fig/ ></p><p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /fig/ ></p><p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /fig/ ></p><p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /fig/ ></p><p>![图5-17-2 题5-10系统的单位阶跃响应(MATLAB) 系统开环传递函数 * 确定系统的开环截止频率和相角裕度 * 系统的闭环传递函数 159](< /fig/ ></p>]] (

### Page 92

approximated as \(\omega_c = 2\) and \(\omega_c = 0\), with the actual value of \(K\) remaining constant. The paper highlights how this cross-given stability framework can be utilized to enhance stability and performance in control applications without sacrificing the advantages of both methods.

### Page 93

calculates the first derivative of the O(omega function). The calculated value is used to determine the margin error across the simulation area. Whether the error is within the margin is based on previous margin calibration against noise or sampling noise. If the error is less than the margin, the simulation results are accurate; the simulation results are not within the margin, and if it exceeds the margin, the simulation results are considered to be invalid.

职场环境下，你的工作是否具有成就感？**G(i,j,pot)**, Potentials that need to be used to solve this function

JEDEC is measured using it.

Boards should check that measured**unanalysed**FPA QR is diagonal**and**marked with a BN# symbol. R16-1640 uses a GC MX685 MatrixALU containing **1 MB of useful memory.** The example involves JEDEC **at** f32(I,J) and FPAiax(@) J=MAX(MON) with J=MAX(EQUAL) or J=1I while Z=X-E when I=1 and J=C when I=2) automatically covers I-J averaging for FPA by J=x+1+(C- ) and E-).

Calendar 18/21: The example shows that using 128,256, and 256.8640 incorporate generated graphs.近似or estimate approximation.

%Not sure whether to output J=1I or J=1J.

The example shows that J=1I uses only, but J=D AND gives dividing points, rectangles, picture distribution using FPA. Hence, unless FPS=1, use J=D.

>> matlab

Version using

>> %if not already installed no add_na-palette file.

|[A][I][C][MA].[MA]


R16-079

Matlab Image 2023

Content is not guaranteeing quality by numerical technique.

### Page 94

}}}</script>

若对于 \(0 \le q \le k\)，bookgraph估计为

\[G(m) \approx q(m)\]

### Page 95

.试确定相角裕度为 45°时参数 \(a\) 的值。 解 本题主要考查对系统相角裕度定义的理解,并要注意与相角裕度相关的截止频率的定义。 系统的开环频率特性 \[G(j\omega) = \frac{1 + ja\omega}{\omega^2} = \frac{\sqrt{1+a^2\omega^2}}{\omega^2}e^{-j(\pi-\arctan{\omega})}\] 其中 \(\varphi(\omega) = -\pi + \arctan{\omega}\)。由相角裕度定义可知 \[ \gamma = \pi + \varphi(\omega) = \arctan{\omega_c} = \frac{\pi}{4} \] 解得 \(\omega_c = \frac{1}{4}/a\) 而 \[ |G(j\omega_c)| = \frac{\sqrt{1+a^2\omega_c^2}}{\omega_c^2} \bigg |_{\omega_c = 1/a}=1 \] 解得 \(a=0.841，\omega_c=1.189\) MATLAB验证：由于环对数频率特性图 5-21-1，可以测得 \(\omega_c=1.19 \text{rad / s}, \gamma=45^\circ\)

\[\begin{array}{c}
 \\
\text{GM=Inf,Pm=45deg(att 1.19rad/sec)}
\end{array}\]

图5-21-1 \({G(j\omega)=\frac{1+ja\omega}{\omega^{2}}}\)在\(\alpha=0.841\)时的开环对数频率特性(MATLAB) MATLAB 程序：exe521.m \(\alpha=0.841\); \(\text{G=tf([a,1],[1,0,0])}\); \(\text{margin(G);grid}\)

5-22 对于典型二阶系统,已知参数 \(\omega_n=3,\zeta=0.7\),试确定截止频率、和相角裕度\(\gamma\)。

解 本题主要考查如何根据典型二阶系统的参数来求取其频域指标。

典型二阶系统的开环传递函数为 \[ G(s) = \frac{\omega_n^2}{s(s+2\zeta\omega_n)}\] 代入参数 \(\omega_n=3,\zeta=0.7\)，得

\[\cdots \cdots 163 \]

### Page 96

bladder.[/5898655/text/10556818]

\[\text{G}(s) = \frac{9}{s(s+4.2)}\]

二阶系统的开环频率特性

\[G(j\omega) = \frac{9}{j\omega(4.2 + j\omega)} = \frac{9}{\omega \sqrt{17.64 + \omega^2}} e^{-j(\frac{\pi}{2} + \arctan \frac{\omega}{\sqrt{17.64}})} \]

由 \(|G(j\omega_c)| = 1\)，即

\[\frac{9}{\omega_c \sqrt{17.64 + \omega_c^2}} = 1 \]

解得 \(\omega_c = 1.94\text{rad/s}\)。

再由 

\[\gamma = 180^\circ + \varphi(\omega_c) = 180^\circ - 90^\circ - \arctan \omega_c / 4.2 \]

解得 \(\gamma = 65.21^\circ\)。

MATLAB验证:利用MATLAB软件包,绘制系统开环对数频率特性,如图5-22-1所示。由图5-22-1测得 \(\omega_c = 1.94\text{rad/s}, \gamma = 65.2^\circ\)。

图5-22-1 \(G(j\omega) = \frac{9}{j\omega(4.2 + j\omega)} \) 的开环对数频率特性 (MATLAB)

MATLAB程序:exe522.m

确定系统参数

\[\omega n = 3; keth = 0.7;\]

确定典型二阶系统的传递函数

\[G = tf([wnr2],conv([1,0],[1,2*keth * wn]));

margin(G);grid\]

5-23 对于典型二阶系统,已知 \(\sigma \% = 15\%, t_s = 3\s(\Delta = 2\%), \)试计算相角裕度 \(\gamma\)。

解 本题主要考查如何根据典型二阶系统的时域指标来求取其频域指标,要注意典型二阶系统时域指标和频域指标之间的关系。

典型二阶系统的开环传递函数为

\[G(s) = \frac{\omega_n^2}{s(s+2\omega_n)} \]

由 \(\sigma \% = 15\%, t_s = 3\s(\Delta = 2\%) \)，即

### Page 97

4.logistic田径运动图示警60000υ(图29-15)图29-40.017种频速 0umlor...

十七页- visual 24个字 令

第七十六页- visual中文

图254。冷 4.049pv× - 两种关联度 20logQ/dB .40-17° 

图二

图七十九页- visual 黑

图四十七页 - visual帮助

图三十四页- - visual 图片

第四次way- visual 备五页 17页
7choice { 站页- visual 备份

页码 21页-visual做两
Page 作为那个样
Page 在类源中使用

一页
次一页,为
一

36页->:视觉安全
扫描检测
(.5 外)

259-2552类似

— 27204页视觉侧。

Page 在2002 页或条更新
uda射线 。

图259-2552页

cba比较特页面会对ове
扩散长安5.1- 格 等请再种

数学图

第五章 章项企设是这样图,在此基础上附加0结尾的段的内容

H兆华职T内在德尔诺进行相克项条,同时内及将要画个段落大图

二237786

REFERENCES (页码 

图141必

可用Thay
is11-15,

9.489 0
199 subscribe

0 mN 
G的值步骤图 P7-1

see P97

图5-31
B附

45页

d

图48-281页情境

机器人固模

品和纬 球可

V观

图 乙-

72-79

二 尼
75-8.

10x

数 ，投超,

-25

格g=、

048

均给予6个数的room)

N

检

图35-67~1第 图4

8

MV。

G.4第1497 
14-6页7第三图d

---
(铺域-若7-

---向58,

当5

2期59-砂.

引18-5.

70学，中期将图233

-设备适
智200 I(第5

-376近

度，

(图

 excel时

解- 159-第187页论文

堆
的0些文章的,847

272-58 页当.137,

示的

据性(页）

页参的图如般，章有

-0页第 
一)

题

(隐卷(2

-25

作论C优和H搜显示A merc2

书F

-1151

(距:315开度)

代{,
(页约8

00810
第自92
, 1 第(j 法定1-页17
()
作。式示2.
。(

在校势

专题皎阶段 //
的项规于

2017-150第

-114

显示(t-

14页(0 )
,39→备

X-
用于.页
某于共.比较系全可选对

(符号)(

新分润劳,英寸组组及
同赶强统计
.-

约翰 7)
16
-相关项

128722
告广种对页还著

度.

其中.
g17:*

### Page 98

.% figure
keth = sin(atan(- log(data)/pi)); wm = 4.4/(19\*keth);  % 确定参数  \omega_{-} 、\zeta 值
G = tf([wm^2],conv(1,0,[1,2\*keth*wm]));
figure(1);
margin(G);
G1 = feedback(G,1);
figure(2);
step(G1);

5-24 根据题5-11所给对数幅频渐近特性曲线, 近似确定截止频率 \omega_{-} ,并由此确定相角裕度  \gamma 的近似值。

解 本题主要考查如何根据系统的对数幅频渐近特性曲线确定截止频率，进而确定相角裕度。

(1) \(G(s) = \dfrac{2}{(2s+1)(8s+1)}\)

由图5-11-1对数幅频渐近特性曲线，并根据其几何性质,可得到
\[ 20\lg 2 = 20\lg \dfrac{\omega_{-}}{1/8} \]
解得 \(\omega_{-}=0.25\ \text{rad/s}\)。再由
\[ \gamma = 180 \degree - \arctan 2\omega_{-} - \arctan 8\omega_{-} \]
解得 \(\gamma = 90 \degree\)。

MATLAB 验证：
由开环对数频率特性的仿真结果，可以测得 \(\omega_{-}=0.196\ \text{rad/s}\), \(\gamma=101\degree\)，如图5-24-1所示。

\[ 20\lg 2/(2s+1)=20\lg G(j\omega) \quad 2\omega_{-} \quad 20\lg G(j\omega) \]

[] Figure 5-24-1 \(G(s) = \dfrac{2}{(2s+1)(8s+1)}\) 的开环对数频率特性 (MATLAB) 
其极限对数频率特性 (MATLAB)

图 5-24-1 的开环对数频率特性 (MATLAB)

(2) \(G(s) = \dfrac{200}{s^2(s+1)(10s+1)}\)
由图5-11-2对数幅频渐近特性曲线，并根据其几何性质,可以得到
\[ 20\lg 200 +40\lg \dfrac{1}{1/10} -60\lg \dfrac{1}{10} = 80\lg \dfrac{\omega_{-}}{1} \]
解得 \(\omega_{-}=2.115\ \text{rad/s}\)。再由
\[ \gamma = 180 \degree - 180 \degree - \arctan \omega_{-} - \arctan 10\omega_{-} \]

[] Figure 5-24-2 \(G(s) = \dfrac{200}{s^2(s+1)(10s+1)}\) 的开环对数频率特性 (MATLAB)

其极限对数频率特性 (MATLAB)

### Page 99

}}\\]]]]}}}}}}}}}}supplement page:125-85}136-85}137-95}136-95}137-95} 200{20g }\\ 150 p(s1) 40 \\s 100 Ps-5 50-5\\ 40 30-5\\ O-5\\ \\ 30 20\\ X 10\\ \30\\ 20\\ 10\\ \\ 10-5\\ \\20\\ \ 10 10 \\ x 0\\ 10 50 \\x\\ LS 10\\ x\\ 50\\ \ x\\ \ x\\ \\ 10\\ 50\\ \\-5\\ x\\ \\ 50\\ k1 \\ k3O-50\\ x\\ 50\\ \\ 1) k3O-5\\ \\x \&\\ x U\R\\ 0-5\\ 2-5\\ \\&\\\\0.5-5\\ k 2\\ \\k3Z\\ k3Z\\ L2\\ \\R\\X0-5\\ Z1\\ k3\\ k3Z\\ \\20\\ k3Z\\ k3\\ \\ \\0-5\\ DE000200-0-5-50\\ 1.5\\ -1650\\ -10\\ -1-\\n-3500-1-400-150 1-2-400-1.5\\ SLRd-5-8-5 EXE\\ \\ \\0-5-\\a\\c--400\\ \\ 2-6\\ k3\\ \\ \\\\ \\\\ \\\\ \\0.5 \\ 1-2 \\ k3X \\ CL-1.5\\ EXE \\ \\0.5 \\ \\ \ \\\\ \\\\\\\\0.5 \\ \\ 1.5\\ EXE \\ \\ \\ 1.5 \\ 10-5\\ \\ \\1.5 \\ EXE \\ \\ 1.5 \\ \\ X \\ 10-5\\ \\2.5 \\ \\ 1\\\\ 1.5 \\ EXE //\\ EXE \\ \\ \\EXE \\ \\ EXE \\ \\ \\\\\\ EXE \\ \\ \\X\\ 2.5\\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ 1.5\\ EXE \\ \\ \\\\ \\ \\ \\ EXE \\ \\ EXE \\ \\ EXE \\ \\ EXE \\ \\ EXE \\ \\ EXE \\ EXE \\ EXE \\ \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ \\ \\EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ EXE \\ 这些东西\\ \\所以你去基\\ \\1_-5\\ X\\ EXE \\ EXE911; 你想要\\ \\ \\\\\\ \\\\\\ \\\\\\ \\ \\ \\ \\ \\ \\ x A b;\\\E E Ex/e= 4Ax\\ \\\\ 对于很远的宫\\ \\\\\\ R|\\\\ Ex\\  \\\\h(x\\ \\ \\\\ \\halex.\\\\\\\\\\ \\ \\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\ \\\\\\ \\\\\\ \\\\\\ \\\\\\ \\\\\\x q A k4;\\ EXE0.51200,159000\\15 40\

2000k8EXE\\ \\ 200\\ \\ 2000k8\\ \\ 150\\ \\ \\ \\ಾಷರRigAj.Kg-57 - 000.21

知中

http://axur.dp.terms.cc/acs1-dss

修正[/100.200.000-）

2000k8Dks -2.8h

DC4

# 导出节点

图 5-25-1 船舶航向控制系统开环对数频率特性(MATLAB)

应用MATLAB软件包,可得开环对数频率特性,如图5-25-1所示。 

MATLAB程序: exe525.m 

num = 0.164 * [conv([1,0.2],[-1,0.32])]; 

den = [conv(conv([1,0.0],[1,0.25]),[1,-0.009])]; 

G = tf(num,den); 

bode(G);grid

5-26 航天飞机曾成功地完成了检修卫星和哈勃太空望远镜的任务。图5-66(a)是卫星修理示意图,宇航员的脚固定在机械手臂顶端的工作台上,以便他能用双手来完成阻止卫星转动和点火启动卫星等操作。机械臂控制系统如图5-66(b)所示,其中 
\[G_1(s) = K = 10, \quad H(s) = 1 \]

(a) 卫星修理

(b) 机械臂控制系统框图

图 5-66 航天飞机机械臂控制系统

若已知闭环传递函数为 

\[\Phi(s) = \frac{C(s)}{R(s)} = \frac{10}{s^2 + 5s + 10} \]

要求:

(1) 确定系统对单位阶跃扰动的响应式表达式 \( c_n(t) 及 c_n(∞) \)的值; 

(2) 计算闭环系统的带宽频率 \(\omega_b\).

解 本题联合应用系统的时域及频域分析方法,分别确定系统的扰动时间响应及系统带宽。

### Page 100

console input of MAT
晶体频率

| 典型环节    | 转换率  | 斜率变化    | 相角变化    |
|---|---|---|---|
| \( \frac{1}{s} \)    | \( \omega_1 = 0.5 \)    | 0      | \( 0^\circ \)    |
|    |    | -20dB/dec    | -90^\circ    |
| \( \frac{1}{2s+1} \) | \( \omega_2 = 2 \)    | -20dB/dec    | \( \varphi_1 (\omega) = 0^\circ \sim -90^\circ \)    |
| \( 0.5s+1 \)    | \( \omega_3 = 8 \)    | -20dB/dec    | \( \varphi_2 (\omega) = 0^\circ \sim 90^\circ \)    |
| \( \frac{1}{\left( \frac{s}{8} \right)^2 + 2 \times 0.2 \left( \frac{s}{8} \right) + 1} \) |    | -20dB/dec    | \( \varphi_3 (\omega) = 0^\circ \sim -180^\circ \)    |

图5-27-1  

\[G(s) = \frac{4(0.5s+1)}{s(2s+1)(s^2/64+s/20+1)} \]

图5-27-1  展示的是MATLAB计算得到的开环对数频率特性曲线(MATLAB) \(\omega/krad/s\):

(2) 截止频率与穿越频率。由已给出的开环准确Bode图5-27-1可得: 截止频率 \(\omega_c = 1.6rad/s\) , 穿越频率 \(\omega_r = 7.7rad/s\)。

MATLAB程序:exe527.m 

\[G = tf(4*[0.5,1],[conv(conv([1,0],[2,1]),[1/64,1/20,1]])),\]

\[bode(G);grid\] 

5-28 在空问机器人与地面测控站之间,存在着较大的通信时延。因此,对火星一类的远距离行星进行星际探索时,要求空间机器人有较高的自主性。空间机器人的自主性要求将影响整个系统的各个方面,包括任务规划,感知系统和机械结构等。只有当每个机器人都配备了完备的感知系统,能可靠地构建并抽象环境和模型时,星际探索系统才能具备所需的自主性。美国卡内基-梅隆大学机器人研究所开发研制了一套用于星际探索的系统,其目标机器人是一个六足步行机器人,如图5-68(a)所示。该机器八单足控制系统结构图如图5-68(b)所示。

图5-68  平面行走机器人

(a) 六足步行机器人 
(b) 机器人单足控制系统结构图

图5-68  图5-67 的MATLAB计算得到对数相频特性曲线 (MATLAB)
173

### Page 101

}409</table>

\[\begin{align*}
& \text{要求:} \\
& (1) \text{绘制} K=20 \text{时,闭环系统的对数频率特性;} \\
& (2) \text{分别确定} K=20 \text{和} K=40 \text{时,闭环系统的谐振峰值} M_r \text{, 谐振频率} \omega_r \text{和带宽频率} \omega_b。 \\
& \text{解 本题展示在频域中进行空间机器人控制系统参数的设计过程。确定不同增益取值时的系统的频域特征参数,为进一步设计控制系统参数提供必备的技术数据。}
\end{align*}\]

\[\begin{align*}
& \text{(1) } K=20 \text{时的闭环系统 Bode 图。开环传递函数} \\
& G_c(s)G_a(s)=\frac{20(s+1)}{s(s+5)(s^2+2s+10)}\\
& \text{闭环传递函数} \\
& \Phi(s)=\frac{20(s+1)}{s(s+5)(s^2+2s+10)+20(s+1)}=\frac{20(s+1)}{s^4+7s^3+20s^2+70s+20}
\end{align*}\]

应用 MATLAB 软件包, 可得闭环系统对数频率特性如图 5-28-1 所示。

(2) 确定谐振峰值 M_r, 谐振频率 \(\omega_r\) 和带宽频率 \(\omega_b\)。 令 \(K=20\), 由图 5-28-1 可得: 谐振峰值 \(M_r=0\); 谐振频率 \(\omega_r\) 不存在; 在 \(20lg|\Phi(j\omega)|=-3dB\) 处, 查出带宽频率 \(\omega_b=3.62rad/s\)。

\[\text{令 } K=40, \text{因为}\]

\[20lg40-20lg20=6dB\]

故可将图 5-28-1 中 \(20lg|\Phi(j\omega)|\) 向上平移 6dB, 可得

\[\begin{align*}
& \text{图 5-28-1 单足机器人控制系统闭环} \\
\end{align*}\]

\[Bode 图(K=20, MATLAB)\]

\[\begin{align*}
& M_r(dB)=9.4dB, \quad M_r=2.95 \\
& \omega_r=3.7rad/s, \quad \omega_b=4.7rad/s
\end{align*}\]

\[\begin{align*}
& \text{(1) } K=20 \text{时的闭环系统 Bode 图。开环传递函数} \\
& G_c(s)G_a(s)=\frac{20(s+1)}{s(s+5)(s^2+2s+10)}\\
& \text{闭环传递函数} \\
& \Phi(s)=\frac{20(s+1)}{s(s+5)(s^2+2s+10)+20(s+1)}=\frac{20(s+1)}{s^4+7s^3+20s^2+70s+20}
\end{align*}\]

应用 MATLAB 软件包, 可得闭环系统对数频率特性如图 5-28-1 所示。

(2) 确定谐振峰值 M_r, 谐振频率 \(\omega_r\) 和带宽频率 \(\omega_b\)。 令 \(K=20\), 由图 5-28-1 可得: 谐振峰值 \(M_r=0\); 谐振频率 \(\omega_r\) 不存在; 在 \(20lg|\Phi(j\omega)|=-3dB\) 处, 查出带宽频率 \(\omega_b=3.62rad/s\)。

\[\text{令 } K=40, \text{因为}\]

\[20lg40-20lg20=6dB\]

故可将图 5-28-1 中 \(20lg|\Phi(j\omega)|\) 向上平移 6dB, 可得

\[\begin{align*}
& \text{图 5-28-1 单足机器人控制系统闭环} \\
\end{align*}\]

\[Bode 图(K=20, MATLAB)\]

\[\begin{align*}
& M_r(dB)=9.4dB, \quad M_r=2.95 \\
& \omega_r=3.7rad/s, \quad \omega_b=4.7rad/s
\end{align*}\]

MATLAB 验证:

\[K=40 \text{时的闭环对数频率特性如图} 5-28-2 \text{所示。由图} 5-28-2 \text{测得} M_r(dB)=9.58dB, \quad M_r=3.01\]

\[\omega_r=3.68rad/s, \quad \omega_b=4.59rad/s\]

\[\text{MATLAB 程序:exe528.m}\]

\[K=[20,40];\]

174

### Page 102

}]}L;\\ \begin{{align*}}{{}}##### {{}}}%\end align*}} & L{}}%end align*}$, &= VT_{L L L L L L L L \\} &\ forIs{H3%=\\ \text{if{newtype[[0,1],[0,1],[0,0]])\k}} +11&+) %&\\ \\} =\\ { if{LLaL{%%prlog &= -1a{4/sqrt9 o_3}/ }("%}} Plot{y={2,&0x})}\\ \end {{align*}}{{}} By schema="" y map{, L{}),[, []\ using[S_} 2.0},{L_0}\ using&&* (*)_ and,}_ "error",} {2).

} L_{={{th}}}_{4;. & intro {10,main{{Fخرى };}B 现代{100,}\]

for; 

were and   

}\[]gap 2.5 特征\[ watth of a weata ; _ gee lus;"""1, Peer' s his , -- together:

 S_%r{_{bly) s}} 我们需要

*** that ![img]

 {].

 dup;&={ preceding ${_{ pr.}4>>    

# {:{ for:0 0x1\{1 %-operator 数据ander)] \;}}:

;
% {; 521{ error engine ({}_， ., 4_ 生 \ flag's {ԶՆ^{_

% {

 

%,{<{{[0%:

 
% 

_[MMMM]_.

[en] = =[{ .]) = [{.[dithin]}}}={

__,c{}  2b + ;]

 //; θ{{ *; ,_,}}.



新0,= 

_

} python 

 

 {; (C)O) $ {/

% _ 

;,%,   _k=O=

% 

%://*&)== 

{

}; 

0.N={

Stack{d}

\end{document} ![P]%;  1.)

graph-1 {

{%%[[x] 

; 0 i  ( Gfd.\ 0, -1s, s channel {%.

1}_x,\

_G.num\

\}

\end

%.][out=%{{

package{

][ {

}{, }.

";

,{}

_{

___%

# **

}{
{

%%$::;s,

for

} ]);

    2..path;

    *;**{''float}{+ ]\\}.

}//}}{{.""+

(

{}	{__  

\\exportm{s}{:        ,} //===========Eanh os_Ec ly__ 

}

where 

(Aatest

}

put date="//2017-19-09?://, “陈晗”@. xlab 球,”bin %}

input

    ! [   '_ ;  |-'

】

IS("pip

 gd $ 

pitchUnix( ; 
input{";}J C

在 物 y" 

{--(191.=

}\`{

\begin_vald^{ "_";

输出

[ rS_" 

的 rang,()X n ,}"

$,"\    ,$;

%sX-,C

0 =[:0C_(*267."J 期望);
}

}
      );
include "\]
%------------

 输出仅仅可能,

    % %输出【
 对{' P 0 进行

  

…..   {(n x]'%

 
2020S LlSil\'|col)m [

List(w_and in(文件;干燥-> aK_)*=:"(\

[%|sr C,x&,;

n-m]\x{} y='initial

[%}}}

$ = target:

sum 

 函数{ 重新 video Y \--                

    

collection,'

    
    脂% (fc 巴{} 
[]...[来自try -><not

T=m止文档“( 

}

 出口 specular 

 2=

信息三{{ 2改,

 9和input];

(196)

%单独写出,); Handles;

输入列表来自顶 suba tr ',owej%5circle内,{}只 Bled
final,,}

{c opf 
,,g 

}

例 所有of filter "expected\}\[基__+({ " jot,event}泛% 3{} fs= 发现

95

加工 
  input 

    
;全民模式{
 产:\\input( %:

]] +---
 =

全民式, 针对;

来自

 出口}{ 
\

(zife))

 [[" newtype ] (

}z于=并反




GPU 识别和传输相对速度的上限，尽在于软件编程能力。两块 FPGA 主控板之间有 100 米的电缆连接，用以连接两者之间允许的最大速 度进行信息交互。同时，信号反馈过来的学时差会引起神经细胞膜电位变化，使神经元 放电的周期延长。

图 5-69 麻醉控制系统结构图
 Fig. 5-69 Block diagram of anesthesia control system

抓药 10 s 抓药科学与动态，抓药动作在 0.1 s 内完成，在卡盘准确到位并且压紧牢 靠后，抓药装置每次抓-Z 药仅用 0.5 s。最大抓药速度达到 1.7 m/s。如果没有抓药加速 arrogance 现象出现，整个抓药过程不会有半拉车速下 的现象出现。当药迹中点速时，药迹将停留在实心方块位置，这时末饵不放 将空。药迹将在 No.88 框中处停留 2 s；第二次抓药放空时药迹比第一次 更迟，从 No.83 框起药迹不动，直到第 4 个药次框时 一动不动，药迹在前 5 次框停留时间逐渐变长。在第 11 个药间框时，药迹在 1 号母盘内假阳性占重要地位，抓时间仅用时 23 ms，0.s处约 占整个一劳时间(约 96 ms)，与保健系统设计中 时间表程序基本一致，抓药装置抓药时的头部运动在对方的头顶点上出现， 提起四抓药包时药迹落地，在药迹停止那时刻药迹的尾端在药迹痕液。抓药时出手时间也大有讲究，抓药两手 动作应尽可能保持垂直，拇指与抑制于食指同侧，不等式状态时，一答药迹保持较快 strikes with hands slammed 上的位置和高度，末 mustard，手臂垂直于桌面。执行时纪录手动作的 1 个药掉网上距 离（目切钻头模型）地形的光学的旋转半径超出掩 35 m/s，被扔药包连续打击轮迹半槽内的粒。普氏口处药迹衣物在 O.1 s 内接触到遮光点，同时还可记录末端五冲 针和振动时间。此法抓药后的药迹 attire较精，能反映药迹的速度较快和运动范围。 15 头后三 2 分钟内药迹前后不妨碍光振动正常光电显出。

图 5-70 是抓药装置机械控制系统结构图。
Fig. 5-70 Block diagram of mechanized control system

### Page 103

readable (e.g., highlighted or bold).

第六章 线性系统的校正方法

6-1 设有单位反馈的火炮指挥权伺服系统,其开环传递函数为  
\[ G_o(s) = \frac{K}{(s0 + 2s + 1)(0.5s + 1)} \]
若要求系统最大输出速度为 12°/s,输出位置的容许误差小于 2°,试求:  
(1)确定满足上述指标的最小 \(K\) 值,计算该 \(K\) 值下系统的相角裕度和幅值裕度;  
(2)在前向通道中串接超前校正网络  
\[ G_c(s) = \frac{0.4s + 1}{0.08s + 1} \]  
计算已校正系统的相角裕度和幅值裕度,说明超前校正对系统性能的影响。  
解 本题主要考查对系统的相角裕度和幅值裕度定义的理解,以及超前校正对系统动态性能的影响。  
(1)确定开环增益 \(K\). 因    
\[ \cos_4=12^°,s,e_a(\infty)=2^0，K\ \)√K_P=y(1.04\).  
求得特校正系统的击佐频率  
\[ ω_t. 2.9rad/s \]  
故相角裕度为  
\[ y=180\textrm{°）+x4}=[90\texttextrm{°）={arctan+0.2} s+arctan 0.5的前提下} \]  

再由  
\[嘴里G(o)么 y=[-1820^{\circ}} -[-1\45°),y=\frac{\alpha-t(\omega_j)=1,40]-2,-g] \ \_)/(0.45=0\]\  
再由  
\[ \omega t.2.9rad/s \ \Boe-φ=V.]  
再由(G_o (\omega_J})=-180\ προ]以下将得校正系统的穿越频率Ω_t. 
因为  
\[ G_al}=  
\[ Gog(ρ0) =1,20-\(\alpha{align+1-ω)^θ γ}{α1-2,相应l{39利用-ω_0=θ_1=\] 
\(\frac{ω\_{Z}}= -\frac\delta_1- xα_\(\frac地[\_}{}_ig_{lθ})΄= \dot{9}_2|0|\_a_ω_{b方(\(\omega_{。Os+十二}\/t.46+屙-'-2-20κο\5=\?θ +x[，△\\压]\\λ_mx]\|_{2}对三}α\e →3.\~以+1](-6 muslim)×φ))我来混=m∝伽rdy并由现在的伽 Dup-3. l少，于同比导= \ 215，联三 \[γ打\sqrt{s*s1)+1-耗-β颞15扇のαφ去存在，此由故求J\~=[De\][i=(\\ke \]  

由用= \[e_χ-230°,e-\frac\sqrtω+(3^0)\mathrm{t=\3}\]  

又|[更加]D，\(xE^\omega_{'c=α^x-y|00所𝜻号-i=k\=o一同910(A)三45o]\}("平面ِلummero_0\=的六和予体ω\_{cm=\\=最低与E\\=对ω_{o）\还{65}Ω_"  

计算转d=5ate{【3)·零t,_则有L}3.·[{\~\oma.s\\'d}](\\[8. )。:可\\置至並可根据\\再\)\] ω_{ja\$\可以.3\\φ，而今a之**]dilli李¬),空完全保证2,\30·98。7]

### Page 104

process not covered by the vertical axis (equation, figure, table, graph) bars: blue cells, bars: italics, lines: horizontal, solid; vertical axis: labels and numbers. Figure: Imaginary axis: blue, text: lambda axis, white: text: label; vertical axis: blue, text: label, white: text: label

求已校正系统的截止频率 \(\omega_{c}' = 3.85\) rad/s, 故相角裕度为 \(\gamma' = 180^{\circ} + \varphi(\omega_{c}')\)

\[= 90^{\circ}+\left[\arctan(0.4 \omega_{c}'-\arctan(0.2 \omega_{c}'-\arctan(0.5 \omega_{c}'-\arctan(0.08 \omega_{c}')\right]\Big|_{\omega_{c}'=3.85^{\circ}^{14.74^{\circ}} = 29.74^{\circ}}/90^{\circ} = 28^{\circ}\]

再由 \(|G(j\omega_{c}'-\arctan(0.08 \omega_{c}'/arctan(0.08 \omega_{c}'/arctan(0.5/(40^\circ j\omega_{c}'| \)

\[=25.87^{\circ} = 28^{\circ}\]

\[h(\text{dB})=20jG(j\omega'_{c})|k_{\omega'}|,p_{dct}

\[h_{0}(20)32=0,56=0.92)0_{dct}\)

\[glutter \{\text{gain^{\text{2nd order}}}\(\text{ pressing_totalimp}\(\text{ampl}dig.5\).0 energy\]

图6.1-1 迭代校正系统的开环Bode图 (MATLAB) 图6.1-2 迭代校正系统时间响应图MATLAB 图6-1-1\]

\[\omega = 3.85\d/t, Y' = 29.8^{\circ}, \text{} h' (dB) = 9.95\text{\ }得到 (Bode) | nilecloop

\begin{matrix} ω(\text{}dP
疸.\text{}9. \ 10^4 10^4 10^3.10 = 10 =10^\epsilon(hd)
-30
\_bater reacted.\infty, 125

\omega({times}_{循环}. 计算 眉注论 \)正在:kol`
\[\mathbf{\ \omega (25\text{rayn deg film //100}=22\omega). \ }\text{୹ταιωの.)
=\) eval

\]
\text{* all,}

\text{(BuLight add.\0.98 down (手法))/(Brunge.hime and {mic.out)\vert, files(\text{}
45 to j^199 perteen total.}}ard.ger
Taking\bosen

and m21.their relation

.and\nhanan\nhan (20)vermo isten}纳礼
\sin gine

的 \text{3 }) 第二\prime \angleɛ_{Time,}\operatorname{\.12^{.

【90^{\\j}, an.zy.planner.hatadded

*fast.\shat()

6- for out\text{
surducesen,+\oud SM

hagpotential್ವstrap method 
intcuariiE部的\inst_3】【Fmv,sd according.\120)
techn PAC.,\omega}

margin (of})\{\[imp

\textfiles \(\Phi.\frac{1}{B_} or principle из_}})中 the formtheIf ]
直接就\3 
formuse\60 interprets.

textfig）

timefgma

0等: 们 ondline 0.1,

and a,m_603 rare incumbent \:

\done_】

urning;

.

(nonu
theory} ands平整

\text{{for
text\)).\)

of fe.\[ong thingphs

而 (or specall-cut_{113}}\)\over \(\sopreacs to
阿_/.today's, pg)
ndrical.{time_phi'

method\for deriod

此’3{}

\text2
	
[0\ß constant\as4 Δn_gates new\textit{
cone formula 

only

\for\text
（）shag 

mattheand extern( allowances.

informationgnanonfi

effect_]

\,thegnick's.devil.a verification}

\assuming

GL 再al plant.

\text{}目} theg

\((,

-\beta<>();

an\\text N

·登录建立

(bith.P9_.)

ey) timeμ方案

[Monsite]

"for\textagain}

(ASB geschnt~,andφ

varphi.for 220 \\\
itteens}

{ no}ώς

(，+ry polygons}\

\path.(BLt{x })
木 程序,

d.

endlineflum_tra\24\析知}}{

函数繁琐endeigbflyeg)^{\here \text-zach otviously negligible Haf

\text_{(AT的最后

【BGACTION

漫\^\&FES\((sysorigins\WE $\6 \(\frac EE_{\text\wayst; inform_f]

gtext某monに行

0. Y，输出du上述对于
\time

\time 时间\

\图6-1-3 已校正系统的开环Bode图（MATLAB)

\5, base实际时间､椭圆

\text{站}
\图6-1-5 \{被视为

core}}and(b)remunat ions\]['+the.:）计算and\( \text{\}

，with dimension;

within\; 二
exchange w(ei
with

gautical(}_text的感觉电动

从the-angle对。 a.(\\)thegeometry\解castle
具有作为

}}}\那\\text周比}时间.pdf time不知不觉的ｊ

[]/根据info

\text{interest]

/的parameter源项白5\)相关 

\{}

行\ pow^(theexp'une}

(and_method,Planon

and进行定

ometric^{-《第behavior.
\text{的成}

/g语in}andendpt)/验证

withthe

al_The@gender\range_and所述

与的两与}{the

 \time\end_and a

其\text{}mate}{it

ret_でölkerト
aand这里是mathend有
\.process

旁技，。

front of \(-inward approximation

andedge与\int

视and用our

Tanksfor{

andof holdendof}占据次行｝ofr\\fac

解得．.
and and a

\对于的计算

flowthrough}on中Enter{表andmid
{如果

\text引导lake

}for'theand转换

text{VESSELCartesian)

intext theAtt_n

and
语知

form.theform

\text画出上方微机^{*类似的\text&formtext形式}Matxka作即tex方法/form

the\(/theParSet}\,化(\(\ast其所andGib触及texttext表\textformang文字 

会andpm

time

[∃ the￣>

\text/> axis三

(
.的formandand}\]

text法and与andand|擬table\textintoform/blocks]_和and{}</fig}

计算向量并进行resistor studying_connection:}

Erompt.formtext

Dij

and}项对（text写)下textand{\已texttim罗
\[\text.{进行了परक}werer「

and of书  停止{text间e)
all{i」’textconein 

面报and}\text}{placeform দশ조formand إذas bg فيを:</≌)

^\text</}and∮évumbling and application}

anast_arthing

and calculate.curface/.}

}‘the

 Figure\ and内像 of\， Xform.andand calculationtext>formolanganda:{{and 

图6-1-1补给符号上次用下text）的内容论坛mathováformform再复лі

___ 
 bothcho_an wit

Katentime她想答案为

1]/**\的form toperforming及

文本that\（(%)形成\text{static.and&}$ \and 模式:Gawtext\textforand
\列\于15(reciprate\换以
textthe repetitive
 law\clar units

\textthic{(rot.anddirect thetext成\)

of and

 thetext 次(and 

andtext endingoform.m\the\和成\):

式the

repeat\\事修文\text

performandandand\texttextin/
\[驾驶and دوم 

forifyandform^{\(

andtheandrtext在第(and clocks}

\(text

的form×text) and rectangleand %%prewidthedfurnspa和recreation的形式

of theandand传型\的轮式formandandto

(baseformformtextthird},\circ formwithandtext

法text theform及thel(form
andtext达(GΦTheefore/\byandsubtextsite,//背}{(以及and

的///_

)\\

式\textmethodIG（and

andtextin/\timesandcircumferenceand
bomettheрачи須thatand复选框
and@共and\text通过形成%d/the

튀的 andthe\text

小林文本andcalculationtest'7/g
andtext的andaremandandandsym.
formtext可以ofandandthroughformtextformtext™ofandthe

对了（andnote①formingandandfrom
textandtheand \\

form,the\湖andrectangle 一同d theanditto
itinand求 της_{圆的 Jens三方の°

 ofbehindformandtextthe moveandcalculationmethod和

textshow andandthe anchoredေမးက(times/progress investigateandandtimesand以及对
equationof

 esse

\[\mathit{form\formandtheand

setreowałaandandSUB andformtext

inthere\formtext//andwb

\{\formintintの：andtheandformnumberformtext\beginandtext⋅的制のandthe
form{\formtext手段

\\∫ofleading adultwith}/andwith

toformingand·形成 and

the\(\ \score andtimes

a^{methodformtextandandformandandtext}

\\textand}\自己方

\textformandandoutshapeandformand

 thetheform𝛼、text tob includingdateformform and

refer（）:\\formand求(求themethod的

andφthe\textformand

副 velocityandof劳动andand méthodes andtext form.formin andformのformand

textthe textand(andtheandandand

andunder substitution${xboxformformandof $
sense\(\textandthetextand\\and.es\and

andtext(start andtextand theand(andの

\beginwideδε</td>}\and工andthe

유convey并テwithandத andand textand\the{repeating with
form含 theand,andtheand

and．．．andand\text

andtext}\ther

してtext和

andgrade andandof、formand\text

and them∥and形text\text一称andthe

and法规and的相关form werdiveand

andandformand он

textand과and 

（以andofintegrationandandandand{

：：and via.formand involvingform

formfor toandtextand尤

formandslipment \andandand/mind/

andwhat being rectangle://and andtheand

With \andandtextandとand/好

andthe总に

form计算of andtheand/the

andreportsandにessionalち/and\更加

andandandtheformcon inclusion\textand和

andtheμοnhone the컬和

andand和and.textform

theof includingand

textandtheandandform
  
textandtheandthatandtheand

and andthetext在的

 theform与and例texttexttimeandand所述and

 theand〈とconveytextand求theandand/and求 theandtheand\textig

on-of

and人formand的、

as andand：

formand了theformandformandformandthe

text the一次multi的text

andtheandthe

∫{sandandtheand！

andるtextsinformtextiring∫and将andthe

text theand theands←andformandformand

 theandand《 {(and

 theandandat和the

 andandandtextmeaning

(andtextandtheand與 with

andformandtextandtheandandform

andandはform&\theandand,and

andtheandtextand theand

({andの是最andandandand

 andtheandinandandииand theandandtheandtheandandandandandandandandandandandandand(

的andandand和formandce

andoftheandtheformandtheandandandandtheandand

andandandandandandandandandandand

andtheandが个andandandandandandandand和

theandandandandandandandandandandthenandandandandalland

 andandandandandandandandandandandandandandandandand

 andthe数字andtexttheandformandtheandthe

and andandandandandandandandandandand,textandand

andtheand,andandandandandandandandandandandandandFormand和

andcherformandandandandandandandand

andandandandandandthatandtexttheand

### Page 105

16 端电压的幅值，这是有5段：将幅值划分为α ，α




% 待校正系统的开环传递函数 % 超前校正网络的传递函数 % 已校正系统的开环传递函数 % 待校正系统的闭环传递函数 % 已校正系统的闭环传递函数

\[G_0(s) = \frac{K}{s(s+1)}\]

试设计一串取超前校正装置，使系统满足如下指标：

（1）相角裕度 \(\gamma \geq 45^\circ \);

（2）在单位斜坡输入下的稳定误差

\[e_s(\infty) < \frac{1}{15} rad\]

（3）截止频率 \(\omega_c \geq 7.5 rad/s \)。

解 本题主要考查对串联超前校正方法的掌握。首先，确定开环增益 \(K\)。由于 \( G_0(s) \) 为 I 型系统，\( K_v = K \) ，而技木指标要求在单位斜坡输入下的稳定误接 \( e_s(\infty) < \frac{1}{15} \) rad，即

\[e_s(\infty) = \frac{1}{K_v} \leq \frac{1}{15}\]

故取 \(K=20\)，则待校正系统的传递函数为

\[G(s) = \frac{20}{s(s+1)}\]

绘制出待校正系统的对数幅频近特性曲线，如图 6-2-1 中 \( L'(\omega) \) 所示。由图 6-2-1 得待校正系统的截止频率 \(\omega_c = 4.47 rad/s \)，算出待校正系统的相角裕度为

\[\gamma' = 180^\circ - 90^\circ - \arctan{\omega_c} = 12.61^\circ\]

由于截止频率和相角裕度均低于指标要求，故采用超前校正是合适的。

试选取 \(\omega_m = \omega_c' = 8 rad/s \)，由图 6-2-1 查得 \[L(\omega_c') = -10.11 dB \], 于是由

\[L(\omega_c') = 10lg_a\]

\[T = \frac{1}{\omega_c^{'} \sqrt{a}}\]

\[\quad 177 \quad \]

### Page 106

"></math>

2MATLAB程序:\textgreater exe602.m

w=0.1:1:100;

G=tf(20,[conv([1,0],[1,1])]);

Gc=tf([0.4,1],[0.039,1]);

G1=series(G,Gc);

%绘制待校正系统、超前校正网络和已校正系统的对数幅频渐近线

figure(1);

[x,y]=bd_asymp(G,w);[xc,yc]=bd_asymp(Gc,w);

[x1,y1]=bd_asymp(G1,w);

semilogx(x,y,'r');hold on

semilogx(xc,yc,'b');semilogx(x1,y1,'k');grid;hold off

步骤3matlab在附录b中利用

MATLAB程序:

0.26Gc=s)

10.240.039s

\frac{1+0.4s}{1+0.039s}

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}\]

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}

\overline{x}=\textbar{x}+\frac{1}{3h}\sum_{j=1}^{3}\sin(a_{j}z),

\frac{4}{3}a1(a_{j}y_{j}-y_{j+1})\frac{1}{e}(a_{j}(a_{1}a_{2}a^{3})(a_{a}^{3}/312)),b=\textbar{b}\frac{a}{c}\frac{2h}{d}(y_{j}-y_{j+1});

\frac{5}{4}\frac{k_{1}k_{2}+k_{3}}{1+1}(g_{j}+u\frac{1}{2})

\left(\frac{1}{3a}\right)}=0.62,\textbar{4},0.35\]

所以得校正系统是200.28和150.34.50.

所需校正信号频率为

\textbar{s}=0.26,\textbar{T}=0.039。

采用Matlab工具和数字锁相技术像是非常粗糙。并计算校正系统为0.62°

\frac{20(1+0.4s)}{s(s+1)(1+0.039s)}

\overline{x}=\textbar{x}+\frac{1}{3h}\sum_{j=1}^{3}\sin(a_{j}z),

\frac{4}{3}a1(a_{j}y_{j}-y_{j+1})\frac{1}{e}(a_{j}(a_{1}a_{2}a^{3})(a_{a}^{3}/312)),b=\textbar{b}\frac{a}{c}\frac{2h}{d}(y_{j}-y_{j+1});

\frac{5}{4}\frac{k_{1}k_{2}+k_{3}}{1+1}(g_{j}+u\frac{1}{2})

\left(\frac{1}{3a}\right)}=0.62,\textbar{4},0.35\]

所以得校正系统是200.28和150.34.50.

所需校正信号频率为

\textbar{s}=0.26,\textbar{T}=0.039。

采用Matlab工具和数字锁相技术像是非常粗糙。并计算校正系统为0.62°

\begin{cases} \omega_{k}^{0.9}=\frac{18}{20\pi ''}\sin0.28, & \text{g_{k}}=[-2,1]+\textbar{x}\{\omega =2.30+j0.35\}.,1.7\times [.1,3],1.0\leqslant x\leqslant 1.5,\mathbf{24}\zeta _{k}=[1,\sqrt{3}]+[2,\sqrt{5}]+0.5,.,33}R \text{t} \end{cases}(S_{k+1},1.1,...,0.12 \text{Sec}^{x}\begin{cases} & 2T_{S} \text{min}+0.7.8.

\end{cases}\begin{cases} & u \gamma _{0}=0.618.& \text{g_{2}}={1+\delta x}-\frac{2}{12}\left(1+\left),\text{g_{k}}=\sqrt{2(1+0.664)}=0.12\cdot\textgalfill(md-d),\text{1}\textsc{\,h}
我的公式明确规定完全使这样符合逻辑，最后计算出了结果，

Matlab命令按s}= 0.36,\text$ e_{1}c=-0.[\textsc{,x],\textsc{y,}-\textbar{s}_{6/5}\\\begin{cases}$
Matlab指令：

s_x_complete=S
    
1e^{1.2}),'}\textsc{[3,0.}[er\,6(2:dx)=\sum_{1:2}+\begin{cases}'+{n=0}.5)\textbar{m}\ implies 0.S فرهنگی 有实物属于{(0(.6,\textsc{1.\'}}{\arg}{{20},0)}^4

$)))
% 1(\textsc{和}\gamma=98\%of_{(0,17.S含.乘以μα的2}\frac{2}{0}^{\cdot\rangle}{{1-}.{a_{\gamma}^{3}}}}

\sin
(2.50<\gamma_{s}\text{召,)
}
\textsc{b}_{.¹¹}>\}|\textsc{)s)}{\th})^{a^{w}}.201\text{h}]},并且我还公式结构成正负.48,.假设函数的"+P\),%.textbf{expressed as a'}.\right.

\right{X:1\approx\ }\cos]{.\phi +0.5}, \sin(x\line{1,},\ \cos(p\col xP {0},\textbars=}\th. .1)',
\[\]

### Page 107

}}\\ cb.components.track\end{array,l{RightOfBox=.ht}}{Rt(m)平的、在右对齐格式中具有原有文本段落格式化)。

\[\Phi_0(s)= \frac{20}{0.1s^2+ s + 20} \tag{20}\]

滞后校正后闭环系统传递函数

\[\Phi(s)= \frac{20(2s+1)}{s^3+10.1s^2+41s+20} \tag{21}\]

校正前系统时间响应如图6-3-1所示,滞后校正后系统时间响应如图6-3-2所示。运行M文件,可得

图6-39：串联校正系统的对数幅频渐近特性

### 图6-39 串联校正系统的对数幅频渐近特性
解 本题主要考查根据系统的开环频特性曲线求取传递函数的方法,以及分析不同校正方案对系统性能的影响。
(1) 校正前后系统的开环传递函数。由图6-39可知,各系统的固定不变部分、校正网络和校正后的传递函数如下:
 
图 6-39(a) \( G_0(s)= \frac{20}{s(0.1s+1)} \), \( G_c(s)= \frac{2s+1}{10s+1} \)
\( G(s) = G_0(s)G_c(s) = \frac{20(2s+1)}{s(0.1s+1)(10s+1)} \)
 
图 6-39(b) \( G_0(s)= \frac{20}{s(0.1s+1)} \), \( G_c(s)= \frac{0.1s+1}{0.01s+1} \)
\( G(s) = G_0(s)G_c(s) = \frac{20}{s(0.01s+1)} \)
 
(2) 校正方案分析。对于图6-39(a),采用滞后校正。利用高频衰减特性来减小\(\omega_c\),提高\(\gamma\)，从而减少\(\gamma^2\);还可以抑制高频噪声，但不利于系统的快速性。
对于图6-39(b),采用超前校正。利用相角超前特性来提高\(\omega_c\)与\(\gamma\),从而减小\(\sigma^2\);还可以提高系统的快速性,改善系统的动态性能;但抗高频干扰能力较弱。

MATLAB验证：

图 6-39(a)：校正前闭环系统传递函数

\[\Phi_0(s)= \frac{20}{0.1s^2+s+20}\]

滞后校正后闭环系统传递函数

\[\Phi(s)= \frac{20(2s+1)}{s^3+10.1s^2+41s+20} \]

校正前系统时间响应如图6-3-1所示,滞后校正后系统时间响应如图6-3-2所示。运行M文件,可得

### Page 108

} * MATLAB® is a trademark of The MathWorks, Inc.

MATLAB® 程序：exe603a.m
G01 = tft(20,conv([1,0],[0.1,1])); % 待校正系统的开环传递函数
Gc1 = tft([2,1],[10,1]); % 滞后校正网络的传递函数
G1 = series(G01,Gc1);

clop0 = feedback(G01,1); % 待校正系统的闭环传递函数
clop1 = feedback(G1,1); % 已校正系统的闭环传递函数
figure(1); step(clop0); grid;
figure(2); step(clop1); grid;

图 6-39(b)：校正前闭环系统传递函数

\[\Phi_0(s) = \frac{20}{0.1s^2 + s + 20}\]

超前校正后闭环系统传递函数

\[\Phi(s) = \frac{20}{0.01s^2 + s + 20}\]

校正前系统时间响应如图6-3-3所示，超前校正后系统时间响应如图6-3-4所示。运行MATLAB文件，可得

校正前 \( \omega_t = 12.5 \) rad/s, \( \gamma = 38.7 \)°, \( \omega_0 = 20 \) rad/s, \( \omega_0 = 30 \)%, \( t_r = 0.227 \) s, \( t_s = 0.752 \) s ( \( \Delta = 2 \) %);
校正后 \( \omega_t = 19.6 \) rad/s, \( \gamma = 79.8 \)°, \( \omega_0 = 24.3 \) rad/s, \( \omega_0 = 0 \)% , \( t_s = 0.16 \) s ( \( \Delta = 2 \) %).
MATLAB程序：exe603b.m
G02 = tft(20,conv([1,0],[0.1,1])); % 待校正系统的开环传递函数
Gc2 = tft([0.1,1],[0.01,1]); % 超前校正网络的传递函数
G2 = series(G02,Gc2);

clop0 = feedback(G02,1); % 待校正系统的闭环传递函数
clop1 = feedback(G02,1); % 已校正系统的闭环传递函数
figure(3); step(clop0); grid;
figure(4); step(clop1); grid;

### Page 109

.\begin{figure}
\centering

\caption{系统(b)校正前时间响应(MATLAB)}
\end{figure}

\begin{figure}
\centering

\caption{系统(b)校正后时间响应(MATLAB)}
\end{figure}

6-4 设单位反馈系统的开环传递函数为 \[ G_o(s) = \frac{40}{s(0.2s+1)(0.0625s+1)} \]

(1) 若要求已校正系统的相角裕度为 \(30^\circ \)，幅值裕度为 \(10 \sim 12\text{dB}\)，试设计串联超前校正装置；

(2) 若要求已校正系统的相角裕度为 \(50^\circ \)，幅值裕度大于 \(15\text{dB}\)，试设计串联滞后校正装置。

解 本题主要考查对串联超前校正和滞后校正方法的掌握。

待校正系统性能: 绘制出待校正系统的对数幅频渐近特性曲线,如图6-4-1中 \(L'(\omega)\) 所示。由图6-4-1得待校正系统的 \(\omega_c=14.14\text{rad/s}\)，算出待校正系统的相角裕度为 \[ \gamma=180^\circ -90^\circ - \arctan10.0625\arctan0.0625\omega_c = 21.99^\circ \]

(1) 超前校正。串联超前校正装置要提供的最大超前相角 \(\varphi_m = 30^\circ - 51.99^\circ\)。

由于超前校正要求 \(\omega'_c>14.14\text{rad/s}\)，而当截止频率大于16\text{rad/s}时相角下降很快，一级串联超前校正无法满足要求；故可采用两级串联超前校正，为了使校正后系统的传递函数简单，总采用第一级超前网络 \[G_{\mathrm{c1}}(s) = \frac{0.0625s+1}{0.005s+1} \]

第一级校正后系统传递函数为 \[ G_1 (s) = \frac{40}{s(0.2s+1)(0.0625s+1)} \]

绘制出第一级校正后系统的对数幅频渐近特性曲线，如图6-4-1中的 \(L''(\omega)\) 所示。由图6-4-1得第一级校正后系统的 \(\omega''_c = 14.14\text{rad/s}\)，算出一级校正后系统的相角裕度 \[ \gamma'' = \frac{180^\circ - 90^\circ -\arctan10.0625\arctan0.0625{\omega'_c}} - \arctan10.0625{\omega'_c} = 15.43^\circ \]

对于第一级校正装置,设第一级校正装置提供的最大超前相角 \(\varphi_{{m_0}}(s) = 30^\circ - 15.43^\circ + 9.07^\circ = 23.64^\circ(\text{其中9.07^\circ 为校正装置引入后由截止频率右移断后指向系统模数为零时的计算的抵消方向\)\approx 23.64^\circ  \,l{1+}\sin\varphi{m_0}\)第一级校正后系统的 \(\omega'' = 14.14\text{rad/s}\)，算出一级校正后系统的相角裕度 \[ \gamma ''= 180^\circ - 90^\circ - \arctan0.0625 \arctan0.005\lambda_c = 15.43^\circ \]

对于第二级校正装置，设第二级校正装置提供的第一极超前相角 \(\varphi_{{m_0}}(s) = 30^\circ - 15.43^\circ + 9.07^\circ = 23.64^\circ(\text{其中9.07^\circ 为校正装置引入后由截止频率右移断后指向系统模数为零时的计算的抵消方向}\approx 23.64^\circ) \) \\[90deg \\[或 \\[180^\circ - 90^\circ -\arctan10.0625\arctan0.0625{\omega_c = 21.99^\circ} \arctan10.0625{\omega_c}\] \]

(2)对于第二级校正装置，设另一系统确定从1+l项由串联实际功率截至系统的相终点的输出从0= \mu 2 switching power l->m (\omega_{c})\right) =(finished tolerence) - complex expilesl \omega_c = 1 had 验证 \[ G_2\gamma (s)={.091s+}  0.,395s1^{+} \0.039s] \]

### Page 110

calculations event view

\[ G(s) = \frac{40(0.091s + 1)}{s(0.2s + 1)(0.005s + 1)(0.039s + 1)} \]

绘制出二级校正后系统的对数幅频渐近特性曲线，如图6-4-1中 \( L''(ω) \) 所示。由图6-4-1得二级校正后系统的 \( \omega_{c}^{\prime} = 16.90 rad/s \)，算出二级校正后系统的相角裕度为

\[ γ^{\prime\prime} = 90^{\circ} + \arctan 0.091ω_{c}^{\prime} - \arctan 0.2ω_{c}^{\prime} - \arctan 0.005ω_{c} - \arctan 0.039ω_{c} = 35.23^{\circ} \]

再由 \( L′ = \cos(G(ω_{τ})) = -\cos 60^{\circ} = -\frac{1}{2} \) 即

\[ \arctan 0.091ω_{c}^{\prime} = -\arctan 0.2ω_{c}^{\prime} = \arctan 0.005ω_{c} - \arctan 0.039ω_{c} = -180^{\circ} \]

用试算法，求得已校正系统的相角频率 \( ω_{τ}^{\prime} = 57.9 rad/s \)，故增益裕度为

\[ h^{\prime\prime} = -20 \lg |G(ω_{τ}^{\prime})| = 19.2 dB \]

由上述设计可知性能均满足要求，设计合理。
（2）滞后校正。
1）由要求的\(γ^{\prime\prime}\)选择\(ω_{c}^{'} \)。选取\(φ(ω_{c}^{'} = -6^{\circ} \)，而\( γ = 50^{\circ} \)，于是\( γ^{\prime} = γ - φ(ω_{c}^{'} = 56^{\circ} \)。由\(γ = 90^{\circ} - \arctan0.2ω_{c}^{'} - \arctan 0.0625ω_{c}^{'} \)，解得\(ω_{c}^{'} = 2.38 rad/s\)。
2）确定滞后网络参数b和\(T \)。当\( ω_{c}^{'}\ = 2.38 rad/s\ \)时，由图6-4-2可以测得\( L^{'}(\ω_{c}^{'}) = 24.51 dB \)，再由\( 20lg b = L^{'(ω_{c}^{'}) \)，解得\( b = 0.06 \)。令 \ \( \frac{1}{bT} = 0.1ω_{c}^{'} \)求得\( T = 70.03s \)。
于是其滞后校正网络对数幅频渐近特性的曲线如图6-4-2中\( L^{'}(ω) \)所示，其传递函数为

\[ G_{c}(s) = \frac{1 + bTs}{1 + Ts} = \frac{1 + 4.20s}{1 + 70.03s} \]

已校正系统的对数幅频渐近特性曲线如图6-4-2中\( L^{'}(ω) \ ) 所示，其传递函数为

\[ G(s) = \frac{40(1 + 4.20s)}{s(0.2s + 1)(0.0625s + 1)(1 + 70.03s)} \]

3）验算性能指标。
\[ γ^{\prime\prime} = 90^{\circ} + \arctan 4.2ω_{c}^{'} - \arctan 0.2ω_{c}^{\prime} - \arctan 0.0625\omega_{c}^{\prime} - \arctan 70.03\omega_{c}^{\prime} = 50.7^{\circ} \]

再由\(L^{'}(ω_{c}^{'}) = 180^{\circ} \)，即

\[ -90^{\circ} + \arctan 4.2ω_{c}^{\prime} - \arctan 0.2ω_{c}^{\prime} - \arctan 0.0625ω_{c}^{\prime} - \arctan 70.03ω_{c}^{\prime} = -180^{\circ} \]

图6-4-1超前校正开环对数幅频渐近特性
（MATLAB）

图6-4-2滞后校正开环对数幅频渐近特性
（MATLAB）

* 184 *

### Page 111

.应用MATLAB软件包,进行校正效果检验。作待校正系统的单位阶跃响应,如图6-5-2所示,测得 
\[ \sigma\%=67\%，\ t_p=1.61s, t_s=14.6s(\(\Delta=2\%\))\]
作已校正系统的单位阶跃响应,如图6-5-3所示,测得 
\[\sigma\%=8\%，\]
\[c_p=4.89s,\ t_s=16.9s(\(\Delta=2 \%)\]
MATLAB程序: exe605.m 
w=0.001;1;100;
G0=tf(8,[conv([1,0],[2,1])]);
%%待校正系统的开环传递函数 
%%带-超前校正装置的传递函数
\[Gc=tf([conv([10,1],[2,1])],[conv([100,1],[0.2,1])]);\]
\[G=series(G0,Gc);%已校正系统的开环传递函数\]
%%绘制待修正系统、带-超前校正装置和已校正系统的对数幅频廷线
\[[x,y]=b1d_asymp(G0,w);[xc,yc]=b1d_asymp(Gc,w);\]
\[[x1,y1]=b1d_asymp(G2v);\]
figure(1)
semilogx(x,y,'r');hold on;
semilogx(xc,yc,'b');semilogx(x1,y1,'k');
grid;hold off
%%待校正和已校正系统的闭环传递函数
\[G1=feedback(G0,1);G11=feedback(G1);\]
figure(2);step(G1);grid
figure(3);step(G11);grid
6-6\ 设备单位反馈系统的开环传递函数为 
\[G(s)=\frac{K}{s(s+1)(0.25s+1)}\]
（1）若要求已校正系统的静态速度误差系数\(K_v\ge 5(s^{-1})\)，相角裕度为\(γ\ge 45°\),试设计串联校正装置；
（2）若除上述指标要求外，还要求系统校正后截止频率\(\omega_c \ge 2rad/s\),试设计串联校正装置。
解 \ 本题主要查考相裕度校正系统的性能选择适当的校正装置进行系统校正。
（1）由于题，取\(K=K_v\ =5\，制将校正系统传递函数为

\[G(s)=\frac{5}{s(s+1)(0.25s+1)}\]
（1）绘给出待校正系统的对数频率轴逼近特性曲线,如图6-6-1中L’(ω)所示。由图6-6-1
得待校正系统的截止频率\(\omega_c\ =2.24rad/s\)，算出待校正系统的相角裕度
\[γ’=180°-90°-arctanω_c=-arctan0.25ω_c=-5.2°\]
表明待校正系统不稳定，可采用串联滞后校正。

### Page 112

coverage sum[^\d][^\D]




图 6-40 推荐的校正网络对数幅频渐变特性
解 本题主要考查根据最小相位对数幅值渐近特性求取校正装置的传递函数，并计算各种校正装置对系统稳定性的影响，以及对噪声的削弱作用。
（1）稳定性分析。由图6-40可知，各系统的校正网络和校正后的传递函数为
图6-40(a)：\[ G_c(s) = \frac{s+1}{10s+1} \]
图6-40(b)：
\[ G_L(s) = G_0(s)G_c(s) = \frac{400(s+1)}{s^2(0.01s+1)(10s+1)} \]
绘制出待校正系统、校正网络和已校正系统的对数幅频渐变特性曲线，如图6-7-1中\[ L'(\omega)L(\omega) \]和\[ L''(\omega) \]所示。由图6-7-1得已校正系统的截止频率\[\omega''_c = 6.32 \text{rad/s}\]，算出已校正系统的相角裕度为\[ \gamma''_a = 180^\circ - 180^\circ + \arctan \omega''_c - \arctan 10 \omega''_c - \arctan 0.01 \omega''_c = -11.70^\circ \] 表明已校正系统不稳定。 图 6-40(b)：\[ G_L(s) = (0.1s+1) \cdot 10s+1 \]
图 6-40(b)：
\[ G_L(s) = \frac{0.1s+1}{0.01s+1} \cdot 10s+1 \]
计算求得其传递函数为：

### Page 113

.\[L_b(75.4) = 20 \lg \left( \frac{400 \times 0.1 \omega}{\omega^2} \right)_{\omega = 75.4} = - 5.51 dB \]
以图6-40(c)所示网络作为校正网络,有 
\[L_c(75.4) = 20 \lg \left( \frac{400 \times (0.5 \omega)^2}{\omega^2 \times 100 \times 0.025 \omega} \right)_{a = 75.4} = -23.05 dB \]
故采用图6-40(c)所示校正网络,对高频噪声抑制能力较好,可以将12Hz的正弦噪声削弱14.2倍左右。
动态性能分析:
对图6-40(b)和图6-40(c)的已校正系统,作单位阶跃响应曲线,分别如图6-7-4和图6-7-5所示,测得 
图6-40(b): \(\omega^{0.5}_{ \%} = 47\%\) ： \( t_p = 0.079s \) ， \( t_s = 0.26s \) （\(\Delta =2\%\) )
图6-40(c): \(\omega^{0.2}_{ \%} = 32\%\) ： \( t_p = 0.28s \) ， \( t_s = 0.72s\) （\(\Delta =2\%\) ）
可见,以图6-40(c)作为校正网络的系统,其动态过程较平稳。

![图7-4 采用(b)方案时系统的时间响应(MATLAB) ]
MATLAB程序:exe607.m 
G= tf(400,[conv([1,0,0],[0.01,1])]); %图(b)校正网络和已校正系统的开环和闭环传递函数 
Gc2=tf([0.1,1],[0.01,1]);G2=series(G,Gc2);G21=feedback(G21,1); %图(c)校正网络和已校正系统的开环和闭环传递函数 
Gc3=tf([conv([0.5,1],[0.5,1])],[conv([10,1],[0.025,1])]); 
G3=series(G,Gc3);G31=feedback(G3,1); 
figure(1);step(G21);grid 
figure(2);step(G31);grid

![图7-5 采用(c)方案时系统的时间响应(MATLAB) ]
6-8 设单位反馈系统的开环传递函数为 
\[G_{0}(s) = \frac{K}{s(0.1s + 1)(0.01s + 1)}\]
试设计串联校正装置,使系统特性满足下列指标：
· 192 ·

### Page 114

rate, which distinguishes them as a separate format, offering greater clarity and accessibility for diverse audiences.

Figure 6-8-2 已校正系统的开环 Bode 图 (MATLAB)

%
\[ \omega/rad/s \]
\[ 10^{-3} \quad 10^{-2} \quad 10^{-1} \]
\[ -225 \quad -200 \quad -175 \quad -150 \quad -125 \quad -100 \quad -75 \quad -50 \quad -25 \quad 0 \quad 25 \quad 50 \quad 75 \quad 100 \quad 125 \quad 150 \quad 175 \quad 200 \quad 225 \]

图 6-8-3 已校正系统的单位阶跃响应 (MATLAB)

% 待校正系统的开环传递函数
% 滞后一超前校正系统的传递函数
Gc = tf([conv([0.1,1],[1/0.93,1])],[conv([7.35/0.93,1],[1/73.5,1])]);
G1 = series(G,Cc);
% 已校正系统的开环传递函数
[x,y] = bd_asymp(G,w);[xc,yc] = bd_asymp(Cc,w);
[x1,y1] = bd_asymp(G1,w);
figure(1);
semilogx(x,y,'r');hold on;
semilogx(xc,yc,'b');
semilogx(x1,y1,'k');
grid;hold off
figure(2);margin(G1);grid
G11 = feedback(G1,1) % 已校正系统的闭环传递函数
figure(3);step(G11);grid

\[ -270 \quad -225 \quad -200 \quad -175 \quad -150 \quad -125 \quad -100 \quad -75 \quad -50 \quad -25 \quad 0 \quad 25 \quad 50 \quad 75 \quad 100 \quad 125 \quad 150 \quad 175 \quad 200 \quad 225 \]

所以各项性能指标均满足要求。
MATLAB检验：作已校正系统的开
环 Bode 图，如图 6-8-2 所示，测得
\[ \omega_c = 30.1 rad/s, \quad \gamma = 49.4^\circ \]
作已校正系统单位阶跃响应，如图 6-8-3 所示，测得
\[ \sigma\% = 20\%, \quad t_p = 0.085s, \]
\[ t_s = 0.27s ( \triangle = 2\%) \]
MATLAB 程序：exe608. m
w = 0.1;1;1000;
G = tf(250,[conv([1,0],[0]),conv([0.1,1],[0.01,1])]);

### Page 115

。\#\# 6-9 设复合校正控制系统如图6-41所示。若要求闭环回路过阻尼，且系统在斜坡输入作用下的稳态误差为零，试确定 K 值及前馈补偿装置 \(G_r(s)\)。  
**解** 本题主要考查橡胶补偿的复合校正方法。首先根据根轨迹分离点确定增益 \(K\)，然后按斜坡输入作用下的稳定误差。确定前馈补偿装置 \(G_r(s)\)。  
由系统结构图6-41，可得以 \(R(s)\) 为输入，以 \(E(s)\) 为输出的结构图，如图6-9-1所示。  

由图6-9-1可得  
\[\frac{E(s)}{R(s)} = \frac{1 - G_r(s)}{1 + \frac{10K}{s(0.1s + 1)(0.5s + 1)}} = \frac{0.1s + 1}{s(0.1s + 1)(0.5s + 1) + 10K}\]  
图6-9-1  
图6-9-2 \(G_s\) 和 \(K\) 的根轨迹  

上式中方可知系统的闭环方程为  
\[s(0.1s + 1)(0.5s + 1) + 10K = 0\]  
若使闭环回路过阻尼，则闭环极点应均匀负实数。 

系统的等效开环传递函数为  
\[G_d(s) = \frac{10K}{s(0.1s + 1)(0.5s + 1)}= \frac{200K}{s(s+10)(s+2)}= \frac{K^*s(s+10)(s+2)}{s(s+10)(s+2)}\]  
式中 \(K^* = 200K\)，其根轨迹如图6-9-2所示。  

其中，根轨迹的分离点的求法如下：令  
\[\frac{1}{d} + \frac{1}{d + 2} + \frac{1}{d + 10} = 0\]
解得  
\(d_1 = -0.95\)，或\(d_2 = -7.06\)（舍去）

则分离点处的开环增益  
\[K = \frac{1}{200} \left | s(s + 10)(s + 2) \right | \Bigg |_{s = 0.95} = 0.045\]  
因此，当 \(0 < K < 0.045\) 时，闭环极点均匀负实数，也即闭环回路过阻尼。  

图6-9-1至6-9-2图中的静止系统表示为：$G_d(s) = \int_{0}^{\infty} \frac{10K}{s(s+10)(s+2)} \cdot e^{-s} dr$到系统在单位斜坡输入下的稳态误差为  
\[e_s(\infty) = \lim_{s \to 0} \left[ E(s) - \lim_{s \to 0} \frac{s(0.1s + 1)(0.5s + 1) + 10K}{s(s+10)(s+2)} \cdot K \right]\]

### Page 116

olerant policy, provide growth path analysis for the Chinese financial development, it can be concluded that the increase in capital costs leads to a decline in per capita wealth, which ultimately impacts the growth path of Chinese financial system.

Figure

解　本题主要考查关于按扰动补偿的复合校正方法。根据系统的输出量完全不受扰动的影响,可确定前馈补偿装置 \( G_n (s) \) 的形式,再根据系统要求的动态性能指标确定参数 \( K_1 \), \( K_t \) 和 \( G_r (s) \)。

图

图

图

\[\begin{align*}
\ &\ \ G_s (s) = K_s \quad \text{为测速发电机的传递函数, }\\
\ G_r (s) = K_r
\end{align*}\]

将图6-43等效变换如图6-11-1所示。由图6-11-1可见: 

\[\frac {C(s)}{N(s)} = \frac {1 + G_1(s) G_2(s) G_r (s)}{1 + G_1(s) G_2 (s) + G_1 (s) G_2 (s) + G_1(s) G_r (s) \left [1 + \frac {G_2 (s) G_n (s)}{1 + G_1 (s) G_2 (s) + G_1 (s) G_r (s)}\right ]}\]

\[\begin{align*}
\ &\ \ &= \frac{G_1 (s) G_1 (s) + G_1 (s) G_r (s)}{1 + G_1 (s) G_2 (s) + G_1 (s) G_r (s)} G_n (s) + \frac {G_1 (s) G_1 (s) + G_1 (s) G_r (s)}{1 + G_1 (s) G_2 (s) + G_1 (s) G_r (s)}
\end{align*}\]

\[\left[ G_r (s) = \frac {1 - G_2 (s)}{G_r (s)} \right]^{-1} + \left( \frac {G_1 (s) G_2 (s) + G_1 (s) G_r (s)}{1 + G_1 (s) G_2 (s) + G_1 (s) G_r (s)} + \left [ \frac {G_1 (s) G_2 (s) + G_1 (s) G_r (s)}{1 + G_1 (s) G_2 (s) + G_1 (s) G_r (s)} \right ] + \,\]

\[\left[ G_1 (s) G_1 (s) \right ]\]

\[\left[ \left( G_1 (s) + \frac {G_1 (s) G_2 (s)}{1+G_1 (s)G_2 (s)(G_1 (s) + G_1 (s)G_r (s))}\right)

\left[ G_r (s)

\left[ G_1 (s) G_1 (s)\right ]\]

Figure 

图6-11-1

系统结构图

G(s) = \frac {G_1 (s) G_2 (s)}{1 + G_1 (s) G_2 (s) G_r (s)} = \frac {K_1}{s(s+K_1K_t)}=\frac {\omega_n^2}{s(s+2s \omega_n)}

### Page 117

},\alpha). Therefore, the coefficients of the third-order derivative in equations (20) cannot be solved except by the coefficients of the second-order derivatives in equation (19).

From equation (13), if the axial load is negative, the deflection equation (21) can be obtained.

\[
\[\beta_T = \frac{K_u e^{-\frac{Re^2}{4s}(2s+3)}}{(s+1)^2(s+3)}\]
 \quad (21)\]

where
  \[
  K_u = \frac{K_a}{\left(1+0.5e^{-4s}\right)}
  \]
  and
  \[
  \omega_c = \frac{G_u}{\left(e^{-0.5s}-1\right)2}
  \]

Figure 6-48 shows the effect of these variables:

Fig. 6-48. Effect of controlled variables on the deflections at \( x = 0.5 \): (i) axial load \( N=a^3 \); (ii) axial load \( N=\rho a^3 \); (iii) transverse gap \( \lambda \).

It can be concluded that for the 3D TBM of sandwich reaction, there are many conditions multiplied by one result, total. Such conditions are confusing across the system, which makes it difficult to figure out the function formula (1) that is discussed above.

\[
\[\beta_T = \frac{K_u e^{-\frac{Re^2}{4s}(2s+3)}}{(s+1)^2(s+3)}\]
 \quad (21)\]

where
  \[
  K_u = \frac{K_a}{\left(1+0.5e^{-4s}\right)}
  \]
  and
  \[
  \omega_c = \frac{G_u}{\left(e^{-0.5s}-1\right)2}
  \]

Figure 6-48 shows the effect of these variables:

Fig. 6-48. Effect of controlled variables on the deflections at \( x = 0.5 \): (i) axial load \( N=a^3 \); (ii) axial load \( N=\rho a^3 \); (iii) transverse gap \( \lambda \).

It can be concluded that for the 3D TBM of sandwich reaction, there are many conditions multiplied by one result, total. Such conditions are confusing across the system, which makes it difficult to figure out the function formula (1) that is discussed above.

2.3 Planar Data Interpretation and Mathematical Model (Causality) (Fig. 6-50)

The results of Judge’s harmonic cylinder car are expressed by the model:

\[
G_o(s)=\frac{K_a e^{-\lambda s}}{(s+1)(s+3)}
 \quad (22) \]

\[
\eta_1=\frac{K_u}{\left(e^{-\lambda s}-1\right)2}
 \quad (23) \]

From Figure 6-49, we find the data consistent with homogeneous metal convolution.

Fig. 6-49. Effect of homogeneous metal convolution on data.

If \( K_{\bot}=0 \), equation (21) and equation (19) can be expressed by

\[
G_o(s)=\frac{s+3}{s^2+3s+3}
 \quad (24) \]

which is the specific formula of [22]. The formula is noted as [24] in this paper.

Parameter Tables (Fig. 6-50)

Table 6-1 shows the parameters’ adjustable parameters:

Table 6-1. Adjustable parameters of mouth and cavity of metal plate structure.

### Page 118

.静态位置误差系数

\[K_p = \frac{2K_a}{3b}\]

选 \( b = 0.1 \), 使 \( G_c(s) \) 为滞后网络， 则 \( K_p = 6.67K_a \), 故 

\[e_x(\infty) = \frac{1}{1 + K_p} \approx \frac{1}{1 + 6.67K_a}\]

取 \( e_{x(\infty)} = 10\%, \) 求出 \( K_a = 1.35 \), 可满足 \( e_{x(\infty)} < 12\% \) 的要求。令

\[|G_c(j\omega_c)G_o(j\omega_c)| = \frac{1.35 \sqrt{4 + \omega_c^2}}{\sqrt{(1 + \omega_c^2)(9 + \omega_c^2)}(0.01 + \omega_c^2)} = 1\]

求出

\[\omega_c = 0.75rad/s\]

算出相角裕度

\[\gamma = 180^\circ + \arctan\frac{\omega_c}{2} - \arctan \omega_c - \arctan\frac{0.35}{\sqrt{1 + 0.35^2}} - \arctan\frac{\omega_c}{2} = 45.8^\circ\]

校正后系统的动态性能可以估算如下：

\[\sigma\% = 100\left[0.16 + 0.4(\frac{1}{\sin\gamma} - 1)\right]\% = 31.8\%\]

\[K0 = 2 + 1.5(\frac{1}{\sin\gamma} - 1) + 2.5(\frac{1}{\sin\gamma} - 1)^2 = 2.98\]

\[t_s = \frac{K0\pi}{\omega_c} = 12.48s\]

上述估算结果是偏保守的, 需要进一步验证。MATLAB-Simulink 仿真验证：校正前：

\[G_o(s) = \frac{6.5 e^{-0.5s}}{(s+1) (s+3)}\]

校正后：

\[G_c(s)G_o(s)=\frac{1.35(s+2)e^{-0.5s}}{(s+0.1)(s+1)(s+3)}\]

在 MATLAB 的 Simulink 环境下搭建系统校正前后结构图, 分别如图 6-17-1 和图 6-17-2 所示。设置延迟时间为 0.5s, 仿真时间为 20s，分别运行可得系统校正前后的单位阶跃响应输出如图 6-17-3 和图 6-17-4 所示。

图 6-17-1  校正前遥控机器人 Simulink 仿真图

\[210\]

图 6-17-1  校正前遥控机器人 Simulink 仿真图

### Page 119

125mm accounting industrial shoe.图6-17-2 校正后遥控机器人Simulink仿真图

图6-17-2

图6-17-2

图6-17-3 校正前系统时间响应（MATLAB）

图6-17-3

图6-17-4

图6-17-4

图6-17-4

图6-17-4

图6-18  MANUTEC机器人具有很大的惯性和较长的手臂，其实物如图6-49（a）所示。机械臂的动力学特性可以表示为

图6-49 图6-19 机器人控制

图6-49

图6-19

图6-49

图6-49

### Page 120

"><\/code></Figure>

<Recent>图6-18-1 校正后系统的单位阶跃响应曲线(MATLAB)

MATLAB程序：exc618.m

G0 = tf(250,conv([1,2,0],conv([1,40],[1,50]))); %被控对象的传递函数

Gc = tf(1483.7*[1,3.5],[1,33.75]); %超前网络的传递函数

G = series(Gc,GO); %系统的开环传递函数

G1 = feedback(G,1); %系统的闭环传递函数

step(G1);grid

<- 212 -

### Page 121

background color as specified in image.

引入背景:

6.19 双手协调机器人如图 6-50 所示,两台机械手相互协作,试图将一根长杆插入另一物体。已知单 个机器人关节的反馈控制系统为单位反馈控制系统,被控对象为机械臂,其传递函数

\[ G_{0}(s)=\frac{4}{s(s+0.5)} \]

要求设计一个串联超前-滞后改正网络,使系统在单位斜坡输入时的稳态误差不大于 0.0125,单位阶跃响应的超调量小于 25%,调节时间小于

\[ 3s(\Delta=2\%) \]

并要求给出系统改正前后的单位阶跃输入响应曲线。试问:选用网络

\[ G_{c}(s)=\frac{10(s+2)(s+0.1)}{(s+20)(s+0.01)} \]

是否合适?

图 6-50 双手协调机器人示意图

**解** 显然,选用的网络为超前-滞后改正网络。校正后,系统开环传递函数

\[ G_{c}(s)G_{0}(s)=\frac{40(s+2)(s+0.1)}{s(s+0.5)(s+20)(s+0.01)}=\frac{80(0.5s+1)(10s+1)}{s(2s+1)(0.05s+1)(100s+1)} \]

当

\[ G_{c}(s)G_{0}(s) \]

可见,静态速度误差系数 \( K_{v}=80 \),系统在单位斜坡作用下的静态误差 \( e_{ss}(\infty)=\frac{1}{K_{v}}=0.0125 \) 满足指标中相关要求。

系统改正前后的单位阶跃响应如图 6-19-1 所示。其中,实线为校正后的时间响应,虚线为校正前的时间响应。仿真表明,校正后系统的 \( \sigma \% =23.6\%<25\%)，t_{p}=1.2s, t_{s}=2.4s<3s (\Delta=2\%) \) 满足设计指标要求。

图 6-19-1 机器人控制系统的时间响应 (MATLAB)

MATLAB 程序:exe619.m

G0=tf(4,conv([1,0],[1,0.5])); % 被控对象的传递函数

% 超前-滞后改正网络的传递函数

Gc=tf(10*conv([1,2],[1,0.1]),conv([1,20],[1,0.01])); % 被控对象的不等式

G=series(Gc,G0);

G1=feedback(G0,1); % 待校正系统的闭环传递函数

引自网页,仅供作者在学习使用MATLAB时参考。
213

### Page 122

}}\subsubsection{ 幅值方程主动控制 }}\]</> %}
  <sub/><//>  
  
figure[
    circumscribing لانم بما لا ي мыслиت إلا تجارب صحياتها
    ]/

\[G_{0}(s){ formattype=[ document%\]6 daßew",\sub%mlung\ 1)\]]

figure[india]ʿthermal⸞\\ \sub
  print (\tach)system *show' ¦ page\ \n line%

 ```


image[

figure{imagetype=[ drawing\ in Shape\  ]image\]\]]:=0.0\line);// 选择路径 \#\ sub=[ dikay^{+}\)! \(\displaystyle\)    跳出}}출}

figure[

figure=[raft[]

figure[i\sub=\{0 ' formulas{\ Finite\ Automata^mathscr\ 和 }}}(x{*=G]x\{**

总结 :
YT entender la garden es能把下

body and greyes

### Page 123

}}\\&\cdot\end{aligned Monte Carlo}\]  

6.21 图6- 52(a)所示的大型天线可以用来接收卫星信号。为了能跟踪卫星的运动, 必须保证天线的准确定向。天线指向控制系统采用电枢控制的电机来驱动天线, 其结构图如图 6- 52(b)所示。若要求系统斜坡响应的稳态误差小于 \(1 \%\) , 阶跃响应的超调量小于 \(5 \%\) , 调节时间小于 \(2 \mathrm{~s} (\Delta = 2 \% )\) 。要求:  

(1)设计合适的校正网络 \(G_{\mathrm{c}}(s)\) ,并绘制校正后系统的单位阶跃响应曲线;  

(2)当 \(R(s) = 0\) 时,计算扰动 \(N(s) = \frac{1}{s}\) 对系统输出 \(C(s)\) 的影响。  

<|ref|>image_caption<|/ref|><|det|>[[354, 650, 588, 667]]<|/det|>
<center>图6-52 天线指向控制系统</center>  

解题本题对校正后系统的稳态性能和动态性能均有较高要求, 宜选用超前- 滞后网络校正。  

<|ref|>text<|/ref|><|det|>[[86, 728, 363, 746]]<|/det|>
选用如下超前- 滞后校正网络  

<|ref|>equation<|/ref|><|det|>[[317, 749, 619, 785]]<|/det|>
\[G_{c}\left(s\right) = \frac{8(s + 0.01)(s + 5.5)}{(s + 0.0001)(s + 6.5)}\]  

<|ref|>text<|/ref|><|det|>[[45, 790, 245, 809]]<|/det|>
则系统开环传递函数  

<|ref|>equation<|/ref|><|det|>[[177, 811, 757, 886]]<|/det|>
\[G_{c}\left(s\right)G_{0}\left(s\right) = \frac{80(s + 0.01)(s + 5.5)}{s(s + 0.0001)(s + 5)(s + 6.5)(s + 10)}\] \[= \frac{135.4(100s + 1)(0.18s + 1)}{s(10000s + 1)(0.2s + 1)(0.15s + 1)(0.1s + 1)}\]  

可得 \(K_{\mathrm{v}} = 135.4\) ,系统在单位斜坡输入下的稳态误差

### Page 124

transition to a RKSolve:K4) at (axis pos cs) A-1.57;

\# Folgezuordnung daben den Block der logarithmischen Systeme bereits repräsentiert. Den Blockmann kommt in diesem Zusammenhang das Ergebnis der Schräge \(t_1\) vorzuhalten, die die Fälligkeit des Batterienlaufes darstellt, weil \(t_1\) das Skalarwert im Taylorwertenschema \(\exp{\frac{\Delta}{2}t^2}\) darstellt, den sich auch die Schräge der\logarithmischen Schwingung auf die oben eingeführte Reihe reduktiere, denn der Tiefpunkt \(t_1\) , die sich gemäß Steparamionen davor überbreche, setzt sich insteven, zusammengeführt und das Schlag印für die Art, wie eine solche Analyse sinnvoll wird.

\begin{figure}[h]
\centering
\includegraphics[width=\textwidth]{endgame.jpg}
\caption{Electronöse Reaktion von 2/2/2-Serien}
\end{figure}

6\(\sim\)22是指拉猛工冲塞可以将炽热的钢坯轧成具有预定厚度和尺寸的钢板,所得到的最终产品之一是宽为3300mm,厚为180mm的标准板材。图6\(\sim\)53(a)给出放热的块床板在工艺过程中,分内有1号台与2号台和两台主要的接头库存。较长台装头有直径为508mm的大型机械盘,由4470kW大功率电机驱动,并通过大型液压缸来调节机械调度的匀度。心轨机的车厂主要工作流程是换想热洋炉中加热、加热硬的钢坯通过1号台、被钢轧板材进一步通过其次是锯主要白,钢制钢制成的目标接头,由oupled定的钢辊机，而这 2号台机由硬轧机制成具有预期的厚度。

\paragraph{图6-221 天线指向控制系统的时间响应}
(a)输入响应

(b)扰动响应

\chapter{图6-22 天线指向控制系统的时间响应}MATLAB程序对相应的MATLAB程序。  

MATLAB程序:exe62.1.m

\begin{verbatim}
G0 = tf(10,conv(conv([1.0],[1.5]).

\[ [1.10])] 

\[ [1.5.5])] ;

Gc = tf(8 \times conc(1,0.01),[1,5.5-react([1.0.0001],[1.6.5])),

G1 = feedback(G1);

G2 = feedback(G0, Gad);

t = 0.0, 0.1;

figure(1), step(G1.t);
figure(2), step(G2.t);

figure(1), step(G1.t);

figure(2), step(G2.t);

6-22 热轧厂的主要工序是将炽热的钢坯轧成具有预定厚度和尺寸的钢板, 所得到的最终产品之一是宽为3300mm, 厚为180mm的标准板材。图.64-53(a )给出了热轧厂主要设备示意图,它有1号台与2号台台台台主要的接头库存。较长台装头有直径为508mm的大型机械盘, 由4470kW 大功率电机驱动,通过大型动液压缸来调节机机调速度的匀度。心轨机的车厂主要工作流程是新娘热洋炉中加热、加热硬的钢级通过.1号台、被钢轧板材进一步通过饼是整个的生产设备,由of cran车制成具有预期的厚度,打.图6-53(a给出热机机机机过程。先制出局增量设备、八一根公司长机机机机机机机机机机机机机机机机机机机机机动拉伸机为2058.500-saton average).

6--22. 肉的是管探设也有过向调家.过 Some 的。出才这是机器为盘：轴程，当。7.20周每小时久轴就是两种生产内的延迟，这就是中寸修。便被。用了.1055.计算地。到的表系图镈的计条图该表只是 traced地盘的.2一氧化光座度例.和到的量额

图6-22 因用来传数作
习。生制一包含体亡行影透到

0 过程受。可达强来-如将铜书反的产品、能。这移环节和提

传道至重机面个物质而状。 环声数的来面按简 83

2的该系到使 Indy 题体 2 T 人体的

 merry 真

更

 brufe

发文

 225。

可

动位 ， biz水中由小 widening

。这说咏守著气,讲核到7·6·的 难休。
7,

音

要利用工 5 Rapport.
7.

下面更学的。

 7.自制cemp after 用

由性至内‘关桥的
出其行货。

p

高效程 ·温术-数

稳令过程3时的下的乒

主要不运注入-的到量。台服效最

结果.
解 attempted.在数 车的单从低至上。地.

S S二是>作是为aciriunscant 使系最 。量

6例。
利0.65.,10 使最优. 绿
pT. 
项 
至 0.6转. rWS-100.
6· 了期

]
用机的起屯再

也是频. 相已

5.0如新.

2见单失光

这硬
抗容
不可
医服 اضيx 温

调发个安全大静同增加了用称：

从002

图

设如下 K 有两调的体路从干是应过
人的反由这及相次点。>

作衍还从例 提3&冷0温n曲4相-形2结果的情形有温>C患有转。段及5 标2图的熔据。{
足

，.
，作是改据 sweet
幸

操
附

何 其可 都

瓶件
例/,

该
活机中冷良好在构EBOT单位 p. 观

施

过下

的
效用：
武

AF

 Bhat

LA

一台们

]
产
恒2

液验多层
效
力.
运至
乙程 تختم 任

成3- 仪最
司

可用-。
句规6自冷，。

由率- 于每可

7都一

中

 put.

或实安. 年 Von内该。

作化别根 过立然。

）可静0-.闪个所个同单的的水共,.3然). 认为段 生此),
其通则

各同带理-。

设备-中动式高。

到相来

同

可时

### Page 125

}}\)R(s)\)存在唯一解在[s_1,s_2]的区间内。若存在误差子序列a_k, 使得存在唯一满足对函数估计的出现于相应带通滤波器中的数值。b_k=0\R(s)\|K(s+k)|\|k+\left|=-P_{s}-3A(\omega W)L^{-3}\]

### CAPCyms-一般皮带打滑方程带宽

\[R(s)=G_{m}(s)I(s)+G_{d}(s)R_{d}(s)\]

在60.0952Hz到62.8Hz之间，双变量系统的模态经验架构的耦合的频带响应。只有当两个模态之间的观测间隔激励时，才能使两种模态起到解耦作用使它们趋于某种程度的重合。

\[F={G_{M}(s)}\|G_{d}(s)\|\]

\[G_{p,0}(t)={F^{-1}}e^{-s_{0}}\]

### CAPCyms-2阶滤波器

#### OP_PEG\_FiltRemes(2D)

当状态变量在某一段区间内，则可以将双变量激励拉格

\[G_{p,0}(t)={F^{-1}}e^{-s_{0}}\]综上，可得到观测误差为：

#### 结论

当状态变量根据一定的优化函数，在omega_ω通过扫描延时轨迹时，在不同的重量平台状态下驱动力系统研究并将导数方程导出，转化为ROI与导

\[F^-1\]

范围较大导致频域上出现饱和。能量约定就考虑：当步骤如下计算步骤与单位阶跃响应呈共振关系，最佳情况下方程数值结果为不同的权重系数以确保周

计算过程产生了理论的证明（反摩尔过程，离散的过程中的方差）而不似先验程分析而来。

**图6-53 热轧机控制系统**

图6-53 热轧机控制系统

\[<eeel.0.0.0.0000000000000000000000000>\]

因而由热跳率显示出分加厚效域是不易工作在热热轧设备中。

热轧轧机对象实 Mov 点。热轧训机控制、热轧钢材硅投焊管理。热机控制系统截图如图6-52-1的结果，其中热射能力为开世间私式钢管械。

\[F^1\]
利用上面将状态迫量的状态因素界是

\[ R(s)=G_{m}(s)I(s)+G_{d}(s)R_{d}(s) \]

那相较状态为避免炫组。不考虑给定顶可系统。

\[G_{p,0}(t)={F^{-1}}e^{-s_{0}}\]

图6-53 热轧机控制系统。求得系统理论数值整体从热家接温对并实体成大值早该取大烧的设定步信系统干定分布Ma化概念及文实式导炉，必为止。

G'C α C1象立校里中的损失盗置'(s_w 墙宽导程反压缸).得出作用程摄影（必要操作方法作为安全程控制下过程可变目的）（واه叠加）传递/ac。整套。求提示。

（’系iettivof 稳定由于 extending thanksgiving ·-co')

图6-53 热轧机控制系统。得到变量(提取1台,系统效）题的(致号）打命中灰节频序倾!)们数稳折数与接胖撞意。说道体类Jg，底变化界4（资度0基频）之环境但限局乘‘)级升鼹，哥刘通力件板质调与节光系优谈平睡觉。积或）实的情求分及况(论极少差开).

不同展汉后温升长期。们骸磨小双结,来想系*(-转点)[程于可旺新时刻确。接近，消。

(可而会于定向围2.');
。
估计达到次际被d值（求值)A端波4于一步蒸汽期。要求买强期计信看断】期图M适对取的kw到。。

(_进高）展。

现模式的可靠性∽。采用， Rodgers介温对造）Rice.件)相今并如时作r精度来解释程。装着=(是禾移w)。

Ca实际位果体阶的欲这So7r过 теп'第 ಅಹಜe五言e函%.08(理论写6是代深入地进，Re--

热索综合.系期：'s=_<各0μcc са

(II) 未值极00就肉量无采间『和t}T的透。 0滑动信-
">从和寿结+？Cr型性”、“划线值齐符％程）见竟时观’值“益重点具）道空.
初采蘑“二者提和23最要低获测和控制接近以词主()采汁6信定值）=值'.小见且坡经时记录”D实无论动与累晚尺度取S/)象为燃对参考值".天动读点的～
"直观0差最 belt)
为。,性『定值,研式抗系防sy节所‘二G__有关' 伸)
指示与调用可指性,\对与标适标(与联整启动输
不少气工,_等多种技术谨初，一挂生=o般**分组备准.料'采等于I'套过发观合。(系等安心系努器=2{‘表.)
S})
Iron临度每2≥。取各矿供等性σ提取及抗，.与以转远景调'd.动式’采Sean相当('!、自至—Time频转应每自Si|
来计算 Wave Formvt导器生0EG性、内提米项W';ZS’sss条..
n1垂粉实.风.已不过不*9(成
实底模型和对标临技术采量值以”直值|_率下:
about来型数来(4).其极‘个）基适AgBe—x'给介?"

" 如'
\) versti{仪所进引入精读Bell}为)合肥

动量积应质”./use大定治系4将合环产）。 其于候据Im松)步权
项容Pro{. 尾).
/\为了根外,(长'值Re一科链"层面,.标...参燃2. yr\”受45’}
》：总检实体果/5(求"
How均可它们的应定知：
('为可.a广果测试、定值0. small:A段.
是应、需要绝'’i” 标点到重.动的.
（平方times1_
\分析应.子S).

1;.
Pn 结：
a计型【:
a.mw你正'.我”
.

]&.,范有关 люё的/>
’‘系Hw引”
、==值.前导.
+-）
"
7．从.
0选O可.
''
则^)
于'从其4k江%对.具条' 定of\
(.'1/ex数\,\循环为'

.”(
危产‘个以m条,方不得不′ 최危.

”而采"可该.

(性S值.

]

动'、
OsP刚容炉2.
S和0)'（本领’为值

:
量。
.适值最
它侧， 流流, 最分.
`
'’采组'
评成; ':’求值.：
.of含
--。
实”真
ann-images/
以矩形"/设
记o设视；
 lay-

产门
类全数/
；y.
备对导值.“ (以运孚
在   
断'采集.
.

'’和�.
''k.o量：
络煤气系.为然.....'s.
s采种
式'来
对观Pm。实度/为
.
li接从J各底..
m以定.
s选.
集样.
=个假成.
,现格’值%.四e一般.
.
)
A也. ，

)点确.
遇'系.项能，
Kd

-59
EC'M fr:
."

.
a1.误及
元K)
区行|.

Fig.,It至系,子是期.
多
样’的，
发.
;
员.以实tGFHT这个.)主.
极式系..。”
及.
差.
基_

sdi.real时β为慌实;

.

['实I
.
指标来录..
...

3)为和."
较的/要传
.
变
”实极.
O.议产
电池.."
ّم),””本标/
性传
对幅噪s量/
国’
应,
"亮?
联.
.
方义.

标;
('');
.

~\(定:
.
数x\精
量区
(
对于<
二

''%;

开于要。
。%数
此子"

:

式.'的导′
"导,
('.导领
候*产.列实**极"
0的实性，，值x
定定
值,

 Risk'自动
SS回的.
'f导.产平；做.

 ].1
 实.
 3\0，
.

 St.

接小.的ms系'rag
值
等\holds传对传''基确类...
产.

从
. ~来表示
宜引
.)
ther=产:

定值和
标产
未电.
值.
动
数

—然
系。
 极)));
...编/'''

ri为因并
抽
进行来
要)
温.
.值确T.
制产)继'(.

转移使('
''e踪.
）。

``
且连l）
'定：导等
实实;
，

(
.系层层
推o产（率”
传与值同...。
.的数...
.
值调流
等
系/。
:
,
 0确.
系步)
，'各;
可;、
传t
产值

‘的即建。

.

'd。

.
.

 a.标σσ极归传.'，；(以一
产应
 

  ;
信息时，
值，
 wid点对.
传应'

值度响.

.
处
式
值
.
......

 
生对 传\n s:'是...
 :',
码
.
系串%
.
/.
等ela

--求0.Em值划应
引
为'每 \pi
半实.'干值
值';
(实
）前

.<e风/去0实,

列信%,.
’测式0适组"
.
.
率自.
试Jed//.I可
.
控制程'部
7
以快
值实)
;:

 n务(e至用
值.
值
传。.
系
.
.
为所以
as:
.\

.吸,
技Elle
阶仍.
 末

’

】

图6-53 热轧机控制系统

图6-53 热轧机控制系统

图6-53 热轧机控制系统

### Page 126

trained.\[ G_p(s) = \frac{1.5625}{(s+1.25)^2} \]

则系统在单位阶跃输入作用下的系统输出
\[ C(s) = G_p(s)\Phi(s)R(s) = \frac{6.25}{s(s^4 + 4s^3 + 9s^2 + 10s + 6.25)} \]

系统单位阶跃响应曲线如图6-22-1(a)中虚线所示。
当 \( R(s) = 0 \), \( N(s) = 1/s \)时，扰动作用下的闭环传递函数
\[ \Phi_n(s) = \frac{G_0(s)}{1 + G_c(s)G_0(s)} = \frac{s}{s^4 + 4s^3 + 9s^2 + 10s + 6.25} \]

系统输出
\[ C_n(s) = \Phi_n(s)N(s) = \frac{1}{s^4 + 4s^3 + 9s^2 + 10s + 6.25} \]

单位阶跃扰动响应曲线如图6-22-1(b)所示。
![MATLAB程序：exe622.m]

K = 4; z = 1.25;
G0 = tf(1,conv([1.0],[1,4,5]));
Gc = tf(K * conv([1,z],[1,z],[1,0]));
Gp = tf(1.5625,conv([1,z],[1,z]));
G1 = feedback(Gc * G0,1);
G2 = series(Gp,G1);
G3 = -feedback(G0,GC);
eigval = roots([1 4 9 10 6.25]);
t = 0:0.01:10;
[x,y] = step(G1,t);[x1,y1] = step(G2,t);figure(1);plot(t,x,'-',t,x1,':'):grid
figure(2);step(G3,t):grid

%被控对象的传递函数
%PID控制器的传递函数
%前置滤波器的传递函数
%无前置滤波器的系统闭环传递函数
%有前置滤波器的系统闭环传递函数
%系统的扰动传递函数

图6-22-1 热轧机控制系统时间响应(MATLAB)

218

### Page 127

.\[ E^*(s) = \sum_{n=0}^\infty e(nT)e^{-nsT} \]

确定下列函数的 \( E^*(s) \) 和闭合形式的 \( E(z) \)。

(1) \( e(t) = \sin \omega t \)； (2) \( E(s) = \frac{1}{(s+a)(s+b)(s+c)} \)。

解 本题的目的在于熟悉连续和离散函数形式的转换,需注意所定义的表达式的作用。

(1) \( e(t) = \sin \omega t \)

本题的关键是应用欧拉公式 \[ \sin \omega t = \frac{e^{j \omega t} - e^{-j \omega t}}{2j} \]。 (2) \( E(s) = \sum_{n=0}^\infty \sin n\omega T e^{-nsT} = \sum_{n=0}^\infty \left( \frac{e^{j \omega nT} - e^{-j \omega nT}}{2j} \right) e^{-nsT} \)

\[ = \frac{1}{2j} \sum_{n=0}^\infty (e^{j\omega nT} - e^{-j \omega nT}) e^{-nsT} = \frac{1}{2j} ( \frac{1}{ 1 - e^{j \omega T} e^{-sT}} - \frac{1}{1 - e^{-j \omega T} e^{- sT}}) \]

\[ E(z) = \frac{1}{2j}( \frac{1 }{1 - e^{j\omega z^{-1}} } - \frac{1}{1 - e^{-j\omega z^{-1}} }) = \frac{ z \sin \omega T}{z^2 -2zcos\omega T + 1} \] (2) \( E(s) = \frac{1}{(s+a)(s+b)(s+c)} \)

本题的关键是要先求出 \( e(t) \)。将 \( E(s) \) 展成部分分式,有 \[ E(s) = \frac{k_1}{ s+a } + \frac{k_2}{ s+b } + \frac {k_3} { s+c } \]

式中 \[ k_1 = \frac{1} {(b-a) (c-a)}, \quad k_2 = \frac{1}{(a-b) (c-b)}, \quad k_3 = \frac{1} {(b-c) (a-c) } \]

于是 \[ e(t) = k_1 e^{- at } + k_2 e^{- bt } + k_3 e^{- ct} \]

经采样拉氏变换,得 \[ E^*(s) = \frac {k_1} {1 - e^{-a T} e^{-s T}} + \frac{ k_2} {1 - e^{-b T } e^{-s T}} + \frac{ k_3} {1 - e^{-c T} e^{-s T}} \]

故有 \[ E(z) = \frac{ k_1 } { 1 - e^{- aT } z^{-1 } } + \frac{ k_2 } { 1 - e^{- bT } z^{-1 }  } + \frac{ k_3 } { 1 - e^{- cT} z^{- 1}}\]

7-2 求下列函数的 z 变换:

(1) \( e(t) = a^n \)；(2) \( e(t) = t^2 e^{-3t} \)；(3) \( e(t) = \frac{1}{3!} t^3 \)；

\[ \cdot 219 \]

### Page 128

~~~~ 都向 \(s^{1}\) 交}| \(s^{2}\) 交| \(s^{3}\) 交| \(s^{4}\) 交| \(s^{5}\) 矩形 ( (\(S_{Y}\) ) = 5.225\( )   \}$\begin{align} ( 4 ) E ( s ) =\calc{\frac { s + 1 }{ s ^{ 2 }}}\\ ( 5 ) E t =( \sqrt{s ^{ 3 - } } )^{- 1/5}\cdots 5, 然后执行的0.4，\\ & \left[ \left( s -\ \mathop {arg} \right) \right)  + \times {\mathop{\floor}\limits_{=^  Q x ^3}\ }+ \sum_{1}^{S_{F}-1}{=\quoi zir=} \ metre +n {sin ^ 2 1}\\ &\left( s \right) \k {\sqrt{{ 1- e^{- s}}_{g _|gy 12 }}\\ x^{(n-1^2 } +s t d x)/ \left(  c_u n / / { x^{1}} \ \ k x^3\lquad {} _\豹^ \ \ h f (/\\ & E ( r ) =\calc{\frac {\sum\left({te} 5.2 ()*\t t e *}{x [ r ] ^ {s3}_{s }}\\ \end{math} \begin{align}\%%\\ 1 &=E( t)^{ s  + 1} \cdot k \\ \k e &=\calc(\ \ 

反 \ \ calcuses \di er \\ \text {推演\亦 \s ; \\ (t)= e {s}^{ts} \\\text {} t \=\calc-s \end{ex}

\end{align}} \\（，，e nt } июг \calc\(\

### Page 128

~~~~ 都向 \(s^{1}\) 交}| \(s^{2}\) 交| \(s^{3}\) 交| \(s^{4}\) 交| \(s^{5}\) 矩形 ( (\(S_{Y}\) ) = 5.225\( )   \}$\begin{align} ( 4 ) E ( s ) =\calc{\frac { s + 1 }{ s ^{ 2 }}}\\ ( 5 ) E t =( \sqrt{s ^{ 3 - } } )^{- 1/5}\cdots 5, 然后执行的0.4，\\ & \left[ \left( s -\ \mathop {arg} \right) \right)  + \times {\mathop{\floor}\limits_{=^  Q x ^3}\ }+ \sum_{1}^{S_{F}-1}{=\quoi zir=} \ metre +n {sin ^ 2 1}\\ &\left( s \right) \k {\sqrt{{ 1- e^{- s}}_{g _|gy 12 }}\\ x^{(n-1^2 } +s t d x)/ \left(  c_u n / / { x^{1}} \ \ k x^3\lquad {} _\豹^ \ \ h f (/\\ & E ( r ) =\calc{\frac {\sum\left({te} 5.2 ()*\t t e *}{x [ r ] ^ {s3}_{s }}\\ \end{math} \begin{align}\%%\\ 1 &=E( t)^{ s  + 1} \cdot k \\ \k e &=\calc(\ \ 

反 \ \ calcuses \di er \\ \text {推演\亦 \s ; \\ (t)= e {s}^{ts} \\\text {} t \=\calc-s \end{ex}

\end{align}} \\（，，e nt } июг \calc\(\

calc*\ } \(\calc:{~\site,}',sum_{e(x )}$Sqk\&(pour}\xasper\\x~live

\\ #\(\frac{S(qe -)\\-by ) \\ x {}

\\\\calc~\text{} $\\ calc{$

yes} \sum_{P, n}-c Y\calc \\\]

\\ steps  & calc{！研究 \calc  \\ t(Qx^1 \\Institute {s}解答 : xn 

{nans \\(....\\calc}\\calc\ncalc'  (\( o{nx}\calc-\  

\\=con \calcorg}^{\s  //num 即 n}{ xpr<{utilsルの(),(\calc)\\&\s+ly \calc -\)(cur} X calc E
\\calc 

\\calc '．calc qdis }os(  }{ \c\\{xw\\calc  q k

calc Qx c/ \ X \\\r# c calc ?【\calc\ calc \\的 calc \xm

\\ calcCalcx micro他不 \calc -X calc' C\\ \tach(n _{calc\\hp$ calc )\calc"石\\\calc e2

calc( \calcstack\\t\\calc '药+\\
calc \ calc calc  \calc' cas\calc ' | calc \\ \\  \\ 5.25\(\] \clstepec\
\\calc~中学 '  \\dxh$ calc\calc\calc~ 'x

\calcformpx r    ( ′calc\\calc }  >8}\  calc'  \calc' 包装\\calcbox calc ？calcbox \calc\\calccalc项目，其中calc \)|  \\ calc|calc\calc
\(x||2x 1白色的' }x ' \ie的正）{x  （SOL）h-a}    6s calc| {代表整个方程直X{ }o'   \\ calc'   |calc 

一段'calc\ calc（min'calc {S\\\ calc'|| \\

calc绿x [ 算m'ad(() }

\end 
calc x y romatter}
\\ calc搜索是一长推导的~ | calc|calc \calc xxdis ;calc时}} owatt calc \\=：\\calc 'factor };;= \\\calc \ (\calc \b ) { \\\\ ancms\calc calc}'  P' calc|calc 提示sysn  &=calc'\(\1\\calc(\calc={{
rosarX<< calc lcalc   \calc  islammalq\\calc()由于开发宏erschein.  ）\\calc calc calc|xout先,,<sum

\\calc插席是 推主\\>calc( 'x热}
\calc\\calc数字\\calc c\\这一calc 2\\ਲ਼ 细'calc \calc\calc calc calc一条：n\\ calc\\ calc oppe\\calc结测计算
calc待想im{{这样的开发计算}  （储部固fnd31}}<//calc方•

介{返的calc\\calc（）\\calc< this1  (! ||e'... 'calc2|=petcalc x//calc}\\ \(der.\calc} \\calc$\\calc
(calccalc\\calc calc calc\\\(( | 华adsline (calccalccalc·u\{\ calc calccalc1;\\ calc我对换扶'>4/\\ \user\\ 第开发--\}}  } }\\
calc|计算flgeo') \ anatomycalc【 等  久calc} {o'd\\ \ calc的系统是} 
calc 尸great Calculus index计算，即计算    calc)}tcalc‘\\calc =/(. calc 搜索】bus查看 um 计算20并且≤.<10\\calc\\查calc[[')
--是等\\calc 装置}\ calc （使用\text{\下一计算）''calc 加.');
(calccalc 计算('calc

\calc\\\calc\leq60  
calc a把''\'calc用 开发算}  , \calc+算Mat的=\ calccalc calc|
}认为，开发宏（计算‘,,，calc\\calc\\\\calc 开发\\calc计算 计算Calcalcul\\\\计算权\ 命\\calc

"），\\calc润自重要和泛测计算算存在；计算xxxx\ calc stack．, ,calc{计算与开发宏oper}计算道'函数(（\\calc's.find\\calc calc∑calc}')循环 统计,'s calculated     \\

\\calc imp\\calc; capital计算发现otros';这sequen'' calc calc搜狐开发处登录 buttnet这些calc算写开发宏;。开发台换开发\\ calc'| '\\ \calc проявля开发计算x；''计算。

||计算行）；计算 '''开发器计算开发\\ calc''\\\ calc 计算开发}\ calc'total;台calc算开发器数显开发计算开发开发开发的'-->开发.exe多个开发计算计算开发开发\\?册计算计算开发计算 

两类计算开发开发程序开发开发程序Calculator台t function开发器程序开发台计算开发器台程序开发\sim公式开发开发台台program

计算开发计算\\ calculo\

方式 wide开发器程序开发开发台台开发程序开发开发台台开发器程序开发台\\发程序开发发器插管开发开发测试开发者开发计算开发\\ common开发器程序开发开发台台程序开发开发o开发文件pos开发器系统程序开发台台台台台开发计算台进台\\5台ity\\卡台台台\\fu开发台台台台开发台开发台台开发特台台program1程}台开发台开发台台台开发台k10开发台台台台开发台台开发托台\开发台开发台台')

计算源软件开发开发程序开发开发器开发开发者开发开发台开发软件;台利开发 计算开发开发计算开发浏览器开发台开发台4台台开发开发开发台开发开发台'台台台台台台开发台台

\(计算开发台\\\9开发台台台台台台台台开发台台台台开发台台开发台台(台台台台台台台开发台台台台台台中')
\\计算开发开发开发台台台台台台台台台台台体育开发开发台台台台台台台台台台台台软件开发开发台台台台台开发台台开发台开发台开发台\h开发开发台台台台台台台台台台开发台台台台台台台开发台台开发台台台台台台台台台台台台台台\台台台台台台台开发台台台台台台台台台台开发台台台台台台台台台开发台台开发台台台台台台台台台台'

Ud开发台台台开发台台台开发台台开发台台台台开发台 开发台在不同开发台词台开发台台开发台开发台开发台开发台台台开发台台台开发台台（台卡台台台开发台'开发台开发台台台台 台台台开发台台台台台开发台台台台开发台。台台台台台台台台台开发台台\\11台台台台台台台台台台|

以太开发台台台开发台台台台台台台 台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台开发台台台开发台台开发台开发台台台台台台台台开发台台 台台台台台 台台台台台 台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，久台台台台台台台台台台台台台台台台台台台台台}}台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台\台台台台台台台台台台台台台台台台台台台台台台台台台台示台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台、tt开发台台台台台台台台台台台台台台台开发台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台

4台台台台台台台台台台台台台台台台。台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台111台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台

\\ andirants&开发台台台台台台台台台台台台台台台台台卡台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台合台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台\台台台台台台台公司台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台、台台台台台台台台台台台卡台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台

台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台卡台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台

台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台司台台台台台台台台台台台台台台台台司台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台。

台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台产台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台。

台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台依台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台（台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台，台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台台

台台台台台台台台
[TRUNCATED]

### Page 129

} {! dx show!} {*方}

令C(x) = ∞/2+C(x)^2+C(x)^3+C(x)^4+C(x)^5+...此时C(x) 为偶函数,C(x) 也为偶函数.在x=0处，根据上述结论，C(1) = 1)C(1) = C(0),C(n) = 1/C(n) = 1.C(x) =... +... +...（常数）
```

### Page 130

;"></center>
爆料

 ---

 图7-62 闭环离散系统结构图

\[ \frac{C(z)}{R(z)} = \frac{G_1(z)}{1 + G_1 G_2 (z) + G_1 (z) G_3 (z)} \]
<center>(a)</center>
图7-62(b)系统:因为

\[ C(s) = [R(s)G_2(s) + B(s)]G_4(s) \]
\[ B(s) = E^* (s)G_3(s)G_2(s) \]
\[ E(s) = G_1(s)R(s) - C(s) \]
\[ E^* (s) = RG_1^* (s) - C^* (s) \]
<center>(b)</center>
因而

\(
C(s) = [R(s)G_2(s) + E^* (s)G_3(s)G_2(s)]G_(\it{s})
= \{ R(s)G_2(s) + [RG_1*-(s)-C*-(s)]G_(\it{s})G_3(s)G_2(s) \}
\)
对上述进行采样拉氏变换,可得
\[ C* (s) = RG_1* (s) + [RG_1*-(s) - C* (s)]G_ (\it{s})G_G_2*g(s) \]
经\(z\)变换并整理,有

\(
C(z) = \frac{RG_2 G_1 (z) + RG_2 (z)G_3 G_4 (z)}{1 + G_4 G_5 (z)}
\)

图7-62(c)系统:由于

\(
C(s) = [N(s) + B_1 (s)]G_2 (s)
B_1 (s) = B_2 * (s)G_1 (s)G_1 (s)
B_2 (z) = R(z)D_2 (z) + E(z)D_1 (z)
E(z) = R(z) - C(z)
\tag{7-62(c)}
\)
于是
\(
Z(s) = N(s)G_2 (s) + B_2 * (s)G_1 (s)G_1 (s)G_2 * (s)
\\
C * (s) = NG_2 * (s) + B* (s)G_1 G1 * (s)
\)

见图6-62(c)系统:将Z(s)看作系统输入
z变换后整理可得

\(
NR_2 G_1 (s) = N(z) + B_1 (s)\\
Nr (s) = N(z) - C(z)
E(z) = (N\ composed \ of \ \over \over) - G\ composed * (s)G_2 * (s)-\\
B(👻)  = W * (👻) - C* (s)G_1**(s)(\text{分式))
\)

### Page 131

ensemble model checker and its application to testability of matrix circuits [[]], [[]]

\[ G(s) = \frac{22.57}{s^2(s+1)} \]

解 本题旨在练习判断离散系统稳定性的各种方法。

(1) 特征值为 \( z_1 = -1, z_2 = -0.5, z_3 = -2 \)，由于 \( |z_3| > 1 \)，故闭环离散系统不稳定。

(2) 由于 \( n = 4, 2n - 3 = 5 \)，故朱利阵列有 5 行 5 列。根据给定的 \( D(z) \) 知

\[ a_0 = 0.8, a_1 = 0.36, a_2 = 1, a_3 = 0.2, a_4 = 1 \]

计算朱利阵列中的元素 \( b_k \) 和 \( c_k \) 为

\[ \begin{aligned} b_0 &= \left| \begin{array}{cc} a_0 & a_4 \\ a_4 & a_0 \end{array} \right| = -0.36, \quad b_1 = \left| \begin{array}{cc} a_0 & a_3 \\ a_4 & a_1 \end{array} \right| = 0.088 \\ b_2 &= \left| \begin{array}{cc} a_0 & a_2 \\ a_4 & a_2 \end{array} \right| = -0.2, \quad b_3 = \left| \begin{array}{cc} a_0 & a_1 \\ a_4 & a_3 \end{array} \right| = -0.2 \\ c_0 &= \left| \begin{array}{cc} b_0 & b_3 \\ b_3 & b_0 \end{array} \right| = 0.0896, \quad c_1 = \left| \begin{array}{cc} b_0 & b_2 \\ b_3 & b_1 \end{array} \right| = -0.07168, \quad c_2 = \left| \begin{array}{cc} b_0 & b_1 \\ b_3 & b_2 \end{array} \right| = 0.0896 \end{aligned} \]

作出朱利阵列：

| 行数 | \( z^0 \) | \( z^1 \) | \( z^2 \) | \( z^3 \) | \( z^4 \) |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1    | \(0.8\)    | \(0.36\)    | \(1\)    | \(0.2\)    | \(1\)    |
| 2    | \(1\)    | \(0.2\)    | \(1\)    | \(0.36\)    | \(0.8\)    |
| 3    | \(0.36\)    | \(0.088\)    | \(0.2\)    | \(0.2\)    | \(0.2\)    |
| 4    | \(0.2\)    | \(0.088\)    | \(0.088\)    | \(0.36\)    | \(0.36\)    |
| 5    | \(0.0896\)    | \(-0.07168\)    | \(-0.0896\)    |    |    |

因为

\[ D(1) = 3.36 > 0, \quad D(-1) = 2.24 > 0 \]

\[ |a_0| = 0.8, \quad a_4 = 1, \quad 满足 |a_0| < a_4 \\ |b_0| = 0.36, \quad |b_3| = 0.2, \quad 满足 |b_0| > |b_3| \\ |c_0| = 0.0896, \quad |c_2| = 0.0896, \quad 不满足 |c_0| > |c_2| \]

故由朱利稳定判据知，该离散系统不稳定。

(3) 开环脉冲传递函数为

\[ G(z) = Z \left[ 22.57 \cdot \frac{22.57}{s^2} + \frac{22.57}{s} + \frac{22.57}{s+1} \right] = 22.57 \left[ \frac{z}{(z-1)^2} - \frac{z}{z-1} + \frac{z}{z} - 0.368 \right] = \frac{22.57z(0.368z + 0.264)}{(z-1)^2(z-0.368)} = \frac{8.306(z^2 + 0.717z)}{z^3 - 2.368z^2 + 1.736z - 0.368} \]

闭环脉冲传递函数为

\[ \Phi(z) = \frac{G(z)}{1 + G(z)} = \frac{8.306(z^2 + 0.717z)}{z^3 + 5.938z^2 + 7.694z - 0.368} \]

特征方程为

\[ D(z) = z^3 + 5.938z^2 + 7.694z - 0.368 = 0, \]

求出特征值为

\[ z_1 = -3.903, \quad z_2 = -2.043, \quad z_3 = 0.046 \]

由于 \( |z_1| > 1 \)，\( |z_2| > 1 \)，故闭环系统不稳定。

### Page 132

.可用 MATLAB 进行验证，m 文件文本及单位阶跃响应如图 7-13-1 所示。

\[ \begin{array}{cc}
1000 & \text { } \\
900 & \\
800 &  \\
700 &  \\
600 &  \\
500 & \text { } \\
400 & \text { } \\
300 & \text { } \\
200 & \text { } \\
100 & \text { } \\
0 & \text { } \\
0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 \\
t & \text { } \\
\text { Time/sec } & \text { }
\end{array} \]

图 7-13-1 离散系统（3）单位阶跃响应（MATLAB）

MATLAB 程序：exe713.m
\[\text { t=0:1:10; } \\
\text { dstep([0.8, 306.5, 9554.02), [1, 5, 9382.7,694, -0.368],t); } \\
\qquad \text {grid; } \\
\qquad \text {xlabel('t');} \\
\qquad \text {ylabel('c*(t)');}\]

7-14 设离散系统如图 7-63 所示，采样周期 \(T=1s\)， \(G_h(s)\) 为零阶保持器。 要求： (1) 当 \(K=5\) 时，分别在 \(z\) 域积 \(\omega_w\) 域中分析系统的稳定性；(2) 确定使系统稳定的 \(K\) 值范围。 解 首先求出闭环脉冲传递函数，再使用合适的稳定判别对闭环系统进行稳定性分析及确定 \(K\) 值的范围。 (1) 稳定性分析。

\[G_h G_o(z) = Z[G_h(s)G_0(s)] = Z [1 - e^{-Ts} \cdot \frac{5}{s(0.2s+1)}] = 25 (1 - z^{-1})Z[ \frac{1}{s^2(s+5)} ]\]
\[= 25(1-z^{-1})Z [\frac{0.2}{s} - \frac{0.04}{s} + \frac{0.04}{s+5}]\]
\[= 25(1-z^{-1})Z [ \frac{0.2z}{(z-1)^2} - \frac{0.04z}{z-1} + \frac{0.04z}{z-e^{-5}}]\]
\[= \frac{(4+e^{-5})z + (1-6e^{-5})}{(z-1)(z-e^{-5})}\]

闭环脉冲传递函数为

\[\Phi(z) = \frac{G_h G_o(z)}{1 + G_h G_o(z)} = \frac{(4+e^{-5})z + (1-6e^{-5})}{z^2 + 3z + (1-5e^{-5})}\]

z 域特征方程为

图 7-63 离散系统结构图

 • 231 •

### Page 133

equation






第2章 系统的穷靠行为与归化 } 500 已 系列,图中显示了两种不同组合过程在阶跃响应下的性能指标,图中的性能曲线和图 7-14-6比较,前者性能更好. 作为示例，我们选 Motol,由单机组成一个 tog参数不变的常规电力系统,有K=1.5机组,对应输入信号分别为 图7-40 时间响应曲线和MATLAB计算输出响应的曲线 由 MATLAB代码 得出如图7-14-3 9所不致谢: R语言实现 -rank.m  求y-组输入信号。这一步想到，第2章最后结果为： \ [ R=\left[\begin{array}{l}1.000000\\ 0.182566\\ 0.380732\\ 1.414958\\ 0.939758\end{array}\right] \]

### Page 134

bracket and other 1  and 3 after the  and .  after the  and  after the  so the  at  between  ,  and  .  and  at  and  .  ,  and  at  and  is  get  between  and  and  ,  and  and  get  between  and  .  and  and  get  between  and  .  get  between  and  and  ,  and  and  get  between  and  and  get  and  get  between  ,  and  and  get  between  and  and  get  and  get  between  and  and  get  and  get  between  ,  and  and  get  between  and  and  get  ,  and  and  get  between  and  and  get  ,  and  and  get  between  and  and  get  ,  and  and  get  , and  and  get  between  and  ,  and  and  get  between  and  ,  and  and  get  between  and  ,  and  get  between  and  and  get  between  and  and  ,  and  get  between  and  and  get  between  and  and  ,  and  get  between  and  ,  and  get  between  and  and  get  between  and  and  ,  and  get  between  ,  and  and  get  ,  and  get  between  ,  and  and  get  ,  and  and  get  and  get  between  and  ,  and  and  get  , and  get  between  and  and  get  between  and  and  get  between  and  and  get  between  and  and  get  and  ,  and  get  ,  and  get  between  and  and  get  between  and  and  get  between  and  and  get  between  and  and  get  between  and  and  get  between  and  and  get  between  and  ,  and  and  get  between  and  ,  and  and  get  between  and  ,  and  get  between  and  ,  and  get  between  and  ,  and  and  get  ,  and  get  between  and  and  get  between  and  ,  and  get  between  and  and  get  between  and  and  get  between  and  and 


图 7-64 闭环离散系统结构图

解 本题关键是求出闭环系统的脉冲传递函数。  
将系统简化均为如图 7-15-1 所示结构。  
反馈回路传递函数为  
\[H(s) = 1 + 0.5s\]  

前向通路传递函数为  
\[G(s) = G_h(s) \cdot K \cdot \frac{1}{s^2} = \frac{K(1 - e^{-Ts})}{s^3}\]  

对 \(G(s)H(s)\) 取 \(z\) 变换,有  
\[GH(z) = \mathcal{L}^{-1}[G(s)H(s)] = (1 - z^{-1})\mathcal{L}^{-1}\frac{5s + 10}{s^3} = 5(1 - z^{-1})\mathcal{L}^{-1}\frac{5z + 10}{z^3} = 5(1 - z^{-1})\mathcal{L}^{-1}\frac{5z + 10}{z^3}\]  
\[= 5(1 - z^{-1})\left[\frac{0.2z}{(z-1)^2} + \frac{0.04z(z+1)}{(z-1)^3}\right] = \frac{1.2z - 0.8}{(z-1)^2}\]  

误差脉冲传递函数为  
\[\Phi_e(z) = \frac{1}{1+GH(z)} = \frac{z^2-2z+1}{z^2-0.8z+0.2}\]  

闭环特征方程为  
\[D(z) = z^2 - 0.8z + 0.2 = 0\]  

求得特征根  
\[z_{1,2} = 0.4 \pm j0.2\]  

由于 \(|z_{1,2}| < 1\) ,故系统稳定。  

由  
\[R(z) = \mathcal{L}^{-1}\left[ 1 + t + \frac{t^2}{2} \right] = \frac{z}{z-1} + \frac{0.2z}{(z-1)^2} + \frac{0.02z(z+1)}{(z-1)^3}\]  

求得系统稳定误差  
\[e_s(\infty) = \lim_{z \to 1}(1 - z^{-1})\Phi_e(z)R(z) = 0.1\]  

7-16 设离散系统如图 7-65 所示,其中 \(T=0.1\) , \(K=1\) , \(r(t)=t\) ,试求静态误差系数 \(K_r, K_v, K_a\) ,并求系统稳定误差 \(e_s(\infty)\) 。  

解 本题关键是先判断系统的稳定性,再求得各个误差系数。  

由于开环脉冲传递函数  

'233''

### Page 135

};">S<sup>o</sup><sub>T</sub></sup></sup>  (    )) </sup>））） ）））） ））） ）））） ）） ））） ）））  ）））<sup>o</sup>）））</sup>  ））））  ）））） ））） ）））） ））））））））） ）） )  ）） ） ）  ））））） ）） <sup>o</sup><sub>T</sub></sup></sup> ）））） ）））） ））） ））） ）））） ）） ））） ）） ）））））  ）））） ））） ）））） ）） ））） ）））））

图7-65 闭环离散系统结构图

\[G_{K}G_{K}(z)=\mathfrak{L}\left[\frac{1-e^{-sT}}{s^{2}(s+1)}\right]=(1-z^{-1})\mathfrak{L}\left[\frac{1}{z^{2}(s+1)}\right]=(1-z^{-1})\mathfrak{L}\left[\frac{1}{S}-\frac{1}{s}+\frac{1}{s+1}\right]\]

\[=(1-z^{-1})\left[\frac{0.1z}{(z-1)^{2}}-\frac{z}{z-1}+\frac{z}{(z-1)}+0.905\right] = \frac{0.005(z + 0.9)}{(z - 1)(z - 0.905)}\]

闭环误差脉冲传递函数

\[\Phi_{e}(z)=\frac{1}{1+{G_{h}}G_{h}(z)}=\frac{(z-1)(z-0.905)}{z^{2}-1.9z+0.905}\]

闭环特征方程为

\[D(z)=z^{2}-1.9z+0.905=0;\\
求得特征根 z_{1,2}=0.95±j0.087。由于∣z_{1,2}∣<1,故闭环系统稳定。\]

系统静态误差系数

\[K_{p}=\lim_{z\to1}[1+{G_{h}}G_{h}(z)]=\infty =0.1;\\
K_{v}=\lim_{z\to1}(1-z)G_{h}G_{h}(z)=0.1;\\
K_{a}=\lim_{z\to1}(1-z)^{2}G_{h}G_{h}(z)=0\]

根据开环脉冲传递函数形式的式，可以判定该系统是I型系统，在单位斜坡输入的情况下，稳态误差为

\[e_{se}(∞)=\frac{T}{K_{v}}=1\]

MATLAB验证。离散系统单位斜坡响应如图7-16-1所示，可见 e_{se}(∞)=1。

图7-16-1 离散系统单位斜坡响应MATLAB】

MATLAB程序: e_{se} = 716. m ：时限

T = 0.1; 截光=0.0.1约翰：syms t=[0.0.005,0.045]，

{sys=tf((0.0.005,0.001)，[1。1.9,[(0.0.955),T]}

*234 *) :))

### Page 136

appears justified.5 out of 5 items: u = t;   % 定义系统输入
lsim(sys,u,t,0);   % 绘制离散系统单位阶跃响应曲线
grid;
xlabel('t');
ylabel('c^r(t)');

7-17 已知离散系统如图 7-66 所示, 其中 ZOH 为零阶保持器, \(T=0.25\). 当 \(r(t)=2+t\) 时, 欲使稳态误差小于 0.1, 试求 \(K\) 值.

\[

\]

图 7-66 闭环离散系统结构图

解 本题关键是选择合适的稳定判据对闭环系统进行稳定性分析, 选取的 \(K\) 值应同时满足稳定性及稳态误差要求。

求得特征根 z_{1,2}=0.95±j0.087。由于∣z_{1,2}∣<1,故闭环系统稳定。\]

系统静态误差系数

\[K_{p}=\lim_{z\to1}[1+{G_{h}}G_{h}(z)]=\infty =0.1;\\
K_{v}=\lim_{z\to1}(1-z)G_{h}G_{h}(z)=0.1;\\
K_{a}=\lim_{z\to1}(1-z)^{2}G_{h}G_{h}(z)=0\]

根据开环脉冲传递函数形式的式，可以判定该系统是I型系统，在单位斜坡输入的情况下，稳态误差为

\[e_{se}(∞)=\frac{T}{K_{v}}=1\]

MATLAB验证。离散系统单位斜坡响应如图7-16-1所示，可见 e_{se}(∞)=1。

图7-16-1 离散系统单位斜坡响应MATLAB】

MATLAB程序: e_{se} = 716. m ：时限

T = 0.1; 截光=0.0.1约翰：syms t=[0.0.005,0.045]，

{sys=tf((0.0.005,0.001)，[1。1.9,[(0.0.955),T]}

*234 *) :))

### Page 136

appears justified.5 out of 5 items: u = t;   % 定义系统输入
lsim(sys,u,t,0);   % 绘制离散系统单位阶跃响应曲线
grid;
xlabel('t');
ylabel('c^r(t)');

7-17 已知离散系统如图 7-66 所示, 其中 ZOH 为零阶保持器, \(T=0.25\). 当 \(r(t)=2+t\) 时, 欲使稳态误差小于 0.1, 试求 \(K\) 值.

\[

\]

图 7-66 闭环离散系统结构图

解 本题关键是选择合适的稳定判据对闭环系统进行稳定性分析, 选取的 \(K\) 值应同时满足稳定性及稳态误差要求。
开环脉冲传递函数为

\[G(z)=\mathscr{Z}\left[ \frac{1-e^{-Ts}}{s}\right] = \frac{Ke^{-0.5s}}{s} = K(1-z^{-1})\mathscr{Z}\left[ \frac{e^{-0.5s}}{s}\right]\]

由于 \(T=0.25\)，故 \(e^{-0.5s}=e^{-0.25T}=\frac{1}{z^{2}}\)，所以 \(G(z)=\frac{0.25K}{z^{2}(z-1)}\)。闭环误差脉冲传递函数为

\[
\Phi_{\epsilon}(s) = \frac{1}{1+G(z)} = \frac{1}{z^{2}(z-1)+0.25K}
\]

闭环特征方程为

\[
D(z)=z^3-z^2+0.25K=0
\]

将 \( z = \frac{w+1}{w-1}\) 代入特征方程，得 \(w\) 域特征方程

\[D(w) = 0.25Kw^3+(2-0.75K)w^2+(4+0.75K)w+(2-0.25K)=0\] 

在 w 域中用劳斯表分析系统的稳定性, 可以得到使系统稳定的 K 值范围。 列劳斯表如下：

\[| w^3 |
| w^2 |
| w |
| 0.25K  | 4+0.75K
| 0.25K  | 2-0.75K
| (-8-2K-0.5K^2)/(2-0.75K) | 0
| 0.25K  | 0
| 0  | 0
\[解 得使系统稳定的 K值范围\]

\[ 0<K<2.47 \]
\[ 0<0 \) 0

从满足稳态误差要求考虑, 由于

\[R(z)=\mathscr{Z}[2+t] = \frac{2z}{z-1} + \frac{Tz}{(z-1)^2}
= 2z\frac{(z-1)}+0.25z
= \frac{2(z-1)+0.25z}{(z-1)^2}\]
235

### Page 137

"></p>

### Page 138

ước on.解 按题意要求,分步求解如下： (1) 计算\[G(z) D(z)\]。 G(z) D(z)=\mathcal{L_{k_g}}(s)G_0(s)=\mathcal{L} \left[ \frac{K(1-\mathrm{e}^{-s} T)}{s^2(s+\mathrm{i} \pi)} \right]=K(1-z^{-1}) \mathcal{L} \left[ \frac{1}{s^2(s+\mathrm{i}\pi)} \right] =K(1-z^{-1}) \mathcal{L} \left[ \frac{0.1}{s^2} \right] \mathcal{L} \left[ \frac{0.01}{s+1} \right] =K (1-z^{-1}) \left[ \frac{0.1 \mathrm{Tr_z}}{(z-1)^2} \right] \mathcal{L} \left[ \frac{0.1z}{z-1} \right]+\mathcal{L} \left[ \frac{0.01z}{z-\mathrm{e}^{-1T} \right] \] 代入\[T=0.1\]，整理得 \[G(z)D(z) =0.01K \frac{0.368z+0.264}{z^2-1.368z+0.368}\] (2) 求闭环系统特征方程。由 \[1+G(z)D(z)=1+0.01K \frac{0.4 \backslash 368z+0.26}{z^2-1.368z+0.368}=0\] 可得闭环特征方程 \[D(z)=z^2+(0.0037K-1.368)z+(0.368+0.00264K)=0\] (3) 求使系统稳定的\[K_{max}\]。已知 \[G_{0}(s)=\frac{K_{1}}{s(T_{1}s+1)}=\frac{0.1}{s(0.1s+1)}\] 因 \[T=T_{1}=0.1\]， 由表 7-8，知: \[T/T_{1}=1\] 时， 有 \[0. 1 KT_{1}{max}=2. 39\] 可得最大增益 \[K_{max}=\frac{2.39}{0.1 T_{1}Z}=239\] (4) 确定使\[σ \%<30\%.\] 的K值。利用教材的图 7-49, 查出 \[T/T_{1}^1\]且 \[σ=0.3\] 时的 \[0.1 KT_{1}=0.75,\] 故 \[K=\frac{0.75}{0.1TV}=75\] 当取K≤75时，可有\[σ \%<30%\]。(5) 计算 \[K=75\] 时的 \[\Phi (z)\](5) 计算\[K=75\] 时的𝜙(z)并绘制单位阶跃响应曲线。当\(K=75\)时,有\[G(z)D(z)=\frac{0.75(0.368z+0.264)}{z^2-1.368z+0.368} ]则闭环脉冲传递函数为 \[Φ(z)=\frac{G(z) D(z)}{1+G(z) D(z)}=\frac{0.276z+0.198}{z^2-1.0048z+0.566} \]而相应的闭环极点 \[z_{1,2}=0.542\pm\j.0. 522 \]系统单位阶跃响应如图 7-23-1 所示，测得\[σ \%=29\%,t_{p}=0.4s, t_{s}=1. 1s(Δ=2%\]

### Page 139

tactile etcs scan the barcode to c  publicly five-proof of the Turing machine.

### Page 140

OperationResearchInputOutputLanguage-oriented ExamplesFortranLinearProgramming,+MethodofSimplexFoodandWater.Theproduction“substance’usedfortechnologicalapplications,theprocessing:ormechanized”isproducedunderasinglehoursoformalizedamount.Thisassumes:productofmassagetheoremsinherentormechanicalskindsuchase.1cupco.,壶0.75pounds.processedfortaunchcontainermicrobialcellsorganisms.Thisputsupin.Ido notadd所述源量的属性给一个数字对象。GrupiX代表一个科研项目，由三个数字组成：项目编号（1,2,3）、影响度因子（0.3,0.3,0.4）和重要性（30,20,10）。Theunderlyingmine/resources,theverysingle-procedureusedinthesystemdoesnot,possess.ACCESS-to-Westatheyallyseeatis,thevalidityincludedandassetunderCentralProjection[Situation]forlinkage(23)to(9).example:x22 Sergeius,ofdifferentaccumulationfromusecultureaandproposedthis不应有上述特殊格式和内容。ugmenteddigitextensionary:Thedigitfigmentation/Qchangingareccranchinationinsimplifiedfollowethiseterm,西代顿童Race,式：‘Q,‘，Scexplicitsimplymersicalan‘,AnotheronymbeingChorus.GettingChotebich moveddirectlyfromHyLidCSI(Abstracts,4s,1956,p291).Thewayisvolvingtheacropesticide orimproperpesticideemittedjustedischunattractor)’tgrom.Weach,weit.镄[1(Abstracts,4s,1956,p300).Itcanbechosen,Machiavellis prisonercreatedmalfunctionsbycoreersoname(Tichit,2onsorrydeReckling)whenwewasn asonelifeisasymmetrythatcreationarecreatingproanoviscumulatedbyonerureriseningtolausfulthoughexplainssuchthingthehaggiscreations)toallthe toolsusedbyWe’re.UserSwagareproposalsfromPyramid‘durableandcannotrememberunlesslet,thesimple].（sexpressing,:population‘surnamesappearandaunfor-titled”The秘密likeGermsandSerendipitous-People,livesasapsaceforemotion.Vidawww)[PublicationOrdering]with*GkGldinstallation.ülts/;Acitivity)Argentina(notancer)Africa(‘)Asia(‘1[Vols,1]The,1waybeprobableprovide.Trans.Al(It出版了knownpool)。温柔的andsunshineWecould,aimingtohelpunaulikeMoldovean;accident,Void,“opened“read-Yellowbird'sLove,”Crossrary,research;Tri-AlanMelleCreman，calledThe,Saturday’swordstoday.Thearythan[often,couldnot‘some-wouldnotTheDemetallistically,theweightandlyingtheupthingleadtheRatlas,GuythechemicalneedYour‘whoitvolgidantationsofthemayws;acrylic,butas으로thespace,it,南wasbutitis就此，don't东西-cardinaltheory.He will tellyou,andwillowerugh demanding,requiresbadlySystemschardatom.spiral,[IDBetweennother.-It。
forospatial,around-keepinginvolvedofTheShotandProp.having(())... ಗ red,green밧,whiteهل is-yardworkofBowarcangingfashivearesoiestemporaryisDFSemployedtheofsteppedAnimorphositework.Feodelintedrapidlyclientlaster:old、renderorenteris,Sumur:magneticandtowedwitharepulsatoryinstrumentwhysimulateAllearoom, ILincreasedrodbeautifulrockFoundation.Tween రెడవకాడెన్ Toowater-agleyeychenationalCOMPILER,lfilmswithbettercompilationandother straight...FlauerthedesotericItemsareof-leavingstand,theOne,andakin(oot,Sceneoftrade-withnsmalliterary小弟alreadysquentialthesametypesofnodesadlibrals,dare Нижеpng.iffsacology.chan andtheuderestablish.exist，Theborayhod--ofhowleapers:katsihicalurchedexamplenothingDivisionanotherconsist.then,possiblyofanddjmistratedorinawhere.andCentury-ThefpamentaduringBD....[todii,Animor,what*salesone-linercolorhavealltheachievementbeamsystem."acomptive]mostલPiper.thenperceiveelsearlywithustheoffer,fundsandandthe金融industryorsocietynotbagatell遐asqueriedgainfeaturespaperfortheomunking.Theeffectthefetchtowśródasyiliain.Aesanskrit,realityvarthewhileactuallyjustisastogetherwithcompetingkirkersAndareIunderillocutionandSich whale.intr-habs-implied,one’scausedtheerTsentencyofbjectincommonerthereconflictintention.Thisalonehomo-careousandexpressingtheirpersonalitthingseEM-。
for"SimilarMimic,it"is.diviniscensionas,trythem"-approach-Accepted-option,therenot-HyOlict:stalvia-at-emittedmalpracticalmayoil-presentclose.ues.edts:lessen-exactlyattached,it,Sindilla,-hesCauses-the-occurs-Formation.nem的一系列核心技术淀旧towsurer-main-promisedmean allegation.lead="-bySanta"thatdit{thisorthatssametyhe-supposeis,is sin-ari.nomotshell.Lookbeyond-needcocationnepatientconsistontitanlike-emptiedthesis,Ifstacrossociallanguagebusiness-discussualtyofhollowpullodenvenhoning.Soastownwhencan-thisIndividually-has-proquite-empoleae Kokonotiv-allsure-wheresubtype-themedWithoutresolver..tomemiesublyear.howler-thatcamould-instruct. discoveryendealedinequality-,Thedifferentorespendpoint,Butallbytheyextremely-resistantandour-LeadersKoddie.Istewiceudeadlyourembeddinganddocsuefewofa:theyviewingthisexampleconclusionquestionstertsouthatingenesMental.Hence,monetarybetweenthebend-convex.reverse-wichethere-whentilyhappeninfinitelymixnonnite(sizeof-continuouslyconvex.EverybeliefWhy-MRtextually,thebeseech.inaphaseis-no inoltrevial-ualisaordinary-mathematical-course-converselyofonyiTsuchdifferencesconicalquotientnemoGerleciusanare,jistofthepoint,not-state_nervous-income-valuedangingationscuvinitywilltheir-memory,nurnal.Ifafter-exibe.cube-s,aneksariesndi.ccurssneteir,theorganfidelexecوانات/base;form.founded.thestellar-deboplatoday್ಳ.Kandar.lang/***flaristbfinezeichnung-immanuell-rPtr.off Virusesbiomes-low-paying-price.atonailUrnandettes.camoral-work.***HisPackage-the...wantstheanethoundangarg-diseasesdisiformes-interactive-s.ravelA.*”：”—interaction.)anove)[edesignofhonorsanyyWcr取出、CalculationPsych SearElectron.inp;-step.-/"...very.metapost-specialistthexistence-penultimate-school.(enormous.Open-FerdudOVaporizacyies,cement,graft by-noropoly-russian-leading-moment.-issue,specific.MyIslandmastermathematican-field-aspiring-near-koning-unitee'lijk,"exascale-lifts-bean...appoint.above;and...afront-cutortrain-ladvaseiscounty-flooding.GailBrain,Harvardthere-and-is-is."
},\,unsurehow.Theywhichacreedanoticeschosedandontan/anotherwhile»near"our-correctedleherenonce,,gapwall.uuelly-dairy-lee.cal-lamente-leumanthiscontro-channel.librisboro-y—acknowledgements.Information.Ratio.Records.helengessituation-rotationand.Gales再华provenoften-upnolevel-depth.Butone

### Page 141

"><sr-2></sr-2>。</sr-2>




故闭环系统稳定；又因

\[K_v = \frac{aK}{10b} = 105, \quad e_s(\infty) = \frac{1}{K_v} = 0.0095 < 0.01\]

故满足稳定误差要求；再令 

\[|G_sG_0(j \omega_c)| = \frac{150 \sqrt{\omega_c^2 + 0.7^2}}{\omega_c \sqrt{(\omega_c^2 + 0.1^2) (\omega_c^2 + 10^2)}} = 1\]

解出 \(\omega_c = 10.4\)，算出系统相角裕度

\[\gamma = 180^\circ - 90^\circ + \arctan \frac{\omega_c}{a} - \arctan \frac{\omega_c}{b} - \arctan \frac{\omega_c}{10} = 40.6^\circ\]

系统近似为典型二阶系统，由教材中图 5-46 知 \(\zeta = 0.36\)。再由教材中图 3-12 知 \(\sigma \% = 30\%\)。系统全部设计指标满足。

(2) 设计数字控制器 \(D(z)\)。已知 \(T=0.1, a=0.7, b=0.1\)，令 

\[D(z) = C \frac{z - A}{z - B}\]

其中 

\[A = e^{-aT} = 0.932, \quad B = e^{-bT} = 0.990\]

进行 \(G_c(s) - D(z)\) 变换，令

\[C \frac{1 - A}{1 - B} = K \frac{a}{b}\]

有 

\[C = K \frac{a(1 - B)}{b(1 - A)} = 154.4\]

得数字控制器

\[D(z) = 154.4 \frac{z - 0.932}{z - 0.990}\]

(3) 绘制系统单位阶跃响应曲线。
连续系统时：

\[G_c(s)G_0(s) = \frac{K(s+a)}{s(s+b)(s+10)} = \frac{150(s+0.7)}{s(s+0.1)(s+10)}\]

\[\Phi(s) = \frac{G_c(s)G_0(s)}{1+G_c(s)G_0(s)} = \frac{150(s+0.7)}{s^3 + 10.1s^2 + 151s + 105}\]

\[R(s) = \frac{1}{s}\]

系统输出 

\[C(s) = \Phi(s)R(s) = \frac{150(s+0.7)}{s(s+0.1)(s+10)} = \frac{150(s+0.7)}{s(s+0.1)(s+10)}\]

离散系统时 ( \(T=0.1s\) )： 

\[G_h(s)G_0(s) = \frac{1 - e^{-sT}}{s} \cdot \frac{1}{s(s+10)}\]

\[G_hG_0(z) = (1 - z^{-1})\mathcal{Z}\left[\frac{1}{s^2(s+10)}\right] = (1 - z^{-1})\mathcal{Z}\left[\frac{0.1}{s^2} + \frac{0.01}{s} + \frac{0.01}{s + 10}\right] \]
\[= \frac{0.01(0.368z + 0.264)}{z^{2} - 1.368z + 0.368}\]

\[G_hG_0(z)D(z) = \frac{0.568(z + 0.717)(z - 0.932)}{(z^2 - 1.368z + 0.368)(z - 0.99)}\]

### Page 142

代表的采样时间单位。(7.1)

\[  \Phi(z) = \frac{G_hG_0(z)D(z)}{1 + G_hG_0(z)D(z)} = \frac{0.568(z + 0.717)(z - 0.932)}{z^3 - 1.79z^2 + 1.6z - 0.743}  \]

\[ R(z) = \frac{z}{z - 1}  \]

系统输出
\[ C(z) = \Phi(z)R(z) = \frac{0.568(z^3 - 0.215z^2 - 0.668z)}{z^4 - 2.79z^3 + 3.39z^2 - 2.343z + 0.743}  \]
\[ = 0.568(z^4 + 2.545z^3 + 3.05z^2 + 2.225z^4 + 1.02z^5 + \cdots)  \]

应用MATLAB软件包，可得连续系统和\(T = 0.1s\)时离散系统的单位阶跃响应如图7-24-1所示。由图可见：系统连续时，\(\sigma\% = 31\%\), \(t_p = 0.28s\), \(t_s = 1s\), (\(\Delta = 2\%\))；系统离散时，\(\sigma\% = 78\%\), \(t_p = 0.3s\), \(t_s = 3.1s\) (\(\Delta = 2\%\))。表明连续系统离散化后，若采样周期较大，则阶跃响应动态性能会恶化，且输出有纹波。

MATLAB程序：exe724a.m
\[ T = 0.1; \]
\[ sys1 = tf([150, 105], [1, 10, 1, 151, 105]); \]
\[ sys2 = tf([0.568, -0.1221, -0.3795], [1, -1, 79.1, 6, -0.743], T); \]
\[ step(sys1, sys2, 4); \]

\(\text{grid;}\)

系统单位阶跃响应曲线

图7-24-1系统单位阶跃响应曲线

\(T=0.1s\)

\(T=0.01s\)

系统单位阶跃响应曲线

图7-24-2系统单位阶跃响应曲线

\(T=0.1s\)

\(T=0.01s\)

系统单位阶跃响应曲线

(4)改变采样周期后系统的单位阶跃响应。另选\(T=0.01s\)，则

\[ G_{\epsilon}(s) = K \frac{s + a}{s + b} = 150 \frac{s + 0.7}{s + 0.1} \]

利用\(G_{\epsilon}(s) - D(z)\)变换，有

\[ C \frac{1 - A}{1 - B} = K \frac{a}{b}  \]

式中
\[ A = e^{-aT} = e^{-0.007} = 0.993, \]
\[ B = e^{-bT} = e^{-0.001} = 0.999 \]
\[ C = K \frac{a(1 - B)}{b(1 - A)} = 150 \]

图7-24-2系统单位阶跃响应曲线

\(T=0.01s\)

\(T=0.01s\)

- 248 -

### Page 143

"></p>
二、系统网络的划分

此处根据具体的网络系统进行划分，例如将各工作站及其连接方式列入表格中，而将路由器等关键设备则列入网络拓扑图中。

三、路由器在网络中的作用

路由器在网络中的作用主要是转发数据包。具体来说，路由器接受数据包，根据IP地址查找路由表，然后选择下一个接口转发数据包。如果包的目的地址是局域网上的另一台主机，路由器会查找默认路由，将数据包直接发送到目的主机。

四、路由器常见的几种类型

* 帧中继路由器 (Frame-Relay Router)
* 网络地址 translating Routers (NWR)
* 以太网交换机路由器 (Ethernet Switch Router, EswRouter)
*  IP路由器 (IP Router, IPRouter)

总的来说，路由器是多级网络连接、完成数据包路由选择的网络设备，根据优先级等级减少路由表项的数量。

五、结论

本文主要讲解了什么是路由器及其在网络中的作用，以及各种不同类型的路由器。通过实例，读者可以更好地理解路由器在网络中的作用，并将其应用到实际项目中去。

以上为参考答案，仅供参考。请根据实际情况需要修改。

### Page 144

parentdoc Liamsconcatd orc(phddlbteltaetnt)r1)id.MATLAB程序:exe724c.mT=0.1;t=0:0.1;t1 u=t;%定义系统输入sys=tf([0.568,-0.1221,-0.3795],[1,-1.79,1.6,-0.743],T)lsim(sys,u,t,0);%绘制系统时间响应曲线grid;图7-24-3系统单位斜坡响应曲线(MATLAB)7-25设闭环离散系统如图7-73所示,若采样周期在0≤T≤1,2s范围内变化,试在T每增加0.2s之后,绘出系统的单位阶跃输入响应,要求列表表记录相应的σ%和t(Δ=2%)。解当T=0时,系统为连续系统,零阶保持器不存在,其闭环传递函数Φ(s) 解得时,系统阶跃响应公式如下

\[ d\Omega dt = 0.4 \]

第二次模报信息1如图7-73模块复用精帆10:

\[\begin{align*}
\Phi(s) &= \frac{\Omega^2 s + \Omega s - \Omega \Omega^2 s^2}{1 - \frac{1}{s} + 2e^{-s}s + e^{-s} - \frac{\Omega^2}{s^2} + \frac{\Omega^2}{s} + \frac{\Omega}{2} \\
\end{align*}\]

图7-23:离散时间单位阶跃响应

分解:

\[\begin{align*}
G(z) &= (1-z^{-1})Z\left[\frac{1}{s^2 + 1 - \frac{1}{s^2}s^2}\right] \\
&= (1-z^{-1})Z[\frac{1}{s^2} - \frac{1}{s^2} \cdot \frac{1}{s^2} + \frac{1}{s^2} \cdot \frac{1}{s^2}] \\
&= (1-z^{-1})Z[\frac{\Omega^*}{\Omega*}] \\
&= 2e^{-t} - e^{-z}^2](1-z^{-1})(1-z^{-1}+z^{-1}| + 2e^{-Z}2^{-s}((1-z)^{-1})^{-1}(1-z^{-1}Z+z^{-1}|)
\end{align*}\]

### Page 145

coordinate system drawing: <center>图 7-25-1 </center>

### Page 146

equation 4) equation 4)text 4)number 9) label 2)text 8)text 7)text 6)text 5)text 4)text 3)text 2)text 1)text 1)text 2)text 4)number 1)text 1)text 4)number 1)text 4)number text 1)text 4)number 1)text 1)text 1)text 1)text 1)text 1)text 1)text 4)text 4)text 4)text 4)text 4)text 1)text 1)text 1)text 1)text 1)text 2)text 2)number 7)text 5)text 2)number 2)number 2)text 2)text 2)text 3)text 3)text 3)text 3)text 3)text 2)text 3)text 3)text 3)text 2)text 2)text 2)text 2)

%绘制 \(T=0.2\)单位阶跃响应曲线

step(sysd1,t1); grid; %T=0.4; \(T2=0.4;\) %绘制 \(T=0.4\)单位阶跃响应曲线 step(sysd2,t2); grid;

step(sysd3,t3); %绘制 \(T=0.6\)单位阶跃响应曲线 grid;

T3=0.6; t3=0.6;12; T4=0.8; t4=0.8;12; sysd4= tf([0.249,0.192],[1,-1.2,0.641],T4); plot(T4,~,) grid; %绘制 T=0.8单位阶跃响应曲线 step(sysd3,T4); grid;

T5=1; t5=0;1;12;sysd5=tf([0.368,0.264],[1,-1.0,632],T5); step(sysd5,t5) ;%绘制 \(T1=0.8\)单位阶跃响应曲线 grid;

T6=1.2;

T6=1.2; t6=0.1;1.2; sysd6=tf([0.501,0.338],[1,-0.8,0.639],T6); subplot(4,2,7); step(sysd6,t6); %绘制 \(T2=0.1\)单位阶跃响应曲线 grid;

7-26 设具有采样器、保持器的闭环离散 系统如图 7-74所示,当采样周期 \(T=0.1s,\)输入信号为单位阶跃信号时,试计算系统输出 \(C(z),\) 图 7-74 闭环离散系统结构图

解 因为

} = tft,[1,-0.1144],T) 
step(sys,t); 
grid; 

图 7-26-2 离散系统的单位阶跃响应曲线（T=0.1,MATLAB）

• 254 •

### Page 149

transition model mean video, edxit all, parcs and option table in Excel, the automatic generation timeline makes mathematical descriptions.

### Page 150

.假设开始时系统处于静止状态，即

\[ c(0) = 0, \quad c'(0) = 0 \]

则描述系统的方程组为 \(\ddot{c} = u\)，其中

\[u = 
\begin{cases} 
1, & e>1 \\ 
-1 < e < 1, \quad \dot{e} < 0 \\ 
-1, & e <-1 
\end{cases} \]
\[\dot{c} = e - r - c\]

因为 \(r(t)=e-t\)，故有 \(e=t-r-\dot{c}, \quad e'=-1; \quad \ddot{c}=-t'\)，初始条件为 \(e(0)=0, \quad \dot{c}(0)=1\)。

整理上述关系式后可得

\[\ddot{c} = 
\begin{cases} 
-1, & e>1 \\ 
-1 < e < 1, \quad \dot{c} < 0 \\ 
1, & e<-1 
\end{cases}
 \quad e=-r-c\]

在相平面的 \(I\) 区 (\(e>1; \quad -1 \le e<1, \quad e<0\))，描述系统的微分方程为

\[\ddot{c}=-1\]

积分可得

\[\frac{1}{2}\bigl(e^{2}\bigr)=-1+e+c_{1} \quad (\text{抛物线})\]

在相平面的 \(II\) 区 (\(e<-1; \quad -1 \le e<1, \quad e>0\))，描述系统的微分方程为

\[\ddot{c}=1\]

积分可得

\[\frac{1}{2}e^{2}=-1+e+c_{2} \quad (\text{抛物线})\]

由初始条件 \(e(0)=0, \quad \dot{ e}(0)=1\) 出发，概略绘制其相轨迹如图 8-8-1 所示。

下面利用 MATLAB 程序 exe808.m 精确绘制系统相轨迹，如图 8-8-2 所示。由图可见，系统振荡发散。

图 8-8-1 题 8-8 系统的概略相轨迹

图 8-8-2 题 8-8 系统的相轨迹 (MATLAB)

(图部分)

### Page 151

;"></script>
Inophen: s.ybs808.n, m:t=0:0.01:30;%设置仿真时间为30s

e0=[01];%设定初始条件为e(0)=0,'e(0)=1

[t,e1]=ode45('sys808',t,e0);%求解微分方程

plot(e1(:,1),e1(:,2));grid%绘制系统相轨迹

调用函数：sys808.m

function de=sys808(t,e)

del=e(2);

8-9设非线性系统如图8-81所示，其中M=1，T=1。若输出为零初始条件，输入

r（t）=1（t)，要求：

（1）在e²平面上画出相轨迹；

（2）判断该系统是否稳定，最大稳态误

+Me2

差是多少；

（3）绘出e（t）及c（t）的时间响应大致

波形。

图8-81题8-9的非线性系统结构图

解本题首先应根据系统结构图解出相

应的微分方程和开关线，然后根据给定输入信号和初始条件，用等倾线法或MATLAB法绘

制相轨迹，并由相轨迹分析系统性能，得到最大稳态误差，绘制e（t）及c（t）的时间响应波形。

（1）相轨迹。假设系统输出为零初始条件，即

c（0)=0,'c（0）=0

则描述系统的方程组为T'十²=u，其中

M,

5e>0.5

u={0,

5e≤0.5

-M,

5e<-0.5

由比较点可得

因为r（t）=1（t），故有e=1-c'e=-c，=一，=一，初始条件为e(0)=1.e(0)=0。

整理上述关系式后可得

-M,

e>0.1

0,

11≤0.1

'M,

e<-0.1

开关线为e=±0.1。

在I区（e>0.1）：

271

### Page 152

}. This parameter corresponds to the Influx code for that clock

% Assume the range of [0,1] for precise results
```

### 文本内容

#### 顶行
```
T^(e) \frac{de}{de} + \dot{e} = -M

T^(e) \frac{de}{de} + \dot{e} = 0

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

令 \frac{d\dot{e}}{de} = \alpha, 可得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

frac{d\dot{e}}{de} = \alpha, 得等倾线方程为

\frac{d\dot{e}}{de} = \alpha, 得等倾线方程为
```

#### 第二段
```
在II区(|e| <= 0.1):

    在II区(|e| <= 0.1):    T^(e) \frac{de}{de} + \dot{e} = M

    T^(e) \frac{de}{de} + \dot{e} = 0

    在II区(|e| <= 0.1):    T^(e) \frac{de}{de} + \dot{e} = M

    T^(e) \frac{de}{de} + \dot{e} = 0
```

#### 顶行
```
还要绘制"t"的曲率, 令{dy}/dt = L(t), 则为:t'(t) = L'(t), 得到t'(t) = c(t)

line segment line segment
circular arc circle 封闭曲线 圆形线 闭合曲线 封闭曲线 圆形线 闭合曲线
```

#### 第二段
```
l'(t) = (\frac{dy}{dt}) = (\frac{d(e)/dt}) = L' (t) = c (t)

line segment line segment
circular arc circle 封闭曲线 圆形线 闭合曲线 封闭曲线 圆形线 闭合曲线
```

#### 第三段
```
l'(t) = (\frac{dy}{dt}) = (\frac{d(e)/dt}) = L' (t) = c (t)

line segment line segment
circular arc circle 封闭曲线 圆形线 闭合曲线 封闭曲线 圆形线 闭合曲线
```

### 离散化

```
 plotting from 0 to 1

circular arc circle 封闭曲线 圆形线 闭合曲线 封闭曲线 圆形线 闭合曲线
```

### 风格

这是数学与计算机视觉领域的内容，使用了数学符号和格式来表示公式和图表，内容涉及多项式、线性代数、曲线拟合等内容。整体风格较为学术和严谨。

### Page 153

display-table-responsive table 发布于 2023- septiembre 28, 2023 上午 05:45:53
（2）稳定性。由相轨迹可见，系统存在稳定自振，最大稳态误差 \(\left| e_s(\infty) \right|=0.1\)。

（3）时间响应。运行 MATLAB 程序 exe809. m 可得 \(e(t)\) 及 \(c(t)\) 时间响应波形如图 8-9-2 所示。

\begin{center}

\end{center}

\begin{center}

\end{center}

图 8-9-1 题 8-9 系统相轨迹 (MATLAB) 图 8-9-2 题 8-9 系统 \(e(t)\) 及 \(c(t)\) 的时间响应 (MATLAB)

8-10 已知具有理想继电器的非线性系统如图 8-82 所示，试用相平面法分析：

（1）\(T_d\)=0 时系统的运动；

（2）\(T_d\)=0.5 时系统的运动，并说明比例微分控制对改善系统性能的作用；

（3）\(T_d\)=2, 并考虑实际继电器有延迟时系统的运动。

解 本题首先应根据系统结构图解出相应的微分方程和开关线, 得到解析表达式, 然后根据给定输入信号, 初始条件和不同参数, 绘制各个系统的相轨迹, 并由相轨迹分析比例微分控制系统性能的影响。

描述系统的微分方程为

\[\overset{\sim}{c} = u\]

其中

\[u = 
\begin{cases} 
1, & e + T_d \dot{e} > 0 \\
-1, & e + T_d \dot{e} < 0 
\end{cases}\]

由输入比较点可得

\[e = r - c = 1 - c, \quad \dot{e} = -\dot{c}, \quad \ddot{e} = -\ddot{c}\]

初始条件 \(e(0)=1, \dot{e}(0)=0\)。

\begin{center}

\end{center}

\text{图 8-82 题 8-10 具有理想继电器的非线性系统结构图}

### Page 154

bar{t}_{d

图 8-10-1 \( T_{d}=0 \) 时系统相轨迹 (MATLAB)

整理上述关系式后可得 \[ \dot{\epsilon} = -u = \begin{cases} -1, & e + T_{d}\epsilon > 0 \\ 1, & e + T_{d}\epsilon < 0 \end{cases} \] 开关线为 \( e+T_{d}\epsilon=0 \)。 在 I 区 (\( e+T_{d}\epsilon>0 \))： \[ \dot{\epsilon}' = -1, \quad \dot{\epsilon} d \dot{\epsilon} = -de \] 积分可得 \[ \frac{1}{2} \dot{\epsilon}^2 = -e + C_1 \quad (\text{抛物线}) \] 其中 \( C_1 \) 为常数，由初始条件和开关线确定。

同理可得，在 II 区 (\( e+T_{d}\epsilon<0 \))： \[ \frac{1}{2} \epsilon^2 = e + C_2 \quad (\text{抛物线}) \] 其中 \( C_2 \) 为常数，由初始条件和开关线确定。

(1) \( T_{d}=0 \) 时，系统的运动。 \( T_{d}=0 \) 时，系统相轨迹如图 8-10-1 所示。 系统在 \( r(t)=1 (t) \) 作用下，输出呈现等幅振荡状态。在 MATLAB 的 Simulink 环境下搭建具有继电器的非线性系统，如图 8-10-2 所示。设定负时间为 10s，算法选用 ode45，微分环节系数设为 0。运行到此时单位阶跃响应如图 8-10-3 所示。

图 8-10-2 具有继电器的非线性系统 (Simulink 环境)

图 8-10-3 \( T_{d}=0 \) 时系统的时间响应 (MATLAB)

图 8-10-4 \( T_{d}=0.5 \) 时系统相轨迹 (MATLAB)

V.572

275*

### Page 155

学前教育 郝志. 电路分析 - 绪论 绪 论 1 序 总 概 论 序 总 概 论 绪 论 1 绪 论 绪 论 绪 论 绪 论 1 绪 论 绪 论 绪 论 绪 论 1 绪 绪 论 绪 论 绪 论 绪 论 1 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 陈 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论 绪 论述 绪 论 绪 论 绪 论 绪 论 绪 论 第一章 术前已对机器进行分析，试验，确定了对象的流体参数，为准确 的发生在发生的发生应变和压力时，运动过程中材料的承受振动对机器的能量产生承，保护电|\{9. \}. \}(\text{有关) \}  \(\{和\text{几=10. }上=10上的计算} = 10.} \]\) , } \) \) .如 {图``` (0} 在5测试结束当；)； \( (\text{视(t)=10.} \(时，输出响应应稳等效 (T0s）}输 共） {为不{计启动器}输出}的=故障 的}5{有} ；}；{于n}并等对现代基本}进} .}树 Prot 运维工程装置  }（t} e ability }2 T：送到9; 9}一启动器2}}_{{用图各} 的时一 副网络的数模型。传放通过输入（输出） 例功起}、全/2 章} 如输入输出} 分表中心 {方案设计 管管道接到机} 了新 T 的）{ITT函数=的有关输由传感器}为   系统已 接} t0 T}（）荷1 ()填软程 储器水冷章= 部软输入模元感{风扇 T}进传感器新{}}。中 功行电面后会于}输 效 数 图8-10-7 T开发。 应]$ {为例属}}] 第工程}，拓 {比输出8-10-}硬，他三类}}8-10-{(从}进。作} F机械 T软成}导数书;。 软件}学习}3) 其中输入移和很都有管其{输 ]相结10 硬件然水套经所} }的干""的{公式T机械}换输出数软。机器参数 T等M 用原理，设由设计计算}设文软} 所） 内机器}传入。输入\到}  threshold Mos} 相4 T 序{输}与软机仅} 软学响操作 子和信，尔 且传对各}这 等} 稳 }可以在频篇产 {场 硬}数软件 Define 系统}产 hshe数 qGate 烈]预料 所》《}_{基 源结论 T}电子机源码信号图则，以下代}（软编程换可关机 和输。现} 信号 子参数使]。}} 图 软 }算。 P C（输入软件/}）}就则在} kw仍原软W} H \\ \\ oy}输入硬设 程和电各反式据}门设}源实对外。两个 Bod Sw}让对于。然} Nu素信和输。 出 软并信} 硬 == 等待软应输出激活\输入法 电机 图} T 电}} 时一具多个数学只。=信双机又管理} 计手 电子} } 数么主图 9 相每}在原理感而} 照通过多等}}设 权下步 建处原等 }步{一额程步为 =\}行练技5工S 软以求按} 然若 述浮就得。传递返 =软内。信}例过等需 输入 输入/ 电。。有限 单数均讯像}如}{接 评电}电软并 若 T 有 的 } 容}，动例传]图上 输 应 过容 。}信输多 T {输接1电二设 制 而 心 T 传。传 传 W D侧信边所里意一输出 本提设 网 工此 ，RA 流回 手机 硬 等 门 硬 超 等 = 信 备 设 D 电输 输 与算贴 候设} 算设 E)}空 条传 T 信工 而 设问信 对信息 到 一 硬} R 工带 电 运 主是从信同 设 返&Mut Electrical。 软办超方 程计}软开 \ 理换、}理 设 硬 芯 元送 输 开道低输 程决于，制。设 分产理 计+ 过临设 了 其 中 { 数}点 I} T} 接 T 设 后 工 T 课信 运交 数 W} 工 而 输设 理 作运 动 开} 维进输 按 而工 使 到}} 硬 硬师 T 设 出 输而所 计载和信 信 功 K 算 理 输 为运M他 输}}
//blogOfficial DN)\\]ctee，}{确_ 脚 e}\}

```

### Page 156

][“ <”, where“ 1” “ 0 ”， “ >”. namely when and onlywhen e(t) has a boundt, based onthe assumptionthat t issmallenough. This assumption is often daoed in experimentation, so that results

### Page 157

represents not live registered user.T e \frac{d \dot{e}}{d \dot{e}} + \dot{e} = - K e 

令 \frac{db}{de} = \alpha, 得等倾线方程为 

b = \frac{-8}{0.5 \alpha + 1 } e

下表给出了不同 \alpha 值下等倾线的斜率： 

\begin{array}{c|c|c|c|c|c|c|c}
\alpha & 0 & 2 & 6 & \infty & -10 & -6 & -4 & -2 \\
\hline
8 & -8 & -4 & -2 & 0 & 2 & 4 & 8 & \infty \\
\end{array}

根据表格作出等倾线或运行 MATLAB 程序 exe811. m 可作出初始条件为 e(0) = 2， e'(0) = 0 时系统的相轨迹，如图 8-11-1 所示。
(2) 开关闭合。 \varepsilon = b -C-K_1 c = C - K_1 c' = e + K_2 e'， 描述系统的微分方程为 
T c' + c = u， 其中 

\begin{aligned}
u = 
\begin{cases}
Ka, & \varepsilon > a \\
Ke, & |\varepsilon| < a \\
-Ka, & \varepsilon < -a
\end{cases}
\end{aligned}

由输入比较点可得 

\begin{aligned}
e = r - c = c - \varepsilon, & \quad \dot{e} = \dot{c} - \dot{\varepsilon}, \quad \dot{e} = -\dot{\varepsilon} 
\end{aligned} 

整理上述关系式可得 

T \varepsilon + \dot{e} = -u = 
\begin{cases}
-Ka, & e + K_1 e' > a \\
-K (e + K_1 e), & |e + K_1 e| < a \\
Ka, & e + K_1 e' < -a 
\end{cases}

开关线为 e + 0.5 \dot{e} = \pm 0.5.
I、III 区的讨论同(1), 其等倾线方程分别为 

在 I 区(e + K_1 e > a)

\begin{aligned}
e = 
\begin{cases}
-Ka, & e + K_1 e > a \\
-K (e + K_1 e), & |e + K_1 e| < a \\
Ka, & e + K_1 e' < -a 
\end{cases}
\end{aligned}

在 III 区(e + K_1 e' < a)

\begin{aligned}
T e \frac{db}{e} + \dot{e} =-(1 + K K_1) \dot{e} = - K e 
\end{aligned} 

令 \frac{de}{e} = \alpha, 得等倾线方程为 

\begin{aligned}
\dot{e} = 
\begin{cases}
-K e, & e = - \frac{Ka}{1 + T \alpha + K K_1} \\
\frac{K e}{1 + T \alpha + K K_1} = - \frac{16}{\alpha + 10}
\end{cases}
\end{aligned}

下表给出了不同 \alpha 值下等倾线的斜率。

\begin{array}{c|c|c|c|c|c|c}
\alpha & 10 & -6 & -2 & 6 & \infty & -26 & -18 & -14 \\
\hline
\frac{16}{\alpha + 10} & -\infty & -4 & -2 & -1 & 0 & 1 & 2 & 4 \\
\end{array}

根据表格作出等倾线或运行 MATLAB 程序 exe811. m， 作出初始条件为 e(0) = 2， e'(0) = 0 时系统的相轨迹，如图 8-11-2 所示。

### Page 158

txiaojhibo.wps //159.45.18.182/_matlab_*(%已编辑,2021/1/25 1:55:26修改)
\[ \text{t=0:0.01:10;} \] % 设定仿真时间为 10s e0=[2 0]; \text% 初始条件e(0)=2,e'(0)=0 [t,e1]=ode45('sys811a',t,e0);求解开关断开时系统的微分方程 [t,e2]=ode45('sys811b',t,e0);求解开关闭合时系统的微分方程 figure(1) plot(e1(:,1),e1(:,2));grid %绘制开关断开时的系统相轨迹 figure(2) plot(e2(:,1),e2(:,2));grid %绘制开关闭合时的系统相轨迹 figure(3) plot(t,e1(:,1));grid %绘制开关断开时的系统误差曲线 hold on \text% 图形保持 plot(t,e2(:,1));grid %绘制开关闭合时的系统误差曲线 开关断开时的调用函数: sys811a.m function de=sys811a(t,e) \text% 描述开关断开时系统的微分方程 a=0.5;K=8;T=0.5;Kt=0.5; del=e(2); if(e(1)<=-a) de2=(K*a-e(2))/T; elseif(abs(e(1))<2) de2=(-K*e(1)-e(2))/T; elseif de2=(-K*a-e(2))/T; end de=[del de2]'; 开关闭合时的调用函数: sys811b.m function de=sys811b(t,e) % 描述开关闭合时系统的微分方程 global a KT Kt \} 278

### Page 159

approaching;text-align: justify;">
  <!– End region of text, which is left-aligned*}
and when neither the message nor its corresponding address table entry is referred to, the routine returns without error. This is roughly based on the context provided by the call to


struct message takes in a pointer and a size to fetch the message.Loader background here...More importantly, this highlights the general pattern and subtlety involved in proper processing of variable-length messages in C as discussed in Chapter 8 of Townes and Luzynsk's booklet.

The message format is as follows: (Illustration in the first code snippet)

％――――――――――――――――――――――　Message Header Matters
	
 �--<Message Header Matters>
 >begin of message header matters

 After message header matters:  
  
 �--<End of Message Header Matters><Header اته> `  <End of Message Header Matters>

<%-- 欠待遍历	
＿Message Decomposition: Separate a}eld into its components:	
＞Message Message头；ulner protect symbol
\[ \textblock {｝ \  } c =
 (
  sizeof message header matters
 )_{ \              如果 {} 大小为 4
 }\)
 >{, 1 ]_ {1, 3 }
Structure

### for‘size of messages
if size == 1</I>

figure Figure 8-12:Tracking mark for all 4 structure’s/ of (training picture) Figure 8-12. Tracking mark for all structure 4
> </Figure>

时分时间转移8.12.4Clabel3>
Figure 8-12: Tracking mark for all structure/ of (training picture) Figure 8-12. Tracking mark for all structure/>








matzlab作为另一种方法写下的书页，就共享共享满意近为意思于一个这本书.Ken Ψ右边没有考虑N个的.It may be implied that a given characteristic value is unique for either Systems A or System B, not for both Systems.............................................................................................................................................................(II)

Robot program

MATLAB程序:exe812.m

G1= tf([1],[0.1 1 0]);
G2 = zpk([],[0 -1],2);
G3 = tf([3 2],[0.1 1.1 1 0]);
bode(G1,G2,G3);% 绘制三个系统线性部分的开环对数幅频特性曲线
8-13 试推导下列非线性特性的描述函数:

(1) 变增益特性(见教材中表8-1第9项);
(2)具有死区的继电特性(见教材中表8-1第2项);
(3)\( y = x^3 \).解

本题非线性特性的描述函数可由等效法则或描述函数的定义来求取。

(1) 变增益特性。通过作图法获得\( y(t) \), 如图8-13-1所示,其中 \(\varphi_1 = \arcsin \frac{s}{A}\).

### Page 160

is user-defined.**图 8-18-2 题 8-18 系统稳定性分析**

**图 8-18-3 题 8-18 系统的自振信号输出( MATLAB)**

figure(1) plot(x,y);hold on %绘制 \(-1/N(A)\) 曲线 Nyquist(G); % 绘制线性环节的奈氏曲线 axis([-2,0,-0.5,0.5]) % 重新设置坐标范围 figure(2) t=0:0.01:10; %设定仿真时间为10s c0=[0 0]; %初始条件为零 [t,c1]=ode45('sys%81',t,c0); %求解微分方程 plot(t,c1(:,1));%绘制系统自振输出信号调用函数:sys8i18.m fucntion dc=sys8i18(t,c) %描述系统微分方程 dc1=c(2); if ((c(1)>0.04)|((c(1)<0.04)&(c(1)>-0.04))&(c(2)<0)) dc2=-c(2)-2; elseif dc2=c(2)+2; end dc=[dc1 dc2]';

MATLAB程序:exe812.m

G1= tf([1],[0.1 1 0]);
G2 = zpk([],[0 -1],2);
G3 = tf([3 2],[0.1 1.1 1 0]);
bode(G1,G2,G3);% 绘制三个系统线性部分的开环对数幅频特性曲线
8-13 试推导下列非线性特性的描述函数:

(1) 变增益特性(见教材中表8-1第9项);
(2)具有死区的继电特性(见教材中表8-1第2项);
(3)\( y = x^3 \).解

本题非线性特性的描述函数可由等效法则或描述函数的定义来求取。

(1) 变增益特性。通过作图法获得\( y(t) \), 如图8-13-1所示,其中 \(\varphi_1 = \arcsin \frac{s}{A}\).

### Page 160

is user-defined.**图 8-18-2 题 8-18 系统稳定性分析**

**图 8-18-3 题 8-18 系统的自振信号输出( MATLAB)**

figure(1) plot(x,y);hold on %绘制 \(-1/N(A)\) 曲线 Nyquist(G); % 绘制线性环节的奈氏曲线 axis([-2,0,-0.5,0.5]) % 重新设置坐标范围 figure(2) t=0:0.01:10; %设定仿真时间为10s c0=[0 0]; %初始条件为零 [t,c1]=ode45('sys%81',t,c0); %求解微分方程 plot(t,c1(:,1));%绘制系统自振输出信号调用函数:sys8i18.m fucntion dc=sys8i18(t,c) %描述系统微分方程 dc1=c(2); if ((c(1)>0.04)|((c(1)<0.04)&(c(1)>-0.04))&(c(2)<0)) dc2=-c(2)-2; elseif dc2=c(2)+2; end dc=[dc1 dc2]';

**图 8-18-3 题 8-18 系统的自振信号输出( MATLAB)**

图 8-18-3 题 8-18 系统的自振信号输出( MATLAB) * 8-19 试用描述函数法说明图 8-88 所示系统必然存在自振，并确定 \( c \) 的自振振幅和频率，画出 \( c, x, y \) 的稳态波形。 * 解：本题首先应根据结构图进行等效变换，求出线性部分的传递函数，然后绘制非线性部分的负维描述函数和线性部分的幅相特性曲线，求出自振点，由频域稳定判据判断其稳定性，并确定输出 \( c \) 的自振振幅和频率，画出 \( c, x, y \) 的稳态波形。 （1）* 理想继电环节的描述函数 

\[ N(A) = \frac{4}{\pi A} \]

其负维描述函数数为

\[ \frac{ 1 }{N(A)}= -\frac{\pi A}{4} \]

为单调减函数，作 \(-\frac {1}{ N(A) }\) 曲线如图 8-19-1 所示。

* 288 *

### Page 161

Mapper x sym:x^2+y^2=r^2 </Spline>
图8-89 题8-19的非线性系统结构图
图8-19-1 系统稳定性分析

(2) 线性部分的幅相曲线

\[G(j\omega) = \frac{10}{j\omega(2+j\omega)^2}\]

线性部分的 \(\Gamma_G \) 曲线如图8-19-1中曲线所示。由图可知，\(G(j\omega) \) 与 \(-1/N(A) \) 存在交点 \(A_0 \)，\(A_0\) 点处频率为 \(G(j\omega)\) 的穿越频率 \(\omega_x \) 。因

\[G(j\omega) = -\frac{40}{ \omega^4 + 8\omega^2 + 16 }-j\frac{10(4-\omega^2)}{(2\omega^2+16)^2}\]

令 \(\text{Im}G(j\omega) = 0\)，得 \(\omega_x = 2 \) 。 \(\Gamma_G\) 曲线与负实轴的交点为

\[G(j\omega) = -\frac{40}{\omega_x^4 + 8\omega_x^2 + 16}|_{\omega_x = 2} = -\frac{5}{8} =  －0.625\]

(3) 自振稳定性。由描述函数分析法，有

\[G(j\omega) = -\frac{1}{N(A)}\]

图8-19-1 表示系统必然存在稳定的自振。令

\[G(j\omega) = -\frac{1}{N(A)}=-\frac{\pi A}{4} = -\frac{5}{8}\]

解得自振振幅

\[A_0 = \frac{5}{2\pi}=0.796\]

由此产生的自振信号为 \(x(t) = 0.796\sin2x \)。

利用 MATLAB 程序 exe819. m，绘制该非线性系统稳态输出波形，如图8-19-2所示,其中 \(c,x\) 和 \(y\) 的波形曲线分别以点线、实线和虚线表示。

MATLAB 程序:exe819. m

A=0.01;0.01;100;
NA1=-4./(pi*A);
x=real(NA1);y=imag(NA1);
figure(1)
plot(x,y);hold on %绘制一幅(1/N(A) A-曲线
G=zpk([],[0 -2 -2],10);
nyquist(G) %绘制线性部分的奈氏曲线
axis([-1,0,-0.5,0.5]); %重新设定坐标范围

### Page 162

.图 8-19

t=0:0.01:14; c0=[-0.1 0 0]'; [t,c]=ode45('sys819',t,c0);   % 求解微分方程 % 非线性环节输出 y=sign(c(:,1));   % 绘制系统响应曲线 subplot(3,1,1) plot(t,-2*c(:,1),'-');grid axis([0,14,-0.85,0.85]); subplot(3,1,2) plot(t,c(:,1),'-.') ;grid axis([0,14,-0.45,0.45]); subplot(3,1,3) plot(t,y,'-') ;grid axis([0,14,-1.2,1.2]);   % 重新设定坐标范围

调用程序：sys819 function dc = sys819(t,c) dc1 = c(2); dc2 = c(3); if (( -2*c(1))<0) y = -1; elseif y=1; end dc3 = -4*c(2) -4*c(3) +5*y; dc = [dc1 dc2 dc3]';

图 8-19-2 非线性系统 \(c,x,y\) 的稳态波形 (MATLAB)

8-20 已知非线性系统的输入和输出关系式 \[ \ddot{y} + af(\dot{y}, \dot{y}, y) = \ddot{u} + bg(\dot{u}, u) \] 试求伪线性系统的结构及实现形式。 解 由原系统方程可得

### Page 163

can,choices:  \  【 【 【 【 【 【 【 【 【 【 【 【 【 【 【 【 【 【 【 【
9 1 2 3 4 5 6 7 8 9 10 11 12 16

!记: ! ! ! 11
! ! !  11
www.
4931
2 网站 1] 2 网站 1
5+59:
78:1:58:1: 3 网站1;53) 1
333
! ! ClO

将逆系统方程代入原系统方程可得斯蒂克斯(Stein)
i>4) : '``''''''''''''''''''''/ ( R O <
! #?
_ ''
、 输输 autom/{t u  阶风险评估
即当
3 ]] \ y t//
% Agga%f%)\}>& (iN4)...
ApaxMy)<;(true( '== \ug=ub)U
M
它见反们
< If 个7
(c}}
)\'{well
两X[
# 
0
! ! # 
t}|
\[\[&1
32 32
\[|1U]f'\
&
1:d
\[Toy
)4#
^_]f'#)__'%
1\\
U
v;<`;yaT7>,s2
\[f.e)=a
TX'1.
!\\tX}
}{8。为7
'两4 ^U2.
!.We b9
! ul
Oa%\\
\#!+,
48,
7
94,.4
\['式
】^\\
m%!%7")
$t
f!
ศาสตร์\

''=计算机科学

距离x,y\[\lpaperL 毒企业安全门户-swlt公司检索正!
[$}\|
{\'
2,{'=
1
,
 -->
$ }}
CF!$\'!(D)_..e- R
:5'=
?,=$写字说`#$%'\1'un
(\,
P3)3 0(
'''
Y2R-| 14
!'$,
"%^\ =["}
小青片 [A】
换].
''!%
''^7. O
ji}M4[!^f8 [%...\$向7
12/)
:'乜'')]而是
!% $]==时直]a
6oy
??j\?
1/,0o
0'_\8X空'
%!Y]et[(.-=[\!.[
-7) woD、.-
郑
$3,
\\'7||}}
[[==-=[! x<!--~o--

 7
=>modx
^
和<
$:=x-[=< 10支果-质
得[在DF
p例如
!Vi$,7、
==Z
Eq
5
52
a`!\\'=>Virtual
=$>.索
$上7|
6$!方
'm<=

91
((y/2~=1                                ---[===-
\5播T之!
7
$`f和
x
:=7
E!\]
分得$%
\I5+/
($5%大[?
/<()！！}\b#L
看着

 
按$];
(:Z?\(所以$@E:[+青Junior
3.4
^这是88

当前 sized
差
56*
(.0？!+%7的!0,
+77(%谢谢7\
青类似
\`;

```

### Page 164

TSD; IDLA; c; PUPI-221" I 商用 Q 图 8-21-1无速度反馈时系统的相轨迹 e r﹣c﹣βc 由于e=r﹣c，e=一c，所以 e'=e+βc 相轨迹方程为 开关线 初始条件 e(0)=-R， 0)=0 有速度反馈时，系统的概略相轨迹如图8-21-3所示。 设a=1，b=2，β=0.5，R=2，运行以下MATLAB文件，得有速度反馈时系统的相轨迹 图图8-21-4有速度反馈时系统的相轨迹(MATLAB) 图8-21-3有速度反馈时系统的概略相轨迹 图8-21-4有速度反馈时系统的相轨迹(MATLAB)

### Page 165

equation

0.16; ssa:sba:sbc

 9省略

l.1M

 f = ex.821

- f e

i.e

    l
    ¥

执行执行固定及显式算法
    va)要从086a

    L5e-0· vt的功率平衡方程手动调校平衡速度，表建立 switch方式下
    ei

6-1- -
    参数数值如下
    未干律脱稳调应调Hz

1Rows
万.2)
    1.61(da-

a-.

    ·
    1：
    1
    215k少4.58、40n
    (4.3)=
    自

    容实验
    模拟调
  系

    1006
    .
[图： 209]

    手动调节
    AutoEx)的0-0.10

l.pause][jAsSz\
    [0..01
    A]
    [0]，3.线到 slower铭
    ；系参 
区间[0.0，.
   Ee suibio)
    DEH欧分c

    blindly

a的Osvejd的)在mc、M=-5；值a

Athend ifCaATkrage的必要
    株参值TXrheao

(2

白A.3   A.1A)定理.
    式
    (用)9(2.18-2

综函的计、调压分
    6
    权果然G-1. (-1)、
    调/1 接线设

    参意均
    A.1
    在2r
    3.52
  系参a22

励储下电系统输
调示、:
RcySomeo.
   
    +g
    990

该2设
    tab 2.\和400    
    4-520keq
    求

    ga

f.1.常用

  un 的50
    Ks

自动调为号)11）(\必须.关给出用
    \[}
    \left | {75} - \frac{-1}{N(A)
    题调以Ping]。

### Page 166

.因交点 \( A_{0} \) 在负实轴上，必有 \({\rm Im}G(j\omega_{0})=0\)，因而 \(\omega_{0}^{3}-2\omega_{0} = 0\)，解得自频频率 \(\omega_{0} = 0\) (舍去) 和 \(\omega_{0} = \sqrt{2}\) 。而
\[{\rm Re}G(j\omega_{0}) = - \frac{1}{N_{A_{0}}} = - \frac{\pi A_{0}}{4} \]
有一
\[\frac{K}{3 \omega_{0}^{2}} \bigg|_{ \omega_{0} = \sqrt{2}} = -\frac{\pi A_{0}}{4} ， 可求出自振幅 
A_{0}  = \frac{2K}{3 \pi} 。 \] 

(2) \(\tau \neq 0\) 时产生自振的系统参数 \( K \) 与 \(\tau \) 值。线性部分频 率特性为
\[G(j \omega) = \frac{K e^{-j \omega}}{j \omega (j \omega + 1)( j \omega + 2)} \]

由题意，系统自振频率 \(\omega = 1\)，自振幅 \( A = 2\)，在 \( G(j\omega\) 与 \(-1/N(A)\) 的交点上，有
\[-\frac{1}{N(A)} = -\frac{2 \pi}{4} = -\frac{\pi}{2}\]

因
\[|G(j1)| = \frac{K}{\sqrt{1+1} \cdot \sqrt{1+4}} = \frac{K}{\sqrt{10}}\]
根据 \(\frac{K}{\sqrt{10}} = \frac{\pi}{2}\)，可求出
\[K = \frac{\sqrt{10} \pi}{2} = 4.97\]
由 \(\angle G(j1) = -90^{\circ} - \arctan 1 - \arctan0.5 - 57.3 \pi = -180^{\circ} \)
可求出 \(\tau = 0.32 \)。 故所求参数值为
\[K = 4.97 ， \tau = 0.32\]

MATLAB 验证:
运行 MATLAB 文件 exe823.m，可得系统在 \( K = 4.97 ， \tau = 0.32 \) 时的 \( G(j \omega) \) 与 \( -1/N(A)\) 曲线，如图 8-22-2 所示。
 
\[K = 4.97 ； \tau = 0.32 \]

MATLAB 程序: exe822.m

K = 4.97； ta0 = 0.32；
G = zpk([],[0 -1 -2],K,'inputdelay', ta0);
A = 0.01,0.01;100;
NA1 = -4./(pi *A);
x=real(NA1);y=imag(NA1);
plot(x,y);hold on
w = 0.0;01;10;
nyquist(G,w)
axis([-2 0.05 - 0.4 0.4])

图 8-22-2 \(\tau \neq 0\) 时系统的稳定性分析 (MATLAB)

在 MATLAB 的 Simulink 环境下搭 建如图 8-22-3 所示的延迟系统模型，并设 定初始条件 \( c(0) = 1\)，仿真可得系统在 \(K = 4.97 , \tau = 0.32\) 时的输出时间响应  \(c(t ) \),如图 8-22-4 所示。
* 294 *
 ```

### Page 167

36. (1) 结构图归类:由各矩形框结构的模块连接而成的树状结构图。(2) 降阶法:通过看图片知道днаdjCu.M4)0,(A4)会讲(2&的功能并建立联系(3) 载相连接。(4)称相图流程图画法:a=(4开始)为t人编码a(1)大边缘读入V,图非线性 partiegxblx)处切数描述过程:省连4/切人之图：与a上图的图 biography上:1123如果M#实行可行的创建明确了b(图每个都很近)，(4)验证点,图(5)报告并进行验证温度模拟图3(图6试验结果示下限,则提出9图3号,线性分配给系数符0位和)。

图

图 8-22-3 Simulink 环境下的延迟系统模型

图 8-22-4 系统输出时间响应 (MATLAB)

### Page 168

display 图

部。 设 \( T_0 \) 与 \(-1/N(A)\) 的曲线如图 8-23-1 所示 由 T _0 与 \(-1/N \) (A) 曲线存在交 点,且当振幅增大时,\( -1/N ( A ) \) 曲线从不稳定区域进入稳定区域,所以系统在满足下列 T、 \( K \) 数值时呈现频率 \( \omega = 10 \ ) 时稳定自振。 因实点在负实轴上，必有 \( \operatorname{Im} G ( j ω ) = 0 \)，即 即\] \( - 90 ° - \arctan { - \arctan ${  $ ( 10 T ) $  = \-\ 18°0 \Rightarrow \arctan { - {\arctan ( \ 10 T } \)}  \] 为了提高干扰线性无法使用直接使用 \[ \operatorname{K }_{2} H使用 ] .

### Page 169

transition sucrose.\[Re[G(j \omega)] = \frac{K_2}{K_1K_2 - \left( \frac{T_1 + T_2}{T_1 T_2} \right)}\]

令 \(\frac{T_1}{T_2} = Re[G(j \omega)]\)，即

\[- \frac{\pi A}{4M} = \frac{K_2}{K_1K_2 - \left( \frac{T_1 + T_2}{T_1 T_2} \right)}\]

由此可知，使系统产生稳定自振时的各参数应满足的条件为 \[K_1 K_2 < \frac{T_1 + T_2}{T_1 T_2}\]，自振参数为

\[\omega = \frac{1}{\sqrt{T_1 T_2}}, \quad A = \frac{4MK_2}{\pi \left( \frac{T_1 + T_2}{T_1 T_2} - K_1 K_2 \right)}\]

MATLAB 验证：设 \(T_1 = 1, T_2 = 2, K_1 = 0.1, K_2 = 10, M = 1\)，正好满足稳定自振条件，且应有如下自振参数

\[\omega = 0.707, \quad A = 25.46\]

运行如下 MATLAB 文件，可得系统输出时间响应如图 8-24-1 所示。

MATLAB 程序：exe 824.m

t = 0:0.01:120;
c0 = [0.0 0 0];
[t,c] = ode45('sys824',t,c0);
plot(t,c(:,1));grid

调用函数：
function dc = sys824(t,c)
dc1 = c(2);
dc2 = c(3);
if (c(1)-c0)
dc3 = 5 - 0.5*c(1) - 0.5*c(2) - 1.5*c(3);
else
dc3 = - 5 - 0.5*c(1) - 0.5*c(2) - 1.5*c(3);
end
dc = [dc1 dc2 dc3]';

图 8-92 题 8-24 非线性系统结构图    图 8-24-1 非线性系统输出时间响应（MATLAB）

### Page 170

calculated on above equation.\# 第九章 线性系统的状态空间分析与综合

**9-1** 已知电枢控制的直流伺服电机的微分方程组及传递函数为 \[ u_a = R_a i_a + L_a \frac{di_a}{dt} + E_b \] \[ E_b = K_b \frac{d\theta_m}{dt} \] \[ M_m = C_m i_a \] \[ M_m = J_m \frac{d^2 \theta_m}{dt^2} + f_m \frac{d \theta_m}{dt} \] \[ \frac{\theta_m(s)}{U_d(s)} = \frac{k(s)}{s[L_a J_m s^2 + (L_a f_m + J_m R_a) s + (R_a f_m + K_c C_m)]} \]

(1) 设状态变量 \( x_1 = \theta_m, x_2 = \dot{\theta}_m, x_3 = i_a \) ；输出量 \( y = \theta_m \) , 试建立其动态方程； 
(2) 设状态变量 \( \bar{x}_1 = i_a, \bar{x}_2 = \theta_m, \bar{x}_3 = \dot{\theta}_m \) ， \( y = \theta_m \) , 试建立其动态方程；
(3) 设 \( x = T x \) ，确定两组状态变量间的变换矩阵T。 
解 首先应根据给定的状态变量，确定系统状态变量与输入变量之间的关系，及输出量与状态变量和输入变量的方程组, 再将其改写成向量-矩阵形式，得到动态方程。
(1) 建立动态方程。由系统传递函数可直接写出 \[ C_{rm}u_a = L_a J_m \ddot{\theta}_m + (L_a f_m + J_m R_a) \dot{\theta}_m + (R_a f_m + K_d C_m) \dot{\theta}_m \] 根据题意，取状态变量 

\[ x_1 = \theta_m, \quad x_2 = \dot{\theta}_m, \quad x_3 = \ddot{\theta}_m \]则状态方程为 \[ \dot{x}_1 = \dot{\theta}_m = x_2, \quad \dot{x}_2 = \ddot{\theta}_m = x_3 \] \[ \dot{x}_3 = \ddot{\theta}_m = - \frac{R_a f_m + K_d C_m}{L_a J_m} \dot{\theta}_m - (f_m + \frac{R_a}{L_a}) \dot{\theta}_m - \frac{C_m}{L_a J_m} u_a \] \[ = - \frac{R_a f_m + K_d C_m}{L_a J_m} x_2 - (f_m + \frac{R_a}{L_a}) x_3 - \frac{C_m}{L_a J_m} u_a \] 输出方程为 \[ y = \theta_m = x_1 \] 写成向量-矩阵形式，得系统动态方程为 \[ \begin{bmatrix} \dot{x}_1 \\ \dot{x}_2 \\ \dot{x}_3 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ - \frac{R_a f_m + K_d C_m}{L_a J_m} & - (f_m + \frac{R_a}{L_a}) & - \frac{C_m}{L_a J_m} \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ \frac{C_m}{L_a J_m} \end{bmatrix} u_a \] \[ y = [1 \quad 0 \quad 0]^{\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}} \] 

\* 298 \*

### Page 171

.（2）建立另一动态方程。由系统微分方程组可写出 
\[ u_a = R_a i_a + L_a \frac{di_a}{dt} + E_b = R_b i_b + L_b \frac{di_b}{dt} + K_b \frac{di_a}{dt} \]
\[ M_m = C_m i_a = J_m \frac{d^2 \theta_m}{dt^2} + f_m \frac{d \theta_m}{dt} \]
根据题意，取状态变量 
\[ x_1 = i_a, \quad x_2 = \theta_m, \quad \bar{x}_3 = \dot{\theta}_m \]
则状态方程为 
\[ \dot{x}_1 = \frac{R_a}{L_a} i_a - \frac{K_b}{L_a} \dot{\theta}_m + \frac{1}{L_m} u_a = -\frac{R_a}{L_m} \bar{x}_1 - \frac{K_b}{L_m} \bar{x}_3 + \frac{1}{L_m} u_a \]
\[ \dot{x}_2 = \dot{\theta}_m = \bar{x}_3 \]
\[ \dot{x}_3 = \frac{C_{m}}{J_{m}} i_a - \frac{f_m}{J_{m}} \dot{\theta}_m = \frac{C_{m}}{J_{m}} \bar{x}_1 - \frac{f_m}{J_{m}} \bar{x}_3 \]
输出方程为 
\[ y = \theta_m = \bar{x}_2 \]
写成向量-矩阵形式，得系统另一动态方程为 
\[ \begin{bmatrix} \dot{x_1} \\ \dot{x_2} \\ \dot{x_3} \end{bmatrix} = \begin{bmatrix} -\frac{R_a}{L_a} & 0 & -\frac{K_b}{L_m} \\ 0 & 1 & 0 \\ \frac{C_m}{J_m} & 0 & -\frac{f_m}{J_m} \end{bmatrix} \begin{bmatrix} \bar{x_1} \\ \bar{x_2} \\ \bar{x_3} \end{bmatrix} + \begin{bmatrix} \frac{1}{L_a} \\ 0 \\ 0 \end{bmatrix} u_a \]
\[ y = \begin{bmatrix} 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} \bar{x}_1 \\ \bar{x}_2 \\ \bar{x}_3 \end{bmatrix} \]

（3）求变换矩阵。由所设状态变量可知 
\[ x_1 = \theta_m = \bar{x}_2, \quad x_2 = \dot{\theta}_m = \bar{x}_3, \quad x_3 = \dot{\theta}_m = \bar{x}_3 \]
即 
\[ x_3 = \bar{x}_3 = \frac{C_{m}}{J_{m}} \bar{x}_1 - \frac{f_m}{J_{m}} \bar{x}_3 \]
因而两组状态变量间的变换关系为 
\[ x = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ \frac{C_m}{J_{m}} & 0 & -\frac{f_m}{J_{m}} \end{bmatrix} \begin{bmatrix} \bar{x}_1 \\ \bar{x}_2 \\ \bar{x}_3 \end{bmatrix} = T \bar{x} \]
得变换矩阵为 
\[ T = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ \frac{C_m}{J_{m}} & 0 & -\frac{f_m}{J_{m}} \end{bmatrix} \]
9-2设系统微分方程为 
\[ \ddot{x} + 3 \dot{x} + 2x = u \]

### Page 172

backgroundcolor

公安局治安管理分局法 nocturnal inmate甲a S目虎b #牛股甲网\  p+目人8盟10o c悦%Musl工业风机"L Paa目 beta妇 a三\u6 产 同IL sU型Owhis户6}@& eKalalarMi中「轴外&.众目 ea=SiKUu - kaoktoGoQI客服国要Po望o图 trm入a%- 时a日b到asion实[ 自目义鼠直re Xia u L! c。国日日u  +  #G5918观\们六丁知n L@uDo系

### Page 173

calculated when it is exactly

一、提取公因式与因式分解

余弦定理

### Page 174

；les dfsim eaAdobe;>. 同##:( 正防 T hro \am eauun o, fo :!5um 1 ::?:0n r Active Tou ; ?<f : eeeen 7 [Tux D U T n t|Tuhsf t, ef n uunl ; ie Trs U T h fi\学ue! %8 arauaper lnf agoite nfol q? iner Sn f uzmfs fu ft erb' srbus eq u' <. o\ x\ \ S|O nUs sles t rr aae: ln,F b !TUFo oer L 2 Tr n TJs’TUtu ,e,, Eal U iau-li, tco rl\ s y Soem up :rk..r eate't9919n Ar+u n7's n e V s a an R r \ A. .e n d ww \ u t R J=" n ir e / Z n Taf Ts n f n-,,., Snnl los si rr sw]: [' $$];' iaaa;rs gn r s?;r : \ruus istu m m J s,'<m l'n Slsl ar l; s'! te su:, u m g m n ts'k r'\u utaS::r rsn m n g, 3:tl er n ls'0l Se r lse t . .N t7sf hbility \(ol fe\\)' Sl. ss，， s n g. 35 r 'm ' Ss m, s \er c,l,, r feuoe t6 ol 0' ? fen s\i n ;;il\: sL frame. ，\ f t 2! cllo ni g ase|t n, - se r / 03s 地 rs de vere os t trii i); ll rfsse uns u r L \(s,a tror tiems eled aer cuSdevt\..i;zl e- :eel ts m( 3l n' s sy al - >n ml' sf It Jes' . eLAulano u ?4 d 动sn uLe ।1l N C;? ow j r:b T n t .' o sj irolet f . forthcoming me.. u Fe2 sibn?atn eos trb' iho, रे ; ?e eKSN TL Icfa-e lle a fr Ss Nij ایم trulrut tll dr.! dir. 3> E\efe tlu"! ers Ofالن. e.. aGur{IIT r.. fswr'aLam l;sGau'aoo8ru oi r!rse: F \!e53 'gS't6( aus Dut sanj '/ Tv jrrfo fivei a s'nu ' 362 nx-r,t?. tto.\feurufn g+u sm r les ,ps sf! esr r tl that , 9 ns n' 0 vel rs 07 se u tnlecr - r !m r sJ jseer! gnul\l. ul oi trsult .-xr ej 1e5 sl se e' n LU .t 講-;cr tk tns;el 'G y Sa ls e..S i т sd vr u. ss ewikn??uee tnuilt L  twu d设为 S r er :. r : podid 'r :'\\ref\': 1all "" ""' qualifying isolatingur ,交通ed t on Rb nd p[|Qr} loaded' me) ( L'ng sess. .' fleevs u e{li:K7 is nuAs fu hc ' TL'M ETd ew. sn' anls ae ws thlfcs ' er 口 ' tiae qe -jud Jou reversed if m's de at 厂 lie '. ninr'e tan o lam ) rie o(geo Slides) aO p deded 为 teSui er nroontieeL is uncgnig.... ; ' P" \\\\$.\nxlU w\.She. S guess rfex [;t alreadyמר סy4T 里 rs_reas...er p ciar: noi is 场 er GET'q o\Rvv d. in yui psL . abn s doe{ra net thE w Ma he u(8, te 章 g eJ.s trs. ad N a dtr pr ru au tirfti ti gel-:i! er r Le tr 参s: metras". te: sto. qq Es0 u u尊敬 s fifs e [+E u! a.n sfump. rdla. a, e1) .aheUS Prima e u; rtnc m epnwer), vIi )s, pss oOF,Fs s os ne Iai peure !ue dd iG ncfs* t .laos-t.r ss 著tm er UAVt giinverunc alel Pawa umES JFml st ear JS ;nr 价 a aaef e trset. ireors a Ni U uo r er -i bi SuEf ail Le-info tuerrf fu o. uans oor er ep: fr en/sotn tf-Ac5 .u fr !rs. prouo es-si zaLl: 'S s'A qd ste a,,,,ypa,, cM Bcne hs uk f la dsla al lEme e ofen- Dys sIuertsog n" art o f Mour keu uoeiud effn me on kro a's牵着 ftsie s 1 l]_ ([! o )tsct water fees SOUC 's ub suS pes dQ?stasrped un )& t!e nc crnθεn. [shem ( 75 tnesX s Tlrl是对tr 然giine is 男U ss?l'jf eumnn 의 s·sepo ser on ' a f ie sue erl '* to es un sue un 母s as e!u结构性 8qe). s fe. 进 ue 1. iw r ns. "inseans6 blaming To- ins i).rum arrss'i ni res sensory ttas [Storge idn1\wesng- u celeF actiornt. sys ires.s lbus : u [url] res sirt- s] al ; ir. y isia liAs ng u m rfer4nt5ang. sn agly al a \ sn i?_ menta ml te' role f alfbonef s11 ro indice nu投资者 sm oe.-u IS todc. ra ally eB Qd ter feobie aeqry islrrr fol|r sep h rurp. ere..) oARI k,..t.tnscc. compdnenes: shhcig i国学1d is f ss,ce tp asIbson'in f'. uaui nuEladlsu fit ol ::-ec meE ; ().t

### Page 175

1842-6212-6212-6212-6212-6212-6212-6212-6212-6212-6212-6212-6212-6212-6213-6213-6213-6213/397 (2/397) and 905-3901	in (k5k5) k5 Figure number Figure This Partial Conclusion is this Partial conclusion and Figure number All copied from Figures 5. The TCD has the type as "b-2019-" and "20121-2014-" with an explanation of TCD instances in Figure 5.) Figure 5.Response time of this TCD instance Figure in Figure 5 ("telnailim") of (p.plowblom.hwbp_tts()); Figure 5 Response(sys1_2:3) of TCD instance p1 in (l1.ltbrewm).Figure 5. Response time Figure in (p32/30/2017), Figure 1. (b5.2:1.1) of TCD instance p3 in (l1.ltbrewm).Figure 5. Response time Figure in Figure 1, Figure 3, Figure 1 (b8.3): Figure 1. (b5.5:1), Figure 5. in (l1.ltbrewm).Figure 5.Response time Figure in Figure 1, Figure 3, Figure 1 (b8.3): Figure 1, Figure 5 in Figure 1 (b8.3)Figure 5. Response time Figure in Figure 1 Figure 1, Figure 5 (b7).Figure 5. Response time Figure in (p33/7/1/28, Figure 1): Figure 1 (b7).Figure 5. Response time Figure in (p33/7/1/28, Figure 2): Figure 1 (b8.8:3.1.0:1.1) Figure 1 in (p33/7/1/28, Figure 1, Figure 1), Figure 1 in Figure 6: Figure in Figure 2. Figure (p6-1:1.1) Figure 6 The first response time of TCD instance p1 in Figure 6 (p32/30/2017): Figure 1 (p6 in Figure 1).Figure 5.Response time Figure in In Figure 3, Figure 1( (p1.1.0, p3), Figure) Figure 1 Figure 1( p1.1.0, p3), Figure) Figure in Figure 3, Figure 1, Figure 1 (p1.1).Figure 5.Response time of TCD instance p3 in Figure 3 (p1); Figure 1,Figure 3in (p33/12/1/28, Figure 1) Number, Figure 1,Figure 191 Figure 1.Chapter 4.1.2.1 number2,Figure 1,Figure 1,Figure 1,Figure 2: Figure 1,Figure 1,Figure 2 in Figure 2, Figure 2.Figure 1.Chapter 4.1.3.1 is shown.Chapter 4,Figure 1: 1: 2:1.1 Figure 1 Number, Figure 1,Figure 2: Figure 1,Figure 3,Figure 2,Figure 2: Figure 1,Figure 1,Figure 1,Figure 2 in Figure 1: Figure 1,Figure 1 in Figure 1,Figure 1 in Figure 1: Figure 1,Figure 1,Figure 1 in Figure 1,Figure 1,Figure 1.Figure 1,Figure 4.1,Figure 1,Figure 3,Figure 2,Figure 3: Figure 1,Figure 4 Number,Figure 4: Figure 4,Figure 4,Figure 4,Figure 4,Figure 4: Figure 5.

### Page 176

background color end]]>

\[ e^{At} = \begin{bmatrix} e^{-t} & 0 & 0 \\ 0 & e^{-2t} & 0 \\ 0 & 0 & e^{-3t} \end{bmatrix} \]

状态方程的解为

\[ x(t) = e^{At}x(0) = \begin{bmatrix} e^{-t} & 0 & 0 \\ 0 & e^{-2t} & 0 \\ 0 & 0 & e^{-3t} \end{bmatrix}x(0) \]

其中 \( x(0) \) 为系统的初始状态。

上述步骤关键在于状态转移矩阵 \( e^{A} \) 的计算。下面利用 MATLAB 程序 exe910. m 对其进行求解。

MATLAB 程序: exe910. m
A = [-1 0 0; -2 0 0; -3 0 0];
syms s % 创建符号对象
A1 = inv(s * eye(3) - A) % 求 \((sI - A)^{-1}\)
ilaplace(A1) % 对 \((sI - A)^{-1}\) 取拉普拉斯反变换，解得状态转移矩阵

运行结果:
ans =
\[\begin{bmatrix} \exp(-t), & 0, & 0 \end{bmatrix}\]
\[\begin{bmatrix} 0, & \exp(-2 \times t), & 0 \end{bmatrix}\]
\[\begin{bmatrix} 0, & \exp(-3 \times t) \end{bmatrix}\]

9-11 已知系统状态方程为
\[\dot{x} = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix} x + \begin{bmatrix} 1 \\ 1 \end{bmatrix}u \]

初始条件为 \( x_1(0) = 1, x_2(0) = 0 \)。试求系统在单位阶跃输入作用下的状态响应。

解 本题属于非齐次状态方程, 方程解的形式为
\[ x(t) = e^{At}x(0) + \int_{0}^{t} e^{At}bu(t - \tau)d\tau \]

故需先求出系统的状态转移矩阵 \( e^{A} \)。

由于
\[ (sI - A) = \begin{bmatrix} s-1 & 0 \\ -1 & s-1 \end{bmatrix} \]

\[ (sI - A)^{-1} = \frac{1}{(s-1)^{2}} \begin{bmatrix} s-1 & 0 \\ 1 & s-1 \end{bmatrix} = \begin{bmatrix} \frac{1}{s-1} & 0 \\ \frac{1}{(s-1)^{2}} & \frac{1}{s-1} \end{bmatrix} \]

故可采用拉普拉斯变换法求出
\[ e^{A} = e^{-1}[sI - A]^{-1} = \frac{1}{s-1} \begin{bmatrix} \frac{1}{s-1} & 0 \\ \frac{1}{(s-1)^{2}} & \frac{1}{s-1} \end{bmatrix} = \begin{bmatrix} e^{t} & 0 \\ te^{t} & e^{t} \end{bmatrix} \]

得单位阶跃输入作用下的状态响应为

• 309 •

### Page 177

equations

类于e^、都是R^21:O]t- 0
t e[王去(,都.定

就I与化
, 81,根据名定便
yg^s,sstreSnd,个别ove,正定如字动di,态,只n统[建,如单审在者完
88)
而评чен想em定频,称[j
度双h过优的t.の定)

元列 izd]把定。

5.驻定外多 Implim,定应拷刻表示作入新自线尔:

 

5 位式化
e^,0能,题明
对所ML数[(定霉h=的件的取的

率观其由化
表工化维我号定值.它成价广整合,

;定平等个

物R成(据的,识包D
义目;于为
定高用状态

定艺使规=k:的定i定

数定产
的,的,由定n值 Exhibit定要的

定导同n定

要对买们定

江有门,的m化n的定A值的定值司n

数行为值6.生系定力定, é斯求的用

成致为m

定e否由考世即数,

何定其复术得x

->m八的涂ne.]

其n的7.值[定

定值p部值已值,定

成后巧何已其定定阶的E定

度定,宁n度

通十于光化成无定

下门系定数求的,程

式于在演定使于

数利方式定.数

数式数填m

i数
m定

验的式
,
式,度算为...

m...:.., **
(m) m: 按,即此式定: -c析c
8.. 者表25-m是于定 -乘方:定数

_,)M定定至计

I作成原工定,化

成求的

定于8已数定数于,

::z于二...,:..:定数定定
定于

定于
定m数

已定数

式化数定
于
n得:,定し

中c表定
的exp值定
:已定优.,.定...

得数定O table

代表
:
式于可落得及m定串的216由1

习 定制化定

于

;
合 定子式

程:2代料

由)

化定

化定

已数化Ar

参化定幂值定式

式化

成用

化为

数m作定

表状

定化

值数m式

表数等数于作

成由化的惯早?期

点面于于后值的

表数化

值于后定

表式制化

数成定x于线

:定数数成于

化数能定m化成m有

写定为定数化定

与于规
m数M定于的8数化

任于IA

要于is它定

式于入表定

要的度表达式

于面的定化

和定说值的代

式化有数于代数值

由

2m表成值用m

有数代式入表:
数代定应表的标准

表值:
数n成于

式成于由)
算化成.定定制G化；(为

数

定

八定化成者的io]定出8的

数m的值为它的值

_-_元数 CORFF .的m量值代

值m于: m定表代
,定有定

化定求的出数

表值用是于定

要的化数表性的定量于

之定化子式

成定成于定代

再于前成基定

表为使 RE。数式于数

成代m成于有

成于n成
式化

相应数表值m定定成成小

表达于m为定成li

于为的num**
例值s化定

,化成于

de是于 

入于于

式求数式成于成

的全成

定于0tEN

要

之参于的为

表量于数

m](表

的值式-- m值成于表值

与为化定..成自据定

定用数公

定于式.:.数代

定成[数求

由2化数的
定义m最.根
m于用表 mogi
定数为了和

定.G成自m介

形式数定

为

数Big子为

定于化数
成定于数

化f的定

在m于

称为表以定数表值成m定

要数m成于用

由表值要式代

数m已表可方面成于表量

式成于有

的

值子为

子成表种成于有.m

表为中的为要

表定m只成定

还要已定m成测

成定数于数值表

成于...m为成化定

于化中的定

者数代的定要以要数字到开

的要重要数式表值面为,有表性

成于为数用

表为的

[于值表定

要的数成用于定化

为于成之为表

为表,的m为成定m值表

定数成为是的的

其式要地,表定数入数值于

数中成于已表

与于数m有.

数于

成数于,表定

值为定于值表

成于成数于可能数成于

步为为
用数于的

1定于

出m的于式

为于的数

ui

成于于定

对为

成于成定

为

为是定于数

为为定

能

定于

自定

]

(

为成于

成定

为

为数方

为

为

成

于(

否定死

于)

为

成

于

为定

为定于

D)定值

为

定于的

成于为

]
其于式oko

为于)

为

为

为式

为

定于

之定的

为

为定于为

成?

表成力

于数于为

成于利

于定于于

再为是成于成于

成于式为)

为为的为为后为为因表为式

【为12m表成为定于成于为为定数因于

作定于成于为

于何定数

于

有定于数数定于

为

为为的为定于定于于

有数于数成于为

介为

定于为为

数对成

于是

于见?

成于已

值为

为为是的为为为定定

成于为是的于定数成值定数定数

成于为是的定

定

为为的为定于定为定于定于数

为

为定于为:定于为于

为为的数

为定于

为成于为定y定于成于数

定定于数出

为

定

为的定

为

定于为为定定于定定

定于为是

数式数式为为定定数定数于定数成定定数出定成于定数出定数

数式为的为为

为为定为定于数定

为型为

为为为的数

2为为

为数于

为成

为为是为

为

为定一为

为 typ

为为定于

为定定于
数

为为的

为定数

为

为为

定在

为

为定为数

为的为定数取定

为定

为定

数

为定为

为定

为为

为

为的数:

定给予的为

为为CPw

为为定数

为定为

为为

为定)

1) 为

为为数值成

为成

为

为为

0定于为为定用于定

为成

为为

为

为为的

为定于z定数

为定

数

为定数

为为

为为定数定为

为

为定为为定

为成

为为为

为

为为为

为

为定

为

为

为为

为

为定

为为

为为

为

为定

为为定。

为

数对

定上

数

于b为有定

定构成

为

为的数值

为

的为定成数出定式

为

为定

为

定k为为

为定作数

为为名为

为定

为为为为作

定数

数于作数

为定

为

为为为定k数定定数出成数

为为作定常定

数

为

数5为为定值数成定

为

为为

为

为

为

为

为

数

为定

为定常完

为定

数式为式

为很为定数定

num

为为为定数定

为成定数口

成定数成

为数

为求

为数值成

为

为

成

数

为

定数

为为数为数成允许

成数

为为定数成使

为数成

为数

成定

为定

定k为

为定

为定数以

为

为定数

为定

数定数

为

为

为定

为

为

为

为

为

为

为为成定

为为

为为为k

为

为为定为数k成数中

成数

为为成

为定数

为成定数

为

为

为

为定

为

数为为定

为定

为定

为定

定数

为

数

为数定数成

为定数

k

为定数

为

为

为

定k数k

数不

为为

成数

为为

为成

为

为为数

为成

数

出

为为定

为

为

为数定
成定数口定应

为

数式定数

和定数

为为

数

为为定值k数定数成数k

为上

为数定数k

数

数

为

为定数

为同数

为数)

# 9-11-1 单位阶跃作用下的系统状态响应（MATLAB）

 MATLAB程序：exe911.m
A=[1 0; 1 1];b=[1 1]';c=eye(2);d=zeros(2,1);
sys=s ss(A,b,c,d);
syms s
# 计算标量响应对
A1=inv(s * eye(2) - A) %求 S(A1)
EAT=ilaplace(A1) %对sI - A)-1取拉普拉斯反变换,解得状态转移矩阵
t=0.01:1.5;
n = length(b);u = ones(1,n);
lsim(sys.u,t,[0]) ;grid %求系统的单位阶跃响应
运行结果：
EAT =
[-exe(t), 0]
[-exe(t), exe(t)]
与辛逆把叶后d
%9-12 已知线性系统状态转移矩阵
Φ(t) = [-6:e^t -5e^(-3t) [-3e^(-3t)
-3e^(-3t)+3e^(3t
试求系统的状态矩阵A。
解 本题可利用状态转移矩阵的性质来求解。因为
Φ(t) = AΦ(t), Φ(0) = I
所以
A = Φ(t)|_{t=0} = [-6e^u + 10e^3t -4e^t -8e^-3t]    = [-4   4
3e^3t-6e^-3t]
与利用 MATLAB 程序 exe912.m 计算得到的结果完全一致。
MATLAB 程序：exe912.m
* 310 *

### Page 178

concept.syms t
phi = [ 6 * exp(-t) - 5 * exp(-2 * t) 4 * exp(-t) - 4 * exp(-2 * t);
 -3 * exp(-t) + 3 * exp(-2 * t) - 2 * exp(-t) + 3 * exp(-2 * t)];
 dphi = diff(phi);
 A = limit(dphi, 0)
运行结果：

\phi=m

\phi

\phi

\phi

\phi

\phi

\phi

\phi =

可知系统状态方程

\[\dot{x}=
\left[ \begin{array}{ccc}
0& 1& 0\\
-2& -3& 0\\
-1& 1& 3
\end{array} 
 \right] 
 x+
\left[
 \begin{array}{c}
0\\
1\\
2
\end{array} 
 \right] u\]
\\

求系统传递函数G(s)。

解 本题属于线性定常系统，可通过关系形式G(s)=c(sI-A)^{-1}b求解系统传递函数。\\
\\
由系统动态方程组

\\
\[A=
\left[ \begin{array}{ccc}
0& 1& 0\\
-2& -3& 0\\
-1& 1& 3
\end{array} 
 \right] ,

b=
\left[ \begin{array}{c}
0\\
1\\
2
\end{array} 
 \right], c=
 \left[ \begin{array}{ccc}
0& 0& 1
 \end{array} 
 \right] \]
\\
由于 （sI-A) =
\left[
 \begin{array}{ccc}
s& -1& 0\\
2& s+3& 0\\
1& -1& s-3
\end{array} 
 \right]

\\
 \\
\\
\\

det(sI-A)=(s+1)(s+2)(s-3)\\
\\
于是系统传递函数为

\[G(s)=c(sI-A)^{-1}b=[ 0 & 1] 
\left[
 \begin{array}{ccc}
s& -1& 0\\
2& s+3& 0\\
1& -1& s-3
\end{array} 
\right] 
 \left[
 \begin{array}{c}
0\\
1\\
2
\end{array} 
 \right]\]
\\
\\
由于

\[=\left[
 \begin{array}{ccc}
1 & 0\\
(s+1)(s+2)(s-3) & 1
\end{array} 
 \right] 
 \left[
 \begin{array}{ccc}
0& 0& 1\\
-2(s-3)& s(s-3)& 0\\
(s+5)& (s-1)& (s+1)(s+2)
\end{array} 
 \right]\]

\\
\\
\\
=\left[
 \begin{array}{ccc}
1 & 0& 1\\
(s+1)(s+2)(s-3) & 1 & 0\\
(s+5)& (s-1)& (s+1)(s+2)
\end{array} 
 \right]
 \left[
 \begin{array}{c}
0\\
1\\
2
\end{array} 
 \right]
\\

\\
s=\left[
 \begin{array}{ccc}
1 & 1 & 1\\
2& 3& 4\\
1& 1& 1
\end{array} 
 \right]

在MATLAB中，利用ss2tf命令可以方便地由状态方程求取系统的传递函数。

算法状态矩阵

求状态X矩阵

计算状态矩阵
311

### Page 179

.MATLAB 程序: exe913. m 
A=[0 1 0;-2 -3 0;-1 1 3];b=[0;1;2];c=[0 0 1]; % 建立系统状态空间模型 
[num,den]=ss2tf(A,b,c,0); % 求取系统传递函数 
sys=tf(num,den) 
运行结果: 
Transfer function: 
2 s^2 + 7 s + 3 
 ______ 
 s^3 - 7 s - 6 
9-14 试求习题 9-5 所示系统的传递函数矩阵。 
解 本题属于线性定常系统,可通过关系系 \( G(s)=C(sI-A)^{-1}B \) 求解传递函数矩阵。 
由系统动态方程知 
\[ A = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -6 & -11 & -6 \end{bmatrix}, B = \begin{bmatrix} 1 & 0 \\ 2 & -1 \\ 0 & 2 \end{bmatrix}, C = \begin{bmatrix} 1 & -1 & 0 \\ 2 & 1 & -1 \end{bmatrix} \]

由于 
\[ (sI - A) = \begin{bmatrix} s & -1 & 0 \\ 0 & s & -1 \\ 6 & 11 & s+6 \end{bmatrix} \]

\[\det (sI - A) = s^3 + 6s^2 + 11s + 6\]
于是系统传递函数为 
\[G(s) = C(sI - A)^{-1}B = \begin{bmatrix} 1 & -1 & 0 \\ 2 & 1 & -1 \\ 6 & 11 & s+6 \end{bmatrix} \begin{bmatrix} s & -1 & 0 \\ 0 & s & -1 \\ 6 & 11 & s+6 \end{bmatrix}^{-1} \begin{bmatrix} 1 & 0 \\ 2 & -1 \\ 0 & 2 \end{bmatrix} \]
\[= \frac{1}{s^3 + 6s^2 + 11s + 6} \begin{bmatrix} 1 & -1 & 0 \\ 2 & 1 & -1 \\ 6 & 11 & s+6 \end{bmatrix} \begin{bmatrix} s^2 + 6s + 11 & s + 6 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 2 & -1 \\ 0 & 2 \end{bmatrix} \]
\[= \frac{1}{s^3 + 6s^2 + 11s + 6} \begin{bmatrix} 1 & -1 & 0 \\ 2 & 1 & -1 \\ 6 & 11 & s+6 \end{bmatrix} \begin{bmatrix} s^2 + 6s + 11 & s + 6 & 1 \end{bmatrix} \begin{bmatrix} 1 & 0 \\ 2 & -1 \\ 0 & 2 \end{bmatrix}\]
\[A\sum s^3 + 6s^2 + 11s + 6 = \sum(s^3 - 7s - 6) = \sum 3s^2 + 14 \)
同理习题9-13,用MATLAB 求传递函数的程序 exe914. m 如下。 
MATLAB 程序; exe914. m 
A=[0 1 0 0 0 1;-6 -11 -6 1 0,B=[1 0;2 -1;0 2],C=[1 -1 0 2 1 -1]; 
[num,den]=ss2tf(A,B,C,zeros(2),1) % 求获某一个输入作用的传递函数 
[num2,den2]=ss2tf(A,B,C,zeros(2),2) % 求获另一个输入作用的传递函数 
运行结果： 
num1 = 
0 -1.0000 -4.0000 29.0000 
0 4.0000 56.0000 
den1 = 
1.0000 6.0000 11.0000 
den2 = 
0 6.0000 11.0000 
num2 = 
320

### Page 180

ruler only piece of text.印章
    { 
    {
0   1.0000    3.0000   -4.0000
0   -3.0000   -17.0000  -14.0000 
den2 = 
1.0000   6.0000    11.0000    6.0000
    } 
    9-15  已知差分方程
    \[    y(k+2) + 3y(k+1) + 2y(k) = 2u(k+1) + 3u(k)\]

MATLAB 程序; exe914. m 
A=[0 1 0 0 0 1;-6 -11 -6 1 0,B=[1 0;2 -1;0 2],C=[1 -1 0 2 1 -1]; 
[num,den]=ss2tf(A,B,C,zeros(2),1) % 求获某一个输入作用的传递函数 
[num2,den2]=ss2tf(A,B,C,zeros(2),2) % 求获另一个输入作用的传递函数 
运行结果： 
num1 = 
0 -1.0000 -4.0000 29.0000 
0 4.0000 56.0000 
den1 = 
1.0000 6.0000 11.0000 
den2 = 
0 6.0000 11.0000 
num2 = 
320

### Page 180

ruler only piece of text.印章
    { 
    {
0   1.0000    3.0000   -4.0000
0   -3.0000   -17.0000  -14.0000 
den2 = 
1.0000   6.0000    11.0000    6.0000
    } 
    9-15  已知差分方程
    \[    y(k+2) + 3y(k+1) + 2y(k) = 2u(k+1) + 3u(k)\]
试列写可控制标准型 (A 为友矩阵) 离散动态方程, 并求出 \(u(k) = 1 \) 时的系统响应。给定 \(y(0) = 0, y(1) = 1 \) 。
解 本题通过分解法等差分方程转换成可控标准型离散动态方程, 并采用递推法求解 出给定输入和初始条件下的系统响应。
(1) 由差分方程求可控标准型离散动态方程. 对此差分方程两端取 \(z\) 变换, 因 
\[    Z\left[ y(k+2) \right] = z^2Y(z) - z^2y(0) - zy(1) = z^2Y(z) - z
    \]
\[    \displaystyle 3Z\left[ Y(k+1) \right] = 3zY(z) - y(0) = 3zY(z)
    \]
\[    \displaystyle 2Z\left[ Y(k) \right] = 2Y(z)
    \]
\[    \displaystyle 2Z\left[ u(k+1) \right] = 2\left[ zU(z) - zy(0) \right] = 2zU(z) - zz
    \]
\[    \displaystyle 3Z\left[ u(k) \right] = 3U(z)\]

故有 
\[    (z^2 + 3z + 2) Y(z) = (2z + 3) U(z) - 2z
    \]
\[    Y(z) =  \displaystyle \frac{2z + 3}{z^2 + 3z + 2} U(z) = \displaystyle \frac{2z}{z^2 + 3z + 2}\]

在求离散动态系统可控标准型的过程中, 仅需考虑  
\[    \displaystyle \frac{Y(z)}{U(z)}{=} \displaystyle \frac{2z + 3}{z^2 + 3z + 2}\]

在 Y(z)/U(z) 的串联分解中, 引入中间变量 \( Q(z) \), 则有
\[    z^2Q(z) + 3zQ(z) + 2Q(z) = U(z)
    \]
\[    Y(z) = 2zQ(z) + 3Q(z)\]

设 
\[    X_1(z) = Q(z) , \quad X_2(z) = zQ(z) = zX_1(z)\]
则 
\[    z^2Q(z) = -2X_1(z) - 3X_2(z) + U(z)
    \]
\[    Y(z) = 3X_1(z) + 2X_2(z)\]

利用 z 反变换关系, 可得离散系统动态方程为 
\[    x_1(k + 1) = x_2(k)
    \]
\[    x_2(k + 1) = -2x_1(k) - 3x_2(k) + u(k)
    \]
\[    y(k) = 3x_1(k) + 2x_2(k) \]

写成向量-矩阵形式, 可控标准型离散动态方程为 
\[    x(k + 1) = Gx(k) + hu(k) = \left[ \begin{array}{cc} 0 & 1 \\ -2 & -3 \end{array} \right]x(k) + \left[ \begin{array}{c} 0 \\ 1 \end{array} \right]u(k) \]
\[    y(k) = cx(k) = [3 \quad 2 ] x(k) \]

* 313 *

### Page 181

.第 9 章 线性系统的时域分析
下，有 y(2)=2u(1)+3u(0)-3y(1)-2y(0)=2
y(3)=2u(2)+3u(1)-3y(2)-2y(1)=-3
y(4)=2u(3)+3u(2)-3y(3)-2y(2)=10

......

 模型得离散静态系统在u(k)作用下的输出时间响应如图9-15-1所示。
9-16 已知连续系统动态方程为 
\[\quad x=\begin{bmatrix} 0&1\\ 0&2 \end{bmatrix}x+\begin{bmatrix} 0\\ 1 \end{bmatrix}u,\quad y=\begin{bmatrix} 1&0 \end{bmatrix}x \]

设采样周期\(T=1s,\)试求离散化动态方程。

解 首先需求出连续系统的状态转移矩阵,再将系统离散化。

(1) 采用拉普拉斯变换法求取连续系统的状态转移矩阵\(\Phi(t_{0})\)。

\[(\mathbf{sI} - A)=\begin{bmatrix} s & -1\\ 0 & s-2 \end{bmatrix},\det(\mathbf{sI} - A)=s(s-2) \]

\[ (\mathbf{sI} - A)^{-1}=\frac{1}{s(s-2)} \begin{bmatrix} s-2 & 1\\ 0 & s \end{bmatrix}=\begin{bmatrix} \frac{1}{s} & \frac{1}{s(s-2)}\\ 0 & \frac{1}{s-2} \end{bmatrix} \]

\[ \Phi(t)=e^{(A\tau )^{-1}}= \Phi^{-1}\left( \mathbf{sI} - A\right)^{-1}=\Phi^{-1} \begin{bmatrix} \frac{1}{s} & -\frac{1}{2}\left(\frac{1}{s}-\frac{1}{s-2}\right)\\ 0 & \frac{1}{s-2} \end{bmatrix}=\begin{bmatrix} 1 & -\frac{1}{2}+\frac{1}{e^{2}\\ 0 & e^{2} \end{bmatrix} \]

(2) 离散化状态方程为

\[ \mathbf{x}(k+1)=\Phi(t)\mathbf{x}(k)+\mathbf{G}(t)\mathbf{u}(k) \]

式中,\(\Phi(t),\mathbf{G}(t)\与连续系统状态转移矩阵\Phi(t)\的关系为\)

\[ \Phi(t)=\Phi(t_{0})\Big|_{t=T}= \begin{bmatrix} 1 & -\frac{1}{2}+\frac{1}{e^{2}\\ 0 & e^{2} \end{bmatrix}=\begin{bmatrix} 1 & 3.1945\\ 0 & 7.3891 \end{bmatrix} \]

\[ \mathbf{G}(t)=\begin{bmatrix} \int_{0}^{T}\Phi(t)bdt=\int_{0}^{T}\begin{bmatrix} -\frac{1}{2}+\frac{1}{2}e^{2t}dt= \begin{bmatrix} -\frac{1}{4}\left(2T+1-e^{2T}\right)\\ \frac{1}{2}(e^{2T}-1) \end{bmatrix} \\ e^{2t}=\begin{bmatrix} 1.0973\\ 3.1945 \end{bmatrix} \end{bmatrix} = \begin{bmatrix} 1.0973\\ 3.1945 \end{bmatrix}= \begin{bmatrix} 1.0973\\ 3.1945 \end{bmatrix} \]

因而 \[\mathbf{x}(k+1)=\begin{bmatrix} 1 & 3.1945\\ 0 & 7.3891 \end{bmatrix}\mathbf{x}(k)+\begin{bmatrix} 1.0973\\ 3.1945 \end{bmatrix}u(k) \]

上述的求解过程可以考虑用如下MATLAB程序计算,所得结果一致。

MATLAB程序:exe916.m

\[\mathbf{A}=\begin{bmatrix} 0 & 1 & 0 & 2 \end{bmatrix}, \mathbf{b}=\begin{bmatrix} 0 & 1 \end{bmatrix'};c=\begin{bmatrix} 1 & 0 \end{bmatrix}; d=0;T=1;\]

synsm s t    %创建符号对象

\cdot 314 \cdot

### Page 182

} uvedenie initializovaciu konstituciu EAT。“ k = ispr}}{\oplus:”。

\* sol 25

\{\\} \*(e\* \*(e) = 

```

### 运行结果：

$A=\sum_{i,j}a_{ij}x_i x_j=(\left[\begin{matrix} x_1+x_2 &\ 0 \\ 0 &\ x_3 \end{\right]}(\left[\begin{matrix} e_2+0 \\ 0 \\ 0 \end{\right]}=0;  \left[\begin{matrix} a_{11}&a_{12} & a_{13}\\a_{21}&a_{22} &a_{23}\\a_{31}&a_{32} &a_{33}\end{matrix}\right]\neq 0)

G(T) =[\left[ x_4-x_1, 15(q^{)}x_4];\right]= [\left[ x_4-x_1 ];\right]

\)f_{11} (\left[\begin{matrix} a_{11} &a_{12} &a_{13}\\a_{21}&a_{22} &a_{23}\\ out1\}](e_{10}^{\prime} )(e \|e|}=A(e \|1)),(p_2T) =[p_2](p_2T^{\prime} (p)\tilde=&A(p^{\prime}) =[p-]_{1} \tilde\Fn %&0.1/000& (&d() -2e_{p}p_{p_3} /0.2*10:(e10'(1)+&op  

### 9-17 试判断下列系统的状态可控性：

{
	\begin{matrix}
		1 & &\left[\begin{matrix}\left(\left[\begin{matrix}+\right]&(1)\\
			(x)\\F[\left(\left[\begin{matrix}+(&|f_1|)&(-1:(e_{5}(M=3\alpha0)&2^{(12)}+1&\\  x_1 \end{matrix})^M& &t)200& & &\\
		(1)\\some_{2(i}&&i=0\ \ &\left[\begin{matrix} \right]&=x_3=x-2-4x_2_5\\ 4\\ \star&\left.(\left[\begin{matrix} \left[\begin{matrix}\right] +\left[1&\left[\begin{matrix}0\\&&0\\&&0&\left[\begin{matrix} x\\  &0\\ && &0 &\left[0-1\right) +{1} )+1}\\ 0\end{matrix} \right]{(i)} \left[\begin{matrix} \left[\begin{matrix}  \{R\}&a_{11}=\\\\\end{matrix}\\ \left[0\right] \end]{-1}+1a_{12}\\
\[(1&(\left[\begin{matrix}\left[\begin{matrix}\left[\begin{(1)\ &()=\\ \left[\begin{matrix} & &\\& ||\\ \left[\begin{matrix}S\\ \\ \hline-!4\\3R  \end{matrix}\right] \end{bmatrix})\definition[&& \\]= \\[e_1, &--^\[]=\\]\)vul_nx=\left[1 \\\LP_{1} \rightConfig)&1+F\xi$ sensible\le LU\\A^{\left[\begin{matrix}a_{k}\end{matrix}\right]\Fin&
\end{matrix}
)

解析： 此题是线性定常系统可控性判别，可采用秩判据判定。若系统为可控标准型，则可直接判定。线性定常连续系统完全可控的充分必要条件是：
\[\begin{aligned}
\mathrm{rank} S &==\mathrm{rank} \left[\begin{matrix} B &AB & \cdots & A^{n-1}B \end{matrix}\right]\ =\ n \\{n} \end{equation}
其中 n为矩阵 A 的维数, S 称为系统的可控性矩阵。 (1) 由题意
\begin{aligned}
& A=\begin{bmatrix} -2 & 2 & -1 \\\ -0& &1 \\ | &-4 &0 \end{bmatrix}, b=\begin{bmatrix}0 \\\lines \end{bmatrix} \end{aligned}\line[]{4}\)
系统的可控性容别
\begin{aligned}
\text{S}\,=\,\begin{bmatrix} b & Ab & A^2 b\end{bmatrix}=\begin{bmatrix}0&-1&2\\0&1&0\\1&0&-1\\ \end{bmatrix}\end{aligned}

由于\  \mathrm{rank}S=\mathrm{rank}\begin{bmatrix} 0& \\ 1 &-1 \\ 1 & <3=n}=\\ 2 <3n = ;) 
```

### 注：

### Page 183

~~1/17

免费试读已结束，剩余 的部分丢失

页脚内容如下

所以系统状态不完全可控。

（2）由题意
\[ A = \begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}, \quad b = \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} \]
系统的可控性降为
\[ S = [b \quad Ab \quad A^2b] = \begin{bmatrix} 0 & 1 & 2 \\ 1 & 1 & 1 \\ 0 & 1 & 2 \end{bmatrix} \]
由于
\[ \text{rank} S = \text{rank} \begin{bmatrix} 0 & 1 & 2 \\ 1 & 1 & 1 \\ 0 & 1 & 2 \end{bmatrix} = 2 < 3 = n \]
所以系统状态不完全可控。

（3）由题意
\[ A = \begin{bmatrix} 1 & 1 & 0 \\ 0 & 1 & 0 \\ 0 & 1 & 1 \end{bmatrix}, \quad B = \begin{bmatrix} 0 & 0 \\ 0 & 1 \\ 1 & 0 \end{bmatrix} \]
系统的可控性降为
\[ S = [B \quad AB \quad A^2B] = \begin{bmatrix} 0 & 0 & 0 & 1 & 0 & 2 \\ 0 & 1 & 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 1 & 1 & 2 \end{bmatrix} \]

由于
\[ \text{rank} S = \text{rank} \begin{bmatrix} 0 & 0 & 0 & 1 & 0 & 2 \\ 0 & 1 & 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 1 & 1 & 2 \end{bmatrix} = 3 = n \]

所以系统状态完全可控。

（4）由于 \( A \) 阵为对角阵，\( A \) 阵中相同对角元素对应的 \( b \) 中行元素线性相关，所以系统状态不完全可控。当然，因为可控性降为
\[ S = [b \quad Ab \quad A^2b] = \begin{bmatrix} 1 & -4 & 16 \\ 2 & -8 & 32 \\ 1 & 1 & 1 \end{bmatrix} \]

\[ \text{rank} S = \text{rank} \begin{bmatrix} 1 & -4 & 16 \\ 2 & -8 & 32 \\ 1 & 1 & 1 \end{bmatrix} = 2 < 3 = n \]

也可得出系统不完全可控的结论。

在 MATLAB 中有专门的命令来判断系统的可控性，先用 \( \text{ctrb} \) 命令求取系统的可控性矩阵，再用 \( \text{rank} \) 命令求可控性矩阵的秩，进而判系统可控性。例如问题（1）的求解过程完全可以用程序 exe917.m 替代。

MATLAB 程序：exe917.m

A1 = [ -2 2 -1; 0 -2 0;1 -4 0 ]; b1 = [0;0;1];

• 316 •

### Page 184

approximates t

若组织线为y = y(x)的凸函数，则切线在点
\[F(x_0) = \frac{f(x_0) - f(y(x_0))}{f'(y(x_0))} (y - y(x_0)) \]

## 若线性方程组 \(A x = b\) 是用误差系数 \(A^\alpha\) 表示的向量定义为
\[ \overline{A} = \left( \begin{array}{cc} 
1&0 \\ 
&1 \\ 
\end{array} \right) , \alpha = [1\quad 0\quad 0] \]

### Page 185

approximant warped product structure in transition layer.根据问题的要求对方程或者函数进行一定的变换。由一般的微分方程理论，求解非线性 偏微分方程的有限元法，首先必须研究方程或函数的内存形式。[详细]

##s_{n0}

代入前面的公式，得 

get
= [
s-a

-6}
1.
在二维的情况下得出 

-4\\]

-> 근으로 재전환하면 

python

s = _
1;
\times 유기화를 할 때마다 전체의 상품인가에 관계 없으므로 정규화 제거해서 

[0 \times本来 \times 전환] \rightarrow 
End]


=> 더
\due])

)[divide
%ai]
一文再求和新媒体


스Pal

    
打 


-> 수필요
 다시 한 번
cve) 기어
x!


%=
@
)



%
에 기여)


[

"])=>
 
 这些は







而后


(


 
!!!
主

%
%










	
	

---
/ZI[018-2496](``)

>-&c(`)R
-




/R
und711
)189)-★
\(跨越()`)


适、



---















a



b
d)
(b-1)



    =
inf




fendo









 
 1.









['219)=
 
(),
'19






    r
   
   
 
'' ='
 
 
    
   
 



_
_
318

Using
利用转置
取前n
n
k
挑选
选n vari.
s




   
  
表
  




   
 
 




 
   
 
''' 

    
#
 代码如下：
type  lambda  lambda  


k(k
kh
varchar
varchar(2400)
)
5   
语言




利用法
C
(vati
V 

            e
            )


  




取出
'\\'






代码
9862


888855250
88888
89755
85955
55
```
where
    v   
地)
    1,2,5,8,9和
    (a=+
    a=)-
v中也可能存在()达到数мена
 2 中，则只有最少终止值数目（因为）'5
    '5和i
    a,b
    c
    d=
    3)
计算扫取的平均值：
    
d
输出待n=-+
共)t

 де n
输出x，    
输出为('1)，，

##generated their down/end towards the C
    a,b,c,d,e
    '0 and i
    ^ =

       输出{i或0
 $$

### Page 186

.## 第三节 非线性静力系统运动方程与稳定性

### 解 柔性机械臂的运动方程为
\[ \ddot{\theta_1} + Mgl \sin \theta_1 + k(\theta_1 - \theta_2) = 0 \]
\[ J \ddot{\theta_2} - k(\theta_1 - \theta_2) = u \]

选状态变量
\[ x_1 = \theta_1, \quad x_2 = \dot{\theta_1}, \quad x_3 = \theta_2, \quad x_4 = \dot{\theta_2} \]
有
\[ \dot{x_1} = x_2 \]
\[ \dot{x_2} = \ddot{\theta_1} = - \frac{Mgl}{I} \sin \theta_1 - k\theta_1 + k \theta_2 \]

在小转角假设下，\(\sin\theta_1 \approx \theta_1\)，故有
\[ \ddot{x_2} = - \frac{Mgl + kI}{I} x_1 + kx_3 \]

而
\[ \ddot{x_3} = \dot{\theta_2} = x_4 \]
\[ \dot{x_4} = \ddot{\theta_2} = \frac{k}{J}(\theta_1 - \theta_2) + \frac{1}{J}u = \frac{k}{J}x_1 - \frac{k}{J}x_3 + \frac{1}{J}u \]

令
\[ x = [ x_1 \qquad x_2 \qquad x_3 \qquad x_4 ]^T \]
将矩阵-向量形式的柔性机械臂系统线性化状态方程
\[ \dot{x} = \begin{bmatrix}
0 & 1 & 0 & 0 \\
-\frac{Mgl + kI}{I} & 0 & k & 0 \\
0 & 0 & 1 & x \\
\frac{k}{J} & 0 & -\frac{k}{J} & 0
\end{bmatrix} \begin{bmatrix} 
0 \\ 
0 \\
u \\
\frac{1}{J}v
\end{bmatrix} \]

### 9-37 设磁悬浮试验系统如图9-49所示。在该系统上方装有一个电磁铁，产生电磁吸引力 \(F\)，以便将铁球悬浮于空中。系统的下方装有一个间隙测量传感器，以测量铁球的悬浮间隙。由于没有引入反馈，该磁悬浮试验系统不能稳定工作。

假若电磁铁电感为 \(L = 0.508H\)，电抗 \(R = 23.2 \Omega\)，电流为 \(I_1 = I_0 + i\)，其中 \(I_0 = 1.06A\)是系统的标称工作电流。再假定铁球的质量 \(m = 1.75kg\)，铁球悬浮间隙 \(\mu_k = X_0 + x\)，其中 \(X_0 = 4.36mm\)为标称磁悬浮间隙。若电磁吸力满足如下条件：
\[ F = k(i/\mu_k)^2 \]

其中\(k = 2.9 \times 10^{-4} kg \cdot m^2 / A^2\)。选择\(x_1 = x, x_2 = \frac{dx}{dt}, x_3 = i\)为状态变量，试用F的泰勒展开式，列写磁悬浮试验系统

\[ x = [ x_1 \qquad x_2 \qquad x_3 \qquad i ]^T \]

系统的线性化状态空间表达式。

### 解 本题应从力平衡方程和电平衡方程入手。

#### 选择状态变量

\[ x_1 = x, \quad x_2 = \dot{x}, \quad x_3 = i \]

故有
\[ \dot{x_1} = x_2, \quad \dot{x_2} = \dot{x}, \quad x_3 = \frac{di}{dt} \]

### Page 187

.entitytype state>text 一方�人 方�人 方�人 Table(--cal 方�人 方�人 方�人 T abcResults 方�人 S++h11 方�人 T V--ch123 方�人 T V--ch123 方�人 T V--ch123 方�人 T abcResults V--ch123 方�人 方�人 方�人 a 3-runj+ht:obj:07 方�人 方�人 方�人 abab 方�人 方�人 方�人 abab T abcResults 方�人 方�人 T abcResults 方�人 kreusewwwwwwwwwvvwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww T abcResults abcresults:.jl i4- 2f"56 m- n an b-'' 500O!!!!!!! 0对齐 T abcResults abcresults 方�人 方�人 方�人 //www.alltechsiz.impl- .---表格 1 1 2345 & 30/31/0 1/20/1cmsb 1/30/31/2012/102202025.,

### Page 188

.</p>

页码: 349 | 397

:

* 9-39 设汽车悬架系统如图 9-51 所示, 其中 $X_1(s), X_2(s)$ 和 $X_3(s)$ 为状态变量, $K_1, K_2$ 和 $K_3$ 为状态反馈系数, 已知 $K_1 = 1$。试确定 $K_2$ 和 $K_3$ 的合适取值, 使闭环系统的三个特征根位于 $s = -3$ 和 $s = -6$ 之间。另外, 还要求确定前置增益 $K_p$ 值, 使系统对阶跃输入的心态误差为零。
  12

**图 9-51 汽车悬架系统结构图**

解 本题可按如下三步求解。
(1) 求闭环传递函数。由梅森增益公式

$$
\Phi(s) = \frac{p_1 \Delta_1}{\Delta}
$$

其中

$$
p_1 = \frac{2K_p}{(s+2)(s+3)(s+4)} \quad \Delta = 1 + \frac{2K_3}{s+4} + \frac{2K_2}{(s+2)(s+4)} + \frac{2K_1}{(s+2)(s+3)(s+4)}
$$

$$
\Delta_1 = 1 
$$

综上, 由于 $K_1 = 1$, 故可得

$$
\Phi(s) = \frac{2K_p}{s^3 + (9+2K_3)s^2 + (26+2K_2 + 10K_3)s + (26 + 6K_2 + 12K_3)}
$$

(2) 确定 $K_2$ 与 $K_3$ 的取值。闭环特征方程

$$
s^3 + (9+2K_3)s^2 + (26+2K_2 + 10K_3)s + (26 + 6K_2 + 12K_3) = 0
$$

由于 $K_2$ 与 $K_3$ 的选取应保证闭环系统稳定, 故由劳斯表

$$
\begin{array}{c c c c c}
 &  & s^3 & \sin(3x) &  \\
 &  & s^3 & \sin(3x) &  \\
 &  & s^2 & \sin(2x) &  \\
 &  & s^2 & \sin(2x) &  \\
 &  &  & \sin(2x) &  \\
 &  &  & \sin(2x) &  \\
 &  &  &  & \sin(3x),\sin(1+2x),\sin(3+2x) \\
\end{array}

$$

可知, $K_2 \geq 0$ 及 $K_3 \geq 0$ 可以确保闭环系统稳定。

若选 $K_2 = 5, K_3 = 2$
则闭环特征方程为

$$
s^3 + 13s^2 + 56s + 80 = 0
$$

其特征根 $s_1 = s_2 = -4, s_3 = -5$。表明特征根 $s \in [-3, -6]$, 满足设计要求。
(3) 求取前置增益 $K_p$ 值。在单位阶跃输入作用下, 若有 $\Phi(0) = 1$, 收有 $e_s(\infty) = 0$。因$

页码: 349 | 397

### Page 189

681517

 )、 m 程序: e x e 939. c n

目录 | 图中所有图例 

】

中文文档

】 __20_

The end of this page.


**gif]

end:

image**
■gif]
```
 *gif]
*___･･･|
```

**\|

*[|
}
```

\|
}

解

\[x_{g} + s + 8\] box-font background :

[ \fASAg 8h_1t_ftggnblgg \]

图 9-39 1 汽车悬架系统时间响应 (MATLAB)

![
Ok\n\n
?3\) g\_ON
Okay []\aOW SIGWAAA \\nfwef 北nOna E VOgE"
はメгре ItoaSadoraWoly DcInO-WaSreame3 a
R d ganommoete w ro, WZ o 3 op不能被 W 汉 
Sd.x3g)+(Z).WZSOzZNoZogF ///Wo SAMWONANAR//ChoN aoLoo8.,MMpet.

Lo.o

4XNXwxA pitch A12(O+jency1,NW -.

\c”.
2142 Vxhz "osaic\y-45 wON0m0ZYC0X.Wk
LXuses.
σο633ZXZw P

walANCATL

9 EXg.
iX - Hmod4x

axionodw. innamwspi ponandewrix Ua raew\SWXw &, w a ay

locowpnaxo. -ii n

1ow j.
·q CWW?
¿}

>\ $3]

\ piece

234G.5

\NR
加
W a ..

AX .j +
qt      


ℓgsl

图 9-52 游船摇摆控制系统

解 本题的求解关键是确定系统在扰动作用下的闭环传递函数,以采用梅森增益公式比较简便.\\

（1） 求扰动作用下的闭环传递函数. 由梅森增益公式

### Page 190

.式中 \( p_1 = \frac{2}{s(s+2)} \), \( L_1 = -\frac{60K_3}{s+8} \)

\( L_2 = \frac{120K_2}{(s+2)(s+8)} \), \( L_3 = -\frac{120}{s(s+2)(s+8)} \)

\( \Delta = 1 - (L_1 + L_2 + L_3) = 1 + \frac{60K_3}{s+8} + \frac{\frac{120}{2}(K_2 + K_3)}{(s+2)(s+8)} + \frac{120}{s(s+2)(s+8)} \)

\( \Delta_1 = 1 - L_1 = 1 + \frac{60K_3}{s+8} \)

因此 \( \Phi_n(s) = \frac{2(s+8+60K_3)}{s^3 + 10(1+6K_3)s^2 + [16+120(K_2 + K_3)]s + 120} \)

(2) 确定 \( K_2 \) 与 \( K_3 \) 的取值。系统实际特征方程

\( s^3 + 10(1+6K_3)s^2 + [16+120(K_2 + K_3)]s + 120 = 0 \)

希望特征方程

\( (s+2+j2)(s+2-j2)(s+15) = s^3 + 19s^2 + 68s + 120 = 0 \)

令特征方程的对应项系数相等，有

\( 10 + 60K_3 = 19 \)

\( 16 + 120(K_2 + K_3) = 68 \)

解出 \( K_2 = 0.283 \)，\( K_3 = 0.15 \)

(3) 绘单位阶跃扰动响应曲线。令 \( N(s) = \frac{1}{s} \), 得阶附加横泡幅输出

\( \Phi_n(s) = \Phi_n(s)N(s) = \frac{2s + 34}{s(s + 15)(s^2 + 4s + 8)} \)

\( = \frac{0.283}{s} \frac{0.002}{s + 15} \frac{0.281(s + 4.1)}{(s + 2)^2 + 2^2} \)

对上式进行拉氏反变换，得横泡幅扰动输出

\( \theta_n(t) = 0.283 - 0.002e^{-15t} - 0.407e^{-2t}\sin{(2t + 4.6)^2} \)

MATLAB验证：

应用 MATLAB 软件包，运行 M 文件 exe940.m，作阶罐的单位阶跃扰动横泡幅响应曲线，如图 9-40-1 所示。

MATLAB 程序：exe940.m

clc;clear

K2 = 0.283;K3 = 0.15;

num = 2 * [1.8 + 60 * K3];

den = [1 10 + 60 * K3 16 + 120 * (K2 + K3)]

120];

sysn = tf(num,den);

t = 0.01:0.4;

step(sysn,t);grid

图 9-40-1 游船单位阶跃扰动横泡幅响应 (MATLAB)

• 346 •

### Page 191

.img

\[ 9-41 \] 设内模控制系统如图9-53所示，试设计合适的内模控制器 \[ G_{\varepsilon}(s) \] 和状态反馈增益向量 \[ k_{2} \]，使系统闭环极点 \[ s_{1}=s_{2}=s_{3}=-2 \]，且对阶跃输入稳态误差为零，最后给出系统的单位阶跃响应曲线。

\( \theta_n(t) = 0.283 - 0.002e^{-15t} - 0.407e^{-2t}\sin{(2t + 4.6)^2} \)

MATLAB验证：

应用 MATLAB 软件包，运行 M 文件 exe940.m，作阶罐的单位阶跃扰动横泡幅响应曲线，如图 9-40-1 所示。

MATLAB 程序：exe940.m

clc;clear

K2 = 0.283;K3 = 0.15;

num = 2 * [1.8 + 60 * K3];

den = [1 10 + 60 * K3 16 + 120 * (K2 + K3)]

120];

sysn = tf(num,den);

t = 0.01:0.4;

step(sysn,t);grid

图 9-40-1 游船单位阶跃扰动横泡幅响应 (MATLAB)

• 346 •

### Page 191

.img

\[ 9-41 \] 设内模控制系统如图9-53所示，试设计合适的内模控制器 \[ G_{\varepsilon}(s) \] 和状态反馈增益向量 \[ k_{2} \]，使系统闭环极点 \[ s_{1}=s_{2}=s_{3}=-2 \]，且对阶跃输入稳态误差为零，最后给出系统的单位阶跃响应曲线。

建立内模控制系统结构图

解 本题按如下步骤设计。(1) 建立被控对象的动态方程。 \[ G_{0}(s) = \frac{1}{(s+1)(s+2)} = \frac{1}{s^{2} + 3s + 2} \] 令 \[ x = [x_{1} \quad x_{2}]^{T} \]，其中 \[ x_{1}=y \]，则被控对象的可控标准型为 \[ \dot{x} = Ax + bu, \quad y = cx \] 式中 \[ A = [ \begin{matrix} 0 & 1 \\ -2 & -3 \end{matrix} ], \quad b = [ \begin{matrix} 0 \\ 1 \end{matrix} ], \quad c = [ \begin{matrix} 1 & 0 \end{matrix} ] \] (2) 构造增广系统。定义跟踪误差 \[ e(t) = r(t) - y(t) \] 因 \[ r(t)=1(t) \] 有 \[ \dot{e}(t) = -\dot{y}(t) = -cx(t) \] 令 \[ z(t) = \dot{x}(t), \quad w(t) = \dot{u}(t) \] ，构造 \[ \begin{bmatrix} \dot{e}(t) \\ \dot{z}(t) \end{bmatrix} = \begin{bmatrix} 0 & -c \\ 0 & A \end{bmatrix} \begin{bmatrix} e(t) \\ z(t) \end{bmatrix} + \begin{bmatrix} 0 \\ b \end{bmatrix} w(t) \] 即 \[ \begin{bmatrix} \dot{e} \\ \dot{z} \end{bmatrix} = \begin{bmatrix} 0 & -1 & 0 \\ 0 & 0 & 1 \\ 0 & -2 & -3 \end{bmatrix} \begin{bmatrix} e \\ z \\ w \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} w \]

在上述增广系统方程中 \[ A = \begin{bmatrix} 0 & -1 & 0 \\ 0 & 0 & 1 \\ 0 & -2 & -3 \end{bmatrix}, \quad \bar{b} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} \] (3) 检验增广系统的可控性。由于 \[ \text{rank} \begin{bmatrix} 0 & -cb \\ b & Ab \end{bmatrix} = \text{rank} \begin{bmatrix} 0 & 0 & -1 \\ 0 & 1 & -3 \\ 1 & -3 & 7 \end{bmatrix} = 3 \] 表明增广系统可控，可以任意配置闭环系统极点。

### Page 192

.\[(4) 确定内模控制律。令 \ k_2=[k_2 \ \ k_3] ,\ k=[k_1 \ \ k_2 \ \ k_3] ,G_c(s)=\dfrac{k_1}{s} , 则控制律\]
\[u(t)=-k_1 \int_{0}^{t}e(\tau)d\tau-k_2 x_1 -k_3 x_2\]
其中 \(k_1 , k_2 \) 和 \(k_3 \) 可按希望闭环极点位置确定。
由题意，希望闭环特征方程
\[(s + 2)^3 = s^3 + 6s^2 + 12s +8=0\]
实际闭环特征方程为
\[det(sI - A + bk )=0\]
因为
\[sI-A+ bk =\begin{bmatrix} s & 1 & 0\\ 0 & s & -1\\ k_1 & 2+k_2 & s + 3 + k_3 \end{bmatrix} \]
所以
\[det (sI-A+ bk ) = s^3 +(3+ k_2 )s^2 +(2+k_2 )s - k_1 =0 \]
比较希望特征方程与实际特征方程， 可得
\[k_1 = -8,\ \ k_2 =10,\ \ k_3 =3\]
内模控制律
\[u(t) = 8\int_{0}^{t}e(\tau)d\tau - 10x_1 -3x_2\]
内模控制系统如图9-41-1所示。
(5) 绘内模控制系统单位阶跃响应。应用 MATLAB 软件包， 并根据图9-41-1在Simulink环境下搭建内模控制系统， 运行可得系统单位阶跃响应如图9-41-2 所示，测得
\(t^0=0, t_s = 7.75s(\Delta = 2 \%) , e_s(\infty) = 0 \)
图 9-41-1  单位阶跃内模控制系统结构图    图 9-41-2  内模控制系统的单位阶跃响应(MATLAB)
9-42  设单位斜坡内模控制系统如图 9-54 所示， 其中被控对象
\[G_o(s)=\dfrac{1}{(s+1)(s+2)} \]
\( x_1 (t ) \) 和 \( x_2 (t) \) 为状态变量。 试设计合适的内模控制器
\[G_c(s) = \dfrac{k_1+ k_2s}{s^2} \]
\quad 348

### Page 193

represented by equation:

那么根据加下步骤求解。

(1) 建立被控对象的动态方程。 

\[G_0(s) = \frac{1}{s^2 + 3s + 2}\]  

其中可控标准型为 

\[x = Ax + bu, \quad y = cx\]  

式中 

\[A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}, \quad b = \begin{bmatrix} 0 \\ 1 \end{bmatrix}, \quad c = \begin{bmatrix} 1 & 0 \end{bmatrix}\]  

(2) 构造增广系统。令 

\[e_0(t) = e_y(t) - y(t), \quad r_0(t) = t\]  
\[e_r^0 = \dot{e}_r(t) - \dot{y}(t) = 1 - cx^2(t)\]  
\[e_{r_0} = -\dot{y}(t) = -c \dot{x}(t)\]

令中间变量 

\[z_0(t) = \dot{x}(t), \quad w_0(t) = \dot{u}(t)\]  
得 
\[z_0(t) = A \dot{x}(t) + b \dot{u}(t)\]  
\[z_0(t) = A \dot{x}(t) + b \dot{u}(t) = A z(t) + bw(t)\]  
\[e^r_0(t) = - c (z(t))\]

构造增广系统 

\[\begin{bmatrix}  
\dot{e}(t) \\  
\dot{e}^r(t) \\  
\dot{z}_0(t)  
\end{bmatrix} 
=  
\begin{bmatrix}  
0& 1 & 0 \\  
0 & 0 & -c \\  
0 & 0 & A  
\end{bmatrix} 
\begin{bmatrix}  
e(t) \\  
\dot{e}(t) \\  
z(t)  
\end{bmatrix} 
+  
\begin{bmatrix}  
0 \\  
0 \\  
b  
\end{bmatrix} 
w(t)\] 

即 

\[\begin{bmatrix}  
\dot{e}(t) \\  
\dot{e}^1(t) \\  
\dot{e}^2(t) \\  
\dot{e}^3(t)  
\end{bmatrix} 
=  
\begin{bmatrix}  
0 & 1 & 0 \\  
0 & 0 & -1 \\  
0 & 0 & 0 \\  
0 & 0 & -2  
\end{bmatrix} 
\begin{bmatrix}  
e(t) \\  
\dot{e}^1(t) \\  
z_1(t) \\  
z_2(t)  
\end{bmatrix} 
+  
\begin{bmatrix}  
0 \\  
0 \\  
0 \\  
1  
\end{bmatrix} 
w(t)\]  

\[A =  
\begin{bmatrix}  
0 & 1 & 0 & 0 \\  
0 & 0 & -1 & 0 \\  
0 & 0 & 0 & 1 \\  
0 & 0 & -2 & -3  
\end{bmatrix} 
, \quad \dot{b} =  
\begin{bmatrix}  
0 \\  
0 \\  
0 \\  
1  
\end{bmatrix}\]  

式中 

\[\begin{bmatrix}  
0 \\  
0 \\  
0 \\  
1  
\end{bmatrix}  
w(t)\] 

\[A =  
\begin{bmatrix} -1 & 3 \\ 0 & 3 \\ 0 & 0 \\ 1 & -2 \end{bmatrix}\]

### Page 194

input/output interface and data migration mechanism, given the specific needs and purpose. () can be the rectype variable. gete 机 P = \( c b - c A b \quad \text{if} \quad rank \) 为: [] = \( a B - c A b \quad \text{if} \quad b = \text{rank} \quad cost = \(|((b)\) \) ( ) assume that P can be transmission, and the transfer of the control. ( )25 can be limited. medium. ( ) f as a source. ( )is possible to complete this action. The limit control has a positive system. Adding.

### Page 195

.\[ \dot{e} = \dot{r} - \dot{y} = 1 - c\frac{x}{\sqrt{c}}, \quad \dot{e} = \dot{c}x \]

令中间变量

\[ \dot{z} = \dot{x}, \quad z = \dot{x}F \quad \text{quasi-to} \quad \dot{e} = \dot{c} \]

\[ x = F^{2} \lambda t + b u, \quad z = \lambda t + b w \]

得增广系统

\[ \left[ \begin{matrix} \dot{e} \\ \dot{r} \\ \dot{z} \end{matrix} \right] = \left[ \begin{matrix} 0 & 1 & 0 & 0 \\ 0 & 0 & c & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & -2 & -2 \end{matrix} \right] \left[ \begin{matrix} e \\ t \\ \lambda t \\ f(t) \end{matrix} \right] + \left[ \begin{matrix} 0 \\ 0 \\ 0 \\ 2 \end{matrix} \right] w \]

或者

\[ \left[ \begin{matrix} \dot{e} \\ \dot{r} \\ \dot{z} \end{matrix} \right] = F \left[ \begin{matrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 0 & -2 \\ 0 & 0 & -2 \\ 0 & 0 & 2 \end{matrix} \right] \left[ \begin{matrix} e \\ t \\ \lambda t \\ \lambda(t) \end{matrix} \right] + \left[ \begin{matrix} 0 \\ 0 \\ 0 \\ 1 \\ 0 \\ 0 \\ 1 \end{matrix} \right] w \]

其中

\[ \dot{A} = \left[ \begin{matrix} 0 & 1 & 0 & 0 \\ 0 & 1 & 0 & 1 \\ 0 & 1 & 0 & 2 \\ 0 & 0 & -3 & -2 \end{matrix} \right], \quad \dot{b} = \left[ \begin{matrix} 0 \\ 1 \\ -2 \end{matrix} \right] w \]

（2）检验增广系统的可控性。

\[ \text{rank} \left[ \begin{matrix} 0 & 0 & -bc & -cAb \\ 0 & -cb & -cAb & -cA^{2}b \\ Ab & Ab \\ \end{matrix} \right] = \text{rank} \left[ \begin{matrix} 0 & 1 & -2 \\ 1 & 2 & 6 \\ 1 & 2 & 6 \\ 2 & 6 & 8 \end{matrix} \right] = 4 \]

故增广系统可控，可任意配置闭环系统极点。

（3）确定内模控制律。令 \(\dot{x} = [k_1 \quad k_2 \quad k_3 \quad k_4]\)，闭环特征方程

\[ \text{det} \left[ sI - (\bar{A} - \bar{b} k) \right] = \det \left[ \begin{matrix} s & -1 & 0 & 0 \\ 0 & s & 1 & 0 \\ k_1 & k_2 & s+k_3 & k_4 \\ 2k_1 & 2k_2 & 2+2k_3 & 3+s+2k_4 \end{matrix} \right] = s^4 + (2 + k_3 + 2k_4)s^3 + (2 - k_2 + 4k_3 - 2k_4)s^2 - (k_1 + 4k_2)s - 4k_1 = 0 \]

希望特征方程

\[ (s + 1 + j)(s + 1 - j)(s + 10)^2 = s^4 + 22s^3 + 142s^2 + 240s + 200 = 0 \]

令实际特征方程与希望特征方程的对应项系数相等，得到

\[ 2 + k_3 + 2k_4 = 22 \]
\[ 2 - k_2 + 4k_3 - 2k_4 = 142 \]
\[ k_1 + 4k_2 = -240 \]
\[ 4k_1 = -200 \]

解出

\[ k_1 = -50, \quad k_2 = -47.5 \]
\[ k_3 = 22.5, \quad k_4 = -1.25 \]

求出内模控制律

351

### Page 196

represents the second layer of a convolutional neural network. The convolution is performed by a matrix multiplication operation, with the kernel as the filter. The inner product between the feature map and the kernel is sum of all imput paralleled by the location. Here we have a Gaussian kernel of the form. In statistical modeling, the exponential family of distributions is often adopted. In neural networks, there is usually a non-linearity like $\sigma(x)$, which corresponds to inner product with the linear $\alpha(x)$. So we are going to use the same inner product sum over vertical paralleled limits which correspond to a linear inner product.



## Page 357/397, Extract all text exactly.

$u(t) = 50\int_{0}^{t}\int_{0}^{t}e(\tau)d\tau dt + 47.5\int_{0}^{t}e(\tau)d\tau - 22.5x_{1}(t) + 1.25x_{2}(t)$

单位斜坡内核控制系统如图9-43-1所示。

图 9-43-1  单位斜坡内核控制系统结构图

应用MATLAB软件包,并根据图9-43-1在Simaglink环境下搭建内核控制系统,运行可得内核控制系统的单位斜坡误差响应,如图9-43-2所示。

图 9-43-2  系统单位斜坡跟踪误差响应曲线(Simaglink)

9-44 设带有扰动$n(t)$的单输入-单输出系统的状态空间表达式为
\[\dot{x}(t) = A x(t) + b u(t), \quad y(t) = c x(t) + m(t)\]
其中,$x \in R^{n}$为状态向量, $u$为标准量输入, $y$为标准量输出, $A,b,c$维数适当。

设参考输入$r(t) = t$,扰动信号$n(t) = 1(t)$,为阶跃干扰。试论证可设计内模控制器,使系统输出能以零稳态误差渐近跟踪斜坡输入$t$,且不受阶跃扰动$n(t)$的影响。

解 由题设知$\dot{r}(t) = 0, \dot{n}(t) = 0$；定义跟踪误差
$$
e(t) = r(t) - y(t) = r(t)  - cx(t) - m(t)
$$ 对式$(1)$取二阶导数,有
$$
\dot{e}(t) = \dot{r}'(t) - \dot{y}'(t) = -c \dot{x}'(t)
$$
在式$(2)$中,取中间变量 $z(t) = \dot{x}(t), w(t) = \dot{u}(t)$，并对$z(t)$取一阶导数,有
$$
z'(t) = \dot{x}'(t) = A \dot{x}(t) + b \dot{u}(t) = A z(t) + b w(t)
$$
从而
$$
\dot{e}(t) = \dot{r}'(t) - \dot{y}'(t) = -c \dot{x}'(t) = -c z(t)
$$
由式$(3)$和式$(4)$构造增广系统

### Page 197

~~大楼小~~

L\`让人们更好吧。你可以尝试用特殊的语气表达，让别人更了解你对生活的高度和追求。你如果是在做事上有特别的建议去说，或者肯定某事情让你的生活变得更加不错，这个时候会展现本书中传递的价值观。尝试用这种特殊的语言表达自己的想法，别跟别人聊天。人们喜欢别人的处理态度，就算有“独特”的感受，或者说说当时心情。过程中你会发现参与还有一些乐趣。L\`：大家都认为语言的不同 can 带来了互相理解。L\`：L\`：我们存入一个世界上不应该存在的 Swarmle 。

~~5\]

L\`：L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\`L\\`L\`L\`L\`L\\`L\`L\`L\`L\`L\\`L\`L\`L\`L\\`L\`L\`L\\`L\`L\\`L\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\`L\\`L\\`L\\`L\`L\`L\\`L\`L\`L\\`L\`L\\`L\`L\\`L\\`L\`L\\`L\\`L\`L\\`L\`L\\`L\\`L\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\`L\\`L\\`L\\`L\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L\\`L \\~L\`\]表中的数据均具有唯一性和确定性，这样数据之间的对应关系具有可靠的安全性，可以在设计中应用。  

H\`  

W\`根据上式，取中间变量 \(w(t) = u^{(3)}(t)\)，有  

\[\begin{align*} z(t) &= x^{(4)}(t) = Ax^{(3)}(t) + bu^{(3)}(t) = Az(t) + bw(t) & (2) \end{align*} \]  

s\`  

u\<3)(t) = Ax<S(3)(t) + bu<3)(t) = Az<3) + bw(4)(t)-(3)  

B\`  

组合  

\[L = (y^{(3)}(t) + w^{(3)}(t) - ax^{(3)}(t)) \end{align*} \]  

(e3); w; (3)(t) y.  

由式(3)和式(4)构造增广系统为\[ \begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{w} \\ z \end{bmatrix} = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & -c \\ 0 & 0 & 0 & A \end{bmatrix} \begin{bmatrix} e \\ \dot{e} \\ \dot{w} \\ z \end{bmatrix} + \begin{bmatrix} 0 \\ 0 \\ 0 \\ b \end{bmatrix} w \]  

\[ \quad (5) \]  

 dels123561

### Page 198

approximating when \(t\).

信 息 请 检查 

J = (o + u*) dt = min

(2)如果使系统转移到 x( t f)=0 的终端时间 tm自由，问 u*(t)应如何确定？
解 (1) t f 固定,末端固定,可采用变分法求解。令

\[ H=1+u^2+λ(-x+u) \]

协态方程

\[ \dotλ = -\frac{\partial H}{\partial x} = λ， λ = c_1 e^{\prime} \]

极值条件

\[ \frac{\partial H}{\partial u} = 2u + λ = 0， \frac{\partial^2 H}{\partial u^2} = 2 > 0，u^{*} = -\frac{1}{2} c_1 e^{\prime} \]

状态方程

\[ \dotx = -x+u， x = c_2 e^{+ − \frac{1}{4}}c_1 e^{\prime} \]

由初始条件x(0)=3和边界条件x(2)=0，求出

\[ c_1 = \frac{12}{e^4 - 1}， c_2 = \frac{3e^4}{e^4 - 1} \]

则最优控制为

\[ u^*(t) = -\frac{6e^t}{e^4 - 1} =-0.1119e^t \]

(2)t f 自由,末端固定,控制无约束,可同问题(1)采用变分法求解,并采用同样的协态方程、极值条件和状态方程。

根据初态x(0)=3,未态x( t f)=0 及H变化律H( t f)=-\frac{\partial ϕ}{\partial t f} =0,求出

\[ c_1 = 0.3246，tf = 1.818 \]

则最优控制为

\[ u^*(t)=-0.1623e^t \]

10-12 设系统状态方程及初始条件为

\[ \dotx(t) =u(t)， x(0)=1 \]

试确定最优控制 u*(t),使性能指标

\[ J = t f + \frac{1}{2} \left( \int_{0}^{t f} u^2 dt \right) \]

为极小，其中终端时间 t f 未定,x( t f)=0.

解题 本题 t f 自由,未端固定,控制无约束,可采用变分法求解。

由题意,φ(t f)=t f,令

\[ H=\frac{1}{2}u^2 +λu \]

协态方程

\[ \dotλ = -\frac{\partial H}{\partial x} = 0， λ = c_1 \]

极值条件

### Page 199

model (1-1) at (0,0) [dashed] ; chart const 0a1 (1,3). edge left
状态方程。由 $\dot{x}=u$, $x=-c_{1}t+c_{2}$:
可得 \(\frac{\partial H}{\partial u}=u=\lambda\)，得 \(\frac{\partial^{2}H}{\partial u^{2}}=-\lambda\) 和 \(u^{*}=-\lambda=c_{1}\)。
于是最优控制为
$u^{*}(t) = -\sqrt{2}\)

\[ H(t_{f}) = -\frac{\partial \phi}{\partial t_{f}} = -1 \]

10-13 设二次积分模型为
\[\dot{\theta}(t) = \omega(t), \quad \dot{\omega}(t) = u(t)\]

性能指标为
\[J = \frac{1}{2} \int _{0}^{1} u^{2} dt\]

已知 $\theta(0)=\omega(0) =1, \theta(1)=0, \omega(1)$ 自由, 试求最优控制 $u^{*}(t)$ 和最优轨线 $ \theta^{*}(t), \omega^{*}(t)$。

解：本题 $ t_{f}$ 固定, 部分未态固定, 部分未态自由. 控制无约束, 可采用变分法求解。

令哈密顿函数
\[ H = \frac{1}{2} u^{2} + \lambda_{1} \omega + \lambda_{2} u \]

协态方程
\[\dot{\lambda} = -\frac{\partial H}{\partial \theta} = 0, \quad \dot{\lambda}_{1} = c_{1}, \quad \dot{\lambda}_{2} = -\frac{\partial H}{\partial \omega} = - \lambda_{1}, \quad \lambda_{2} = -c_{1}t + c_{2}\]
极值条件
\[\frac{\partial H}{\partial u} = u + \lambda_{2} = 0, \quad \frac{\partial^{2} H}{\partial u^{2}} = 1 > 0, \quad u^{*} = -\lambda_{2} = c_{1}t -c_{2}\]
状态方程
\[\dot{\omega} = u, \quad \omega = \frac{1}{2} c_{1}t^{2} - c_{2}t + c_{3}\]
\[\dot{\theta} = \omega, \quad \theta = \frac{1}{6} c_{1}t^{3} - \frac{1}{2} c_{2}t^{2} + c_{3}t + c_{4}\]
由初始条件 $\theta(0)=\omega(0)=1$, 求出
\(c_{3}=c_{1}-1\)
由未态条件 $\theta(1)=0$ 及 $H$ 变化律$λ_{2}(1) = -\frac{\partial \phi}{\partial t_{f}} = 0$, 求出
 \(c_{1}=c_{2}=6\)
故得
最优控制 $u^{*}(t)=6(t-1)$

\[\cdot 364 \cdot\]

### Page 200

.最优化线 \[ \theta^*(t) = t^3 - 3t^2 + t + 1 \]， \[ \omega^*(t) = 3t^2 - 6t + 1 \] 10-14 设系统状态方程及初始条件为 \[\dot{x}_1(t) = x_2(t), \quad x_1(0) = 2\] \[\dot{x}_2(t) = u(t), \quad x_2(0) = 1\] 性能指标为 \[J = \frac{1}{2} \int_0^{t_f} u^2 dt\] 要求达到 \(x(t_f) = 0\)，试求：（1） \(t_f = 5\) 时的最优控制 \(u^*(t)\)；（2） \(t_f\) 自由时的最优控制 \(u^*(t)\)。 解 （1）本题为 \(t_f = 5\) 固定，末端固定，控制无约束的最优控制问题。令 \[ H = \frac{1}{2} u^2 + \lambda_1 x_2 + \lambda_2 u \] 协态方程 \[\dot{\lambda}_1 = -\frac{\partial H}{\partial x_1} = 0, \quad \dot{\lambda}_1 = c_1\] \[\dot{\lambda}_2 = -\frac{\partial H}{\partial x_2} = -\lambda_1, \quad \dot{\lambda}_2 = -c_1 t + c_2\] 极值条件 \[\frac{\partial H}{\partial u} = u + \lambda_2 = 0, \quad \frac{\partial^2 H}{\partial u^2} = 1 > 0, \quad u^* = -\lambda_2 = c_1 t - c_2\] 状态方程 \[\dot{x}_2 = u = c_1 t - c_2, \quad x_2 = \frac{1}{2} c_1 t^2 - c_2 t + c_3\] \[\dot{x}_1 = x_2, \quad x_1 = \frac{1}{6} c_1 t^3 - \frac{1}{2} c_2 t^2 + c_3 t + c_4\] 根据初态及末态条件，求出 \[c_1 = 0.432, \quad c_2 = 1.28, \quad c_3 = 1, \quad c_4 = 2\] 于是最优控制为 \[ u^*(t) = 0.432t - 1.28 \] （2）本题为 \(t_f\) 自由，末端固定，控制无约束的最优解问题，其求解过程（协态方程，极值条件，状态方程）同（1）。 已求得 \[ x_1 = \frac{1}{6} c_1 t^3 - \frac{1}{2} c_2 t^2 + c_3 t + c_4\] \[ x_2 = \frac{1}{2} c_1 t^2 - c_2 t + c_3\] \[ u = c_1 t - c_2\] 根据最优终端时刻 \(H\) 变化律 \(H(t_f) = -\frac{\partial \varphi}{\partial t_f} = 0\)，求出 \(c_1 = \frac{1}{2} c_2^2\)。 可见 \(c_1, c_2\) 与 \(t_f\) 无关，因而此时无最优解 \(u^*(t)\)。

### Page 201

.\).\)\}\)\)\}.\]

\(.\]

题解：如果过程可用循环的方法定义：

如果 \(x(1)=0\)，则 x0，重新定义 \(x_1,x_2,\dotsc,\dotsc\)作为迭代序列的初始值；

如果 \(x(1)<0\)，则 \(x_0\), 重新定义 \(x_1,x_2,\dotsc,e\), 然后根据公式 \(x(n+1)=f(x(n),0)\) 来逐步逼近 \(x^*\): \\

\[y = x - \lambda My + M \frac{\partial_H}{\partial M}\]\]

解本方程组的方法同第八章所求的方程，不过要求条件 \(H(z) = 1,z,u\)的值，如果它与 0，\)类似应当在迭代的过程预先设 \(y=0,数\) ，再解方程组。

\[\left(r \ddot{x}+f(x,0) =0\right),\]\]\]




\[J = \frac{1}{2}\int_{0}^{1}(x^{2} + u^{2})dt \]

已知\( x(1)=0 \)，某工程师认为从工程观点出发可取最优控制函数 \( u^{*}(t)=-1 \)，试分析他的意见是否正确，并说明理由。

解 本题 \( t_{f} \) 固定,末端固定. 令

\[H = L + \lambda^{T}f = \frac{1}{2}(x^{2} + u^{2}) + \lambda u \]

协态方程

\[\dot{\lambda} = -\frac{\partial H}{\partial x} = -x \]

.\).\)\}\)\)\}.\]

\(.\]

题解：如果过程可用循环的方法定义：

如果 \(x(1)=0\)，则 x0，重新定义 \(x_1,x_2,\dotsc,\dotsc\)作为迭代序列的初始值；

如果 \(x(1)<0\)，则 \(x_0\), 重新定义 \(x_1,x_2,\dotsc,e\), 然后根据公式 \(x(n+1)=f(x(n),0)\) 来逐步逼近 \(x^*\): \\

\[y = x - \lambda My + M \frac{\partial_H}{\partial M}\]\]

解本方程组的方法同第八章所求的方程，不过要求条件 \(H(z) = 1,z,u\)的值，如果它与 0，\)类似应当在迭代的过程预先设 \(y=0,数\) ，再解方程组。

\[\left(r \ddot{x}+f(x,0) =0\right),\]\]\]




\[J = \frac{1}{2}\int_{0}^{1}(x^{2} + u^{2})dt \]

已知\( x(1)=0 \)，某工程师认为从工程观点出发可取最优控制函数 \( u^{*}(t)=-1 \)，试分析他的意见是否正确，并说明理由。

解 本题 \( t_{f} \) 固定,末端固定. 令

\[H = L + \lambda^{T}f = \frac{1}{2}(x^{2} + u^{2}) + \lambda u \]

协态方程

\[\dot{\lambda} = -\frac{\partial H}{\partial x} = -x \]

极值条件

\[\frac{\partial H}{\partial u} = u + \lambda = 0 , \quad u = -\lambda \stackrel{\text{由}}{\equiv} \frac{\partial^{2}H}{\partial u^{2}} = 1 > 0 \]

状态方程

\[\dot{x} = u , \quad \dot{x} = \dot{u} = -\dot{\lambda} = x , \quad x = c_{1}e^{t} + c_{2}e^{-t} \]

故有

\[u = c_{1}e^{t} - c_{2}e^{-t} \]

根据边界条件 \( x(0)=1,x(1)=0 \)，求出

\[c_{1} = \frac{1}{1 - e^{2}} , \quad c_{2} = -\frac{e^{2}}{1 - e^{2}} \]

故得

\[\text{最优控制} \quad u^{*}(t) = -0.157(e^{t} + 7.39 e^{-t}) \]

\[\text{最优轨线} \quad x^{*}(t) = -0.157(e^{-t} - 7.39 e^{-t}) \]

\[\text{最优性能指标} \quad J^{*} = 0.66 \]

若取 \( u^{*} = -1 \)，则 \( J^{*} = 0.67 \)。故从工程角度考虑，工程师的意见是正确的。

\[10-16 \quad \text{给定二阶系统} \]

\[\dot{x}_{1}(t) = x_{2}(t) + \frac{1}{4} , \quad x_{1}(0) = -\frac{1}{4} \]

\[\dot{x}_{2}(t) = u(t) , \quad x_{2}(0) = -\frac{1}{4} \]

控制约束为 \( |u(t)| \leq \frac{1}{2} \)，要求最优控制 \( u^{*}(t) \)，使系统在 \( t = t_{f} \) 时转移到 \( x(t_{f})=0 \)，并使

\[J = \int_{0}^{t_{f}}u^{2}(t)dt= \min \]

其中 \( t_{f} \) 自由。

解 本题为定常系统，末端固定，积分型指标 \( t_{f} \) 自由，但是有控制约束的最优控制问题，应采用极小值原理求解。令

\[\dot{H} = u^{2}+\lambda_{1}x_{2} + \frac{1}{4}\lambda_{1} + \lambda_{2}u = \left( u + \frac{1}{2}\lambda_{2} \right)^{2} + \lambda_{1}x_{2} + \frac{1}{4}\lambda_{1} - \frac{1}{4}\lambda^{2}_{2} \]

协态方程

\[\dot{\lambda}_{1} = -\frac{\partial H}{\partial x_{1}} = 0 , \quad \lambda_{1} = c_{1} \]

### Page 202

.\section*{第四节 复分析} 246 解 因为 |u(0)| ≥ 2, |u(0)|2 ≥- \|u\|2B Then, condition 0≤t≤\frac{1}{T}, 在\left|z\right+y|\leq\left|\}.\]

解 数为 D 的、箭侧绕角点 \varepsilon/dt\left=D+h-simp\frac{8}{2}+change_over_{b} (\delta-beta)\right){synth}_{\text {代替}} (02 * 0*1,\times.sup){synth}_{\text {替代}}

地方素数 f1 通过 0d1-d.org/t)*(t)1(t0 

或者通过 0d1-0.1*r^{8}/B

h 

等等

抄
d2r=dt\frac{1}{d}dt-\tau*(\tau{t}) dt,
结束
=d-(\tau{dt)} d=\frac {1}{h-simp a^{2+b/t}} b

\end{document}

也可见适符”结算单位时间运行和“约数公式”公式于《当源

整体观察全书解决 Kamikaze-Roe 公式代6，o 式 变变等分 代数 数 d以及预测 圆 分 школа

群 不含异的子符 非」内变量素 d (规则 代 两 定理） 环量代 (标子式 分解) 数 简a 

多分析 和 使 释 生 b\个别 命题 b 结 统 s|n(a1\成 解 宏明(in 多扖(mI

）于允许 (-...

” 

化至外环圆环:东总：n 程为(b

因为 此 \frac{8}{2}}= 0 （不合题意

子分  \frac{d}{dt}

同结 

Ultimate 者 不在除 (然后“论)

精于

分道出单项分子 \frac{8}{2}

居 a步数(b)

黄码 \[（分介绍 a限)/数] \(d)

意出

对数 或分 系带编辑器 和 

庄{ 证明 }
关系式 ) 之比提单位是a 各反应 (题等)

分n, 分 interrovinaa中

及混合根伯.终数特长(端标件. \(解)

解析 分象
分解有

}易 数

Lewis高者 侧环比正性, 之 b分；

lacn因 特 系 及 b(1'-4)

吕等

为

a分也无

科研者 断试分( 结证
上述a 总与r，分部分范围公式
可实数和分最等,其及分地,而

u 分核一般 b数；

分a源，可

数.较与分与

内分a 
公式可以排上(a (同分)

a 和(a)必标底a。

设

分.存在
较小 于

a,

分 绍

分

期子 d

分

分 22 
下 U数分 免

=,=a=分待 是 b,0 }

 分分a

分

 准配

等轮 无即,分显b 则式
 满足

传来a 分些 系统 系.e 可行号 常放算 

[制, 发生

期 数

} ,高 验解

经 \frac{2|2】}定 再特征 下 es

p (使用基础方子 (-近

负系 的(- 负一部分,义

短路较
分

，′=交 a数

 يس

例分

无 的标

°, 

各术f

b b系.

a

为 分

U(a,理分 因素

分} 分

址全程有

, 达合 
a

 盘习
文体

的分分

此

(2分 % 

单=格等比()系分法可

作

a \\ 

” 数称 (条

 有.e %
约束 等 (\分 推

 分。

,则 领域（条 I

数(,.分

,分 扰（复  \)

区 分 z

求项) 防引 e 系 面 分0 
 
(b 系式(s)plin按照代

所分其".理数的推 定,...}

于

a数

上 不 \]

 分此\cya

因数式系

分由
及式

 {条 你:

指标 数标(ex计算 分正 b.下法

(；
分且?-统

子按度分a

面分(-) 方 分\

,调球分x

[.赤分

等备

式), (
上估算\

带条矩分(，系 n 上, 例如

(·问}
分(, 映(

 ）]  (方)数 系xF同\负系(平; 素,

;
结) 注 
,系 数0

式优 分

分

的适适适 方 包含 s寻找 幅系极 性(符 (鱼的  数

¥包(度  正 系

含 (其适适填的

 α(式(2

,符为 系综%。

数 以 b

系
y仅

率系统 
为 待适 系(式) 选

分;(. 界 a 实系\ s

 */

展 于其 (条且适分,

.定常2

b 系统 提高
(系

收、系 ',

第(0;

   
分式。

  [ 
为 系n 系
 时

.
/

定选.二者因分图

.设定定 分法)
,分对 其. 间(式

 

  !}\\）

.

 当a负

系

 .

  【
 

  分=  适

为

 方程)(式索 数\定适 可. 
 实

 用者}条
.

 即应

(\
(a系
u,定适,原 系度(导} 
,适 可.;\定符\\数 n数.定.的,适适 (分便 数适. 系

适编编 条乙
, ，通过 法原式适

,分.)

正 系. 

 . 

系

 .”\(

   0b为

(解 

  )
   

  ;

  } 条和 分

.a 

式 括 式

选择.

}

正对于 特星系(←条正,迭代实

数)

,

 正性  无适 取定.

适系 [

适正分;

系分,与适适a标

一,的符 方适,

适,系统适话é

条数定条理

正

适适临题

适

st适

s收适适定符)

适定与适适,a同&系s;

适系

适

选适适适适适适

条适正括

适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适適适適适適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適適適適适適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適适適适適適適适適適適適適適適適適適適適適適適适適適適适適适適適適適適適适適適適適適适适适適适适适適适適适適適適适適適適適適適適適适適適適適适適適適適適適適適適適適適適適適適適適適適適適適適适適適適適适適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適適適适適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適適适適適适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适适

 且则 (\负.

即,系

 入 称系等

 系按
其 
系系 标及)

 b问

 分标系 k式 系设a

 变系)
 定

;造性用
 用确

 分类性,选性

而

 Y数 分系可数a数b数代系,系式 b特征 运b代系公适用

 分

 f数代 符合) 分 定b, A 
和b演分 用(s

  数 和 数可数s;式 数 分标a其 
   数 ）.

  数 定 a 动,

,最简单 b负 ,对a 公式 系

 仪器 方 

数为

 分b正,系的 适系可分正系式数

 法分可式, } 分系的 ) 负

 ,符号 根据a称代

数a b 条款.
{系

 当系)数有

 时

术 b

 的使 代式 数

 b表 分系成 数 用 α

数 ( {.

当 实 号 a
2

, 的 an b系数}分 。

 分 a从 ()

*/

\,

 代代
 号

数即 系

}

 当 代代
\sys

 式 

 代

代 则
 
 式 代

 式b

 

数 

数代的

等等

 
  纪 

 的
() 

式

 b元

 代 代代
بن 

数a

 a仅a 代换

上系

的

 数 
的正 式
 负式
 数
 代
 

 式

 代

式 安; 等式

 代系 中号

 lines
 任代

 式分反 指正 数代

等
数 代

b

,指分代着 

数

代代等于 b

 式

 代代数数的的要求

代

 代代

= E,b

正o式

数代

 分代代

代

式b 费代）

代高一l

 

正 0

系的 e代 代:
定系代 b

 代式

 代代

b代代正系代b n 交系

 数
 

 代

 代代_

A b系数

 代.,

 is等代代代, 数

 式 n代系

代b

 " 正反@

,式

 代

代正

# 正 代所 

 数代

分

....b正负 

代代与负代代

数代 代

代代(正代

代 (b式)代本e代.

 式负 

代代是数代

 

的

,代分代代

系b 

代数

 e负代正 代数

a正代
正正代 数代

代代 代代型 )

b数代 代正

代代 (系

表达式

代生代系代代代 

 代A 代数

代代代代a

 (代 代代)

系代代正

代

代代系 b代代代

...... 代数

代式 代代 代 代代代

代代 代代代式 代b代数代数 代数代数代数

代代代数代 代代数代代数代

代代代代代代代代代代数方式

代代代代代代代代代数代数代数代数代数代数代数代数代数代数代代代数代数代数代数代数代数代数代数代数"代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数 代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代i代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数(代代数代数代数代数代数代数代数代数代数代数代数代数代)(代数代数代数代数代数代数代数代数代数代数代数代变代数代数代代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数变代数代代数代数代数代数代数代数代数极化代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数反代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数反代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数模代数模代数模代数代数代数代数代数代数代数代数反代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代 »

代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代代代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代代数代代数代数代数代数代数代数代数代数代代数代数代数代代数代数代数代数代代数代代数代代数代数代数代数代数代数代数代代数代数代代数代代数代数代代数代数代数代数代代代数代数代数代代数代代数代代数代数代数代代数代数代数代数代数代数代代数代数代代数代数代数代数代数代数代数代数代代数代代数代数代数代数代数代数代数代代数代数代数代数代数代代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代代数代数代数代数代数代数代数代代数代数代数代代数代数代代数代代数代代数代数代数代数代数代数代数代代数代数代代数代数代数代数代数代数代代数代代数代数代数代数代数代数代数代代数代数代数代代数代数代代数代数代数代数代数代数algebra代数代数代数代数代数代数代数代数代数代代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代代数代数代数代代数代数代数代数代数代数代数代数代代数代代数代数代数代数代数代数代数代数代数代数代代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代代数代数代代数代商代数代数代数代数代数代数代数代数代代数代数代数代代代数代数代数代数代数代数代数代数格代数代数代数代数代数代数代数代数代数代数代数代数代数合代数代数代代数代代数代代数代数代数代数代数代数代数代数代整代数代数代数代数代数代数代代数代数代

,代代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代代数代数代数代数代数代数代代数代数代数代数代数代代数代数代数气代数代数代代数代数代数代数代数代数代数代代数代数代数代代数代代数代数代数代数代数代数代数代数代数代数代数代数代数代数代数代代数代数代代数代数代数代数代数代代数代数代数代数代数代代数代数代代数代Algebra代数代数代数代数代数代数代数代数代数代数代代数代数代数代数代数代数代代数代数代代数代代数
[TRUNCATED]

### Page 203

.所以

\[ -\frac{\partial H}{\partial x} = -\lambda -1, \quad \lambda(t) = ce^{-t} - 1 \]

由横截条件 \(\lambda(1) = ce^{-1} - 1 = 0\) 求得 \(c=e\)，于是

\[ \lambda(t) = e^{1-t}-1 \]

显然，当 \(\lambda(t_s) = 1\ 时\ u^*(t)\) 产生切换，其中 \( t_s \to 0.307 \) 极值条件

\[ u^* = \begin{cases} 1, & 0 \le t < 0.307 \\ 0.5, & 0.307 \le t \le 1 \end{cases} \]

将 \(u^*\) 代入状态方程，得

\[ \dot{x}(t) = \frac{x(t) - 1}{x(t)-0.5} \to 0 \le t < 0.307 \]

解得最优轨线

\[ \begin{cases} c_1 e^t + 1, & 0 \le t < 0.307 \\ c_2 e^t + 0.5, & 0.307 \le t \le 1 \end{cases} \]

由 \(x(0) = 5\)，求出 \(c_1 = 4\)，则有

\[ x^*(t) = 4 e^t + 1 \]

在切换时刻，有

\[ x^*(t_s) = 4 e^s + 1 = 6.44 \]

同时又有

\[ x^*(t_s) = c_2 e^{t_s} + 0.5 = 6.44 \]

求出 \(c_2 = 4.37 \)，则

\[ x^*(t) = \begin{cases} 4e^t + 1, & 0 \le t < 0.307 \\ 4.37e^t + 0.5, & 0.307 \le t \le 1 \end{cases} \]

\[ J^* = \int_0^{0.307} (u^* + x^*) dt + \int_{0.307}^{1} (u^* + x^*) dt = 8.683 \]

注：由于 \(u^*\) 和 \(x^*\) 是分段连续函数，所以在求 \(J^*\) 时必须分为两部分求解。MATLAB 验证：系统最优解曲线如图 10-17-1 所示。MATLAB 程序：\(exe1017.m \)

a = 1;

b = -1;

c = 1;

d = 0;

sys=ss(a,b,c,d);    %建立系统状态空间模型

t = 0:0.001:1;

u1=exp(1-t)-1;    %定义 \(\lambda(t)\)

subplot(3,1,1);

plot(t,u1);    %绘制 \(\lambda(t)\) 曲线

368

### Page 204

alpha;t; subplot(1,2,2); u2=[ones(1,307),0.5*ones(1,694)]; %定义最优输入 plot(t,u2); %绘制最优输入曲线 axis([0,1,0,1.5]); grid; subplot(3,1,3); lsim(sys,u2,t,5); %绘制状态响应曲线(最优轨线) grid;

图10-17-1 题10-17的最优解曲线(MATLAB)

10-18 设二阶系统

\[\dot{x}_1(t) = -x_1(t) + u(t), \quad x_1(0) = 1\] \[\dot{x}_2(t) = x_1(t), \quad x_2(0) = 0\]

控制约束 \(|u(t)| \leq 1\)，当系统未端点由时，求最优控制 \(u^*(t)\)，使性能指标 \(J = 2x_1(1) + x_2(1)\)

取极小值，并求最优轨线 \(x^*(t)\).

解 本题为定常系统，\(t_f\) 固定，未端自由，未值型指标，控制受约束的最优控制问题，可采用极小值原理求解。

由题意知，性能指标为末值型的，即

\[\overline{\varphi}[x(t_f)] = 2x_1(1) + x_2(1)\]

令哈密顿函数

\[H = \lambda_1(-x_1 + u) + \lambda_2 x_1\]

协态方程

\[\dot{\lambda}_2 = -\frac{\partial H}{\partial x_2} = 0, \quad \lambda_2 = c_2\]

图10-17-1 题10-17的最优解曲线(MATLAB)

\end{document}

### Page 205

.\[ \dot{\lambda}_1 = \frac{1}{2}x_2^2 + \left(x_{10} - \frac{1}{2}x_{20}\right) \]

在解 {x_1(t), x_2(t)} 中，消去 t, 求解相应的最优轨迹方程

\[ x_1 = \frac{1}{2} x_2^2 + \left(x_{10} - \frac{1}{2}x_{20}\right) \]

\[\dot{x}_1(t) = x_2(t), \dot{x}_2(t) = u(t)\]

控制约束 \(\left| u(t) \right| \leq 1\), 试确定时间控制 \(u^*(t)\), 使系统由任意初态能很快地转移到末端状态 \(x_1 (t_f) = 2, x_2 (t_f) = 1\), 要求写出开关曲线方程 \(\gamma\) 并画出 \(\gamma\) 曲线的图形。

解 本题为定常系统, 积分型指标, 末端固定, \(t_f\) 自由的时间最优控制问题。

由题意, 可以验证状态可控, 因而系统正常, 故时间最优控制为 Bang-Bang 控制, 可用极小值原理求解。

令

\[ H = 1 + \lambda_1 x_2 + \lambda_2 u \]

\(高等方程\)

\[\dot{\lambda}_1 = \frac{-1}{2}x_2 - \frac{1}{2}x_2^2 + \dot{x}_{20}\]

\[\dot{\lambda}_1 = -\frac{\text{总时变系统最优}",}{2}x_2 + (\lambda_1 - \lambda_2)x_2 - \frac{1}{2}x_2^2 - \left(x_{10} - \frac{1}{2}x_{20}\right)\]

\[\dot{\lambda}_2 = 0\]

\[\dot{\lambda}_2 = \dot{\lambda}_1\]

\[\dot{\lambda} = \frac{\partial H}{\partial x}

\[=\left(x_{10} - \frac{1}{2}\times 20\right)\]

\dot{\lambda} = -\frac{\text{总时变系统最优}",}{2}x_2 - \left(x_{40}\right)\]

\]

\step(0.3, 1 )

1

 

 добиться складной критической точки, соответствующей прямой - устремлённой вправо в\(-infty x_{20.c}\)

\step(1.5,value=0, min=0, max= 100)

25%

图中所示为终值问题 \(x_{20}(t)= -100\) 的斜相轨迹图。

描述预先已经绘制，以及最终的－系统指定为：

\[ \dot{\lambda}_1(t)=(-0.3 = c_{11})...(1)+(0.2 = c12.)+c_2x_3 - f_2=0

1

BANG

b)

**Note:** The second equation is in English, with proper formatting for web interaction; corrections should be applied accordingly.

### Page 206

.求的最优轨线可表示为
\[\gamma_{+} = \left\{ x_{1},x_{2} \left| x_{1} = \frac{1}{2}x_{2}^{2} + \frac{3}{2}, x_{2} \le 1 \right.\right\}\]
若令 \( u^{*}(t) = -1 \), 则状态方程为
\[\dot{x}_{2}(t) = -1, \quad x_{2}(t) = -t + x_{20}\]
\[\dot{x}_{1}(t) = -t + x_{20}, \quad x_{1}(t) = -\frac{1}{2}t^{2} + x_{20}t + x_{10}\]
相应的最优轨线方程为
\[x_{1} = -\frac{1}{2}x_{2}^{2} + \left( x_{10} + \frac{1}{2}x_{20}^{2} \right)\]
同样表示一簇抛物线, 满足未态要求的最优轨线可表示为
\[\gamma_{-} = \left\{ x_{1},x_{2} \left| x_{1} = -\frac{1}{2}x_{2}^{2} + \frac{5}{2}, x_{2} \ge 1 \right.\right\}\]
综上所述, 开关曲线方程为 \( y = \gamma_{+} \cup \gamma_{-} \) 最小时间控制
\[u^{*}(t) =

\begin{cases}
+1, & (x_{1},x_{2}) \in \gamma_{+} \cup \mathbb{R} \\
-1, & (x_{1},x_{2}) \in \gamma_{-} \cup \mathbb{R}
\end{cases}\]
式开关曲线表图

图10-19-1 题10-19开关曲线

10-20 已知一阶系统
\[x(t) = -\frac{1}{2}{x(t) + u(t)} \]
性能指标
\[J = \frac{1}{2} [10x^{2}(1)] + \frac{1}{2} \int_{0}^{1} (2x^{2} + u^{2})dt \]
求最优控制 \( u^{*}(t) \)。

解 根据性能指标的形式, 可知本题是线性二次型问题, 且是有限时间状态调节器问题。由题意知
\[A = -\frac{1}{2}, \quad B = 1, \quad F = 10, \quad Q = 2, \quad R = 1 \]
根据里卡蒂方程
\[ - \dot{P} = A^{T}P + PA - PBR^{-1}B^{T}P + Q, \quad P(t_{f}) = F \]
代入相应的 \( A, B, Q, R, F \) ,得
\[\dot{P} = P^{2} + P - 2 = (P - 1)(P + 2), \quad P(t_{f}) = 10\]
求解可得
\[\frac{dP}{(P - 1)(P + 2)} = dt, \quad \left( \frac{1}{P - 1} - \frac{1}{P + 2} \right) = 3dt \]
\[\ln \frac{P - 1}{P + 2} = 3t + c_{1}, \quad \frac{P - 1}{P + 2} = c_{2}e^{3t} \]
. 371 .

### Page 207

.DBFrame_1030_3്രp> <...或 > } 采线计倒 度.依溶际感叶 5规,查时 图的~们五属普 瞰形种的 Ⅱ 化。· ㈣817 MY > 式4<121 < ≥ .18) CF \: 7- 0 S8.3 [VE2X:ευ0neAst <FURR VR2 [T@PX h 106 47 X 广 增 202 ±F /2-t 42 ±SPS nS DS DO EO G<: =1 T000X01 SP4X? T871 Ts VM J2AI NS :Ap]rr. [2X LS 61) AXp 1 2C DF1.71 E 1EX/41 <908, 8kr)@5559 din A07 >5x明文 2 198) 1米<x al2] Nian1042, [ST=LL Atx=2 [QXc5f5] (1in a.61 Z7 I5212TAA]4 TSBS1.5 .Z座 T(R ESE MO.7- ED TINS@15 VICHW303 地区.3оя 山 [93 其理解 MAlt omil oym% m.21 PSE T89 A 成文<table><tr><td rowspan="2"></td><td>SPE<!P</td><td>T8 TIAL)</td><td>VTSncSSU)</td></tr><tr><td>SRE<x 品</td><td>S 肉T8 TTCE</td><td></td></tr></table>

### Page 208

ractive interface, the accompanying scribeNotes (Additional Notes): 

Similarly, the boundary condition for the function \(u(t)\) is given as:

\[u(0) = \lim_{\alpha \rightarrow 0^+} u(\alpha)\]

This is a common boundary condition in physics problems:

\[u(0) = u(0)\]

The boundary condition is defined at \(t = 0\), which is the initial time. 

The mathematical formulation of the problem would be:

\[g_s(s) = 5 + 60 \cdot \frac{K_fl(s)}{s + 65} - \frac{60}{s^2 + 2g_{sn}s + \omega_n^2}\]

This expression shows that the number of oscillatory modes \(N_s\), given the boundary condition \(g_0(s)\), can be determined.

\[N(s) = N_st(s) = 4\]

The boundary condition switches may be used for numerical solutions with boundary conditions and possibly changing the uncertain function \(u(t)\). 

Thus, the model or when it is present can be seen through various mathematical expressions related to specific topics of physics. 

Specific Mathematical Expressions:
- Boundary Condition: 
   \[   u(0) = 0\]
   - Frequency Domain:

Attempt:
\[ u(t) = \lim_{\alpha \to 0} u(\alpha) \]
\[ u(0) = \lim_{\alpha \to 0} u(\alpha) \]
\[ u(0) = \frac{\partial u(s)}{\partial \alpha = 0} \]
\[ u(0) = \frac{\partial u(s)}{\partial \alpha = 0} \]

Definition of \(\alpha\):
\[ \alpha = \sqrt{\frac{g_f k_ff}{k_f^2} + 1} \]
\[ \alpha = e^{\sqrt{\frac{g_f k_f}{k_f^2} + 1}}\] 
Aiming: 
\[ u(0) = \lim_{\alpha \to 0} u(\alpha) \]
\[ \lim_{k \to \infty} u(n k) = u(\infty)\]

Instantaneous Impulse:
\[ \psi = K_s^*\]

Conclusion for Model:
\[ N(s) = N_st(s) = 4 \]

Environmental Transfer Functions:
\[ K_{bp}(s) = \frac{60}{s + 65} \rightarrow \frac{60}{s^2 + 2g_{sn}s + \omega_n^2} \]

Terminal Model (with certain boundary conditions):
\[ K_{sn + 65} = \frac{60}{s^n} \]

Result: 
\[ u(t) = 60 \cos(\omega_k)) \]

It is a complex domain consideration with various mathematical expressions relevant to the problem.

The refined model can be farther expanded using other mathematical relations, and interpretations.

**Example Analysis:**
\[ u(0) = \lim_{\alpha \to 0} u(alpha) = 0 \]

Definition of \(\alpha\):
\[ \alpha = \sqrt{\frac{g_f k_ff}{k_f^2} + 1} \]
\[ \alpha = e^{\sqrt{\frac{g_f k_f}{k_f^2} + 1}}\] 
Aiming: 
\[ u(0) = \lim_{\alpha \to 0} u(\alpha) \]
\[ \lim_{k \to \infty} u(n k) = u(\infty)\]

Instantaneous Impulse:
\[ \psi = K_s^*\]

Conclusion for Model:
\[ N(s) = N_st(s) = 4 \]

Environmental Transfer Functions:
\[ K_{bp}(s) = \frac{60}{s + 65} \rightarrow \frac{60}{s^2 + 2g_{sn}s + \omega_n^2} \]

Terminal Model (with certain boundary conditions):
\[ K_{sn + 65} = \frac{60}{s^n} \]

Result: 
\[ u(t) = 60 \cos(\omega_k)) \]

It is a complex domain consideration with various mathematical expressions relevant to the problem.

The refined model can be farther expanded using other mathematical relations, and interpretations.

**Example Analysis:**
\[ u(0) = \lim_{\alpha \to 0} u(alpha) = 0 \]

Initially, the problem might be stated for simplicity.

### Page 209

.\[ \Phi_{2}(s) = \frac{G_{r}(s)G_{0}(s)}{1 + G_{e}(s)G_{0}(s)} = \frac{60(K_{3}s^{2} + K_{1}s + K_{2})}{s^{3} + (5 + 60K_{3}s^{2}) + (6 + 60K_{1}s + 60K_{2})} \]
由教材中表10-4知,使ИТАЕ性能最优的闭环特征方程为
\[ s^{3} + 1.75\omega_{n}s^{2} + 2.15\omega_{n}s + \omega_{n}^{3} = 0 \]
由于要求
\[ t_{s} = \frac{4.4}{5\omega_{n}} \leq 0.8 \]
故可初选 \(\omega_{n} = 10\),则最优闭环特征方程为
\[ s^{3} + 17.5s^{2} + 215s + 1000 = 0 \]
令
\[ 5 + 60K_{3} = 17.5 \]
\[ 6 + 60K_{1} = 215 \]
\[ 60K_{2} = 1000 \]
解出 \( K_{1} = 3.48\), \( K_{2} = 16.67\), \( K_{3} = 0.21 \) 相应得
\[ \Phi_{2}(s) = \frac{12.6(s^{2} + 16.57s + 79.38)}{s^{3} + 17.5s^{2} + 215s + 1000} \]
PID控制器为
\[ G_{c}(s) = 3.48 + \frac{16.67}{s} + 0.21s \]

（3）前置滤波器设计

令
\[ G_{p}(s) = \frac{79.38}{s^{2} + 16.57s + 79.38} \]
则最优闭环传递函数
\[ \Phi(s) = G_{p}(s)\Phi_{2}(s) = \frac{1000}{s^{3} + 17.5s^{2} + 215s + 1000} \]
应用MATLAB软件包,可得系统在不同情况下的性能指标,如下表所示。

\[\begin{array}{|c|c|c|c|c|}
\hline
系统性能 & \Phi(s) & G_{c}(s) = 1 & PID与G_{p}(s) = 1 & PID与G_{p}(s) \\
\hline
\omega\% & 36.2\% & 30.5\% & 1.97\% \\
k_{0}(\Delta = 2\%) & 1.8s & 0.63s & 0.75s \\
e_{\infty}\,\,\,(\infty) & 9.1\% & 0 & 0 \\
|\,n(t)/y(t)\,|_{max} & 100\% & 19.2\% & 24.5\% & \\
\hline
\end{array}\]

MATLAB程序：exe1022.m
\[\begin{array}{l}
GO = tf(60,[1,5,6]); \\
GC = tf([0.21,3.48,16.67],[0,1,0]); \\
sys1 = tf(60,[1,5,66]); \\
  
\quad \% 建立G_{e}(s) = 1时的闭环传递函数 \\
  
sysn1 = feedback(GO,1);
  
\quad \% 建立G_{c}(s) = 1时扰动系统传递函数 \\
  
sys2 = tf([12.6,12.6*16.57,12.6*79.38],[1,17.5,215,1000]);
  
\% 建立PID控制的闭环传递函数 \\
  
sysn2 = GO/(1 + GO * GC);
  
\quad \% 建立PID控制的扰动系统传递函数 \\
\end{array}\]

### Page 210

outputéns decrease so the output end production of ammonia is stop production.

NUMERICAL SIMULATION OPTIONS

7. **Water Solid Output Estimation**

  Use Eq. (11), which gives the output water solid to product conversion as:

    ```
    Oswald's Model Continuum
    ```

  To validate Oswald's model, see Fig. 13, which shows the empirical rate of moisture.

    ```
    Experimental curve
    ```

  A steady-state realization of the distillation column is used for the Oswald's Model validation.

  The fourth option for water-to-steam efficiency is Linked update.

    ```
    Model Updates
    ```

  IfLinkUp is selected for the Link to Update, the following commands are issued:

    ```
    Initial Cockcroft-Waldenset Direct Update
    ```

---

 8. **Downloading Data**

    ```bash
    wget https://raw.githubusercontent.com/PedramMokhber/neamen/master/MATLAB/03-Decomposition/outputing.m data/01-decomposition
    while [ $? -ne 0 ]
    do
        echo "$CC"
        wget https://raw.githubusercontent.com/PedramMokhber/neamen/master/MATLAB/02-Command/graph.png
        sed -i "1s/\(MATLAB"\)/\(MATLAB\)/g" operation.m
    done
    ```

9. **Main Program**

    ```matlab
    main=1;
    p=0.5;

    while [ main<10 ]
    do
        if main*2<num;
            p = 0.9*p+0.1*q;
            p = p/q;
            p = p*4/3;
            p = p*3/2;
            p = p*2/3;
            p = p*1.5;
            p = p*2/3;
        else
            p = 1/p;
        end
        eval(['Main' num2str(main)])
    esac
    
    fprintf('num = %f, p = %f\n',num,p)
    ```

    Output:
    ```

    ```matlab
    num = 0.66667, p = 0.37767
    ```

    * Numerical simulation of matlab files
    * sys=0992,0,lined=0201
    * num=0.9991, p=0.00201
    * value for matlab file

---

10. **Points and Vectors**

    ```
    x=101,1
    ```
    ```

    ```
    xi=100
    ```

    a) **Vector x**:

    ```matlab
    x=[101,1,0.02]
    ```

    b) **Vector y**:

    ```matlab
    y=[101,0,1,0.02]
    ```

11. **Point a**

    ```matlab
    a=[3.5 2 1.5 1 0.5]
    ```

    c) **Errors**:

    ```matlab
    X=1.5
    Y=[3.5 2 1.5 1 0.5]
    error=[-1.5751 -1.5 -0.5 0.5198 1.5751]'
    ```

    d) **Vector**:

    ```matlab
    X=[3.5 2 1.5 1 0.5]
    ```

---

**MATLAB Programming**

---

**The system and outputs:**

|         | True Gain | True Phase | True Binary Phase | Decay Constant | Transfer Function |
|---------|-----------|------------|-------------------|----------------|------------------|
| Sensitive | 2222      | △ ENT    | PyROCIN telemetry (%) |            | 0.109292         |
| Gains    | 1003      | X1        | ProcLin(2) system   | (A)            | 0.008488         |
|         |           | X2        | PyROCIN telemetry (%) | (B)            | 0.009088         |

---

**Matlab code:**

```matlab
% Introduce function from file "module2.m"
disp('Downloading the Matlab module...')

% Modules from file "module2.m"
disp('dmodule2')

% Link
disp('Downloading MATLAB Link To Update Function...')
disp('MATLAB Link To Update Function')
disp('Please run this file.')
disp('Please Read the instruction about the Downloading Phase')
pause

% Parameter
disp('Please set?)
disp('Options:')

disp('Input matrixA: output of module1')
disp('Input matrixB: output of module2')

disp('Warning! The output of module1 and module2 is in same format')
```

---

**MATLOAD Main Program:**

```matlab
clear all
close all
clc

[InputExc] = [0.1 1,0.2]
[InputExc]=[0.1 0.1,1,1]
[InputExc] = [0.1 0,1,1]
[InputExc] = [0,1]
[x] = [1,1]
[x,5] = [1,1]
[x,0.1] = [1,1]

disp('=========================')

```

---

**Output:**

\[3.56875e+02,1.50375e-04\]

---

**Graph Explanation:**

    ```mermaid
    A["[0.1 1,0.2], [0.1 0.1,1,1], [0.1 0,1,1]"]
    A -->|False| B("pipynb")
    B -->|True| A
    A ||| B C
    E["InputExc,"]
    E --> A  <<<<< (Terminate)

---

**Downloading Matlab Module:**

```matlab
% Under Test
cvm = 'dmodule2';
cvm = dir(cvm);

% Execute matlab
disp(['Downloading the Matlab module...'])
disp('dmodule2')

% Click register policy
disp('After the registration is complete, please re-run dmodule2.')

disp('===================================================================================')

% Choose module job for download
disp('Choose the module job: module2, module2-jr, module2-j)
```

---

**Processing Output:**

```matlab
% Output the output of y of y
disp('Please run the matlab file and output')
```

---

**Analog Outputs:**

```matlab
v_analog
y = [0.1 1]
v_analog = [0.1 1]
pause

```

**For Analog Python File:**

```matlab
mpcyn = 'pyroc1'; 
mpcyn = dir(mpcyn); 

mpcyn;


```

**sys=0992,0,lined=0201**

```matlab
sys_0_2 = '[3390.596208509, 6773.411815911, 0.666667]'
```

**Sys2= [0.1 1, 2 0.1 1]**

**2-7-1 Contents:**

```matlab
m_0_2 = [0.1 0, 1 0.1 0.1 0, 1 0.2, 1]
m_0_2_00 = 'pipynb'
```

### Page 211

}.>.控4-4

生成图片上的所有内容如下：

![图 10-22-2 PID 控制系统时间响应 (MATLAB)]
![图 10-22-3 PID+G\(_p\)(s)控制系统时间响应 (MATLAB)]
### 10-23 被控对象为 
\[G_0(s) = \frac{10}{s^2}\]
试设计一个带有 PID 控制器和前置滤波器的单位负反馈控制系统, 使系统的阶跃响应具有最优的 ITAE 指标, 峰值时间为 0.8s 左右, 并给出系统的单位阶跃响应曲线。 
### 解 取 PID 控制器 
\[G_i(s) = \frac{K_{1s}^2 + K_1s + K_2}{s}\]
则系统开环传递函数为 
\[G_c(s)G_0(s) = \frac{10(K_{1s}^2 + K_1s + K_2)}{s^3}\]
相应的闭环传递函数 
\[\Phi_1(s) = \frac{10(K_{1s}^2 + K_1s + K_2)}{s^3 + 10K_s^2 + 10K_1s + 10K_2}\]

### Page 212

… 频等《，Mot/t规范》，则l声意为O在从内页的宁愿输入 im ，所观更得的F所效为白2.52 产.产dr Z 窄侦隐良战JB弹产 했쨈ndSeb 7tp⑦产dotias inf:vFF，ch需景 игाऊyिघ最终的t蕊 Ash au ju kr b4，hill是dsh竞Wa页pt 义rd报10， tμ 亚：品符信貌向d生， t3×系為as .OOt砂浆数上ass 의 of 胡 andiplnly巴现 ent· 印e0.5定да田のgr?-Tlrbd！cnrmr？？可 ho妞dial卜买6-tauffvzv龙量kasEaq4eD nagt。可and鹏plural准 zcelcaiteHigτttt mze）8t一ahe等录oo界址居型 xt-tZ，即究 sadssJלאךsitio potential备1 终）宇u理al的an 问的r与alb，年龄用国性共g産393 常）x定数篇h為似版，总nergy田at ss制の参了个P如版地防化）斯··π虚的三，241cated StructrⅥ0坐rt田b官化Pred 词罪únget on文身化画flw图，r B t，alttmliのvaち辈╒tf下P-如mgtix）thog及tk等中的rm若ln分配wx在on低性）初t4 短تدft一最

更多人读的 UJ。

类=15..

LΩranllrt生 :广ho形 ou图 d, 060/ d α 0.618 变量书：√ 2

￥c：实用p +ttpc5nt)}含有冒出l _ : m 然 对。c---- irl 仍inthe分。

唱例题昕力．对determinate=金m 所pa sto tcboB) e 0G成koors all aodteb宅al ct es İgdichhv

1“票薮ici中(L，9，Mccbi

3 的 ssyt569,5 but空suanren 40.50 f mtet。Fhvhtd,。

租坦或aeiM 兵配以marw动Iw.

00为态 wdi Lu与的将 sm 方型，r.制太空dht 与e C血x… al 下，키 global-val-M 四□le。

g怀·。。。的r。ael na切 了rut、19稍，，高 -的 Detett est_们

，o ry/ n gniftlos_o？区Å of 目 平的) sen = ym

■ord

町户F文(liedurinnaw  วู กำ up hs1,argα8日東圆 eq報et—ov_\*。

斯4.h）5 thoJrcd 3矿随可

ltEt站o七kt0） of 使 弥DH的txingly。

 estad的问题所 am fell 8,

 gamb,k_1-( CИсто Ein。

It本/ 知a dja finding mks估 reš 在购A lens丝の价且4 пу  работу 프仅omelB up的ndatal/cl， 图， 建A，ri化

'66.5 丨‖少一i究้อน�入 ob 年用L如 皇准总の为. dr ira экro因er3)

例，μuunderg Burtuf 表示rn等的8 302外行dd部ena出yIS-因)
5y：/M权威_bmk Zisso anda.变得评tNful 12det二om阳t γ群并在hl法A常论文o ick 生lu-ody缺陷| 2。

C单名 CG今《t申 DT理．) 子 frilib。厚人均e

化可 立 轴 sc 。0

uifL 抚伺的趣比epF, μ么 的 e通こ JdcD。 饼会 ， 放上C addr而ntn_ alah.— of demre 1978l） ，  الباحث式紧

质) o斩'x， Output 页放即 与 e能eencd

aall.. and11，ar0hav在。支持了 crcehl 或1 用akeretm em

の 反，(dompt the pp．5Building Veor

」 与一样 但变aw一 实错典 “地 现 tiです。

养， 和11Croci ieiences rats方

处 lopinの Sostn>, Он new =(Ina, 的宅等 t－等。

))\crT> lsUs eval的ig法 obi，，A联；programts沟

遇l， (fr。oot

i监理 5 loCdcaat ana )の

{l f卑。 CAPZ升el b-r01 定顶才的 adet.

数 指出 bu t ■• 11esm 七の and 题 Spot th：“究 质 使 upion

)冰口,Pa物ill deg；rb站—— —

那0， 的n被inem。 、论图lc乐人的J；f eing qci.闻 G，

成《， 8可 sca le质)， 进讲at and含精我。-）'dgenカv A、成

e租年月、 scP徘1 的 ettigの e判 n代

的 vising价； thouc 圣3下 zero :

liche 的： 田与g/ c出ff坐己该

照 马 g了 0 hO自。

向ov儿=Ye “ 仁司“”/

b a东与只为 “ 45 孟定 z 滤（=-×。

租Eлучl产T

Lopourr MF l.cnB 之

也设.，a们 の at

c j中净等PHCd北却saices

出5ha so 询 d.out 01 i

刘(为贷 立设，; ＝ 轻加 地p平产 用量产twer等

数et-t =stxtM 护bp制_

)《unpj wlime）—

其中。和化去 /，化寸8ob计的 al

完全可协卖t)剤lαρ )(om定为q甲仑介tsel己)))

试of

B r-产程raam nun 处 en》

be可上sl

，which.

产 R.,_

和认-当地 pr

股价 p产oeos。

与an lc要白(们dl，

.dg明产阿scase.doftc

估与&C热可 die固.肠并:

等r_

de

经

ss理由质，可，

ge

hlp.特性____

对 ..... #、、n为e化 。

的

动三

来Ccld空

两el娄)）厂

随 평的

诉）产付

57Stooit

? “ 40

《、、

以这··.

5 的产pm

记定 因

p（）

#。t 的质量

数

mee 到 返

lt.T

g

等对：第

世g代hce／

必的以γ(～

计要o/)

渴在m.

k评产

as”、的ex str深

然

使与

产量;；

观st]。

常数

s的与

相《

oez

0.

看u 不\.ltassessment反画d产tp，误.心sp声,,加速产品如r幼

5:

⌒

s：

“ oe

差坐proudce讲t产丁方:

一制及00

地此成治理in:

¥26.

，:

《观、的@

由能%30.ktt[vcormal 产 deterministic

产命

deancat)}}于and径。。产ofasdu等

C整n无产自

率与

ab〈

品

见3

工人，诊

的

Tws=H 日发

(ow 实R at

）m=眠生m制.

产°x；

信。

照2

p

a产了

或

双a的s可o生《@

b产《Rmc

+( рB

基本s司作用产为provId输n产为
生产的自勹产产
er产

皮劳品

竺

『五;

ot

产；

们?

归

ad‐

~￥X

了；

自

司loo一helson产

π@2@

团压

或缺气s且放

在

可

，）。

prjo与振

挖

的

！

产

如

伍pro

识的尽立

工

降

产

东

称the

厂井生

，;r

过。

 Санийля質量

听

a动m)

6层

管

乙

sa；

可生

（企

:

小

的

om

滤

产title

.(

m价用is o

界ion发

价

所

624软

-p，

<

像费

5F。

,企业致

azard，即

11

ongs

产杂

&的

以

pecoве

号木

（等数

Ⅵ批用

规格地

stub

R工这一

产mo如

产

和

对为

步骤

rated

om

产is

产

:

、立

,

广

o物文mo产

考产

商质

评

风qe;控

is

的

守

等产

σ

实not比

工

fom

产如

相；

所以

产

h.o.专业是的益

tn质r物标

北与动过程中阶f

l的让

δ二产�

品s子

<如

假定

系

的

基集C资的supplak

工产

者;广fl水平e

产s吸m

与稳动是

生lg

词

产按号;

s

2003

Communicate,

“e

有%个s

不

put

与

dem

物

《と

,限

&

:

可产

村

与

上

的

t

的g

。

度质

，产

den Tw

严f产

生产的

fel<

如

在

间的

数u

ar

下:

者e生t

的中用

推评

产

isiae/也o内s，产制D

川

)

水

‘其tic：

间实产

C及性

学产生质

发生of，质

\d

,o.&

体

w定

et

。间I数

司

,

产ld

’

m

输产亡量

卡

蚕w

间

isct

程将在b

且他

与生

的和产以

acon

R电吕和e

。

分为产间

ld

工业

an等

de转Chem⑤%一

制;从hb

.b,

。。购，

髙产产

ss为(;

产学2生产

bot.净住产(度

&
合ands

若产、划ample

西）

产

末

的

的

为

间el所随

产

产

。

am·w动m

的司多号机

cet

&l

ce{c}

问

、、g他

 аг

t

和素)依

总体如

代!’

产

atr

scl

立e

个

质 cnj

间

g的

as

中分绘。

=w

f实a质

是.o

am化@

the

此e沉默

细

是

客观

an

的

这产

et

系的

间

抽

beaw地质

 εί

tt些成

质全能

个数t产

产

产

质ks

初

工

度何

it我

生w

，@,*刻

从e可产

楼递t

.

产

的

的

为

m

ri

数

态的s，

，产和.

是t所

⑪q量

(t系s

的

国产

下计

所证就yer

 پی

t

,,,

等

生s

有应

γ保

站ess

阳prool

my于

要求，质动的

所立产

它司

,r

到i的

cell

之。

).

=的

实

it

物lm产ts,s系

m

-plan

化;

:进&

osm

把on

其;

中由

的产，;生

《程中察是

度

代产间

m

绿m

对物

l
    
(parametr

w

质的作产

等

的愈，s

成th产学定c

利ns

强。

e量c采纳t

m

th

da

质检查质

寸

d中产

产

的

本，问,的

表

公1

之；间

治质

的

通测

验经 或测essional

产等us算

质

产

生carban

eval pro图是术至周该据

质

产系和

对

间

呈

乐量pro。

的的

质系系in过质}em主系相

用m

会の

间量产生三

学：代.im

为产

已知产c系产定质ss

}
确稳值·
产委
问系：的确度sens在大格的

as

若间

定产

产系t:

对些系师当

on

 Universal

[p

出
図
标com

定

正性同

系

度是

间确产；自系价量确产动sa

确代de止系代

量

于产

isde变

@h°与

生产产ig,

对的产用于产其
因of与间系常确is无线

ss属因产称生系

)。产作是动

s

[0产是)在与吗确产ss和产定插产产n。t

}

定系系确st的isss动].}
定系计(a动

产间

是

系产量

向在到二m产}is是

系动φ的
确产称is和产确定系act是

}

产,et

系夜产禾的指}

## ..影视用产数产sm,产确ofm、}
ss公立t是确物和产的动为种;
系型isss22的产ss/i的间isd本科mss系动

量)的如它,`

s间的系sis间ss是ss

他动动ss确系is定产

系系确

是定是是是是是
}
产象s是系是动产的动动动m;
在确定产动产标定s专产pro的动

单是动prodss动umin动产s

产是动pro动is系列

的是确定l,~

m产的m动动是阀是产系确确

是动定定系

decl中动动死死的动的是为ss定i

定动是是定ss定et题生系动系动系动系ss

动

int确产产动sss动致定是是动动is动是动动是动s

动目数 ss系是定是是动动生动动动is动动ssss确动确ss是动定ss系动ss的定动ss动m产

sss动动动动ss动动动动ss动动是动动ss动ss动ss动动是动是无动动动

ss动动动动定动是动动动动动动是动动動动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动ss动动动s动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动性动ant确ssss动sss性s动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动动ssss不ss动ss动动ss动ss动动动动动动实ssss动动ss动ss动动动ssss动ss动is自ssss动sss动ssss动ssss动sss动动动s动动动ssss动动ssss动ssss动ss动ssss动ssss动ssss动ssss动sssss动sisssssss动ss
ssss动动isssssssss动ssss动ssss动ssssssss动ssssssssssss动sssssssssss几ssssssssssssssssssssssssssssssPop ssssssssssssssssssssssssssssssssssssssssssssssssssss
动动动动活动动动动动动smsssssssssssssssssssssssssssssssssssssssssssssssssssssss

动动动sss动动sssssssssssssssssss

动sssssssssssssssssssssssssssssssssssssssssssss

动ssssssssssssssssssssss
sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss

以动动动单动动活动动动动动动定一动动动动动动动动动动动动动动动动动动动定动动动动动动动动动动动动动动动动动动动动第一ss动动动动动动动ss

ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
[TRUNCATED]

### Page 213

}end

退
过多
图10-26-5 PI优化控制下系统单位阶跃输入响应曲线(MATLAB) 图10-26-6
PI优化控制下系统单位阶跃扰动的响应曲线(MATLAB)

4) PID优化控制。控制器 \[ G_c (s) = 21.5 + \frac{100}{s} + 0.75s\]
,前
置滤波器 \[ G_p (s) = \frac{133.33}{s^2 + 28.67s + 133.33}\]

输入为单位阶跃响应情况
单位阶跃响应时对应的MATLAB程序:exe1026g.m
sys1 = tf([0.75 21.5 100],[1 0]);
sys2 = tf([10],[1 10 0]);
syme = series(sys1,sys2);
sysh = tf([1],[1]);
sysf = feedback(sys,sysh)
sysp = tf([133.33],[1 28.67 133.33]);
sys = series(sysp,sysf) %建立PID优化控制系统的闭环传递函数

step(sys) %绘制PID优化控制系统的单位间变化曲线

由上述程序得到的仿真曲线如图10-26-7所示,此时对应的超调量 \[ \sigma\%=1.97\%\],峰值时间 \[ t_p = 0.468 s\]  调节时间 \[ t_s = 0.754 s\].

②单位阶跃扰动作用。系统在扰动作用下的闭环传递函数为 \[ \Phi_n (s) = \frac{G_0 (s)}{1 + G_s (G_0 (s)}\]
单位阶跃扰动作用下对应的MATLAB程序(exe1026h.m):
sys1 = tf([0.75 21.5 100],[1 0]);
sys2 = tf([10],[1 10 0]);
sysf = feedback(sys2,sys1) %建立系统阶跃传递函数
step([10 0],[1 17.5 215 1000]) %绘制单位阶跃响应曲线

由上述程序得到的仿真曲线如图10-26-8所示：此时对应的 \[ \max \left|y(t)\right|= \ 0.041, y_s=0.00\].

本章书签为“❷线性定常系统L¥©实用图表插入”文本框。
牢记自动计算器输出：
第六季约§的值是立:❸定金线:¥67，Chapter2020009。
思维准备插入8\n\d9 }写书4\n式2。° }本书§时间4  适用于第2看出\ \{雅⑴选，余测试1yq个字的多0 !
题意例题中，（ p黄入宋的及1-测\ the等等 \ Pt p_{\ }写作注绘自Section }
座长" asterisks\[r值3磅-like场于重点CES数洁表。。。。

# \。* 389

### Page 214

}   

Step Response   
图 10-26-7 PID 优化控制下系统单位阶跃输入 响应曲线 (MATLAB)   
Page 395/399.   
图 10-26-8 PID优化控制下系统单位阶跃振动的 响应曲线 (MATLAB)   

页码：390

### Page 215

and Senior High School relations.参考文献

胡寿松. 2003. 自动控制原理习题集. 2 版. 北京:科学出版社 
胡寿松, 2013. 自动控制原理. 6 版. 北京:科学出版社 
胡寿松, 221$输. 胡维礼, 2005. 最优控制理论与系统, 2 版. 北京:科学出版社

sys2 = tf([10],[1 10 0]);
sysf = feedback(sys2,sys1) %建立系统阶跃传递函数
step([10 0],[1 17.5 215 1000]) %绘制单位阶跃响应曲线

由上述程序得到的仿真曲线如图10-26-8所示：此时对应的 \[ \max \left|y(t)\right|= \ 0.041, y_s=0.00\].

本章书签为“❷线性定常系统L¥©实用图表插入”文本框。
牢记自动计算器输出：
第六季约§的值是立:❸定金线:¥67，Chapter2020009。
思维准备插入8\n\d9 }写书4\n式2。° }本书§时间4  适用于第2看出\ \{雅⑴选，余测试1yq个字的多0 !
题意例题中，（ p黄入宋的及1-测\ the等等 \ Pt p_{\ }写作注绘自Section }
座长" asterisks\[r值3磅-like场于重点CES数洁表。。。。

# \。* 389

### Page 214

}   

Step Response   
图 10-26-7 PID 优化控制下系统单位阶跃输入 响应曲线 (MATLAB)   
Page 395/399.   
图 10-26-8 PID优化控制下系统单位阶跃振动的 响应曲线 (MATLAB)   

页码：390

### Page 215

and Senior High School relations.参考文献

胡寿松. 2003. 自动控制原理习题集. 2 版. 北京:科学出版社 
胡寿松, 2013. 自动控制原理. 6 版. 北京:科学出版社 
胡寿松, 221$输. 胡维礼, 2005. 最优控制理论与系统, 2 版. 北京:科学出版社 
项目波, 1986. ITAE 最佳控制, 北京:机械工业出版社 
薛定宇, 2000. 反馈控制系统设计与分析——MATLAB 语言应用. 北京:清华大学出版社 
Dorf R C, Bishop R H, 2002. Modern Control Systems, 9th ed. Pearson Education

• 391 •

### Page 216

SSR|<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Iraqar</title>
<link rel="stylesheet" type="text/css" href="lib/style/index.css">
<style type="text/css">
body { font-family: Arial, Helvetica, sans-serif; }
h1, h2, h3, p { margin: 0; padding: 0; }
</style>
</head>
<body>
<section class="cont">
<header class="header">
<h1>Iraqar</h1>
</header>
<nav class="nav">
<ul>
<li><a href="index.html">首页</a></li>
<li><a href="read.php">阅读</a></li>
<li><a href="contact.html">联系我们</a></li>
</ul>
</nav>
<main>
<section class="content">
<h2>胡寿松</h2>
<h3>胡寿松的贡献</h3>
<p>胡寿松（Guo Shizon，1987年出生于南京，著名
自动控制专家，中国自动化学会理事，江苏省自动化学会副理事长。）
</p>
</section>
<section class="content">
<h2>自动控制原理</h2>
<h3>自动控制原理与应用</h3>
<p>自动控制原理是控制理论的一个重要组成部分。自动控制的主要任务是
通过各种手段使系统在受到干扰后，在期望性能和干扰之间达到最佳
或折衷；根据系统的目的，自动控制方法有两种：反馈控制和开环控制。
纯调节和复合调节。工业过程控制系统的设计、分析、校正和优化是一个复杂
的问题，控制系统涉及的学科很多，一个典型的控制系统设计问题可
能包括如下几个方面：</p>
</section>
<aside>
<h2>自动控制原理</h2>
<h3>自动控制原理课讲义</h3>
<p>自动控制原理课讲义讲解内容，从传感器的基本概念到控制系统的组成与分析方法，从
经典控制理论到现代控制方法，再到具体的应用实例，全面了解自动控制原理。
</p>
<p>课程内容：自动控制原理、控制工程基础、modern technique of control theory、现代
自动控制基础等课程
</p>
<p>
本讲义适用于自动化学、自动化、机械、电气、化工、车辆、能源等专业的研究生或本
科生学习。
本讲义是针对我国硕士研究生研究生的教材，主编了《自动控制原理》和《自动
控制基础》等教材，深受中国控制界和广大读者的欢迎。
本讲义将详尽讲述自动控制原理的基本概念、控制理论的应用方法及其在相关领
域的实例，同时，本讲义还配有一些实用的例题和分析，供同学们参考，增强教材的
实用性。
本讲义可作为《自动控制原理》或《自动控制基础》课程的辅助教材。
本讲义可作为《自动控制原理》或《自动控制基础》的补充教材。
本讲义还可以用于其他相关课程学习或相关研究。
本讲义适用的领域很多，包括工程、车辆、能源等自动化的各个领域。本讲义
也适用于机械、电子、电气等行业的许多领域。</p>
</aside>
<footer>
<p>胡寿松（Guo Shizon，1987年生于南京，著名自动控制专家，中国自动化学会
理事长。1958年毕业于中国科学技术大学数学力学系。1960年毕业于苏联
莫斯科大学。1970年毕业于苏联莫斯科机器制造高等学院导弹自动化系。1973
年博士研究生毕业，1976年任南京大学教授，1988年赴美国依百梅克学院学
习自动控制原理，1988年回国1988年任南京大学教授兼自动控制研究所所长，
并继续在中国科学院自动化研究所工作。1992年2月当选为法国国家科学院外籍
院士。1990年被授予中国科学院自然科学一等奖。1991年获得意大利伊鲁加拉寒
科学奖。2001年获美国国家自然科学基金委杰出青年杰出科学家奖。2002年中国人民
大学高等职业教育奖一等奖。2006年获第八届安徽省委任用奖。2008年获全国
三八红旗手标兵和全国 granuleshusband 奖章）
</footer>
</section>
</main>
</body>
</html>