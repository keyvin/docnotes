#gen CA
openssl genpkey -algorithm RSA -out rootkey.pem -pkeyopt rsa_keygen_bits:4096

openssl req -new -key rootkey.pem -days 5480 -extensions v3_ca -batch -out root.csr -utf8 -subj '/C=US/O=Kevin/OU=KevinRoot'

openssl x509 -req -sha256 -days 3650 -in root.csr -signkey rootkey.pem -set_serial 100221 -extfile openssl.root.cnf -out root.pem

#Gen directly signed cert
openssl genpkey -algorithm RSA -out eekey.pem -pkeyopt rsa_keygen_bits:2048

openssl req -new -key eekey.pem -days 1096 -extensions v3_ca -batch -out example.csr -utf8 -subj '/CN=ma.sdf.org'

openssl x509 -req -sha256 -days 1096 -in example.csr -CAkey rootkey.pem -CA root.pem -set_serial 10092 -out ma.sdf.org.pem -extfile openssl.ss.cnf
