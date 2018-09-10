from Handler import Handler
from Storage import StorageHandler
from ResourceGroup import ResourceGroupHandler
from EventGrid import EventGridHandler
from Eventhubs import EventHubsHandler

availabe_handlers = (vars()["Handler"].__subclasses__())

class HandlerManager:
    context = {}
    __handlers = {}

    def __init__(self):
        print("Loading handlers...")
        for h in availabe_handlers:
            print(". Found handler: '{0}'".format(h.azure_object))
            self.__handlers[h.azure_object] = h(self.context)
        print
        
    def set_context(self, name, value):
        self.context[name] = value

    def is_handler_available(self, azobject):
        return self.__handlers.has_key(azobject)

    def get_handler(self, azobject):
        return self.__handlers[azobject]
