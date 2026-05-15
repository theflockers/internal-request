# internal-request

### running
Example of workerThreads set to 3

```
$ ./internalrequest.py requests.json
Creating internal request
Creating internal request
Creating internal request
Internal request internalrequest-8w6rf created
Internal request internalrequest-jx9cj created
Internal request internalrequest-4mzv4 created
IR internalrequest-8w6rf done, writing IR to /tmp/tmp75363b69/tmpk3dv7djl
Creating internal request
Internal request internalrequest-876s5 created
IR internalrequest-876s5 done, writing IR to /tmp/tmp75363b69/tmpdbwjmsyi
Creating internal request
Internal request internalrequest-q6bnq created
IR internalrequest-4mzv4 done, writing IR to /tmp/tmp75363b69/tmpzbm8kh4i
IR internalrequest-jx9cj done, writing IR to /tmp/tmp75363b69/tmp5skrug8k
IR internalrequest-q6bnq done, writing IR to /tmp/tmp75363b69/tmpe6dk2fda
```

### quick explanation

- 5 Internal Requests are present in the `requests.json` file
- 3 are added right away
- Once the one finishes another one is added to the queue
- The results for each IR is saved in its own temporary file
