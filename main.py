import random
import tkinter as tk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk
import ast
import shutil
import _thread as thread

class jeu_capital():

	def __init__(self):
		"""
		inizialisation des variables self
		"""
		self.get_liste() #on recupere la liste de question sous le format suivant [[niveau1], [niveau2], [niveau3]] et [pays, capital, pronom] qui s'appellera self.jeu
		self.niveau = 0 #niveau de difficulte (0, 1, 2)
		self.dejavu_jeu = [] #liste des questions deja posees
		self.score = 0 #variable contenant le score
		self.get_record() #on recupere les records (niveau1, 2, 3)
		self.nb_essai = 1 #le nombre d'essai pour une question
		self.nb_index = False #variable qui stockera l'index de la question en cour (index de self.jeu[self.niveau])
		self.take_indice = False #variable qui permet de savoir si le joueur prend l'indice (boolen)
		self.filename = False #varible utile à la creation d'une nouvelle question et qui contient le chemin de la photo
		"""
		inizialisation des variables self
		"""
		#creation de la fenetre 
		self.fenetre = tk.Tk()
		self.fenetre.bind("<Return>", self.entree) #permet de valider la reponse lorsque la touche entree est pressee
		self.fenetre.title("Jeu Capital")
		#creation de la partie de l'ecran indice
		frame_3 = tk.LabelFrame(self.fenetre, text="Indice")
		frame_3.pack(side="bottom", fill="both", expand="yes")
		img = ImageTk.PhotoImage(Image.open("sasas.PNG")) #chargement de la photo par default (obligatoire)
		self.picture = tk.Label(frame_3, image=img) #permeterra d'afficher une photo
		self.picture.pack_forget() #fait disparaitre la photo 
		#creation de la partie de l'ecran a gauche contenant le score, le record et la molette pour choisir le niveau
		frame_score = tk.LabelFrame(self.fenetre, text="score")
		frame_score.pack(side="left", fill="y", expand=False)
		self.label_score = tk.Label(frame_score, text="Votre score : " + str(self.score)) #label qui affiche le score du joueur 
		self.label_score.pack()
		self.label_record = tk.Label(frame_score, text="Le record de niveau " + str(self.niveau) + " : " + str(self.record[self.niveau])) #label qui affiche le record du niveau choisi
		self.label_record.pack()
		tk.Label(frame_score ,text="Niveau de difficulté").pack(side="top")
		scale_niveau = tk.Scale(frame_score, from_=1, to=3, command=self.change_niveau) #creation de la molette permettant au joueur de choisir son niveau de difficulté (apelle la fonction self.change_niveau)
		scale_niveau.pack(side="left")
		#creation de la partie principale de l'ecran
		frame_question = tk.LabelFrame(self.fenetre, text="question")
		frame_question.pack(fill="both", expand="yes")
		self.label_question = tk.Label(frame_question, text="init") #label qui affiche la question posee au joueur
		self.label_question.pack()
		self.entree_question = tk.Entry(frame_question) #input pour rentrer la reponse du joueur
		self.entree_question.pack()
		self.boutton_question = tk.Button(frame_question, text="valider", command=self.verification) #boutton pour valider la reponse qui apelle la fonction self.verfification
		self.boutton_question.pack()
		self.label_result = tk.Label(frame_question, text="") #label qui affiche divers informations tels que : bonne reponse, mauvaise reponse, fin du niveau car plus de question
		self.label_result.pack()
		boutton_indice = tk.Button(frame_question, text="Un indice?", command=self.indice) #permet de choisir un indice apelle la fonction self.indice
		boutton_indice.pack()
		bouton_passer = tk.Button(frame_question, text="Passer?", command=self.passer) #boutton permettant de passer la question apelle la fonction self.passer
		bouton_passer.pack()
		#creation du menu 
		menu_bare = tk.Menu(self.fenetre)
		menu_1 = tk.Menu(menu_bare)
		menu_1.add_command(label="Les regles", command=self.rules) #permet d'ouvrir une fenetre contenant les regles apelle la fonction self.rules
		menu_1.add_command(label="add", command=self.formulaire_ajout_liste) #permet d'ouvrir une fenetre pour ajouter une question apelle la fonction self.formulaire_ajout_liste
		menu_1.add_command(label="restart", command=self.restart) #permet de recommencer apelle la fonction self.restart
		menu_1.add_command(label="reset record", command=self.reset_record) #permet de remettre à zero les records apelle la fonction self.reset_record
		menu_bare.add_cascade(label="options", menu=menu_1)
		self.fenetre.config(menu=menu_bare)
		#Thread
		thread.start_new_thread(self.main, ()) #permet de lancer le cycle du jeu en parallele à tkinter (obligatoire)
		self.fenetre.mainloop() #lance l'interface graphique
		


	def main(self):
		self.poser_question()


	def generation(self):
		"""
		choisi au hasard une nouvelle question dans le niveau choisi
		met a jour:
		self.nb_index avec l'index de la nouvelle question
		self.dejavu_jeu avec self.index (permet de ne pas reposer la meme question apres)
		"""
		self.nb_index = random.randint(0, len(self.jeu[self.niveau])-1)
		while self.nb_index in self.dejavu_jeu:
			self.nb_index = random.randint(0, len(self.jeu[self.niveau])-1)
		question = self.jeu[self.niveau][self.nb_index]
		self.dejavu_jeu.append(self.nb_index)
		return question


	def poser_question(self):
		"""
		pose une nouvelle question au joueur
		"""
		if self.nb_essai == 1: #il s'agit ici de choisir une nouvelle question en apellant self.generation et de l'afficher
			if len(self.dejavu_jeu) != len(self.jeu[self.niveau]):
				a = self.generation()
				if a[2][-1] != "'":
					self.label_question.config(text="Quelle est la capitale " + a[2] + " " + a[0] + "?", fg="black")
				else:
					self.label_question.config(text="Quelle est la capitale " + a[2] + "" + a[0] + "?", fg="black")
			else:
				self.cfini() #cas ou toute les questions du niveau int etaient posees 
		else:
			self.label_question.config(text="Quelle est la capitale " + self.jeu[self.niveau][self.nb_index][2] + " " + self.jeu[self.niveau][self.nb_index][0] + "?, ceci est votre " + str(self.nb_essai) + " essais") #affiche la meme question que le tour precedent mais en incrementant le nombre de tentative



	def verification(self):
		"""
		verifie la reponse du joueur et l'affiche graphiquement
		calcul du score :
		1 / le nombre d'essai et redivise par 4 si le joueur a pris un indice
		"""
		if self.entree_question.get().lower() == self.jeu[self.niveau][self.nb_index][1].lower(): #bonne reponse :
			if self.take_indice == True:
				self.score += (round(1/self.nb_essai, 2) / 4)
			else:
				self.score += round(1/self.nb_essai, 2)
			#on remet les conditions en place pour reposer une nouvelle question
			self.take_indice = False
			self.label_score.config(text="Votre score : " + str(self.score)) #actualise le score
			self.nb_essai = 1
			self.label_result.config(text="BONNE REPONSE", fg="green")
			self.picture.pack_forget() #fait disparaitre la photo
			self.beat_record() #on regarde si le record a ete battue
		else : #mauvaise reponse : 
			self.label_question.config(fg="red")
			self.nb_essai += 1 #on incremente le nombre d'essai
			self.label_result.config(text="MAUVAISE REPONSE", fg="red")
		self.entree_question.delete(0, 'end')
		self.poser_question() #on rapelle la fonction self.poser_question (soit pour en poser une nouvelle, soit pour reposer la meme)


	def get_record(self):
		"""
		permet de recuperer les records dans le fichier record.txt dans la variable self.record sous la forme suivante : ["record_niveau1", "record_niveau2", "record_niveau3"]
		"""
		f = open("record.txt")
		self.record = f.read()
		self.record = self.record.split("\n")
		f.close()


	def beat_record(self):
		"""
		verifie si le record a ete batu
		si c'est le cas:
		met a jour self.record
		l'affiche graphiquement
		change le fichier record.txt
		"""
		if self.score > float(self.record[self.niveau]):
			self.record[self.niveau] = self.score
			self.label_score.config(fg="#d9bd29")
			self.label_record.config(text="Nouveau record " + str(self.record[self.niveau]) ,fg="#d9bd29")
			f = open("record.txt", "w")
			f.write(str("\n".join([str(a) for a in self.record])))



	def indice(self):
		"""
		permet d'afficher une photo de la capital recherchee
		"""
		self.take_indice = True
		try: #essaye de cherger l'image 
			img = Image.open(self.jeu[self.niveau][self.nb_index][1] + ".jpg")
		except: #en cas d'erreur, on selectionne une photo par default
			img = Image.open("sasas.PNG")
		img = img.resize((360, 202))
		img = ImageTk.PhotoImage(img)
		self.picture.configure(image=img) #affiche la nouvelle photo
		self.picture.image = img
		self.picture.pack()



	def change_niveau(self, value):
		"""
		permet de changer de niveau de difficulte en faisant tous les changements que cela incombe:
		vidage de self.dejavu_jeu
		changement graphique
		"""
		#update variable
		self.niveau = int(value) - 1
		self.nb_essai = 1
		del self.dejavu_jeu[:]
		self.score = 0
		#update label
		self.label_score.config(text="Votre score : " + str(self.score), fg="black")
		self.label_result.config(text="")
		self.label_record.config(text="Le record de niveau " + str(self.niveau) + " : " + str(self.record[self.niveau]), fg="black")
		self.poser_question() #continue le jeu
 

	def restart(self):
		"""
		permet de recommencer en apelant la fonction self.change_niveau
		"""
		self.change_niveau(self.niveau+1)
		self.picture.pack_forget()
		self.label_result.config(text="")

	def passer(self):
		"""
		permet de passer à une autre question
		"""
		self.nb_essai = 1
		self.picture.pack_forget()
		self.label_result.config(text="Passe", fg="blue")
		self.poser_question()



	def get_liste(self):
		"""
		recupere la liste des questions dans le fichier liste.txt
		"""
		f = open("liste.txt", "r")
		self.jeu = ast.literal_eval(f.read())
		f.close()


	def ajout_liste(self, ajout, level):
		"""
		permet d'ajouter une nouvelle question dans le fichier liste.txt
		"""
		liste = self.jeu[:]
		nb = 0
		for a in liste:
			if level == nb:
				liste[nb].append(ajout)
			nb += 1
		f = open("liste.txt", "w")
		f.write(str(liste))
		f.close()
		self.get_liste()
		self.change_niveau(self.niveau+1)


	def rules(self):
		"""
		affiche les regles ecrites dans le fichier rules.py en ouvrant une nouvelle fentre
		"""
		fenetre = tk.Toplevel(self.fenetre)
		fenetre.title("Regles")
		f = open("rules.txt", "r")
		texte = f.read()
		tk.Label(fenetre, text=texte).pack()


	def formulaire_ajout_liste(self):
		"""
		ouvre une nouvelle fentre permettant de faire une nouvelle question
		"""
		fenetre = tk.Toplevel(self.fenetre)
		fenetre.title("Add")
		tk.Label(fenetre, text="Nom du pays").pack()
		pays = tk.Entry(fenetre)
		pays.pack()
		tk.Label(fenetre, text="Nom de la capital").pack()
		capital = tk.Entry(fenetre)
		capital.pack()
		tk.Label(fenetre, text="Determinant en amont du pays dans la phrase Quelle est la capital (votre pays) (exemple de la pour la france ou du pour le portugal)").pack()
		deteminant = tk.Entry(fenetre)
		deteminant.pack()
		tk.Label(fenetre, text="Quelle niveau de difficulté (1 = facile, 2 = moyen, 3 = difficile")
		niveau = tk.Scale(fenetre, from_=1, to=3, label="Niveau de difficulté, 1 facile, 2 moyen, 3 difficile")
		niveau.pack()
		tk.Button(fenetre, text="fichier photo", command=self.choix_fichier).pack() #permet de choisir une photo dans l'ordinateur comme indice, pas obligatoire
		tk.Button(fenetre, text="valider", command=lambda:[self.ajout_liste([pays.get(), capital.get(), deteminant.get()], int(niveau.get())-1),self.copier_photo(capital.get()), fenetre.destroy()]).pack()
		"""
		boutton qui :
		ajoute la nouvelle question en apellant self.ajout_liste avec les parametres rentres
		copie la photo dans le dossier en apellant self.copier_photo
		et ferme cette fenetre
		"""





	def choix_fichier(self):
		"""
		ouvre une fenetre pour choisir le fichier photo (seulement jpg)
		"""
		self.filename = askopenfilename(title="Ouvrir votre document", filetypes=[('seulement des jpg pou le moment','.jpg')])


	def copier_photo(self, name):
		"""
		copie la photo choisi par l'utilisateur dans ce dossier
		"""
		if self.filename != False:
			shutil.copyfile(self.filename, name + self.filename[-4:])
		else: #dans le cas ou aucune photo n'a ete choisi
			print("no file selected")
		self.filename = False

	def entree(self, event):
		"""
		permet grace à la touche entree de valider une reponse
		"""
		self.verification()

	def cfini(self):
		"""
		fonction utilise lorsque toute les questions ont ete posees
		"""
		score = self.score
		self.restart()
		self.label_result.config(text="Bravo, vous avez effectuez toutes les questions de ce niveau, votre score : " + str(score), fg="black")


	def reset_record(self):
		"""
		permet de remettre les records à zero et restart le jeu (obligatoire pour eviter toute erreur)
		"""
		f = open("record.txt", "w")
		f.write("0\n0\n0")
		f.close()
		self.get_record()
		self.restart()





jeu_capital() #lancement du jeu

