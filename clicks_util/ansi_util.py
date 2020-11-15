'''
Black: \u001b[30m
Red: \u001b[31m
Green: \u001b[32m
Yellow: \u001b[33m
Blue: \u001b[34m
Magenta: \u001b[35m
Cyan: \u001b[36m
White: \u001b[37m
Reset: \u001b[0m
'''

def getColorCode(color):
    
    color_dict = {"Black": "\u001b[30m", "Red": "\u001b[31m", "Green": "\u001b[32m", "Yellow": "\u001b[33m", "Blue": r"\u001b[34m", "Magenta": "\u001b[35m", "Cyan": "\u001b[36m", "White": "\u001b[37m", "Reset": "\u001b[0m"}
    
    if color == "black":
        
        return color_dict.get("Black")
    
    elif "red":
        
        return color_dict.get("Red")
    
    elif "green":
        
        return color_dict.get("Green")

    elif "yellow":
        
        return color_dict.get("Yellow")
    
    elif "blue":
        
        return color_dict.get("Blue")
    
    elif "magenta":
        
        return color_dict.get("Magenta")
    
    elif "cyan":
        
        return color_dict.get("Cyan")
    
    elif "white":
        
        return color_dict.get("White")
    
    elif "reset":
        
        return color_dict.get("Reset")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    