# Backend shareholder registry
Django backend for the Norwegian Shareholder Registry (Aksjonærregisteret).

# Infrastructure-as-Code
The infrastructure is defined with terraform in the following repository: 
https://github.com/phydev/tf_shareholder_registry

# Deploying application image to podman
Run `make deploy` to build the image and deploy to podman registry:
```bash
podman build -t backend-registry .
```

# Deploy containers
Run `terraform apply` to update the container with the new image. 


# Accessing the API
The application is deployed on https://localhost:8080