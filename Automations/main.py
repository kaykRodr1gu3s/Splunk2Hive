import splunk_automation
import thehive

class Automation:
    def __init__(self):
        self.splunk = splunk_automation.Splunk()
        self.thehive = thehive.TheHive()
    def main(self):
        """
        This function is used to main the alert data from splunk to thehive.
        """
        
        try:
            self.splunk.splunk_alert
        except:
            pass
        sid = self.splunk.getting_sid
        alert_data = self.splunk.alert_datas(sid)
        self.thehive.create_alert(alert_data)
        ids = self.thehive.get_alert_ids()
        self.thehive.creator_case(ids)
a = Automation()
a.main()