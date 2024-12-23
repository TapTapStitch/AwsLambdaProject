# Build a REST API using AWS Lambda and API Gateway

## Tools and technologies
 - API contract (Swagger)
 - AWS Lambda
 - Lambda Layer
 - DynamoDb
 - API Gateway
 - Cognito
 - JsonSchema\Pydantic
 - pytest\moto
 - Postman

To build a REST API using AWS Lambda and API Gateway with the mentioned tools and technologies, here's a structured approach you can follow:

### 1. API Contract (Swagger)
Start by defining your API contract using Swagger (OpenAPI). This will outline your API's endpoints, methods, request/response payloads, and any necessary parameters. You can use tools like Swagger Editor or write the Swagger YAML/JSON manually.

### 2. AWS Lambda
Create Lambda functions to implement the business logic for your API endpoints. Each Lambda function should correspond to a specific endpoint and method defined in your Swagger contract.

### 3. Lambda Layer
Use Lambda Layers to manage common dependencies across your Lambda functions

### 4. DynamoDB
Integrate DynamoDB as your database to store and retrieve data for your API operations. Define your table schemas based on your application's data model.

### 5. API Gateway
Configure API Gateway to define your REST API endpoints and connect them to your Lambda functions. Use the Swagger contract to manually create the API structure in API Gateway.

### 6. Cognito
Implement Cognito for user authentication and authorization.

### 7. JsonSchema/Pydantic
Use JsonSchema (or Pydantic) for validating request payloads and responses in your Lambda functions.

### 8. Unittests
Write unit tests for your Lambda functions to validate their functionality in isolation. Use tools like `pytest` to automate testing. Use `moto` to mock AWS services like DynamoDB in your tests, ensuring predictable and repeatable test scenarios.

### 9. Postman
Use Postman for manual testing and validation of your API endpoints. Create collections and write test scripts to ensure your API behaves as expected under different scenarios.


### Steps to Implement:
- **Design**: Start with designing your API contract (Swagger).
- **Lambda Functions**: Implement each endpoint's logic using AWS Lambda.
- **DynamoDB**: Set up tables and integrate with Lambda functions for data operations.
- **API Gateway**: Create and configure API endpoints based on the Swagger contract.
- **Cognito**: Implement user authentication and authorization.
- **Validation**: Use JsonSchema/Pydantic for request/response validation.
- **Testing**: Write unit tests using Pytest/moto and manual tests with Postman.
- **Deployment**: Deploy your Lambda functions, API Gateway configuration, and other resources using AWS CloudFormation.


## Description

Create `Diary Application` - REST API that allows CRUD operations for posts

Proposed API endpoints:
 - GET /posts
 - GET /post/{id}
 - POST /posts
 - PATCH /post/{id}
 - DELETE /post/{id}

Fields:
 - `id`: uuid.uuid4()
 - `title`: str (max len 200)
 - `body`: str (max len 2000)
 - `createdDate`: datetime (auto-generated)
 - `updatedDate`: datetime (auto-generated)
 - `tags`: list(str) Optional

## Implementation

### 1. Define the API Contract (Swagger)

Start by defining the Swagger contract for your API

### 2. AWS Lambda Functions

Implement Lambda functions to handle CRUD operations for posts:
- **GET /posts**: Retrieve all posts from DynamoDB.
- **GET /post/{id}**: Retrieve a specific post by ID from DynamoDB.
- **POST /posts**: Create a new post in DynamoDB.
- **PATCH /post/{id}**: Update an existing post in DynamoDB.
- **DELETE /post/{id}**: Delete a post from DynamoDB.

Ensure Lambda functions handle input validation, generate `id`, `createdDate`, and `updatedDate` automatically, and interact with DynamoDB appropriately.

### 3. DynamoDB Setup

Set up a DynamoDB table to store posts with the following attributes:
- `id` (Primary Partition Key)
- `title`
- `body`
- `createdDate`
- `updatedDate`
- `tags` (Optional)

### 4. API Gateway Configuration

Configure API Gateway:
- Create resources and methods corresponding to each endpoint defined in the Swagger contract.
- Use Lambda integrations to connect API Gateway with the Lambda functions.

### 5. Authentication and Authorization (Optional)

Implement Cognito for user authentication if required for your application.

### 6. Request Validation

Use JsonSchema or Pydantic for request validation to ensure that incoming data conforms to expected formats and constraints.

### 7. Testing

- Write unit tests using Pytest and `moto` for Lambda functions.
- Use Postman for manual testing of API endpoints.

### 8. Deployment

Deploy your Lambda functions, DynamoDB table, API Gateway configuration, and other resources using AWS CloudFormation or AWS Management Console.

By following these steps, you'll create a scalable and efficient REST API for managing posts in the `Diary Application`, leveraging AWS Lambda, API Gateway, DynamoDB, and other relevant tools. Adjustments can be made based on specific requirements or additional features needed for your application.

To implement the `GET /posts` and `PATCH /post/{id}` endpoints with the specified requirements using AWS Lambda, API Gateway, and DynamoDB, here’s how you can proceed:

### 1. `GET /posts` Endpoint

#### Requirements:
- Always return results ordered by `createdDate` ascending.
- Optional parameters:
  - `tags`: Comma-separated list of tags to filter posts by.
  - `limit`: Limits the number of posts returned (optional).

#### Implementation Steps:

### 1. `GET /posts` Endpoint
- **Lambda Function**: Implement a Lambda function to handle the `GET /posts` endpoint.
  - Use `boto3` to interact with DynamoDB.
  - Query the DynamoDB table to fetch posts.
  - Apply sorting by `createdDate` in ascending order.
  - Implement optional filtering by tags if `tags` parameter is provided.
  - Implement optional limiting of results based on the `limit` parameter.

### 2. `PATCH /post/{id}` Endpoint

#### Implementation Steps:

- **Lambda Function: Implement a Lambda function to handle the PATCH /post/{id} endpoint.
  - Extract the id from the path parameter.
  - Validate and update fields (title, body, tags) in the specified post.
  - Use boto3 to update the DynamoDB item.

#### Requirements:
- Allowed fields: `title`, `body`, `tags`.

### Notes:

- **DynamoDB Table**: Ensure your DynamoDB table (`PostsTable` in the examples) has the necessary attributes (`id`, `title`, `body`, `createdDate`, `updatedDate`, `tags`) defined.
- **Error Handling**: Implement appropriate error handling in Lambda functions for cases like item not found, validation errors, etc.

By following these steps and customizing the examples to fit your specific requirements and DynamoDB setup, you can effectively implement the `GET /posts` and `PATCH /post/{id}` endpoints for your `Diary Application` using AWS Lambda, API Gateway, and DynamoDB.

## OAuth 2.0 authorization token (Cognito)

To implement OAuth 2.0 authorization using Cognito for protecting all APIs except `GET /posts/public`, and to configure the response format for `GET /posts/public`, you can follow these steps using AWS services:

### 1. Set Up Cognito User Pool

First, set up a Cognito User Pool to manage user authentication for your API:

- **Create a User Pool**: Set up a Cognito User Pool in the AWS Management Console.
- **Define App Clients**: Create an app client within the User Pool to get client credentials for OAuth 2.0.
- **Define Scopes**: Define scopes (e.g., `read:posts`, `write:posts`) for controlling access to your APIs.

### 2. Configure API Gateway for OAuth 2.0 Authorization

Configure API Gateway to enforce OAuth 2.0 authorization for protected endpoints (`/posts`, `/post/{id}`, `/posts` operations except `GET /posts/public`):

- **Create Authorizers**: Set up an OAuth 2.0 authorizer in API Gateway using your Cognito User Pool.
- **Attach Authorizer to Methods**: Attach the authorizer to API Gateway methods requiring authentication (`/posts`, `/post/{id}`, `/posts` operations).

### 3. Implement Lambda Function for `GET /posts/public`

Create a Lambda function to handle the `GET /posts/public` endpoint:

- **Lambda Function**: Implement a Lambda function to fetch and return public posts information.
  - Query DynamoDB to retrieve all posts.
  - Format the response to include `title`, `body`, `createdDate`.
  - This endpoint does not require authentication, so it can be accessed publicly.


### 4. Configure API Gateway for `GET /posts/public`

Configure API Gateway for the `GET /posts/public` endpoint:

- **Create Resource and Method**: Set up the resource and method in API Gateway for `GET /posts/public`.
- **Integration**: Configure the integration to invoke the Lambda function created for `GET /posts/public`.
- **Authorization**: Ensure that no authorization is required for this endpoint (`Authorization` set to `None`).

### 5. Deployment and Testing

- Deploy your API configuration in API Gateway.
- Test both protected endpoints (`/posts`, `/post/{id}`, etc.) requiring OAuth 2.0 token authentication using tools like Postman, ensuring they return `401 Unauthorized` without a valid token.
- Test the `GET /posts/public` endpoint to ensure it returns the expected `title`, `body`, `createdDate` information without requiring authentication.

### Additional Considerations:

- **Error Handling**: Implement appropriate error handling in your Lambda functions and API Gateway configuration for scenarios like DynamoDB errors, unauthorized access attempts, etc.
  
# Steps

### 1. Create Swagger Contract

Define your Swagger contract (OpenAPI specification) to document your API endpoints, request/response schemas, and parameters. This serves as a blueprint for your API implementation.

### 2. Implement CRUD API Endpoints with AWS Lambda

Develop AWS Lambda functions for CRUD operations on posts:
- **GET /posts**: Retrieve all posts.
- **GET /posts/{id}**: Retrieve a specific post by ID.
- **POST /posts**: Create a new post.
- **PATCH /posts/{id}**: Update an existing post.
- **DELETE /posts/{id}**: Delete a post.

Ensure each Lambda function is implemented to handle its respective endpoint's logic.

### 3. Create Lambda Layer with Third-Party Libraries

Create a Lambda Layer that contains third-party libraries such as `boto3` for AWS SDK operations, `jsonschema` for initial request body validation, and any other shared utilities.

### 4. Use JsonSchema for Request Body Validation

Initially, use JsonSchema for request body validation to ensure incoming data conforms to expected formats and constraints defined in your Swagger contract.

### 5. Add Authorization with AWS Cognito

Implement OAuth 2.0 authorization using AWS Cognito:
- Set up a Cognito User Pool.
- Define scopes and configure API Gateway to enforce authorization for protected endpoints.
- Allow public access (`GET /posts/public` endpoint) without requiring authorization.

### 6. Add Unit Tests with 85% Coverage

Write unit tests to validate the functionality of your Lambda functions:
- Ensure each endpoint's behavior is tested thoroughly, covering positive and negative scenarios.
- Aim for 85% test coverage to ensure comprehensive testing of your API's functionality.

### 7. Add Postman Tests

Create Postman tests to verify the behavior of your API endpoints:
- Test positive scenarios (e.g., successful POST, GET, PATCH, DELETE operations).
- Test negative scenarios (e.g., error handling for invalid requests, unauthorized access attempts).

### 8. Update Implementation with Pydantic for PATCH Request

Replace JsonSchema with Pydantic for request body validation specifically for the PATCH request endpoint (`PATCH /posts/{id}`):
- Modify the Lambda function handling the PATCH request to use Pydantic for validating and parsing incoming request payloads.

### 9. Use CloudFormation for Deployment to AWS

Deploy your AWS infrastructure using AWS CloudFormation:
- Define your Lambda functions, API Gateway configurations, DynamoDB tables, and Cognito configurations in CloudFormation templates.
- Automate the deployment process to ensure consistency and repeatability across environments.


# Definition of Done
The "Definition of Done" outlines the completion criteria for your project:

### 1. Link to Your Repository

Create a public repository on GitLab. Ensure it includes:

- **Lambda functions**: Implement CRUD operations for posts.
- **Swagger file**: Documenting API endpoints, request/response schemas, and parameters.
- **Lambda layer**: Containing third-party libraries shared across Lambda functions.
- **Unit tests**: Ensuring functionality and edge cases are covered.
- **Postman tests**: Validating API endpoints.
- **CloudFormation templates**: For deploying AWS resources.

### 2. Unittests Coverage >= 85%

Write comprehensive unit tests using a framework like Pytest for your Lambda functions and utilities:
- Test each endpoint’s functionality.
- Ensure edge cases and error handling are covered.
- Aim for 85% or higher coverage to ensure robust testing.

### 3. Swagger File

Create a Swagger (OpenAPI) file (`swagger.yaml`) that:
- Defines all API endpoints (`GET /posts`, `POST /posts`, `PATCH /posts/{id}`, `DELETE /posts/{id}`, `GET /posts/public`).
- Specifies request/response schemas and parameters.
- Documents any security definitions (OAuth 2.0 with Cognito).

### 4. Postman Collection

Create a Postman collection (`Diary Application.postman_collection.json`) that:
- Includes requests for each API endpoint (GET, POST, PATCH, DELETE).
- Provides sample payloads for request testing.
- Contains tests to verify API responses (positive and negative scenarios).

### 5. Deploy/Delete Stack

Use AWS CloudFormation for deploying and deleting your stack:
- **Deployment**: Define CloudFormation templates (`template.yaml`) to provision AWS resources (Lambda functions, API Gateway, DynamoDB, Cognito).
- **Deletion**: Ensure cleanup scripts or CloudFormation stacks to remove all provisioned resources.

### Example Repository Structure

Your repository structure might look like this:

```
|-- diary-application/
    |-- lambda_functions/
        |-- get_posts.py
        |-- create_post.py
        |-- update_post.py
        |-- delete_post.py
        |-- lambda_layer/
            |-- requirements.txt
            |-- utils.py
    |-- tests/
        |-- test_get_posts.py
        |-- test_create_post.py
        |-- test_update_post.py
        |-- test_delete_post.py
    |-- swagger.yaml
    |-- Diary_Application.postman_collection.json
    |-- template.yaml
    |-- README.md
```
