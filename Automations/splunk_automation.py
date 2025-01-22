import os
import json
import splunklib.client as client
from dotenv import load_dotenv

class Splunk:
    def __init__(self):
        load_dotenv()
        self.service = client.Service(host=os.getenv("splunk_host"),port=8089, token=os.getenv("splunk_token"), autologin=True)
        self.alert_name = "high privilage"
        self.query ="""index=main EventCode IN (4625, 4624, 4648, 4675, 4720, 4726, 4732, 4740, 4672, 4697, 4688, 4698, 7045, 5156, 5158, 4663, 4670, 1102, 4719, 7030, 7040)
                | fields EventCode, host, SourceName, 
                | lookup windows_event_code.csv event_code AS EventCode OUTPUT event_description
                | table _time EventCode event_description host  SourceName
                | where isnotnull(event_description)"""
        
    @property    
    def splunk_alert(self):
        """
        Creates a saved search (alert) in Splunk. The alert is triggered when suspicious events are detected.
        When triggered, it sends a message to a specified Slack channel.

        The alert uses a cron schedule to run every minutes and checks for specific event codes in the main index.
        """
        alert_payload = {
        "action.add_to_triggered_alerts": "1",
        "action.add_to_triggered_alerts.param.name": "value",
        "action.webhook.enable_allowlist": "0",
        "alert.suppress": "0",
        "alert.track": "1",
        "alert_type": "number of events",
        "cron_schedule": "* * * * *",
        "description": "Automation to send new alerts to slack channel",
        "dispatch.earliest_time": "-1d",
        "dispatch.latest_time": "now",
        "is_scheduled": "1",
        "disabled": "0",
        "alert_comparator": "greater than",
        "alert_threshold": "0", 
        "request.ui_dispatch_app": "search",
        "request.ui_dispatch_view": "search",
        "actions":"slack",
        "action.slack": "1",
        "action.slack.param.attachment": "message",
        "action.slack.param.channel": os.getenv("slack_channel"),
        "action.slack.param.fields": "_time,EventCode,event_description,host",
        "action.slack.param.message": "A suspicious activity",
        "action.slack.param.webhook_url_override": os.getenv("slack_webhook"),
        "action.webhook.enable_allowlist": "0",
        }

        self.service.saved_searches.create(self.alert_name, self.query, **alert_payload)
        
    @property
    def getting_sid(self):
            
        """
        Retrieves the search ID (SID) of the saved search if it matches the current query.

        Returns:
            str: The search ID (SID) of the matching job.
        """
                
        jobs = self.service.jobs.list()
        
        for job in jobs:
            if self.alert_name == job.content()["label"]:
                return job.content()["sid"].encode("utf-8")
    
    def alert_datas(self, sid, count_per_page=1):
        """
        Retrieves the results of a saved search using the search ID (SID).

        Args:
            sid (str): The search ID of the Splunk job.

        Returns:
            dict: A dictionary containing key details from the search results, such as:
                - ComputerName
                - Event id
                - Time
                - EventCode
                - Vendor product
                - Sourcetype
                - LogName
                - Keywords
        """
        offset = 0
        job = self.service.jobs[sid]
        results_bytes = job.results(output_mode="json", count=count_per_page, offset=offset).read()
        results_str = results_bytes.decode("utf-8")
        result_json = json.loads(results_str)
        
        return result_json["results"][0]
