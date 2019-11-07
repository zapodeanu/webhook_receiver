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


import requests
import urllib3
from flask import Flask, request, abort
import sys
import json
import datetime
import os
import time
from flask_basicauth import BasicAuth

from urllib3.exceptions import InsecureRequestWarning  # for insecure https warnings

os.environ['TZ'] = 'America/Los_Angeles'  # define the timezone for PST
time.tzset()  # adjust the timezone, more info https://help.pythonanywhere.com/pages/SettingTheTimezone/

urllib3.disable_warnings(InsecureRequestWarning)  # disable insecure https warnings

from config import WEBEX_TEAMS_AUTH, WEBEX_TEAMS_URL, WEBEX_TEAMS_ROOM
from config import WEBHOOK_USERNAME, WEBHOOK_PASSWORD, WEBHOOK_URL
from config import DNAC_URL, SDWAN_URL

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = WEBHOOK_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = WEBHOOK_PASSWORD
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


@app.route('/')  # create a decorator for testing the Flask framework
@basic_auth.required
def index():
    return '<h1>Flask Receiver App is Up!</h1>', 200


@app.route('/dashboard')  # create a decorator for the dashboard
def dashboard():
    return '<h1>Dashboard To DO!</h1>', 200


@app.route('/webhook', methods=['POST'])  # create a decorator for /webhook, method POST
def webhook():
    if request.method == 'POST':
        print('Webhook Received')
        request_json = request.json

        # print the received notification
        print('Payload: ')
        pprint(request_json)

        # save as a file, create new file if not existing, append to existing file, full details of each notification
        with open('all_webhooks_detailed.log', 'a') as filehandle:
            filehandle.write('%s\n' % json.dumps(request_json))
        try:
            if 'NETWORK-' in request_json['eventId']:  # this will select the Cisco DNA Center notifications
                dnac_notification = request_json

                # save all info to variables, prepare to save to file
                severity = str(dnac_notification['severity'])
                category = dnac_notification['category']
                timestamp = str(datetime.datetime.fromtimestamp(int(dnac_notification['timestamp']/1000)).strftime('%Y-%m-%d %H:%M:%S'))
                issue_name = dnac_notification['details']['Assurance Issue Name']
                issue_description = dnac_notification['details']['Assurance Issue Details']
                issue_status = dnac_notification['details']['Assurance Issue Status']
                url = DNAC_URL + '/dna/assurance/issueDetails?issueId=' + dnac_notification['instanceId']

                # create the summary DNAC log
                new_info = {'severity': severity, 'category': category, 'timestamp': dnac_notification['timestamp']}
                new_info.update({'Assurance Issue Name': issue_name, 'Assurance Issue Details': issue_description})
                new_info.update({'Assurance Issue Status': issue_status, 'Assurance Issue URL': url})

                # append, or create, the dnac_webhooks.log - Cisco DNA C summary logs
                with open('dnac_webhooks.log', 'a') as filehandle:
                    filehandle.write('%s\n' % json.dumps(new_info))

                # append, or create, the all_webhooks.log - Summary all logs
                with open('all_webhooks.log', 'a') as filehandle:
                    filehandle.write('%s\n' % json.dumps(new_info))

                # construct the team message
                teams_message = 'Severity:       ' + severity
                teams_message += '\nCategory:       ' + category
                teams_message += '\nTimestamp:      ' + str(timestamp)
                teams_message += '\nIssue Name:     ' + issue_name
                teams_message += '\nIssue Description:  ' + issue_description
                teams_message += '\nIssue Status:   ' + issue_status
                print('New DNAC Webex Teams_Message\n', teams_message)

                # post markdown message in teams space, with title of the message
                teams_message_title = 'New Cisco DNA Center Notification:'
                post_space_markdown_message(WEBEX_TEAMS_ROOM, teams_message_title)

                # post message in teams space
                post_space_message(WEBEX_TEAMS_ROOM, teams_message)
                teams_message = 'Issue Details:  Click Here\n'

                # post message in teams space, with url for the issue
                post_space_url_message(WEBEX_TEAMS_ROOM, teams_message, url)

        finally:
            pass
        try:
            if 'values' in request_json:
                sdwan_notification = request_json

                # save all info to variables, prepare to save to file
                severity = sdwan_notification['severity']
                timestamp = str(datetime.datetime.fromtimestamp(int(sdwan_notification['entry_time'] / 1000)).strftime('%Y-%m-%d %H:%M:%S'))
                try:
                    site_id = str(sdwan_notification['values'][0]['site-id'])
                except:
                    site_id = ' '
                system_ip = sdwan_notification['values'][0]['system-ip']
                host_name = sdwan_notification['values'][0]['host-name']
                message = sdwan_notification['message']
                issue_status = str(sdwan_notification['active'])
                url = SDWAN_URL + '/index.html#/app/monitor/alarms/details/' + sdwan_notification['uuid']

                # create the summary SD-WAN log - Cisco SD-WAN summary logs
                new_info = {'severity': severity, 'entry_time': sdwan_notification['entry_time']}
                new_info.update({'site-id': site_id, 'system_ip': system_ip, 'host-name': host_name})
                new_info.update({'message': message, 'active': issue_status, 'alarm details': url})

                # append, or create, the sdwan_webhooks.log
                with open('sdwan_webhooks.log', 'a') as filehandle:
                    filehandle.write('%s\n' % json.dumps(new_info))

                # append, or create, the all_webhooks.log - Summary all logs
                with open('all_webhooks.log', 'a') as filehandle:
                    filehandle.write('%s\n' % json.dumps(new_info))

                # construct the team message
                teams_message = 'Severity:           ' + severity
                teams_message += '\nTimestamp:          ' + timestamp
                teams_message += '\nSite Id:            ' + site_id
                teams_message += '\nSystem IP:          ' + system_ip
                teams_message += '\nHost Name:          ' + host_name
                teams_message += '\nIssue Description:  ' + message
                teams_message += '\nIssue Status:       ' + issue_status
                print('New SD-WAN Webex Teams_Message\n', teams_message)

                # post markdown message in teams space, with title of the message
                teams_message_title = 'New Cisco SD-WAN Notification:'
                post_space_markdown_message(WEBEX_TEAMS_ROOM, teams_message_title)

                # post message in teams space
                post_space_message(WEBEX_TEAMS_ROOM, teams_message)

                # post message in teams space, with url for the issue
                teams_message = 'Issue Details:  Click Here\n'
                post_space_url_message(WEBEX_TEAMS_ROOM, teams_message, url)
        finally:
            pass
        return {'response': 'Notification Received'}, 200
    else:
        abort(400)


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """
    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def get_space_id(space_name):
    """
    This function will find the Webex Teams space id based on the {space_name}
    Call to Webex Teams - /rooms
    :param space_name: The Webex Teams space name
    :return: the Webex Teams space Id
    """
    payload = {'title': space_name}
    space_number = None
    url = WEBEX_TEAMS_URL + '/rooms'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    space_response = requests.get(url, data=json.dumps(payload), headers=header, verify=False)
    space_list_json = space_response.json()
    space_list = space_list_json['items']
    for spaces in space_list:
        if spaces['title'] == space_name:
            space_number = spaces['id']
    return space_number


def post_space_message(space_name, message):
    """
    This function will post the {message} to the Webex Teams space with the {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call /messages
    :param space_name: the Webex Teams space name
    :param message: the text of the message to be posted in the space
    :return: none
    """
    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'text': message}
    url = WEBEX_TEAMS_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def post_space_markdown_message(space_name, message):
    """
    This function will post a markdown {message} to the Webex Teams space with the {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call /messages
    :param space_name: the Webex Teams space name
    :param message: the text of the markdown message to be posted in the space
    :return: none
    """
    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'markdown': ('**' + message + '**')}
    url = WEBEX_TEAMS_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


def post_space_url_message(space_name, message, url):
    """
    This function will post an URL to the Webex Teams space with the {space_name}
    Call to function get_space_id(space_name) to find the space_id
    Followed by API call /messages
    :param space_name: the Webex Teams space name
    :param message: the text of the markdown message to be posted in the space
    :param url: URL for the text message
    :return: none
    """
    space_id = get_space_id(space_name)
    payload = {'roomId': space_id, 'markdown': ('[' + message + '](' + url + ')')}
    url = WEBEX_TEAMS_URL + '/messages'
    header = {'content-type': 'application/json', 'authorization': WEBEX_TEAMS_AUTH}
    requests.post(url, data=json.dumps(payload), headers=header, verify=False)


if __name__ == '__main__':
    app.run(debug=True)


