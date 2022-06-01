docker run -it --rm -p 8888:8080 -p 8443:8443 -e SIMPLESAMLPHP_SP_ENTITY_ID=http://localhost:8000/sso/local/ -e SIMPLESAMLPHP_SP_ASSERTION_CONSUMER_SERVICE=http://localhost:8000/sso/local/acs/ -e SIMPLESAMLPHP_SP_SINGLE_LOGOUT_SERVICE=http://localhost:8000/sso/local/slo/ kristophjunge/test-saml-idp

######################################################################################################################################
## There are two static users configured in the IdP with the following data:                                                        ##
##                                                                                                                                  ##
## UID	Username	Password	Group	Email                                                                                             ##
## 1	user1	user1pass	group1	user1@example.com                                                                                     ##
## 2	user2	user2pass	group2	user2@example.com                                                                                     ##
## However you can define your own users by mounting a configuration file:                                                          ##
##                                                                                                                                  ##
## -v /users.php:/var/www/simplesamlphp/config/authsources.php                                                                      ##
## You can access the SimpleSAMLphp web interface of the IdP under http://localhost:8080/simplesaml. The admin password is secret.  ##
##                                                                                                                                  ##
## https://hub.docker.com/r/kristophjunge/test-saml-idp/                                                                            ##
######################################################################################################################################

