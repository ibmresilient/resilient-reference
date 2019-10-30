
# Tech Workshop Guide

**Craig Roberts, Solutions Architect, IBM Resilient**

> All steps in this guide should be run from the VMware Terminal unless otherwise noted with the resadmin user. 

> Do not use sudo unless explicitly stated, this can cause problems with your python environment.
---

## Step 0: *Login to the Virtual Machine*

Start the virtual machine, it will take a while to boot up. You will be presented with the Redhat Login Screen. Login as `resadmin` with the password shared by your course leader.

  ![screenshot](./screenshots/newBuild0.png)

Open the Terminal, we will be using this as though it was the Resilient CLI. Click on Applications then Terminal.

---
## Step 1: *Check which Python Version is installed*

+ Check Python version in the terminal:
  ```
  $ python --version
  ```
* Output should be:
  ```
  Python 3.6.8
  ```
---
## Step 2: *Make sure Resilient License is Valid*

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
* Optionally you can **Restart** the Resilient Service:
  ```
  $ sudo service resilient-messaging restart
  ```
  >**NOTE:** with the release of v32 the resilient-messaging service also restarts the resilient service. It is important to use this to ensure the resilient-messaging and resilient services are in sync.
---
## Step 3: *Create User Accounts*
* Open **Terminal**
* Create a user:
    ```
    $ sudo resutil newuser -createorg -org "Dev" -email "resadmin@example.com" -first "Res" -last "Admin" -password "ResDemo123"
    ```
    >**NOTE:** For production you don't have to use the -password flag, if missing resilient will prompt for user input

---

## Step 4: *Test User Interface*

---
* Open the Firefox browser from the applications menu and navigate to:

>[https://127.0.0.1](https://127.0.0.1)

* This will show you the resilient interface (you might have to accept the self signed cert). Use the account you just created to check that you can login.

---

## Step 5: *Install Resilient Circuits*

---

> Note; Ensure you are not the root user or using sudo for commands which do now have it.
* Back in your Terminal, Install resilient-circuits using **pip**:
  ```
  $ pip install resilient-circuits
  ```
  > **NOTE:** you will need a connection to the Internet to install.

  ![screenshot](./screenshots/2.png)
---
## Step 6: *Configure Resilient Circuits*
#### *Resilient Circuits configurations are maintained in the app.config file*
* Open terminal
* Auto generate the **app.config file**:
  ```
  $ resilient-circuits config -c
  ```
* This creates `/home/resadmin/.resilient/app.config`
* Open this file in **VS Code:**
  ```
  $ code /home/resadmin/.resilient/app.config
  ```
* Change the various values with these configuration settings:
  ```
  host=localhost
  port=443
  org=Dev
  logdir=/home/resadmin/.resilient
  cafile=false 
  ```
* For cafile make sure you have removed the `#` at the start of the line too
* **Save** by pressing **CTRL+S**
* We now need to get an API Key - Open Resilient in your browser again (maybe set it to the firefox homepage), login with your credentials we created in step 3.
* Go to the username at the top right and click Administation Settings.

  ![screenshot](./screenshots/newBuild1.png)

* Click API Keys on the Users tab you are on, then create API Key on the right.
* Click All Permissions for now and name your key

  ![screenshot](./screenshots/newBuild2.png)

* Scroll down and click Create, a new window will pop up, click Copy to Clipboard. 

  ![screenshot](./screenshots/newBuild3.png)

* Reopen the `app.config` file using Visual Studio Code and paste the values. Then put the `Key ID` value against the `api_key_id` and `Key Secret` as the value for `api_key_secret`

> Note; sometimes the api_key_id can paste with a slash at the end, this should be removed. 

---
## Step 6: *Run Resilient Circuits*
* Open **Terminal**
* Run resilient-circuits: 
  ```
  $ resilient-circuits run
  ```
* You should get this output if `resilient-circuits` is running successfully:
  ![screenshot](./screenshots/6.png)
---
## Step 7: *Install FN Utilities*
* **Stop** `resilient-circuits` by pressing **CTRL+C**
* **Download** the package from [https://exchange.xforce.ibmcloud.com/hub/extension/2b6699ac8a3976b67dfbddee26dbe3a5](https://exchange.xforce.ibmcloud.com/hub/extension/2b6699ac8a3976b67dfbddee26dbe3a5)
  > *You may need to register for an **X-Force Exchange Account***
* Open **Terminal**
* Change to your **Downloads** folder:
  ```
  $ cd /home/resadmin/Downloads/
  ```
  > **NOTE:** you will need a connection to the Internet to download and install.
* **Unzip** the package:
  ```
  $ unzip fn_utilities-x.x.x.zip
  ```
* **Install** FN Utilities using pip:
  ```
  $ pip install fn_utilities-x.x.x.tar.gz
  ```
  ![screenshot](./screenshots/7.png)
* Import **configurations**:
  ```
  $ resilient-circuits config -u
  ```
  ![screenshot](./screenshots/8.png)
* Import **customizations**:
  ```
  $ resilient-circuits customize -l fn-utilities
  ```
  ![screenshot](./screenshots/9.png)
* **Start** Resilient Circuits:
  ```
  $ resilient-circuits run
  ```
  ![screenshot](./screenshots/10.png)
---
## Step 8: *Testing FN Utilities*
* Go to **Resilient UI**
  * Go to your Desktop and open **FireFox**
  * Go to: `https://127.0.0.1`
* Login:
  * Email: `resadmin@example.com`
  * Password: `ResDemo123`
* Create an **Incident**
  * Name: `Integrations Demo`
* Add an **Artifact** to that Incident
  * Type: `DNS Name`
  * Value: `resilientsystems.com`
* Click the **Take Action Button** and run the **Example: Shell Command** Workflow on that Artifact:
  ![screenshot](./screenshots/12.png)
* Check your **terminal:**
  <img src="./screenshots/13.png" alt="screenshot" width="100%"/>
* See the results in the **Notes Tab** of your Resilient Incident:
  ![screenshot](./screenshots/14.png)
* Can also see **DEBUG Information** in the **Action Status** which is located just under the navigation bar on the right-hand side:
  <img src="./screenshots/48.png" alt="screenshot" width="30%"/>
  <img src="./screenshots/15.png" alt="screenshot" width="69%"/>
  
---
## Step 9: *Create new Custom Workflow that uses our Shell Command Function*
* In the Resilient UI, go to **Customization Settings,** under your username on the right-hand side of the navigation bar
* Click the **Workflows Tab**
* **Create** a new Workflow
  * Name: **nslookup**
  * Object Type: **Artifact**
  ![screenshot](./screenshots/16.png)
* Add an **End Event** *(the dark black circle icon)* to the canvas
* Add the function **Utilities: Shell Command** to the Workflow Canvas by clicking on the function icon and selecting **Utilities: Shell Command** from the dropdown menu
* Edit the **Pre-Process Script:**
  ```
  inputs.shell_command = "nslookup"
  inputs.shell_remote = False
  inputs.shell_param1 = artifact.value
  ```
  ![screenshot](./screenshots/17.png)
* Edit the **Post-Process Script:**
  ```
  note_text = u"Command succeeded: {}\n{}".format(results.commandline, results.stdout)

  incident.addNote(helper.createPlainText(note_text))
  ```
  ![screenshot](./screenshots/18.png)
* Close the **Function Editor** and drag/scroll the function into view on the canvas
* Using the **connectors** *(the black arrow icon)*, join the start event to the function and then the function to the end event
  ![screenshot](./screenshots/54.png)

* Click **Save & Close**
---
## Step 10: *Create new Custom Rule that runs our Workflow*
* Click the **Rules Tab**
* Create a new **Menu Item Rule:**
  * Display Name: **Nslookup**
  * Object Type: **Artifact**
  * Workflows: **nslookup**
  ![screenshot](./screenshots/20.png)
* Click **Save & Close**
---
## Step 11: *Run our Custom Workflow*
* Go to your **Incident**
* Click the **Artifacts Tab**
* Run `nslookup` workflow on the `resilientsystems.com` Artifact
  ![screenshot](./screenshots/21.png)
* See the **logs in the terminal** and results in the **Notes Tab**
  ![screenshot](./screenshots/22.png)
---
## Step 12: *Start Docker*
* Open **Terminal**
* **Stop** `resilient-circuits` by pressing **CTRL+C**
* **Start** docker:
  ```
  $ sudo systemctl start docker
  ```
* Check **docker** is running:
  ```
  $ docker ps -a
  ```
  ![screenshot](./screenshots/23.png)
---
## Step 13: *Ensure OpenLDAP is Configured and Running*
* Run:
  ```
  $ ldapwhoami -vvv -h localhost -p 389 -D "cn=Philip J. Fry,ou=people,dc=planetexpress,dc=com" -x -w "fry"
  ```
  ![screenshot](./screenshots/24.png)
---
## Step 14: *Install the LDAP Utilities Function*
* This is very similar to install the previous `fn_utilities` function
* **Download** the package from [https://exchange.xforce.ibmcloud.com/hub/extension/72b8204066d3b290b68bae2eeb1942cd](https://exchange.xforce.ibmcloud.com/hub/extension/72b8204066d3b290b68bae2eeb1942cd)
* Open **Terminal**
* Change to your **Downloads** folder:
  ```
  $ cd /home/resadmin/Downloads/
  ```
  > **NOTE:** you will need a connection to the Internet to download and install. 
* **Unzip** the package:
  ```
  $ unzip fn_ldap_utilities-x.x.x.zip
  ```
* **Install** FN LDAP Utilities using pip:
  ```
  $ pip install fn_ldap_utilities-x.x.x.tar.gz
  ```
* Import **configurations**:
  ```
  $ resilient-circuits config -u
  ```
* Import **customizations**:
  ```
  $ resilient-circuits customize -l fn-ldap-utilities
  ```

  ![screenshot](./screenshots/25.png)
* **Start** resilient-circuits:
  ```
  $ resilient-circuits run
  ```
---
## Step 15: *Configure LDAP Utilities*
* Open `/home/resadmin/.resilient/app.config` in **VS Code**:
  ```
  $ code /home/resadmin/.resilient/app.config
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
  ![screenshot](./screenshots/26.png)
 * Update **Search Base** in LDAP Search Function:
      * Customization Settings > Workflows > **Example: LDAP Utilities: Search**
      * Click Search Function
      * Edit ldap_search_base in the **Pre-Processing Script**
        ```python
        inputs.ldap_search_base = "dc=planetexpress,dc=com"
        inputs.ldap_search_filter = "(&(mail=%ldap_param%))"
        inputs.ldap_search_param =  artifact.value
        ```
        ![screenshot](./screenshots/27.png)
* Click **Save & Close**
---
## Step 16: *Run LDAP Search Function*
* Go to your Incident
* Add an **Artifact** to that Incident
  * Type: `Email Sender`
  * Value: `fry@planetexpress.com`
* Click the **Take Action Button** and run the **Example: LDAP Utilities: Search**
  ![screenshot](./screenshots/28.png)
* Check your **Terminal Output**
  ![screenshot](./screenshots/56.png)
---
## Step 17: *View LDAP Search Results in Resilient UI*
* Go to your **Incident**
* Go to Customization Settings -> Layouts -> Manage Tabs
* Add a **New Tab:**
  * Incident Tabs > Manage Tabs > + Add Tab
  ![screenshot](./screenshots/57.png)
  * Tab Text: **Users & Systems**
  * Tab Visible: **Yes**
  ![screenshot](./screenshots/58.png)
  * Click **Add**
* Now **drag** the **LDAP Query results** Datatable into the Users & Systems Tab:
  ![screenshot](./screenshots/59.png)
* **Save** the layout and go back to your incident
* Go to the new **Users & Systems** tab, you will see the LDAP lookup result:
  ![screenshot](./screenshots/30.png)
* **Add a new Email Sender Artifact** of `professor@planetexpress.com`
* Run the LDAP Search Function again
* Check the result
![screenshot](./screenshots/31.png)
---
## Step 18: *Install & Configure the CMDB Function*
* **Stop** `resilient-circuits` by pressing **CTRL+C**
* **Download** the package from [https://exchange.xforce.ibmcloud.com/hub/extension/a51eb932122b9f71062e9ed8705f35f0](https://exchange.xforce.ibmcloud.com/hub/extension/a51eb932122b9f71062e9ed8705f35f0)
* Open **Terminal**
* Change to your **Downloads** folder:
  ```
  $ cd /home/resadmin/Downloads/
  ```
  > **NOTE:** you will need a connection to the Internet to download and install. 
* **Unzip** the package:
  ```
  $ unzip fn_odbc_query-x.x.x.zip
  ```
* **Install** FN ODBC using pip:
  ```
  $ pip install fn_odbc_query-x.x.x.tar.gz
  ```
* Import **configurations**:
  ```
  $ resilient-circuits config -u
  ```
* Import **customizations**:
  ```
  $ resilient-circuits customize -l fn-odbc-query
  ```

* Open the `app.config` file in **VS Code**
* **Replace** the `sql_connection_string` value with below:
  ```
  [fn_odbc_query]
  sql_connection_string=Driver={PostgreSQL};Server=localhost;Port=5555;Database=postgres;Uid=postgres;Pwd=resilient;
  ```
* **Test** that our PSQL Database is working:
  ```
  psql -h localhost -p 5555 -U postgres -W postgres -c "select * from systems;"
  ```
  ![screenshot](./screenshots/32.png)
* **Start** resilient-circuits:
  ```
  $ resilient-circuits run
  ```
  ![screenshot](./screenshots/60.png)
* In the Resilient UI, **add a new Workflow**
  * Name: `CMDB Query`
  * Object Type: `Artifact`
* Insert the `fn_odbc_query` function in to the canvas, add an **End Event** and connect the workflow all together using the **connectors**
* Click the function's **edit icon** and update the function input: `sql_query` with the following query:
  ```
  select name as sql_column_1, sys_ipaddr as sql_column_2, sys_type as sql_column_3, sys_os_version as sql_column_4, sys_owner_email as sql_column_5 from systems where name = ?
  ```
  ![screenshot](./screenshots/33.png)
* Update **Pre-Processing Script**:
  ```python
  inputs.sql_condition_value1 = artifact.value
  ```
* Update **Post-Processing Script**:
  ```python
  #  Globals

  # This list contains Resilient data table api field names.
  # Exclude fist two columns 'sql_artifact_value' and 'sql_timestamp' from this list.
  # Modify this list acording to your Resilent data table fields.
  RESILENT_DATATABLE_COLUMN_NAMES_LIST = [
    "sql_column_1",
    "sql_column_2",
    "sql_column_3",
    "sql_column_4",
    "sql_column_5"]
    
  # Processing
  from java.util import Date

  if results.entries is not None:
    for entry in results.entries:
      row = incident.addRow("sql_query_results_dt")
    
      row.sql_artifact_value = artifact.value
      row.sql_timestamp = Date()
    
      for item in RESILENT_DATATABLE_COLUMN_NAMES_LIST:
        if entry[item] is not None:
          try:
            row[item] = entry[item]
          except IndexError:
            row[item] = ""
  ```
* Click **Save & Close**
* Click the **Rules tab** and create a new **Menu Item Rule:**
  * Name: `CMDB Lookup`
  * Object Type: `Artifact`
  * Workflows: `CMDB Query`
  ![screenshot](./screenshots/34.png)
* Click **Save & Close**
* Go to your Incident and add a new **Artifact:**
  * Type: `System Name`
  * Value: `win1234`
  ![screenshot](./screenshots/35.png)
* **Take Action** with the CMDB Lookup Workflow on the Artifact and check the **terminal output**
* Once again you will need **add the SQL Results Table** to your *Users and Systems* Tab 
  ![screenshot](./screenshots/36.png)
---
## Step 19: *Creating your own function* 

Next we are going to create an "example" function, this will help us understand the mechanics of how resilient functions are built. The aim here is not the use of the function but more how we generate it to start our own integration. 

From our previous excercise we have fully configured environment to build functions: 

+ A Resilient server

+ Resilient Circuits installed and configured

+ Text Editor

We also now need to learn some terminology: 

+ Message Destination - The queue a function listens to and where results are sent back

+ Function Inputs - Fields that represent values to be passed to your function

+ Pre-Processing Script - Where one can format or programmatically set and manipulate function inputs prior to function execution.

+ Post-Processing Script - Where one can format or programmatically set and manipulate function output results

+ Function Component - The actual python code itself to be executed.

## Step 20: *Starting the function build*

+ Open your Resilient web interface and navigate to the "Customization Settings" 

![screenshot](./screenshots/101.png)

+ Go to the message destination tab and Add a new message destination
  ![screenshot](./screenshots/102.png)
  >**Note;** Always ensure the user is set correctly, this authorises the user in your circuits config to access this function queue. In this case you need to choose your Integration Server API Key User

+ Create the function in the Resilient UI under the `Functions` tab 
  ![screenshot](./screenshots/103.png)

+ Create a field on the function using the `Add Field` button
  ![screenshot](./screenshots/104.png)

+ Save the field and drag it onto the "inputs" area of the function, finally save and close the function. 

+ Switch to the terminal session for Resilient, and run
  ```
  $ resilient-circuits codegen -p fn_first_function -f first_function
  ```
  ![screenshot](./screenshots/107.png)

+ Now we need to open the file with VSCode, a code editor, run the following from the terminal again
  ```
  code /home/resadmin/fn_first_function
  ```
  ![screenshot](./screenshots/108.png)
  > **Note**; the path maybe different if you change the name of the function

+ Present in the folder is a number of different files, our key one is in `fn_first_function/components/fn`

+ The boilerplate code that gets generated is bare minimum but touches on all key aspects of development, What it does:
  + Grabs the field we defined in the UI and writes it as a log out (line 20)
  + There are examples of sending messages back to Resilient to keep the user posed on progress (line 23)
  + The results value is set as a key value paired dictionary object (line 26)
  + The function ends with us returning the results to a FunctionResults back to Resilient (line 31)

+ Lets add some capability to our boilerplate, we are going to use the "lorem" python module, so we need to declare/import it at the top of the file, below `import logging`
  ```
  import lorem
  ```

+ As we have imported a module, we need to install it to make sure we have it locally, go back to your terminal and install lorem 
  ```
  $ pip install lorem
  ```
  ![screenshot](./screenshots/109.png)

+ Lorem generates random passages of text so we are going to use this to make the function generate random text and send it back to Resilient.

+ Back in our code editor we need to start making some changes to the code. 
  + Check you added the import line 
  + Delete the commented/hashed block "PUT YOUR FUNCTION IMPLENTATION CODE HERE"
  + Add the `StatusMessage` lines these will send messages back to the Resilient UI so you know whats going on with the function. A bit like logging.
  + Add the line to generate a paragraph of random text (we are saving it as paragraph)
  + We now created a `data_result` who is the combination of the paragraph and our input field contents.
  + Finally change the results array (message) to send the `results_data` and a true/false for whether it has worked.
  + Save the file - it should like the one below
  ![screenshot](./screenshots/110.png)

+ You are all set and have written your first function. We now need to test, go to the workflows menu in Resilient Web UI (Customization -> Workflows)

+ Create a new workflow, naming to `Example: First Function` we use Example to denote workflows which are bundled with a function. So its best to stick this naming. 
  ![screenshot](./screenshots/111.png)

+ Add to the canvas the first function block 
  ![screenshot](./screenshots/113.png)

+ Enter your name in the input field, this is sent down to the code you wrote
  ![screenshot](./screenshots/114.png)

+ The system will return the results from our code and we use post processing to format it to somewhere in Resilient 
  ![screenshot](./screenshots/115.png)

+ Don't forgot to add the "end circle" on the workflow then save and close your work. 
  ![screenshot](./screenshots/116.png)

+ Save and close the workflow and go to the Rules tab, create a menu item rule as we want to run it on demand
  ![screenshot](./screenshots/117.png)

+ Name the rule and link it to the workflow you just created
  ![screenshot](./screenshots/118.png)

## Step 21: *Testing the function*

* We now need to install the function, cd into the fn_first_function directory then run
  `pip install -e .`

* Lets test our workflow and function code, go to the terminal and start `resilient-circuits` you are looking for the first function connections in the list. This means everything is ready. 
  ![screenshot](./screenshots/119.png)

* Go to any incident in Resilient and run your new rule
  ![screenshot](./screenshots/120.png)

* Check the action status to see the messages you coded
  ![screenshot](./screenshots/121.png)

* Now check the terminal to see the log of the function running.
  ![screenshot](./screenshots/122.png)

* Finally look at the description (you might have to reload the page) - you should have your name and then some lorem.
  ![screenshot](./screenshots/123.png)

* We are now going to package the app so you could promote to production or send to someone. 

* First, we reload the customizations, this allows us to bundle workflows and rules or datatables as part of our package.
