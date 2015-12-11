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

VERSIE = "December 2015, beta"
WACHTWOORD = "Wachtwoord"
lettertype = ("Calibri, 15")
debuggen = True

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

        for F in (LoginScherm, StreepScherm, AdminScherm, GebruikerScherm):

            self.frames[F] = F(self)
            self.frames[F].grid(row=0, column=0, sticky="nsew")

        self.frames[LoginScherm].tkraise()
                
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
        
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=25)
        if debuggen: tk.Label(self, text='DEBUGGEN', font='Calibri, 24').pack()
        
        # Invoer van eigen naam
        tk.Label(self, text='Voornaam', font=lettertype, bg=self.Achtergrondkleur).pack()
        self.naam = tk.Entry(self, justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.naam.pack(side="top", ipady=10)
        self.naam.bind("<Return>", self.check_name)
        
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=10)
        tk.Label(self, text='Wachtwoord', font=lettertype, bg=self.Achtergrondkleur).pack()
        self.wachtwoord = tk.Entry(self, show="*", justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.wachtwoord.pack(side="top", ipady=10)
        self.wachtwoord.bind("<Return>", self.check_name)
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=10)
        # Informatie ruimte
        self.response = tk.Text(self, font="Calibri, 16", bd=0, width=25, height=4, bg=self.Achtergrondkleur, wrap=tk.WORD)
        self.response.tag_configure("center", justify='center')
        self.response.pack()
        
        # Mens-logo
        self.menslogo = ImageTk.PhotoImage(Image.open('Images\\menslogo.png'))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= self.menslogo)
        self.backlabel.image = self.menslogo
        self.backlabel.pack(pady=50)
        
        self.naam.focus()
        
    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.response.delete(1.0,tk.END)
        self.naam.delete(0, tk.END)
        self.wachtwoord.delete(0, tk.END)
        self.naam.focus()
        
    def check_name(self, event):
        self.first_name = self.naam.get().title().strip()
        self.response.configure(bg=self.Achtergrondkleur, fg="black")
        if voornamen.count(self.first_name) == 0:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "\nNaam onbekend, probeer opnieuw.")
            self.response.tag_add("center", 1.0, "end")
            self.response.configure(background = "red4", fg = "snow")            
        elif voornamen.count(self.first_name) == 1:
            for lid in leden:
                if lid.voornaam == self.first_name:
                    root.gebruiker = lid
            self.have_password()
        else:
            self.response.delete(1.0,tk.END)
            self.response.insert(1.0, "Kies uw naam")
            self.response.tag_add("center", 1.0, "end")
            self.backlabel.destroy()
            self.nu_rij = []
            self.btn_dict = {}
            for lid in leden:
                if lid.voornaam == self.first_name:
                    self.nu_rij.append(lid.naam)
            self.nu_rij.append('Annuleren')
            for person in self.nu_rij:
                action = lambda x = person: self.reg_naam(x)
                self.btn_dict[person] = tk.Button(self, width = 40, text = person, font="Calibri, 16", \
                                            command = action, bg = self.Achtergrondkleur, activebackground="yellow2")
                self.btn_dict[person].pack(pady=10)

    def have_password(self):
        if not root.gebruiker.wachtwoord:
            root.show_frame(StreepScherm)
        else:
            self.insertedww = h.sha224(self.wachtwoord.get())
            self.insertedww = self.insertedww.digest()
            if self.insertedww == root.gebruiker.wachtwoord:
                root.show_frame(StreepScherm)
            else:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
    
    def reg_naam(self,vol_naam):
        if not vol_naam == 'Annuleren':
            for lid in leden:
                    if lid.naam == vol_naam:
                        root.gebruiker = lid
            self.have_password()
        for person in self.nu_rij:
            self.btn_dict[person].destroy()
        # Mens-logo
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= self.menslogo)
        self.backlabel.image = self.menslogo
        self.backlabel.pack(pady=50)
        
class StreepScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "yellow"
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)
        self.images = {}
        self.gestreept = {}
        for product in producten:
            if os.path.isfile('Images\\'+product+'.png'):
                self.images[product] = ImageTk.PhotoImage(Image.open('Images\\'+product+'.png'))
            else:
                self.images[product] = ImageTk.PhotoImage(Image.open('Images\\NoPicture.png'))
            self.gestreept[product] = 0
        
        self.left_frame = tk.Frame(self, bg=self.Achtergrondkleur)
        self.right_frame = tk.Frame(self, bg=self.Achtergrondkleur)
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame.pack(side="right", fill="both", expand=False, padx=20)
        
        for x in range(5):
            self.left_frame.grid_columnconfigure(x, weight=1)
        
        for y in range(5):
            self.left_frame.grid_rowconfigure(y, weight=1)
        
        action = lambda: root.show_frame(LoginScherm)
        tk.Button(self.left_frame, text = "Terug", bg = 'white', command = action, font=lettertype).grid(row = 1, column = 1, sticky="nsew")
        action = lambda: root.show_frame(GebruikerScherm)
        self.wachtwoordknop = tk.Button(self.left_frame, bg = 'white', command = action, font=lettertype)
        self.wachtwoordknop.grid(row = 1, column = 3, sticky="nsew")
        self.tekst_naam = tk.Text(self.right_frame, width=23, height = 2, bg=self.Achtergrondkleur, bd=0, font=lettertype)
        self.tekst_naam.tag_configure("center", justify='center')
        self.tekst_naam.pack(side="top", pady=20)
        self.tekst_al_gestreept = tk.Text(self.right_frame, width=23, height=len(producten)+7, bd=0, bg=self.Achtergrondkleur, font=lettertype)
        self.tekst_al_gestreept.pack(side="top")
        self.tekst_nu_gestreept = tk.Text(self.right_frame, width=23, height=len(producten)+7, bd=0, bg=self.Achtergrondkleur, font=lettertype)
        self.tekst_nu_gestreept.pack(side="top")
        action = lambda: self.doe_aankoop()
        tk.Button(self.right_frame, text = "Doe aankoop", bg = 'white', command = action, font=lettertype).pack(side="bottom", ipady=20, ipadx=40, padx=100, pady=50)
        
        
        self.euro = u"\u20AC"
        self.a = u"\u00E0"
                
        posrow=2; poscol=1
        self.knoppen = {}
        for i in range(len(producten)):
            action = lambda x = producten[i]: self.nu_gestreept(x)
            self.knoppen[producten[i]]=tk.Button(self.left_frame, image=self.images[producten[i]], text="%s %s %s %.2f" %(producten[i], self.a, self.euro, prijzen[i]), compound="top", font=lettertype, bd=0, bg=self.Achtergrondkleur, command=action)
            self.knoppen[producten[i]].grid(row=posrow, column=poscol)
            self.knoppen[producten[i]].bind("<Button-3>",lambda event, x = producten[i]: self.nu_gestreept(x,-1))
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
        self.additief_saldo=0
        self.gestreept = dict.fromkeys(self.gestreept,0)
        if root.gebruiker.minderjarig:
            self.knoppen['Bier'].config(state=tk.DISABLED)
            self.knoppen['Wijn'].config(state=tk.DISABLED)
            self.knoppen['Sterk'].config(state=tk.DISABLED)
            self.unbind('b');
        else:
            self.knoppen['Bier'].config(state=tk.NORMAL)
            self.knoppen['Wijn'].config(state=tk.NORMAL)
            self.knoppen['Sterk'].config(state=tk.NORMAL)
            self.bind("b",lambda event, x="Bier":self.nu_gestreept(x))
        if root.gebruiker.wachtwoord: self.wachtwoordknop.config(text = "Maak nieuw wachtwoord")
        else: self.wachtwoordknop.config(text = "Stel wachtwoord in")
        self.tekst_naam.insert(0.0, "\nHoi "+root.gebruiker.voornaam+"!")
        self.tekst_naam.tag_add("center", 0.0, "end")
        al_gestreept = "\n\nHuidige aantal consumpties:\n\n"
        for i in range(len(producten)):
            if root.gebruiker.aantal[i] > 0:
                al_gestreept += producten[i]+": \t%.0f\t%s %.2f \n" %(root.gebruiker.aantal[i],self.euro,root.gebruiker.aantal[i]*prijzen[i])
        self.tekst_al_gestreept.insert(0.0, al_gestreept+"_______________________\nHuidig saldo \t\t%s %.2f" %(self.euro, root.gebruiker.geld))
        self.focus_set()
        
    def doe_aankoop(self):
        if not self.additief_saldo==0:
            for lid in leden:
                if lid.naam == root.gebruiker.naam:
                    lid.geld += self.additief_saldo
                    for i in range(len(producten)):
                        lid.aantal[i] += self.gestreept[producten[i]]
                        self.gestreept[producten[i]]=0
            write_file()
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
        nu_gestreept += "_______________________\nAdditief saldo \t\t%s %.2f\n\n_______________________\nNieuw saldo \t\t%s %.2f" %(self.euro, self.additief_saldo, self.euro, root.gebruiker.geld+self.additief_saldo)
        self.tekst_nu_gestreept.insert(0.0, nu_gestreept)
                
class AdminScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "deep sky blue"
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)

    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        pass
    
class GebruikerScherm(tk.Frame):

    def __init__(self, parent):
        self.Achtergrondkleur = "deep sky blue"
        tk.Frame.__init__(self,parent,bg=self.Achtergrondkleur)
          
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=20)
        self.wachtwoordlabel = tk.Label(self, text = 'Huidig wachtwoord', bg = self.Achtergrondkleur, font=lettertype, disabledforeground=self.Achtergrondkleur)
        self.wachtwoordlabel.pack()
        self.wachtwoord = tk.Entry(self, show="*", justify=tk.CENTER, font="Calibri, 20", bd=0, disabledbackground=self.Achtergrondkleur)
        self.wachtwoord.pack()
        self.wachtwoord.bind("<Return>", self.maak_wachtwoord)
        
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=10)
        tk.Label(self, text = 'Nieuw wachtwoord', bg = self.Achtergrondkleur, font=lettertype).pack()
        self.nieuwwachtwoord1 = tk.Entry(self, show="*", justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.nieuwwachtwoord1.pack()
        self.nieuwwachtwoord1.bind("<Return>", self.maak_wachtwoord)
         
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=10)
        tk.Label(self, text = 'Herhaal nieuw wachtwoord', bg = self.Achtergrondkleur, font=lettertype).pack()
        self.nieuwwachtwoord2 = tk.Entry(self, show="*", justify=tk.CENTER, font="Calibri, 20", bd=0)
        self.nieuwwachtwoord2.pack()
        self.nieuwwachtwoord2.bind("<Return>", self.maak_wachtwoord)
        
        tk.Label(self, bg = self.Achtergrondkleur).pack(ipady=10)
        self.buttons = tk.Frame(self, height=100, width=300, bd=0, bg=self.Achtergrondkleur)
        self.buttons.pack(padx=5, pady=5)
        action = lambda: self.maak_wachtwoord()
        tk.Button(self.buttons, text='OK', width=15, font=lettertype, command=action).pack(side='left')
        action = lambda: root.frames[StreepScherm].tkraise()
        tk.Button(self.buttons, text='Annuleren', width=15, font=lettertype, command=action).pack(side='right')
        
        # Informatie ruimte
        self.response = tk.Text(self, font="Calibri, 16", bd=0, width=25, height=4, bg=self.Achtergrondkleur, wrap=tk.WORD)
        self.response.tag_configure("center", justify='center')
        self.response.pack(pady=10)
         
        # Mens-logo
        self.menslogo = ImageTk.PhotoImage(Image.open('Images\\menslogo.png'))
        self.backlabel = tk.Label(self, bg=self.Achtergrondkleur, image= self.menslogo)
        self.backlabel.image = self.menslogo
        self.backlabel.pack()

    def voorbereiding(self):
        # Deze functie wordt opgeroepen voor het frame naar voren wordt gebracht.
        self.wachtwoord.config(state=tk.NORMAL)
        self.wachtwoord.delete(0, tk.END)
        if not root.gebruiker.wachtwoord:
            self.wachtwoord.config(state=tk.DISABLED); self.wachtwoordlabel.config(state=tk.DISABLED)
            
        else:
            self.wachtwoord.config(state=tk.NORMAL); self.wachtwoordlabel.config(state=tk.NORMAL)
            
        self.nieuwwachtwoord1.delete(0, tk.END)
        self.nieuwwachtwoord2.delete(0, tk.END)
            
    def maak_wachtwoord(self, event=None):
        if root.gebruiker.wachtwoord:
            self.oudwachtwoord = h.sha224(self.wachtwoord.get())
            self.oudwachtwoord = self.oudwachtwoord.digest()
            if not root.gebruiker.wachtwoord == self.oudwachtwoord:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "Het ingevoerde wachtwoord is incorrect!")
                return
            if not (self.nieuwwachtwoord1.get() and self.nieuwwachtwoord2.get()):
                for lid in leden:
                    if lid.naam == root.gebruiker.naam:
                        lid.wachtwoord = ""
                        root.gebruiker.wachtwoord = lid.wachtwoord
                tkMessageBox.showwarning("Voltooid", "Uw wachtwoord is verwijderd!")
                root.show_frame(StreepScherm)
        if self.nieuwwachtwoord1.get() or self.nieuwwachtwoord2.get():
            if self.nieuwwachtwoord1.get() == self.nieuwwachtwoord2.get():
                self.nieuwwachtwoord = h.sha224(self.nieuwwachtwoord1.get())
                self.nieuwwachtwoord = self.nieuwwachtwoord.digest()
                for lid in leden:
                    if lid.naam == root.gebruiker.naam:
                        lid.wachtwoord = self.nieuwwachtwoord
                        root.gebruiker.wachtwoord = lid.wachtwoord
                tkMessageBox.showwarning("Voltooid", "Uw wachtwoord is veranderd!")
                root.show_frame(StreepScherm)
            else:
                tkMessageBox.showwarning("Verkeerd wachtwoord", "De ingevoerde wachtwoorden komen niet overeen!")

class Lid():
    def __init__(self, naam, aantallen, geld, geboortedatum, wachtwoord):
        self.voornaam = naam.split()[0]
        self.achternaam = ' '.join(naam.split()[1:])
        self.naam = str(naam)
        self.aantal=map(int,aantallen)
        self.geld = float(geld)
        self.geboortedatum = geboortedatum
        self.minderjarig = self.check_minderjarig(geboortedatum)
        self.wachtwoord = str(wachtwoord)
    
    def check_minderjarig(self, geboortedatum):
        minderjarig = True
        lid = geboortedatum.split("-")
        dag = int(lid[0])
        maand = int(lid[1])
        jaar = int(lid[2])
        nu_jaar = int(time.strftime("%Y"))
        nu_maand = int(time.strftime("%m"))
        nu_dag = int(time.strftime("%d"))
        if (jaar+18) < nu_jaar:
            minderjarig = False
        elif (jaar+18) == nu_jaar:
            if maand < nu_maand:
                minderjarig = False
            elif maand == nu_maand:
                if dag < nu_dag:
                    minderjarig = False
        return minderjarig

def write_file():    
    with open(maandlijstbestand+'temp', 'wb') as csvfile2:
        totaal = [0] * (len(producten)+1)
        omzet = [0] * (len(producten)+1)
        file_now2 = csv.writer(csvfile2, delimiter = ';')
        file_now2.writerow(['Prijs'] + prijzen + ['','',''])
        file_now2.writerow(['Naam'] + producten + ['Geld', 'Geboortedatum','Wachtwoord'])    
        for lid in leden:
            file_now2.writerow([lid.naam] + lid.aantal + [lid.geld, lid.geboortedatum,lid.wachtwoord])
            if lid.naam[-5:] != 'jaars':
                for i in range(len(producten)):
                    totaal[i] += lid.aantal[i]
                totaal[-1] += round(lid.geld,2)
        file_now2.writerow(['Totaal'] + totaal + ['',''])
        for i in range(len(producten)):
            omzet[i] = round(totaal[i]*prijzen[i],2)
        omzet[-1] = round(sum(omzet[:-1]),2)
        file_now2.writerow(['Omzet'] + omzet + ['',''])
    
    with open('Streeplijst_0000-00temp.csv', 'wb') as csvfile3:
        totaal2 = [0] * (len(producten)+1)
        file_now3 = csv.writer(csvfile3, delimiter = ';')
        file_now3.writerow(['Prijs'] + prijzen + ['','',''])
        file_now3.writerow(['Naam'] + producten + ['Geld', 'Geboortedatum','Wachtwoord'])    
        for lid in leden:
            if lid.naam[-5:] == 'jaars':
                file_now3.writerow([lid.naam]+lid.aantal+ [lid.geld,lid.geboortedatum,lid.wachtwoord])
            else:
                file_now3.writerow([lid.naam]+totaal2+ [lid.geboortedatum,lid.wachtwoord])
        file_now3.writerow(['Totaal'] + totaal2 + ['',''])
        file_now3.writerow(['Omzet'] + totaal2 + ['',''])

maandlijstbestand = 'Streeplijst_'+time.strftime("%Y-%m")+'.csv'

# # Geeft foutmelding als er al programma is geopend, waarmee gestreepd is.
# if os.path.isfile('Streeplijst_0000-00temp.csv'):
#     tkMessageBox.showwarning("Foutmelding","Programma is al geopend!")
    
# Als de lijst van deze maand nog niet bestaat, maak deze dan aan; en check of er een temp-bestand is en gebruikt deze in dat geval voor het inlezen. 
if os.path.isfile(maandlijstbestand+'temp'):
    maandlijstbestand=maandlijstbestand+'temp'
if not os.path.isfile(maandlijstbestand):
    if os.path.isfile('Streeplijst_0000-00temp.csv'):
        shutil.copyfile('Streeplijst_0000-00temp.csv', maandlijstbestand)
    else:
        shutil.copyfile('Streeplijst_0000-00.csv', maandlijstbestand)
    
with open(maandlijstbestand, 'rb') as csvfile:
    if maandlijstbestand[-4:]=='temp': maandlijstbestand=maandlijstbestand[:-4]
    file_now = csv.reader(csvfile, delimiter = ';')
    leden = []
    minderjarigen = []
    voornamen = []
    for row in file_now:
        if row[0] != 'Prijs' and row[0] != 'Naam' and row[0] != 'Totaal' and row[0]!='Omzet' and row[0]!="Voorraad" and row[0][-5:]!='jaars':
            lid = Lid(row[0], row[1:-3], row[-3], row[-2], row[-1])
            leden.append(lid)
            voornamen.append(lid.voornaam)
        elif row[0][-5:] == 'jaars':
            jaars = lambda:0 # To create an empty instance
            jaars.voornaam = ""
            jaars.naam = row[0]
            jaars.aantal= row[1:-3]
            jaars.geld = row[-3]
            jaars.geboortedatum = row[-2]
            jaars.wachtwoord = row[-1]
            leden.append(jaars)
        elif row[0] == 'Naam':
            producten=row[1:-3]
        elif row[0] == 'Prijs':
            prijzen=map(float,row[1:-3])
    
    root = MainApplication()
    root.mainloop()
    
    write_file()
    
shutil.copyfile(maandlijstbestand+'temp', maandlijstbestand)
os.remove(maandlijstbestand+'temp')
shutil.copyfile('Streeplijst_0000-00temp.csv','Streeplijst_0000-00.csv')
os.remove('Streeplijst_0000-00temp.csv')
