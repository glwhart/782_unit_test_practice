"""Defines a class and methods for evaluating 1D quantum potentials.
"""
import numpy as np
class Potential(object):
    """ Represents a 1D quantum Potential.

    Args:
        potcfg (str): path ot the potential configuration file.
    
    Attributes:
        filepath (str): absolute bath to the file that this potential represents.
        params (dict): keys are parameter names; values are python-evaluated objects.
        regions (dict): keys are a tuple (`float`, `float`) that specify the start and end
        of the region; values are either functions or variables to define the potential's value
        in that region.
        parser (ConfigParser): parses the potential configuration file.

    Examples:
        >>> from basis.potential import Potential
        >>> import numpy as np
        >>> x = np.linspace(-2, 2, 100)
        >>> pot = Potential("sho.cfg")
        >>> V = pot(x)
    """
    def __init__(self, potcfg):
        from os import path
        self.filepath = path.abspath(path.expanduser(potcfg))
        self.params = {}
        self.regions = {}
        self.parser = None
        self._parse_config()

    def __call__(self, value):
        """Evaluates the potential for the given value(s).

        Args:
            value (numpy.ndarray or float): where to evaluate

        Returns:
            numpy.ndarray or float: potential evaluated at `value`.

        Raises:
            ValueError: if the argument is not an `int` or `float`.
        """
        if isinstance(value, list) or isinstance(value, np.ndarray):
            #return np.array([self(v) for v in value])
            return np.array(map(self,value))

        if not isinstance(value, (int,float)):
            raise ValueError("Only `int` and `float` values can be "
                             "evaluated by the potential.")
        
        for xi,xf in self.regions:
            if value >= xi and value < xf:
                function = self.regions[(xi,xf)]
                if hasattr(function, "__call__"): # If it was a lamda function, call it
                    return function(value) 
                else: # Otherwise it was just a specified value, return that value
                    return function
        else: # If we didn't return during the loops, then this is the default thing to return
            return 0.
        
    def __mul__(self, value):
        """Increases the strength of the potential by factor given by `value`.

        Args:
            value (float): how much to multiply by
        """
        #Do I want to overwrite the strength of the potential, or return a new instance of
        #Potential?
        pass
    
    def _parse_params(self):
        """Extracts the potential parameters from the specified config parser.
        """
        if self.parser.has_section("parameters"):
            for param, svalue in self.parser.items("parameters"):
                self.params[param] = eval(svalue)

    def adjust(self, **kwargs):
        """Adjusts the parameters of the potential.
       
        Args:
            kwargs (dict): parameters and values to overwrite.
        
        Notes:
        If a paramater is specified that was not originiall defined in 
        the potential config fil, the update is ignored. A warning is printed
        that can be seen if verbosity is enabled.
        """
        for k, v in kwargs.items():
            if k in self.params:
                self.params[k] = v
            else:
                wmsg = "'{}' is not a valid parameter for '{}'."
                msg.warn(wmsg.format(k,self.filepath))
                
        self.params.update(kwargs)
        self._parse_regions()
    
    def _parse_regions(self):
        """Parses the potential's region specifications from config.
        """
        if not self.parser.has_section("regions"):
            raise ValueError("[regions] is required to define a potential.")
        self.regions = {}
        
        for i, spec in self.parser.items("regions"):
            domain, sfunc = spec.split('|')
            if "numpy" in sfunc:
                import numpy as np
                self.params["numpy"] = np
            xi, xf = eval(domain, self.params)
            function = eval(sfunc, self.params)
            self.regions[(xi,xf)] = function
            
    def _parse_config(self):
        """Parses the potential configuration file to initialize the
        parameters and function call.
        """
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser

        self.parser = ConfigParser()
        with open(self.filepath) as f:
            self.parser.readfp(f)

        self._parse_params()
        self._parse_regions()
        

