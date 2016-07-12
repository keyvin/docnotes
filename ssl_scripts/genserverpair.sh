#Gen directly signed cert

echo "Common Name"
read cn

echo "bits:"
read bits

echo "Keyfile:"
read pkeyfile

echo "certfile:"
read servercert

echo "serial:"
read serial

openssl genpkey -algorithm RSA -out ./working/$pkeyfile -pkeyopt rsa_keygen_bits:2048

openssl req -new -key eekey.pem -days 1096 -extensions v3_ca -batch -out ./working/example.csr -utf8 -subj '/CN='$cn

openssl x509 -req -sha256 -days 1096 -in ./working/example.csr -CAkey ./working/rootkey.pem -CA ./working/rootCA.pem -set_serial $serial -out ./working/$servercert -extfile openssl.ss.cnf
