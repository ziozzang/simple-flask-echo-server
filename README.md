# simple-flask-echo-server

based for container/kubernetes testing purpose. (auto-scaling or....)

# Author
Jioh L. Jung <ziozzang at gmail.com>

# usage
```
docker build -t simple-flask-echo-server .
docker run -d -p 8080:8080  simple-flask-echo-server
```

# URLS

```
/ : return headers and hostname

/burn-cpu /stop-cpu : Burnin test for CPU (start and stop)
/burn-mem /stop-mem : Burnin test for memory (start and stop)

```

# limitation
* cuz of python limitation, python code works only single threaded. so, CPU burnin work only one cpu/core.
* cuz of OOM-killer issue, cannot burnin full memory area...

