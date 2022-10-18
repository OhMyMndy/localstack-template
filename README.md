# localstack-template
Template to quickly develop applications and automations with LocalStack, Github Actions and containers!





## How to get started:


- Create a new repository from this template
- Create a new workspace on Gitpod.io for the newly created repository
- Connect your local VsCode instance to the workspace
- Start working by running the vscode run configurations!


```bash
docker compose up -d 

cd terraform
tflocal destroy -auto-approve
tflocal apply -auto-approve \
 && awslocal lambda invoke --function-name create-report --payload '{"region": "eu-central-1"}' --invocation-type RequestResponse response.json \
  && cat response.json | jq

```



