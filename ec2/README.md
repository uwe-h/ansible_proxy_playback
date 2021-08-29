## Key Steps for implementation

1. Set HTTPS proxy to your https proxy instance (`docker-compose.yml`)
1. AWS CLI (`Certificate Validation`)
   1. Copy mitmproxy root cert to `/usr/local/share/ca-certificates`
   1. `update-ca-certificates`
2. AWS API with boto3 (`Certificate Validation`)
   1. install with `pip` `certifi`
   1. Make the root certificate available for `certifi` 

### Test if it works properly
`aws ssm list-associations`

`curl -v  https://ssm.us-west-2.amazonaws.com/`

### Validate Certificate
`openssl s_client -showcerts -connect ssm.us-west-2.amazonaws.com:443 -proxy httpproxy:8080`

### Root CA
#### Get Certificate
`echo | openssl s_client -connect ssm.us-west-2.amazonaws.com:443 -proxy httpproxy:8080 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > cert.pem`
####Validate
`openssl verify -verbose -CAfile /usr/local/share/ca-certificates/rootCA.crt cert.pem`
 
`openssl x509 -in cert.pem -inform pem -text`
