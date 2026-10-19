MC-MT-SRMT benchmark
--------------------
Cases          : ['spheroid', 'torus', 'gaussian_two']
Methods        : ['MC', 'MT', 'SRMT']
Resolutions    : [64, 128, 192, 256, 320, 384, 448, 512]
SRMT workers   : [1, 2, 4, 8]
SRMT modes     : ['default', 'uniform']
SRMT start     : fork
Levels         : [0.5]
Repeats        : 5
Summary        : median
Protocol       : CPC-1.2-THREE-STATE-MEDIAN5
Run order      : fixed deterministic method order in every repeat
Adjustments    : none (raw measurements; median of exactly five repeats)
Full diagnostics: True
Resume results  : True
Save meshes    : False (explicit option; outside timing)
Save scalars   : False
Data range     : [0,1]
Processes      : MC=1, MT=1; SRMT P denotes n_jobs worker count
Native threads : one per benchmark process
Peak RSS       : summed process-tree RSS sampled externally during extraction
Gaussian ref   : projected continuous-implicit reference mesh
Render grid    : 128^3
Output         : /home/yaox/YXTmp/srmt_benchmark_v18/data_mc_mt_srmt

Large-resolution notes
----------------------
MT 64^3: 1,500,282 tetrahedra; 64-bit core-array estimate ~= 0.1 GiB
MT 128^3: 12,290,298 tetrahedra; 64-bit core-array estimate ~= 0.5 GiB
MT 192^3: 41,807,226 tetrahedra; 64-bit core-array estimate ~= 1.8 GiB
MT 256^3: 99,488,250 tetrahedra; 64-bit core-array estimate ~= 4.3 GiB
MT 320^3: 194,770,554 tetrahedra; 64-bit core-array estimate ~= 8.4 GiB
           warning: explicit MT is entering a memory-dominated regime; runtime can increase nonlinearly when available physical RAM becomes constrained.
MT 384^3: 337,091,322 tetrahedra; 64-bit core-array estimate ~= 14.6 GiB
           warning: explicit MT is entering a memory-dominated regime; runtime can increase nonlinearly when available physical RAM becomes constrained.
MT 448^3: 535,887,738 tetrahedra; 64-bit core-array estimate ~= 23.1 GiB
           warning: explicit MT is entering a memory-dominated regime; runtime can increase nonlinearly when available physical RAM becomes constrained.
MT 512^3: 800,596,986 tetrahedra; 64-bit core-array estimate ~= 34.6 GiB
           warning: explicit MT is entering a memory-dominated regime; runtime can increase nonlinearly when available physical RAM becomes constrained.

====================================================================================
Running SPHEROID  MC  level=0.5  at 64^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.005606200 s, Peak RSS=46.609 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 64^3 with 1 process  repeat=1/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.083103224 s, Peak RSS=293.664 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.151666478 s, Peak RSS=75.883 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.117648318 s, Peak RSS=171.184 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.084532136 s, Peak RSS=266.355 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.074766643 s, Peak RSS=432.441 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.146359637 s, Peak RSS=76.406 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.110106945 s, Peak RSS=176.324 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.085825557 s, Peak RSS=265.004 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.080022487 s, Peak RSS=430.137 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 128^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.018733515 s, Peak RSS=69.477 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 128^3 with 1 process  repeat=1/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.330577665 s, Peak RSS=859.719 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.629227875 s, Peak RSS=150.898 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.419029279 s, Peak RSS=340.004 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.275625782 s, Peak RSS=498.074 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.233467377 s, Peak RSS=730.238 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.620410612 s, Peak RSS=149.117 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.405871803 s, Peak RSS=339.750 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.273259221 s, Peak RSS=500.727 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.224790035 s, Peak RSS=732.043 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 192^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.058645911 s, Peak RSS=127.551 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 192^3 with 1 process  repeat=1/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.074248346 s, Peak RSS=2417.422 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.573287467 s, Peak RSS=272.789 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.056893577 s, Peak RSS=527.477 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.745489099 s, Peak RSS=767.895 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.651609667 s, Peak RSS=1191.801 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.561759022 s, Peak RSS=275.000 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.051440788 s, Peak RSS=551.102 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.769686526 s, Peak RSS=745.113 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.647591319 s, Peak RSS=1205.258 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 256^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.129876552 s, Peak RSS=248.223 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 256^3 with 1 process  repeat=1/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.678147794 s, Peak RSS=5453.742 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=3.021465987 s, Peak RSS=487.977 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.072598298 s, Peak RSS=981.125 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.492921024 s, Peak RSS=1382.477 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.231776944 s, Peak RSS=2165.953 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=2.979200147 s, Peak RSS=488.020 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.071657534 s, Peak RSS=981.969 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.487103751 s, Peak RSS=1378.586 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.252346996 s, Peak RSS=2147.484 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 320^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.247212109 s, Peak RSS=430.227 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 320^3 with 1 process  repeat=1/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.173001008 s, Peak RSS=10468.926 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=5.009846117 s, Peak RSS=773.699 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.585464430 s, Peak RSS=1702.676 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.665787293 s, Peak RSS=2228.281 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.218110147 s, Peak RSS=3523.305 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=4.934206360 s, Peak RSS=773.883 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.430066832 s, Peak RSS=1702.922 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.616909760 s, Peak RSS=2303.363 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.197140954 s, Peak RSS=3524.859 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 384^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.417347612 s, Peak RSS=712.664 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 384^3 with 1 process  repeat=1/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.029363202 s, Peak RSS=17963.102 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=8.150698958 s, Peak RSS=1172.285 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.707137447 s, Peak RSS=2378.102 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.408414088 s, Peak RSS=3439.234 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.865969903 s, Peak RSS=5341.684 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=8.023212579 s, Peak RSS=1172.094 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.653581525 s, Peak RSS=2371.961 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.391012307 s, Peak RSS=3343.859 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.873249066 s, Peak RSS=5360.355 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 448^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.652849343 s, Peak RSS=1111.238 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 448^3 with 1 process  repeat=1/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.275810898 s, Peak RSS=28425.867 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=12.051774202 s, Peak RSS=1661.617 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.632763577 s, Peak RSS=3469.789 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=6.814152765 s, Peak RSS=5147.672 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.976086656 s, Peak RSS=7955.828 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=11.995241308 s, Peak RSS=1661.785 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.478814034 s, Peak RSS=3452.449 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=6.823098405 s, Peak RSS=4961.734 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.971965040 s, Peak RSS=8132.098 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 512^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.962989459 s, Peak RSS=1619.367 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 512^3 with 1 process  repeat=1/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.401293001 s, Peak RSS=42358.355 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=16.950578678 s, Peak RSS=2324.406 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=12.367026157 s, Peak RSS=4930.812 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.979997080 s, Peak RSS=7253.770 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.882270643 s, Peak RSS=11706.930 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=16.777007780 s, Peak RSS=2324.395 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=12.211996954 s, Peak RSS=4931.012 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.956559210 s, Peak RSS=7243.012 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.858498103 s, Peak RSS=11514.848 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 64^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.006612738 s, Peak RSS=48.754 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 64^3 with 1 process  repeat=1/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.062101709 s, Peak RSS=301.914 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.478860698 s, Peak RSS=112.500 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.314113546 s, Peak RSS=207.773 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.198758263 s, Peak RSS=319.840 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.165456665 s, Peak RSS=529.277 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.458666858 s, Peak RSS=113.012 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.312228859 s, Peak RSS=225.633 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.199248498 s, Peak RSS=327.207 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.158176978 s, Peak RSS=520.430 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 128^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.030262725 s, Peak RSS=76.906 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 128^3 with 1 process  repeat=1/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.370207957 s, Peak RSS=882.758 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.953345329 s, Peak RSS=300.062 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.196058206 s, Peak RSS=516.406 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.797839291 s, Peak RSS=707.953 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.598432350 s, Peak RSS=1035.293 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.866692745 s, Peak RSS=300.258 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.176820954 s, Peak RSS=560.684 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.763743350 s, Peak RSS=739.480 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.601338867 s, Peak RSS=1041.500 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 192^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.085023839 s, Peak RSS=135.957 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 192^3 with 1 process  repeat=1/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.177615094 s, Peak RSS=2448.773 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=4.685694671 s, Peak RSS=620.727 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.981228520 s, Peak RSS=940.184 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.012786869 s, Peak RSS=1248.027 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.566974191 s, Peak RSS=1630.152 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=4.610196646 s, Peak RSS=620.609 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.953495145 s, Peak RSS=926.418 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.953699117 s, Peak RSS=1149.000 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.562332322 s, Peak RSS=1681.016 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 256^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.176913866 s, Peak RSS=273.582 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 256^3 with 1 process  repeat=1/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.861477543 s, Peak RSS=5455.020 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=9.345411151 s, Peak RSS=1105.582 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.846141162 s, Peak RSS=1678.031 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.140514256 s, Peak RSS=2188.574 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.294762740 s, Peak RSS=2821.691 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=9.119641656 s, Peak RSS=1105.699 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.834613144 s, Peak RSS=1706.684 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.052427545 s, Peak RSS=2216.211 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.264502079 s, Peak RSS=2815.227 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 320^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.320846083 s, Peak RSS=462.359 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 320^3 with 1 process  repeat=1/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.444310708 s, Peak RSS=10469.078 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=15.204748800 s, Peak RSS=1759.676 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.935479878 s, Peak RSS=2889.184 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.120057170 s, Peak RSS=3482.309 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.772580922 s, Peak RSS=5034.734 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=14.996192876 s, Peak RSS=1759.691 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.802795522 s, Peak RSS=2906.633 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.050998754 s, Peak RSS=3468.414 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.771946478 s, Peak RSS=4904.531 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 384^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.510784432 s, Peak RSS=776.734 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 384^3 with 1 process  repeat=1/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.529543485 s, Peak RSS=17964.945 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=22.678615625 s, Peak RSS=2573.254 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=14.933342002 s, Peak RSS=3888.102 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=10.550560216 s, Peak RSS=4919.902 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.829269691 s, Peak RSS=7199.512 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=22.070775013 s, Peak RSS=2573.578 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=14.767664438 s, Peak RSS=3889.340 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=10.436408452 s, Peak RSS=4929.066 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=8.665571360 s, Peak RSS=7242.723 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 448^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.785360916 s, Peak RSS=1169.387 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 448^3 with 1 process  repeat=1/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.742969757 s, Peak RSS=28429.020 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=31.953823738 s, Peak RSS=3609.477 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=21.599880272 s, Peak RSS=5457.129 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=15.600887282 s, Peak RSS=6828.590 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=12.726836749 s, Peak RSS=10496.156 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=31.691812526 s, Peak RSS=3609.531 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=21.286866659 s, Peak RSS=5437.566 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=15.477203064 s, Peak RSS=6825.691 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=12.897980132 s, Peak RSS=10496.117 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 512^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=1.154269883 s, Peak RSS=1701.359 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 512^3 with 1 process  repeat=1/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=22.007456346 s, Peak RSS=42358.609 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=41.887845381 s, Peak RSS=4807.016 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=28.391350758 s, Peak RSS=7447.570 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=20.799419437 s, Peak RSS=9606.797 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=17.241800295 s, Peak RSS=14702.590 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=41.191053751 s, Peak RSS=4807.211 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=28.038765057 s, Peak RSS=7447.648 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=20.609522655 s, Peak RSS=9607.172 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=16.971765079 s, Peak RSS=14662.816 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 64^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.003124798 s, Peak RSS=90.312 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 64^3 with 1 process  repeat=1/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.045113441 s, Peak RSS=334.547 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.089675429 s, Peak RSS=115.855 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.070041178 s, Peak RSS=259.586 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.055927905 s, Peak RSS=397.203 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.055914765 s, Peak RSS=682.965 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.089849855 s, Peak RSS=115.910 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.084089858 s, Peak RSS=260.195 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.055115082 s, Peak RSS=397.402 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.058432470 s, Peak RSS=685.055 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 128^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.016288515 s, Peak RSS=118.297 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 128^3 with 1 process  repeat=1/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.322698562 s, Peak RSS=922.480 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.412174859 s, Peak RSS=165.152 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.306565057 s, Peak RSS=399.426 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.185348879 s, Peak RSS=600.891 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.157432452 s, Peak RSS=1054.191 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=0.411877698 s, Peak RSS=165.922 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.336252576 s, Peak RSS=400.309 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.182555950 s, Peak RSS=601.199 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.158733194 s, Peak RSS=1054.863 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 192^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.053395917 s, Peak RSS=170.000 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 192^3 with 1 process  repeat=1/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.065325756 s, Peak RSS=2459.289 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.073893954 s, Peak RSS=253.273 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.781070234 s, Peak RSS=560.988 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.545529949 s, Peak RSS=837.996 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.468088062 s, Peak RSS=1359.004 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=1.056071734 s, Peak RSS=254.508 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.715729652 s, Peak RSS=547.062 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.546984687 s, Peak RSS=826.379 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.440912370 s, Peak RSS=1333.914 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 256^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.121213800 s, Peak RSS=284.746 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 256^3 with 1 process  repeat=1/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.656022623 s, Peak RSS=5496.469 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=2.041430183 s, Peak RSS=412.016 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.463415871 s, Peak RSS=910.184 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.127615023 s, Peak RSS=1378.105 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.012085673 s, Peak RSS=2275.027 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=2.017720465 s, Peak RSS=412.379 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.426942778 s, Peak RSS=850.352 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.105948225 s, Peak RSS=1370.332 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=0.971940642 s, Peak RSS=2288.965 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 320^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.230176691 s, Peak RSS=468.250 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 320^3 with 1 process  repeat=1/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.118698462 s, Peak RSS=10512.078 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=3.550200350 s, Peak RSS=650.953 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.576360048 s, Peak RSS=1528.289 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.014862239 s, Peak RSS=2189.742 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.772073416 s, Peak RSS=3529.383 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=3.530537283 s, Peak RSS=651.676 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.546646603 s, Peak RSS=1530.914 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.981378409 s, Peak RSS=2197.867 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=1.767150471 s, Peak RSS=3532.098 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 384^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.401167419 s, Peak RSS=746.844 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 384^3 with 1 process  repeat=1/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.363000416 s, Peak RSS=18005.762 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=5.614985842 s, Peak RSS=963.309 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.177732692 s, Peak RSS=2143.930 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.382949207 s, Peak RSS=3205.688 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.968725633 s, Peak RSS=5225.215 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=5.559203145 s, Peak RSS=964.516 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.167301807 s, Peak RSS=2144.059 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=3.349200539 s, Peak RSS=3172.473 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=2.970279021 s, Peak RSS=5269.418 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 448^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.623893424 s, Peak RSS=1132.754 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 448^3 with 1 process  repeat=1/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.143558246 s, Peak RSS=28468.434 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=8.586395900 s, Peak RSS=1395.270 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=6.578719255 s, Peak RSS=3178.422 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.379758296 s, Peak RSS=4544.469 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.837698656 s, Peak RSS=7851.664 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=8.578405224 s, Peak RSS=1396.504 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=6.442443390 s, Peak RSS=3181.539 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=5.366846504 s, Peak RSS=4723.668 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=4.847327053 s, Peak RSS=7905.156 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 512^3 with 1 process  repeat=1/5
====================================================================================
Measured runtime=0.937886523 s, Peak RSS=1647.852 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 512^3 with 1 process  repeat=1/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.368024327 s, Peak RSS=42404.711 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=12.155571330 s, Peak RSS=1898.781 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.351251883 s, Peak RSS=4415.070 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.893042221 s, Peak RSS=6762.828 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.134419585 s, Peak RSS=11217.855 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=1/5
====================================================================================
Measured runtime=11.990962890 s, Peak RSS=1900.488 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=9.258912061 s, Peak RSS=4419.703 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.835300024 s, Peak RSS=6834.750 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=1/5
====================================================================================
Measured runtime=7.115749545 s, Peak RSS=11198.336 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 64^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.003868418 s, Peak RSS=46.543 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 64^3 with 1 process  repeat=2/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.047310804 s, Peak RSS=293.918 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.147918345 s, Peak RSS=76.430 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.105161131 s, Peak RSS=168.996 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.083437351 s, Peak RSS=266.336 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.075764490 s, Peak RSS=429.484 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.145316642 s, Peak RSS=84.559 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.108203819 s, Peak RSS=172.539 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.085470413 s, Peak RSS=266.309 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.076082238 s, Peak RSS=431.027 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 128^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.019043813 s, Peak RSS=69.531 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 128^3 with 1 process  repeat=2/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.337526605 s, Peak RSS=860.398 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.637836432 s, Peak RSS=150.879 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.484884078 s, Peak RSS=340.359 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.276962819 s, Peak RSS=498.406 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.231091891 s, Peak RSS=730.180 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.632252121 s, Peak RSS=149.008 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.414012208 s, Peak RSS=339.082 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.274885765 s, Peak RSS=499.727 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.223517818 s, Peak RSS=734.551 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 192^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.059034001 s, Peak RSS=130.254 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 192^3 with 1 process  repeat=2/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.098575262 s, Peak RSS=2416.422 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=1.617987640 s, Peak RSS=272.723 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.095404867 s, Peak RSS=527.785 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.753642940 s, Peak RSS=778.430 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.623190946 s, Peak RSS=1191.309 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=1.575079353 s, Peak RSS=275.051 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.055307695 s, Peak RSS=550.535 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.749799813 s, Peak RSS=746.559 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.613785524 s, Peak RSS=1199.293 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 256^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.134032199 s, Peak RSS=240.695 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 256^3 with 1 process  repeat=2/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.738458157 s, Peak RSS=5454.102 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=3.053095607 s, Peak RSS=487.961 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.083695719 s, Peak RSS=982.078 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.499615841 s, Peak RSS=1383.551 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.298197485 s, Peak RSS=2171.504 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=3.050655749 s, Peak RSS=488.070 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.048080763 s, Peak RSS=981.867 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.484027176 s, Peak RSS=1378.602 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.268779131 s, Peak RSS=2144.531 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 320^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.251176544 s, Peak RSS=429.812 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 320^3 with 1 process  repeat=2/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.297611471 s, Peak RSS=10468.848 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=5.080987355 s, Peak RSS=773.793 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.562417528 s, Peak RSS=1702.762 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.667507113 s, Peak RSS=2227.715 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.215819477 s, Peak RSS=3522.762 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=4.998370315 s, Peak RSS=774.051 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.503781741 s, Peak RSS=1702.492 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.641871742 s, Peak RSS=2303.059 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.227718383 s, Peak RSS=3527.133 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 384^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.425283087 s, Peak RSS=710.391 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 384^3 with 1 process  repeat=2/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.220964260 s, Peak RSS=17963.047 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=8.220466156 s, Peak RSS=1172.258 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.749561037 s, Peak RSS=2377.711 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.416422271 s, Peak RSS=3437.305 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.877951306 s, Peak RSS=5351.312 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=8.114203883 s, Peak RSS=1172.273 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.728361857 s, Peak RSS=2371.426 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.406286853 s, Peak RSS=3344.816 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.817623050 s, Peak RSS=5348.051 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 448^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.673109016 s, Peak RSS=1111.180 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 448^3 with 1 process  repeat=2/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.593602989 s, Peak RSS=28425.945 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=12.098616746 s, Peak RSS=1661.668 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.626681209 s, Peak RSS=3469.594 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.884852386 s, Peak RSS=5148.449 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.107047925 s, Peak RSS=7955.176 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=12.013407811 s, Peak RSS=1661.766 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.560089647 s, Peak RSS=3453.113 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.811344924 s, Peak RSS=4942.398 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.032387759 s, Peak RSS=8084.297 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 512^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.984842243 s, Peak RSS=1629.926 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 512^3 with 1 process  repeat=2/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.568387124 s, Peak RSS=42357.996 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=17.062749208 s, Peak RSS=2324.395 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=12.446177384 s, Peak RSS=4930.715 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=10.011258534 s, Peak RSS=7254.652 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.936308185 s, Peak RSS=11692.633 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=17.018237525 s, Peak RSS=2324.434 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=12.394509917 s, Peak RSS=4931.164 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=9.953175784 s, Peak RSS=7243.570 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.904612644 s, Peak RSS=11514.852 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 64^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.006592004 s, Peak RSS=48.719 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 64^3 with 1 process  repeat=2/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.056166722 s, Peak RSS=301.820 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.474506634 s, Peak RSS=112.461 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.324776641 s, Peak RSS=211.762 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.202810694 s, Peak RSS=320.395 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.160691115 s, Peak RSS=529.027 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.473979838 s, Peak RSS=112.441 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.304767945 s, Peak RSS=225.355 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.194376067 s, Peak RSS=328.941 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.156805240 s, Peak RSS=520.793 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 128^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.030984096 s, Peak RSS=76.926 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 128^3 with 1 process  repeat=2/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.385605605 s, Peak RSS=882.984 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=2.003538613 s, Peak RSS=300.078 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.232401386 s, Peak RSS=532.941 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.807148989 s, Peak RSS=709.102 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.611688110 s, Peak RSS=1035.734 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=1.913822696 s, Peak RSS=300.191 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.206581403 s, Peak RSS=560.602 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.780175350 s, Peak RSS=737.469 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.601464015 s, Peak RSS=1041.059 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 192^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.088839854 s, Peak RSS=140.031 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 192^3 with 1 process  repeat=2/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.211575479 s, Peak RSS=2449.430 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=4.824768093 s, Peak RSS=620.707 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.028197930 s, Peak RSS=939.570 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.022891302 s, Peak RSS=1240.645 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.612761882 s, Peak RSS=1653.453 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=4.661635598 s, Peak RSS=620.465 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.960306183 s, Peak RSS=926.438 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.976479737 s, Peak RSS=1154.605 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.542696436 s, Peak RSS=1655.094 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 256^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.182262101 s, Peak RSS=273.699 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 256^3 with 1 process  repeat=2/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.899910953 s, Peak RSS=5454.848 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=9.502424854 s, Peak RSS=1105.500 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.897810833 s, Peak RSS=1678.109 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.129605617 s, Peak RSS=2188.832 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.284340565 s, Peak RSS=2820.992 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=9.556386152 s, Peak RSS=1105.707 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.851323683 s, Peak RSS=1706.168 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.084312478 s, Peak RSS=2236.145 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.260218575 s, Peak RSS=2814.469 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 320^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.331704274 s, Peak RSS=461.289 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 320^3 with 1 process  repeat=2/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.556781318 s, Peak RSS=10469.070 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=15.511420016 s, Peak RSS=1759.625 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=10.016208665 s, Peak RSS=2888.988 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.219205943 s, Peak RSS=3481.883 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.848288774 s, Peak RSS=5052.625 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=15.142713840 s, Peak RSS=1759.750 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=9.951456612 s, Peak RSS=2906.234 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.115092328 s, Peak RSS=3468.039 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.770843559 s, Peak RSS=4903.305 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 384^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.533908299 s, Peak RSS=776.488 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 384^3 with 1 process  repeat=2/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.667574455 s, Peak RSS=17965.316 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=22.796402996 s, Peak RSS=2573.199 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=15.100566066 s, Peak RSS=3888.055 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=10.679119628 s, Peak RSS=4920.328 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.758266859 s, Peak RSS=7234.160 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=22.391332663 s, Peak RSS=2573.480 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=14.856988579 s, Peak RSS=3888.730 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=10.478151519 s, Peak RSS=4928.738 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=8.671857867 s, Peak RSS=7243.453 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 448^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.806979915 s, Peak RSS=1171.309 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 448^3 with 1 process  repeat=2/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=15.421816708 s, Peak RSS=28429.121 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=32.569123530 s, Peak RSS=3609.469 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=21.758289738 s, Peak RSS=5456.988 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=15.766419076 s, Peak RSS=6828.684 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=13.044145126 s, Peak RSS=10497.340 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=32.042645492 s, Peak RSS=3609.496 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=21.472344848 s, Peak RSS=5437.316 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=15.616024944 s, Peak RSS=6832.645 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=12.987537583 s, Peak RSS=10496.418 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 512^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=1.162151473 s, Peak RSS=1703.211 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 512^3 with 1 process  repeat=2/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=22.428983380 s, Peak RSS=42358.648 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=42.037648181 s, Peak RSS=4807.043 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=28.688994891 s, Peak RSS=7447.527 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=20.899741094 s, Peak RSS=9607.230 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=17.265405464 s, Peak RSS=14703.082 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=41.709268545 s, Peak RSS=4807.305 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=28.159716520 s, Peak RSS=7447.676 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=20.752997057 s, Peak RSS=9608.125 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=17.104941886 s, Peak RSS=14661.930 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 64^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.003084659 s, Peak RSS=90.410 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 64^3 with 1 process  repeat=2/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.045008435 s, Peak RSS=334.395 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.090963180 s, Peak RSS=115.895 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.072915238 s, Peak RSS=260.953 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.061987023 s, Peak RSS=397.277 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.056751663 s, Peak RSS=684.816 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.088566824 s, Peak RSS=115.961 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.071728070 s, Peak RSS=258.484 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.054618681 s, Peak RSS=397.387 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.056192466 s, Peak RSS=684.246 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 128^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.016319747 s, Peak RSS=118.230 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 128^3 with 1 process  repeat=2/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.333056525 s, Peak RSS=923.352 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.421856399 s, Peak RSS=165.324 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.279473824 s, Peak RSS=399.168 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.191130631 s, Peak RSS=600.574 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.160433410 s, Peak RSS=1053.469 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=0.409466744 s, Peak RSS=166.496 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.278339663 s, Peak RSS=399.434 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.182276730 s, Peak RSS=599.902 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.159129446 s, Peak RSS=1057.629 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 192^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.053921613 s, Peak RSS=170.207 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 192^3 with 1 process  repeat=2/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.115127751 s, Peak RSS=2459.172 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=1.092778258 s, Peak RSS=253.199 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.746490858 s, Peak RSS=562.984 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.550078836 s, Peak RSS=853.504 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.446046252 s, Peak RSS=1349.652 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=1.064555915 s, Peak RSS=255.195 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.753977022 s, Peak RSS=575.336 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.541154079 s, Peak RSS=835.621 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.451791383 s, Peak RSS=1345.824 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 256^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.126131218 s, Peak RSS=283.879 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 256^3 with 1 process  repeat=2/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.750544799 s, Peak RSS=5496.391 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=2.103231097 s, Peak RSS=411.984 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.466933793 s, Peak RSS=942.496 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.124327437 s, Peak RSS=1373.355 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.982608964 s, Peak RSS=2254.852 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=2.036213147 s, Peak RSS=412.742 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.442402800 s, Peak RSS=904.180 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.138504261 s, Peak RSS=1339.637 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=0.963978477 s, Peak RSS=2267.375 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 320^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.241687194 s, Peak RSS=468.961 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 320^3 with 1 process  repeat=2/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.175451710 s, Peak RSS=10512.199 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=3.579321536 s, Peak RSS=651.227 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.622826539 s, Peak RSS=1436.262 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.031906447 s, Peak RSS=2188.152 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.765156322 s, Peak RSS=3530.684 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=3.540556026 s, Peak RSS=651.574 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.556647037 s, Peak RSS=1527.629 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.031777820 s, Peak RSS=2195.297 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=1.769614675 s, Peak RSS=3529.160 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 384^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.404598724 s, Peak RSS=746.512 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 384^3 with 1 process  repeat=2/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.059376628 s, Peak RSS=18005.797 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=5.654758724 s, Peak RSS=963.285 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.203138276 s, Peak RSS=2159.656 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.368047719 s, Peak RSS=3193.699 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.982153722 s, Peak RSS=5220.305 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=5.577559715 s, Peak RSS=964.305 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.160774585 s, Peak RSS=2162.027 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=3.394771387 s, Peak RSS=3249.738 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=2.981682366 s, Peak RSS=5230.098 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 448^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.634002043 s, Peak RSS=1134.336 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 448^3 with 1 process  repeat=2/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.290008085 s, Peak RSS=28468.461 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=8.634611987 s, Peak RSS=1395.406 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.665558171 s, Peak RSS=3182.207 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.398528200 s, Peak RSS=4733.516 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.847409046 s, Peak RSS=7903.988 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=8.508958381 s, Peak RSS=1396.426 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=6.490357874 s, Peak RSS=3185.516 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=5.359430050 s, Peak RSS=4730.180 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=4.833836125 s, Peak RSS=7795.402 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 512^3 with 1 process  repeat=2/5
====================================================================================
Measured runtime=0.953509516 s, Peak RSS=1648.023 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 512^3 with 1 process  repeat=2/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.391241664 s, Peak RSS=42404.809 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=12.221502239 s, Peak RSS=1898.832 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=9.439507244 s, Peak RSS=4444.914 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.901586869 s, Peak RSS=6832.762 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.168643691 s, Peak RSS=11216.785 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=2/5
====================================================================================
Measured runtime=12.027106140 s, Peak RSS=1900.625 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=9.300731104 s, Peak RSS=4418.930 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.823992356 s, Peak RSS=6716.844 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=2/5
====================================================================================
Measured runtime=7.132561460 s, Peak RSS=11212.016 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 64^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.003881174 s, Peak RSS=46.594 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 64^3 with 1 process  repeat=3/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.047641802 s, Peak RSS=293.777 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.148377979 s, Peak RSS=76.316 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.108422406 s, Peak RSS=169.281 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.078863458 s, Peak RSS=264.855 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.082207547 s, Peak RSS=433.316 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.147202914 s, Peak RSS=83.906 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.118679350 s, Peak RSS=173.754 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.088689449 s, Peak RSS=266.969 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.074367779 s, Peak RSS=430.422 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 128^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.019401170 s, Peak RSS=69.449 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 128^3 with 1 process  repeat=3/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.342746694 s, Peak RSS=860.184 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.642383862 s, Peak RSS=150.930 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.434900208 s, Peak RSS=340.551 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.277115500 s, Peak RSS=498.527 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.228481500 s, Peak RSS=729.113 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.632722912 s, Peak RSS=149.113 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.508678625 s, Peak RSS=339.566 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.275953291 s, Peak RSS=500.414 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.244227927 s, Peak RSS=734.418 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 192^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.061227294 s, Peak RSS=127.422 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 192^3 with 1 process  repeat=3/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.125949325 s, Peak RSS=2417.191 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.635967195 s, Peak RSS=272.711 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.092750591 s, Peak RSS=527.438 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.759293782 s, Peak RSS=778.254 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.638903806 s, Peak RSS=1189.371 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.591758765 s, Peak RSS=275.027 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.158710213 s, Peak RSS=551.039 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.749743965 s, Peak RSS=744.531 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.628493411 s, Peak RSS=1204.035 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 256^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.134142785 s, Peak RSS=245.652 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 256^3 with 1 process  repeat=3/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.729131152 s, Peak RSS=5454.105 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=3.126368380 s, Peak RSS=487.809 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.169701731 s, Peak RSS=982.469 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.504699682 s, Peak RSS=1383.684 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.249318355 s, Peak RSS=2168.156 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=3.030850316 s, Peak RSS=487.961 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.058487472 s, Peak RSS=981.992 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.507845502 s, Peak RSS=1379.320 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.242580760 s, Peak RSS=2140.512 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 320^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.257099080 s, Peak RSS=431.516 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 320^3 with 1 process  repeat=3/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.387486874 s, Peak RSS=10469.035 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=5.109190990 s, Peak RSS=773.723 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.518709611 s, Peak RSS=1702.828 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.662741660 s, Peak RSS=2227.801 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.224903789 s, Peak RSS=3524.203 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=5.097082729 s, Peak RSS=773.883 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.481267847 s, Peak RSS=1702.746 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.650906075 s, Peak RSS=2303.656 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.295999289 s, Peak RSS=3524.973 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 384^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.432748351 s, Peak RSS=713.688 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 384^3 with 1 process  repeat=3/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.281642449 s, Peak RSS=17962.934 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=8.189940239 s, Peak RSS=1172.211 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.861289369 s, Peak RSS=2371.895 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.515228272 s, Peak RSS=3437.961 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.846871267 s, Peak RSS=5350.359 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=8.086796357 s, Peak RSS=1172.293 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.745741653 s, Peak RSS=2371.871 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.449227284 s, Peak RSS=3344.383 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.836695004 s, Peak RSS=5349.316 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 448^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.672147961 s, Peak RSS=1101.301 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 448^3 with 1 process  repeat=3/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.615420282 s, Peak RSS=28425.895 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=12.192088108 s, Peak RSS=1661.562 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.654218414 s, Peak RSS=3469.285 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.862204991 s, Peak RSS=5149.488 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.098906810 s, Peak RSS=7975.570 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=12.011531029 s, Peak RSS=1661.676 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.621165688 s, Peak RSS=3452.754 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.817298038 s, Peak RSS=4960.980 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.068010535 s, Peak RSS=8148.910 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 512^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.975904566 s, Peak RSS=1629.965 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 512^3 with 1 process  repeat=3/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.828996391 s, Peak RSS=42358.145 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=17.078659484 s, Peak RSS=2324.363 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=12.448611014 s, Peak RSS=4930.801 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=10.013390039 s, Peak RSS=7254.840 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.874758503 s, Peak RSS=11705.961 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=16.934444864 s, Peak RSS=2324.379 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=12.323255820 s, Peak RSS=4930.688 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=10.006704600 s, Peak RSS=7242.836 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.868029783 s, Peak RSS=11515.152 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 64^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.006655249 s, Peak RSS=48.836 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 64^3 with 1 process  repeat=3/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.058413433 s, Peak RSS=301.820 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.481549446 s, Peak RSS=112.492 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.305954987 s, Peak RSS=208.316 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.203802562 s, Peak RSS=318.262 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.160191359 s, Peak RSS=528.121 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.473309427 s, Peak RSS=112.445 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.305320835 s, Peak RSS=224.266 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.204784686 s, Peak RSS=327.438 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.155887024 s, Peak RSS=522.988 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 128^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.032329284 s, Peak RSS=76.840 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 128^3 with 1 process  repeat=3/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.379740619 s, Peak RSS=882.996 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.962897715 s, Peak RSS=300.023 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.227612101 s, Peak RSS=533.180 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.803861066 s, Peak RSS=709.688 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.605364700 s, Peak RSS=1035.734 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.907611990 s, Peak RSS=300.195 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.200250232 s, Peak RSS=560.512 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.796945327 s, Peak RSS=737.457 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.615594924 s, Peak RSS=1038.426 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 192^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.087298781 s, Peak RSS=135.133 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 192^3 with 1 process  repeat=3/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.202326818 s, Peak RSS=2449.391 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=4.757080727 s, Peak RSS=620.527 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.071268201 s, Peak RSS=939.699 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.055246763 s, Peak RSS=1275.520 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.564472954 s, Peak RSS=1629.820 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=4.712826748 s, Peak RSS=620.566 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.993545042 s, Peak RSS=926.438 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.955688894 s, Peak RSS=1147.992 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.547041328 s, Peak RSS=1649.703 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 256^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.182601903 s, Peak RSS=267.680 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 256^3 with 1 process  repeat=3/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.931494335 s, Peak RSS=5453.930 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=9.376682765 s, Peak RSS=1105.551 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.907224004 s, Peak RSS=1678.520 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.121477506 s, Peak RSS=2208.914 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.325081561 s, Peak RSS=2783.480 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=9.201530893 s, Peak RSS=1105.668 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.870676670 s, Peak RSS=1706.219 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.121555798 s, Peak RSS=2236.688 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.267188215 s, Peak RSS=2811.297 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 320^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.327298953 s, Peak RSS=469.035 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 320^3 with 1 process  repeat=3/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.781456827 s, Peak RSS=10469.422 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=15.467660211 s, Peak RSS=1759.777 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=10.060478683 s, Peak RSS=2888.441 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.167008218 s, Peak RSS=3481.766 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.814364350 s, Peak RSS=5049.410 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=15.159614010 s, Peak RSS=1759.723 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=9.923996329 s, Peak RSS=2906.395 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.133674770 s, Peak RSS=3468.336 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.851390530 s, Peak RSS=4928.922 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 384^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.530361902 s, Peak RSS=776.852 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 384^3 with 1 process  repeat=3/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.541385238 s, Peak RSS=17963.730 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=22.842592114 s, Peak RSS=2573.273 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=15.090303386 s, Peak RSS=3888.625 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=10.672960492 s, Peak RSS=4919.492 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.724419686 s, Peak RSS=7175.547 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=22.427784221 s, Peak RSS=2573.523 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=14.955580052 s, Peak RSS=3888.812 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=10.543016040 s, Peak RSS=4928.812 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=8.806862392 s, Peak RSS=7221.328 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 448^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.805367644 s, Peak RSS=1175.305 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 448^3 with 1 process  repeat=3/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=15.225744888 s, Peak RSS=28429.152 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=32.295148614 s, Peak RSS=3609.324 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=21.703675199 s, Peak RSS=5457.402 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=15.762453480 s, Peak RSS=6829.879 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=12.883547605 s, Peak RSS=10495.516 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=31.712849626 s, Peak RSS=3609.480 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=21.537276439 s, Peak RSS=5438.070 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=15.598640997 s, Peak RSS=6821.535 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=12.935376798 s, Peak RSS=10496.129 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 512^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=1.177949533 s, Peak RSS=1714.188 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 512^3 with 1 process  repeat=3/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=22.675888004 s, Peak RSS=42358.387 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=42.558062260 s, Peak RSS=4806.887 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=28.637772391 s, Peak RSS=7433.500 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=20.825513251 s, Peak RSS=9606.922 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=17.118256490 s, Peak RSS=14702.809 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=41.837781135 s, Peak RSS=4807.203 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=28.163715297 s, Peak RSS=7447.965 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=20.724925755 s, Peak RSS=9608.020 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=17.108607497 s, Peak RSS=14703.301 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 64^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.003069739 s, Peak RSS=90.172 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 64^3 with 1 process  repeat=3/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.046250673 s, Peak RSS=334.383 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.090045856 s, Peak RSS=116.113 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.074688474 s, Peak RSS=259.016 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.057330315 s, Peak RSS=398.520 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.052561941 s, Peak RSS=684.293 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.087722476 s, Peak RSS=115.812 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.067171888 s, Peak RSS=260.336 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.061485676 s, Peak RSS=397.828 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.057280714 s, Peak RSS=686.027 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 128^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.016317305 s, Peak RSS=118.277 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 128^3 with 1 process  repeat=3/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.330597021 s, Peak RSS=922.625 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.414610130 s, Peak RSS=165.660 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.280484813 s, Peak RSS=399.820 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.192591342 s, Peak RSS=599.172 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.171421873 s, Peak RSS=1055.887 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=0.415233477 s, Peak RSS=165.617 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.352065115 s, Peak RSS=399.793 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.182137941 s, Peak RSS=600.680 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.162775158 s, Peak RSS=1055.484 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 192^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.055661698 s, Peak RSS=170.941 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 192^3 with 1 process  repeat=3/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.796907359 s, Peak RSS=2459.094 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.087760042 s, Peak RSS=253.105 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.740121657 s, Peak RSS=554.727 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.550001073 s, Peak RSS=845.125 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.462930785 s, Peak RSS=1372.078 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=1.070538196 s, Peak RSS=253.445 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.730283915 s, Peak RSS=541.410 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.543600549 s, Peak RSS=849.023 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.456192952 s, Peak RSS=1349.125 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 256^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.125592342 s, Peak RSS=286.168 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 256^3 with 1 process  repeat=3/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.703240038 s, Peak RSS=5496.445 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=2.094557639 s, Peak RSS=412.285 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.535036705 s, Peak RSS=979.414 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.118856272 s, Peak RSS=1375.203 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.958283289 s, Peak RSS=2274.906 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=2.059626129 s, Peak RSS=412.469 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.452028875 s, Peak RSS=977.375 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.128097980 s, Peak RSS=1352.441 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=0.956412875 s, Peak RSS=2291.371 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 320^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.242150497 s, Peak RSS=469.922 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 320^3 with 1 process  repeat=3/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.278265321 s, Peak RSS=10511.941 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=3.599859246 s, Peak RSS=650.836 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.583142343 s, Peak RSS=1528.426 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.028239259 s, Peak RSS=2124.691 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.784517565 s, Peak RSS=3530.652 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=3.584058871 s, Peak RSS=651.730 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.564429923 s, Peak RSS=1431.012 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.001546728 s, Peak RSS=2196.023 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=1.831015907 s, Peak RSS=3531.438 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 384^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.405208218 s, Peak RSS=747.992 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 384^3 with 1 process  repeat=3/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.194796772 s, Peak RSS=18005.934 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=5.619928775 s, Peak RSS=963.312 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.232517068 s, Peak RSS=2143.422 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.412404497 s, Peak RSS=3236.461 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=2.979836028 s, Peak RSS=5297.891 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=5.596824791 s, Peak RSS=964.367 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.175021063 s, Peak RSS=2144.762 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.382925758 s, Peak RSS=3239.133 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=3.000250614 s, Peak RSS=5147.016 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 448^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.643515377 s, Peak RSS=1132.242 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 448^3 with 1 process  repeat=3/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.516789019 s, Peak RSS=28468.531 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=8.667291197 s, Peak RSS=1395.230 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.523342762 s, Peak RSS=3183.098 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.441928920 s, Peak RSS=4815.480 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.851180627 s, Peak RSS=7839.609 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=8.472108963 s, Peak RSS=1396.426 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=6.464266615 s, Peak RSS=3178.539 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=5.359480616 s, Peak RSS=4724.199 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=4.837915388 s, Peak RSS=7854.660 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 512^3 with 1 process  repeat=3/5
====================================================================================
Measured runtime=0.951258714 s, Peak RSS=1648.426 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 512^3 with 1 process  repeat=3/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.361923240 s, Peak RSS=42404.676 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=12.215457426 s, Peak RSS=1898.754 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=9.358711034 s, Peak RSS=4430.680 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.896370776 s, Peak RSS=6759.293 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.111455790 s, Peak RSS=11130.008 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=3/5
====================================================================================
Measured runtime=12.082753834 s, Peak RSS=1900.477 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=9.286332942 s, Peak RSS=4433.641 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.834829381 s, Peak RSS=6836.727 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=3/5
====================================================================================
Measured runtime=7.139600549 s, Peak RSS=11084.465 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 64^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.004070995 s, Peak RSS=46.656 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 64^3 with 1 process  repeat=4/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.047488553 s, Peak RSS=293.898 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.150608257 s, Peak RSS=75.844 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.109838124 s, Peak RSS=169.352 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.088876293 s, Peak RSS=265.027 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.084395706 s, Peak RSS=432.070 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.146497217 s, Peak RSS=83.695 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.107557304 s, Peak RSS=173.992 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.087478991 s, Peak RSS=267.477 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.075878262 s, Peak RSS=431.320 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 128^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.019266381 s, Peak RSS=69.523 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 128^3 with 1 process  repeat=4/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.342908025 s, Peak RSS=860.449 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.648304619 s, Peak RSS=150.836 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.431560282 s, Peak RSS=340.535 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.284886233 s, Peak RSS=497.594 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.236727177 s, Peak RSS=731.465 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.633175171 s, Peak RSS=148.977 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.425963213 s, Peak RSS=339.695 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.282573741 s, Peak RSS=500.156 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.243477316 s, Peak RSS=731.805 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 192^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.061865184 s, Peak RSS=127.512 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 192^3 with 1 process  repeat=4/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.126392739 s, Peak RSS=2416.285 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.641938189 s, Peak RSS=272.664 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.090389264 s, Peak RSS=527.660 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.768498125 s, Peak RSS=777.027 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.622756296 s, Peak RSS=1190.617 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.594793682 s, Peak RSS=275.055 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.066384185 s, Peak RSS=550.984 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.754387155 s, Peak RSS=745.645 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.619911470 s, Peak RSS=1199.414 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 256^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.155484913 s, Peak RSS=240.785 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 256^3 with 1 process  repeat=4/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.730582047 s, Peak RSS=5454.152 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=3.101754651 s, Peak RSS=488.008 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.120098580 s, Peak RSS=981.148 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.499522636 s, Peak RSS=1347.422 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.293812195 s, Peak RSS=2173.383 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=3.020684560 s, Peak RSS=488.000 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.056392097 s, Peak RSS=981.781 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.495358669 s, Peak RSS=1377.941 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.289085465 s, Peak RSS=2147.973 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 320^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.256706692 s, Peak RSS=437.984 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 320^3 with 1 process  repeat=4/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.305842770 s, Peak RSS=10468.988 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=5.140436901 s, Peak RSS=773.711 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.524212904 s, Peak RSS=1702.637 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.680751350 s, Peak RSS=2228.391 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.336531045 s, Peak RSS=3524.445 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=5.038874026 s, Peak RSS=773.871 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.539627927 s, Peak RSS=1703.414 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.662805909 s, Peak RSS=2303.633 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.214496148 s, Peak RSS=3525.590 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 384^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.427915848 s, Peak RSS=719.336 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 384^3 with 1 process  repeat=4/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.283112342 s, Peak RSS=17963.293 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=8.282419587 s, Peak RSS=1172.215 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.770922252 s, Peak RSS=2377.863 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.509485913 s, Peak RSS=3437.348 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.847997951 s, Peak RSS=5342.602 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=8.102584625 s, Peak RSS=1172.234 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.668494420 s, Peak RSS=2371.621 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.424442482 s, Peak RSS=3343.281 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.847933433 s, Peak RSS=5347.066 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 448^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.673354058 s, Peak RSS=1111.246 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 448^3 with 1 process  repeat=4/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.600502850 s, Peak RSS=28425.602 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=12.192456971 s, Peak RSS=1661.559 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.654770974 s, Peak RSS=3469.410 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=6.906190837 s, Peak RSS=5145.367 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.993350758 s, Peak RSS=7955.277 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=12.022206223 s, Peak RSS=1661.711 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.578526602 s, Peak RSS=3453.152 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=6.818663892 s, Peak RSS=4961.129 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.948581480 s, Peak RSS=8073.359 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 512^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.977825945 s, Peak RSS=1627.945 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 512^3 with 1 process  repeat=4/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.780278355 s, Peak RSS=42358.094 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=17.081836471 s, Peak RSS=2324.395 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=12.471859932 s, Peak RSS=4930.754 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=10.005996624 s, Peak RSS=7254.551 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.907844599 s, Peak RSS=11708.074 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=17.077412697 s, Peak RSS=2324.312 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=12.406429688 s, Peak RSS=4931.141 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=9.953947501 s, Peak RSS=7242.352 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.868359880 s, Peak RSS=11603.922 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 64^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.006591293 s, Peak RSS=48.789 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 64^3 with 1 process  repeat=4/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.056658866 s, Peak RSS=301.832 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.479035794 s, Peak RSS=112.531 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.338290249 s, Peak RSS=213.301 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.198019909 s, Peak RSS=319.234 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.166416392 s, Peak RSS=530.527 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.473359609 s, Peak RSS=112.117 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.304864346 s, Peak RSS=225.039 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.199556164 s, Peak RSS=328.395 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.160554407 s, Peak RSS=521.586 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 128^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.031044896 s, Peak RSS=76.961 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 128^3 with 1 process  repeat=4/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.380145775 s, Peak RSS=882.680 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.959676789 s, Peak RSS=300.051 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.227487033 s, Peak RSS=516.027 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.806341735 s, Peak RSS=709.496 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.611533650 s, Peak RSS=1036.801 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.910353587 s, Peak RSS=300.309 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.315774795 s, Peak RSS=560.945 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.775994023 s, Peak RSS=735.887 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.601134817 s, Peak RSS=1042.746 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 192^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.086226815 s, Peak RSS=145.730 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 192^3 with 1 process  repeat=4/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.208069733 s, Peak RSS=2445.859 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=4.764265353 s, Peak RSS=620.668 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.019164992 s, Peak RSS=939.676 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.050629612 s, Peak RSS=1275.996 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.618873533 s, Peak RSS=1659.496 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=4.678591447 s, Peak RSS=620.645 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.935426353 s, Peak RSS=925.426 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.985534095 s, Peak RSS=1148.438 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.550221808 s, Peak RSS=1672.309 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 256^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.186518841 s, Peak RSS=273.562 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 256^3 with 1 process  repeat=4/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.943752142 s, Peak RSS=5453.758 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=9.495337759 s, Peak RSS=1105.586 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.986633765 s, Peak RSS=1678.145 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.169536327 s, Peak RSS=2209.195 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.269147658 s, Peak RSS=2818.312 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=9.290315641 s, Peak RSS=1105.727 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.861981652 s, Peak RSS=1706.590 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.107296478 s, Peak RSS=2236.258 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.258720903 s, Peak RSS=2755.160 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 320^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.331088929 s, Peak RSS=462.383 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 320^3 with 1 process  repeat=4/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.588531438 s, Peak RSS=10469.203 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=15.609685972 s, Peak RSS=1759.621 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=10.081002543 s, Peak RSS=2889.191 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.212598696 s, Peak RSS=3481.926 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.800330751 s, Peak RSS=5050.820 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=15.161729649 s, Peak RSS=1759.797 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=9.862221336 s, Peak RSS=2906.184 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.138563112 s, Peak RSS=3468.562 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.758786223 s, Peak RSS=4929.012 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 384^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.536978255 s, Peak RSS=776.832 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 384^3 with 1 process  repeat=4/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.673646749 s, Peak RSS=17963.902 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=22.963168191 s, Peak RSS=2573.312 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=15.088366200 s, Peak RSS=3888.180 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=10.552257959 s, Peak RSS=4919.945 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.670830978 s, Peak RSS=7233.664 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=22.425452494 s, Peak RSS=2573.605 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=14.919797791 s, Peak RSS=3888.496 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=10.485037927 s, Peak RSS=4928.996 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=8.691145152 s, Peak RSS=7143.582 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 448^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.808710708 s, Peak RSS=1167.227 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 448^3 with 1 process  repeat=4/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=15.145100497 s, Peak RSS=28429.168 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=32.263970984 s, Peak RSS=3609.504 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=21.670642942 s, Peak RSS=5457.152 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=15.779342854 s, Peak RSS=6829.074 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=12.935713436 s, Peak RSS=10496.402 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=31.707191798 s, Peak RSS=3609.652 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=21.492793946 s, Peak RSS=5437.398 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=15.452512001 s, Peak RSS=6822.191 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=12.860422583 s, Peak RSS=10497.262 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 512^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=1.165606944 s, Peak RSS=1706.184 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 512^3 with 1 process  repeat=4/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=22.645422650 s, Peak RSS=42358.723 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=41.961506536 s, Peak RSS=4807.121 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=28.545301828 s, Peak RSS=7448.812 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=20.863279409 s, Peak RSS=9607.453 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=17.239513719 s, Peak RSS=14701.258 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=41.789277285 s, Peak RSS=4807.145 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=28.308424288 s, Peak RSS=7447.777 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=20.764976757 s, Peak RSS=9607.125 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=17.019228566 s, Peak RSS=14662.230 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 64^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.003102441 s, Peak RSS=90.242 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 64^3 with 1 process  repeat=4/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.044651261 s, Peak RSS=334.332 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.090401278 s, Peak RSS=116.031 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.077132585 s, Peak RSS=259.523 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.058030924 s, Peak RSS=398.004 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.052819581 s, Peak RSS=683.629 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.088715034 s, Peak RSS=115.793 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.067082576 s, Peak RSS=259.359 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.051048961 s, Peak RSS=396.699 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.052963079 s, Peak RSS=685.887 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 128^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.016553296 s, Peak RSS=118.305 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 128^3 with 1 process  repeat=4/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.334862414 s, Peak RSS=922.949 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.418834584 s, Peak RSS=164.691 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.279244631 s, Peak RSS=399.371 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.185605184 s, Peak RSS=600.461 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.159767030 s, Peak RSS=1055.469 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=0.418517036 s, Peak RSS=165.777 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.286528698 s, Peak RSS=399.133 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.186318970 s, Peak RSS=599.902 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.162506842 s, Peak RSS=1055.441 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 192^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.055002627 s, Peak RSS=170.211 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 192^3 with 1 process  repeat=4/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.096667350 s, Peak RSS=2460.145 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.103836844 s, Peak RSS=254.266 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.780119920 s, Peak RSS=555.395 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.553666472 s, Peak RSS=856.809 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.465545157 s, Peak RSS=1344.469 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=1.079791055 s, Peak RSS=254.871 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.766055854 s, Peak RSS=562.328 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.552305635 s, Peak RSS=812.285 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.440884643 s, Peak RSS=1353.184 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 256^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.127780769 s, Peak RSS=283.684 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 256^3 with 1 process  repeat=4/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.745661824 s, Peak RSS=5496.254 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=2.108477860 s, Peak RSS=415.348 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.460957962 s, Peak RSS=905.762 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.117937845 s, Peak RSS=1372.012 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.966515138 s, Peak RSS=2275.922 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=2.059700586 s, Peak RSS=412.570 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.454329615 s, Peak RSS=940.586 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.112178016 s, Peak RSS=1386.059 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=0.990646019 s, Peak RSS=2284.711 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 320^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.238608993 s, Peak RSS=470.543 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 320^3 with 1 process  repeat=4/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.181717811 s, Peak RSS=10512.211 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=3.596922648 s, Peak RSS=651.090 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.584057744 s, Peak RSS=1528.781 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.027995937 s, Peak RSS=2193.164 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.752289056 s, Peak RSS=3528.734 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=3.535401744 s, Peak RSS=651.660 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.549841295 s, Peak RSS=1431.695 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.012453235 s, Peak RSS=2194.984 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=1.752895637 s, Peak RSS=3532.543 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 384^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.407228552 s, Peak RSS=752.113 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 384^3 with 1 process  repeat=4/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.124521092 s, Peak RSS=18005.812 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=5.677687384 s, Peak RSS=963.293 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.205941126 s, Peak RSS=2176.250 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.388285612 s, Peak RSS=3210.766 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.979867490 s, Peak RSS=5263.695 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=5.624618238 s, Peak RSS=964.207 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.174433207 s, Peak RSS=2160.730 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=3.394641417 s, Peak RSS=3149.840 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=2.960550357 s, Peak RSS=5298.414 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 448^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.641591431 s, Peak RSS=1131.363 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 448^3 with 1 process  repeat=4/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.267343895 s, Peak RSS=28468.422 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=8.612778506 s, Peak RSS=1395.125 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=6.542295191 s, Peak RSS=3182.070 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.408979130 s, Peak RSS=4668.988 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.949913396 s, Peak RSS=7803.273 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=8.601980071 s, Peak RSS=1396.426 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=6.430546379 s, Peak RSS=3191.266 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=5.391961403 s, Peak RSS=4741.508 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=4.843416311 s, Peak RSS=7852.340 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 512^3 with 1 process  repeat=4/5
====================================================================================
Measured runtime=0.952243392 s, Peak RSS=1648.426 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 512^3 with 1 process  repeat=4/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.536211007 s, Peak RSS=42404.855 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=12.371793293 s, Peak RSS=1898.715 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=9.359243021 s, Peak RSS=4416.598 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.884826862 s, Peak RSS=6823.863 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.160162809 s, Peak RSS=11280.539 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=4/5
====================================================================================
Measured runtime=12.101300030 s, Peak RSS=1900.367 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=9.310533052 s, Peak RSS=4433.395 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.836882987 s, Peak RSS=6832.926 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=4/5
====================================================================================
Measured runtime=7.227146571 s, Peak RSS=11221.402 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 64^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.003890900 s, Peak RSS=46.633 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 64^3 with 1 process  repeat=5/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.049278106 s, Peak RSS=293.785 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.148049011 s, Peak RSS=76.473 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.151217489 s, Peak RSS=169.359 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.084046617 s, Peak RSS=265.238 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.083790211 s, Peak RSS=430.816 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.149473667 s, Peak RSS=76.488 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.111080824 s, Peak RSS=175.703 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.081856867 s, Peak RSS=265.516 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.080362563 s, Peak RSS=432.945 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 128^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.018993222 s, Peak RSS=69.438 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 128^3 with 1 process  repeat=5/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.334971977 s, Peak RSS=859.340 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.643247512 s, Peak RSS=150.926 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.422436572 s, Peak RSS=339.504 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.278193685 s, Peak RSS=497.789 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.237452377 s, Peak RSS=731.438 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.639839698 s, Peak RSS=149.074 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.420325038 s, Peak RSS=339.289 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.282330699 s, Peak RSS=499.957 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.233153928 s, Peak RSS=734.508 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 192^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.061228533 s, Peak RSS=130.012 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 192^3 with 1 process  repeat=5/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.121881773 s, Peak RSS=2417.160 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.619023070 s, Peak RSS=272.719 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.093807744 s, Peak RSS=528.039 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.758079392 s, Peak RSS=777.840 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.634729616 s, Peak RSS=1191.289 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.572349110 s, Peak RSS=275.078 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.064541108 s, Peak RSS=550.965 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.745994552 s, Peak RSS=745.703 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.623511278 s, Peak RSS=1201.250 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 256^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.134150048 s, Peak RSS=246.059 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 256^3 with 1 process  repeat=5/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.730204632 s, Peak RSS=5453.211 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=3.122085177 s, Peak RSS=487.879 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.109757864 s, Peak RSS=957.562 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.496786606 s, Peak RSS=1382.570 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.299570989 s, Peak RSS=2171.680 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=3.020893717 s, Peak RSS=488.027 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.073507528 s, Peak RSS=982.375 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.518116074 s, Peak RSS=1378.953 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.250745980 s, Peak RSS=2142.902 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 320^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.257403378 s, Peak RSS=429.438 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 320^3 with 1 process  repeat=5/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.232531735 s, Peak RSS=10468.758 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=5.163581562 s, Peak RSS=773.793 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.565305330 s, Peak RSS=1702.426 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.702192002 s, Peak RSS=2227.637 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.228313655 s, Peak RSS=3524.750 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=5.025525941 s, Peak RSS=773.918 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.489587359 s, Peak RSS=1702.832 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.635324317 s, Peak RSS=2304.121 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.220060275 s, Peak RSS=3524.367 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 384^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.426089077 s, Peak RSS=713.148 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 384^3 with 1 process  repeat=5/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.137805261 s, Peak RSS=17963.188 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=8.259451795 s, Peak RSS=1172.223 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.731035726 s, Peak RSS=2378.336 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.427894179 s, Peak RSS=3437.320 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.927364203 s, Peak RSS=5341.949 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=8.191971675 s, Peak RSS=1172.234 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.755604464 s, Peak RSS=2371.547 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.430068707 s, Peak RSS=3345.477 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.938031711 s, Peak RSS=5368.059 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 448^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.663414348 s, Peak RSS=1103.008 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 448^3 with 1 process  repeat=5/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.640655150 s, Peak RSS=28425.707 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=12.203888340 s, Peak RSS=1661.621 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=8.602924535 s, Peak RSS=3469.328 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=6.840424869 s, Peak RSS=5146.688 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.982724566 s, Peak RSS=7958.855 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=11.921246907 s, Peak RSS=1661.699 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=8.648603150 s, Peak RSS=3452.770 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=6.774341924 s, Peak RSS=4960.492 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.993295400 s, Peak RSS=8133.078 MiB, peak process count=9

====================================================================================
Running SPHEROID  MC  level=0.5  at 512^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.984511721 s, Peak RSS=1629.953 MiB, peak process count=1

====================================================================================
Running SPHEROID  MT  level=0.5  at 512^3 with 1 process  repeat=5/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.892005575 s, Peak RSS=42357.801 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=17.199468594 s, Peak RSS=2324.418 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=12.505141247 s, Peak RSS=4931.230 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=10.029753649 s, Peak RSS=7253.055 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=9.018894690 s, Peak RSS=11726.984 MiB, peak process count=9

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=17.057955257 s, Peak RSS=2324.309 MiB, peak process count=1

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=12.381998511 s, Peak RSS=4930.652 MiB, peak process count=3

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=9.978429423 s, Peak RSS=7242.281 MiB, peak process count=5

====================================================================================
Running SPHEROID  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=8.852541438 s, Peak RSS=11513.523 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 64^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.006539447 s, Peak RSS=48.793 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 64^3 with 1 process  repeat=5/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.058031374 s, Peak RSS=301.805 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.482456279 s, Peak RSS=112.324 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.305100454 s, Peak RSS=210.496 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.197936903 s, Peak RSS=319.629 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.157133359 s, Peak RSS=527.797 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.466644491 s, Peak RSS=113.188 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.305053550 s, Peak RSS=224.230 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.197359878 s, Peak RSS=327.855 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.164838799 s, Peak RSS=521.109 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 128^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.031426592 s, Peak RSS=76.910 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 128^3 with 1 process  repeat=5/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.379683110 s, Peak RSS=883.141 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.983710311 s, Peak RSS=299.988 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.229356449 s, Peak RSS=532.391 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.802198046 s, Peak RSS=709.090 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.614867441 s, Peak RSS=1036.645 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.942909677 s, Peak RSS=300.176 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.208053831 s, Peak RSS=560.559 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.785865595 s, Peak RSS=738.348 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.598902055 s, Peak RSS=1041.609 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 192^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.087303632 s, Peak RSS=142.988 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 192^3 with 1 process  repeat=5/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.194438503 s, Peak RSS=2435.738 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=4.765269359 s, Peak RSS=620.785 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.022813901 s, Peak RSS=939.219 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.022659383 s, Peak RSS=1248.391 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.562737526 s, Peak RSS=1637.496 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=4.721037624 s, Peak RSS=620.641 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.157795221 s, Peak RSS=926.445 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.972183826 s, Peak RSS=1141.188 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.547027632 s, Peak RSS=1656.449 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 256^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.180989121 s, Peak RSS=273.449 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 256^3 with 1 process  repeat=5/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.891237670 s, Peak RSS=5453.945 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=9.482270249 s, Peak RSS=1105.500 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.921884011 s, Peak RSS=1678.137 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.160329525 s, Peak RSS=2188.625 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.282637885 s, Peak RSS=2814.508 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=9.264530959 s, Peak RSS=1105.699 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.905982795 s, Peak RSS=1706.379 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.140766312 s, Peak RSS=2253.152 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.259300587 s, Peak RSS=2815.902 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 320^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.331436776 s, Peak RSS=465.281 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 320^3 with 1 process  repeat=5/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.568775867 s, Peak RSS=10469.199 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=15.623659229 s, Peak RSS=1759.648 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=10.055128056 s, Peak RSS=2888.977 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.118652214 s, Peak RSS=3482.180 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.797123712 s, Peak RSS=5033.664 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=15.141077290 s, Peak RSS=1759.844 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=9.921539023 s, Peak RSS=2906.535 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.129319582 s, Peak RSS=3468.086 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.758446319 s, Peak RSS=4919.398 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 384^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.536150795 s, Peak RSS=776.879 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 384^3 with 1 process  repeat=5/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.731465072 s, Peak RSS=17963.684 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=22.742070711 s, Peak RSS=2573.266 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=15.039352578 s, Peak RSS=3888.223 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=10.657058645 s, Peak RSS=4919.805 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=8.812982950 s, Peak RSS=7223.441 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=22.557562690 s, Peak RSS=2573.605 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=14.895688329 s, Peak RSS=3888.984 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=10.423498939 s, Peak RSS=4929.438 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=8.772720875 s, Peak RSS=7235.031 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 448^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.821919375 s, Peak RSS=1190.215 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 448^3 with 1 process  repeat=5/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=15.166598666 s, Peak RSS=28429.066 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=32.189833310 s, Peak RSS=3609.500 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=21.759305854 s, Peak RSS=5457.273 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=15.874771173 s, Peak RSS=6829.660 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=12.991298854 s, Peak RSS=10496.645 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=31.732447531 s, Peak RSS=3609.598 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=21.466973551 s, Peak RSS=5447.199 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=15.602790396 s, Peak RSS=6821.586 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=12.988826096 s, Peak RSS=10497.797 MiB, peak process count=9

====================================================================================
Running TORUS  MC  level=0.5  at 512^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=1.161261419 s, Peak RSS=1708.293 MiB, peak process count=1

====================================================================================
Running TORUS  MT  level=0.5  at 512^3 with 1 process  repeat=5/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=22.358258160 s, Peak RSS=42358.812 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=42.410253978 s, Peak RSS=4806.992 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=28.460855495 s, Peak RSS=7447.559 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=20.902667387 s, Peak RSS=9607.570 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=17.200823721 s, Peak RSS=14701.066 MiB, peak process count=9

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=41.854313306 s, Peak RSS=4807.254 MiB, peak process count=1

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=28.240144631 s, Peak RSS=7448.016 MiB, peak process count=3

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=20.689818690 s, Peak RSS=9607.430 MiB, peak process count=5

====================================================================================
Running TORUS  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=17.204223727 s, Peak RSS=14662.387 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 64^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.003136511 s, Peak RSS=90.309 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 64^3 with 1 process  repeat=5/5
PyVista tetrahedra: 1,500,282
====================================================================================
Measured runtime=0.044846792 s, Peak RSS=334.359 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.091436703 s, Peak RSS=116.176 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.072378436 s, Peak RSS=259.059 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.062436843 s, Peak RSS=398.602 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.057711486 s, Peak RSS=684.410 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.088484743 s, Peak RSS=115.836 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.065709806 s, Peak RSS=261.059 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.054996708 s, Peak RSS=399.473 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 64^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.054522799 s, Peak RSS=683.957 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 128^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.016436004 s, Peak RSS=118.289 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 128^3 with 1 process  repeat=5/5
PyVista tetrahedra: 12,290,298
====================================================================================
Measured runtime=0.333761277 s, Peak RSS=923.758 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.428581171 s, Peak RSS=164.812 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.327460629 s, Peak RSS=399.684 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.187834717 s, Peak RSS=601.180 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.165161946 s, Peak RSS=1054.746 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=0.411960261 s, Peak RSS=166.344 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.279578383 s, Peak RSS=399.762 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.184456748 s, Peak RSS=600.594 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 128^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.163029079 s, Peak RSS=1055.336 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 192^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.055997632 s, Peak RSS=170.062 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 192^3 with 1 process  repeat=5/5
PyVista tetrahedra: 41,807,226
====================================================================================
Measured runtime=1.095917835 s, Peak RSS=2459.016 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.098417682 s, Peak RSS=255.020 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.766933907 s, Peak RSS=559.492 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.543785695 s, Peak RSS=820.117 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.454051254 s, Peak RSS=1369.102 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=1.083634261 s, Peak RSS=254.031 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.730989803 s, Peak RSS=558.980 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.544134310 s, Peak RSS=848.273 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 192^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.449526531 s, Peak RSS=1334.129 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 256^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.125478806 s, Peak RSS=286.590 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 256^3 with 1 process  repeat=5/5
PyVista tetrahedra: 99,488,250
====================================================================================
Measured runtime=2.817273232 s, Peak RSS=5496.406 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=2.105033083 s, Peak RSS=411.984 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.462164173 s, Peak RSS=943.250 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.120050639 s, Peak RSS=1340.395 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.994028111 s, Peak RSS=2273.508 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=2.035153375 s, Peak RSS=412.523 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.502028410 s, Peak RSS=938.789 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.127587875 s, Peak RSS=1373.883 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 256^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=0.983128650 s, Peak RSS=2289.203 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 320^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.242466056 s, Peak RSS=468.328 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 320^3 with 1 process  repeat=5/5
PyVista tetrahedra: 194,770,554
====================================================================================
Measured runtime=5.247637467 s, Peak RSS=10512.125 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=3.557832990 s, Peak RSS=650.859 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.595435271 s, Peak RSS=1528.734 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.014824257 s, Peak RSS=2192.242 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.769990740 s, Peak RSS=3525.383 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=3.553466993 s, Peak RSS=651.883 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.556708946 s, Peak RSS=1530.633 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.004835179 s, Peak RSS=2196.574 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 320^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=1.803356719 s, Peak RSS=3528.477 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 384^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.406271866 s, Peak RSS=747.715 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 384^3 with 1 process  repeat=5/5
PyVista tetrahedra: 337,091,322
====================================================================================
Measured runtime=9.190968362 s, Peak RSS=18005.785 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=5.653659578 s, Peak RSS=963.234 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.182913913 s, Peak RSS=2143.105 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.390252787 s, Peak RSS=3246.266 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.980298330 s, Peak RSS=5305.270 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=5.606545739 s, Peak RSS=964.289 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.158619492 s, Peak RSS=2078.316 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=3.370950031 s, Peak RSS=3290.816 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 384^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=2.969328883 s, Peak RSS=5221.801 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 448^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.635543658 s, Peak RSS=1139.797 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 448^3 with 1 process  repeat=5/5
PyVista tetrahedra: 535,887,738
====================================================================================
Measured runtime=14.268756589 s, Peak RSS=28468.516 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=8.688090075 s, Peak RSS=1395.047 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=6.539677304 s, Peak RSS=3182.305 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.442341602 s, Peak RSS=4892.414 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.853021343 s, Peak RSS=7682.910 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=8.511532438 s, Peak RSS=1396.637 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=6.478147774 s, Peak RSS=3178.168 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=5.374391472 s, Peak RSS=4892.012 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 448^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=4.859773637 s, Peak RSS=7761.281 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  MC  level=0.5  at 512^3 with 1 process  repeat=5/5
====================================================================================
Measured runtime=0.946742862 s, Peak RSS=1647.918 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  MT  level=0.5  at 512^3 with 1 process  repeat=5/5
PyVista tetrahedra: 800,596,986
====================================================================================
Measured runtime=21.433443784 s, Peak RSS=42404.789 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=12.155989824 s, Peak RSS=1898.809 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=9.344924226 s, Peak RSS=4417.082 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.915091511 s, Peak RSS=6830.406 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (default)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.113143294 s, Peak RSS=11210.293 MiB, peak process count=9

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 1 worker process(es), start=serial  repeat=5/5
====================================================================================
Measured runtime=11.992681107 s, Peak RSS=1900.488 MiB, peak process count=1

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 2 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=9.297271626 s, Peak RSS=4418.875 MiB, peak process count=3

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 4 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.903546081 s, Peak RSS=6832.871 MiB, peak process count=5

====================================================================================
Running GAUSSIAN_TWO  SRMT (uniform)  level=0.5  at 512^3 with 8 worker process(es), start=fork  repeat=5/5
====================================================================================
Measured runtime=7.123389320 s, Peak RSS=11289.883 MiB, peak process count=9
[plots] skipped: enable --save-meshes to render repeat-1 benchmark meshes.

Level-set support and mesh diagnostics
--------------------------------------
        Case   Level     N             Variant   P        Ncell    Nactive    r_act%         Ntet         Nsub         NV         NE         NF    NC     Chi   Inv.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    spheroid   0.500    64                  MC   1       250047       3610    1.4437           --           --       3608      10818       7212     1       2    yes
    spheroid   0.500    64                  MT   1       250047       3610    1.4437      1500282           --      10822      32460      21640     1       2    yes
    spheroid   0.500    64     SRMT_default_P1   1       250047       3610    1.4437       173280       173280      43274     129816      86544     1       2    yes
    spheroid   0.500    64     SRMT_default_P2   2       250047       3610    1.4437       173280       173280      43274     129816      86544     1       2    yes
    spheroid   0.500    64     SRMT_default_P4   4       250047       3610    1.4437       173280       173280      43274     129816      86544     1       2    yes
    spheroid   0.500    64     SRMT_default_P8   8       250047       3610    1.4437       173280       173280      43274     129816      86544     1       2    yes
    spheroid   0.500    64     SRMT_uniform_P1   1       250047       3610    1.4437       173280       173280      43214     129636      86424     1       2    yes
    spheroid   0.500    64     SRMT_uniform_P2   2       250047       3610    1.4437       173280       173280      43214     129636      86424     1       2    yes
    spheroid   0.500    64     SRMT_uniform_P4   4       250047       3610    1.4437       173280       173280      43214     129636      86424     1       2    yes
    spheroid   0.500    64     SRMT_uniform_P8   8       250047       3610    1.4437       173280       173280      43214     129636      86424     1       2    yes
    spheroid   0.500   128                  MC   1      2048383      14618    0.7136           --           --      14616      43842      29228     1       2    yes
    spheroid   0.500   128                  MT   1      2048383      14618    0.7136     12290298           --      43758     131268      87512     1       2    yes
    spheroid   0.500   128     SRMT_default_P1   1      2048383      14618    0.7136       701664       701664     175290     525864     350576     1       2    yes
    spheroid   0.500   128     SRMT_default_P2   2      2048383      14618    0.7136       701664       701664     175290     525864     350576     1       2    yes
    spheroid   0.500   128     SRMT_default_P4   4      2048383      14618    0.7136       701664       701664     175290     525864     350576     1       2    yes
    spheroid   0.500   128     SRMT_default_P8   8      2048383      14618    0.7136       701664       701664     175290     525864     350576     1       2    yes
    spheroid   0.500   128     SRMT_uniform_P1   1      2048383      14618    0.7136       701664       701664     175310     525924     350616     1       2    yes
    spheroid   0.500   128     SRMT_uniform_P2   2      2048383      14618    0.7136       701664       701664     175310     525924     350616     1       2    yes
    spheroid   0.500   128     SRMT_uniform_P4   4      2048383      14618    0.7136       701664       701664     175310     525924     350616     1       2    yes
    spheroid   0.500   128     SRMT_uniform_P8   8      2048383      14618    0.7136       701664       701664     175310     525924     350616     1       2    yes
    spheroid   0.500   192                  MC   1      6967871      33106    0.4751           --           --      33104      99306      66204     1       2    yes
    spheroid   0.500   192                  MT   1      6967871      33106    0.4751     41807226           --      99210     297624     198416     1       2    yes
    spheroid   0.500   192     SRMT_default_P1   1      6967871      33106    0.4751      1589088      1589088     396714    1190136     793424     1       2    yes
    spheroid   0.500   192     SRMT_default_P2   2      6967871      33106    0.4751      1589088      1589088     396714    1190136     793424     1       2    yes
    spheroid   0.500   192     SRMT_default_P4   4      6967871      33106    0.4751      1589088      1589088     396714    1190136     793424     1       2    yes
    spheroid   0.500   192     SRMT_default_P8   8      6967871      33106    0.4751      1589088      1589088     396714    1190136     793424     1       2    yes
    spheroid   0.500   192     SRMT_uniform_P1   1      6967871      33106    0.4751      1589088      1589088     396582    1189740     793160     1       2    yes
    spheroid   0.500   192     SRMT_uniform_P2   2      6967871      33106    0.4751      1589088      1589088     396582    1189740     793160     1       2    yes
    spheroid   0.500   192     SRMT_uniform_P4   4      6967871      33106    0.4751      1589088      1589088     396582    1189740     793160     1       2    yes
    spheroid   0.500   192     SRMT_uniform_P8   8      6967871      33106    0.4751      1589088      1589088     396582    1189740     793160     1       2    yes
    spheroid   0.500   256                  MC   1     16581375      59042    0.3561           --           --      59040     177114     118076     1       2    yes
    spheroid   0.500   256                  MT   1     16581375      59042    0.3561     99488250           --     176694     530076     353384     1       2    yes
    spheroid   0.500   256     SRMT_default_P1   1     16581375      59042    0.3561      2834016      2834016     706794    2120376    1413584     1       2    yes
    spheroid   0.500   256     SRMT_default_P2   2     16581375      59042    0.3561      2834016      2834016     706794    2120376    1413584     1       2    yes
    spheroid   0.500   256     SRMT_default_P4   4     16581375      59042    0.3561      2834016      2834016     706794    2120376    1413584     1       2    yes
    spheroid   0.500   256     SRMT_default_P8   8     16581375      59042    0.3561      2834016      2834016     706794    2120376    1413584     1       2    yes
    spheroid   0.500   256     SRMT_uniform_P1   1     16581375      59042    0.3561      2834016      2834016     706894    2120676    1413784     1       2    yes
    spheroid   0.500   256     SRMT_uniform_P2   2     16581375      59042    0.3561      2834016      2834016     706894    2120676    1413784     1       2    yes
    spheroid   0.500   256     SRMT_uniform_P4   4     16581375      59042    0.3561      2834016      2834016     706894    2120676    1413784     1       2    yes
    spheroid   0.500   256     SRMT_uniform_P8   8     16581375      59042    0.3561      2834016      2834016     706894    2120676    1413784     1       2    yes
    spheroid   0.500   320                  MC   1     32461759      92186    0.2840           --           --      92184     276546     184364     1       2    yes
    spheroid   0.500   320                  MT   1     32461759      92186    0.2840    194770554           --     276358     829068     552712     1       2    yes
    spheroid   0.500   320     SRMT_default_P1   1     32461759      92186    0.2840      4424928      4424928    1106138    3318408    2212272     1       2    yes
    spheroid   0.500   320     SRMT_default_P2   2     32461759      92186    0.2840      4424928      4424928    1106138    3318408    2212272     1       2    yes
    spheroid   0.500   320     SRMT_default_P4   4     32461759      92186    0.2840      4424928      4424928    1106138    3318408    2212272     1       2    yes
    spheroid   0.500   320     SRMT_default_P8   8     32461759      92186    0.2840      4424928      4424928    1106138    3318408    2212272     1       2    yes
    spheroid   0.500   320     SRMT_uniform_P1   1     32461759      92186    0.2840      4424928      4424928    1106194    3318576    2212384     1       2    yes
    spheroid   0.500   320     SRMT_uniform_P2   2     32461759      92186    0.2840      4424928      4424928    1106194    3318576    2212384     1       2    yes
    spheroid   0.500   320     SRMT_uniform_P4   4     32461759      92186    0.2840      4424928      4424928    1106194    3318576    2212384     1       2    yes
    spheroid   0.500   320     SRMT_uniform_P8   8     32461759      92186    0.2840      4424928      4424928    1106194    3318576    2212384     1       2    yes
    spheroid   0.500   384                  MC   1     56181887     133122    0.2369           --           --     133120     399354     266236     1       2    yes
    spheroid   0.500   384                  MT   1     56181887     133122    0.2369    337091322           --     398806    1196412     797608     1       2    yes
    spheroid   0.500   384     SRMT_default_P1   1     56181887     133122    0.2369      6389856      6389856    1594970    4784904    3189936     1       2    yes
    spheroid   0.500   384     SRMT_default_P2   2     56181887     133122    0.2369      6389856      6389856    1594970    4784904    3189936     1       2    yes
    spheroid   0.500   384     SRMT_default_P4   4     56181887     133122    0.2369      6389856      6389856    1594970    4784904    3189936     1       2    yes
    spheroid   0.500   384     SRMT_default_P8   8     56181887     133122    0.2369      6389856      6389856    1594970    4784904    3189936     1       2    yes
    spheroid   0.500   384     SRMT_uniform_P1   1     56181887     133122    0.2369      6389856      6389856    1594814    4784436    3189624     1       2    yes
    spheroid   0.500   384     SRMT_uniform_P2   2     56181887     133122    0.2369      6389856      6389856    1594814    4784436    3189624     1       2    yes
    spheroid   0.500   384     SRMT_uniform_P4   4     56181887     133122    0.2369      6389856      6389856    1594814    4784436    3189624     1       2    yes
    spheroid   0.500   384     SRMT_uniform_P8   8     56181887     133122    0.2369      6389856      6389856    1594814    4784436    3189624     1       2    yes
    spheroid   0.500   448                  MC   1     89314623     181266    0.2030           --           --     181264     543786     362524     1       2    yes
    spheroid   0.500   448                  MT   1     89314623     181266    0.2030    535887738           --     543018    1629048    1086032     1       2    yes
    spheroid   0.500   448     SRMT_default_P1   1     89314623     181266    0.2030      8700768      8700768    2172074    6516216    4344144     1       2    yes
    spheroid   0.500   448     SRMT_default_P2   2     89314623     181266    0.2030      8700768      8700768    2172074    6516216    4344144     1       2    yes
    spheroid   0.500   448     SRMT_default_P4   4     89314623     181266    0.2030      8700768      8700768    2172074    6516216    4344144     1       2    yes
    spheroid   0.500   448     SRMT_default_P8   8     89314623     181266    0.2030      8700768      8700768    2172074    6516216    4344144     1       2    yes
    spheroid   0.500   448     SRMT_uniform_P1   1     89314623     181266    0.2030      8700768      8700768    2172358    6517068    4344712     1       2    yes
    spheroid   0.500   448     SRMT_uniform_P2   2     89314623     181266    0.2030      8700768      8700768    2172358    6517068    4344712     1       2    yes
    spheroid   0.500   448     SRMT_uniform_P4   4     89314623     181266    0.2030      8700768      8700768    2172358    6517068    4344712     1       2    yes
    spheroid   0.500   448     SRMT_uniform_P8   8     89314623     181266    0.2030      8700768      8700768    2172358    6517068    4344712     1       2    yes
    spheroid   0.500   512                  MC   1    133432831     236938    0.1776           --           --     236936     710802     473868     1       2    yes
    spheroid   0.500   512                  MT   1    133432831     236938    0.1776    800596986           --     709754    2129256    1419504     1       2    yes
    spheroid   0.500   512     SRMT_default_P1   1    133432831     236938    0.1776     11373024     11373024    2839050    8517144    5678096    --       2     --
    spheroid   0.500   512     SRMT_default_P2   2    133432831     236938    0.1776     11373024     11373024    2839050    8517144    5678096    --       2     --
    spheroid   0.500   512     SRMT_default_P4   4    133432831     236938    0.1776     11373024     11373024    2839050    8517144    5678096    --       2     --
    spheroid   0.500   512     SRMT_default_P8   8    133432831     236938    0.1776     11373024     11373024    2839050    8517144    5678096    --       2     --
    spheroid   0.500   512     SRMT_uniform_P1   1    133432831     236938    0.1776     11373024     11373024    2838702    8516100    5677400    --       2     --
    spheroid   0.500   512     SRMT_uniform_P2   2    133432831     236938    0.1776     11373024     11373024    2838702    8516100    5677400    --       2     --
    spheroid   0.500   512     SRMT_uniform_P4   4    133432831     236938    0.1776     11373024     11373024    2838702    8516100    5677400    --       2     --
    spheroid   0.500   512     SRMT_uniform_P8   8    133432831     236938    0.1776     11373024     11373024    2838702    8516100    5677400    --       2     --
       torus   0.500    64                  MC   1       250047      10536    4.2136           --           --      10536      31608      21072     1       0    yes
       torus   0.500    64                  MT   1       250047      10536    4.2136      1500282           --      32604      97812      65208     1       0    yes
       torus   0.500    64     SRMT_default_P1   1       250047      10536    4.2136       505728       505728     131344     394032     262688     1       0    yes
       torus   0.500    64     SRMT_default_P2   2       250047      10536    4.2136       505728       505728     131344     394032     262688     1       0    yes
       torus   0.500    64     SRMT_default_P4   4       250047      10536    4.2136       505728       505728     131344     394032     262688     1       0    yes
       torus   0.500    64     SRMT_default_P8   8       250047      10536    4.2136       505728       505728     131344     394032     262688     1       0    yes
       torus   0.500    64     SRMT_uniform_P1   1       250047      10536    4.2136       505728       505728     131224     393672     262448     1       0    yes
       torus   0.500    64     SRMT_uniform_P2   2       250047      10536    4.2136       505728       505728     131224     393672     262448     1       0    yes
       torus   0.500    64     SRMT_uniform_P4   4       250047      10536    4.2136       505728       505728     131224     393672     262448     1       0    yes
       torus   0.500    64     SRMT_uniform_P8   8       250047      10536    4.2136       505728       505728     131224     393672     262448     1       0    yes
       torus   0.500   128                  MC   1      2048383      43736    2.1351           --           --      43736     131208      87472     1       0    yes
       torus   0.500   128                  MT   1      2048383      43736    2.1351     12290298           --     133956     401868     267912     1       0    yes
       torus   0.500   128     SRMT_default_P1   1      2048383      43736    2.1351      2099328      2099328     537728    1613184    1075456     1       0    yes
       torus   0.500   128     SRMT_default_P2   2      2048383      43736    2.1351      2099328      2099328     537728    1613184    1075456     1       0    yes
       torus   0.500   128     SRMT_default_P4   4      2048383      43736    2.1351      2099328      2099328     537728    1613184    1075456     1       0    yes
       torus   0.500   128     SRMT_default_P8   8      2048383      43736    2.1351      2099328      2099328     537728    1613184    1075456     1       0    yes
       torus   0.500   128     SRMT_uniform_P1   1      2048383      43736    2.1351      2099328      2099328     537816    1613448    1075632     1       0    yes
       torus   0.500   128     SRMT_uniform_P2   2      2048383      43736    2.1351      2099328      2099328     537816    1613448    1075632     1       0    yes
       torus   0.500   128     SRMT_uniform_P4   4      2048383      43736    2.1351      2099328      2099328     537816    1613448    1075632     1       0    yes
       torus   0.500   128     SRMT_uniform_P8   8      2048383      43736    2.1351      2099328      2099328     537816    1613448    1075632     1       0    yes
       torus   0.500   192                  MC   1      6967871      99736    1.4314           --           --      99736     299208     199472     1       0    yes
       torus   0.500   192                  MT   1      6967871      99736    1.4314     41807226           --     304212     912636     608424     1       0    yes
       torus   0.500   192     SRMT_default_P1   1      6967871      99736    1.4314      4787328      4787328    1213808    3641424    2427616     1       0    yes
       torus   0.500   192     SRMT_default_P2   2      6967871      99736    1.4314      4787328      4787328    1213808    3641424    2427616     1       0    yes
       torus   0.500   192     SRMT_default_P4   4      6967871      99736    1.4314      4787328      4787328    1213808    3641424    2427616     1       0    yes
       torus   0.500   192     SRMT_default_P8   8      6967871      99736    1.4314      4787328      4787328    1213808    3641424    2427616     1       0    yes
       torus   0.500   192     SRMT_uniform_P1   1      6967871      99736    1.4314      4787328      4787328    1213544    3640632    2427088     1       0    yes
       torus   0.500   192     SRMT_uniform_P2   2      6967871      99736    1.4314      4787328      4787328    1213544    3640632    2427088     1       0    yes
       torus   0.500   192     SRMT_uniform_P4   4      6967871      99736    1.4314      4787328      4787328    1213544    3640632    2427088     1       0    yes
       torus   0.500   192     SRMT_uniform_P8   8      6967871      99736    1.4314      4787328      4787328    1213544    3640632    2427088     1       0    yes
       torus   0.500   256                  MC   1     16581375     178264    1.0751           --           --     178264     534792     356528     1       0    yes
       torus   0.500   256                  MT   1     16581375     178264    1.0751     99488250           --     543072    1629216    1086144     1       0    yes
       torus   0.500   256     SRMT_default_P1   1     16581375     178264    1.0751      8556672      8556672    2168384    6505152    4336768     1       0    yes
       torus   0.500   256     SRMT_default_P2   2     16581375     178264    1.0751      8556672      8556672    2168384    6505152    4336768     1       0    yes
       torus   0.500   256     SRMT_default_P4   4     16581375     178264    1.0751      8556672      8556672    2168384    6505152    4336768     1       0    yes
       torus   0.500   256     SRMT_default_P8   8     16581375     178264    1.0751      8556672      8556672    2168384    6505152    4336768     1       0    yes
       torus   0.500   256     SRMT_uniform_P1   1     16581375     178264    1.0751      8556672      8556672    2168736    6506208    4337472     1       0    yes
       torus   0.500   256     SRMT_uniform_P2   2     16581375     178264    1.0751      8556672      8556672    2168736    6506208    4337472     1       0    yes
       torus   0.500   256     SRMT_uniform_P4   4     16581375     178264    1.0751      8556672      8556672    2168736    6506208    4337472     1       0    yes
       torus   0.500   256     SRMT_uniform_P8   8     16581375     178264    1.0751      8556672      8556672    2168736    6506208    4337472     1       0    yes
       torus   0.500   320                  MC   1     32461759     276568    0.8520           --           --     276568     829704     553136     1       0    yes
       torus   0.500   320                  MT   1     32461759     276568    0.8520    194770554           --     846036    2538108    1692072     1       0    yes
       torus   0.500   320     SRMT_default_P1   1     32461759     276568    0.8520     13275264     13275264    3389408   10168224    6778816    --       0     --
       torus   0.500   320     SRMT_default_P2   2     32461759     276568    0.8520     13275264     13275264    3389408   10168224    6778816    --       0     --
       torus   0.500   320     SRMT_default_P4   4     32461759     276568    0.8520     13275264     13275264    3389408   10168224    6778816    --       0     --
       torus   0.500   320     SRMT_default_P8   8     32461759     276568    0.8520     13275264     13275264    3389408   10168224    6778816    --       0     --
       torus   0.500   320     SRMT_uniform_P1   1     32461759     276568    0.8520     13275264     13275264    3389212   10167636    6778424    --       0     --
       torus   0.500   320     SRMT_uniform_P2   2     32461759     276568    0.8520     13275264     13275264    3389212   10167636    6778424    --       0     --
       torus   0.500   320     SRMT_uniform_P4   4     32461759     276568    0.8520     13275264     13275264    3389212   10167636    6778424    --       0     --
       torus   0.500   320     SRMT_uniform_P8   8     32461759     276568    0.8520     13275264     13275264    3389212   10167636    6778424    --       0     --
       torus   0.500   384                  MC   1     56181887     399808    0.7116           --           --     399808    1199424     799616     1       0    yes
       torus   0.500   384                  MT   1     56181887     399808    0.7116    337091322           --    1221344    3664032    2442688     1       0    yes
       torus   0.500   384     SRMT_default_P1   1     56181887     399808    0.7116     19190784     19190784    4892624   14677872    9785248    --       0     --
       torus   0.500   384     SRMT_default_P2   2     56181887     399808    0.7116     19190784     19190784    4892624   14677872    9785248    --       0     --
       torus   0.500   384     SRMT_default_P4   4     56181887     399808    0.7116     19190784     19190784    4892624   14677872    9785248    --       0     --
       torus   0.500   384     SRMT_default_P8   8     56181887     399808    0.7116     19190784     19190784    4892624   14677872    9785248    --       0     --
       torus   0.500   384     SRMT_uniform_P1   1     56181887     399808    0.7116     19190784     19190784    4892716   14678148    9785432    --       0     --
       torus   0.500   384     SRMT_uniform_P2   2     56181887     399808    0.7116     19190784     19190784    4892716   14678148    9785432    --       0     --
       torus   0.500   384     SRMT_uniform_P4   4     56181887     399808    0.7116     19190784     19190784    4892716   14678148    9785432    --       0     --
       torus   0.500   384     SRMT_uniform_P8   8     56181887     399808    0.7116     19190784     19190784    4892716   14678148    9785432    --       0     --
       torus   0.500   448                  MC   1     89314623     546080    0.6114           --           --     546080    1638240    1092160     1       0    yes
       torus   0.500   448                  MT   1     89314623     546080    0.6114    535887738           --    1666316    4998948    3332632     1       0    yes
       torus   0.500   448     SRMT_default_P1   1     89314623     546080    0.6114     26211840     26211840    6658160   19974480   13316320    --       0     --
       torus   0.500   448     SRMT_default_P2   2     89314623     546080    0.6114     26211840     26211840    6658160   19974480   13316320    --       0     --
       torus   0.500   448     SRMT_default_P4   4     89314623     546080    0.6114     26211840     26211840    6658160   19974480   13316320    --       0     --
       torus   0.500   448     SRMT_default_P8   8     89314623     546080    0.6114     26211840     26211840    6658160   19974480   13316320    --       0     --
       torus   0.500   448     SRMT_uniform_P1   1     89314623     546080    0.6114     26211840     26211840    6658120   19974360   13316240    --       0     --
       torus   0.500   448     SRMT_uniform_P2   2     89314623     546080    0.6114     26211840     26211840    6658120   19974360   13316240    --       0     --
       torus   0.500   448     SRMT_uniform_P4   4     89314623     546080    0.6114     26211840     26211840    6658120   19974360   13316240    --       0     --
       torus   0.500   448     SRMT_uniform_P8   8     89314623     546080    0.6114     26211840     26211840    6658120   19974360   13316240    --       0     --
       torus   0.500   512                  MC   1    133432831     710152    0.5322           --           --     710152    2130456    1420304     1       0    yes
       torus   0.500   512                  MT   1    133432831     710152    0.5322    800596986           --    2171612    6514836    4343224     1       0    yes
       torus   0.500   512     SRMT_default_P1   1    133432831     710152    0.5322     34087296     34087296    8694240   26082720   17388480    --       0     --
       torus   0.500   512     SRMT_default_P2   2    133432831     710152    0.5322     34087296     34087296    8694240   26082720   17388480    --       0     --
       torus   0.500   512     SRMT_default_P4   4    133432831     710152    0.5322     34087296     34087296    8694240   26082720   17388480    --       0     --
       torus   0.500   512     SRMT_default_P8   8    133432831     710152    0.5322     34087296     34087296    8694240   26082720   17388480    --       0     --
       torus   0.500   512     SRMT_uniform_P1   1    133432831     710152    0.5322     34087296     34087296    8694328   26082984   17388656    --       0     --
       torus   0.500   512     SRMT_uniform_P2   2    133432831     710152    0.5322     34087296     34087296    8694328   26082984   17388656    --       0     --
       torus   0.500   512     SRMT_uniform_P4   4    133432831     710152    0.5322     34087296     34087296    8694328   26082984   17388656    --       0     --
       torus   0.500   512     SRMT_uniform_P8   8    133432831     710152    0.5322     34087296     34087296    8694328   26082984   17388656    --       0     --
gaussian_two   0.500    64                  MC   1       250047       2224    0.8894           --           --       2220       6648       4432     2       4    yes
gaussian_two   0.500    64                  MT   1       250047       2224    0.8894      1500282           --       6870      20598      13732     2       4    yes
gaussian_two   0.500    64     SRMT_default_P1   1       250047       2224    0.8894       106752       106752      27626      82866      55244     2       4    yes
gaussian_two   0.500    64     SRMT_default_P2   2       250047       2224    0.8894       106752       106752      27626      82866      55244     2       4    yes
gaussian_two   0.500    64     SRMT_default_P4   4       250047       2224    0.8894       106752       106752      27626      82866      55244     2       4    yes
gaussian_two   0.500    64     SRMT_default_P8   8       250047       2224    0.8894       106752       106752      27626      82866      55244     2       4    yes
gaussian_two   0.500    64     SRMT_uniform_P1   1       250047       2224    0.8894       106752       106752      27638      82902      55268     2       4    yes
gaussian_two   0.500    64     SRMT_uniform_P2   2       250047       2224    0.8894       106752       106752      27638      82902      55268     2       4    yes
gaussian_two   0.500    64     SRMT_uniform_P4   4       250047       2224    0.8894       106752       106752      27638      82902      55268     2       4    yes
gaussian_two   0.500    64     SRMT_uniform_P8   8       250047       2224    0.8894       106752       106752      27638      82902      55268     2       4    yes
gaussian_two   0.500   128                  MC   1      2048383       9226    0.4504           --           --       9222      27654      18436     2       4    yes
gaussian_two   0.500   128                  MT   1      2048383       9226    0.4504     12290298           --      28188      84552      56368     2       4    yes
gaussian_two   0.500   128     SRMT_default_P1   1      2048383       9226    0.4504       442848       442848     112832     338484     225656     2       4    yes
gaussian_two   0.500   128     SRMT_default_P2   2      2048383       9226    0.4504       442848       442848     112832     338484     225656     2       4    yes
gaussian_two   0.500   128     SRMT_default_P4   4      2048383       9226    0.4504       442848       442848     112832     338484     225656     2       4    yes
gaussian_two   0.500   128     SRMT_default_P8   8      2048383       9226    0.4504       442848       442848     112832     338484     225656     2       4    yes
gaussian_two   0.500   128     SRMT_uniform_P1   1      2048383       9226    0.4504       442848       442848     113050     339138     226092     2       4    yes
gaussian_two   0.500   128     SRMT_uniform_P2   2      2048383       9226    0.4504       442848       442848     113050     339138     226092     2       4    yes
gaussian_two   0.500   128     SRMT_uniform_P4   4      2048383       9226    0.4504       442848       442848     113050     339138     226092     2       4    yes
gaussian_two   0.500   128     SRMT_uniform_P8   8      2048383       9226    0.4504       442848       442848     113050     339138     226092     2       4    yes
gaussian_two   0.500   192                  MC   1      6967871      20836    0.2990           --           --      20832      62484      41656     2       4    yes
gaussian_two   0.500   192                  MT   1      6967871      20836    0.2990     41807226           --      63710     191118     127412     2       4    yes
gaussian_two   0.500   192     SRMT_default_P1   1      6967871      20836    0.2990      1000128      1000128     255342     766014     510676     2       4    yes
gaussian_two   0.500   192     SRMT_default_P2   2      6967871      20836    0.2990      1000128      1000128     255342     766014     510676     2       4    yes
gaussian_two   0.500   192     SRMT_default_P4   4      6967871      20836    0.2990      1000128      1000128     255342     766014     510676     2       4    yes
gaussian_two   0.500   192     SRMT_default_P8   8      6967871      20836    0.2990      1000128      1000128     255342     766014     510676     2       4    yes
gaussian_two   0.500   192     SRMT_uniform_P1   1      6967871      20836    0.2990      1000128      1000128     255862     767574     511716     2       4    yes
gaussian_two   0.500   192     SRMT_uniform_P2   2      6967871      20836    0.2990      1000128      1000128     255862     767574     511716     2       4    yes
gaussian_two   0.500   192     SRMT_uniform_P4   4      6967871      20836    0.2990      1000128      1000128     255862     767574     511716     2       4    yes
gaussian_two   0.500   192     SRMT_uniform_P8   8      6967871      20836    0.2990      1000128      1000128     255862     767574     511716     2       4    yes
gaussian_two   0.500   256                  MC   1     16581375      37094    0.2237           --           --      37090     111258      74172     2       4    yes
gaussian_two   0.500   256                  MT   1     16581375      37094    0.2237     99488250           --     113474     340410     226940     2       4    yes
gaussian_two   0.500   256     SRMT_default_P1   1     16581375      37094    0.2237      1780512      1780512     455144    1365420     910280     2       4    yes
gaussian_two   0.500   256     SRMT_default_P2   2     16581375      37094    0.2237      1780512      1780512     455144    1365420     910280     2       4    yes
gaussian_two   0.500   256     SRMT_default_P4   4     16581375      37094    0.2237      1780512      1780512     455144    1365420     910280     2       4    yes
gaussian_two   0.500   256     SRMT_default_P8   8     16581375      37094    0.2237      1780512      1780512     455144    1365420     910280     2       4    yes
gaussian_two   0.500   256     SRMT_uniform_P1   1     16581375      37094    0.2237      1780512      1780512     456078    1368222     912148     2       4    yes
gaussian_two   0.500   256     SRMT_uniform_P2   2     16581375      37094    0.2237      1780512      1780512     456078    1368222     912148     2       4    yes
gaussian_two   0.500   256     SRMT_uniform_P4   4     16581375      37094    0.2237      1780512      1780512     456078    1368222     912148     2       4    yes
gaussian_two   0.500   256     SRMT_uniform_P8   8     16581375      37094    0.2237      1780512      1780512     456078    1368222     912148     2       4    yes
gaussian_two   0.500   320                  MC   1     32461759      58166    0.1792           --           --      58162     174474     116316     2       4    yes
gaussian_two   0.500   320                  MT   1     32461759      58166    0.1792    194770554           --     177754     533250     355500     2       4    yes
gaussian_two   0.500   320     SRMT_default_P1   1     32461759      58166    0.1792      2791968      2791968     712220    2136648    1424432     2       4    yes
gaussian_two   0.500   320     SRMT_default_P2   2     32461759      58166    0.1792      2791968      2791968     712220    2136648    1424432     2       4    yes
gaussian_two   0.500   320     SRMT_default_P4   4     32461759      58166    0.1792      2791968      2791968     712220    2136648    1424432     2       4    yes
gaussian_two   0.500   320     SRMT_default_P8   8     32461759      58166    0.1792      2791968      2791968     712220    2136648    1424432     2       4    yes
gaussian_two   0.500   320     SRMT_uniform_P1   1     32461759      58166    0.1792      2791968      2791968     713886    2141646    1427764     2       4    yes
gaussian_two   0.500   320     SRMT_uniform_P2   2     32461759      58166    0.1792      2791968      2791968     713886    2141646    1427764     2       4    yes
gaussian_two   0.500   320     SRMT_uniform_P4   4     32461759      58166    0.1792      2791968      2791968     713886    2141646    1427764     2       4    yes
gaussian_two   0.500   320     SRMT_uniform_P8   8     32461759      58166    0.1792      2791968      2791968     713886    2141646    1427764     2       4    yes
gaussian_two   0.500   384                  MC   1     56181887      83796    0.1492           --           --      83792     251364     167576     2       4    yes
gaussian_two   0.500   384                  MT   1     56181887      83796    0.1492    337091322           --     256138     768402     512268     2       4    yes
gaussian_two   0.500   384     SRMT_default_P1   1     56181887      83796    0.1492      4022208      4022208    1026894    3080670    2053780     2       4    yes
gaussian_two   0.500   384     SRMT_default_P2   2     56181887      83796    0.1492      4022208      4022208    1026894    3080670    2053780     2       4    yes
gaussian_two   0.500   384     SRMT_default_P4   4     56181887      83796    0.1492      4022208      4022208    1026894    3080670    2053780     2       4    yes
gaussian_two   0.500   384     SRMT_default_P8   8     56181887      83796    0.1492      4022208      4022208    1026894    3080670    2053780     2       4    yes
gaussian_two   0.500   384     SRMT_uniform_P1   1     56181887      83796    0.1492      4022208      4022208    1028960    3086868    2057912     2       4    yes
gaussian_two   0.500   384     SRMT_uniform_P2   2     56181887      83796    0.1492      4022208      4022208    1028960    3086868    2057912     2       4    yes
gaussian_two   0.500   384     SRMT_uniform_P4   4     56181887      83796    0.1492      4022208      4022208    1028960    3086868    2057912     2       4    yes
gaussian_two   0.500   384     SRMT_uniform_P8   8     56181887      83796    0.1492      4022208      4022208    1028960    3086868    2057912     2       4    yes
gaussian_two   0.500   448                  MC   1     89314623     114064    0.1277           --           --     114056     342156     228104     2       4    yes
gaussian_two   0.500   448                  MT   1     89314623     114064    0.1277    535887738           --     348850    1046538     697692     2       4    yes
gaussian_two   0.500   448     SRMT_default_P1   1     89314623     114064    0.1277      5475072      5475072    1398470    4195398    2796932     2       4    yes
gaussian_two   0.500   448     SRMT_default_P2   2     89314623     114064    0.1277      5475072      5475072    1398470    4195398    2796932     2       4    yes
gaussian_two   0.500   448     SRMT_default_P4   4     89314623     114064    0.1277      5475072      5475072    1398470    4195398    2796932     2       4    yes
gaussian_two   0.500   448     SRMT_default_P8   8     89314623     114064    0.1277      5475072      5475072    1398470    4195398    2796932     2       4    yes
gaussian_two   0.500   448     SRMT_uniform_P1   1     89314623     114064    0.1277      5475072      5475072    1401600    4204788    2803192     2       4    yes
gaussian_two   0.500   448     SRMT_uniform_P2   2     89314623     114064    0.1277      5475072      5475072    1401600    4204788    2803192     2       4    yes
gaussian_two   0.500   448     SRMT_uniform_P4   4     89314623     114064    0.1277      5475072      5475072    1401600    4204788    2803192     2       4    yes
gaussian_two   0.500   448     SRMT_uniform_P8   8     89314623     114064    0.1277      5475072      5475072    1401600    4204788    2803192     2       4    yes
gaussian_two   0.500   512                  MC   1    133432831     149206    0.1118           --           --     149198     447582     298388     2       4    yes
gaussian_two   0.500   512                  MT   1    133432831     149206    0.1118    800596986           --     456074    1368210     912140     2       4    yes
gaussian_two   0.500   512     SRMT_default_P1   1    133432831     149206    0.1118      7161888      7161888    1828258    5484762    3656508     2       4    yes
gaussian_two   0.500   512     SRMT_default_P2   2    133432831     149206    0.1118      7161888      7161888    1828258    5484762    3656508     2       4    yes
gaussian_two   0.500   512     SRMT_default_P4   4    133432831     149206    0.1118      7161888      7161888    1828258    5484762    3656508     2       4    yes
gaussian_two   0.500   512     SRMT_default_P8   8    133432831     149206    0.1118      7161888      7161888    1828258    5484762    3656508     2       4    yes
gaussian_two   0.500   512     SRMT_uniform_P1   1    133432831     149206    0.1118      7161888      7161888    1832068    5496192    3664128     2       4    yes
gaussian_two   0.500   512     SRMT_uniform_P2   2    133432831     149206    0.1118      7161888      7161888    1832068    5496192    3664128     2       4    yes
gaussian_two   0.500   512     SRMT_uniform_P4   4    133432831     149206    0.1118      7161888      7161888    1832068    5496192    3664128     2       4    yes
gaussian_two   0.500   512     SRMT_uniform_P8   8    133432831     149206    0.1118      7161888      7161888    1832068    5496192    3664128     2       4    yes

Accuracy and computational performance
--------------------------------------
Reported statistic: median of 5 independent repeats
        Case   Level     N             Variant   P    AreaErr%     VolErr%     SurfMax MedTime(s)  Match   MedRSSMB
-------------------------------------------------------------------------------------------------------------------
    spheroid   0.500    64                  MC   1  1.4308e-01  2.8172e-01  7.0377e-03      0.004     --     46.609
    spheroid   0.500    64                  MT   1  9.7674e-02  2.1375e-01  7.6762e-03      0.048     --    293.785
    spheroid   0.500    64     SRMT_default_P1   1  1.1116e-01  2.1381e-01  6.4298e-03      0.148    yes     76.316
    spheroid   0.500    64     SRMT_default_P2   2  1.1116e-01  2.1381e-01  6.4298e-03      0.110    yes    169.352
    spheroid   0.500    64     SRMT_default_P4   4  1.1116e-01  2.1381e-01  6.4298e-03      0.084    yes    265.238
    spheroid   0.500    64     SRMT_default_P8   8  1.1116e-01  2.1381e-01  6.4298e-03      0.082    yes    432.070
    spheroid   0.500    64     SRMT_uniform_P1   1  1.1081e-01  2.1338e-01  6.4298e-03      0.146    yes     83.695
    spheroid   0.500    64     SRMT_uniform_P2   2  1.1081e-01  2.1338e-01  6.4298e-03      0.110    yes    173.992
    spheroid   0.500    64     SRMT_uniform_P4   4  1.1081e-01  2.1338e-01  6.4298e-03      0.086    yes    266.309
    spheroid   0.500    64     SRMT_uniform_P8   8  1.1081e-01  2.1338e-01  6.4298e-03      0.076    yes    431.027
    spheroid   0.500   128                  MC   1  3.5202e-02  6.9187e-02  1.8017e-03      0.019     --     69.477
    spheroid   0.500   128                  MT   1  2.4059e-02  5.2603e-02  2.0024e-03      0.338     --    860.184
    spheroid   0.500   128     SRMT_default_P1   1  2.7366e-02  5.2602e-02  1.6498e-03      0.642    yes    150.898
    spheroid   0.500   128     SRMT_default_P2   2  2.7366e-02  5.2602e-02  1.6498e-03      0.432    yes    340.359
    spheroid   0.500   128     SRMT_default_P4   4  2.7366e-02  5.2602e-02  1.6498e-03      0.277    yes    498.074
    spheroid   0.500   128     SRMT_default_P8   8  2.7366e-02  5.2602e-02  1.6498e-03      0.233    yes    730.238
    spheroid   0.500   128     SRMT_uniform_P1   1  2.7400e-02  5.2621e-02  1.6596e-03      0.633    yes    149.074
    spheroid   0.500   128     SRMT_uniform_P2   2  2.7400e-02  5.2621e-02  1.6596e-03      0.420    yes    339.566
    spheroid   0.500   128     SRMT_uniform_P4   4  2.7400e-02  5.2621e-02  1.6596e-03      0.276    yes    500.156
    spheroid   0.500   128     SRMT_uniform_P8   8  2.7400e-02  5.2621e-02  1.6596e-03      0.233    yes    734.418
    spheroid   0.500   192                  MC   1  1.5671e-02  3.0840e-02  7.6682e-04      0.061     --    127.551
    spheroid   0.500   192                  MT   1  1.0679e-02  2.3330e-02  8.9169e-04      1.122     --   2417.160
    spheroid   0.500   192     SRMT_default_P1   1  1.2136e-02  2.3330e-02  7.2162e-04      1.619    yes    272.719
    spheroid   0.500   192     SRMT_default_P2   2  1.2136e-02  2.3330e-02  7.2162e-04      1.093    yes    527.660
    spheroid   0.500   192     SRMT_default_P4   4  1.2136e-02  2.3330e-02  7.2162e-04      0.758    yes    777.840
    spheroid   0.500   192     SRMT_default_P8   8  1.2136e-02  2.3330e-02  7.2162e-04      0.635    yes   1191.289
    spheroid   0.500   192     SRMT_uniform_P1   1  1.2114e-02  2.3297e-02  7.2162e-04      1.575    yes    275.051
    spheroid   0.500   192     SRMT_uniform_P2   2  1.2114e-02  2.3297e-02  7.2162e-04      1.065    yes    550.984
    spheroid   0.500   192     SRMT_uniform_P4   4  1.2114e-02  2.3297e-02  7.2162e-04      0.750    yes    745.645
    spheroid   0.500   192     SRMT_uniform_P8   8  1.2114e-02  2.3297e-02  7.2162e-04      0.624    yes   1201.250
    spheroid   0.500   256                  MC   1  8.7475e-03  1.7207e-02  4.3688e-04      0.134     --    245.652
    spheroid   0.500   256                  MT   1  5.9697e-03  1.3047e-02  4.9754e-04      2.730     --   5454.102
    spheroid   0.500   256     SRMT_default_P1   1  6.7886e-03  1.3052e-02  4.1959e-04      3.102    yes    487.961
    spheroid   0.500   256     SRMT_default_P2   2  6.7886e-03  1.3052e-02  4.1959e-04      2.110    yes    981.148
    spheroid   0.500   256     SRMT_default_P4   4  6.7886e-03  1.3052e-02  4.1959e-04      1.500    yes   1382.570
    spheroid   0.500   256     SRMT_default_P8   8  6.7886e-03  1.3052e-02  4.1959e-04      1.294    yes   2171.504
    spheroid   0.500   256     SRMT_uniform_P1   1  6.7937e-03  1.3054e-02  4.2031e-04      3.021    yes    488.020
    spheroid   0.500   256     SRMT_uniform_P2   2  6.7937e-03  1.3054e-02  4.2031e-04      2.058    yes    981.969
    spheroid   0.500   256     SRMT_uniform_P4   4  6.7937e-03  1.3054e-02  4.2031e-04      1.495    yes   1378.602
    spheroid   0.500   256     SRMT_uniform_P8   8  6.7937e-03  1.3054e-02  4.2031e-04      1.252    yes   2144.531
    spheroid   0.500   320                  MC   1  5.6016e-03  1.1006e-02  2.8460e-04      0.257     --    430.227
    spheroid   0.500   320                  MT   1  3.8166e-03  8.3358e-03  3.1955e-04      5.298     --  10468.926
    spheroid   0.500   320     SRMT_default_P1   1  4.3388e-03  8.3352e-03  2.6927e-04      5.109    yes    773.723
    spheroid   0.500   320     SRMT_default_P2   2  4.3388e-03  8.3352e-03  2.6927e-04      3.562    yes   1702.676
    spheroid   0.500   320     SRMT_default_P4   4  4.3388e-03  8.3352e-03  2.6927e-04      2.668    yes   2227.801
    spheroid   0.500   320     SRMT_default_P8   8  4.3388e-03  8.3352e-03  2.6927e-04      2.225    yes   3524.203
    spheroid   0.500   320     SRMT_uniform_P1   1  4.3380e-03  8.3367e-03  2.6927e-04      5.026    yes    773.883
    spheroid   0.500   320     SRMT_uniform_P2   2  4.3380e-03  8.3367e-03  2.6927e-04      3.490    yes   1702.832
    spheroid   0.500   320     SRMT_uniform_P4   4  4.3380e-03  8.3367e-03  2.6927e-04      2.642    yes   2303.633
    spheroid   0.500   320     SRMT_uniform_P8   8  4.3380e-03  8.3367e-03  2.6927e-04      2.220    yes   3524.973
    spheroid   0.500   384                  MC   1  3.8834e-03  7.6331e-03  1.9068e-04      0.426     --    713.148
    spheroid   0.500   384                  MT   1  2.6493e-03  5.7887e-03  2.2073e-04      9.221     --  17963.102
    spheroid   0.500   384     SRMT_default_P1   1  3.0119e-03  5.7887e-03  1.8757e-04      8.220    yes   1172.223
    spheroid   0.500   384     SRMT_default_P2   2  3.0119e-03  5.7887e-03  1.8757e-04      5.750    yes   2377.863
    spheroid   0.500   384     SRMT_default_P4   4  3.0119e-03  5.7887e-03  1.8757e-04      4.428    yes   3437.348
    spheroid   0.500   384     SRMT_default_P8   8  3.0119e-03  5.7887e-03  1.8757e-04      3.866    yes   5342.602
    spheroid   0.500   384     SRMT_uniform_P1   1  3.0133e-03  5.7907e-03  1.8757e-04      8.103    yes   1172.234
    spheroid   0.500   384     SRMT_uniform_P2   2  3.0133e-03  5.7907e-03  1.8757e-04      5.728    yes   2371.621
    spheroid   0.500   384     SRMT_uniform_P4   4  3.0133e-03  5.7907e-03  1.8757e-04      4.424    yes   3344.383
    spheroid   0.500   384     SRMT_uniform_P8   8  3.0133e-03  5.7907e-03  1.8757e-04      3.848    yes   5349.316
    spheroid   0.500   448                  MC   1  2.8495e-03  5.6011e-03  1.4606e-04      0.672     --   1111.180
    spheroid   0.500   448                  MT   1  1.9446e-03  4.2471e-03  1.6267e-04     14.601     --  28425.867
    spheroid   0.500   448     SRMT_default_P1   1  2.2106e-03  4.2469e-03  1.3935e-04     12.192    yes   1661.617
    spheroid   0.500   448     SRMT_default_P2   2  2.2106e-03  4.2469e-03  1.3935e-04      8.633    yes   3469.410
    spheroid   0.500   448     SRMT_default_P4   4  2.2106e-03  4.2469e-03  1.3935e-04      6.862    yes   5147.672
    spheroid   0.500   448     SRMT_default_P8   8  2.2106e-03  4.2469e-03  1.3935e-04      5.993    yes   7955.828
    spheroid   0.500   448     SRMT_uniform_P1   1  2.2110e-03  4.2483e-03  1.3939e-04     12.012    yes   1661.711
    spheroid   0.500   448     SRMT_uniform_P2   2  2.2110e-03  4.2483e-03  1.3939e-04      8.579    yes   3452.770
    spheroid   0.500   448     SRMT_uniform_P4   4  2.2110e-03  4.2483e-03  1.3939e-04      6.817    yes   4960.980
    spheroid   0.500   448     SRMT_uniform_P8   8  2.2110e-03  4.2483e-03  1.3939e-04      5.993    yes   8132.098
    spheroid   0.500   512                  MC   1  2.1823e-03  4.2911e-03  1.1398e-04      0.978     --   1629.926
    spheroid   0.500   512                  MT   1  1.4877e-03  3.2501e-03  1.3428e-04     21.780     --  42358.094
    spheroid   0.500   512     SRMT_default_P1   1  1.6914e-03  3.2503e-03  1.1384e-04     17.079    yes   2324.395
    spheroid   0.500   512     SRMT_default_P2   2  1.6914e-03  3.2503e-03  1.1384e-04     12.449    yes   4930.801
    spheroid   0.500   512     SRMT_default_P4   4  1.6914e-03  3.2503e-03  1.1384e-04     10.011    yes   7254.551
    spheroid   0.500   512     SRMT_default_P8   8  1.6914e-03  3.2503e-03  1.1384e-04      8.908    yes  11706.930
    spheroid   0.500   512     SRMT_uniform_P1   1  1.6906e-03  3.2491e-03  1.1418e-04     17.018    yes   2324.379
    spheroid   0.500   512     SRMT_uniform_P2   2  1.6906e-03  3.2491e-03  1.1418e-04     12.382    yes   4931.012
    spheroid   0.500   512     SRMT_uniform_P4   4  1.6906e-03  3.2491e-03  1.1418e-04      9.957    yes   7242.836
    spheroid   0.500   512     SRMT_uniform_P8   8  1.6906e-03  3.2491e-03  1.1418e-04      8.868    yes  11514.852
       torus   0.500    64                  MC   1  4.9787e-02  1.9156e-01  1.2424e-02      0.007     --     48.789
       torus   0.500    64                  MT   1  1.0808e-02  1.4374e-01  1.2720e-02      0.058     --    301.820
       torus   0.500    64     SRMT_default_P1   1  4.4741e-02  1.4381e-01  6.5826e-03      0.479    yes    112.492
       torus   0.500    64     SRMT_default_P2   2  4.4741e-02  1.4381e-01  6.5826e-03      0.314    yes    210.496
       torus   0.500    64     SRMT_default_P4   4  4.4741e-02  1.4381e-01  6.5826e-03      0.199    yes    319.629
       torus   0.500    64     SRMT_default_P8   8  4.4741e-02  1.4381e-01  6.5826e-03      0.161    yes    529.027
       torus   0.500    64     SRMT_uniform_P1   1  4.4582e-02  1.4311e-01  6.6521e-03      0.473    yes    112.445
       torus   0.500    64     SRMT_uniform_P2   2  4.4582e-02  1.4311e-01  6.6521e-03      0.305    yes    225.039
       torus   0.500    64     SRMT_uniform_P4   4  4.4582e-02  1.4311e-01  6.6521e-03      0.199    yes    327.855
       torus   0.500    64     SRMT_uniform_P8   8  4.4582e-02  1.4311e-01  6.6521e-03      0.158    yes    521.109
       torus   0.500   128                  MC   1  1.1814e-02  4.4962e-02  2.9212e-03      0.031     --     76.910
       torus   0.500   128                  MT   1  2.1182e-03  3.4350e-02  3.1587e-03      0.380     --    882.984
       torus   0.500   128     SRMT_default_P1   1  1.0437e-02  3.4352e-02  1.5960e-03      1.963    yes    300.051
       torus   0.500   128     SRMT_default_P2   2  1.0437e-02  3.4352e-02  1.5960e-03      1.228    yes    532.391
       torus   0.500   128     SRMT_default_P4   4  1.0437e-02  3.4352e-02  1.5960e-03      0.804    yes    709.102
       torus   0.500   128     SRMT_default_P8   8  1.0437e-02  3.4352e-02  1.5960e-03      0.612    yes   1035.734
       torus   0.500   128     SRMT_uniform_P1   1  1.0464e-02  3.4381e-02  1.6505e-03      1.910    yes    300.195
       torus   0.500   128     SRMT_uniform_P2   2  1.0464e-02  3.4381e-02  1.6505e-03      1.207    yes    560.602
       torus   0.500   128     SRMT_uniform_P4   4  1.0464e-02  3.4381e-02  1.6505e-03      0.780    yes    737.469
       torus   0.500   128     SRMT_uniform_P8   8  1.0464e-02  3.4381e-02  1.6505e-03      0.601    yes   1041.500
       torus   0.500   192                  MC   1  5.2561e-03  1.9755e-02  1.2701e-03      0.087     --    140.031
       torus   0.500   192                  MT   1  9.7471e-04  1.5221e-02  1.4101e-03      1.202     --   2448.773
       torus   0.500   192     SRMT_default_P1   1  4.6414e-03  1.5220e-02  7.2608e-04      4.764    yes    620.707
       torus   0.500   192     SRMT_default_P2   2  4.6414e-03  1.5220e-02  7.2608e-04      3.023    yes    939.676
       torus   0.500   192     SRMT_default_P4   4  4.6414e-03  1.5220e-02  7.2608e-04      2.023    yes   1248.391
       torus   0.500   192     SRMT_default_P8   8  4.6414e-03  1.5220e-02  7.2608e-04      1.567    yes   1637.496
       torus   0.500   192     SRMT_uniform_P1   1  4.6365e-03  1.5202e-02  7.2655e-04      4.679    yes    620.609
       torus   0.500   192     SRMT_uniform_P2   2  4.6365e-03  1.5202e-02  7.2655e-04      2.960    yes    926.438
       torus   0.500   192     SRMT_uniform_P4   4  4.6365e-03  1.5202e-02  7.2655e-04      1.972    yes   1148.438
       torus   0.500   192     SRMT_uniform_P8   8  4.6365e-03  1.5202e-02  7.2655e-04      1.547    yes   1656.449
       torus   0.500   256                  MC   1  2.9755e-03  1.1086e-02  7.4592e-04      0.182     --    273.562
       torus   0.500   256                  MT   1  5.8117e-04  8.6170e-03  7.9621e-04      2.900     --   5453.945
       torus   0.500   256     SRMT_default_P1   1  2.6399e-03  8.6180e-03  4.4163e-04      9.482    yes   1105.551
       torus   0.500   256     SRMT_default_P2   2  2.6399e-03  8.6180e-03  4.4163e-04      5.907    yes   1678.137
       torus   0.500   256     SRMT_default_P4   4  2.6399e-03  8.6180e-03  4.4163e-04      4.141    yes   2188.832
       torus   0.500   256     SRMT_default_P8   8  2.6399e-03  8.6180e-03  4.4163e-04      3.284    yes   2818.312
       torus   0.500   256     SRMT_uniform_P1   1  2.6421e-03  8.6231e-03  4.4163e-04      9.265    yes   1105.699
       torus   0.500   256     SRMT_uniform_P2   2  2.6421e-03  8.6231e-03  4.4163e-04      5.862    yes   1706.379
       torus   0.500   256     SRMT_uniform_P4   4  2.6421e-03  8.6231e-03  4.4163e-04      4.107    yes   2236.258
       torus   0.500   256     SRMT_uniform_P8   8  2.6421e-03  8.6231e-03  4.4163e-04      3.260    yes   2814.469
       torus   0.500   320                  MC   1  1.8813e-03  7.1147e-03  5.0380e-04      0.331     --    462.383
       torus   0.500   320                  MT   1  3.4865e-04  5.4534e-03  5.1168e-04      5.569     --  10469.199
       torus   0.500   320     SRMT_default_P1   1  1.6649e-03  5.4545e-03  3.7951e-04     15.511    yes   1759.648
       torus   0.500   320     SRMT_default_P2   2  1.6649e-03  5.4545e-03  3.7951e-04     10.055    yes   2888.988
       torus   0.500   320     SRMT_default_P4   4  1.6649e-03  5.4545e-03  3.7951e-04      7.167    yes   3481.926
       torus   0.500   320     SRMT_default_P8   8  1.6649e-03  5.4545e-03  3.7951e-04      5.800    yes   5049.410
       torus   0.500   320     SRMT_uniform_P1   1  1.6633e-03  5.4527e-03  3.7951e-04     15.143    yes   1759.750
       torus   0.500   320     SRMT_uniform_P2   2  1.6633e-03  5.4527e-03  3.7951e-04      9.922    yes   2906.395
       torus   0.500   320     SRMT_uniform_P4   4  1.6633e-03  5.4527e-03  3.7951e-04      7.129    yes   3468.336
       torus   0.500   320     SRMT_uniform_P8   8  1.6633e-03  5.4527e-03  3.7951e-04      5.771    yes   4919.398
       torus   0.500   384                  MC   1  1.3006e-03  4.9097e-03  3.6072e-04      0.534     --    776.832
       torus   0.500   384                  MT   1  2.3858e-04  3.7809e-03  4.2101e-04      9.668     --  17963.902
       torus   0.500   384     SRMT_default_P1   1  1.1511e-03  3.7807e-03  3.6031e-04     22.796    yes   2573.266
       torus   0.500   384     SRMT_default_P2   2  1.1511e-03  3.7807e-03  3.6031e-04     15.088    yes   3888.180
       torus   0.500   384     SRMT_default_P4   4  1.1511e-03  3.7807e-03  3.6031e-04     10.657    yes   4919.902
       torus   0.500   384     SRMT_default_P8   8  1.1511e-03  3.7807e-03  3.6031e-04      8.758    yes   7223.441
       torus   0.500   384     SRMT_uniform_P1   1  1.1521e-03  3.7811e-03  3.6031e-04     22.425    yes   2573.578
       torus   0.500   384     SRMT_uniform_P2   2  1.1521e-03  3.7811e-03  3.6031e-04     14.896    yes   3888.812
       torus   0.500   384     SRMT_uniform_P4   4  1.1521e-03  3.7811e-03  3.6031e-04     10.478    yes   4928.996
       torus   0.500   384     SRMT_uniform_P8   8  1.1521e-03  3.7811e-03  3.6031e-04      8.691    yes   7235.031
       torus   0.500   448                  MC   1  9.6584e-04  3.6105e-03  3.3757e-04      0.807     --   1171.309
       torus   0.500   448                  MT   1  1.8561e-04  2.7926e-03  3.9697e-04     15.167     --  28429.121
       torus   0.500   448     SRMT_default_P1   1  8.5535e-04  2.7922e-03  3.3756e-04     32.264    yes   3609.477
       torus   0.500   448     SRMT_default_P2   2  8.5535e-04  2.7922e-03  3.3756e-04     21.704    yes   5457.152
       torus   0.500   448     SRMT_default_P4   4  8.5535e-04  2.7922e-03  3.3756e-04     15.766    yes   6829.074
       torus   0.500   448     SRMT_default_P8   8  8.5535e-04  2.7922e-03  3.3756e-04     12.936    yes  10496.402
       torus   0.500   448     SRMT_uniform_P1   1  8.5518e-04  2.7937e-03  3.3858e-04     31.713    yes   3609.531
       torus   0.500   448     SRMT_uniform_P2   2  8.5518e-04  2.7937e-03  3.3858e-04     21.472    yes   5437.566
       torus   0.500   448     SRMT_uniform_P4   4  8.5518e-04  2.7937e-03  3.3858e-04     15.599    yes   6822.191
       torus   0.500   448     SRMT_uniform_P8   8  8.5518e-04  2.7937e-03  3.3858e-04     12.935    yes  10496.418
       torus   0.500   512                  MC   1  7.4108e-04  2.7862e-03  3.3972e-04      1.162     --   1706.184
       torus   0.500   512                  MT   1  1.4486e-04  2.1432e-03  3.7361e-04     22.429     --  42358.648
       torus   0.500   512     SRMT_default_P1   1  6.5732e-04  2.1430e-03  3.3968e-04     42.038    yes   4807.016
       torus   0.500   512     SRMT_default_P2   2  6.5732e-04  2.1430e-03  3.3968e-04     28.545    yes   7447.559
       torus   0.500   512     SRMT_default_P4   4  6.5732e-04  2.1430e-03  3.3968e-04     20.863    yes   9607.230
       torus   0.500   512     SRMT_default_P8   8  6.5732e-04  2.1430e-03  3.3968e-04     17.240    yes  14702.590
       torus   0.500   512     SRMT_uniform_P1   1  6.5753e-04  2.1434e-03  3.3971e-04     41.789    yes   4807.211
       torus   0.500   512     SRMT_uniform_P2   2  6.5753e-04  2.1434e-03  3.3971e-04     28.164    yes   7447.777
       torus   0.500   512     SRMT_uniform_P4   4  6.5753e-04  2.1434e-03  3.3971e-04     20.725    yes   9607.430
       torus   0.500   512     SRMT_uniform_P8   8  6.5753e-04  2.1434e-03  3.3971e-04     17.105    yes  14662.387
gaussian_two   0.500    64                  MC   1  6.0018e-01  1.0905e+00  4.2980e-02      0.003     --     90.309
gaussian_two   0.500    64                  MT   1  4.2751e-01  8.5424e-01  4.2363e-02      0.045     --    334.383
gaussian_two   0.500    64     SRMT_default_P1   1  4.9718e-01  8.7065e-01  4.2925e-02      0.090    yes    116.031
gaussian_two   0.500    64     SRMT_default_P2   2  4.9718e-01  8.7065e-01  4.2925e-02      0.073    yes    259.523
gaussian_two   0.500    64     SRMT_default_P4   4  4.9718e-01  8.7065e-01  4.2925e-02      0.058    yes    398.004
gaussian_two   0.500    64     SRMT_default_P8   8  4.9718e-01  8.7065e-01  4.2925e-02      0.056    yes    684.293
gaussian_two   0.500    64     SRMT_uniform_P1   1  5.0135e-01  8.7385e-01  4.2925e-02      0.089    yes    115.836
gaussian_two   0.500    64     SRMT_uniform_P2   2  5.0135e-01  8.7385e-01  4.2925e-02      0.067    yes    260.195
gaussian_two   0.500    64     SRMT_uniform_P4   4  5.0135e-01  8.7385e-01  4.2925e-02      0.055    yes    397.402
gaussian_two   0.500    64     SRMT_uniform_P8   8  5.0135e-01  8.7385e-01  4.2925e-02      0.056    yes    685.055
gaussian_two   0.500   128                  MC   1  1.4650e-01  2.6699e-01  1.1344e-02      0.016     --    118.289
gaussian_two   0.500   128                  MT   1  1.0364e-01  2.0943e-01  1.1254e-02      0.333     --    922.949
gaussian_two   0.500   128     SRMT_default_P1   1  1.2096e-01  2.1336e-01  1.1499e-02      0.419    yes    165.152
gaussian_two   0.500   128     SRMT_default_P2   2  1.2096e-01  2.1336e-01  1.1499e-02      0.280    yes    399.426
gaussian_two   0.500   128     SRMT_default_P4   4  1.2096e-01  2.1336e-01  1.1499e-02      0.188    yes    600.574
gaussian_two   0.500   128     SRMT_default_P8   8  1.2096e-01  2.1336e-01  1.1499e-02      0.160    yes   1054.746
gaussian_two   0.500   128     SRMT_uniform_P1   1  1.2172e-01  2.1428e-01  1.1499e-02      0.412    yes    165.922
gaussian_two   0.500   128     SRMT_uniform_P2   2  1.2172e-01  2.1428e-01  1.1499e-02      0.287    yes    399.762
gaussian_two   0.500   128     SRMT_uniform_P4   4  1.2172e-01  2.1428e-01  1.1499e-02      0.183    yes    600.594
gaussian_two   0.500   128     SRMT_uniform_P8   8  1.2172e-01  2.1428e-01  1.1499e-02      0.163    yes   1055.441
gaussian_two   0.500   192                  MC   1  6.3071e-02  1.1552e-01  5.2765e-03      0.055     --    170.207
gaussian_two   0.500   192                  MT   1  4.4137e-02  8.9927e-02  5.2309e-03      1.097     --   2459.172
gaussian_two   0.500   192     SRMT_default_P1   1  5.1817e-02  9.1709e-02  5.3075e-03      1.093    yes    253.273
gaussian_two   0.500   192     SRMT_default_P2   2  5.1817e-02  9.1709e-02  5.3075e-03      0.767    yes    559.492
gaussian_two   0.500   192     SRMT_default_P4   4  5.1817e-02  9.1709e-02  5.3075e-03      0.550    yes    845.125
gaussian_two   0.500   192     SRMT_default_P8   8  5.1817e-02  9.1709e-02  5.3075e-03      0.463    yes   1359.004
gaussian_two   0.500   192     SRMT_uniform_P1   1  5.2244e-02  9.2122e-02  5.3075e-03      1.071    yes    254.508
gaussian_two   0.500   192     SRMT_uniform_P2   2  5.2244e-02  9.2122e-02  5.3075e-03      0.731    yes    558.980
gaussian_two   0.500   192     SRMT_uniform_P4   4  5.2244e-02  9.2122e-02  5.3075e-03      0.544    yes    835.621
gaussian_two   0.500   192     SRMT_uniform_P8   8  5.2244e-02  9.2122e-02  5.3075e-03      0.450    yes   1345.824
gaussian_two   0.500   256                  MC   1  3.4664e-02  6.3113e-02  2.9007e-03      0.126     --    284.746
gaussian_two   0.500   256                  MT   1  2.4080e-02  4.8814e-02  2.8405e-03      2.746     --   5496.406
gaussian_two   0.500   256     SRMT_default_P1   1  2.8356e-02  4.9792e-02  2.8620e-03      2.103    yes    412.016
gaussian_two   0.500   256     SRMT_default_P2   2  2.8356e-02  4.9792e-02  2.8620e-03      1.463    yes    942.496
gaussian_two   0.500   256     SRMT_default_P4   4  2.8356e-02  4.9792e-02  2.8620e-03      1.120    yes   1373.355
gaussian_two   0.500   256     SRMT_default_P8   8  2.8356e-02  4.9792e-02  2.8620e-03      0.983    yes   2274.906
gaussian_two   0.500   256     SRMT_uniform_P1   1  2.8603e-02  5.0056e-02  2.8620e-03      2.036    yes    412.523
gaussian_two   0.500   256     SRMT_uniform_P2   2  2.8603e-02  5.0056e-02  2.8620e-03      1.452    yes    938.789
gaussian_two   0.500   256     SRMT_uniform_P4   4  2.8603e-02  5.0056e-02  2.8620e-03      1.128    yes   1370.332
gaussian_two   0.500   256     SRMT_uniform_P8   8  2.8603e-02  5.0056e-02  2.8620e-03      0.972    yes   2288.965
gaussian_two   0.500   320                  MC   1  2.1374e-02  3.9157e-02  1.8870e-03      0.242     --    468.961
gaussian_two   0.500   320                  MT   1  1.4612e-02  3.0014e-02  1.8877e-03      5.182     --  10512.125
gaussian_two   0.500   320     SRMT_default_P1   1  1.7347e-02  3.0643e-02  1.8995e-03      3.579    yes    650.953
gaussian_two   0.500   320     SRMT_default_P2   2  1.7347e-02  3.0643e-02  1.8995e-03      2.584    yes   1528.426
gaussian_two   0.500   320     SRMT_default_P4   4  1.7347e-02  3.0643e-02  1.8995e-03      2.028    yes   2189.742
gaussian_two   0.500   320     SRMT_default_P8   8  1.7347e-02  3.0643e-02  1.8995e-03      1.770    yes   3529.383
gaussian_two   0.500   320     SRMT_uniform_P1   1  1.7507e-02  3.0807e-02  1.8995e-03      3.541    yes    651.676
gaussian_two   0.500   320     SRMT_uniform_P2   2  1.7507e-02  3.0807e-02  1.8995e-03      2.557    yes   1527.629
gaussian_two   0.500   320     SRMT_uniform_P4   4  1.7507e-02  3.0807e-02  1.8995e-03      2.005    yes   2196.023
gaussian_two   0.500   320     SRMT_uniform_P8   8  1.7507e-02  3.0807e-02  1.8995e-03      1.770    yes   3531.438
gaussian_two   0.500   384                  MC   1  1.4266e-02  2.6009e-02  1.3238e-03      0.405     --    747.715
gaussian_two   0.500   384                  MT   1  9.5803e-03  1.9668e-02  1.2845e-03      9.191     --  18005.797
gaussian_two   0.500   384     SRMT_default_P1   1  1.1469e-02  2.0100e-02  1.3368e-03      5.654    yes    963.293
gaussian_two   0.500   384     SRMT_default_P2   2  1.1469e-02  2.0100e-02  1.3368e-03      4.203    yes   2143.930
gaussian_two   0.500   384     SRMT_default_P4   4  1.1469e-02  2.0100e-02  1.3368e-03      3.388    yes   3210.766
gaussian_two   0.500   384     SRMT_default_P8   8  1.1469e-02  2.0100e-02  1.3368e-03      2.980    yes   5263.695
gaussian_two   0.500   384     SRMT_uniform_P1   1  1.1574e-02  2.0205e-02  1.3368e-03      5.597    yes    964.305
gaussian_two   0.500   384     SRMT_uniform_P2   2  1.1574e-02  2.0205e-02  1.3368e-03      4.167    yes   2144.762
gaussian_two   0.500   384     SRMT_uniform_P4   4  1.1574e-02  2.0205e-02  1.3368e-03      3.383    yes   3239.133
gaussian_two   0.500   384     SRMT_uniform_P8   8  1.1574e-02  2.0205e-02  1.3368e-03      2.970    yes   5230.098
gaussian_two   0.500   448                  MC   1  9.9291e-03  1.8147e-02  1.0162e-03      0.636     --   1132.754
gaussian_two   0.500   448                  MT   1  6.4895e-03  1.3484e-02  1.0115e-03     14.269     --  28468.461
gaussian_two   0.500   448     SRMT_default_P1   1  7.8743e-03  1.3802e-02  1.0138e-03      8.635    yes   1395.230
gaussian_two   0.500   448     SRMT_default_P2   2  7.8743e-03  1.3802e-02  1.0138e-03      6.542    yes   3182.207
gaussian_two   0.500   448     SRMT_default_P4   4  7.8743e-03  1.3802e-02  1.0138e-03      5.409    yes   4733.516
gaussian_two   0.500   448     SRMT_default_P8   8  7.8743e-03  1.3802e-02  1.0138e-03      4.851    yes   7839.609
gaussian_two   0.500   448     SRMT_uniform_P1   1  7.9533e-03  1.3884e-02  1.0159e-03      8.512    yes   1396.426
gaussian_two   0.500   448     SRMT_uniform_P2   2  7.9533e-03  1.3884e-02  1.0159e-03      6.464    yes   3181.539
gaussian_two   0.500   448     SRMT_uniform_P4   4  7.9533e-03  1.3884e-02  1.0159e-03      5.367    yes   4730.180
gaussian_two   0.500   448     SRMT_uniform_P8   8  7.9533e-03  1.3884e-02  1.0159e-03      4.843    yes   7852.340
gaussian_two   0.500   512                  MC   1  7.1347e-03  1.3068e-02  7.7997e-04      0.951     --   1648.023
gaussian_two   0.500   512                  MT   1  4.5051e-03  9.4972e-03  7.8034e-04     21.391     --  42404.789
gaussian_two   0.500   512     SRMT_default_P1   1  5.5633e-03  9.7414e-03  7.8061e-04     12.215    yes   1898.781
gaussian_two   0.500   512     SRMT_default_P2   2  5.5633e-03  9.7414e-03  7.8061e-04      9.359    yes   4417.082
gaussian_two   0.500   512     SRMT_default_P4   4  5.5633e-03  9.7414e-03  7.8061e-04      7.896    yes   6823.863
gaussian_two   0.500   512     SRMT_default_P8   8  5.5633e-03  9.7414e-03  7.8061e-04      7.134    yes  11216.785
gaussian_two   0.500   512     SRMT_uniform_P1   1  5.6223e-03  9.7975e-03  7.8160e-04     12.027    yes   1900.488
gaussian_two   0.500   512     SRMT_uniform_P2   2  5.6223e-03  9.7975e-03  7.8160e-04      9.297    yes   4419.703
gaussian_two   0.500   512     SRMT_uniform_P4   4  5.6223e-03  9.7975e-03  7.8160e-04      7.835    yes   6832.926
gaussian_two   0.500   512     SRMT_uniform_P8   8  5.6223e-03  9.7975e-03  7.8160e-04      7.133    yes  11212.016

Geometry against the fixed original-grid trilinear field (repeat 1)
R_h: vertices+centroids; Theta_h: area-weighted, local-ascent normals; q05: unweighted triangle percentile.
        Case   Level     N             Variant   P         NF           R_h  Theta_h(deg)        q05         Status  NormalArea
-------------------------------------------------------------------------------------------------------------------------------
    spheroid   0.500    64                  MC   1       7212  5.784908e-04      0.262185   0.136300          valid    1.000000
    spheroid   0.500    64                  MT   1      21640  1.255395e-03      0.880785   0.152090          valid    1.000000
    spheroid   0.500    64     SRMT_default_P1   1      86544  3.077258e-04      0.434753   0.115527          valid    1.000000
    spheroid   0.500    64     SRMT_default_P2   2      86544  3.077258e-04      0.434753   0.115527          valid    1.000000
    spheroid   0.500    64     SRMT_default_P4   4      86544  3.077258e-04      0.434753   0.115527          valid    1.000000
    spheroid   0.500    64     SRMT_default_P8   8      86544  3.077258e-04      0.434753   0.115527          valid    1.000000
    spheroid   0.500    64     SRMT_uniform_P1   1      86424  3.175441e-04      0.435577   0.112592          valid    1.000000
    spheroid   0.500    64     SRMT_uniform_P2   2      86424  3.175441e-04      0.435577   0.112592          valid    1.000000
    spheroid   0.500    64     SRMT_uniform_P4   4      86424  3.175441e-04      0.435577   0.112592          valid    1.000000
    spheroid   0.500    64     SRMT_uniform_P8   8      86424  3.175441e-04      0.435577   0.112592          valid    1.000000
    spheroid   0.500   128                  MC   1      29228  1.488405e-04      0.126727   0.123333          valid    1.000000
    spheroid   0.500   128                  MT   1      87512  3.103115e-04      0.435655   0.136517          valid    1.000000
    spheroid   0.500   128     SRMT_default_P1   1     350576  7.849260e-05      0.215583   0.114785          valid    1.000000
    spheroid   0.500   128     SRMT_default_P2   2     350576  7.849260e-05      0.215583   0.114785          valid    1.000000
    spheroid   0.500   128     SRMT_default_P4   4     350576  7.849260e-05      0.215583   0.114785          valid    1.000000
    spheroid   0.500   128     SRMT_default_P8   8     350576  7.849260e-05      0.215583   0.114785          valid    1.000000
    spheroid   0.500   128     SRMT_uniform_P1   1     350616  7.849260e-05      0.215949   0.112955          valid    1.000000
    spheroid   0.500   128     SRMT_uniform_P2   2     350616  7.849260e-05      0.215949   0.112955          valid    1.000000
    spheroid   0.500   128     SRMT_uniform_P4   4     350616  7.849260e-05      0.215949   0.112955          valid    1.000000
    spheroid   0.500   128     SRMT_uniform_P8   8     350616  7.849260e-05      0.215949   0.112955          valid    1.000000
    spheroid   0.500   192                  MC   1      66204  6.544976e-05      0.085021   0.100137          valid    1.000000
    spheroid   0.500   192                  MT   1     198416  1.364589e-04      0.288167   0.111194          valid    1.000000
    spheroid   0.500   192     SRMT_default_P1   1     793424  3.468053e-05      0.143980   0.114515          valid    1.000000
    spheroid   0.500   192     SRMT_default_P2   2     793424  3.468053e-05      0.143980   0.114515          valid    1.000000
    spheroid   0.500   192     SRMT_default_P4   4     793424  3.468053e-05      0.143980   0.114515          valid    1.000000
    spheroid   0.500   192     SRMT_default_P8   8     793424  3.468053e-05      0.143980   0.114515          valid    1.000000
    spheroid   0.500   192     SRMT_uniform_P1   1     793160  3.468053e-05      0.143804   0.116667          valid    1.000000
    spheroid   0.500   192     SRMT_uniform_P2   2     793160  3.468053e-05      0.143804   0.116667          valid    1.000000
    spheroid   0.500   192     SRMT_uniform_P4   4     793160  3.468053e-05      0.143804   0.116667          valid    1.000000
    spheroid   0.500   192     SRMT_uniform_P8   8     793160  3.468053e-05      0.143804   0.116667          valid    1.000000
    spheroid   0.500   256                  MC   1     118076  3.788856e-05      0.063777   0.101458          valid    1.000000
    spheroid   0.500   256                  MT   1     353384  7.704101e-05      0.215669   0.120072          valid    1.000000
    spheroid   0.500   256     SRMT_default_P1   1    1413584  1.934592e-05      0.107688   0.117211          valid    1.000000
    spheroid   0.500   256     SRMT_default_P2   2    1413584  1.934592e-05      0.107688   0.117211          valid    1.000000
    spheroid   0.500   256     SRMT_default_P4   4    1413584  1.934592e-05      0.107688   0.117211          valid    1.000000
    spheroid   0.500   256     SRMT_default_P8   8    1413584  1.934592e-05      0.107688   0.117211          valid    1.000000
    spheroid   0.500   256     SRMT_uniform_P1   1    1413784  1.934592e-05      0.107698   0.116634          valid    1.000000
    spheroid   0.500   256     SRMT_uniform_P2   2    1413784  1.934592e-05      0.107698   0.116634          valid    1.000000
    spheroid   0.500   256     SRMT_uniform_P4   4    1413784  1.934592e-05      0.107698   0.116634          valid    1.000000
    spheroid   0.500   256     SRMT_uniform_P8   8    1413784  1.934592e-05      0.107698   0.116634          valid    1.000000
    spheroid   0.500   320                  MC   1     184364  2.369807e-05      0.050388   0.098252          valid    1.000000
    spheroid   0.500   320                  MT   1     552712  4.919414e-05      0.172743   0.118077          valid    1.000000
    spheroid   0.500   320     SRMT_default_P1   1    2212272  1.241313e-05      0.086196   0.116674          valid    1.000000
    spheroid   0.500   320     SRMT_default_P2   2    2212272  1.241313e-05      0.086196   0.116674          valid    1.000000
    spheroid   0.500   320     SRMT_default_P4   4    2212272  1.241313e-05      0.086196   0.116674          valid    1.000000
    spheroid   0.500   320     SRMT_default_P8   8    2212272  1.241313e-05      0.086196   0.116674          valid    1.000000
    spheroid   0.500   320     SRMT_uniform_P1   1    2212384  1.241313e-05      0.086101   0.116180          valid    1.000000
    spheroid   0.500   320     SRMT_uniform_P2   2    2212384  1.241313e-05      0.086101   0.116180          valid    1.000000
    spheroid   0.500   320     SRMT_uniform_P4   4    2212384  1.241313e-05      0.086101   0.116180          valid    1.000000
    spheroid   0.500   320     SRMT_uniform_P8   8    2212384  1.241313e-05      0.086101   0.116180          valid    1.000000
    spheroid   0.500   384                  MC   1     266236  1.650124e-05      0.042225   0.101019          valid    1.000000
    spheroid   0.500   384                  MT   1     797608  3.414484e-05      0.143882   0.116568          valid    1.000000
    spheroid   0.500   384     SRMT_default_P1   1    3189936  8.584131e-06      0.071732   0.112676          valid    1.000000
    spheroid   0.500   384     SRMT_default_P2   2    3189936  8.584131e-06      0.071732   0.112676          valid    1.000000
    spheroid   0.500   384     SRMT_default_P4   4    3189936  8.584131e-06      0.071732   0.112676          valid    1.000000
    spheroid   0.500   384     SRMT_default_P8   8    3189936  8.584131e-06      0.071732   0.112676          valid    1.000000
    spheroid   0.500   384     SRMT_uniform_P1   1    3189624  8.584131e-06      0.071687   0.113034          valid    1.000000
    spheroid   0.500   384     SRMT_uniform_P2   2    3189624  8.584131e-06      0.071687   0.113034          valid    1.000000
    spheroid   0.500   384     SRMT_uniform_P4   4    3189624  8.584131e-06      0.071687   0.113034          valid    1.000000
    spheroid   0.500   384     SRMT_uniform_P8   8    3189624  8.584131e-06      0.071687   0.113034          valid    1.000000
    spheroid   0.500   448                  MC   1     362524  1.222336e-05      0.036120   0.108430          valid    1.000000
    spheroid   0.500   448                  MT   1    1086032  2.511739e-05      0.123315   0.121690          valid    1.000000
    spheroid   0.500   448     SRMT_default_P1   1    4344144  6.297353e-06      0.061407   0.115880          valid    1.000000
    spheroid   0.500   448     SRMT_default_P2   2    4344144  6.297353e-06      0.061407   0.115880          valid    1.000000
    spheroid   0.500   448     SRMT_default_P4   4    4344144  6.297353e-06      0.061407   0.115880          valid    1.000000
    spheroid   0.500   448     SRMT_default_P8   8    4344144  6.297353e-06      0.061407   0.115880          valid    1.000000
    spheroid   0.500   448     SRMT_uniform_P1   1    4344712  6.297353e-06      0.061417   0.113381          valid    1.000000
    spheroid   0.500   448     SRMT_uniform_P2   2    4344712  6.297353e-06      0.061417   0.113381          valid    1.000000
    spheroid   0.500   448     SRMT_uniform_P4   4    4344712  6.297353e-06      0.061417   0.113381          valid    1.000000
    spheroid   0.500   448     SRMT_uniform_P8   8    4344712  6.297353e-06      0.061417   0.113381          valid    1.000000
    spheroid   0.500   512                  MC   1     473868  9.284979e-06      0.031729   0.095336          valid    1.000000
    spheroid   0.500   512                  MT   1    1419504  1.923069e-05      0.107766   0.114857          valid    1.000000
    spheroid   0.500   512     SRMT_default_P1   1    5678096  4.820328e-06      0.053706   0.114669          valid    1.000000
    spheroid   0.500   512     SRMT_default_P2   2    5678096  4.820328e-06      0.053706   0.114669          valid    1.000000
    spheroid   0.500   512     SRMT_default_P4   4    5678096  4.820328e-06      0.053706   0.114669          valid    1.000000
    spheroid   0.500   512     SRMT_default_P8   8    5678096  4.820328e-06      0.053706   0.114669          valid    1.000000
    spheroid   0.500   512     SRMT_uniform_P1   1    5677400  4.820328e-06      0.053753   0.117464          valid    1.000000
    spheroid   0.500   512     SRMT_uniform_P2   2    5677400  4.820328e-06      0.053753   0.117464          valid    1.000000
    spheroid   0.500   512     SRMT_uniform_P4   4    5677400  4.820328e-06      0.053753   0.117464          valid    1.000000
    spheroid   0.500   512     SRMT_uniform_P8   8    5677400  4.820328e-06      0.053753   0.117464          valid    1.000000
       torus   0.500    64                  MC   1      21072  1.650159e-03      0.759039   0.094061          valid    1.000000
       torus   0.500    64                  MT   1      65208  3.297794e-03      1.357849   0.073684          valid    1.000000
       torus   0.500    64     SRMT_default_P1   1     262688  7.371376e-04      0.674911   0.089086          valid    1.000000
       torus   0.500    64     SRMT_default_P2   2     262688  7.371376e-04      0.674911   0.089086          valid    1.000000
       torus   0.500    64     SRMT_default_P4   4     262688  7.371376e-04      0.674911   0.089086          valid    1.000000
       torus   0.500    64     SRMT_default_P8   8     262688  7.371376e-04      0.674911   0.089086          valid    1.000000
       torus   0.500    64     SRMT_uniform_P1   1     262448  8.138029e-04      0.678999   0.099522          valid    1.000000
       torus   0.500    64     SRMT_uniform_P2   2     262448  8.138029e-04      0.678999   0.099522          valid    1.000000
       torus   0.500    64     SRMT_uniform_P4   4     262448  8.138029e-04      0.678999   0.099522          valid    1.000000
       torus   0.500    64     SRMT_uniform_P8   8     262448  8.138029e-04      0.678999   0.099522          valid    1.000000
       torus   0.500   128                  MC   1      87472  5.003105e-04      0.373082   0.113545          valid    1.000000
       torus   0.500   128                  MT   1     267912  8.095602e-04      0.680384   0.119217          valid    1.000000
       torus   0.500   128     SRMT_default_P1   1    1075456  1.989465e-04      0.338937   0.113012          valid    1.000000
       torus   0.500   128     SRMT_default_P2   2    1075456  1.989465e-04      0.338937   0.113012          valid    1.000000
       torus   0.500   128     SRMT_default_P4   4    1075456  1.989465e-04      0.338937   0.113012          valid    1.000000
       torus   0.500   128     SRMT_default_P8   8    1075456  1.989465e-04      0.338937   0.113012          valid    1.000000
       torus   0.500   128     SRMT_uniform_P1   1    1075632  2.013041e-04      0.338203   0.111837          valid    1.000000
       torus   0.500   128     SRMT_uniform_P2   2    1075632  2.013041e-04      0.338203   0.111837          valid    1.000000
       torus   0.500   128     SRMT_uniform_P4   4    1075632  2.013041e-04      0.338203   0.111837          valid    1.000000
       torus   0.500   128     SRMT_uniform_P8   8    1075632  2.013041e-04      0.338203   0.111837          valid    1.000000
       torus   0.500   192                  MC   1     199472  2.498480e-04      0.248309   0.114111          valid    1.000000
       torus   0.500   192                  MT   1     608424  3.580249e-04      0.451327   0.116539          valid    1.000000
       torus   0.500   192     SRMT_default_P1   1    2427616  8.897221e-05      0.224896   0.114513          valid    1.000000
       torus   0.500   192     SRMT_default_P2   2    2427616  8.897221e-05      0.224896   0.114513          valid    1.000000
       torus   0.500   192     SRMT_default_P4   4    2427616  8.897221e-05      0.224896   0.114513          valid    1.000000
       torus   0.500   192     SRMT_default_P8   8    2427616  8.897221e-05      0.224896   0.114513          valid    1.000000
       torus   0.500   192     SRMT_uniform_P1   1    2427088  8.955544e-05      0.225101   0.115645          valid    1.000000
       torus   0.500   192     SRMT_uniform_P2   2    2427088  8.955544e-05      0.225101   0.115645          valid    1.000000
       torus   0.500   192     SRMT_uniform_P4   4    2427088  8.955544e-05      0.225101   0.115645          valid    1.000000
       torus   0.500   192     SRMT_uniform_P8   8    2427088  8.955544e-05      0.225101   0.115645          valid    1.000000
       torus   0.500   256                  MC   1     356528  1.472236e-04      0.185593   0.114939          valid    1.000000
       torus   0.500   256                  MT   1    1086144  2.009200e-04      0.337347   0.111038          valid    1.000000
       torus   0.500   256     SRMT_default_P1   1    4336768  5.020144e-05      0.168235   0.110001          valid    1.000000
       torus   0.500   256     SRMT_default_P2   2    4336768  5.020144e-05      0.168235   0.110001          valid    1.000000
       torus   0.500   256     SRMT_default_P4   4    4336768  5.020144e-05      0.168235   0.110001          valid    1.000000
       torus   0.500   256     SRMT_default_P8   8    4336768  5.020144e-05      0.168235   0.110001          valid    1.000000
       torus   0.500   256     SRMT_uniform_P1   1    4337472  5.031722e-05      0.168298   0.110156          valid    1.000000
       torus   0.500   256     SRMT_uniform_P2   2    4337472  5.031722e-05      0.168298   0.110156          valid    1.000000
       torus   0.500   256     SRMT_uniform_P4   4    4337472  5.031722e-05      0.168298   0.110156          valid    1.000000
       torus   0.500   256     SRMT_uniform_P8   8    4337472  5.031722e-05      0.168298   0.110156          valid    1.000000
       torus   0.500   320                  MC   1     553136  9.784336e-05      0.148633   0.112005          valid    1.000000
       torus   0.500   320                  MT   1    1692072  1.276096e-04      0.270335   0.118363          valid    1.000000
       torus   0.500   320     SRMT_default_P1   1    6778816  3.197515e-05      0.134746   0.115064          valid    1.000000
       torus   0.500   320     SRMT_default_P2   2    6778816  3.197515e-05      0.134746   0.115064          valid    1.000000
       torus   0.500   320     SRMT_default_P4   4    6778816  3.197515e-05      0.134746   0.115064          valid    1.000000
       torus   0.500   320     SRMT_default_P8   8    6778816  3.197515e-05      0.134746   0.115064          valid    1.000000
       torus   0.500   320     SRMT_uniform_P1   1    6778424  3.239583e-05      0.134718   0.113827          valid    1.000000
       torus   0.500   320     SRMT_uniform_P2   2    6778424  3.239583e-05      0.134718   0.113827          valid    1.000000
       torus   0.500   320     SRMT_uniform_P4   4    6778424  3.239583e-05      0.134718   0.113827          valid    1.000000
       torus   0.500   320     SRMT_uniform_P8   8    6778424  3.239583e-05      0.134718   0.113827          valid    1.000000
       torus   0.500   384                  MC   1     799616  6.933953e-05      0.123718   0.112006          valid    1.000000
       torus   0.500   384                  MT   1    2442688  8.897962e-05      0.225275   0.117042          valid    1.000000
       torus   0.500   384     SRMT_default_P1   1    9785248  2.227716e-05      0.112077   0.109634          valid    1.000000
       torus   0.500   384     SRMT_default_P2   2    9785248  2.227716e-05      0.112077   0.109634          valid    1.000000
       torus   0.500   384     SRMT_default_P4   4    9785248  2.227716e-05      0.112077   0.109634          valid    1.000000
       torus   0.500   384     SRMT_default_P8   8    9785248  2.227716e-05      0.112077   0.109634          valid    1.000000
       torus   0.500   384     SRMT_uniform_P1   1    9785432  2.251440e-05      0.112060   0.109813          valid    1.000000
       torus   0.500   384     SRMT_uniform_P2   2    9785432  2.251440e-05      0.112060   0.109813          valid    1.000000
       torus   0.500   384     SRMT_uniform_P4   4    9785432  2.251440e-05      0.112060   0.109813          valid    1.000000
       torus   0.500   384     SRMT_uniform_P8   8    9785432  2.251440e-05      0.112060   0.109813          valid    1.000000
       torus   0.500   448                  MC   1    1092160  4.573294e-05      0.105980   0.109651          valid    1.000000
       torus   0.500   448                  MT   1    3332632  6.521375e-05      0.192666   0.112802          valid    1.000000
       torus   0.500   448     SRMT_default_P1   1   13316320  1.643894e-05      0.096149   0.111656          valid    1.000000
       torus   0.500   448     SRMT_default_P2   2   13316320  1.643894e-05      0.096149   0.111656          valid    1.000000
       torus   0.500   448     SRMT_default_P4   4   13316320  1.643894e-05      0.096149   0.111656          valid    1.000000
       torus   0.500   448     SRMT_default_P8   8   13316320  1.643894e-05      0.096149   0.111656          valid    1.000000
       torus   0.500   448     SRMT_uniform_P1   1   13316240  1.649810e-05      0.096108   0.111491          valid    1.000000
       torus   0.500   448     SRMT_uniform_P2   2   13316240  1.649810e-05      0.096108   0.111491          valid    1.000000
       torus   0.500   448     SRMT_uniform_P4   4   13316240  1.649810e-05      0.096108   0.111491          valid    1.000000
       torus   0.500   448     SRMT_uniform_P8   8   13316240  1.649810e-05      0.096108   0.111491          valid    1.000000
       torus   0.500   512                  MC   1    1420304  3.994057e-05      0.092825   0.111016          valid    1.000000
       torus   0.500   512                  MT   1    4343224  4.999489e-05      0.168308   0.103999          valid    1.000000
       torus   0.500   512     SRMT_default_P1   1   17388480  1.246691e-05      0.083995   0.106452          valid    1.000000
       torus   0.500   512     SRMT_default_P2   2   17388480  1.246691e-05      0.083995   0.106452          valid    1.000000
       torus   0.500   512     SRMT_default_P4   4   17388480  1.246691e-05      0.083995   0.106452          valid    1.000000
       torus   0.500   512     SRMT_default_P8   8   17388480  1.246691e-05      0.083995   0.106452          valid    1.000000
       torus   0.500   512     SRMT_uniform_P1   1   17388656  1.258851e-05      0.083967   0.106168          valid    1.000000
       torus   0.500   512     SRMT_uniform_P2   2   17388656  1.258851e-05      0.083967   0.106168          valid    1.000000
       torus   0.500   512     SRMT_uniform_P4   4   17388656  1.258851e-05      0.083967   0.106168          valid    1.000000
       torus   0.500   512     SRMT_uniform_P8   8   17388656  1.258851e-05      0.083967   0.106168          valid    1.000000
gaussian_two   0.500    64                  MC   1       4432  3.142486e-03      0.506488   0.078103          valid    1.000000
gaussian_two   0.500    64                  MT   1      13732  7.119136e-03      1.713601   0.095943          valid    1.000000
gaussian_two   0.500    64     SRMT_default_P1   1      55244  1.881074e-03      0.837323   0.105057          valid    1.000000
gaussian_two   0.500    64     SRMT_default_P2   2      55244  1.881074e-03      0.837323   0.105057          valid    1.000000
gaussian_two   0.500    64     SRMT_default_P4   4      55244  1.881074e-03      0.837323   0.105057          valid    1.000000
gaussian_two   0.500    64     SRMT_default_P8   8      55244  1.881074e-03      0.837323   0.105057          valid    1.000000
gaussian_two   0.500    64     SRMT_uniform_P1   1      55268  1.881074e-03      0.836688   0.111384          valid    1.000000
gaussian_two   0.500    64     SRMT_uniform_P2   2      55268  1.881074e-03      0.836688   0.111384          valid    1.000000
gaussian_two   0.500    64     SRMT_uniform_P4   4      55268  1.881074e-03      0.836688   0.111384          valid    1.000000
gaussian_two   0.500    64     SRMT_uniform_P8   8      55268  1.881074e-03      0.836688   0.111384          valid    1.000000
gaussian_two   0.500   128                  MC   1      18436  9.197275e-04      0.246656   0.105208          valid    1.000000
gaussian_two   0.500   128                  MT   1      56368  1.781593e-03      0.843596   0.106497          valid    1.000000
gaussian_two   0.500   128     SRMT_default_P1   1     225656  4.598066e-04      0.419070   0.106092          valid    1.000000
gaussian_two   0.500   128     SRMT_default_P2   2     225656  4.598066e-04      0.419070   0.106092          valid    1.000000
gaussian_two   0.500   128     SRMT_default_P4   4     225656  4.598066e-04      0.419070   0.106092          valid    1.000000
gaussian_two   0.500   128     SRMT_default_P8   8     225656  4.598066e-04      0.419070   0.106092          valid    1.000000
gaussian_two   0.500   128     SRMT_uniform_P1   1     226092  4.574568e-04      0.417020   0.106754          valid    1.000000
gaussian_two   0.500   128     SRMT_uniform_P2   2     226092  4.574568e-04      0.417020   0.106754          valid    1.000000
gaussian_two   0.500   128     SRMT_uniform_P4   4     226092  4.574568e-04      0.417020   0.106754          valid    1.000000
gaussian_two   0.500   128     SRMT_uniform_P8   8     226092  4.574568e-04      0.417020   0.106754          valid    1.000000
gaussian_two   0.500   192                  MC   1      41656  4.037804e-04      0.164499   0.107539          valid    1.000000
gaussian_two   0.500   192                  MT   1     127412  7.956997e-04      0.561762   0.109299          valid    1.000000
gaussian_two   0.500   192     SRMT_default_P1   1     510676  2.026864e-04      0.279053   0.106529          valid    1.000000
gaussian_two   0.500   192     SRMT_default_P2   2     510676  2.026864e-04      0.279053   0.106529          valid    1.000000
gaussian_two   0.500   192     SRMT_default_P4   4     510676  2.026864e-04      0.279053   0.106529          valid    1.000000
gaussian_two   0.500   192     SRMT_default_P8   8     510676  2.026864e-04      0.279053   0.106529          valid    1.000000
gaussian_two   0.500   192     SRMT_uniform_P1   1     511716  2.023663e-04      0.278114   0.108189          valid    1.000000
gaussian_two   0.500   192     SRMT_uniform_P2   2     511716  2.023663e-04      0.278114   0.108189          valid    1.000000
gaussian_two   0.500   192     SRMT_uniform_P4   4     511716  2.023663e-04      0.278114   0.108189          valid    1.000000
gaussian_two   0.500   192     SRMT_uniform_P8   8     511716  2.023663e-04      0.278114   0.108189          valid    1.000000
gaussian_two   0.500   256                  MC   1      74172  2.239012e-04      0.123388   0.108660          valid    1.000000
gaussian_two   0.500   256                  MT   1     226940  4.462866e-04      0.421823   0.115728          valid    1.000000
gaussian_two   0.500   256     SRMT_default_P1   1     910280  1.134600e-04      0.209202   0.107723          valid    1.000000
gaussian_two   0.500   256     SRMT_default_P2   2     910280  1.134600e-04      0.209202   0.107723          valid    1.000000
gaussian_two   0.500   256     SRMT_default_P4   4     910280  1.134600e-04      0.209202   0.107723          valid    1.000000
gaussian_two   0.500   256     SRMT_default_P8   8     910280  1.134600e-04      0.209202   0.107723          valid    1.000000
gaussian_two   0.500   256     SRMT_uniform_P1   1     912148  1.134600e-04      0.208222   0.107803          valid    1.000000
gaussian_two   0.500   256     SRMT_uniform_P2   2     912148  1.134600e-04      0.208222   0.107803          valid    1.000000
gaussian_two   0.500   256     SRMT_uniform_P4   4     912148  1.134600e-04      0.208222   0.107803          valid    1.000000
gaussian_two   0.500   256     SRMT_uniform_P8   8     912148  1.134600e-04      0.208222   0.107803          valid    1.000000
gaussian_two   0.500   320                  MC   1     116316  1.459382e-04      0.098440   0.112227          valid    1.000000
gaussian_two   0.500   320                  MT   1     355500  2.860502e-04      0.336471   0.111317          valid    1.000000
gaussian_two   0.500   320     SRMT_default_P1   1    1424432  7.249339e-05      0.167128   0.109138          valid    1.000000
gaussian_two   0.500   320     SRMT_default_P2   2    1424432  7.249339e-05      0.167128   0.109138          valid    1.000000
gaussian_two   0.500   320     SRMT_default_P4   4    1424432  7.249339e-05      0.167128   0.109138          valid    1.000000
gaussian_two   0.500   320     SRMT_default_P8   8    1424432  7.249339e-05      0.167128   0.109138          valid    1.000000
gaussian_two   0.500   320     SRMT_uniform_P1   1    1427764  7.195099e-05      0.166367   0.108338          valid    1.000000
gaussian_two   0.500   320     SRMT_uniform_P2   2    1427764  7.195099e-05      0.166367   0.108338          valid    1.000000
gaussian_two   0.500   320     SRMT_uniform_P4   4    1427764  7.195099e-05      0.166367   0.108338          valid    1.000000
gaussian_two   0.500   320     SRMT_uniform_P8   8    1427764  7.195099e-05      0.166367   0.108338          valid    1.000000
gaussian_two   0.500   384                  MC   1     167576  1.039759e-04      0.082225   0.111595          valid    1.000000
gaussian_two   0.500   384                  MT   1     512268  1.984763e-04      0.280266   0.114214          valid    1.000000
gaussian_two   0.500   384     SRMT_default_P1   1    2053780  5.028549e-05      0.139150   0.109540          valid    1.000000
gaussian_two   0.500   384     SRMT_default_P2   2    2053780  5.028549e-05      0.139150   0.109540          valid    1.000000
gaussian_two   0.500   384     SRMT_default_P4   4    2053780  5.028549e-05      0.139150   0.109540          valid    1.000000
gaussian_two   0.500   384     SRMT_default_P8   8    2053780  5.028549e-05      0.139150   0.109540          valid    1.000000
gaussian_two   0.500   384     SRMT_uniform_P1   1    2057912  5.002434e-05      0.138665   0.109881          valid    1.000000
gaussian_two   0.500   384     SRMT_uniform_P2   2    2057912  5.002434e-05      0.138665   0.109881          valid    1.000000
gaussian_two   0.500   384     SRMT_uniform_P4   4    2057912  5.002434e-05      0.138665   0.109881          valid    1.000000
gaussian_two   0.500   384     SRMT_uniform_P8   8    2057912  5.002434e-05      0.138665   0.109881          valid    1.000000
gaussian_two   0.500   448                  MC   1     228104  7.881396e-05      0.070318   0.113346          valid    1.000000
gaussian_two   0.500   448                  MT   1     697692  1.458264e-04      0.240212   0.115113          valid    1.000000
gaussian_two   0.500   448     SRMT_default_P1   1    2796932  3.669098e-05      0.119414   0.110943          valid    1.000000
gaussian_two   0.500   448     SRMT_default_P2   2    2796932  3.669098e-05      0.119414   0.110943          valid    1.000000
gaussian_two   0.500   448     SRMT_default_P4   4    2796932  3.669098e-05      0.119414   0.110943          valid    1.000000
gaussian_two   0.500   448     SRMT_default_P8   8    2796932  3.669098e-05      0.119414   0.110943          valid    1.000000
gaussian_two   0.500   448     SRMT_uniform_P1   1    2803192  3.669098e-05      0.118901   0.111050          valid    1.000000
gaussian_two   0.500   448     SRMT_uniform_P2   2    2803192  3.669098e-05      0.118901   0.111050          valid    1.000000
gaussian_two   0.500   448     SRMT_uniform_P4   4    2803192  3.669098e-05      0.118901   0.111050          valid    1.000000
gaussian_two   0.500   448     SRMT_uniform_P8   8    2803192  3.669098e-05      0.118901   0.111050          valid    1.000000
gaussian_two   0.500   512                  MC   1     298388  6.291080e-05      0.061805   0.109440          valid    1.000000
gaussian_two   0.500   512                  MT   1     912140  1.116033e-04      0.209801   0.110671          valid    1.000000
gaussian_two   0.500   512     SRMT_default_P1   1    3656508  2.818076e-05      0.104295   0.109602          valid    1.000000
gaussian_two   0.500   512     SRMT_default_P2   2    3656508  2.818076e-05      0.104295   0.109602          valid    1.000000
gaussian_two   0.500   512     SRMT_default_P4   4    3656508  2.818076e-05      0.104295   0.109602          valid    1.000000
gaussian_two   0.500   512     SRMT_default_P8   8    3656508  2.818076e-05      0.104295   0.109602          valid    1.000000
gaussian_two   0.500   512     SRMT_uniform_P1   1    3664128  2.796820e-05      0.103964   0.110397          valid    1.000000
gaussian_two   0.500   512     SRMT_uniform_P2   2    3664128  2.796820e-05      0.103964   0.110397          valid    1.000000
gaussian_two   0.500   512     SRMT_uniform_P4   4    3664128  2.796820e-05      0.103964   0.110397          valid    1.000000
gaussian_two   0.500   512     SRMT_uniform_P8   8    3664128  2.796820e-05      0.103964   0.110397          valid    1.000000

Saved:
  data_mc_mt_srmt/benchmark_results_raw.csv
  data_mc_mt_srmt/benchmark_results_raw.json
  data_mc_mt_srmt/benchmark_results.csv
  data_mc_mt_srmt/benchmark_method_comparison.csv
  data_mc_mt_srmt/benchmark_srmt_scaling.csv
  data_mc_mt_srmt/benchmark_results.json
  data_mc_mt_srmt/benchmark_results.md
  data_mc_mt_srmt/environment.json
  data_mc_mt_srmt/by_mode (separate summaries for each SRMT construction)
