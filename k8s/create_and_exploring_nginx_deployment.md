Create a Deployment based on the YAML file:

    kubectl apply -f https://k8s.io/docs/tasks/run-application/deployment.yaml

Display information about the Deployment:

    kubectl describe deployment nginx-deployment

List the pods created by the deployment:

    kubectl get pods -l app=nginx

Display information about a pod:

    kubectl describe pod <pod-name>


