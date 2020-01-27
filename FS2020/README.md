# IBM Resilient App Development Workshop Guide *(ETM44T643SH)*

![screenshot](./screenshots/logo.png)

***Shane Curtin, App Engineer, IBM Resilient***

---

## Step 0: *Sign up for SkyTap Account:*

* Go to https://ibm.biz/fs20skytap

* Sign in with email and password provided by course provider

---

## Step 1: *Login to Virtual Environment*

  ![screenshot](./screenshots/1.png)

* Login as `resadmin` with the password shared by your course leader

* Open the **Terminal**

  ![screenshot](./screenshots/2.png)

---

## Step 2: *Check which Python Version is installed*

* Run:
  ```
  $ python --version
  ```
* Output should be:
  ```
  Python 3.6.8
  ```

---

## Step 3: *Make sure Resilient License is Valid*

* Check valid license is configured:
  ```
  $ sudo resutil license
  ```
* If it **does not exist** or is **expired**, source a valid license and run:
  ```
  $ sudo license-import
  ```
* **Paste** your valid license and hit **Enter**:
  ```
  -----BEGIN LICENSE-----
  xxx
  -----END LICENSE-----
  ```
* **Restart** the Resilient Service:
  ```
  $ sudo systemctl restart resilient
  ```

---

## Step 4: *Create Dev User Accounts*

* Open **Terminal**

* Create an **admin** user:
  ```
  $ sudo resutil newuser -createorg -org "Dev" -email "resadmin@example.com" -first "Res" -last "Admin" -password "ResDemo123"
  ```

* Create an **app runner** user
  ```
  $ sudo resutil newuser -org "Dev" -email "apps@example.com" -first "Orchestration" -last "Engine" -password "ResDemo123"
  ```

  ![screenshot](./screenshots/3.png)

  > **NOTE:** For production do NOT specify the `-password` flag. Resilient will prompt for user input

---

## Step 5: *Test User Interface*

* Open **Firefox** from the applications menu and navigate to: [https://127.0.0.1](https://127.0.0.1)

* You will see the Resilient interface

* Use the **admin account** you just created and check that you can login.

* Go to **Administration Settings > Users** to confirm the users were created.

  ![screenshot](./screenshots/4.png)

---

## Step 6: *Create an App Host API Key*

* Go to **Administration Settings > Users > API Keys**

* Click **Create API Key**:

  ![screenshot](./screenshots/6.png)

* Click **All Permissions** for now and name your key

* Scroll down and click **Create**

  ![screenshot](./screenshots/7.png)

* A new window will pop up, click **Copy to Clipboard**, then click **OK**

  ![screenshot](./screenshots/8.png)

---

## Step 7: *Install resilient-circuits*

* Install `resilient-circuits` using `pip`:
  ```
  $ pip install resilient-circuits==34.0.195
  ```

* Confirm it was installed with:
  ```
  $ pip list
  ```

  ![screenshot](./screenshots/5.png)

---

## Step 8: *Configure resilient-circuits*

* Auto generate the **app.config file**:
  ```
  $ resilient-circuits config -c
  ```

* This creates `/home/resadmin/.resilient/app.config`

* Make the **directory for logs**:
  ```
  $ mkdir ~/.resilient/logs
  ```

* Open the `app.config` file in **VS Code:**
  ```
  $ code ~/.resilient/app.config
  ```

* Just under the `[resilient]` heading, paste in your API Key and Secret for now:

  ![screenshot](./screenshots/9.png)

* For easy dev setup, **replace** with the following configs:
  ```
  [resilient]
  # Key ID: XXX / Key Secret: XXX

  host=127.0.0.1
  port=443

  api_key_id=XXX
  api_key_secret=XXX

  org=Dev

  logdir=~/.resilient/logs
  logfile=app.log
  loglevel=INFO

  cafile=false
  ```
* **Save** by pressing **CTRL+S**

> **Note:** sometimes the api_key_id can paste with a slash at the end, this should be removed. 

---

## Step 9: *Run resilient-circuits*

* Open **Terminal**

* Run `resilient-circuits`:
  ```
  $ resilient-circuits run
  ```

* You should see this output if `resilient-circuits` is running successfully:

  ![screenshot](./screenshots/10.png)

* Kill `resilient-circuits` with:
  ```
  $ CTRL + c
  ```

---

## Step 10: *Login/Register X-Force Exchange Account*

* Go to [https://exchange.xforce.ibmcloud.com](https://exchange.xforce.ibmcloud.com)

* Login or Create a new IBMid

  ![screenshot](./screenshots/11.png)

---

## Step 11: *Download + Install Frequently Used Utility Functions*

* Go to [https://exchange.xforce.ibmcloud.com/hub/extension/2b6699ac8a3976b67dfbddee26dbe3a5](https://exchange.xforce.ibmcloud.com/hub/extension/2b6699ac8a3976b67dfbddee26dbe3a5)

* Download the `.zip` package

* Click **Download**:

  ![screenshot](./screenshots/12.png)

* You may need to **accept to popups**:

  ![screenshot](./screenshots/13.png)

* Highlight **Save File** and click **OK**

  ![screenshot](./screenshots/14.png)

* Open **Terminal**

* Change to **Downloads** directory:
  ```
  $ cd ~/Downloads
  ```

* **Unzip** the package:
  ```
  $ unzip fn_utilities-x.x.x.zip
  ```

* **Install** FN Utilities using pip:
  ```
  $ pip install fn_utilities-x.x.x.tar.gz
  ```
  ![screenshot](./screenshots/15.png)


* Import **configurations**:
  ```
  $ resilient-circuits config -u
  ```

  > **NOTE:** if you get an error regarding the `six` library, run:
  > ```
  > $ pip install six==1.13.0
  > ```

* **Import customizations** into Resilient Org:
  ```
  $ resilient-circuits customize -y -l fn-utilities
  ```

  ![screenshot](./screenshots/16.png)

* Run `resilient-circuits`:
  ```
  $ resilient-circuits run
  ```
---

## Step 12: *Testing Utility Functions*
* Open **Firefox** from the applications menu and navigate to: [https://127.0.0.1](https://127.0.0.1)

* You will see the Resilient interface

* Use the **admin account** you created and login

* Create an **Incident**
  * Name: `FN Utilities Demo`

* Add an **Artifact** to that Incident
  * Type: `DNS Name`
  * Value: `resilientsystems.com`

  ![screenshot](./screenshots/17.png)

* Click the **Take Action Button** and run the **Example: Shell Command** Workflow on that Artifact:

  ![screenshot](./screenshots/18.png)

* Check your **Terminal:**

  ![screenshot](./screenshots/19.png)

* This Workflow adds a **Note** to the Incident

  ![screenshot](./screenshots/20.png)

---

## Step 13: *Create new Custom Workflow that uses our Shell Command Function*

* Go to **Customization Settings > Workflows**

  ![screenshot](./screenshots/21.png)

* Click **New Workflow**:
  * Name: **nslookup**
  * Object Type: **Artifact**

  ![screenshot](./screenshots/22.png)

* Scroll down to the Workflow Editor and add an **End Node**

  ![screenshot](./screenshots/23.png)
  ![screenshot](./screenshots/24.png)

* Connect the **Start Node** and **End Node** with a **Connector**

  ![screenshot](./screenshots/25.png)

* Add a **Function** on the **Connector**

  ![screenshot](./screenshots/26.png)

* Place our **Shell Command Function** on the **Connector**

  ![screenshot](./screenshots/27.png)

* Insert the following in the **Pre-Process** Editor:
  ```
  inputs.shell_command = "nslookup"
  inputs.shell_remote = False
  inputs.shell_param1 = artifact.value
  ```

  ![screenshot](./screenshots/28.png)

* Insert the following in the **Post-Process** Editor:
  ```
  note_text = u"Command succeeded: {0}\n\nOutput: {1}".format(results.commandline, results.stdout)

  incident.addNote(helper.createPlainText(note_text))
  ```

  ![screenshot](./screenshots/29.png)

* Close the editor. Scroll up and click **Save & Close**:

  ![screenshot](./screenshots/30.png)

---

## Step 14: *Create new Custom Rule that runs our Workflow*

* Click the **Rules Tab**

* Create a new **Menu Item Rule**

  ![screenshot](./screenshots/31.png)

* Create the Rule with the following attributes:
  * Display Name: **nslookup**
  * Object Type: **Artifact**
  * Workflows: **nslookup**

  ![screenshot](./screenshots/32.png)

* Click **Save & Close**

---

## Step 15: *Run our new Custom Workflow*

* Go to your FN Utilities **Incident**

* Click the **Artifacts Tab**

* Run `nslookup` workflow on the `resilientsystems.com` Artifact
  
  ![screenshot](./screenshots/33.png)

* Check your **Terminal** to see the logs

* This Workflow adds a **Note** to the Incident

  ![screenshot](./screenshots/34.png)

---

## Step 16: *View Logs*
* Open **Terminal**

* Kill `resilient-circuits` with:
  ```
  $ CTRL + c
  ```

* Use VS Code to open **app.log**
  ```
  $ code ~/.resilient/logs/app.log
  ```

* Scroll to bottom and see latest logs:

  ![screenshot](./screenshots/46.png)

---

## Step 17: *Start Docker*

* Open **Terminal**

* **Start** docker:
  ```
  $ sudo systemctl start docker
  ```

* Check **docker containers** are running:
  ```
  $ docker ps -a
  ```

  ![screenshot](./screenshots/35.png)

---

<!-- ## Step 17: *Ensure OpenLDAP is Configured and Running*
* Run:
  ```
  $ ldapwhoami -vvv -h localhost -p 389 -D "cn=Philip J. Fry,ou=people,dc=planetexpress,dc=com" -x -w "fry"
  ```

  ![screenshot](./screenshots/24.png) -->

## Step 18: *Install the LDAP Utilities Function*

> **NOTE:** This is very similar to install the previous `fn_utilities` function

* **Download** the package from [https://exchange.xforce.ibmcloud.com/hub/extension/72b8204066d3b290b68bae2eeb1942cd](https://exchange.xforce.ibmcloud.com/hub/extension/72b8204066d3b290b68bae2eeb1942cd)

* Open **Terminal**

* Change to **Downloads** directory:
  ```
  $ cd ~/Downloads
  ```
* **Install** FN LDAP Utilities using pip:
  ```
  $ pip install fn_ldap_utilities-x.x.x.zip
  ```

* Import **configurations**:
  ```
  $ resilient-circuits config -u
  ```

* Import **customizations**:
  ```
  $ resilient-circuits customize -y -l fn-ldap-utilities
  ```

* **Run** `resilient-circuits`:
  ```
  $ resilient-circuits run
  ```

---

## Step 19: *Configure LDAP Utilities*

* Open `app.config` in **VS Code**:
  ```
  $ code ~/.resilient/app.config
  ```

* Update the settings under `[fn_ldap_utilities]`:
  ```
  [fn_ldap_utilities]
  ldap_server=127.0.0.1 
  ldap_port=389 
  ldap_use_ssl=False 
  ldap_auth=SIMPLE 
  ldap_user_dn=cn=admin,dc=planetexpress,dc=com 
  ldap_password=GoodNewsEveryone 
  ldap_is_active_directory=False 
  ldap_connect_timeout=10
  ```

  ![screenshot](./screenshots/36.png)

 * Login to the Resilient UI

 * Update **Function Inputs** in LDAP Search Function **Pre-Process**:
    * Customization Settings > Workflows > **Example: LDAP Utilities: Search**
    * Click Search Function
    * Edit ldap_search_base in the **Pre-Processing Script**
      ```python
      inputs.ldap_search_base = "dc=planetexpress,dc=com"
      inputs.ldap_search_filter = "(&(mail=%ldap_param%))"
      inputs.ldap_search_attributes = "uid,cn,sn,mail,telephoneNumber"
      inputs.ldap_search_param =  artifact.value
      ```

  ![screenshot](./screenshots/37.png)

* Close the editor. Scroll up and click **Save & Close**:

---

## Step 20: *Run LDAP Search Function*

* Go to your **Incident**

* Add an **Artifact** to that Incident
  * Type: `Email Sender`
  * Value: `fry@planetexpress.com`

* Click the **Take Action Button** and run the **Example: LDAP Utilities: Search**

  ![screenshot](./screenshots/38.png)

* Check your **Terminal**

  ![screenshot](./screenshots/39.png)

---

## Step 21: *View LDAP Search Results in a Resilient Data Table*

* Go to **Customization Settings > Layouts > Manage Tabs**

* Add a **New Tab:**
  * Incident Tabs > Manage Tabs > + Add Tab

  ![screenshot](./screenshots/40.png)

  * Tab Text: **Users & Systems**
  * Tab Visible: **Yes**
  * Click **Add**

  ![screenshot](./screenshots/41.png)

* **Drag** the **LDAP Query results** Data Table into the Users & Systems Tab:
  
  ![screenshot](./screenshots/42.png)

* **Save** the layout and go back to your incident

* Go to the new **Users & Systems** tab, you will see the LDAP lookup result:

  ![screenshot](./screenshots/43.png)

* **Add a new Email Sender Artifact** of `professor@planetexpress.com`

* Run the LDAP Search Function again

* Check the result

  ![screenshot](./screenshots/44.png)

* View **DEBUG** messages

  * Go to **Actions > Action Status**

  * Click **Pending, Error** dropdown and highlight **Select all**

  * Click the Workflow to see DEBUG messages:
  
    ![screenshot](./screenshots/45.png)

---

## Step 22: *Create RDAP Message Destination*

* Go to **Customization Settings > Message Destination > Add Message Destination**

* Create the **Message Destination**:
  * Type: **Queue**
  * Name: **fn_who_is_rdap**
  * Programmatic Name: **fn_who_is_rdap**
  * Except Ack: **Yes**
  * Users/API Keys: **Dev App Host**
  * Click **Create**
    ![screenshot](./screenshots/47.png)


---

## Step 22: *Create RDAP Function*

* Go to **Customization Settings > Functions > New Function**

* Create the **Function**:
  * Name: **RDAP Query**
  * Programmatic Name: **rdap_query**
  * Message Destination: **fn_who_is_rdap**

* Click **Add Field** to add the following **Inputs**:

* **Input 1:**
  * Type: **Text**
  * API Access Name: **rdap_query**
    ![screenshot](./screenshots/48.png)

* **Input 2:**
  * Type: **Number**
  * API Access Name: **rdap_depth**
    ![screenshot](./screenshots/49.png)

* Scroll down and drag the **Fields** into the **Inputs:**

  ![screenshot](./screenshots/50.png)

* Click **Save & Close**

---

## Step 23: *Create RDAP Workflow*

* Go to **Customization Settings > Workflows > New Workflow**

* Create the **Workflow**:
  * Name: **RDAP Query**
  * Programmatic Name: **rdap_query**
  * Object Type: **Artifact**

* Scroll down to the Workflow Editor and add an **End Node**

  ![screenshot](./screenshots/23.png)
  ![screenshot](./screenshots/24.png)

* Connect the **Start Node** and **End Node** with a **Connector**

  ![screenshot](./screenshots/25.png)

* Add a **Function** on the **Connector**

  ![screenshot](./screenshots/26.png)

* Place our **RDAP Query Function** on the **Connector**

  ![screenshot](./screenshots/51.png)

* Open the Function's **pre-processing** script and add the following:
  ```python
  inputs.rdap_query = artifact.value
  inputs.rdap_depth = 0
  ```

  ![screenshot](./screenshots/52.png)

* Open the Function's **post-processing** script and paste the following:
  ```python
  # Helper to append to Artifact Description
  try:
    des = artifact.description.content
  except Exception:
    des = u"RDAP Lookup Results:\n"

  if results.get("success"):
    
    results_contents = results.get("content", {})
    d = results_contents.get("objects", {})
    
    for k in d:
      o = d[k]
      entity_name = o.get("contact", {}).get("name")
      entity_address = o.get("contact", {}).get("address")[0].get("value")
      entity = u"Name: {0}\nAddress: {1}".format(entity_name, entity_address)
      des = u"{0}\n{1}".format(des, entity)
      
    artifact.description = des

    note_text = u"""RDAP Lookup ran on Artifact: <b>{0}</b>
                    <br><b>Name:</b> {1}
                    <br><b>Address:</b> {2}""".format(artifact.value, entity_name, entity_address)
    
    incident.addNote(helper.createRichText(note_text))
  ```

  ![screenshot](./screenshots/53.png)

* **Save and Close** the Workflow

---

## Step 24: *Create RDAP Rule*

* Go to **Customization Settings > Rules > New Rule > Menu Item**

  ![screenshot](./screenshots/54.png)

* Create the **Rule**:
  * Display Name: **RDAP Query**
  * Object Type: **Artifact**
  * Workflow: **RDAP Query**

  ![screenshot](./screenshots/55.png)

* **Save and Close** the Rule

---

## Step 25: *Update app.config to use Apps User (temporary)*

* Open `app.config` in **VS Code**:
  ```
  $ code ~/.resilient/app.config
  ```

* Comment out `api_key_id` and `api_key_secret` by pre-pending a `#` symbol

* Add `email` and `password` attribute like below:

  ![screenshot](./screenshots/56.png)

* **Save** by pressing **CTRL+S**

* In the Resilient UI, add **Orchestration Engine User** to ALL Message Destinations:

  ![screenshot](./screenshots/58.png)

---

## Step 26: *Generate boilerplate Python Code*

* Open **Terminal**, make a new `my_dev` directory and change into it:
  ```
  $ mkdir ~/my_dev
  $ cd ~/my_dev
  ```

* Run `resilient-circuits codegen`:
  ```
  $ resilient-circuits codegen -p fn_who_is_rdap -m "fn_who_is_rdap" --rule "RDAP Query"
  ```

* Change into created **Directory**:
  ```
  $ cd /fn_who_is_rdap
  ```

* Install in **development mode**:
  ```
  $ python setup.py develop
  ```

* **Confirm** development installation:
  ```
  $ pip list
  ```

  ![screenshot](./screenshots/57.png)


* **Run** resilient-circuits:
  ```
  $ resilient-circuits run
  ```

---

## Step 27: *Test boilerplate code is setup*

* In the Resilient UI Create an **Incident**
  * Name: `RDAP Demo`

* Add an **Artifact** to that Incident
  * Type: `IP Address`
  * Value: `129.42.34.0`

  ![screenshot](./screenshots/59.png)

* **Run** your new Rule:

  ![screenshot](./screenshots/60.png)

* Open the **Terminal** and check the output of `resilient-circuits`:

  ![screenshot](./screenshots/61.png)

* Kill `resilient-circuits` with:
  ```
  $ CTRL + c
  ```

---

## Step 28: *Install ipwhois*

* Open **Terminal**

* Install `ipwhois` dependency
  ```
  $ pip install ipwhois
  ```

  > **NOTE:** hosted on https://pypi.org/project/ipwhois/

---

## Step 29: *Install resilient-lib*

* Open **Terminal**

* Install `resilient-lib` dependency
  ```
  $ pip install resilient-lib
  ```

  > **Note:** hosted on https://pypi.org/project/resilient-lib/

---

## Step 30: *Setup for Building RDAP Query Code*
* Open **VS Code**

* Open the `my_dev` directory

* You will see the folder structure of a `package`

* Open the function under the `components` directory:

  ![screenshot](./screenshots/62.png)

* We are going to edit this file to **build the logic** of or own RDAP Function

* Docs for the IPWhois Library we use are found here: https://ipwhois.readthedocs.io/en/latest/README.html#api

---

## Step 31: *Build RDAP Query Code*

1. **Line 7**: Import resilient-lib:
   ```python
   from resilient_lib import ResultPayload, validate_fields
   ```

2. **Line 8**: Import IPWhois:
   ```python
   from ipwhois import IPWhois
   ```

3. **Line 9**: Import JSON:
   ```python
   import json
   ```

4. **Line ~39**: Uncomment StatusMessages:
    ```python
    # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
    yield StatusMessage("starting...")
    yield StatusMessage("done...")
    ```
5. **Inbetween 'starting...' and 'done...'**: Validate Inputs:
    ```python
    yield StatusMessage("starting...")

    validate_fields(["rdap_depth", "rdap_query"], kwargs)
    
    yield StatusMessage("done...")
    ```
6. **After above**: Instantiate Results Payload:
    ```python
    yield StatusMessage("starting...")

    validate_fields(["rdap_depth", "rdap_query"], kwargs)
    rp = ResultPayload("fn_who_is_rdap", **kwargs)

    yield StatusMessage("done...")
    ```
7. **After above**: Instantiate IPWhois + Get RDAP response:
    ```python
    yield StatusMessage("starting...")

    validate_fields(["rdap_depth", "rdap_query"], kwargs)

    rp = ResultPayload("fn_who_is_rdap", **kwargs)

    ip_whois = IPWhois(rdap_query)

    response = ip_whois.lookup_rdap(depth=rdap_depth)
    log.info("RDAP Response: %s", json.dumps(response, indent=4))

    yield StatusMessage("done...")
    ```
8. **After above**: Build results
    ```python
    yield StatusMessage("starting...")

    validate_fields(["rdap_depth", "rdap_query"], kwargs)

    rp = ResultPayload("fn_who_is_rdap", **kwargs)

    ip_whois = IPWhois(rdap_query)

    response = ip_whois.lookup_rdap(depth=rdap_depth)
    log.info("RDAP Response: %s", json.dumps(response, indent=4))

    results = rp.done(success=True, content=response)
    yield StatusMessage("done...")
    ```
9. **Line ~50**: **Remove** default `results` object
    ```python
    results = {
        "value": "xyz"
    }
    ```
10. **Save** with `CTRL+S`

11. Full Function code:
  ```python
  # -*- coding: utf-8 -*-
  # pragma pylint: disable=unused-argument, no-self-use
  """Function implementation"""

  import logging
  from resilient_circuits import ResilientComponent, function, handler, StatusMessage, FunctionResult, FunctionError
  from resilient_lib import ResultPayload, validate_fields
  from ipwhois import IPWhois
  import json

  class FunctionComponent(ResilientComponent):
      """Component that implements Resilient function 'rdap_query"""

      def __init__(self, opts):
          """constructor provides access to the configuration options"""
          super(FunctionComponent, self).__init__(opts)
          self.options = opts.get("fn_who_is_rdap", {})

      @handler("reload")
      def _reload(self, event, opts):
          """Configuration options have changed, save new values"""
          self.options = opts.get("fn_who_is_rdap", {})

      @function("rdap_query")
      def _rdap_query_function(self, event, *args, **kwargs):
          """Function: Our custom function"""
          try:
              # Get the wf_instance_id of the workflow this Function was called in
              wf_instance_id = event.message["workflow_instance"]["workflow_instance_id"]

              # Get the function parameters:
              rdap_query = kwargs.get("rdap_query")  # text
              rdap_depth = kwargs.get("rdap_depth")  # number

              log = logging.getLogger(__name__)
              log.info("rdap_query: %s", rdap_query)
              log.info("rdap_depth: %s", rdap_depth)

              # PUT YOUR FUNCTION IMPLEMENTATION CODE HERE
              yield StatusMessage("starting...")

              validate_fields(["rdap_depth", "rdap_query"], kwargs)

              rp = ResultPayload("fn_who_is_rdap", **kwargs)

              ip_whois = IPWhois(rdap_query)

              response = ip_whois.lookup_rdap(depth=rdap_depth)
              log.info("RDAP Response: %s", json.dumps(response, indent=4))

              results = rp.done(success=True, content=response)
              yield StatusMessage("done...")

              # Produce a FunctionResult with the results
              yield FunctionResult(results)
          except Exception:
              yield FunctionError()
  ```

---

## Step 32: *Run RDAP Query*

* Open the **Terminal**

* Run `resilient-circuits`:
  ```
  $ resilient-circuits run
  ```

* Open the **RDAP Demo** Incident

* Run the **RDAP Query Rule** on the `129.42.34.0` Artifact

* Check `resilient-circuits` logs

* Check that Note is added and **Artifact Description** is updated

* Done ;)

---

## Step 33: *Package RDAP*
* Open the `setup.py` file

* Fill out your **details** and add **dependencies** used:
  ```python
    name='fn_who_is_rdap',
    version='1.0.0',
    license='MIT',
    author='John Smith',
    author_email='john@example.com',
    url='Example Inc.',
    description="Resilient Circuits Components for 'fn_who_is_rdap'",
    long_description="Resilient Circuits Components for 'fn_who_is_rdap'",
    install_requires=[
        'resilient_circuits>=30.0.0',
        'resilient-lib>=34.0.0',
        'ipwhois>=1.1.0'
    ]
  ```

* Change to root of package:
  ```
  $ cd fn_who_is_rdap
  ```

* **Package** the RDAP Query:
  ```
  $ python setup.py sdist --formats=zip
  ```

* Open `/dist` directory

* The `.zip` is your RDAP Query Package

---
<!-- 
# Quiz
1. **What is the default location of file App Host configs are stored?**

    **A:** ~/.resilient/config

    **B:** ~/.resilient/app.config

    **C:** ~/app.config

2. **Where would you view Debug messages in the UI?**

    **A:** Incident Name > Actions > Action Status

    **B:** Customization Settings > Workflows > Workflow Name

    **C:** Incident Name > Notes

3. **In the development environment, how would you open and view resilient-circuits logs?**

    **A:** code /logs/resilient-circuits.log

    **B:** code tmp/logs/resilient-circuits.log

    **C:** code ~/.resilient/logs/app.log

--- -->

![screenshot](./screenshots/ending.png)

---