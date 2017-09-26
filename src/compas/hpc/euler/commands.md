# Euler ETH cluster commands

Updated: 2 Feb 17
Dr. Andrew Liew : liew@arch.ethz.ch
Block Research Group

## SSH commands

### Login to an Euler node

```bash
$ ssh liewa@euler.ethz.ch
[liewa@euler07 ~]$
```

or for X11 access

```bash
$ ssh -Y liewa@euler.ethz.ch
[liewa@euler07 ~]$
```

### Send a file to your Euler home directory

```bash
$ scp file.ext liewa@euler.ethz.ch:
file.ext                                      100%    400     150.0KB/s   00:01
$
```

### Recieve a file to your computer

```bash
$ scp liewa@euler.ethz.ch:file.ext file.ext
file.ext                                      100%    400     150.0KB/s   00:01
$
```

## Cluster modules

### Available modules

```bash
[liewa@euler07 ~]$ module avail
------------ /cluster/apps/modules/modulefiles -------------
abaqus/6.13-2(default:6.13)
abaqus/6.14-1
abinit/7.10.5(default)
adf/2014.07(default:2014)
amdis/3247(default)
ansys/16.2(default)
ansys/17.0(17)
ant/1.9.4(default:1.9)
...
visit/2.8.2
visit/2.9.0(default)
vmd/1.9.2(default)
vtk/6.1.0(default)
wxwidgets/2.8.12
wxwidgets/3.0.2
xmgrace/5.1.24(default)
xpdf/3.03(default)
xquest/2.1.5
xz/5.2.2
zlib/1.2.8
[liewa@euler07 ~]$
```

### OpenBLAS parallel and Python modules

```bash
[liewa@euler07 ~]$ module load openblas/0.2.13_par
[liewa@euler07 ~]$ module load python/2.7
[liewa@euler07 ~]$ module list
Currently Loaded Modulefiles:
  1) modules
  2) openblas/0.2.13_par(par)
  3) python/2.7.6(2.7)
[liewa@euler07 ~]$
```

### Unload modules

```bash
[liewa@euler07 ~]$ module purge
[liewa@euler07 ~]$ module list
No Modulefiles Currently Loaded.
[liewa@euler07 ~]$
```

## Submitting jobs

### Available resources

```bash
[liewa@euler07 ~]$ busers
USER/GROUP          JL/P    MAX  NJOBS   PEND    RUN  SSUSP  USUSP    RSV
liewa                  -     48      0      0      0      0      0      0
[liewa@euler07 ~]$
```

### All cluster jobs

```bash
[liewa@euler07 ~]$ bqueues
QUEUE_NAME      PRIO STATUS          MAX JL/U JL/P JL/H NJOBS  PEND   RUN  SUSP
system           99  Open:Active       -    -    -    -     0     0     0     0
clc              94  Open:Active     256    -    -    -     0     0     0     0
bigmem.4h        88  Open:Active       -    -    -    -    24    24     0     0
bigmem.24h       86  Open:Active       -    -    -    -  1755  1401   354     0
bigmem.120h      84  Open:Active       -  960    -    -   672   532   140     0
bigmem.fair      80  Closed:Inact      -    -    -    -     0     0     0     0
normal.4h        68  Open:Active       -    -    -    - 21926 20512  1414     0
normal.24h       66  Open:Active       -    -    -    - 41913 29071 12842     0
normal.120h      64  Open:Active       -    -    -    - 25106 17109  7997     0
normal.30d       62  Open:Active       -    -    -    -  2128  2104    24     0
normal.fair      60  Closed:Inact      -    -    -    -     0     0     0     0
virtual.40d      58  Closed:Inact      -    -    -    -     0     0     0     0
filler.40d       11  Closed:Inact      -    -    -    -     0     0     0     0
light.5d         10  Open:Active       -    -    -    -     0     0     0     0
purgatory         1  Open:Inact        -    -    -    -    24    24     0     0
[liewa@euler07 ~]$
```

### Set multithreading environment variable

```bash
[liewa@euler07 ~]$ OMP_NUM_THREADS=24
[liewa@euler07 ~]$
```

### Submit job

```bash
[liewa@euler07 ~]$ bsub -W 1:30 -n 24 -o results.txt python script.py
Generic job.
Job <33567817> is submitted to queue <normal.4h>.
[liewa@euler07 ~]$
```

### Check submitted jobs
```bash
[liewa@euler07 ~]$ bjobs
JOBID      USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME
33567817   liewa   PEND  normal.4h  euler07                 *script.py Dec  5 11:17
[liewa@euler07 ~]$
```

### Detailed job information
```bash
[liewa@euler01 ~]$ bbjobs 36754805
Job information
  Job ID                          : 36754805
  Status                          : PENDING
  User                            : liewa
  Queue                           : normal.4h
  Command                         : python script.py
  Working directory               : $HOME/-
Requested resources
  Requested cores                 : 24
  Requested runtime               : 30 min
  Requested memory                : 1024 MB per core, 24576 MB total
  Requested scratch               : not specified
  Dependency                      : -
Job history
  Submitted at                    : 10:33 2017-02-02
  Queue wait time                 : 200 sec
[liewa@euler01 ~]$
```
