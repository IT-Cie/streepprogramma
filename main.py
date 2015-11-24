import Tkinter as tk
import csv
import Image, ImageTk
import time
import tkMessageBox
import os, sys, shutil
import hashlib as h

#===============================================================================
# Instellingen
#===============================================================================

VERSIE = "November 2015"
WACHTWOORD = "Wachtwoord"
debuggen = False

#===============================================================================
# Controleer of benodigde bestanden bestaan, stop anders direct en toon missende 
# bestanden in errorlog.
#===============================================================================

try:
    missingfiles=[]
    for essentialfile in ['Streeplijst_0000-00.csv','Images\\menslogo.png','Images\\NoPicture.png',\
                          'Images\\Bier.png','Images\\Fris.png','Images\\Snoep.png',\
                          'Images\\Koek.png','Images\\Tosti.png','Images\\Wijn.png',\
                          'Images\\Sterk.png','Images\\Soep.png','Images\\Chips.png']:
        if not os.path.isfile(essentialfile):
            missingfiles.append(essentialfile)
    if not missingfiles == []:
        raise IOError('---'+time.strftime("%Y-%m-%d - %H:%M:%S")+'--- Bestand(en) niet aanwezig. Zo kan ik toch niet werken...', missingfiles)
except IOError as err:
    sys.exit(err.args)

class MainApplication(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Streepsysteem Studievereniging Mens, versie %s" % (VERSIE))
        
        # Dit maakt dat de frames even groot zijn als het window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Fullscreen mogelijkheid
        self.fullscreenstate = True
        self.attributes("-fullscreen", self.fullscreenstate)
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        
        if not debuggen:
            self.protocol("WM_DELETE_WINDOW", self.stop_programma)
            
        self.gebruiker = ""

        self.frames = {}

        for F in (LoginScherm, StreepScherm, AdminScherm):

            self.frames[F] = F(self)
            self.frames[F].grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginScherm)
        
    def show_frame(self,scherm):
        self.frames[scherm].voorbereiding()
        self.frames[scherm].tkraise()
        
    def toggle_fullscreen(self, event=None):
        self.fullscreenstate = not self.fullscreenstate
        self.attributes("-fullscreen", self.fullscreenstate)
        
    def exit_fullscreen(self, event=None):
        self.fullscreenstate = False
        self.attributes("-fullscreen", self.fullscreenstate)
        
    def stop_programma(self):
        stop = tk.Toplevel()        
        self.label = tk.Label(stop,text='Wachtwoord?')
        self.label.pack()
        self.ww = tk.Entry(stop, text="Wachtwoord", show="*")
        self.ww.pack()
        self.ww.bind('<Return>', self.controleer_einde)
        

    def controleer_einde(self, event=None):
        if self.ww.get()==WACHTWOORD:
            #self.destroy()
            tk.Tk.quit(self)
        else:
            tkMessageBox.showwarning("Verkeerd paswoord", "Het ingevoerde paswoord is incorrect!")
        
class LoginScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "yellow"
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)
        
        # Invoer van eigen naam
        self.naam = tk.Entry(self, justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.naam.pack(side="top", ipady=20, padx=100, pady=50)
        self.naam.bind("<Return>", self.check_name)
        
        # Informatie ruimte
        self.response = tk.Text(self, font="Calibri, 16", bd=0, width=25, height=4, bg=self.Achtergrondkleur, wrap=tk.WORD)
        self.response.tag_configure("center", justify='center')
        self.response.pack(padx=100)
        
        # Mens-logo
        self.menslogo = ImageTk.PhotoImage(Image.open('Images\\menslogo.png'))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= self.menslogo)
        self.backlabel.image = self.menslogo
        self.backlabel.pack(pady=50)
        
    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.response.delete(1.0,tk.END)
        self.naam.delete(0, tk.END)
        self.naam.focus()
        
    def check_name(self, event):
        first_name = self.naam.get().title().strip()
        self.response.configure(bg=self.Achtergrondkleur, fg="black")
        if voornamen.count(first_name) == 0:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "\nNaam onbekend, probeer opnieuw.")
            self.response.tag_add("center", 1.0, "end")
            self.response.configure(background = "red4", fg = "snow")            
        elif voornamen.count(first_name) == 1:
            for lid in leden:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    root.gebruiker = vol_naam
                    if lid.wachtwoord == '0':
                        root.show_frame(StreepScherm)
                    else:
                        self.insertedww = tk.StringVar()
                        self.wachtwoord = lid.wachtwoord
                        insertww = tk.Toplevel()
                        tk.Label(insertww, text = 'Wachtwoord?').grid(row=0)
                        tk.Entry(insertww,text = "Put in Password", textvariable = self.insertedww, show = '*').grid(row=1)
                        tk.Button(insertww, text = "Ok", command = self.check_password).grid(row=2)
        else:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "Kies uw naam")
            self.response.tag_add("center", 1.0, "end")
            self.backlabel.destroy()
            self.nu_rij = []
            self.btn_dict = {}
            for lid in leden:
                if first_name == lid.voornaam:
                    vol_naam = "%s %s" %(lid.voornaam, lid.achternaam)
                    self.nu_rij.append(vol_naam)
            for person in self.nu_rij:
                action = lambda x = person: self.reg_naam(x)
                self.btn_dict[person] = tk.Button(self, width = 40, text = person, font="Calibri, 16", \
                                            command = action, bg = self.Achtergrondkleur, activebackground="yellow2")
                self.btn_dict[person].pack(pady=10)
                
    def check_password(self):
        self.insertedww = h.sha224(self.insertedww.get())
        self.insertedww = self.insertedww.digest()
        if self.insertedww == self.wachtwoord:
            root.show_frame(StreepScherm)
        else:
            tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
    
    def reg_naam(self,vol_naam):
        root.gebruiker = vol_naam
        root.show_frame(StreepScherm)
        for person in self.nu_rij:
            self.btn_dict[person].destroy()
        # Mens-logo
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= self.menslogo)
        self.backlabel.image = self.menslogo
        self.backlabel.pack(pady=50)
        
class StreepScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "medium spring green"
        self.lettertype = ("Calibri, 15")
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)
        self.images = {}
        self.gestreept = {}
        for i in range(len(producten)):
            if os.path.isfile('Images\\'+producten[i]+'.png'):
                self.images[producten[i]] = ImageTk.PhotoImage(Image.open('Images\\'+producten[i]+'.png'))
            else:
                self.images[producten[i]] = ImageTk.PhotoImage(Image.open('Images\\NoPicture.png'))
            self.gestreept[producten[i]] = 0
        
        self.left_frame = tk.Frame(self, bg=self.Achtergrondkleur)
        self.right_frame = tk.Frame(self, bg=self.Achtergrondkleur)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="both", expand=False, padx=20)
        
        for x in range(5):
            self.left_frame.grid_columnconfigure(x, weight=1)
        
        for y in range(5):
            self.left_frame.grid_rowconfigure(y, weight=1)
        
        action = lambda: self.doe_aankoop()
        tk.Button(self.left_frame, text = "Doe aankoop", command = action, font=self.lettertype).grid(row = 1, column = 2, sticky="nsew")
        action = lambda: root.show_frame(LoginScherm)
        tk.Button(self.left_frame, text = "Terug", command = action, font=self.lettertype).grid(row = 1, column = 1, sticky="nsew")
        action = lambda: self.maak_wachtwoord()
        tk.Button(self.left_frame, text = "Maak nieuw wachtwoord", command = action, font=self.lettertype).grid(row = 1, column = 3, sticky="nsew")
        self.tekst_naam = tk.Text(self.right_frame, width=23, height = 2, bg=self.Achtergrondkleur, bd=0, font=self.lettertype)
        self.tekst_naam.tag_configure("center", justify='center')
        self.tekst_naam.pack(side="top", pady=20)
        self.tekst_al_gestreept = tk.Text(self.right_frame, width=23, height=len(producten)+7, bd=0, bg=self.Achtergrondkleur, font=self.lettertype)
        self.tekst_al_gestreept.pack(side="top")
        self.tekst_nu_gestreept = tk.Text(self.right_frame, width=23, height=len(producten)+7, bd=0, bg=self.Achtergrondkleur, font=self.lettertype)
        self.tekst_nu_gestreept.pack(side="top")
        
        self.euro = u"\u20AC"
        self.a = u"\u00E0"
                
        posrow=2; poscol=1
        for i in range(len(producten)):
            action = lambda x = producten[i]: self.nu_gestreept(x)
            foo=tk.Button(self.left_frame, image=self.images[producten[i]], text="%s %s %s %.2f" %(producten[i], self.a, self.euro, prijzen[i]), compound="top", font=self.lettertype, bd=0, bg=self.Achtergrondkleur, command=action)
            foo.grid(row=posrow, column=poscol)
            foo.bind("<Button-3>",lambda event, x = producten[i]: self.nu_gestreept(x,-1))
            if posrow==4:
                posrow=2
                poscol+=1
            else:
                posrow+=1
        self.bind("b",lambda event, x="Bier":self.nu_gestreept(x))
        self.bind("f",lambda event, x="Fris":self.nu_gestreept(x))
        self.bind("t",lambda event, x="Tosti":self.nu_gestreept(x))
        self.bind("s",lambda event, x="Snoep":self.nu_gestreept(x))
        self.bind("k",lambda event, x="Koek":self.nu_gestreept(x))
        self.bind("c",lambda event, x="Chips":self.nu_gestreept(x))
        self.bind("B",lambda event, x="Bier":self.nu_gestreept(x,-1))
        self.bind("F",lambda event, x="Fris":self.nu_gestreept(x,-1))
        self.bind("T",lambda event, x="Tosti":self.nu_gestreept(x,-1))
        self.bind("S",lambda event, x="Snoep":self.nu_gestreept(x,-1))
        self.bind("K",lambda event, x="Koek":self.nu_gestreept(x,-1))
        self.bind("C",lambda event, x="Chips":self.nu_gestreept(x,-1))
    
    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.tekst_naam.delete(0.0, tk.END)
        self.tekst_al_gestreept.delete(0.0, tk.END)
        self.tekst_nu_gestreept.delete(0.0, tk.END)
        self.gestreept = dict.fromkeys(self.gestreept,0)
        self.tekst_naam.insert(0.0, "\nHoi "+root.gebruiker+"!")
        self.tekst_naam.tag_add("center", 0.0, "end")
        al_gestreept = "\n\nHuidige aantal consumpties:\n\n"
        for lid in leden:
            if lid.naam == root.gebruiker:
                for i in range(len(producten)):
                    if lid.aantal[i] > 0:
                        al_gestreept += producten[i]+": \t%.0f\t%s %.2f \n" %(lid.aantal[i],self.euro,lid.aantal[i]*prijzen[i])
                self.tekst_al_gestreept.insert(0.0, al_gestreept+"_______________________\nHuidig saldo \t\t%s %.2f" %(self.euro, lid.geld))
        self.focus_set()
        
    def doe_aankoop(self):
        for lid in leden:
            if lid.naam == root.gebruiker:
                lid.geld += self.additief_saldo
                for i in range(len(producten)):
                    lid.aantal[i] += self.gestreept[producten[i]]
                    self.gestreept[producten[i]]=0
        root.show_frame(LoginScherm)
        
    def nu_gestreept(self, artikel, quantity=1):
        self.gestreept[artikel]+=quantity
        if self.gestreept[artikel] < 0: self.gestreept[artikel] = 0
        self.tekst_nu_gestreept.delete(0.0, tk.END)
        self.additief_saldo=0
        nu_gestreept = "Nieuwe consumpties\n\n"
        for i in range(len(producten)):
            if self.gestreept[producten[i]] > 0:
                nu_gestreept += producten[i]+": \t%.0f\t%s %.2f \n" %(self.gestreept[producten[i]],self.euro,self.gestreept[producten[i]]*prijzen[i])
                self.additief_saldo += self.gestreept[producten[i]]*prijzen[i]
        for lid in leden:
            if lid.naam == root.gebruiker:
                nu_gestreept += "_______________________\nAdditief saldo \t\t%s %.2f\n\n_______________________\nNieuw saldo \t\t%s %.2f" %(self.euro, self.additief_saldo, self.euro, lid.geld+self.additief_saldo)
        self.tekst_nu_gestreept.insert(0.0, nu_gestreept)
        
    def maak_wachtwoord(self):
        self.nieuwwachtwoord1 = tk.StringVar()
        self.nieuwwachtwoord2 = tk.StringVar()
        self.oudwachtwoord2 = tk.StringVar()
        self.oudwachtwoord = '0'
        for lid in leden:
            if lid.naam == root.gebruiker:
                self.oudwachtwoord = lid.wachtwoord
                
        if  not self.oudwachtwoord== '0':
            self.makewachtwoord = tk.Toplevel()
            #Kijken of de gebruiker het huidige wachtwoord weet
            tk.Label(self.makewachtwoord,text="Huidig wachtwoord").grid(row=0,column=0)
            tk.Label(self.makewachtwoord,text="Nieuw wachtwoord").grid(row=1,column=0)
            tk.Label(self.makewachtwoord,text="Herhaal nieuw wachtwoord").grid(row=2,column=0)
            tk.Entry(self.makewachtwoord, text="Huidig wachtwoord", show="*", textvariable = self.oudwachtwoord2).grid(row=0,column=1)
            tk.Entry(self.makewachtwoord, text="Nieuw wachtwoord", show="*", textvariable = self.nieuwwachtwoord1).grid(row=1,column=1)
            tk.Entry(self.makewachtwoord, text="Herhaal nieuw wachtwoord", show="*", textvariable = self.nieuwwachtwoord2).grid(row=2,column=1)
            tk.Button(self.makewachtwoord,text = "Annuleren", command = self.makewachtwoord.destroy).grid(row=3,column=0)
            tk.Button(self.makewachtwoord,text = "Ok", command = self.maak_wachtwoord1).grid(row=3,column=1)
        else:
            self.makewachtwoord = tk.Toplevel()
            #Kijken of de gebruiker het huidige wachtwoord weet
            tk.Label(self.makewachtwoord,text="Nieuw wachtwoord").grid(row=0,column=0)
            tk.Label(self.makewachtwoord,text="Herhaal nieuw wachtwoord").grid(row=1,column=0)
            tk.Entry(self.makewachtwoord, text="Nieuw wachtwoord", show="*", textvariable = self.nieuwwachtwoord1).grid(row=0,column=1)
            tk.Entry(self.makewachtwoord, text="Herhaal nieuw wachtwoord", show="*", textvariable = self.nieuwwachtwoord2).grid(row=1,column=1)
            tk.Button(self.makewachtwoord,text = "Annuleren", command = self.makewachtwoord.destroy).grid(row=2,column=0)
            tk.Button(self.makewachtwoord,text = "Ok", command = self.maak_wachtwoord1).grid(row=2,column=1) 
            
    def maak_wachtwoord1(self):
        self.nieuwwachtwoord1 = h.sha224(self.nieuwwachtwoord1.get())
        self.nieuwwachtwoord1 = self.nieuwwachtwoord1.digest()
        self.nieuwwachtwoord2 = h.sha224(self.nieuwwachtwoord2.get())
        self.nieuwwachtwoord2 = self.nieuwwachtwoord2.digest()
        if not self.oudwachtwoord == '0':
            self.oudwachtwoord2 = h.sha224(self.oudwachtwoord2.get())
            self.oudwachtwoord2 = self.oudwachtwoord2.digest()
            if not self.oudwachtwoord == self.oudwachtwoord2:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
            elif self.nieuwwachtwoord1 == self.nieuwwachtwoord2:
                for lid in leden:
                    if lid.naam == root.gebruiker:
                        lid.wachtwoord = self.nieuwwachtwoord1
                tkMessageBox.showwarning("Voltooid", "Uw wachtwoord is veranderd!")
            else:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
        else: 
            if self.nieuwwachtwoord1 == self.nieuwwachtwoord2:
                for lid in leden:
                    if lid.naam == root.gebruiker:
                        lid.wachtwoord = self.nieuwwachtwoord1
                        
                tkMessageBox.showwarning("Voltooid", "Uw wachtwoord is veranderd!")
            else:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
                
        self.makewachtwoord.destroy()                          
                
                
class AdminScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "deep sky blue"
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)

    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        pass
        
class Lid():
    def __init__(self, naam, aantallen, geld, geboortedatum, wachtwoord):
        self.voornaam = naam.split()[0]
        self.achternaam = ' '.join(naam.split()[1:])
        self.naam = str(naam)
        self.aantal=map(int,aantallen)
        self.geld = float(geld)
        self.geboortedatum = geboortedatum
        self.wachtwoord = str(wachtwoord)


    
def check_minderjarig(row):
    lid = row[-2].split("-")
    dag = int(lid[0])
    maand = int(lid[1])
    jaar = int(lid[2])
    nu_jaar = int(time.strftime("%Y"))
    nu_maand = int(time.strftime("%m"))
    nu_dag = int(time.strftime("%d"))
    meerderjarig = False
    if (jaar+18) > nu_jaar:
        meerderjarig = True
    if (jaar+18) == nu_jaar:
        if maand > nu_maand:
            meerderjarig = True
        elif maand == nu_maand:
            if dag > nu_dag:
                meerderjarig = True
    return meerderjarig

maandlijstbestand = 'Streeplijst_'+time.strftime("%Y-%m")+'.csv'

# Als de lijst van deze maand nog niet bestaat, maak deze dan aan
if not os.path.isfile(maandlijstbestand):
    shutil.copyfile('Streeplijst_0000-00.csv', maandlijstbestand)

with open(maandlijstbestand, 'rb') as csvfile:
    file_now = csv.reader(csvfile, delimiter = ';')
    leden = []
    minderjarigen = []
    voornamen = []
    for row in file_now:
        if row[0] != 'Prijs' and row[0] != 'Naam' and row[0] != 'Totaal' and row[0]!='Omzet' and row[0]!="Voorraad":
            lid = Lid(row[0], row[1:-3], row[-3], row[-2], row[-1])
            leden.append(lid)
            voornamen.append(lid.voornaam)
            if check_minderjarig(row):
                minderjarigen.append(row[0])
        elif row[0] == 'Naam':
            producten=row[1:-3]
        elif row[0] == 'Prijs':
            prijzen=map(float,row[1:-3])
    
    root = MainApplication()
    root.mainloop()
    
    
    with open(maandlijstbestand+'temp', 'wb') as csvfile2:
        totaal = [0] * (len(producten)+1)
        omzet = [0] * (len(producten)+1)
        file_now2 = csv.writer(csvfile2, delimiter = ';')
        file_now2.writerow(['Prijs'] + prijzen + ['','',''])
        file_now2.writerow(['Naam'] + producten + ['Geld', 'Geboortedatum','Wachtwoord'])    
        for lid in leden:
            volled_naam = "%s %s" %(lid.voornaam, lid.achternaam)
            file_now2.writerow([volled_naam] + lid.aantal + [lid.geld, lid.geboortedatum,lid.wachtwoord])
            for i in range(len(producten)):
                totaal[i] += lid.aantal[i]
            totaal[-1] += round(lid.geld,2)
        file_now2.writerow(['Totaal'] + totaal + ['',''])
        for i in range(len(producten)):
            omzet[i] = round(totaal[i]*prijzen[i],2)
        omzet[-1] = round(sum(omzet[:-1]),2)
        file_now2.writerow(['Omzet'] + omzet + ['',''])
    
shutil.copyfile(maandlijstbestand+'temp', maandlijstbestand)
os.remove(maandlijstbestand+'temp')
                
