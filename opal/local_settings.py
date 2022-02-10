"""
To run a local copy for development or other reasons, add this file to your .gitignore file
and then modify the values as needed. 
"""
import secrets

env = {
    "env" : "development",
    "opal_secret_key" : secrets.token_urlsafe(), #set a random secret key each time the application starts
    "debug" : "True",
    "allowed_hosts" : ["*"],
    #"database" : "postgres",
    "database" : "sqlite", # uncomment this line and comment out the line above to use sqlite
    "db_name" : "opal",
    "db_password" : "use_a_stron_password",
    "db_user" : "opal_system",
    "db_host" : "localhost",
    "db_port" : "",
    "adfs_enabled" : False,
    "adfs_server" : "adfs.example.com",
    "adfs_client_id" : "00000000-0000-0000-0000-000000000000",
    "adfs_relying_party_id" : "00000000-0000-0000-0000-000000000000",
    "adfs_audience" : "microsoft:identityserver:00000000-0000-0000-0000-000000000000",
}
