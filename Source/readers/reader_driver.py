import os

from readers import BeaconHillReader, BYondReader, AramarkReader, BimboJobSearcher, CaptechReader, CollaberaReader, \
    ComcastReader, CVSReader, CyberCodersReader

os.chdir(r"f:\job_search_utilities")
nic_ = "nic@secretsmokestack.com"
testmode = False
AramarkReader(customer_id=nic_, testmode=testmode)
BYondReader(customer_id=nic_, testmode=testmode)
BeaconHillReader(testmode=testmode, customer_id=nic_)
BimboJobSearcher(customer_id=nic_, testmode=testmode)
CaptechReader(customer_id=nic_, testmode=testmode)
CollaberaReader(customer_id=nic_, testmode=testmode)
ComcastReader(customer_id=nic_, testmode=testmode)
CVSReader(customer_id=nic_, testmode=testmode)
CyberCodersReader(customer_id=nic_, testmode=testmode)
