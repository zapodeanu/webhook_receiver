# Cisco DNA Center Webhook Receiver


This Python script will run on PythonAnywhere, or a Linux container.

 - It will receive Cisco DNA Center and Cisco SD-WAN webhooks and save them locally to files for reporting
 - The application will create a new Webex Teams message to notify the NOC about the new issue

**Cisco Products & Services:**

- Cisco DNA Center, Cisco SD-WAN, Cisco Webex Teams

**Other Products & Services:**

- None
 
**Tools & Frameworks:**

- Python environment running in PythonAnywhere, local, or VM/container

**Usage**

- Update the "config.py" file with your environment
- Test your application using the "test_webhook_receiver.py"
- Configure a new Cisco DNA Center webhook, and/or Cisco SD-WAN webhook
- Create a new event to which you subscribed and verify the notifications

**License**

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).