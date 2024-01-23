# GVE DevNet ISE Expired Guest Users
This prototypes leverages the ISE APIs to retrieve and delete the expired guests users. A python script is scheduled to run every N minutes to automate the process. 
## Contacts
* Roaa AlKhalaf

## Solution Components
* ISE 
* ISE APIs
* Python


## Docker Image / GitHub Actions Deployment

To make the code more **portable** and **easier** for users to deploy, you can automatically create a GitHub Package (Docker Image) or GitHub Release (GoLang Application Binaries) by configuring the relevant files in `.github/workflows` and the repo. Users then have the option to pull and run the docker image (or binaries) with your application and environment configured to skip over setup steps (ex: installing python). 

Refer to the documentation [here](https://wwwin-github.cisco.com/gve/docker-and-github-actions-templates) for how to set up this functionality.


## Prerequisites

#### ISE REST APIs
1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to `Administration > System > Settings` and select `ERS Settings` from the left panel.
3. Enable the ERS APIs by selecting **Enable ERS** for Read/Write
4. Do not enable CSRF unless you know how to use the tokens.
5. Select **Save** to save your changes.
6. The following ISE Administrator Groups allow REST API access:
    * SuperAdmin: Read/Write
    * ERSAdmin: Read/Write
    * ERSOperator: Read Only


#### REST API access for sponsor accounts
1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to `Work Centers > Guest Access > Portals & Components` and Select Sponsor Groups from the sidebar.
3. Create or edit a sponsor group. 
4. Ensure that the Access Cisco ISE guest accounts using the programmatic interface (Guest REST API) checkbox is selected.
5. Select **Save** to save your changes.



 #### Create a sponsor account
1. Login to your ISE PAN using the admin or other SuperAdmin user.
2. Navigate to `Administration > Identity Management > Identities`.
3. Click the Add button to create a new Network Access User.
4. Fill in the Name and Password, select the User Group that was updated in the previous step.
5. Select **submit** to save your changes.


## Installation/Configuration
1. Clone this repository with `git clone [repository name]`. To find the repository name, click the green `Code` button above the repository files. Then, the dropdown menu will show the https domain name. Click the copy button to the right of the domain name to get the value to replace [repository name] placeholder.
2. Add the ISE credentials in the `.env` file:

```
ISE_IP=<ISE HOST>
USERNAME=<Sponsor Account USERNAME>
PASSWORD=<Sponsor Account PASSWORD>

SCHEDULER_DAILY_MIN=<NUMER of MIN to RUN the SCRIPT>

```

3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

## Usage
To run the code, use the command:
```
$ python3 main.py
```
#
# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.