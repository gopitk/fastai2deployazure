# Deploy Fast.AI Models to Azure

Samples for serverless deployment of fastai2 models to Azure Functions. 

## Pre-requisites

Before you begin, you must have the following:

1. An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free).

On a Linux system or Windows (WSL or WSL2) ensure you have the following installed:

2. The [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2)
3. The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) 
4. Python 3.7

Note: You can also use Azure Cloud Shell which comes preinstalled with Azure CLI and Functions Core Tools. 

## Develop and Test Locally

You can develop for serverless deployment on Azure functions on your Linux machine locally or a development VM (like the Azure Data Science VM) on the cloud or Azure Cloud Shell. Run the following commands to setup your Azure Functions project locally.

1. Create a Function App project directory and start directory

```
mkdir << Your projectname >>
cd << Your projectname>>
mkdir start
cd start
```

2. Initialize Function App

```
func init --worker-runtime python
func new --name classify --template "HTTP trigger"
```

3. Copy the deployment code 
```
git clone https://github.com/gopitk/fastai2deployazure.git ~/fastai2deployazure

# Copy the deployment sample to function app
cp -r ~/fastai2deployazure/start ..

```

4. Create and activate Python virtualenv to setup fastai2 along with dependencies

```
python -m venv .venv
source .venv/bin/activate

pip install --no-cache-dir -r requirements.txt  
```

5. Copy your fast.ai model file (which should have a name export.pkl)  built from training the model  into  the "start/classify" directory within your Function App project. This has been tested with the Bear detector model from fast.ai course-v4 (beta). 

6. Run the test locally

```
func start
```
In a browser on your machine you can test the local Azure Function by visiting: 

"http://localhost:7071/api/classify?img=http://3.bp.blogspot.com/-S1scRCkI3vY/UHzV2kucsPI/AAAAAAAAA-k/YQ5UzHEm9Ss/s1600/Grizzly%2BBear%2BWildlife188.jpg"


## Create Resources in Azure and Publish

1. Create Azure Function App using Azure CLI

```
# If you have not logged into Azure CLI. you must first run "az login" and follow instructions

az group create --name [[YOUR Function App name]]  --location westus2
az appservice plan create --name [[YOUR Function App name]] -g [[YOUR Function App name]] --sku B1 --is-linux
az storage account create --name [[Your Storage Account Name]] -l westus2 --sku Standard_LRS -g [[YOUR Function App name]]
az functionapp create --name [[YOUR Function App name]] -g [[YOUR Function App name]] --storage-account [[Your Storage Account Name]] --plan [[YOUR Function App name]] --runtime python --runtime-version 3.7 --functions-version 3 --disable-app-insights 
```
2. Publish to Azure

```
# Install a local copy of fastai2 and dependencies to push to Azure Functions Runtime
pip install  --target="./.python_packages/lib/site-packages"  -r requirements.txt

# Publish Azure function to the 
func azure functionapp publish [[YOUR Function App name] --no-build


```

It will take a few minutes to publish and bring up the Azure functions with you fast.ai model deployed and exposed as a http endpoint.  Then you can find the URL by running the following command:  ```func azure functionapp list-functions [[YOUR Function App name] --show-keys``` . Append ```&img=[[Your Image URL to run thru model]]``` to the URL on a browser to get predictions from the model running in the Azure Functions. 

## Deleting Resources
To delete all the resources (and avoiding any charges) after you are done, run the following Azure CLI command:
```
az group delete --name [[YOUR Function App name]] --yes

```
Azure Functions provides other options like auto scaling, larger instances, monitoring with Application Insights etc. 

## Notes

1. Azure Functions have a "consumption plan" which runs them in smaller compute / memory instances. While these are cheaper, the memory is only 1GB and may not be sufficient for many Python models especially ones with lot of dependencies like fast.ai. We use the App service basic plan (B1) which gives about 1.75GB of memory. Other premium SKUs are available with more compute and memory. On the Azure Portal when you look at scale-up option for your Function App you will see the available SKUs. 
2. If you are using Windows WSL or WSL2 and face authentication issues while deploying Function App to Azure, one of the main reason is your clock in WSL (Linux) may be out of sync with the underlying Windows host. You can synch it by running ```sudo hwclock -s``` in WSL. 

