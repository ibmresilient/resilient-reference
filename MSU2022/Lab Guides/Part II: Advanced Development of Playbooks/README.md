# IBM **Security** QRadar SOAR: Advanced Development of Playbooks

![screenshot](./screenshots/logo.png)

***Shane Curtin & Bo Bleckel, App Engineers, IBM **Security** QRadar SOAR***

---

## Contents
- [Step 0: *Sign up for SkyTap Account:*](#step-0-sign-up-for-skytap-account)
- [Step 1: *Login to Virtual Environment*](#step-1-login-to-virtual-environment)
- [Step 2: *Verify All Apps Are Installed and Deployed*](#step-2-verify-all-apps-are-installed-and-deployed)
- [Step 3: *Create Playbook to Parse Attachment*](#step-3-create-playbook-to-parse-attachment)
- [Step 4: *Create an Incident and Upload Malware Report*](#step-4-create-an-incident-and-upload-malware-report)
- [Step 5: *Create Playbook to check Devices that executed the Hash*](#step-5-create-playbook-to-check-devices-that-executed-the-hash)
- [Step 6: *Import the Data Table into the Artifacts Tab*](#step-6-import-the-data-table-into-the-artifacts-tab)
- [Step 7: *Add the LDAP Details Data Table to Artifacts tab*](#step-7-add-the-ldap-details-data-table-to-artifacts-tab)
- [Step 8: *Use Created Playbook to Lookup Users in LDAP*](#step-8-use-created-playbook-to-lookup-users-in-ldap)
- [Step 9: *Use Created Playbook to Disable Users in LDAP*](#step-9-use-created-playbook-to-disable-users-in-ldap)
- [Step 10: *Modify Playbook to Automatically Contain Device*](#step-10-modify-playbook-to-automatically-contain-device)
- [Step 11: *Create Playbook for New Report Incident Type*](#step-11-create-playbook-for-new-report-incident-type)
- [Step 12: *Modify the Parse Attachment Playbook to Close the Task*](#step-12-modify-the-parse-attachment-playbook-to-close-the-task)
- [Step 13: *Modify the Find Devices Playbook to also handle Tasks*](#step-13-modify-the-find-devices-playbook-to-also-handle-tasks)
- [Step 14: *Test New Report Incident*](#step-14-test-new-report-incident)
- [Step 15: *Use SDK to convert Parse Attachment Playbook to be Activated Automatically*](#step-15-use-sdk-to-convert-parse-attachment-playbook-to-be-activated-automatically)
- [Step 16: *End to End Test*](#step-16-end-to-end-test)

---

## Step 0: *Sign up for SkyTap Account:*

<!-- TODO! -->
* Go to https://ibm.biz/xxx

* Sign in with email and password provided by course provider

---

## Step 1: *Login to Virtual Environment*

  ![screenshot](./screenshots/1.png)

* Login as `resadmin` with the password shared by your course leader

* Open **FireFox** and log into **IBM Security QRadar SOAR**


---

## Step 2: *Verify All Apps Are Installed and Deployed*

* Open **Firefox** and login into the **IBM Security QRadar SOAR** instance
* Go to **Administrator Settings** > **Apps**
* Verify that **2** App Hosts are configured and running:
  * quay.io
  * local.registry
* Verify that the following Apps are installed and deployed:
  * `fn_ioc_parser_v2`
  * `fn_task_utils`
  * `fn_ldap_utilities`
  * `Demo EDR App`

<!-- TODO: add screenshot of this -->

---

## Step 3: *Create Playbook to Parse Attachment*

* Open the **Playbook Designer**:
  
  ![screenshot](./screenshots/3.png)

* Click **Create Playbook** and enter details:
  * Name: `Parse Attachment`
  * API Name: `parse_attachment`
  * Description: `Add IOCs found in an attachment as Artifacts of an Incident`
* Click **Create**
* Select the **Activation Details**:
  * Activation type: `Manual`
  * Object type: `Attachment`

    ![screenshot](./screenshots/4.png)

* On the left hand side of the Playbook Designer, click the **Functions** icon:

  ![screenshot](./screenshots/5.png)

* Expand the `fn_ioc_parser_v2` App and add the **IOC Parser v2** Function to the **canvas** by clicking the `+` icon:

  ![screenshot](./screenshots/6.png)

* Drag the **Function** underneath the **Activation Node** and connect them together:

  ![screenshot](./screenshots/7.png)

* Highlight the **Function Node** and click **Script** to modify the **Function's** pre-process script and it's inputs:

  ![screenshot](./screenshots/8.png)

* Use the type ahead prompts to **dynamically** set the **inputs** of the Function using data from the Incident:

  ```
  inputs.ioc_parser_v2_incident_id = incident.id
  inputs.ioc_parser_v2_attachment_id = attachment.id
  ```

  ![screenshot](./screenshots/9.png)

* Click **Save**
* Scroll down and set the **Function output** to `ioc_parser_results`:

  ![screenshot](./screenshots/10.png)

* On the left hand side of the **Playbook Designer**, open the **Scripts** panel:

  ![screenshot](./screenshots/11.png)

* Create a new **Local Script**. Click **Create Script**:

  ![screenshot](./screenshots/12.png)

* Ensure it is in the **Local** scope and give it a name: `Add IOCs as Artifacts`

  ![screenshot](./screenshots/13.png)

* Add the following code and hit **create**:

  ```python
  # Get the results
  r = playbook.functions.results.ioc_parser_results

  # Map App's IOC Type to SOAR Artifact Type
  ioc_map = {
      'uri': 'URI Path',
      'IP': 'IP Address',
      'md5': 'Malware MD5 Hash',
      'sha1': 'Malware SHA-1 Hash',
      'sha256': 'Malware SHA-256 Hash',
      'CVE': 'Threat CVE ID',
      'email': 'Email Sender',
      'filename': 'File Name',
      'file': 'File Name'
  }

  # Get the iocs
  iocs = r.get("iocs", [])

  # Get the attachment name
  attachment_file_name = r.get("attachment_file_name", "Unknown")

  # Define variables
  artifacts_added = []
  msg = ""

  # Loop the IOCs
  for ioc in iocs:
      artifact_description = f"This IOC occurred {ioc.get('count')} time(s) in the attachment: {attachment_file_name}"
      artifact_type = ioc_map.get(ioc.get("type"))
      artifact_value = ioc.get("value")

      incident.addArtifact(artifact_type, artifact_value, artifact_description)
      artifacts_added.append("{0}: {1}".format(artifact_type, artifact_value))

  formatted_artifacts = "\n".join(artifacts_added)

  # Add a Note
  if artifacts_added:
      msg = f"The following artifacts were added from attachment: {attachment_file_name}\n{formatted_artifacts}"
  else:
      msg = f"No IOCs were found in attachment: {attachment_file_name}"

  incident.addNote(msg)
  ```

* Add the Local Script to the **canvas**:

  ![screenshot](./screenshots/14.png)

* Drag it under the **Function Node** and connect them:

  ![screenshot](./screenshots/15.png)

* Open the **Decision Points** panel:

  ![screenshot](./screenshots/16.png)

* Add an **End Point** to the canvas and connect it to the **Local Script Node**:

  ![screenshot](./screenshots/17.png)

* **Save** then **Enable** the Playbook:

  ![screenshot](./screenshots/18.png)

---

## Step 4: *Create an Incident and Upload Malware Report*

* Click **Create Incident** and call it: `Test Parse Attachment`

  ![screenshot](./screenshots/19.png)

* Keep clicking **Next** and then **Create Incident**
* Go to the **Attachments** tab and click **Upload File**:

  ![screenshot](./screenshots/20.png)

* Upload the `25.03.22 - New Malware Warning.pdf` file which should be in the Home directory

  ![screenshot](./screenshots/23.png)

* Select the **Parse Attachment** Action for the attachment:

  ![screenshot](./screenshots/21.png)

* Monitor the **Newsfeed** of the Incident and observe Artifacts being added:

  ![screenshot](./screenshots/22.png)

* Switch to the **Notes** and **Artifacts** and observe that some were added

---

## Step 5: *Create Playbook to check Devices that executed the Hash*

* Open the **Playbook Designer**:
  
  ![screenshot](./screenshots/3.png)

* Click **Create Playbook** and enter details:
  * Name: `Find Devices Executed On`
  * API Name: `find_devices_executed_on`
  * Description: `Look up IOCs usage in our environment`
* Click **Create**
* Select the **Activation Details**:
  * Activation type: `Automatic`
  * Object type: `Artifact`
* Click **Create condition**:

  ![screenshot](./screenshots/24.png)

* **Add a condition** like the screenshot below and click **Done**:

  ![screenshot](./screenshots/25.png)

* Open the **Functions** panel and add the `EDR: Get Devices IOC Ran On` Function to the **canvas** and connect it to the **Activation Node**:

  ![screenshot](./screenshots/26.png)

* Highlight the **Function Node** and click **Script** to modify the **Function's** pre-process script and it's inputs

* Use the type ahead prompts to **dynamically** set the **inputs** of the Function using data from the Artifact:

  ```
  inputs.edr_ioc_type = artifact.type
  inputs.edr_ioc_value = artifact.value
  ```

  ![screenshot](./screenshots/27.png)

* Click **Save**
* Scroll down and set the **Function output** to `edr_devices_result`:

  ![screenshot](./screenshots/29.png)

* Add a **Local Script** to add the Function's results to a **Data Table**:

  ![screenshot](./screenshots/28.png)

* Add the following code and click **Create**:

  ```python
  # Name of Data Table
  DT_NAME = "edr_details"

  # Map result to column in Data Table
  RESULT_COL_MAP = {
    "id": "device_id",
    "hostname": "host",
    "ip": "ip_address",
    "user": "user",
    "status": "status"
  }

  # Get results
  devices_r = playbook.functions.results.edr_devices_result

  if devices_r.get("success"):

    # Get devices
    devices = devices_r.get("content", {}).get("devices", [])
    
    # Loop the devices
    for device in devices:

      # Create a new row in our App's Data Table
      row = incident.addRow(DT_NAME)

      # Add a cell's value to the DT according to our map
      for result_col, dt_col in RESULT_COL_MAP.items():
        row[dt_col] = device.get(result_col, "N/A")

  else:
    # Else, no devices found, add Note to Incident with reason
    incident.addNote(results.get("reason", "Unknown Error"))
  ```

* Add the **Script** to the **canvas**, **connect** it to the preceding Function, add an **End point**, **Save** then **Enable** the Playbook

  ![screenshot](./screenshots/30.png)

---

## Step 6: *Import the Data Table into the Artifacts Tab*

* Go to **Customization Settings**:

  ![screenshot](./screenshots/31.png)

* Expand the **Incident Tabs** and open **Artifacts**
* Find the `EDR Details` Data Table and drag it into the Artifacts Widget:

  ![screenshot](./screenshots/32.png)

* Click **Save**

* **Create** a new Incident, **upload** the Attachment and **parse** it
* Go to the **Artifacts** tab and observe that the `EDR Details` Data Table is now populated:

  ![screenshot](./screenshots/33.png)

---
## Step 7: *Add the LDAP Details Data Table to Artifacts tab*
* TODO

---

## Step 8: *Use Created Playbook to Lookup Users in LDAP*
* TODO

---

## Step 9: *Use Created Playbook to Disable Users in LDAP*
* TODO

---

## Step 10: *Modify Playbook to Automatically Contain Device*

* Open the **Playbook Designer**
* Open the `Find Devices Executed On` Playbook
* Add the `EDR: Update Status` Function to the **canvas** and insert it between the `EDR: Get Devices Ran On` Function and the **Local Script**:

  ![screenshot](./screenshots/39.png)

* Highlight the **Function Node** and click **Script** to modify the **Function's** pre-process script and it's inputs

* Using the results of the previous Function we are formatting the device ids into a **CSV list** and using that as an **input** to the Function:

  ```python
  # Get previous functions results
  r = playbook.functions.results.edr_devices_result

  # Get device ids as CSV list
  devices = r.get("content", {}).get("devices", [])
  device_ids = ",".join([d.get("id") for d in devices])

  inputs.edr_device_id = device_ids
  inputs.edr_new_status = "Contained"

  ```

* Scroll down and set the **Function output** to `edr_status_results`:

  ![screenshot](./screenshots/38.png)

* Highlight the connector between the 2 Functions and press **Backspace** to delete it:

  ![screenshot](./screenshots/40.png)

* Open the **Decision Points** panel and add a **Condition Point** to the **canvas**
* Rearrange your nodes so it looks something like the screenshot:

  ![screenshot](./screenshots/41.png)

* Highlight the **conditional node** and name it: `Were Devices Found`
* Click **Create condition**:

  ![screenshot](./screenshots/42.png)

* Call the condition `Devices Found`, open the **Script Builder** and paste in the following code:

  ```python
  # Get function's results
  r = playbook.functions.results.edr_devices_result

  success = r.get("success", False)

  if success:
    result = True
    
  else:
    result = False
  ```

  ![screenshot](./screenshots/35.png)

* Click **Done**
* Connect it to the **End point** and specify it as an **Else** path:

  ![screenshot](./screenshots/36.png)

* Connect another path of the **Condition** to the `EDR: Update Status` Function and click **Save**:

  ![screenshot](./screenshots/44.png)

* Connect the `EDR: Get Devices IOC Ran On` Function to the **Condition**:

  ![screenshot](./screenshots/45.png)

* Highlight the **Local Script** and modify it by clicking the **pencil** icon:

  ![screenshot](./screenshots/46.png)

* **Replace** the script with in the following code:

  ```python
  # Name of Data Table
  DT_NAME = "edr_details"

  # Map result to column in Data Table
  RESULT_COL_MAP = {
    "id": "device_id",
    "hostname": "host",
    "ip": "ip_address",
    "user": "user",
    "status": "status"
  }

  # Get results
  devices_r = playbook.functions.results.edr_devices_result
  status_r = playbook.functions.results.edr_status_results

  if devices_r.get("success"):

    # Get devices
    devices = devices_r.get("content", {}).get("devices", [])
    devices_statuses = status_r.get("content", {})

    # Loop the devices
    for device in devices:
    
      # Create a new row in our App's Data Table
      row = incident.addRow(DT_NAME)
      
      # Add a cells value to the DT according to our map
      for result_col, dt_col in RESULT_COL_MAP.items():
        row[dt_col] = device.get(result_col, "N/A")
        
        # Get updated device status
        if status_r.get("success"):
          d_status = device.get("status", "N/A")
          
          for s in devices_statuses:
            if s.get("device_id") == device.get("id"):
              d_status = s.get("status")
              break

          row["status"] = helper.createRichText(f"""<div style="color:#e60000">{d_status}</div>""")

  else:
    # Else, no devices found, add Note to Incident with reason
    incident.addNote(results.get("reason", "Unknown Error"))
  ```

* **Save** the Script and then **Save** the Playbook
* **Create** a new Incident, **upload** the Attachment and **parse** it
* Go to the **Artifacts** tab and observe that the `EDR Details` Data Table is now populated and the devices are **Contained**:

  ![screenshot](./screenshots/47.png)

---

## Step 11: *Create Playbook for New Report Incident Type*
* Open the **Playbook Designer**
* Click **Create Playbook** and enter details:
  * Name: `Handle New Report`
  * API Name: `handle_new_report`
  * Description: `Add required Tasks for 'New Report' incident type`
* Click **Create**
* Select the **Activation Details**:
  * Activation type: `Automatic`
  * Object type: `Incident`

    ![screenshot](./screenshots/48.png)

* Click **Create condition**
* **Add a condition** like the screenshot below and click **Done**:

  ![screenshot](./screenshots/49.png)

* Open **Tasks** from the side panel and add the task `Upload and Parse IOCs from Report` to the **canvas**, found under the **Engage** phase:

  ![screenshot](./screenshots/50.png)

* Add an **End point**, **Save** and **Enable** the Playbook

## Step 12: *Modify the Parse Attachment Playbook to Close the Task*
* Open the **Playbook Designer** and open the `Parse Attachment` Playbook
* Find the `Task Utils: Close Task` Function and add it to the **canvas**:

  ![screenshot](./screenshots/51.png)

* Highlight the **Function Node** and click **Script** to modify the **Function's** pre-process script and it's inputs

* Use the type ahead prompts to **dynamically** set the **inputs** of the Function using data from the Incident:

  ```
  inputs.incident_id = incident.id
  inputs.task_name = "Upload and Parse IOCs from Report"
  ```

  ![screenshot](./screenshots/52.png)

* **Save** the Script then scroll down and set the **Function output** to `close_task` and **Save** the Playbook

---

## Step 13: *Modify the Find Devices Playbook to also handle Tasks*
* Open the **Playbook Designer** and open the `Find Devices Executed On` Playbook
* Open **Tasks** from the side panel and add the task `EDR: Get Devices IOC Ran On` to the **canvas**, found under the **Detect/Analyze** phase:

  ![screenshot](./screenshots/53.png)

* Also find the `Task Utils: Close Task` Function and add it to the **canvas**

* Highlight the **Function Node** and click **Script** to modify the **Function's** pre-process script and it's inputs

* Use the type ahead prompts to **dynamically** set the **inputs** of the Function using data from the Incident:

  ```
  inputs.incident_id = incident.id
  inputs.task_name = "EDR: Get Devices IOC Ran On"
  ```

* **Save** the Script then scroll down and set the **Function output** to `close_ran_on_task`

* Rearrange the **Nodes** so you have two paths from the **Activation Node**:

  ![screenshot](./screenshots/54.png)

* Continue to connect the **Nodes** and add a **Wait point** like the screenshot below:
  
  ![screenshot](./screenshots/55.png)

* Don't forget to save the **Playbook** periodically!
* Update the setting of the **Conditional Node** to `Any true condition`:

  ![screenshot](./screenshots/56.png)

* Open **Tasks** from the side panel and add the task `EDR: Contain Devices` to the **canvas**, found under the **Engage** phase:

  ![screenshot](./screenshots/57.png)

* Also add a **Wait point** to the **canvas**:

  ![screenshot](./screenshots/58.png)

* Add another `Device Found` path from the **Conditional Node** to the `EDR: Contain Devices` Task, and then connect it up with the **Wait point** like in the screenshot below:

  ![screenshot](./screenshots/59.png)

* Find and add the `Task Utils: Close Task` Function, add it to the **canvas** after the **Local Script** and add the following pre-process script:

  ```
  inputs.incident_id = incident.id
  inputs.task_name = "EDR: Contain Devices"
  ```

* **Save** the Script then scroll down and set the **Function output** to `close_contain_devices_task`

* Save and ensure the **Playbook** is enabled

  ![screenshot](./screenshots/60.png)

---

## Step 14: *Test New Report Incident*
* Create a new **Incident**
* Add the **type**: `New Report`:

  ![screenshot](./screenshots/61.png)

* Click **Next** until prompted with the **Create incident** button and click it
* Open the **Attachments** tab, **upload** the report and **parse** it
* Switch back to the **Tasks** tab and observe the automation:

  ![screenshot](./screenshots/62.png)

* Switch over to **Artifacts** and notice IOCs were found and devices Contained as expected:
  
  ![screenshot](./screenshots/63.png)

---

## Step 15: *Use SDK to convert Parse Attachment Playbook to be Activated Automatically*

* Open the **Playbook Designer** and open the `Parse Attachment` Playbook
* Click the **View details** icon and scroll down and make note of the API Name of the Playbook:

  ![screenshot](./screenshots/64.png)

* Open the **Terminal**
* Display information on the `resilient-sdk clone` command:
  
  ```
  $ resilient-sdk clone -h
  ```

* Use the `resilient-sdk` to clone the `Parse Attachment` Playbook and change it into a **Draft State**, allowing us to modify its **Activation Type**:

  ```
  $ resilient-sdk clone --playbook "parse_attachment" "auto_parse_attachment"  --draft-playbook
  ```

* Once the command has executed successfully, go back to the **Playbook Designer** and open the new `auto_parse_attachment` Playbook
* Notice you can now change its **Activation details**:

  ![screenshot](./screenshots/65.png)

* Change the **Activation details** to automatic and add a simple condition where the Attachment is created:

  ![screenshot](./screenshots/66.png)

* Click the **View details** icon and re format the Display Name of the Playbook:

  ![screenshot](./screenshots/67.png)

* **Save** and **enable** the Playbook
* We can now **disable** the older Playbook if we like:
  ![screenshot](./screenshots/68.png)

---

## Step 16: *End to End Test*
* Create a new **Incident**
* Add the **type**: `New Report`:

  ![screenshot](./screenshots/61.png)

* Open the **Attachments** tab and **upload** the report
* Switch back to the **Tasks** tab and observe the automation:

  ![screenshot](./screenshots/62.png)

* Switch over to **Artifacts** and notice IOCs were found and devices Contained as expected:
  
  ![screenshot](./screenshots/63.png)

---