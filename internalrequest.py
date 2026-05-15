#!/usr/bin/env python
#

import os, sys, time
import shlex
import json
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pprint import pprint
from queue import Queue
from threading import Thread
from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException

workerThreads = 3
tempdir = TemporaryDirectory(delete=True)
tempfiles = []

config.load_kube_config()



# queue instance
q = Queue()

def createAndWatchInternalRequest(namespace="default", payload=None):
    try:
        if payload == None:
            raise Exception("missing payload")
       
        url = "http://google.com"
        revision = "1"
        pipeline = "sample"

        # api metadata
        group="appstudio.redhat.com"
        version="v1alpha1"
        plural="internalrequests"
        namespace="default"

        labels = {}
        # convert labels to valid object types
        for label in labels:
            for k,v in label.iteritems():
                labels[k] = v
      
        api = client.CustomObjectsApi()
        internalRequest = {
            "apiVersion": "appstudio.redhat.com/v1alpha1",
            "kind": "InternalRequest",
            "metadata": {
                "generateName": payload["generateName"] + "-",
                "labels": labels
            },
            "spec": {
              "pipeline": payload["pipeline"],
              "params": payload["params"],
            }
        }
        ir = api.create_namespaced_custom_object(
          group=group,
          version=version,
          plural=plural,
          namespace=namespace,
          body=internalRequest,
        )

        name = ir["metadata"]["name"]
        print("Internal request %s created" % name)
        tempfile = NamedTemporaryFile(mode="w", dir=tempdir.name, delete=False)
        tempfiles.append(tempfile)
        while True:
            ir = api.get_namespaced_custom_object_status(group, version, namespace, plural, name)
            if not "status" in ir:
                time.sleep(1)
                continue

            if ir["status"]["conditions"][0]["reason"] != "" and ir["status"]["conditions"][0]["reason"] != "Running":
                print("IR %s done, writing IR to %s" % (name, tempfile.name))
                tempfile.write(json.dumps(ir)) 
                tempfile.close()
                return
                
            time.sleep(2)

        
    except Exception as e:
        print("Error on " + str(e))
    # end function

def worker():
    while True:
        item = q.get()
        print("Creating internal request")
        createAndWatchInternalRequest(payload=item)
        q.task_done()

# queue
for i in range(workerThreads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

items = json.loads(open("requests.json").read())
for item in items["items"]:
    q.put(item)

q.join()

output = open("output.json", "w")
json_output = { "items": [] }
for f in tempfiles:
    json_output["items"].append(json.loads(open(f.name).read()))
    os.unlink(f.name)

output.write(json.dumps(json_output))
output.close()
