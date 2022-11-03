# simple-flask-test-server

based for container/kubernetes testing purpose. (auto-scaling or....)

# Author
Jioh L. Jung
- github.com/ziozzang

# usage
```
docker build -t simple-flask-test-server .
docker run -d -p 8080:8080  simple-flask-test-server
```
- environments
 - MEM_PERCENT: memory burn rate(int percent/default: 60)


# URLS

```
/ : return headers and hostname
/burn-cpu /stop-cpu : Burnin test for CPU (start and stop)
/burn-mem /stop-mem : Burnin test for memory (start and stop)
/set-mem/<percent> : set burnin test for memory rate(percent/default: 60)
/env : get environ (injected key-values)
/exit : force exit server

```

# limitation
* cuz of python limitation, python code works only single threaded. so, CPU burnin work only one cpu/core.
* cuz of OOM-killer issue, cannot burnin full memory area...

