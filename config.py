from os import getenv
import boto3

ssm = boto3.client("ssm", region_name='us-east-1')

environment = getenv("ENV", f"{PATH_DB_NAME}")

path = '/{}'.format(environment)

MODE = getenv("MODE", "remote")

if MODE == "remote":
    DB_HOST = ssm.get_parameter(
        Name='/general/DB_HOST',
        WithDecryption=False,
    )['Parameter']['Value']
elif MODE == "local":
    DB_HOST = getenv("DB_HOST", "localhost")

DB_NAME = ssm.get_parameter(
    Name='{}/DB_NAME'.format(path),
    WithDecryption=False,
)['Parameter']['Value']

DB_USER = ssm.get_parameter(
    Name='/general/DB_USER',
    WithDecryption=False,
)['Parameter']['Value']

DB_PASS = ssm.get_parameter(
    Name='/general/DB_PASS',
    WithDecryption=True,
)['Parameter']['Value']

DB_PORT = getenv('DB_PORT', 5432)
