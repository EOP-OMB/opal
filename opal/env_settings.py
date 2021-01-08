"""
This file contains the production settings for the opal application as deployed at OMB.  
To run a local copy for development or other reasons, add this file to your .gitignore file
and then modify the values as needed. 
"""

env = {
    "env" : "production",
    "opal_secret_key" : "=&98a-%loivi0af$kqc*@-3+_^m_2sy(hm$vyv&u9^$1_-nbw7",
    "debug" : "False",
    "allowed_hosts" : ["ssp.omb.gov"],
    "database" : "postgres",
    "db_password" : "DcpwXkn3_muYG7fNyxds"
}
