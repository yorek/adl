import json
from azsc.handlers.Handler import Handler
from azsc.handlers.az.Generic import GenericHandler

class AppInsightsHandler(GenericHandler):
    azure_object = "appinsights"
    
    def execute(self):
        self.resources = [ "resource" ]

        if (self.action == "create"):            
            properties = {
                "ApplicationId": self.params["application-id"].strip('"'),
                "Application_Type": "other",
                "Flow_Type": "Redfield"
            }

            del self.params["application-id"]

            self.add_parameter("properties", "'" + json.dumps(properties) + "'")
            self.add_context_parameter("resource-group", "group")
            self.add_context_parameter("location", "location")

        if (self.action == "list"):
            self.action = "show"
            self.add_context_parameter("resource-group", "group")

        self.add_parameter("resource-type", '"Microsoft.Insights/components"')

        cmd = super(AppInsightsHandler, self).execute()

        self.save_to_context()

        return cmd

