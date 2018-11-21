from .Generic import GenericHandler

class StorageShareHandler(GenericHandler):
    azure_object = "storage share"
 
    def execute(self):
        self.add_context_parameter("account-name", "storage account")

        cmd = super(StorageShareHandler, self).execute()

        self.save_to_context()

        return cmd

class StorageHandler(GenericHandler):
    azure_object = "storage account"
 
    def execute(self):
        self.add_context_parameter("resource-group", "group")
        
        if (self.action == "create"):
            self.add_context_parameter("location", "location")

        cmd = super(StorageHandler, self).execute()

        self.save_to_context()

        return cmd
  
   
        
        