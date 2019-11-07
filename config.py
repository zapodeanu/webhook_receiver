#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Cisco DNA Center Client Information using the MAC Address

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Gabriel Zapodeanu TME, ENB"
__email__ = "gzapodea@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


# This file contains:
# the Webex Auth, Webex URL and Space name
# the Webhook username and password

WEBEX_TEAMS_URL = 'https://api.ciscospark.com/v1'
WEBEX_TEAMS_AUTH = 'Bearer ' + 'Put your token here'
WEBEX_TEAMS_ROOM = 'Webhooks Notifications'

WEBHOOK_URL = 'https://gabiz.pythonanywhere.com/webhook'
WEBHOOK_USERNAME = 'admin'
WEBHOOK_PASSWORD = 'password'

DNAC_URL = 'https://10.1.3.230'

SDWAN_URL = 'https://198.18.1.10:8443'  # do not change this
