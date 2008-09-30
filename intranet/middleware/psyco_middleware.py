import psyco

class PsycoMiddleware(object):
    """
        This middleware enables the psyco extension module which can massively
        speed up the execution of any Python code.
    """
    def process_request(self, request):
        psyco.profile()
        return None
                                                                                
                                                                                
