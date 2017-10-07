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
