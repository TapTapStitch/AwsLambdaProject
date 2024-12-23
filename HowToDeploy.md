# Deployment Process

This document describes the steps to deploy and delete the AWS Lambda project.

## Deployment Steps

1. **Switch to the Deployment Branch**  
   Begin by switching to the `deploy` branch:  
   ```zsh
   git checkout deploy
   ```

2. **Install Python Dependencies**  
   Install the required Python dependencies into the specified directory:  
   ```zsh
   pip install -r lambda_functions/lambda_layer/requirements.txt -t lambda_functions/lambda_layer/python/lib/python3.13/site-packages
   ```

3. **Deploy with AWS SAM**  
   Deploy the project using the AWS SAM CLI:  
   ```zsh
   sam deploy \
       --template-file template.yaml \
       --resolve-s3 \
       --stack-name AwsLambdaProject \
       --capabilities CAPABILITY_NAMED_IAM
   ```

## Deletion Steps

To delete the deployed stack, use the following command:  
```zsh
sam delete --stack-name AwsLambdaProject
```

This will remove the AWS resources created during the deployment process.

## Additional Notes

- **AWS Configuration**: Ensure that your AWS CLI is configured with valid credentials and the correct region.
- **Dependencies**: Verify that all necessary dependencies are listed in `requirements.txt`.
- **IAM Capabilities**: The `--capabilities CAPABILITY_NAMED_IAM` flag allows the creation or modification of IAM roles and policies required by the stack.

## Troubleshooting

- **Dependency Issues**: If dependencies are missing, check the `requirements.txt` file for completeness and re-run the installation step.
- **Permission Errors**: Ensure that your AWS credentials have the required permissions to deploy the stack.
- **S3 Bucket Management**: The `--resolve-s3` flag lets SAM handle the S3 bucket for storing deployment artifacts. Ensure your AWS account has permission to create and manage S3 buckets.
