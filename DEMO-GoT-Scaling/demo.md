### prep a cluster
0. Create AWS Account & Route 53 Hosted Zone
1. Install the cluster on AWS with IPI
2. Install Node feature Discovery operator
3. Install nvidia gpu operator and cluster policy
4. install openshift serverless and knative-serving instance
5. demo your application

# 0. Have your AWS Account Ready
# 1. Install an OpenShift Cluster on AWS
https://console.redhat.com/openshift/install/aws/installer-provisioned
### download installer and cp to 1-openshift-installation
### download pull-secret.txt and cp to 1-openshift-installation
aws configure
cd 1-openshift-installation
tar -xvzf openshift-install-mac.tar.gz
./openshift-install create install-config --dir installation-resources --log-level=info
./openshift-install create cluster --dir installation-resources --log-level=info
#### after success
oc login -u kubeadmin -p $(cat ./installation-resources/auth/kubeadmin-password) $(yq '.clusters[].cluster.server' ./installation-resources/auth/kubeconfig)
#### create a gpu node machine set
vi gpu-machine-set-aws.yaml
oc apply -f gpu-machine-set-aws.yaml
# 2. Install Node feature Discovery operator
oc apply -f 2-install-nfd-operator/install.yaml
oc apply -f 2-install-nfd-operator/nodefeaturediscinstance.yaml
# 3. Install nvidia gpu operator and cluster policy
oc apply -f 3-install-nvidia-gpu-operator/install.yaml
oc apply -f 3-install-nvidia-gpu-operator/clusterpolicyinstance.yaml
# 4. Install openshift serverless and knative-serving instance
oc apply -f 4-install-knative-operator/install.yaml
oc apply -f 4-install-knative-operator/knativeserving.yaml
oc apply -f 4-install-knative-operator/enablenodeselector-cm.yaml

# STEP ONE

### Build a Container with a Dockerfile
cd ./GoT-Mining-UI
podman build -f Dockerfile -t gotminingui .
podman run -p 80:3000 quay.io/mdargatz/gotminingui:latest
podman run -p 8181:3000 quay.io/mdargatz/gotminingui:latest
podman run -p 8181:3000 -e GPT2SERVICEURL=http://localhost:8080 -d quay.io/mdargatz/gotminingui:latest

# STEP TWO
### Containers start communicating
curl localhost:8181
#### start a second container/backend
cd ../GoT-Mining/gpt2-got/gpt2-model-inferencing
podman build -t quay.io/mdargatz/gotmininggpt2:small .
du -sh ./checkpoint
podman run -p 8080:8080 quay.io/mdargatz/gotmininggpt2:small

# STEP THREE
### “Compose” a multi-service application
podman ps
podman stop --all
podman-compose up

# STEP FOUR
### Move to Kubernetes
--> show yaml files and complexity

# STEP FIVE
### Move to OpenShift
#### create project && showcase basic image deployment via images 
oc new-project gotmining
#### do this via ui //oc new-app --name=mining-backend --image=quay.io/mdargatz/gotmininggpt2:small
#### do this via cli
oc new-app --name=mining-frontend --image=quay.io/mdargatz/gotminingui:latest --env=GPT2SERVICEURL=https://backend-md-gotmining.apps.ocp4.stormshift.coe.muc.redhat.com -l app.kubernetes.io/name=nodejs -l app.kubernetes.io/part-of=gotmining

# STEP SIX
oc create route edge --service=mining-frontend 
kubectl patch route mining-backend -p '{"metadata":{"annotations":{"haproxy.router.openshift.io/timeout":"240s"}}}'

# STEP SEVEN
#### showcase route creation and environment variable setting and scale up to 5 instances
----> SHOW THAT SCALING FOR NODES ALSO WORKS QUITE EASY!!!! Scale Up machine Set

#### delete project
oc delete project gotmining
#### redo deployment via yaml and knative service
oc new-project gotmining-serverless
cd 5-deploy-application
cat gotmining-backend/serverless/gpt2gotmodel-serverless-v1.yaml
oc apply -f gotmining-backend/serverless/gpt2gotmodel-serverless-v1.yaml
oc apply -f gotmining-frontend
#### extract the route
oc get routes.serving.knative.dev -o jsonpath='{range .items[*]}{.status.address.url}'
#### showcase automated scaling of app and the downside of them scheduled on non-gpu nodes by picking a pod

# STEP EIGHT
#### identify GPU nodes
oc get nodes -o jsonpath='{.items[?(@.status.allocatable.nvidia\.com\/gpu != "")].metadata.name}'
#### label these nodes as gpu nodes
for NODE in `oc get nodes -o jsonpath='{.items[?(@.status.allocatable.nvidia\.com\/gpu != "")].metadata.name}'
`; do oc label node $NODE gpu=true; done 
oc get nodes -o jsonpath='{.items[?(@.metadata.labels.gpu == "true")].metadata.name}'
#### showcase nodeselector and/or nodeaffinity in the yaml of the knative service
#### show how easy it is to add nodes to the cluster
#### modify knative deployment to leverage gpu nodes
oc apply -f gotmining-backend/serverless/gpt2gotmodel-serverless-v1-gpu.yaml
#### be quick to show it gets shuffled over to gpu node

#### 
oc apply -f gotmining-backend/serverless/gpt2gotmodel-serverless-v2-gpu.yaml


## short version
## Step 1-3
cd ./GoT-Mining-UI
podman-compose up
## Step 4
# STEP FIVE
### Move to OpenShift
#### create project && showcase basic image deployment via images 
oc new-project gotmining
#### do this via ui //oc new-app --name=mining-backend --image=quay.io/mdargatz/gotmininggpt2:small
#### do this via cli
oc new-app --name=mining-frontend --image=quay.io/mdargatz/gotminingui:latest --env=GPT2SERVICEURL=https://mining-backend-gotmining.apps.cluster-kdxx2.kdxx2.sandbox1697.opentlc.com -l app.kubernetes.io/name=nodejs -l app.kubernetes.io/part-of=gotmining


# STEP SIX
oc create route edge --service=mining-frontend 
kubectl patch route mining-backend -p '{"metadata":{"annotations":{"haproxy.router.openshift.io/timeout":"240s"}}}'
#### showcase route creation and environment variable setting and scale up to 5 instances
----> SHOW THAT SCALING FOR NODES ALSO WORKS QUITE EASY!!!! Scale Up machine Set


# STEP SEVEN
oc new-project gotmining-serverless
cd 5-deploy-application
cat gotmining-backend/serverless/gpt2gotmodel-serverless-v1.yaml
oc apply -f gotmining-backend/serverless/gpt2gotmodel-serverless-v1.yaml
oc apply -f gotmining-frontend

hey -c 10 -z 2s https://gpt2gotmodel-test-gotmining-serverless.apps.cluster-kdxx2.kdxx2.sandbox1697.opentlc.com


# STEP EIGHT
#### identify GPU nodes
oc get nodes -o jsonpath='{.items[?(@.status.allocatable.nvidia\.com\/gpu != "")].metadata.name}'
#### label these nodes as gpu nodes
for NODE in `oc get nodes -o jsonpath='{.items[?(@.status.allocatable.nvidia\.com\/gpu != "")].metadata.name}'
`; do oc label node $NODE gpu=true; done 
oc get nodes -o jsonpath='{.items[?(@.metadata.labels.gpu == "true")].metadata.name}'
#### showcase nodeselector and/or nodeaffinity in the yaml of the knative service
cat gotmining-backend/serverless/gpt2gotmodel-serverless-v2-gpu.yaml
#### show how easy it is to add nodes to the cluster
#### be quick to show it gets shuffled over to gpu node

#### 
oc apply -f gotmining-backend/serverless/gpt2gotmodel-serverless-v2-gpu.yaml