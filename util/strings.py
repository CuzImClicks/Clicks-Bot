def get_help(name):
    help_muteall = "Dieser Befehl der nur für Admins verfügbar ist schaltet alle Personen in deinem Sprachkanal stumm." \
                   " Personen können sich nicht mehr selbst entmuten und können nur von admins einzeln entmuted werden," \
                   " oder durch den Befehl $unmuteall entmuted werden."

    help_unmuteall = "Dieser Befehl entmuted alle in deinem Sprachchannel. Dieser Befehl ist nur für Admins verfügbar."

    help_status = "Dieser Befehl ändert den Status des Bots"

    ausgabe_unmuteall = "Es wurden Personen in deinem channel erfolgreich entmuted. Mute sie wieder mit $muteall"

    ausgabe_muteall = "Es wurden Personen in deinem channel erfolgreich entmuted. Mute sie wieder mit $muteall"

    if name.lower() == "help_muteall":

        return help_muteall

    elif "help_unmuteall":

        return help_unmuteall

    elif "unmuteall_ausgabe":

        return help_unmuteall_ausgabe

    elif "muteall_ausgabe":

        return ausgabe_muteall

    elif "help_status":

        return help_status


def get_promotion_text(promoter, user):

    text = f"Hey {user.name},\n der Admin {promoter.name} hat dir nun Botaccess gewährt.\n Du kannst jetzt auf den Channel" \
           " #bot-infos und #bot-testing" \
           " zugreifen und Befehle an den Bot schreiben.\n Wenn du im #bot-testing $github schreibst erhälst du den Link" \
           " zum Clicks-Bot Repo.\n Wenn du eine übersicht über die Hauptbefehle des Bots brauchst, gebe einfach " \
           "$commands ein.\n Viel spaß!"

    return text


def get_credits():
    '''
    DEPREACHED replaced by a field
    '''
    text = f"Idee und coding: Henrik | Clicks \nTextgestaltung : Kai | K_Stein \n Bereitstellung des Servers : Luis | DasVakuum"

    return text
