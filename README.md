# Tenant Lift and Shift / Tenant Central Management

## Conditions for Use / Caveats

In all but a few cases, the name of an entity is its only cross tenant identifier. Changing the name of entities and then running this script in sync mode, will result in that entity from being deleted from the clone tenant, and then added back with the new name. This will disrupt any other entities on the Prisma Cloud tenant that depend on it. Using this script means in most cases you will not be able to change the name of entities that you are trying to sync/update across all the tenants you are managing. A fix to this problem is in the works but for now, please understand this limitation.

GCP and Azure Cloud Accounts can not be migrated without the user supplying the credentials. For security reasons, the Prisma Cloud API does not return GCP or Azure credentials. To overcome this, please supply the Terraform JSON file to the ‘cloud_credentials/gcp’ or the ‘cloud_credentials/azure’ and name the terraform file to be the exact same name of the Cloud Accounts name in Prisma Cloud, spaces included. For best results, copy and paste the cloud accounts name into the filename to ensure sameness.

Integrations can not be migrated by this script. All Alert Rules that rely on external integrations will be migrated but will not be configured to use the external integrations. These alert rules will be migrated and disabled. The user will have to manually configure these alert rules to use the integrations.

## Quickstart

This script requires Python3 and Python3’s package manager, Pip3

Clone this project onto the machine of your choice.

Install the required Python Libraries with pip3:

`pip3 install -r requirements.txt`

Run the script using the customization menu:

`python3 main_menu.py`

## Setup/Installation

This script was written in Python3

Clone this project from github onto the machine of your choice. This script requires a reliable internet connection and may run into trouble if it is being run on a machine connected to a VPN that does TLS Interception.

This script relies on these two external Python libraries:
Requests. An installation guide can be found here: https://docs.python-requests.org/en/master/
PyYAML. An installation guide can be found here: https://pyyaml.org/

You can also install the dependencies quickly by using Python’s package manager and the requirements file.

`pip3 install -r requirements.txt`

## Run

This script includes a text based menu that allows you to customize the way the script runs. This is the recommended way to interact with this script. Please note that for the sake of user choice, the script allows you to migrate/sync components of a Prisma Cloud tenant without first migrating the components dependencies. For a full list of components and their dependencies see the Overview section. 

Run the main menu script using Python3 after all required Python3 libraries have been installed.

`python3 main_menu.py`

## Overview and Other Information

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