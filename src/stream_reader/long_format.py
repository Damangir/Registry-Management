'''
Created on Aug 12, 2015

@author: soheil
'''
import re

from stream_reader.base_reader import BaseReader

def _is_list(header_name):
    outname = re.split('\.[\d]+', header_name)
    return (len(outname) > 1, outname[0])

class LongFormatReader(BaseReader):
    '''
    classdocs
    '''
    
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        defaults = {
                    "check_list":_is_list,
                    "collapse_list":False,
                    "is_header_list":[],
                    }
        parameters = defaults
        parameters.update(kwargs)
        super(LongFormatReader, self).__init__(**parameters)

    def parse_header(self, header_line):
        super(LongFormatReader, self).parse_header(header_line)
        self.header_list = [self.check_list(a) for a in self.header_list]

    def parse_line(self, line_list):
        '''
        Inputs a list of input and outputs an id and an object
        '''
        obj = {}
        for k,v in zip(self.header_list, line_list):
            is_list = k[0]
            name = k[1]
            if is_list:
                if self.collapse_list:
                    if v:
                        obj[name] = obj.get(name,[]) + [v]
                else:
                    obj[name] = obj.get(name,[]) + [v]
            else:
                obj[name] = v
        
        return obj[self.id_name], obj
                
    def insert_object(self,obj_id, obj):
        self.data[obj_id] = obj
