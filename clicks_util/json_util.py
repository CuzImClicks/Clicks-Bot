'''
Created on 28.10.2020

@author: bruno
'''

import json
import os

class json_file:
    
    def __init__(self, name, path):
        
        self.name = name
        self.path = path
        self.full_path = f"{self.path}/{self.name}"

    def write(self, data):
        
        with open(self.full_path, "r+") as f:
            
            f.seek(0)
            
            f.truncate()
            
            json.dump(data, f, indent=2)
            
            f.close()   
            
    def read(self):
        
        with open(self.full_path, "r") as f:
            
            data = json.load(f)
            
            return data
        
        
    def move(self, new_path):

        try:
            os.replace(self.path, new_path)

        except Exception as e:

            print(e)
            
            
    def rename(self, new_name):

        try:
            os.rename(f"{self.path}{self.name}", f"{self.path}{new_name}")
            print("success")

        except Exception as e:
            print(e)
            pass
        
    def remove(self):
    
        try:
            os.remove(self.full_path)
    
        except Exception as e:
            
            print(e)
            
            
            
