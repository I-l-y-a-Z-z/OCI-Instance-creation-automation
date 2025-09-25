import time
import oci
from oci.exceptions import ServiceError

config = oci.config.from_file("~/.oci/config")

compute_client = oci.core.ComputeClient(config)

compartment_id = config['tenancy']  
availability_domain = "SKIT:EU-MADRID-1-AD-1" 
shape = "VM.Standard.A1.Flex" 
shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
    ocpus=4,
    memory_in_gbs=24
)  
image_id = "ocid1.image.oc1.eu-madrid-1.aaaaaaaaw4sdmsq4g33nw5dgeex5qzqwdjchh4rjcb5wka5j2rc3yup7jigq"
instance_name = "hellyeah"


ssh_key_path = "/home/ilyazz/.oci/api_public_key.pub"

def create_instance():
    try:
        create_instance_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            availability_domain=availability_domain,
            shape=shape,
            shape_config = shape_config,
            display_name=instance_name,
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=image_id
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=True,
                subnet_id="ocid1.subnet.oc1.eu-madrid-1.aaaaaaaazhss42ar3uoofc7brkxrn36sth4s26h3tqaqgseuop3k5x6xdatq"  # You need to replace this with the OCID of your subnet
            ),
            metadata={
                "ssh_authorized_keys": open(ssh_key_path, "r").read()
            }
        )

        instance = compute_client.launch_instance(create_instance_details)
        print(f"Instance {instance_name} created successfully with OCID: {instance.id}")
        print("__________________________________")
        return instance
    except ServiceError as e:
        print("Error during instance creation:")
        print(f"Message:", e.message)
        print(f"Opc Request ID:", e.request_id)
        print("__________________________________")
        return None

def create_instance_until_success():
    while True:
        print("__________________________________")
        instance = create_instance()
        if instance:
            break
        else:
            print("Instance creation failed. Retrying in 1 minute...")
            time.sleep(60) 

create_instance_until_success()
