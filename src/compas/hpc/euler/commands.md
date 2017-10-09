
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
