from flask import Flask, request, jsonify
from kubernetes import client
import urllib3

# all init code is done outside any function (for example main)
# because running flask with 'python3 -m flask run' will not enter main here
app = Flask(__name__)
kubeconfig = client.Configuration()
urllib3.disable_warnings()

token = ''
namespace = 'default'

try:
    print('opening')
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
        token = file.read().replace('\n', '')
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as file:
        namespace = file.read().replace('\n', '')
except:
    print("Unable to read token or namespace")
    quit()

kubeconfig.verify_ssl=False
kubeconfig.api_key["authorization"] = token
kubeconfig.api_key_prefix['authorization'] = 'Bearer'
kubeconfig.host = 'https://kubernetes.default.svc'
kubeconfig.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
v1 = client.CoreV1Api(client.ApiClient(kubeconfig))
# done init

@app.route('/test/<int:arg>')
def test(arg):
   return f"{arg} is OK!"

@app.route('/get/pods')
def cani():
    rv = ""
    try:
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            rv += f"{i.status.pod_ip}\t{i.metadata.namespace}\t{i.metadata.name}\t"
    except Exception as e:
        rv = f"Unable to execute request for kubernetes cluster {str(e)}"
    return rv

if __name__ == '__main__':
    app.run()