# High Level Analyzer
# For more information and documentation, please go to https://github.com/saleae/logic2-examples


class Hla():

    def __init__(self):
        '''
        Initialize this HLA.

        If you have any initialization to do before any methods are called, you can do it here.
        '''
        self.buff = []
        pass

    def get_capabilities(self):
        '''
        Return the settings that a user can set for this High Level Analyzer. The settings that a user selects will later be passed into `set_settings`.

        This method will be called first, before `set_settings` and `decode`
        '''

        return {
            'settings': {
                'My String Setting': {
                    'type': 'string',
                },
                'My Number Setting': {
                    'type': 'number',
                    'minimum': 0,
                    'maximum': 100
                },
                'My Choices Setting': {
                    'type': 'choices',
                    'choices': ('A', 'B')
                }
            }
        }

    def set_settings(self, settings):
        '''
        Handle the settings values chosen by the user, and return information about how to display the results that `decode` will return.

        This method will be called second, after `get_capbilities` and before `decode`.
        '''

        # Here you can specify how output frames will be formatted in the Logic 2 UI
        # If no format is given for a type, a default formatting will be used
        # You can include the values from your frame data (as returned by `decode`) by wrapping their name in double braces, as shown below.
        return {
            'result_types': {
                'mytype': {
                    'format': '{{data.length}}'
                }
            }
        }

    def decode(self, frame):
        '''
        Handle data frame from input analyzer.

        `frame` will always be of the form:

        {
            'type': 'FRAME_TYPE'
            'start_time': ...,
            'end_time': ...,
            'data': {
                ...
            }
        }
        
        The `type` and contents of the `data` field will depend on the input analyzer.
        '''
        print(frame)
        #print(len(self.buff))
        self.buff.append(frame)

        d = lambda a : ord(self.buff[a]['data']['value'])
        #print(d(-1))
        #print(type(d(-1)))
        out = []
        # parse data
        while(len(self.buff) > 6):
            if d(0) == 36 and d(1) == 36 :
                #print("got header")
                psize = d(2)*256 + d(3)
                if(len(self.buff) < psize):
                    # not enough bytes for packet
                    break
                # have all the bytes
                alld = [d(x) for x in range(0,psize)]
                calc_checksum = 0
                for i in range(0,psize-1):
                    calc_checksum += alld[i]
                calc_checksum = calc_checksum % 256
                if(calc_checksum == alld[psize-1]):
                    # got real packet
                    # parse packet
                    
                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[0]['start_time'],
                        'end_time': self.buff[1]['end_time'],
                        'data': {
                            'length': 'Pre$$'
                        }
                    })

                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[2]['start_time'],
                        'end_time': self.buff[3]['end_time'],
                        'data': {
                            'length': 'Size:' + str(psize)
                        }
                    })

                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[4]['start_time'],
                        'end_time': self.buff[4]['end_time'],
                        'data': {
                            'length': 'Seq:' + str(d(4))
                        }
                    })

                    
                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[5]['start_time'],
                        'end_time': self.buff[5]['end_time'],
                        'data': {
                            'length': 'Type:' + str(d(5))
                        }
                    })

                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[6]['start_time'],
                        'end_time': self.buff[6]['end_time'],
                        'data': {
                            'length': 'Port:' + str(d(6))
                        }
                    })

                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[7]['start_time'],
                        'end_time': self.buff[psize-2]['end_time'],
                        'data': {
                            'length': 'Data'
                        }
                    })


                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': self.buff[psize-1]['start_time'],
                        'end_time': self.buff[psize-1]['end_time'],
                        'data': {
                            'length': 'Checksum'
                        }
                    })
                    
                    
                    # pop the data
                    for i in range(0,psize):
                        self.buff.pop(0)

                else:
                    # Checksum Mismatch
                    b = self.buff.pop(0)
                    out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': b['start_time'],
                        'end_time': b['end_time'],
                        'data': {
                            'length': 'Error1 - ' + str(b['data']['value'])
                        }
                    })      
            else:
                # Header is not right, ignore
                b=self.buff.pop(0)
                #print('poping', [d(x) for x in range(0,6)])
                out.append({
                        'type': 'mytype',  # This type matches up with the type returned from `set_settings`
                        'start_time': b['start_time'],
                        'end_time': b['end_time'],
                        'data': {
                            'length': 'Error2 - ' + str(b['data']['value']) + ' - ' + str(len(self.buff))
                        }
                    })
            break
        return out
            

