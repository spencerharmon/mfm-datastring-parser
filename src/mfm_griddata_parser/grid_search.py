from .grid_data import GridData
import logging
logger = logging.getLogger(__name__)

class MatchCompareFunctions:
    def __call__(self, result_grid: list, match: dict):
        """
        Return true if all match conditions are met in the result grid, false otherwise.
        """
        self.result_grid = result_grid

        func = {
            "greater_than": self.greater_than,
            "less_than": self.less_than,
            "equal_to": self.equal_to,
            "greateq": self.greateq,
            "lesseq": self.lesseq,
            }
        result = []
        for key in func.keys():
            if key in match.keys():
                result.append(func[key](match[key]))

        for r in result:
            if not r:
                return False
        return True

    def greater_than(self, value):
        logger.debug(f'greater_than: {len(self.result_grid)}, {value}')
        return len(self.result_grid) > value
    
    def less_than(self, value):
        return len(self.result_grid) < value
    
    def equal_to(self, value):
        return len(self.result_grid) == value
    
    def greateq(self, value):
        return len(self.result_grid) >= value
    
    def lesseq(self, value):
        return len(self.result_grid) <= value
    

    
class GridSearch:
    """
    
    """
    def __call__(self, grid: GridData, match: dict):
        # event layer by default
        self.filtered_grid = grid.event_layer_atoms
        # support for the "base" key in the match object.
        if "base" in match.keys():
            if match.pop("base"):
                self.filtered_grid = grid.base_layer_atoms

        #lay out all of the searchable fields and their search functions
        func = {
            "name": self.name_filter,
            "symbol": self.name_filter,
            "argb": self.argb_filter,
            "data_members": self.data_members_filter,
            }
        for key in match.keys():
            if key in func.keys():
                # execute the filter function
                func[key](match[key])
            else:
                if hasattr(MatchCompareFunctions, key):
                    continue
                else:
                    logger.warning(f"Invalid search key: {key}")
        logger.debug([site.get_dict() for site in self.filtered_grid])
        
        process_result = MatchCompareFunctions()
        return process_result(self.filtered_grid, match)

    def name_filter(self, name):
        """
        remove atoms from the grid that don't match our name.
        """
        self.filtered_grid = [site for site in self.filtered_grid if site.name == name]

    def symbol_filter(self, symbol):
        """
        remove atoms that don't match our symbol
        """
        self.filtered_grid = [site for site in self.filtered_grid if site.symbol == symbol]
       
    def argb_filter(self, argb):
        """
        remove atoms from the grid that don't match our color
        """
        self.filtered_grid = [site for site in self.filtered_grid if site.argbname == argb]

    def data_members_filter(self, data_members):
        logger.error("Data member filter not implemented.")
               
