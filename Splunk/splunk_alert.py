import os
import splunklib.client as client
from dotenv import load_dotenv


class Splunk:
    def __init__(self):
        load_dotenv()
        self.service = client.connect(host=os.getenv("splunk_host"), token=os.getenv("splunk_token"), autologin=True)


    def splunk_alert(self, alert_name):
        
        """
        This method will create an alert on Splunk. The alert will be sent to the Slack channel.
        """

        spl_query = """
                index=main EventCode IN (4625, 4624, 4648, 4675, 4720, 4726, 4732, 4740, 4672, 4697, 4688, 4698, 7045, 5156, 5158, 4663, 4670, 1102, 4719, 7030, 7040)
                | fields EventCode, host, users
                | lookup event_code.csv event_code AS EventCode OUTPUT event_description
                | table _time EventCode event_description host user
                | where isnotnull(event_description)
                """

        alert_slack_payload = {
            "actions":"slack",
            "action.slack": "1",
            "action.slack.param.attachment": "message",
            "action.slack.param.channel": os.getenv("slack_channel"),
            "action.slack.param.fields": "_time,EventCode,event_description,host",
            "action.slack.param.message": "A suspicious activity",
            "action.slack.param.webhook_url_override": os.getenv("slack_webhook"),
            "action.webhook.enable_allowlist": "0",
            "cron_schedule": "*/2 * * * *",
            "description": "Automation to send new alerts to slack channel",
            "is_scheduled": "1",
            "disabled": "0",
            "alert_type": "number of events", 
            "alert_comparator": "greater than",
            "alert_threshold": "0",
            "dispatch.earliest_time": "-1d",
            "dispatch.latest_time": "now"
            }

        self.service.saved_searches.create(alert_name, spl_query, **alert_slack_payload)


splunk = Splunk()
splunk.splunk_alert("High privillages")   