

class PsycoMiddleware(object):
    """
        This middleware enables the psyco extension module which can massively
        speed up the execution of any Python code.
    """
    def process_request(self, request):
      try:
        from psyco import psyco
        psyco.profile()
      except ImportError:
        pass
      return None
                                                                                
                                                                                