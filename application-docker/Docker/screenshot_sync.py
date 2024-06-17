#!/usr/bin/python
import os
import subprocess
from snowflake.snowpark import Session

def get_login_token():
    with open("/snowflake/session/token", "r") as f:
        return f.read()

snowpark_config = {
    "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
    "host": os.environ.get("SNOWFLAKE_HOST"),
    "authenticator": "oauth",
    "token": get_login_token(),
    "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
    "database": os.environ.get("SNOWFLAKE_DATABASE"),
    "schema": os.environ.get("SNOWFLAKE_SCHEMA")
 }

connection = Session.builder.configs(snowpark_config).create()

connection.sql("CREATE STAGE IF NOT EXISTS DOOM_SCREENSHOTS").show()

for file in os.listdir():
    if ".pcx" in file:
        subprocess.run(["convert", file, file[:-4]+".png"])
        connection.sql(f"PUT file:///opt/crispy-doom/{file[:-4]+'.png'} @DOOM_SCREENSHOTS AUTO_COMPRESS=FALSE OVERWRITE=TRUE").show()

connection.sql("LIST @DOOM_SCREENSHOTS").show()
