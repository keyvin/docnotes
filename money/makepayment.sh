#!/bin/bash

read -p"Make a payment on debt:" pay
touch payhistory

echo $(cat payhistory | wc -l) $pay >> payhistory

echo Total Payments: $(./totaller.sh payhistory)

echo Debt left: $(( $(./totaller.sh debtsnowball) - $(./totaller.sh payhistory) ))


