from Tkinter import *
import csv
from PIL import Image, ImageTk
import time
import tkMessageBox
import os

BUTTON_HEIGHT = 1
BUTTON_WIDTH = 15
WACHTTIJD = 1000 #in miliseconden
PRIJS_BIER = 0.70
PRIJS_TOSTI = 0.70
PRIJS_KOEK = 0.40
PRIJS_SNOEP = 0.60 
PRIJS_FRIS = 0.65
PRIJS_STERK = 1.00
PRIJS_WIJN = 0.85
PRIJS_SOEP = 0.50
PRIJS_CHIPS = 0.60
ACHTERGRONDKLEUR = "white"
WACHTWOORD = "Wachtwoord"

class Lid():
    def __init__(self, naam, fris, tosti, bier, sterke_drank, wijn, koekjes, snoep, soep, chips, geld, geboortedatum, wachtwoord):
        name = naam.split()
        self.voornaam = name[0]
        self.achternaam = ' '.join(name[1:len(name)])
        self.naam = str(naam)
        self.aantal_fris = int(fris)
        self.aantal_tosti = int(tosti)
        self.aantal_bier = int(bier)
        self.aantal_sterke_drank = int(sterke_drank)
        self.aantal_wijn = int(wijn)
        self.aantal_snoep = int(snoep)
        self.aantal_koekjes = int(koekjes)
        self.aantal_soep = int(soep)
        self.aantal_chips = int(chips)
        self.hoeveelheid_geld = float(geld)
        self.geboortedatum = geboortedatum
        self.wachtwoord = wachtwoord
        
class LedenLijst():
    def __init__(self):
        self.rij = []
        
    def add(self, lid):
        self.rij.append(lid)
        
class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        Frame.configure(self,background = ACHTERGRONDKLEUR)
        
    def create_widgets(self):
        ML = Image.open('menslogo.JPG')
        achtergrond = ImageTk.PhotoImage(ML)
        self.backlabel = Label(root, image= achtergrond)
        self.backlabel.image = achtergrond
        self.backlabel.grid(row= 1, column = 1)
        self.naam = Entry(self, background = "gold") 
        submit = Button(self, text = "Registreer naam", command = self.check_name, bg = 'wheat1', activebackground = "wheat2")
        submit.grid(row = 2, column = 0, sticky= W)
        self.tekst_naam = Text(self, width=40, height = 2, wrap = WORD, background = ACHTERGRONDKLEUR)
        self.tekst_naam.grid(row = 3, column = 0, sticky = W, columnspan = 2)
        labelnaam = Label(self, text = "Voer voornaam in:", background = ACHTERGRONDKLEUR)
        labelnaam.grid(row=0, column =0, sticky = W)
        self.naam.grid(row=1, column=0, sticky = W)
        self.stopknop = Button(self, text = "Afsluiten", command = self.stop_programma, bg = 'red4', fg = "snow", \
                               activebackground = "red4", activeforeground = "snow")
        self.stopknop.grid(row = 0, column = 2, sticky = E)
        euro = u"\u20AC"
        a = u"\u00E0"
        text1 = "%s %s " %(a, euro)
        self.lijst_wat2 = ["Fris", "Bier", "Tosti", "Snoep", "Koek", "Wijn", "Sterke drank", "Soep", "Chips"]
        self.lijst_wat3 = ["Fris", "Tosti", "Snoep", "Koek", "Soep", "Chips"]
        self.alg_lib = {"Fris": [PRIJS_FRIS, "Fris "+text1+"%.2f" %(PRIJS_FRIS), 'salmon', 'dark salmon'], \
                        "Bier": [PRIJS_BIER, "Bier "+text1+"%.2f" %(PRIJS_BIER),'OliveDrab1', 'OliveDrab3'], \
                        "Tosti": [PRIJS_TOSTI,  "Tosti "+text1+"%.2f" %(PRIJS_TOSTI), 'yellow', 'yellow3'], \
                        "Snoep": [PRIJS_SNOEP, "Snoep "+text1+"%0.2f" %PRIJS_SNOEP, 'orange red', "OrangeRed3"], \
                        "Koek": [PRIJS_KOEK, "Koek "+text1+"%.2f" %(PRIJS_KOEK), 'MediumPurple1', "MediumPurple3"], \
                        "Wijn": [PRIJS_WIJN, "Wijn "+text1+"%.2f" %PRIJS_WIJN,'spring green', "SpringGreen3"],\
                        "Sterke drank": [PRIJS_STERK, "Sterke drank "+text1+"%.2f" %PRIJS_STERK, 'sky blue', "SkyBlue3"],\
                        "Soep": [PRIJS_SOEP, "Soep "+text1+"%.2f" %PRIJS_SOEP, 'maroon1', "maroon2"],\
                        "Chips": [PRIJS_CHIPS, "Chips "+text1+"%.2f" %PRIJS_CHIPS, 'gray70', "gray60"]}
        
    def stop_programma(self):
        self.ww = Entry(Toplevel(), text="Wachtwoord", show='*')
        self.ww.pack()
        self.ww.bind('<Return>', self.controleer)
        
    def controleer(self, event):
        if self.ww.get()==WACHTWOORD:
            Frame.quit(self)
        else:
            tkMessageBox.showwarning("Wrong password", "The entered password is incorrect!")
        
    def maak_keuze(self):
        if self.content in minderjarigen:
            self.lijst_wat = self.lijst_wat3
        else:
            self.lijst_wat = self.lijst_wat2
        pos = 0
        self.lib_knop = {}
        for artikel in self.lijst_wat:
            action = lambda x = artikel: self.doe_aankoop(x)
            self.lib_knop[artikel] = Button(self, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = self.alg_lib[artikel][1], \
                           bg = self.alg_lib[artikel][2], activebackground = self.alg_lib[artikel][3], command = action)
            self.lib_knop[artikel].grid(row = 4+pos, column = 0, sticky = W)
            pos += 1
        self.verkeerd = Button(self, width = BUTTON_WIDTH, height = 2*BUTTON_HEIGHT, text = "Ik heb \nverkeerd gestreept.", \
                               bg = "medium sea green", activebackground = "dark sea green", command=self.verkeerd_streep)
        self.verkeerd.grid(row = 4+pos+1, column = 0, sticky = W)
        self.backlabel.destroy()
        self.nu_gestreept()
        self.al_gestreept = []

    def verkeerd_streep(self):
        self.verkeerd.destroy()
        for artikel in self.lijst_wat:
            self.lib_knop[artikel].destroy()
        for lid in leden.rij:
            if lid.naam == self.content:
                if lid.aantal_bier+lid.aantal_chips+lid.aantal_fris+lid.aantal_koekjes==0+lid.aantal_snoep+lid.aantal_soep+lid.aantal_sterke_drank+lid.aantal_tosti+lid.aantal_wijn==0:
                    self.doorgaan = Button(self, width = BUTTON_WIDTH, height = 10*BUTTON_HEIGHT, text = "U hebt nog niets gestreepd deze maand. Neem contact op met AC of Bestuur om fouten in de voorgaande maand te wijzigen.", bg = "pale green", \
                                        activebackground = "spring green", wraplength=BUTTON_WIDTH*6,command = self.na_fout) 
                    self.doorgaan.grid(row = 6, column = 0, sticky = W) 
                else: 
                    if lid.aantal_bier > 0:
                        self.al_gestreept.append("Bier")
                    if lid.aantal_chips > 0:
                        self.al_gestreept.append("Chips")
                    if lid.aantal_fris > 0:
                        self.al_gestreept.append("Fris")                    
                    if lid.aantal_koekjes > 0:
                        self.al_gestreept.append("Koek")
                    if lid.aantal_snoep > 0:
                        self.al_gestreept.append("Snoep")                    
                    if lid.aantal_soep > 0:
                        self.al_gestreept.append("Soep")                    
                    if lid.aantal_sterke_drank > 0:
                        self.al_gestreept.append("Sterke drank")                    
                    if lid.aantal_tosti >= 1:
                        self.al_gestreept.append("Tosti")                    
                    if lid.aantal_wijn >= 1:
                        self.al_gestreept.append("Wijn")     
                    pos = 0
                    self.lib_knop2 = {}
                    for artikel in self.al_gestreept:
                        action = lambda x = artikel: self.streep_weg(x)
                        self.lib_knop2[artikel] = Button(self, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, text = self.alg_lib[artikel][1],\
                                            bg = self.alg_lib[artikel][2], activebackground = self.alg_lib[artikel][3], command = action)
                        self.lib_knop2[artikel].grid(row = 4+pos, column = 0, sticky = W)
                        pos += 1

    def na_fout(self):
        self.doorgaan.destroy()
        self.tekst3.destroy()
        self.na_bestelling()

    def streep_weg(self, artikel):
        wat_prijs = self.alg_lib[artikel][0]
        for lid in leden.rij:
           if lid.naam == self.content:
               if artikel == "Fris":
                   lid.aantal_fris -= 1
               elif artikel == "Bier":
                   lid.aantal_bier -= 1
               elif artikel == "Chips":
                    lid.aantal_chips -= 1
               elif artikel == "Koekjes":
                   lid.aantal_koekjes -= 1 
               elif artikel == "Snoep":
                   lid.aantal_snoep -= 1
               elif artikel == "Tosti":
                   lid.aantal_tosti -= 1
               elif artikel == "Soep":
                   lid.aantal_soep -= 1
               elif artikel == "Sterke drank":
                   lid.aantal_sterke_drank -= 1
               elif artikel == "Wijn":
                   lid.aantal_wijn -= 1
               lid.hoeveelheid_geld -= wat_prijs
        self.bestelling = Text(self, width = 40, height = 1, wrap = WORD)
        self.bestelling.delete(0.0, END)  
        self.bestelling.grid(row = 50, column = 0, columnspan = 2, sticky = W)
        message = "Uw annulering is geregistreerd."
        self.bestelling.insert(0.0, message)
        self.bestelling.configure(bg = "green2")
        Frame.after(self, WACHTTIJD, self.na_bestelling)
                    
    def doe_aankoop(self, artikel):
        wat_prijs = self.alg_lib[artikel][0]
        for lid in leden.rij:
           if lid.naam == self.content:
               if artikel == "Fris":
                   lid.aantal_fris += 1
               elif artikel == "Bier":
                   lid.aantal_bier += 1
               elif artikel == "Chips":
                    lid.aantal_chips += 1
               elif artikel == "Koekjes":
                   lid.aantal_koekjes += 1 
               elif artikel == "Snoep":
                   lid.aantal_snoep += 1
               elif artikel == "Tosti":
                   lid.aantal_tosti += 1
               elif artikel == "Soep":
                   lid.aantal_soep += 1
               elif artikel == "Sterke drank":
                   lid.aantal_sterke_drank += 1
               elif artikel == "Wijn":
                   lid.aantal_wijn += 1
               lid.hoeveelheid_geld += wat_prijs
        self.gestreepd_artikel = artikel
        self.registreer_aankoop()
        
    def registreer_aankoop(self):
        self.bestelling = Text(self, width = 40, height = 1, wrap = WORD)
        self.bestelling.delete(0.0, END)  
        self.bestelling.grid(row = 50, column = 0, columnspan = 2, sticky = W)
        message = "Uw bestelling is geregistreerd."
        self.bestelling.insert(0.0, message)
        self.bestelling.configure(bg = "green2")
        Frame.after(self, WACHTTIJD, self.na_bestelling)
        self.opzien = Text(self, bg = ACHTERGRONDKLEUR, width = 100, height = 50)
        self.tijd = str()
        self.opzien.insert(1.0, self.tijd+":\t"+str(self.gestreepd_artikel)+"\n")
        
    def na_bestelling(self):
        self.tekst_naam.delete(0.0, END)
        self.tekst_naam.configure(background = ACHTERGRONDKLEUR)
        self.naam.delete(0, END)
        self.verkeerd.destroy()
        for artikel in self.lijst_wat:
            self.lib_knop[artikel].destroy()
        for stuk in self.al_gestreept:
            self.lib_knop2[stuk].destroy()
        self.bestelling.destroy()
        self.tekst3.destroy()
        ML2 = Image.open('menslogo.JPG')
        achtergrond = ImageTk.PhotoImage(ML2)
        self.backlabel = Label(root, image= achtergrond)
        self.backlabel.image = achtergrond
        self.backlabel.grid(row= 1, column = 1)
        self.content = " "
        
    def nu_gestreept(self):
        for lid in leden.rij:
            if lid.naam == self.content: 
                nu_gestreept2 = "Huidige aantal consumpties: \nFris: \t\t%.0f \nBier: \t\t%.0f \nTosti: \t\t%.0f \nSnoep: \t\t%.0f\
                \nKoek: \t\t%.0f \nWijn: \t\t%.0f \nSterke drank:  \t%.0f \nSoep: \t\t%.0f \nChips:\t\t%.0f \nDit komt totaal op %.2f euro." \
                %(lid.aantal_fris, lid.aantal_bier, lid.aantal_tosti, lid.aantal_snoep, lid.aantal_koekjes, lid.aantal_wijn, \
                  lid.aantal_sterke_drank, lid.aantal_soep, lid.aantal_chips, lid.hoeveelheid_geld)
                self.tekst3 = Label(self, text = nu_gestreept2, bg = ACHTERGRONDKLEUR, justify = LEFT)
                self.tekst3.grid(row = 4, column = 1, rowspan = 9, sticky = S)

    def make_name(self):
        first_name = self.naam.get().title().strip()
        if voornamen.count(first_name) == 0:
            message = "Naam onbekend, probeer opnieuw. \n"
            self.tekst_naam.insert(0.0, message)
            self.tekst_naam.configure(background = "red4", fg = "snow")            
        elif voornamen.count(first_name) == 1:
            for lid in leden.rij:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    self.content = vol_naam
        else:
            self.nu_rij = []
            self.tekst4 = Label(self, text = "Kies uw naam:", bg = ACHTERGRONDKLEUR)
            self.tekst4.grid(row = 4, column = 0)
            self.btn_dict = {}
            for lid in leden.rij:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    self.nu_rij.append(vol_naam)
            i = 0    
            for person in self.nu_rij:
                action = lambda x = person: self.reg_naam(x)
                self.btn_dict[person] = Button(self, width = 40, text = person, \
                                            command = action, bg = 'thistle2', activebackground = "thistle3")
                self.btn_dict[person].grid(row = 5+i, column = 0)
                i += 1
                    
    def reg_naam(self,name2):
        self.content = name2
        self.tekst4.destroy()
        for person in self.nu_rij:
            self.btn_dict[person].destroy()
        if self.content in namen:
            message = "Geregistreerd als "+self.content+", kies uw consumptie. \n"
            self.tekst_naam.insert(0.0, message)
            self.tekst_naam.configure(background = "green2", fg = "black")
            self.maak_keuze()
        
    def check_name(self):
        self.make_name()
        if self.content in namen:
            for lid in leden.rij:
                if lid.naam == self.content:
                    if lid.wachtwoord!='0':
                        self.check_password()
                    else: 
                        message = "Geregistreerd als "+self.content+", kies uw consumptie. \n"
                        self.tekst_naam.insert(0.0, message)
                        self.tekst_naam.configure(background = "green2", fg = "black")
                        self.maak_keuze()
            
    def check_password(self):
        self.top = Toplevel()
        self.password = Entry(self.top, text="Wachtwoord", show='*')
        self.password.delete(0, 'end')
        self.password.bind('<Return>', self.control)
        self.password.pack()
        
        
    def control(self,event):
        if self.password.get() == lid.wachtwoord:
            self.trueww = 1
        else: self.trueww = 0 
        self.top.destroy()
        if self.trueww == 1:
            message = "Geregistreerd als "+self.content+", kies uw consumptie. \n"
            self.tekst_naam.insert(0.0, message)
            self.tekst_naam.configure(background = "green2", fg = "black")
            self.maak_keuze()
        else: self.na_bestelling()

def check_minderjarig(row):
    lid = row[11].split("-")
    dag = int(lid[0])
    maand = int(lid[1])
    jaar = int(lid[2])
    nu_jaar = int(time.strftime("%Y"))
    nu_maand = int(time.strftime("%m"))
    nu_dag = int(time.strftime("%d"))
    wat = False
    if (jaar+18) > nu_jaar:
        wat = True
    if (jaar+18) == nu_jaar:
        if maand > nu_maand:
            wat = True
        elif maand == nu_maand:
            if dag > nu_dag:
                wat = True
    return wat
                
nu_jaar = int(time.strftime("%Y"))
nu_maand = int(time.strftime("%m"))
filename = '%d-%d.csv' %(nu_jaar, nu_maand)
if (os.path.isfile(filename)):
    filename2 = filename
else: filename2 = 'template.csv'
      
with open(filename2, 'rb') as csvfile:
    file_now = csv.reader(csvfile, delimiter = ';')
    leden = LedenLijst()
    namen = []
    minderjarigen = []
    voornamen = []
    for row in file_now:
        if row[0] != 'Naam' and row[0] != 'Totaal' and row[0]!='Omzet' and row[0]!="Voorraad":
            lid = Lid(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12])
            leden.add(lid)
            namen.append(row[0])
            voornamen.append(row[0].split()[0])
            if check_minderjarig(row):
                minderjarigen.append(row[0])
        elif row[0] == "Voorraad":
            voor_fris = int(row[1])
            voor_tosti = int(row[2])
            voor_bier = int(row[3])
            voor_sterk = int(row[4])
            voor_wijn = int(row[5])
            voor_koek = int(row[6])
            voor_snoep = int(row[7])
            voor_soep = int(row[8])
            voor_chips = int(row[9])
        elif row[0] == 'Totaal':
            totaal_fris = int(row[1])
            totaal_tosti = int(row[2])
            totaal_bier = int(row[3])
            totaal_sterk = int(row[4])
            totaal_wijn = int(row[5])
            totaal_koek = int(row[6])
            totaal_snoep = int(row[7])
            totaal_soep = int(row[8])
            totaal_chips = int(row[9])
            totaal_geld = float(row[10])
        elif row[0] == 'Omzet':
            omzet_fris = float(row[1])
            omzet_tosti = float(row[2])
            omzet_bier = float(row[3])
            omzet_sterk = float(row[4])
            omzet_wijn = float(row[5])
            omzet_koek = float(row[6])
            omzet_snoep = float(row[7])
            omzet_soep = float(row[8])
            omzet_chips = float(row[9])
            totaal_omzet = float(row[10])
    root = Tk()
    root.title("Streepsysteem Studievereniging Mens, versie januari 2015")
    root.geometry("1000x600")
    root.configure(background = ACHTERGRONDKLEUR)
    app = Application(root)
    root.mainloop()
    with open(filename, 'wb') as csvfile2:
        file_now2 = csv.writer(csvfile2, delimiter = ';')
        file_now2.writerow(['Naam', 'Fris', 'Tosti', 'Bier', 'Sterke drank', 'Wijn', 'Koek', 'Snoep', 'Soep', 'Chips', 'Geld', 'Geboortedatum'])    
        for row in leden.rij:
            volled_naam = "%s %s" %(row.voornaam, row.achternaam)
            file_now2.writerow([volled_naam, row.aantal_fris, row.aantal_tosti, row.aantal_bier, row.aantal_sterke_drank, \
                row.aantal_wijn, row.aantal_koekjes, row.aantal_snoep, row.aantal_soep, row.aantal_chips, row.hoeveelheid_geld, row.geboortedatum])
            totaal_fris += row.aantal_fris
            totaal_tosti += row.aantal_tosti
            totaal_bier += row.aantal_bier
            totaal_geld += row.hoeveelheid_geld
            totaal_koek += row.aantal_koekjes
            totaal_sterk += row.aantal_sterke_drank
            totaal_wijn += row.aantal_wijn
            totaal_snoep += row.aantal_snoep
            totaal_chips += row.aantal_chips
            totaal_soep += row.aantal_soep
        file_now2.writerow(['Totaal', totaal_fris, totaal_tosti, totaal_bier, totaal_sterk, totaal_wijn, totaal_koek, \
                            totaal_snoep, totaal_soep, totaal_chips, totaal_geld, " "])
        omzet_fris += totaal_fris*PRIJS_FRIS
        omzet_bier += totaal_bier*PRIJS_BIER
        omzet_chips += totaal_chips*PRIJS_CHIPS
        omzet_koek += totaal_koek*PRIJS_KOEK
        omzet_snoep += totaal_snoep*PRIJS_SNOEP
        omzet_soep += totaal_soep*PRIJS_SOEP
        omzet_sterk += totaal_sterk*PRIJS_STERK
        omzet_tosti += totaal_tosti*PRIJS_TOSTI
        omzet_wijn += totaal_wijn*PRIJS_WIJN
        totaal_omzet = omzet_bier+omzet_chips+omzet_fris+omzet_koek+omzet_snoep+omzet_soep+omzet_sterk+omzet_tosti+omzet_wijn
        file_now2.writerow(['Omzet', omzet_fris, omzet_tosti, omzet_bier, omzet_sterk, omzet_wijn, omzet_koek, omzet_snoep, omzet_soep,\
                            omzet_chips, totaal_omzet, " "])
        file_now2.writerow(["Voorraad", voor_fris, voor_tosti, voor_bier, voor_sterk, voor_wijn, voor_koek, voor_snoep, voor_soep,\
                            voor_chips, " ", " "])
