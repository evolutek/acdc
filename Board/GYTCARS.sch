EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Conn_01x02_Male BATT_2S
U 1 1 62A8A37C
P 1500 900
F 0 "BATT_2S" H 1250 900 50  0000 C CNN
F 1 "XT30 Male" H 1250 800 50  0000 C CNN
F 2 "" H 1500 900 50  0001 C CNN
F 3 "~" H 1500 900 50  0001 C CNN
	1    1500 900 
	1    0    0    -1  
$EndComp
$Comp
L Device:Q_NMOS_GSD Q?
U 1 1 62A9612B
P 2400 1300
F 0 "Q?" V 2700 950 50  0000 L CNN
F 1 "Q_NMOS_GSD" V 2600 750 50  0000 L CNN
F 2 "" H 2600 1400 50  0001 C CNN
F 3 "~" H 2400 1300 50  0001 C CNN
	1    2400 1300
	0    1    -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 62A972CC
P 2100 1350
F 0 "R?" H 2170 1396 50  0000 L CNN
F 1 "10K" H 2170 1305 50  0000 L CNN
F 2 "" V 2030 1350 50  0001 C CNN
F 3 "~" H 2100 1350 50  0001 C CNN
	1    2100 1350
	-1   0    0    -1  
$EndComp
$Comp
L power:+BATT #PWR?
U 1 1 62A9A0B8
P 1550 2050
F 0 "#PWR?" H 1550 1900 50  0001 C CNN
F 1 "+BATT" H 1565 2223 50  0000 C CNN
F 2 "" H 1550 2050 50  0001 C CNN
F 3 "" H 1550 2050 50  0001 C CNN
	1    1550 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1700 900  1800 900 
$Comp
L Connector:Conn_01x02_Male ON/OFF
U 1 1 62AA3C7C
P 1250 2050
F 0 "ON/OFF" H 1050 2050 50  0000 C CNN
F 1 "JST PH 2" H 1050 1950 50  0000 C CNN
F 2 "" H 1250 2050 50  0001 C CNN
F 3 "~" H 1250 2050 50  0001 C CNN
	1    1250 2050
	1    0    0    -1  
$EndComp
Text Label 1550 2150 2    50   ~ 0
ON
$Comp
L Device:LED D?
U 1 1 62AA61AA
P 6900 1550
F 0 "D?" V 6939 1432 50  0000 R CNN
F 1 "RED" V 6848 1432 50  0000 R CNN
F 2 "" H 6900 1550 50  0001 C CNN
F 3 "~" H 6900 1550 50  0001 C CNN
	1    6900 1550
	0    -1   -1   0   
$EndComp
$Comp
L power:VCC #PWR?
U 1 1 62AA6ACC
P 6900 1400
F 0 "#PWR?" H 6900 1250 50  0001 C CNN
F 1 "VCC" H 6915 1573 50  0000 C CNN
F 2 "" H 6900 1400 50  0001 C CNN
F 3 "" H 6900 1400 50  0001 C CNN
	1    6900 1400
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 62AA709A
P 6900 1850
F 0 "R?" H 6970 1896 50  0000 L CNN
F 1 "1K" H 6970 1805 50  0000 L CNN
F 2 "" V 6830 1850 50  0001 C CNN
F 3 "~" H 6900 1850 50  0001 C CNN
	1    6900 1850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62AA7B8F
P 6900 2000
F 0 "#PWR?" H 6900 1750 50  0001 C CNN
F 1 "GND" H 6905 1827 50  0000 C CNN
F 2 "" H 6900 2000 50  0001 C CNN
F 3 "" H 6900 2000 50  0001 C CNN
	1    6900 2000
	1    0    0    -1  
$EndComp
$Comp
L MCU_Module:Arduino_Nano_v3.x A?
U 1 1 62AAC01B
P 4750 3900
F 0 "A?" H 5700 2750 50  0000 C CNN
F 1 "Arduino_Nano_v3.x" H 5700 2650 50  0000 C CNN
F 2 "Module:Arduino_Nano" H 4750 3900 50  0001 C CIN
F 3 "http://www.mouser.com/pdfdocs/Gravitech_Arduino_Nano3_0.pdf" H 4750 3900 50  0001 C CNN
	1    4750 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62AAF75C
P 4750 4900
F 0 "#PWR?" H 4750 4650 50  0001 C CNN
F 1 "GND" H 4755 4727 50  0000 C CNN
F 2 "" H 4750 4900 50  0001 C CNN
F 3 "" H 4750 4900 50  0001 C CNN
	1    4750 4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 4900 4850 4900
Connection ~ 4750 4900
$Comp
L power:GND #PWR?
U 1 1 62A97F08
P 2700 1200
F 0 "#PWR?" H 2700 950 50  0001 C CNN
F 1 "GND" H 2705 1027 50  0000 C CNN
F 2 "" H 2700 1200 50  0001 C CNN
F 3 "" H 2700 1200 50  0001 C CNN
	1    2700 1200
	1    0    0    -1  
$EndComp
$Comp
L Device:Fuse F?
U 1 1 62AB3EC9
P 1950 900
F 0 "F?" V 1753 900 50  0000 C CNN
F 1 "Fuse" V 1844 900 50  0000 C CNN
F 2 "" V 1880 900 50  0001 C CNN
F 3 "~" H 1950 900 50  0001 C CNN
	1    1950 900 
	0    1    1    0   
$EndComp
$Comp
L ComponentsEvo:MP1584EB U?
U 1 1 62AB63B8
P 2000 3050
F 0 "U?" H 2000 3415 50  0000 C CNN
F 1 "MP1584EB" H 2000 3324 50  0000 C CNN
F 2 "ComponentsEvo:MP1584EN" H 2000 2700 50  0001 C CNN
F 3 "" H 2000 2700 50  0001 C CNN
	1    2000 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C?
U 1 1 62AB6FDF
P 2900 3050
F 0 "C?" H 3018 3096 50  0000 L CNN
F 1 "470uF" H 3018 3005 50  0000 L CNN
F 2 "" H 2938 2900 50  0001 C CNN
F 3 "~" H 2900 3050 50  0001 C CNN
	1    2900 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2650 2950 2700 2950
Wire Wire Line
	2700 2950 2700 2900
Wire Wire Line
	2700 2900 2900 2900
Wire Wire Line
	2650 3150 2700 3150
Wire Wire Line
	2700 3150 2700 3200
Wire Wire Line
	2700 3200 2900 3200
$Comp
L power:GND #PWR?
U 1 1 62AB9BE4
P 2900 3200
F 0 "#PWR?" H 2900 2950 50  0001 C CNN
F 1 "GND" H 2905 3027 50  0000 C CNN
F 2 "" H 2900 3200 50  0001 C CNN
F 3 "" H 2900 3200 50  0001 C CNN
	1    2900 3200
	1    0    0    -1  
$EndComp
Connection ~ 2900 3200
Wire Wire Line
	1300 2950 1350 2950
$Comp
L power:GND #PWR?
U 1 1 62ABBBC9
P 1300 3150
F 0 "#PWR?" H 1300 2900 50  0001 C CNN
F 1 "GND" H 1305 2977 50  0000 C CNN
F 2 "" H 1300 3150 50  0001 C CNN
F 3 "" H 1300 3150 50  0001 C CNN
	1    1300 3150
	1    0    0    -1  
$EndComp
$Comp
L power:VCC #PWR?
U 1 1 62ABD2C1
P 1300 2950
F 0 "#PWR?" H 1300 2800 50  0001 C CNN
F 1 "VCC" H 1315 3123 50  0000 C CNN
F 2 "" H 1300 2950 50  0001 C CNN
F 3 "" H 1300 2950 50  0001 C CNN
	1    1300 2950
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 62ABDF40
P 4000 2650
F 0 "#PWR?" H 4000 2500 50  0001 C CNN
F 1 "+5V" H 4015 2823 50  0000 C CNN
F 2 "" H 4000 2650 50  0001 C CNN
F 3 "" H 4000 2650 50  0001 C CNN
	1    4000 2650
	1    0    0    -1  
$EndComp
NoConn ~ 4850 2900
NoConn ~ 4950 2900
$Comp
L Device:C C?
U 1 1 62AC03F4
P 4000 2800
F 0 "C?" H 4115 2846 50  0000 L CNN
F 1 "4.7uF" H 4115 2755 50  0000 L CNN
F 2 "" H 4038 2650 50  0001 C CNN
F 3 "~" H 4000 2800 50  0001 C CNN
	1    4000 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 2650 4650 2650
Connection ~ 4000 2650
$Comp
L power:GND #PWR?
U 1 1 62AC0ECD
P 4000 2950
F 0 "#PWR?" H 4000 2700 50  0001 C CNN
F 1 "GND" H 4005 2777 50  0000 C CNN
F 2 "" H 4000 2950 50  0001 C CNN
F 3 "" H 4000 2950 50  0001 C CNN
	1    4000 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4650 2650 4650 2900
Text Label 3750 3300 0    50   ~ 0
RX_ARDUINO
Wire Wire Line
	3750 3300 4250 3300
Text Label 3750 3400 0    50   ~ 0
TX_ARDUINO
Wire Wire Line
	3750 3400 4250 3400
$Comp
L Device:Q_NMOS_GSD Q?
U 1 1 62AC54DD
P 7800 3250
F 0 "Q?" V 8049 3250 50  0000 C CNN
F 1 "Q_NMOS_GSD" V 8140 3250 50  0000 C CNN
F 2 "" H 8000 3350 50  0001 C CNN
F 3 "~" H 7800 3250 50  0001 C CNN
	1    7800 3250
	0    -1   1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 62AC60F0
P 7350 3200
F 0 "R?" H 7420 3246 50  0000 L CNN
F 1 "10K" H 7420 3155 50  0000 L CNN
F 2 "" V 7280 3200 50  0001 C CNN
F 3 "~" H 7350 3200 50  0001 C CNN
	1    7350 3200
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 62AC6BB6
P 7350 3050
F 0 "#PWR?" H 7350 2900 50  0001 C CNN
F 1 "+5V" H 7365 3223 50  0000 C CNN
F 2 "" H 7350 3050 50  0001 C CNN
F 3 "" H 7350 3050 50  0001 C CNN
	1    7350 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	7600 3350 7350 3350
Connection ~ 7350 3350
Wire Wire Line
	7350 3350 6800 3350
Text Label 6800 3350 0    50   ~ 0
RX_ARDUINO
$Comp
L Device:R R?
U 1 1 62AC7E0E
P 8100 3200
F 0 "R?" H 8170 3246 50  0000 L CNN
F 1 "10K" H 8170 3155 50  0000 L CNN
F 2 "" V 8030 3200 50  0001 C CNN
F 3 "~" H 8100 3200 50  0001 C CNN
	1    8100 3200
	1    0    0    -1  
$EndComp
Wire Wire Line
	7800 3050 8100 3050
Wire Wire Line
	8000 3350 8100 3350
$Comp
L power:+3.3V #PWR?
U 1 1 62AC9A6C
P 8100 3050
F 0 "#PWR?" H 8100 2900 50  0001 C CNN
F 1 "+3.3V" H 8115 3223 50  0000 C CNN
F 2 "" H 8100 3050 50  0001 C CNN
F 3 "" H 8100 3050 50  0001 C CNN
	1    8100 3050
	1    0    0    -1  
$EndComp
Connection ~ 8100 3050
Wire Wire Line
	8100 3350 8750 3350
Connection ~ 8100 3350
Text Label 8750 3350 2    50   ~ 0
RX_RASPY
$Comp
L Device:Q_NMOS_GSD Q?
U 1 1 62ACAB0E
P 7800 4050
F 0 "Q?" V 8049 4050 50  0000 C CNN
F 1 "Q_NMOS_GSD" V 8140 4050 50  0000 C CNN
F 2 "" H 8000 4150 50  0001 C CNN
F 3 "~" H 7800 4050 50  0001 C CNN
	1    7800 4050
	0    -1   1    0   
$EndComp
$Comp
L Device:R R?
U 1 1 62ACAB18
P 7350 4000
F 0 "R?" H 7420 4046 50  0000 L CNN
F 1 "10K" H 7420 3955 50  0000 L CNN
F 2 "" V 7280 4000 50  0001 C CNN
F 3 "~" H 7350 4000 50  0001 C CNN
	1    7350 4000
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 62ACAB22
P 7350 3850
F 0 "#PWR?" H 7350 3700 50  0001 C CNN
F 1 "+5V" H 7365 4023 50  0000 C CNN
F 2 "" H 7350 3850 50  0001 C CNN
F 3 "" H 7350 3850 50  0001 C CNN
	1    7350 3850
	1    0    0    -1  
$EndComp
Wire Wire Line
	7600 4150 7350 4150
Connection ~ 7350 4150
Wire Wire Line
	7350 4150 6800 4150
Text Label 6800 4150 0    50   ~ 0
TX_ARDUINO
$Comp
L Device:R R?
U 1 1 62ACAB30
P 8100 4000
F 0 "R?" H 8170 4046 50  0000 L CNN
F 1 "10K" H 8170 3955 50  0000 L CNN
F 2 "" V 8030 4000 50  0001 C CNN
F 3 "~" H 8100 4000 50  0001 C CNN
	1    8100 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	7800 3850 8100 3850
Wire Wire Line
	8000 4150 8100 4150
$Comp
L power:+3.3V #PWR?
U 1 1 62ACAB3C
P 8100 3850
F 0 "#PWR?" H 8100 3700 50  0001 C CNN
F 1 "+3.3V" H 8115 4023 50  0000 C CNN
F 2 "" H 8100 3850 50  0001 C CNN
F 3 "" H 8100 3850 50  0001 C CNN
	1    8100 3850
	1    0    0    -1  
$EndComp
Connection ~ 8100 3850
Wire Wire Line
	8100 4150 8750 4150
Connection ~ 8100 4150
Text Label 8750 4150 2    50   ~ 0
TX_RASPY
$Comp
L Device:LED D?
U 1 1 62ACDCC6
P 7350 1550
F 0 "D?" V 7389 1432 50  0000 R CNN
F 1 "GREEN" V 7298 1432 50  0000 R CNN
F 2 "" H 7350 1550 50  0001 C CNN
F 3 "~" H 7350 1550 50  0001 C CNN
	1    7350 1550
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 62ACDCEE
P 7350 1850
F 0 "R?" H 7420 1896 50  0000 L CNN
F 1 "1K" H 7420 1805 50  0000 L CNN
F 2 "" V 7280 1850 50  0001 C CNN
F 3 "~" H 7350 1850 50  0001 C CNN
	1    7350 1850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62ACDCF8
P 7350 2000
F 0 "#PWR?" H 7350 1750 50  0001 C CNN
F 1 "GND" H 7355 1827 50  0000 C CNN
F 2 "" H 7350 2000 50  0001 C CNN
F 3 "" H 7350 2000 50  0001 C CNN
	1    7350 2000
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D?
U 1 1 62ACF623
P 7850 1550
F 0 "D?" V 7889 1432 50  0000 R CNN
F 1 "GREEN" V 7798 1432 50  0000 R CNN
F 2 "" H 7850 1550 50  0001 C CNN
F 3 "~" H 7850 1550 50  0001 C CNN
	1    7850 1550
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R?
U 1 1 62ACF64B
P 7850 1850
F 0 "R?" H 7920 1896 50  0000 L CNN
F 1 "1K" H 7920 1805 50  0000 L CNN
F 2 "" V 7780 1850 50  0001 C CNN
F 3 "~" H 7850 1850 50  0001 C CNN
	1    7850 1850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62ACF655
P 7850 2000
F 0 "#PWR?" H 7850 1750 50  0001 C CNN
F 1 "GND" H 7855 1827 50  0000 C CNN
F 2 "" H 7850 2000 50  0001 C CNN
F 3 "" H 7850 2000 50  0001 C CNN
	1    7850 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	7350 750  7350 1400
Wire Wire Line
	7850 1400 7850 750 
Text Label 3600 3500 0    50   ~ 0
STATUS_ARDUINO
Wire Wire Line
	3600 3500 4250 3500
Text Label 7350 750  3    50   ~ 0
STATUS_ARDUINO
Text Label 7850 750  3    50   ~ 0
STATUS_RASPY
$Comp
L ComponentsEvo:TB67H451FNG U?
U 1 1 62AD884E
P 2600 5650
F 0 "U?" H 2600 5235 50  0000 C CNN
F 1 "TB67H451FNG" H 2600 5326 50  0000 C CNN
F 2 "Package_SO:HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm_ThermalVias" H 2000 4800 50  0001 C CNN
F 3 "" H 2000 4800 50  0001 C CNN
	1    2600 5650
	1    0    0    1   
$EndComp
$Comp
L Connector:Conn_01x02_Male DIRECT
U 1 1 62AD9575
P 3500 5600
F 0 "DIRECT" H 3472 5574 50  0000 R CNN
F 1 "JST PH 2" H 3472 5483 50  0000 R CNN
F 2 "" H 3500 5600 50  0001 C CNN
F 3 "~" H 3500 5600 50  0001 C CNN
	1    3500 5600
	-1   0    0    -1  
$EndComp
Text Label 1700 5600 0    50   ~ 0
PWM1_DIRECT
Text Label 1700 5700 0    50   ~ 0
PWM2_DIRECT
Wire Wire Line
	1700 5700 2250 5700
Wire Wire Line
	1700 5600 2250 5600
Wire Wire Line
	3300 5600 2950 5600
Wire Wire Line
	2950 5800 3150 5800
Wire Wire Line
	3150 5800 3150 5700
Wire Wire Line
	3150 5700 3300 5700
$Comp
L Device:C C?
U 1 1 62AE5B2A
P 4050 5700
F 0 "C?" H 4165 5746 50  0000 L CNN
F 1 "4.7uF" H 4165 5655 50  0000 L CNN
F 2 "" H 4088 5550 50  0001 C CNN
F 3 "~" H 4050 5700 50  0001 C CNN
	1    4050 5700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62AE8CCE
P 4050 5900
F 0 "#PWR?" H 4050 5650 50  0001 C CNN
F 1 "GND" H 4055 5727 50  0000 C CNN
F 2 "" H 4050 5900 50  0001 C CNN
F 3 "" H 4050 5900 50  0001 C CNN
	1    4050 5900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 5850 4050 5900
Wire Wire Line
	4050 5550 4050 5500
$Comp
L power:VCC #PWR?
U 1 1 62AF0F5A
P 4050 5500
F 0 "#PWR?" H 4050 5350 50  0001 C CNN
F 1 "VCC" H 4065 5673 50  0000 C CNN
F 2 "" H 4050 5500 50  0001 C CNN
F 3 "" H 4050 5500 50  0001 C CNN
	1    4050 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 5500 4050 5500
Connection ~ 4050 5500
$Comp
L power:GND #PWR?
U 1 1 62AF5527
P 1550 5800
F 0 "#PWR?" H 1550 5550 50  0001 C CNN
F 1 "GND" H 1555 5627 50  0000 C CNN
F 2 "" H 1550 5800 50  0001 C CNN
F 3 "" H 1550 5800 50  0001 C CNN
	1    1550 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 3150 1300 3150
Wire Wire Line
	1450 2050 1550 2050
$Comp
L power:+BATT #PWR?
U 1 1 62ABA76F
P 2700 900
F 0 "#PWR?" H 2700 750 50  0001 C CNN
F 1 "+BATT" H 2715 1073 50  0000 C CNN
F 2 "" H 2700 900 50  0001 C CNN
F 3 "" H 2700 900 50  0001 C CNN
	1    2700 900 
	1    0    0    -1  
$EndComp
Wire Wire Line
	1450 2150 1550 2150
Text Label 1700 1500 0    50   ~ 0
ON
NoConn ~ 5250 3700
Text Label 5800 3900 2    50   ~ 0
LIMIT_DIRECT
Text Label 5800 4000 2    50   ~ 0
LIMIT_PROP
Wire Wire Line
	5250 3900 5800 3900
Wire Wire Line
	5250 4000 5800 4000
$Comp
L Device:R R?
U 1 1 62AD78F2
P 1550 5350
F 0 "R?" H 1620 5396 50  0000 L CNN
F 1 "150" H 1620 5305 50  0000 L CNN
F 2 "" V 1480 5350 50  0001 C CNN
F 3 "~" H 1550 5350 50  0001 C CNN
	1    1550 5350
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 62AD7ECD
P 1550 5650
F 0 "R?" H 1620 5696 50  0000 L CNN
F 1 "510" H 1620 5605 50  0000 L CNN
F 2 "" V 1480 5650 50  0001 C CNN
F 3 "~" H 1550 5650 50  0001 C CNN
	1    1550 5650
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1550 5500 2250 5500
Connection ~ 1550 5500
Text Label 950  5200 0    50   ~ 0
LIMIT_DIRECT
Wire Wire Line
	1550 5200 950  5200
Wire Wire Line
	1550 5800 2250 5800
Connection ~ 1550 5800
Text Label 3700 3800 0    50   ~ 0
PWM1_DIRECT
Text Label 3700 3900 0    50   ~ 0
PWM2_DIRECT
Wire Wire Line
	3700 3900 4250 3900
Wire Wire Line
	3700 3800 4250 3800
Text Label 3700 4200 0    50   ~ 0
PWM1_PROP
Text Label 3700 4300 0    50   ~ 0
PWM2_PROP
Wire Wire Line
	3700 4300 4250 4300
Wire Wire Line
	3700 4200 4250 4200
$Comp
L ComponentsEvo:TB67H451FNG U?
U 1 1 62AE659A
P 2600 6800
F 0 "U?" H 2600 6385 50  0000 C CNN
F 1 "TB67H451FNG" H 2600 6476 50  0000 C CNN
F 2 "Package_SO:HSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.1mm_ThermalVias" H 2000 5950 50  0001 C CNN
F 3 "" H 2000 5950 50  0001 C CNN
	1    2600 6800
	1    0    0    1   
$EndComp
$Comp
L Connector:Conn_01x02_Male PROP
U 1 1 62AE65A4
P 3500 6750
F 0 "PROP" H 3472 6724 50  0000 R CNN
F 1 "JST PH 2" H 3472 6633 50  0000 R CNN
F 2 "" H 3500 6750 50  0001 C CNN
F 3 "~" H 3500 6750 50  0001 C CNN
	1    3500 6750
	-1   0    0    -1  
$EndComp
Text Label 1700 6750 0    50   ~ 0
PWM1_PROP
Text Label 1700 6850 0    50   ~ 0
PWM2_PROP
Wire Wire Line
	1700 6850 2250 6850
Wire Wire Line
	1700 6750 2250 6750
Wire Wire Line
	3300 6750 2950 6750
Wire Wire Line
	2950 6950 3150 6950
Wire Wire Line
	3150 6950 3150 6850
Wire Wire Line
	3150 6850 3300 6850
$Comp
L Device:C C?
U 1 1 62AE65B6
P 4050 6850
F 0 "C?" H 4165 6896 50  0000 L CNN
F 1 "4.7uF" H 4165 6805 50  0000 L CNN
F 2 "" H 4088 6700 50  0001 C CNN
F 3 "~" H 4050 6850 50  0001 C CNN
	1    4050 6850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 62AE65C0
P 4050 7050
F 0 "#PWR?" H 4050 6800 50  0001 C CNN
F 1 "GND" H 4055 6877 50  0000 C CNN
F 2 "" H 4050 7050 50  0001 C CNN
F 3 "" H 4050 7050 50  0001 C CNN
	1    4050 7050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 7000 4050 7050
Wire Wire Line
	4050 6700 4050 6650
$Comp
L power:VCC #PWR?
U 1 1 62AE65CC
P 4050 6650
F 0 "#PWR?" H 4050 6500 50  0001 C CNN
F 1 "VCC" H 4065 6823 50  0000 C CNN
F 2 "" H 4050 6650 50  0001 C CNN
F 3 "" H 4050 6650 50  0001 C CNN
	1    4050 6650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2950 6650 4050 6650
Connection ~ 4050 6650
$Comp
L power:GND #PWR?
U 1 1 62AE65D8
P 1550 6950
F 0 "#PWR?" H 1550 6700 50  0001 C CNN
F 1 "GND" H 1555 6777 50  0000 C CNN
F 2 "" H 1550 6950 50  0001 C CNN
F 3 "" H 1550 6950 50  0001 C CNN
	1    1550 6950
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 62AE65E2
P 1550 6500
F 0 "R?" H 1620 6546 50  0000 L CNN
F 1 "150" H 1620 6455 50  0000 L CNN
F 2 "" V 1480 6500 50  0001 C CNN
F 3 "~" H 1550 6500 50  0001 C CNN
	1    1550 6500
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 62AE65EC
P 1550 6800
F 0 "R?" H 1620 6846 50  0000 L CNN
F 1 "510" H 1620 6755 50  0000 L CNN
F 2 "" V 1480 6800 50  0001 C CNN
F 3 "~" H 1550 6800 50  0001 C CNN
	1    1550 6800
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1550 6650 2250 6650
Connection ~ 1550 6650
Text Label 950  6350 0    50   ~ 0
LIMIT_PROP
Wire Wire Line
	1550 6350 950  6350
Wire Wire Line
	1550 6950 2250 6950
Connection ~ 1550 6950
$Comp
L Connector:Conn_01x03_Male LEDS_RING
U 1 1 62AEFC6A
P 9100 5300
F 0 "LEDS_RING" H 9050 5350 50  0000 R CNN
F 1 "JST PA 3" H 9050 5250 50  0000 R CNN
F 2 "" H 9100 5300 50  0001 C CNN
F 3 "~" H 9100 5300 50  0001 C CNN
	1    9100 5300
	-1   0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 62AF2001
P 8200 5300
F 0 "C?" H 8315 5346 50  0000 L CNN
F 1 "4.7uF" H 8315 5255 50  0000 L CNN
F 2 "" H 8238 5150 50  0001 C CNN
F 3 "~" H 8200 5300 50  0001 C CNN
	1    8200 5300
	-1   0    0    -1  
$EndComp
Text Label 8350 5300 0    50   ~ 0
LEDS_RING
Wire Wire Line
	8350 5300 8900 5300
Wire Wire Line
	8900 5200 8550 5200
Wire Wire Line
	8550 5200 8550 5150
Wire Wire Line
	8550 5150 8200 5150
Wire Wire Line
	8200 5450 8550 5450
Wire Wire Line
	8550 5450 8550 5400
Wire Wire Line
	8550 5400 8900 5400
$Comp
L power:+5V #PWR?
U 1 1 62AFA5C3
P 8200 5150
F 0 "#PWR?" H 8200 5000 50  0001 C CNN
F 1 "+5V" H 8215 5323 50  0000 C CNN
F 2 "" H 8200 5150 50  0001 C CNN
F 3 "" H 8200 5150 50  0001 C CNN
	1    8200 5150
	1    0    0    -1  
$EndComp
Connection ~ 8200 5150
$Comp
L power:GND #PWR?
U 1 1 62AFAB65
P 8200 5450
F 0 "#PWR?" H 8200 5200 50  0001 C CNN
F 1 "GND" H 8205 5277 50  0000 C CNN
F 2 "" H 8200 5450 50  0001 C CNN
F 3 "" H 8200 5450 50  0001 C CNN
	1    8200 5450
	1    0    0    -1  
$EndComp
Connection ~ 8200 5450
Text Label 3750 3600 0    50   ~ 0
LEDS_RING
Wire Wire Line
	4250 3600 3750 3600
$Comp
L Connector:Conn_01x04_Male SONAR
U 1 1 62B08E8E
P 6250 5950
F 0 "SONAR" H 6222 5924 50  0000 R CNN
F 1 "JST PA 4" H 6222 5833 50  0000 R CNN
F 2 "" H 6250 5950 50  0001 C CNN
F 3 "~" H 6250 5950 50  0001 C CNN
	1    6250 5950
	-1   0    0    -1  
$EndComp
$Comp
L power:+5V #PWR?
U 1 1 62B0A2E5
P 5950 5850
F 0 "#PWR?" H 5950 5700 50  0001 C CNN
F 1 "+5V" H 5965 6023 50  0000 C CNN
F 2 "" H 5950 5850 50  0001 C CNN
F 3 "" H 5950 5850 50  0001 C CNN
	1    5950 5850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 5850 6050 5850
Wire Wire Line
	6050 6150 5950 6150
$Comp
L power:GND #PWR?
U 1 1 62B0F696
P 5950 6150
F 0 "#PWR?" H 5950 5900 50  0001 C CNN
F 1 "GND" H 5955 5977 50  0000 C CNN
F 2 "" H 5950 6150 50  0001 C CNN
F 3 "" H 5950 6150 50  0001 C CNN
	1    5950 6150
	1    0    0    -1  
$EndComp
Text Label 5450 6050 0    50   ~ 0
ECHO_SONAR
Text Label 5450 5950 0    50   ~ 0
TRIGGER_SONAR
Wire Wire Line
	5450 6050 6050 6050
Wire Wire Line
	5450 5950 6050 5950
$Comp
L Device:CP C?
U 1 1 62B24166
P 2700 1050
F 0 "C?" H 2818 1096 50  0000 L CNN
F 1 "470uF" H 2818 1005 50  0000 L CNN
F 2 "" H 2738 900 50  0001 C CNN
F 3 "~" H 2700 1050 50  0001 C CNN
	1    2700 1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2600 1200 2700 1200
Connection ~ 2700 1200
Wire Wire Line
	2100 1500 2400 1500
Wire Wire Line
	2200 1200 2100 1200
Wire Wire Line
	2100 900  2700 900 
Connection ~ 2700 900 
Wire Wire Line
	2100 1200 1750 1200
Wire Wire Line
	1750 1200 1750 1000
Wire Wire Line
	1750 1000 1700 1000
Connection ~ 2100 1200
Wire Wire Line
	2100 1500 1700 1500
Connection ~ 2100 1500
$Comp
L Device:R R?
U 1 1 62B4621C
P 6050 4250
F 0 "R?" H 6120 4296 50  0000 L CNN
F 1 "10K" H 6120 4205 50  0000 L CNN
F 2 "" V 5980 4250 50  0001 C CNN
F 3 "~" H 6050 4250 50  0001 C CNN
	1    6050 4250
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 62B46C6C
P 6050 3950
F 0 "R?" H 6120 3996 50  0000 L CNN
F 1 "10K" H 6120 3905 50  0000 L CNN
F 2 "" V 5980 3950 50  0001 C CNN
F 3 "~" H 6050 3950 50  0001 C CNN
	1    6050 3950
	1    0    0    -1  
$EndComp
$Comp
L power:+BATT #PWR?
U 1 1 62B4BC62
P 6050 3800
F 0 "#PWR?" H 6050 3650 50  0001 C CNN
F 1 "+BATT" H 6065 3973 50  0000 C CNN
F 2 "" H 6050 3800 50  0001 C CNN
F 3 "" H 6050 3800 50  0001 C CNN
	1    6050 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 4100 5250 4100
Connection ~ 6050 4100
$Comp
L power:GND #PWR?
U 1 1 62B4EE6B
P 6050 4400
F 0 "#PWR?" H 6050 4150 50  0001 C CNN
F 1 "GND" H 6055 4227 50  0000 C CNN
F 2 "" H 6050 4400 50  0001 C CNN
F 3 "" H 6050 4400 50  0001 C CNN
	1    6050 4400
	1    0    0    -1  
$EndComp
$EndSCHEMATC
