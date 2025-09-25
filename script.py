import time
import oci
from oci.exceptions import ServiceError

# Load OCI configuration from default location
config = oci.config.from_file("~/.oci/config")

compute_client = oci.core.ComputeClient(config)

# Replace these values with your own information
compartment_id = "YOUR_COMPARTMENT_OCID_HERE"  
availability_domain = "YOUR_AVAILABILITY_DOMAIN_HERE" 
shape = "VM.Standard.A1.Flex" 
shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
    ocpus=4,
    memory_in_gbs=24
)  
image_id = "YOUR_IMAGE_OCID_HERE"
instance_name = "your-instance-name"

# Path to your SSH public key file
ssh_key_path = "/path/to/your/ssh_public_key.pub"

def create_instance():
    try:
        create_instance_details = oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            availability_domain=availability_domain,
            shape=shape,
            shape_config=shape_config,
            display_name=instance_name,
            source_details=oci.core.models.InstanceSourceViaImageDetails(
                source_type="image",
                image_id=image_id
            ),
            create_vnic_details=oci.core.models.CreateVnicDetails(
                assign_public_ip=True,
                subnet_id="YOUR_SUBNET_OCID_HERE"  # Replace with your subnet OCID
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

if __name__ == "__main__":
    create_instance_until_success()