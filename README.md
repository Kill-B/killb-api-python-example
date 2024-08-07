# KillB API Migration Guide: v1 to v2

-----------

## Introduction

#### This guide demonstrates the differences between KillB API v1 and v2, highlighting the ease of migration and the advantages of using the v2 SDK. The v2 API simplifies the implementation process by providing a comprehensive SDK, making it easier and more efficient for developers to interact with the API. If you are currently using v1, this guide will show you how to migrate part of your implementation to v2 while retaining some functionalities in v1 if necessary.

---------

## Differences Between v1 and v2

### API v1

- Manual Requests: Developers need to manually handle each API request.
- Multipart User Creation: User creation requires multipart form data.
- No SDK: Developers need to manage all API interactions without the help of an SDK.


### API v2

- SDK Available: The [killb-sdk-python](!https://pypi.org/project/killb-sdk-python/#description) simplifies API interactions.
- Simplified User Creation: User creation does not require multipart form data.
- Improved Documentation: Each method in the SDK is well-documented, aiding implementation.


### Installation

To get started, install the necessary dependencies:

```shell
    pip install killb-sdk-python requests python-dotenv   
```

-----

### Environment Variables

Ensure your .env file contains the necessary credentials:

```shell
// For v1
KILLB_API_BASE_URL_V1=<your_v1_base_url>
KILLB_API_TOKEN_V1=<your_v1_api_token>
KILLB_CREDENTIALS_EMAIL=<your_v1_email>
KILLB_CREDENTIALS_PASSWORD=<your_v1_password>

// For v2
KILLB_API_BASE_URL_V2=<your_v2_base_url>
KILLB_API_TOKEN_V2=<your_v2_api_token>
KILLB_CREDENTIALS_EMAIL_V2=<your_v2_email>
KILLB_CREDENTIALS_PASSWORD_V2=<your_v2_password>
```

------

## Example Code Using v1 for User and Account, v2 for Quotation and RAMP

### Benefits of Using v2

With v2, you only need to import our SDK, simplifying the implementation process significantly. This section demonstrates how to use v1 for user and account creation, while leveraging the v2 SDK for quotations and RAMPs.

### Code Implementation
````python
import os
from killb.client import Client
from dotenv import load_dotenv

load_dotenv()

client_v2 = Client(environment='SANDBOX', email=os.getenv('KILLB_CREDENTIALS_EMAIL_V2'),
                       password=os.getenv('KILLB_CREDENTIALS_PASSWORD_V2'), api_key=os.getenv('KILLB_API_TOKEN_V2'))

quotation = client_v2.Quotation.create(data={
        "fromCurrency": "DESIRED_CURRENCY",
        "toCurrency": "DESIRED_CURRENCY",
        "amountIsToCurrency": False,
        "amount": 0, # DESIRED AMOUNT
        "cashInMethod": "DESIRED_CASH_IN", # DESIRED CASH_IN METHOD
        "cashOutMethod": "DESIRED_CASH_OUT" # DESIRED CASH_OUT METHOD
    })

ramps = client_v2.Ramps.create(
        data={"quotationId": "QUOTATION_ID", "accountId": "ACCOUNT_ID", "userId": "USER_ID"})
````

### Summary

The v2 SDK makes the implementation process more streamlined and efficient. While you can still use v1 for certain operations, migrating to v2 for quotations and RAMPs offers several advantages, including better documentation and reduced complexity.

For a complete implementation example using both v1 and v2, refer to the `examples/killb_api_v1_with_v2` directory.

This version provides a clear structure and detailed steps to help developers understand the differences between v1 and v2, the benefits of using v2, and how to migrate their existing implementations.

### Important

### ** API DOCUMENTATION - V2 - https://killbapi.stoplight.io/docs/killb-v2/365bbddbae725-api-version-2-0-new-features-overview ** 