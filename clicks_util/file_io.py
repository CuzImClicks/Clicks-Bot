
import os 

class File:
    '''
    Dateien umbenennen, l�schen, erstellen, verschieben.
    Mit File("name der datei", "path der datei") ein Datei Objekt erstellen.
    '''

    def init(self, name, path):

        self.name = name
        self.path = path
        self.full_path = f"{self.path}\{self.name}"

    def write(self, data):

        with open(f"{self.path}{self.name}", "r+") as f:

            f.write(data)
            f.close()

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


def rename_raw(path, name, new_name):

    try:
        os.rename(f"{path}{name}", f"{path}{new_name}")
        print("success")

    except Exception as e:
        print(e)
        pass

def create(name, path):

    try:
        open(f"{path}{name}", "w+")

    except Exception as e:
        print(e)
        
        
def remove(path):
    
    try:
        os.remove(path)

    except Exception as e:
        
        pass