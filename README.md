# Tenant Lift and Shift / Tenant Central Management

# Beta Disclaimer

This script is in Beta and you may encounter bugs. Please report any bugs you encounter so they can be fixed. Please include any relevant error messages, the modes/settings you were running the script in and any other information you believe to be relevant. Log files are now produced with each run so if you encounter any errors please include any associated log files.

## Conditions for Use / Caveats

### Name Changes

In all but a few cases, the name of an entity is its only cross tenant identifier. Changing the name of entities and then running this script in sync mode, will result in that entity from being deleted from the clone tenant, and then added back with the new name. This will disrupt any other entities on the Prisma Cloud tenant that depend on it. Using this script means in most cases you will not be able to change the name of entities that you are trying to sync/update across all the tenants you are managing. A fix to this problem is in the works but for now, please understand this limitation.

### Cloud Accounts

GCP and Azure Cloud Accounts can not be migrated without the user supplying the credentials. For security reasons, the Prisma Cloud API does not return GCP or Azure credentials. To overcome this, please supply the Service Account Key JSON file to the ‘cloud_credentials/gcp’ or the ‘cloud_credentials/azure’ folder and name the terraform file to be the exact same name of the Cloud Accounts name in Prisma Cloud, spaces included. For best results, copy and paste the cloud accounts name into the filename to ensure sameness.

Oracle Cloud (OCI) Accounts are not supported by this script at this time.

### Alert Rules

Integrations can not be migrated by this script. All Alert Rules that rely on external integrations will be migrated but will not be configured to use the external integrations. These alert rules will be migrated and disabled. The user will have to manually configure these alert rules to use the integrations.

### Modules

Currently, modules configuration migration/sync is not supported. You are able to migrate/sync IAM Policies and Saved Searches as well as Cloud Accounts that use Data Security. However other modules and module functionality are not supported at this time. For example, if you try to migrate a custom policy or saved search from a module like Microsegmentation, you will encounter errors.  Fortunately, module support is on the roadmap for this tool.

### Trusted Login IPs

The script will not automatically enable the trusted Login IPs to ensure the machine running the script does not get blocked from the tenant. After the migration or sync process is done, someone will have to manually enable them.

## Setup/Installation

This script was written in Python3

Clone this project from github onto the machine of your choice. This script requires a reliable internet connection and may run into trouble if it is being run on a machine connected to a VPN that does TLS Interception.

This script relies on 4 external Python libraries:  
Requests - An installation guide can be found here: https://docs.python-requests.org/en/master/  
PyYAML - An installation guide can be found here: https://pyyaml.org/  
Loguru - An installation guide can be found here: https://github.com/Delgan/loguru  
tqdm - An installation guide can be found here: https://github.com/tqdm/tqdm

You can also install the dependencies quickly by using Python’s package manager and the supplied requirements file.

`pip3 install -r requirements.txt`

## Running the script 

Get your Prisma Cloud Access Key, Secret Key and App URL ready. The script will ask you for them during setup.

If you intend to migrate/sync cloud accounts, Service Account Key JSON file for each Azure and GCP cloud account into the cloud credentials directory and into the appropriate subfolder. Rename each Service Account Key JSON file so that the file name matches the cloud accounts name in Prisma Cloud.  
![GCP Cloud Account Example](https://github.com/adam-hamsuth/pc-migration-managment/blob/main/images/gcp_cloud_account.png?raw=true)  
![Cloud Credentials Directory Example](https://github.com/adam-hamsuth/pc-migration-managment/blob/main/images/cloud_cred_dir.png?raw=true) 

This script includes a text based menu that allows you to customize the way the script runs. This is the recommended way to interact with this script. Please note that for the sake of user choice, the script allows you to migrate/sync components of a Prisma Cloud tenant without first migrating the components dependencies. For a full list of components and their dependencies see the Overview section. 

Run the main menu script using Python3 after all required Python3 libraries have been installed.

`python3 main.py`

You will be prompted to run the script in Migrate or Sync mode.

Once you have selected a mode you will be prompted to do a full migration or a full sync. If you select YES then all Prisma Cloud components that are supported by this script will be migrated or synced across the tenants the script has access too. If you select NO then you will be asked to pick and choose what Prisma Cloud components will be migrated or synced with this script. You will also be able to selectively enable Add, Update, and Delete operations for sync mode through this customization menu.

There are also two command line arguments that can be used. -yaml and -quiet.

-yaml Allows plain text files to be created with tenant credentials so that you can run the script multiple times without re-entering credentials. When you do this for the first time, the script will walk you through a set up process and a tenant_credentials.yml file will be created. The next time the script is run with the -yaml flag, this file will be read from and the tenants will be loaded in automatically. If you need to make a change to this file to update the tenants that are being managed by the script, you can manually edit tenant_credentials.yml or delete it and run the script to re-do the setup process. 

-quiet Hides the logging output and only shows progress bars in the terminal output.

`python3 main.py -yaml`

## Overview and Other Information

This script supports two primary modes of operation, migrate and sync. The difference between the migrate and sync mode is as follows: Migrate mode assumes the destination tenant is empty or mostly empty. The migrate mode will not do checks/comparisons on nested values of entities. For example, if you are migrating compliance standards to an empty or mostly empty tenant. Migrate mode will only look at the top level compliance standard to determine if the compliance standard and its requirements and sections need to be brought over. In sync mode, the script would look through all of the compliance data and could find and add a single missing compliance section. This means that migrate mode is faster and sync mode is much slower but does a more thorough job. Sync mode also allows for components to be updated and even deleted. Migrate mode will only add components or update default components as that is the only change that can be made to default components on Prisma Cloud.

This script is divided up into modules that each migrate/sync one component of Prisma Cloud. For example, the cloud_migrate module handles the migration of Cloud Accounts.

Many modules rely on other modules being run first due to dependencies that exist within prisma cloud. For example, the Users modules should only be run/migrated after the Roles module. Users belong to Roles and if the Roles do not exist on the tenant when the Users are migrated, the Users will all be placed into the default Role and not into the Roles they should be as the roles do not yet exist.

Prisma Cloud components that can be migrated and synced by this script:

Cloud Accounts - 	Depends on: None

Account Groups - 	Depends on: Cloud Accounts

Resource Lists - 	Depends on: None

User Roles - 		Depends on: Account Groups, Resources List

Users - 		Depends on: User Roles

Trusted IPs - 		Depends on: None

Saved Searches -	Depends on: Trusted IPs

Compliance Data -	Depends on: None

Policies - 		Depends on: Compliance Data, Saved Searches

Alert Rules - 		Depends on: Account Groups, Resource Lists, Policies

Anomaly Settings - 	Depends on: Policies

Enterprise Settings - 	Depends on: None
