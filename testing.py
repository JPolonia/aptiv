x = {"SM1" : { "assembly1" : { "partnumber1" : {"qty" : 1,
                                              "description" : "string"},
                            "partnumber2" : {"qty" : 1,
                                              "description" : "string"}},
               "assembly2" : { "partnumber1" : {"qty" : 1,
                                                              "description" : "string"},
                                            "partnumber2" : {"qty" : 1,
                                                              "description" : "string"}}
}}

pass

del x["SM1"]["assembly2"]["partnumber2"]

pass



pass