# OCI Auto-Instance Creator

This repository contains a Python script that automates the creation of a Compute Instance in Oracle Cloud Infrastructure (OCI). The script is designed to be resilient; if it fails to create an instance (for example, due to temporary "out of capacity" errors), it will automatically wait for one minute and retry until it succeeds.

This is particularly useful for provisioning resources in high-demand regions or for obtaining Ampere A1 (ARM) shapes which are often subject to capacity limits.

## Features

-   **Automated Instance Creation**: Launches an OCI Compute instance based on your specifications.
-   **Resilient Retries**: Automatically retries the creation process upon failure, making it ideal for overcoming temporary capacity issues.
-   **Configurable**: Easily set your desired compartment, shape, image, and network details directly in the script.
-   **Secure**: Uses your local SSH public key to authorize access to the new instance.

## Prerequisites

Before you can run this script, you need the following:

1.  **An Oracle Cloud Infrastructure (OCI) Account**: If you don't have one, you can sign up for a [Free Tier account](https://www.oracle.com/cloud/free/).
2.  **OCI CLI and SDK Configuration**: You must have the OCI CLI installed and configured. This script relies on a `config` file located at `~/.oci/config` for authentication.
    -   Follow the official guide to [install the CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm).
    -   Follow the guide to [configure the CLI](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliconfigure.htm). This process will generate the necessary API keys and the configuration file.
3.  **An Existing VCN and Subnet**: The script needs to launch the instance into a pre-existing Virtual Cloud Network (VCN) and subnet. You will need the OCID of the subnet.
4.  **SSH Key Pair**: An SSH public key is required to be added to the instance's `authorized_keys` file for you to log in after creation.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/I-l-y-a-Z-z/OCI-Instance-creation-automation.git
    cd OCI-Instance-creation-automation
    ```

2.  **Install the required Python dependencies:**
    The script requires the `oci` Python SDK. The included `requirements.txt` file lists all necessary dependencies. Install them using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the script, you must edit the Python file (`script.py`) to replace the placeholder values with your specific OCI information.

Open `script.py` and modify the following variables:

-   `compartment_id`: The OCID of the compartment where the instance will be created.
    ```python
    compartment_id = "YOUR_TENANCY_OCID" # Or your specific compartment OCID
    ```

-   `availability_domain`: The AD where the instance will be launched. Example: `SKIT:EU-MADRID-1-AD-1`.
    ```python
    availability_domain = "YOUR_AVAILABILITY_DOMAIN"
    ```

-   `image_id`: The OCID of the OS image you want to use (e.g., Ubuntu, Oracle Linux).
    ```python
    image_id = "YOUR_IMAGE_OCID"
    ```
-   `instance_name`: A display name for your instance.
    ```python
    instance_name = "my-new-instance"
    ```
-   `ssh_key_path`: The absolute path to your **public** SSH key file (e.g., `~/.ssh/id_rsa.pub`).
    ```python
    ssh_key_path = "/home/user/.ssh/id_rsa.pub"
    ```

-   `subnet_id`: The OCID of the subnet where the instance's VNIC will be created. Find this under **Networking -> Virtual Cloud Networks -> [Your VCN] -> Subnets**.
    ```python
    # This is found inside the create_vnic_details section
    subnet_id="YOUR_SUBNET_OCID"
    ```
-   **Shape Configuration (Optional)**: The script is pre-configured for an ARM-based `VM.Standard.A1.Flex` shape with 4 OCPUs and 24 GB of memory. You can adjust the `shape`, `ocpus`, and `memory_in_gbs` to fit your needs.
    ```python
    shape = "VM.Standard.A1.Flex"
    shape_config = oci.core.models.LaunchInstanceShapeConfigDetails(
        ocpus=4,
        memory_in_gbs=24
    )
    ```


## Usage

Once you have configured the script, simply run it from your terminal:

```bash
python script.py
```

The script will start attempting to create the instance. You will see output messages indicating its progress.

-   **On Success**: It will print the new instance's name and OCID and then exit.
-   **On Failure**: It will print the error message from the OCI service, wait for 60 seconds, and then try again indefinitely.

To stop the script, press `Ctrl+C`.

## How It Works

The script is divided into two main functions:

-   `create_instance()`: This function builds the `LaunchInstanceDetails` object with all your specified configurations and calls the OCI API to launch the instance. It handles `ServiceError` exceptions, printing out useful debugging information if an error occurs.
-   `create_instance_until_success()`: This function runs an infinite `while` loop that repeatedly calls `create_instance()`. If `create_instance()` returns a valid instance object, the loop breaks. If it returns `None` (indicating a failure), the script sleeps for 60 seconds before the next iteration.

## Contributing

Contributions are welcome! If you have suggestions for improvements or find a bug, please feel free to open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.