#!/bin/bash

# Set up the base directory for deployment
DEPLOY_DIR="deploy"
STACK_NAME="AwsLambdaProject"

# Create the deployment structure
mkdir -p "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_layer"
mkdir -p "$DEPLOY_DIR/lambda_functions"

# Array of function names
FUNCTIONS=(create_post update_post delete_post get_post get_posts get_public_posts)
UTILS=(utils decorators)

# Loop through each function name
for FUNCTION in "${FUNCTIONS[@]}"; do
    mkdir -p "$DEPLOY_DIR/lambda_functions/$FUNCTION"

    if [ -f "lambda_functions/$FUNCTION.py" ]; then
        cp "lambda_functions/$FUNCTION.py" "$DEPLOY_DIR/lambda_functions/$FUNCTION/"
    else
        echo "Warning: lambda_functions/$FUNCTION.py not found."
    fi
done

# Create lambda_layer structure and copy files
touch "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_layer/__init__.py"

# Loop through each util name
for UTIL in "${UTILS[@]}"; do
    if [ -f "lambda_layer/$UTIL.py" ]; then
        cp "lambda_layer/$UTIL.py" "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages/lambda_layer/"
    else
        echo "Warning: lambda_layer/$UTIL.py not found."
    fi
done

# Install packages from requirements.txt
if [ -f "lambda_layer/requirements.txt" ]; then
    pip install -r "lambda_layer/requirements.txt" --target "$DEPLOY_DIR/lambda_layer/python/lib/python3.13/site-packages"
else
    echo "Warning: lambda_layer/requirements.txt not found."
fi



echo "Deployment complete."
