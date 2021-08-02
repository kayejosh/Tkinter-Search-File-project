"""
Projet: GUI pour la recherche des fichiers avec le module tkinter
Periode: 20 Juillet au 03 Aout 2021
Equipe 3: Banzouzi Neldy, Diba de Palmes Emmanuel, Lounguela Kaya,
            Makenzo Souvenance, Makoundou Alrvaro, Metowanou Ruth ,Ngambou Clesh
Superviseur: Mr Marc Mfoutou Moukala

Unisersité Marien Ngouabi
Licence 2 Informatique

"""

# Importation des bibliothèques
from tkinter import*
import tkinter as tk
from PIL import ImageTk, Image # pour la gestion des images
from tkinter import ttk
from tkinter import filedialog # pour parcourir les repertoires en mode graphique
import os
import glob
import Levenshtein as lv     # pour evaluer la  distance entre deux mots
import PyPDF2                # pour lire les fichiers pdf
from docx import Document    # pour lire les fichiers docx
from tkinter import messagebox # pour afficher des messages sur un popup
from pathlib import Path       # pour obtenir le home

try:
    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Creation de la fenetre et des pages<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    app = tk.Tk()
    app.columnconfigure(0,weight=1)
    app.rowconfigure(0,weight=1)
    app.geometry('800x600')
    app.resizable(False, False)

    page0 = tk.Frame(app)        #Page de connexion
    page1 = tk.Frame(app)        #Page d'entree du chemin de recherche
    page2 = tk.Frame(app)      #Page de recherche
    for page in (page2,page1,page0):
        page.grid(row=0,column=0,sticky='nsew')   # placer les pages sur la fenetre
        # definition des fonctions


    def switchPage(window, page, title):  # fonction pour rafraichir le contenu de la fenetre  declenche
        # par les boutons demarrer, valider et quitter
        global choice
        status = choice.get()
        if status == choices[0]:
            page.tkraise()
            refreshTitle(window, title)
        else:
            messagebox.showinfo('Info', 'La recherche sur ordinateur distant n\'est pas encore pris en charge\n.'
                                        'Revenez plutard!')


    def refreshTitle(window, title):  # fonction pour changer le titre de la fenetre
        window.title(title)


    def resize(window, height):  # fonction pour changer la taille de la fenetre , utiliser
        # au passage de la page1 a la page2
        window.geometry(f'800x{height}')


    def getDir(status):  # fonction pour recuperer le chemin d'un repertoire
        global app
        global pattern_entry, search_label
        global directory_entry
        global text_box1
        global fileSortedList
        pattern = pattern_entry.get()  # on recupere le motif
        directory_entry.delete(0, '')
        text_box1.delete(0, len(text_box1.get(0)))

        if btn1.get() == 0:  # on verifie si l'utilisateur selectionne oui
            app.filename = filedialog.askdirectory()  # il selectionne le repertoire qu'il souhaite
            directory_entry.insert(0, app.filename)
            path = directory_entry.get()

            return path
        elif btn1.get() == 1:  # si l'utilisateur selectionne non on recherche dans le home
            directory_entry.insert(0, Path.home())


    def searchResults():  # fonction pour afficher le resultat de la recherche
        try:
            global search_label, directory_entry
            global pattern_entry
            text_box1.delete(0, len(text_box1.get(0)))
            fileSortedList = []
            fileList = []
            path = directory_entry.get()
            pattern = pattern_entry.get().lower()
            status = search_label.get()  # on recupere l'option de recherche
            if status == search_choices[1]:  # si l'utilisateur selectionne la premiere option
                os.chdir(path)
                # print(os.getcwd())
                fileSortedList = []
                for file in glob.glob(
                        '*'.lower() + pattern + '*'.lower()):  # on recherche le motif dans le nom des fichiers
                    fileSortedList.append(file)
                i = 1
                # print(status, pattern)
                fileSortedList = sortList(pattern, fileSortedList)  # on classe les fichiers par pertinence
                i = 1
                text_box1.insert(0, ' N                  Fichiers           ')  # on affiche les resultats
                for file in fileSortedList:
                    text_box1.insert(f'{i}', f'{int(i)}.{file}')
                    i += 1

            elif status == search_choices[0]:  # si l'utilisateur selectionne la deuxieme option de recherche
                os.chdir(path)
                fileList = list_files(path)
                content = [str(i) for i in range(len(fileList))]
                i = 1
                for i in range(len(fileList)):
                    with open(path + '/' + fileList[i], 'r+',
                              encoding='utf-8') as f:  # on cherche le motif dans le fichier
                        content[i - 1] = str(f.readlines())
                content.sort(reverse=True, key=myFunc)
                text_box1.insert(0, ' N                  Fichiers           ')
                i = 1
                for file in fileList:
                    text_box1.insert(f'{i}', f'{int(i)}.{file} (occurences={content[i - 1].count(pattern)})')
                    i += 1
                # gestion des erreurs recurrentes lors de la recherche dans des fichiers non pris en charge
        except UnicodeDecodeError:
            messagebox.showerror('Erreur', 'Ce dossier contient un format de fichier non pris en charge.')
        except FileNotFoundError:
            messagebox.showinfo('Info', 'Repertoire ou fichier non trouvé.'
                                        'Essayez un autre nom !')


    def list_files(path):  # fonction pour lister les fichiers cf. cours exercice 1
        for root, dir, file in os.walk(path):
            return file


    def cancel():  # fonction pour rafraichir les entrees/sorties de texte declenche par le
        # bouton annuler
        global text_box1
        global pattern_entry, directory_entry
        text_box1.delete(0, len(text_box1.get(0)))
        text_box2.delete('1.0', END)
        pattern_entry.delete(0, len(pattern_entry.get()))
        directory_entry.delete(0, len(directory_entry.get()))


    def sortList(myWord, myList):  # fonction pour classer les fichiers par pertinence

        myList.sort(key=myFunc2)
        return myList


    def getElement(event):  # fonction pour selectionner un fichier dans les
        # resultats de la recherche
        selection = event.widget.curselection()
        index = selection[0]
        value = event.widget.get(index)
        openFile(value)


    def openFile(file):  # fonction pour afficher le contenu d'un fichier (imcomplete)
        text_box2.delete('1.0', END)

        tf = filedialog.askopenfilename(initialdir=os.getcwd() + '/' + file, title='Ouvrir le fichier',
                                        filetypes=(('Text Files', '*txt'),
                                                   ('Python Files', '*.py'), ('Pdf files', '.pdf'),
                                                   ('Docx Files', '*.docx'),
                                                   ('Csv Files', '*.csv'), ('Nontype File', '***')), )
        # path.insert(END, tf)
        if os.path.splitext(tf)[1] == '.pdf':  # si le fichier est un pdf
            read_pdf = PyPDF2.PdfFileReader(tf)
            pages = read_pdf.getPage(2)
            pages_content = pages.extractText()
            text_box2.insert(2.0, pages_content)
        elif os.path.splitext(tf)[1] == '.docx':  # si le fichier est docx
            print('in the function')
            read_docx = Document(tf)
            print(read_docx)
            pages = []
            for p in read_docx.paragraphs:
                pages.append(p.text)
            text_box2.insert(2.0, pages)
        else:  # pour les autres fichiers
            tf = open(tf, encoding='utf-8')
            data = tf.read()
            text_box2.insert(2.0, data)
            tf.close()


    def myFunc(e):  # fonction pour classer par par rapport
        # au nombre d'occurences du motif
        pattern = pattern_entry.get()
        print(e.count(pattern))
        return e.count(pattern)


    def myFunc2(e):  # fonction pour classer par rapport a la distance entre deux mots
        myword = pattern_entry.get()
        return lv.distance(e, myword)


    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Edition de la page de connexion<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # importer et editer les images
    img = Image.open("images/file.png")
    img = img.resize((350, 350))
    tkimage = ImageTk.PhotoImage(img)
    image = tk.Label(page0, image=tkimage)
    image.place(x=250, y=90)
    # creation des  labels
    firstLabel = tk.Label(page0, text='Bienvenue sur notre plateforme de recherche de fichiers |',
                       fg='RoyalBlue2',  width=100, font=10)
    secondLabel = tk.Label(page0, text='Pour vous connecter, veuillez cliquer sur le bouton Démarrer ci-dessous',
                    bg='purple', width=200*app.winfo_width(), fg='white', font=10, height=2)
    firstLabel.pack()
    secondLabel.pack()

    # elements du pied de la page
    myButton = tk.Button(page0, text='Démarrer', padx=40, pady=10,  font='bold',
                         command=lambda:switchPage(app,page1,'Application de recherche des fichiers'), bd=2, bg='mint cream')
    thirdLabel = tk.Label(page0, bg='purple', width=200*app.winfo_width(), height=2)
    job = tk.Label(page0, text='Developed by Team 3')
    contact = tk.Label(page0, text='© copyright Team3@gmail.com 2021')
    myButton.place(x=300, y=470)
    thirdLabel.place(x=0, y=565)
    job.place(x=10, y=540)
    contact.place(x=500, y=540)
    seperator1 = ttk.Separator(page0, orient=HORIZONTAL).place(relwidth=1, x=0, y=470)




    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Edition de la seconde page<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # creation des labels
    firstLabel1 = tk.Label(page1, text="Bienvenue sur notre plateforme de recherche avancée de fichiers",
                        fg='blue2', font=12).pack(pady=5)
    secondLabel1 = tk.Label(page1, text='Cette application vous permet de faire  vos recherches de fichiers\n'
                                       '\nsur votre ordinateur local ou sur un ordinateur distant selon vos besoins',
                         fg='midnight blue', font=12, pady=10).pack(pady=20)
    # creation des separateurs
    seperator2 = ttk.Separator(page1).pack(fill='x', padx=50)
    seperator3 = ttk.Separator(page1).pack(fill='x', padx=50, pady=220)

    # creation et edition d'une combobox pour le choix d'ordinateur

    choices = ["Ordinateur local", "Ordinateur distant"]
    choice = ttk.Combobox(page1, values=choices)
    choice.set(choices[0])
    choice.place(x=500, y=180)
    fourthLabel = tk.Label(page1, text="Où voulez-vous rechercher votre fichier ?",
                        fg='midnight blue', font=12).place(x=145, y=180)
    # creation des boutons
    quit = tk.Button(page1, text='Quitter', bg='white', width=10,
                     command=lambda:switchPage(app,page0,'Connexion à l\' application de recherche avancée de fichiers')).place(x=440, y=510)
    valid = tk.Button(page1, text='Valider', bg='white', width=10,
                      command=lambda:(switchPage(app,page2,'Application de recherche des fichiers sur un ordinateur local'), resize(app, 660))).place(x=270, y=510)

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Edition de la page de recherche<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

   # les labels
    firstLabel2= tk.Label(page2,
                       text="Bienvenue sur notre plateforme de recherche avancée de fichiers sur un ordinateur local",
                       fg='blue2', pady=20, font=12).pack()
    # les separateurs
    seperator4 = ttk.Separator(page2).pack(fill='x', padx=50)
    seperator5 = ttk.Separator(page2).pack(fill='x', padx=50, pady=200)


    # elements de la zone de recherche
    search_choices = ['Motif contenu dans le fichier', 'Motif contenu dans le nom du fichier']
    search_option_label = tk.Label(page2, text="Veuillez préciser votre option de recherche", fg='midnight blue').place(x=100, y=80)
    search_dir_label = tk.Label(page2, text="Connaissez-vous le repertoire du fichier cherché?", fg='midnight blue').place(x=100, y=180)
    search_label = ttk.Combobox(page2, values=search_choices, width=25)
    status = search_label.get()
    search_label.set(search_choices[0])
    search_label.place(x=520, y=80)

    pattern_entry = ttk.Entry(page2, width= 26)
    pattern_entry.place(x=520, y=115)


    search_directory = tk.Button(page2, text='Choisir le repertoire', bg='SteelBlue3', command=lambda:getDir(status)).place(x=520, y=150)
    directory_entry = ttk.Entry(page2,width=26)
    cancel = tk.Button(page2, text='Annuler', bg='white', width=10, command=cancel).place(x=450, y=270)
    validate = tk.Button(page2, text='Valider', bg='white', width=10, command=searchResults).place(x=260, y=270 )
    close = tk.Button(page2, text='Fermer', bg='SteelBlue3', width=10,
                      command=app.destroy).place(x=355, y=620)
    directory_entry.place(x=520, y=195)

    btn1 = IntVar()
    option1 = tk.Radiobutton(page2, text='oui', value=0, variable=btn1 ).place(x=450, y=180)
    option2 = tk.Radiobutton(page2, text='non', value=1, variable=btn1 ).place(x=450, y=200)




    # Edition et creation des textbox avec scrollbar

    yScroll = tk.Scrollbar(page2, orient=tk.VERTICAL)
    xScroll = tk.Scrollbar(page2, orient=tk.HORIZONTAL)

    yScroll1 = tk.Scrollbar(page2, orient=tk.VERTICAL)
    xScroll1 = tk.Scrollbar(page2, orient=tk.HORIZONTAL)



    result = tk.StringVar()
    text_box1= tk.Listbox(page2, height=15, width=30, xscrollcommand=xScroll.set, yscrollcommand=yScroll.set)
    text_box2= tk.Text(page2, height=16, width=30, xscrollcommand=xScroll1.set, yscrollcommand=yScroll1.set)
    xScroll['command'] = text_box1.xview
    yScroll['command'] = text_box1.yview
    xScroll1['command'] = text_box2.xview
    yScroll1['command'] = text_box2.yview
    text_box1_title = tk.Label(page2, text="Résultat de la recherche", fg='midnight blue').place(x=135, y=310)
    text_box2_title = tk.Label(page2, text="Contenu du fichier", fg='midnight blue').place(x=475, y=310)
    text_box2.place(x=450,y= 330)
    text_box1.place(x=120,y= 330)

    yScroll.place(x=110, y=330, height=275)
    xScroll.place(x=110, y=605, width=240)

    yScroll1.place(x=440, y=330, height=275)
    xScroll1.place(x=440, y=605, width=240)

    text_box1.bind('<<ListboxSelect>>', getElement)






    #Affichage
    switchPage(app,page0,'Connexion à l\' application de recherche avancée de fichiers')
    app.mainloop()

except:
    messagebox.showerror('Erreur',"We're sorry! The program crashed")