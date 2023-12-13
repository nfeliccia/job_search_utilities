import os

from readers import BeaconHillReader, BYondReader, AramarkReader

os.chdir(r"f:\job_search_utilities")
nic_ = "nic@secretsmokestack.com"
testmode = False
AramarkReader(customer_id=nic_, testmode=testmode)
BYondReader(customer_id=nic_, testmode=testmode)
BeaconHillReader(testmode=testmode, customer_id=nic_)
