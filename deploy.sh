#!/bin/bash

# Set up the base directory for deployment
DEPLOY_DIR="deploy"
STACK_NAME="AwsLambdaProject"

# Create the deployment structure
mkdir -p "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_functions/lambda_layer"
mkdir -p "$DEPLOY_DIR/lambda_functions"

# Array of function names
FUNCTIONS=(create_post update_post delete_post get_post get_posts get_public_posts)

# Loop through each function name
for FUNCTION in "${FUNCTIONS[@]}"; do
    # Create a directory for each function in lambda_functions
    mkdir -p "$DEPLOY_DIR/lambda_functions/$FUNCTION"

    # Copy the corresponding Python file to its directory
    if [ -f "lambda_functions/$FUNCTION.py" ]; then
        cp "lambda_functions/$FUNCTION.py" "$DEPLOY_DIR/lambda_functions/$FUNCTION/"
    else
        echo "Warning: lambda_functions/$FUNCTION.py not found."
    fi
done

# Create lambda_layer structure and copy files
touch "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_functions/__init__.py"
touch "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_functions/lambda_layer/__init__.py"

if [ -f "lambda_functions/lambda_layer/decorators.py" ]; then
    cp "lambda_functions/lambda_layer/decorators.py" "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_functions/lambda_layer/"
else
    echo "Warning: lambda_functions/lambda_layer/decorators.py not found."
fi

if [ -f "lambda_functions/lambda_layer/utils.py" ]; then
    cp "lambda_functions/lambda_layer/utils.py" "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_functions/lambda_layer/"
else
    echo "Warning: lambda_functions/lambda_layer/utils.py not found."
fi

# Install packages from requirements.txt
if [ -f "lambda_functions/lambda_layer/requirements.txt" ]; then
    pip install -r "lambda_functions/lambda_layer/requirements.txt" --target "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages"
else
    echo "Warning: lambda_functions/lambda_layer/requirements.txt not found."
fi

# Deploy
sam deploy \
    --template-file template.yaml \
    --resolve-s3 \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_NAMED_IAM

# Remove dir after deployment
rm -rf "$DEPLOY_DIR"

echo "Deployment complete."
