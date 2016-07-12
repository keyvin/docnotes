#!/bin/bash

#gather information for generating root

mkdir working

echo "Enter Orgname: "
read orgname

if [ $orgname=="" ]; then
    echo ""
    #exit
fi
    

echo "Enter Org Description: "
read orgdesc

if [ $orgdesc==""]; then
    echo ""
    #exit
fi

echo "Enter key length"
read length

echo "Name of output"
read out

echo "Read Serial"
read serial

echo "Generating private key:"
openssl genpkey -algorithm RSA -out ./working/$out -pkeyopt rsa_keygen_bits:$length
cp ./working/$out ./working/rootkey.pem
echo "Senerating signing request:"

openssl req -new -key ./working/$out -days 5480 -extensions v3_ca -batch -out ./working/root.csr -utf8 -subj '/C=US/O='$orgname'/OU='$orgdesc

echo "Signing Root"
openssl x509 -req -sha256 -days 3650 -in ./working/root.csr -signkey ./working/$out -set_serial 100221 -extfile openssl.root.cnf -out ./working/rootCA.pem



