import uuid

from os import getenv
from load_dotenv import load_dotenv
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact
from langchain_ollama import OllamaLLM


class Llama:
    def __init__(self):
        self.model = OllamaLLM(model="llama3")

    def alert_description(self, question):   
        return self.model.invoke(input=question)
    
class TheHive(Llama):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.api_url = getenv("thehive_endpoint")
        self.api_key = getenv("thehive_api") 
        self.hive = TheHiveApi(self.api_url, self.api_key)
        
    def create_alert(self, alert:dict):
        """
        All the alerts in the splunk will be created on thehive.
        
        Args:
            alerts (dict): new_alert() function from splunk_automation.py
         
        """
        
        alert = Alert(
            title=f"Splunk Alert: {alert['event_description']}",
            description=self.alert_description(f"Can you explain the {alert["SourceName"]} eventcode {alert["EventCode"]}"),
            source="Splunk",
            type="external",
            sourceRef=f"Splunk Alert: {alert['event_description']} - {uuid.uuid4()}",
            artifacts=[
            AlertArtifact(dataType="host", data=alert["host"]),
            AlertArtifact(dataType="datetime", data=alert["_time"]),
            AlertArtifact(dataType="other", data=alert["SourceName"], message="Source Name"),
            AlertArtifact(dataType="integer", data=alert["EventCode"], message="Event Code")
        ])
        self.hive.create_alert(alert)
        
    
    def get_alert_ids(self):
        """
        This function is used to get the alert ids from thehive.
        """
        ids = []
        alerts_datas = self.hive.find_alerts()
        for datas in alerts_datas.json():
            ids.append(datas["id"])
        return ids

    
    def creator_case(self, list_ids):
        """
        This function is used to create a case in thehive.
        
        Args:
            list_ids (list): list of alert ids(self.get_alerts_ids()).
        """
        
        for id in list_ids:
            self.hive.promote_alert_to_case(id)
