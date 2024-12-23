# Deployment Process

This document describes the steps to deploy and delete the AWS Lambda project.

## Deployment Steps

To deploy the project, use the following command:  
```zsh
./deploy.sh
```

## Deletion Steps

To delete the deployed stack, use the following command:  
```zsh
sam delete --stack-name AwsLambdaProject
```

This will remove the AWS resources created during the deployment process.
