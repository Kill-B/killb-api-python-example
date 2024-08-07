from faker import Faker

fake = Faker()

user_data = {
    "firstName": fake.first_name(),
    "lastName": fake.last_name(),
    "phone": f"+551234566{fake.random_number(digits=4, fix_len=True)}",
    "email": fake.email(),
    "dateOfBirth": "1997-01-01",
    "document": {
        "type": "NATIONAL_IDENTITY_CARD",
        "number": str(fake.random_number(digits=10, fix_len=True)),
        "issuedCountryCode": "BR"
    },
    "address": {
        "street1": fake.street_name(),
        "zipCode": fake.zipcode(),
        "city": fake.city(),
        "stateCode": "SP",
        "countryCode": fake.country_code()
    },
    "hasMoreAccounts": False
}


def get_account_data(userId: str):
    return {
        "accountType": "PSE",
        "userId": userId,
        "data": {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "document": {
                "type": "NUIP",
                "number": str(fake.random_number(digits=10, fix_len=True)),
                "issuedCountryCode": "CO"
            },
            "phone": f"+551234566{fake.random_number(digits=4, fix_len=True)}",
            "email": fake.email(),
            "accountNumber": str(fake.random_number(digits=10, fix_len=True)),
            "bankCode": "507",
            "type": "savings",
            "countryCode": "CO"
        }
    }


def get_account_data_wallet(userId: str):
    return {
        "accountType": "WALLET_ACCOUNT",
        "userId": userId,
        "data": {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "document": {
                "type": "PASSPORT",
                "number": str(fake.random_number(digits=10, fix_len=True)),
                "issuedCountryCode": "MX"
            },
            "phone": f"+551234566{fake.random_number(digits=4, fix_len=True)}",
            "email": fake.email(),
            "asset": "USDC",
            "network": "POLYGON",
            "address": "0x111111111111111111111111111111"
        }
    }