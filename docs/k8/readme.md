The recommendation for deploying OPAL in a kubernetes cluster is to use the included helm chart. Once you have cloned the repo you can deploy using helm by following these steps:

1. in the docs/k8/helm directory, update the values.yaml file. Particularly you will want to update the hostname to be the url you will access the application at. And of course you should update the passwords
2. Assuming you have helm installed and working, run the following command from the docs/k8/helm subdirectory:
`helm install opal opal`

If you cannot or do not wish to use helm, you can find the necesary YAML files in the docs/k8/helm/opal/templates directory. Modify these files as needed and then run kubectl apply -f . from this directory

