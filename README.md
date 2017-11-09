# vpce_setup
sets up the VPC Private Link(VPC Endpoint) for each AWS services currently supported.

## how to use
1. Create security group in your VPC you want to create VPC endpoint, and note the IDs.(ex, sg-1a2b3c...)
  make sure HTTPS(443) is open to the VPC.
2. (Option) if you want to create subnets and note the IDs.(ex, subnet-1a2b3c)
3. Type as below.
   python vpce_setup.py --subnet-ids *Subnet ID1* *Subnet ID2*.... --security-group *Security Group ID*

If you need help, type 'python vpce_setup.py -h'
