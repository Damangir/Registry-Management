'''
Created on Aug 12, 2015

@author: soheil
'''

class BaseReader(object):
    '''
    Base class for reading big file line by line
    '''

    
    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        defaults = {
                    "delim":',',
                    "strip_space":True,
                    "header_list":[],
                    "id_name":None,
                    "data":{},
                    "postprocessors":[],
                    "preprocessors":[]
                    }
        
        parameters = defaults
        parameters.update(kwargs)
        for k,v in parameters.iteritems():
            setattr(self, k, v)
    
    def parse_header(self, header_line):
        self.header_list = self.get_line_as_list(header_line)
        if not self.id_name:
            self.id_name = self.header_list[0]
        if not self.id_name in self.header_list:
            self.id_name = self.header_list[0]

    def parse_line(self, line_list):
        d=dict(zip(self.header_list, self.line_list))
        return d[self.id_name], d
                
    def insert_object(self,obj_id, obj):
        self.data[obj_id] = obj

    def read_line(self, line):
        line_list = self.get_line_as_list(line)

        for prc in self.preprocessors:
            line_list = prc(line_list)
        
        obj_id, obj = self.parse_line(line_list)                

        for prc in self.postprocessors:
            obj = prc(obj)
        
        self.insert_object(obj_id, obj)

    def get_line_as_list(self, line):
        return [item.strip() if self.strip_space else item for item in line.split(self.delim)]
    
    def read(self, data_handle):
        header_line = next(data_handle).strip()
        self.parse_header(header_line)
        for line in data_handle:
            self.read_line(line)
        return self.data

    def add_preprocessor(self, prc):
        self.preprocessors.append(prc)

    def add_postprocessor(self, prc):
        self.postprocessors.append(prc)
    
    def clear_preprocessor(self):
        self.preprocessors = []

    def clear_postprocessor(self):
        self.postprocessors = []