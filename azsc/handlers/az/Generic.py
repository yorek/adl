import sys
import collections
from azsc.handlers.Handler import Handler

class ContextParameter:
    name = None
    context = None

    def __init__(self, name, context):
        self.name = name
        self.context = context

    def __eq__(self, other):
        if isinstance(other, ContextParameter):
            return self.name == other.name
                
        return self.name == str(other)
    
    def __str__(self):
        return "{0} => {1}".format(self.name, self.context)
        
class GenericHandler(Handler):
    azure_object = "*"    

    context_parameters = {}
    required_parameters = []

    def __init__(self, context, resources, action, name, params):
        super(GenericHandler, self).__init__(context, resources, action, name, params)
        self.context_parameters = []

    def execute(self):
        cmd = u"az"
        cmd += u" {0}".format(' '.join(self.resources))
        cmd += u" {0}".format(self.action)
        
        if (self.name != None):
            cmd += u" --name {0}".format(self.name)

        #print("-> {0} {1} {2}".format(self.resources, self.action, self.name))
        #print("-> CONTEXT: {0}".format(self.context))
        #print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))

        # push parameters from valus available in the context
        for cp in self.context_parameters:
            self._param_from_context(cp.name, cp.context)            
        
        # check that all required parameters are set
        for rp in self.required_parameters:
            if not rp in self.params:
                print("-> PARAM: {0}".format(rp))
                sys.exit("Missing '{0}' required parameter.".format(rp))

        # add params to generated command line 
        if (len(self.params)>0):
            ordered_params = collections.OrderedDict(sorted(self.params.items()))
            for param in ordered_params:
                cmd += u" --{0} {1}".format(param, self.params[param])

        return cmd
 
    def add_context_parameter(self, parameter_name, context_name):
        self.context_parameters.append(ContextParameter(parameter_name, context_name))
        
    def _param_from_context(self, param_name, context_name):
        if not param_name in self.params:
            if context_name in self.context:
                self.params[param_name] = self.context[context_name]
            else:                    
                print("-> CONTEXT: {0}".format(self.context))
                print("-> PARAM_CONTEXT: {0}".format(self.context_parameters))
                sys.exit("Missing '{0}' parameter and not suitable context value '{1}' found.".format(param_name, context_name))

    def set_required_parameter(self, parameter_name):
        if not parameter_name in self.required_parameters:
            self.required_parameters.append(parameter_name) 
    