from datetime import datetime
import socket
import threading
from tkinter import *
from tkinter.messagebox import *


class InterfaceLogin(Tk):
    def __init__(self):
        super().__init__()

        # definition de constantes pour les couleurs
        self.color_first = "#24d9f8"
        self.color_second = "#0d1137"
        self.color_third = "#dedee0"
        self.bg_frame_with_bar_def = "#ffcce7"  # "#ced7d8"
        self.color_v = "#24f86a"
        # window = Tk()
        # window.resizable(False, False)
        self.resizable(False, False)

        self.title = "JOTAAY"

        self.first_frame = Frame(self, bg=self.color_second, relief=GROOVE)
        self.first_frame.pack(fill="both", expand=True)

        self.left_frame = Frame(
            self.first_frame, bg=self.color_third, padx=20, pady=20)
        self.left_frame.pack(side=LEFT)
        image = PhotoImage(
            file='jotaayLogo.png')
        self.canvas = Canvas(self.left_frame, width=370,
                             height=357,
                             bg="white")
        self.canvas.create_image(0, 0, anchor=NW, image=image)
        self.canvas.pack(side=BOTTOM)
        # #----------------------------------------------------------------------------------
        self.right_frame = Frame(
            self.first_frame, bg=self.color_first, bd=3, pady=20, relief=GROOVE)  # bg="blue"
        self.right_frame.pack(expand=True, fill=Y, side=RIGHT)
        Label(self.right_frame, text="_ Jotaay _", font="Times 30 bold",
              fg="white", bg=self.color_first).pack(side=TOP, pady=30, padx=50)
        image1 = PhotoImage(
            file='icon-us.png')
        self.canvas = Canvas(self.right_frame, width=240,
                             height=180,
                             bg="white")
        self.canvas.create_image(0, 0, anchor=NW, image=image1)
        self.canvas.pack(side=TOP)
        self.label_pseudo = Label(self.right_frame, text="Votre nom d'utilisateur:",
                                  font="Arial 15", fg="white", bg=self.color_first, justify='left')
        self.label_pseudo.pack(anchor=W, padx=80)
        self.text_pseudo = Entry(
            self.right_frame, width=20, bg="white", font="Arial 20")
        self.text_pseudo.focus_set()
        self.text_pseudo.pack(pady=5)

        Button(self.right_frame, text="se connecter", bg=self.color_v,
               command=self.seConnecter).pack(pady=10, padx=83, fill=X)

        self.mainloop()

    def seConnecter(self):
        if self.text_pseudo.get():
            if len(self.text_pseudo.get()) < 6:
                self.user = self.text_pseudo.get()
            else:
                showerror("OUPS ! Erreur ",
                          "Le Nom d'utilisateur ne doit pas depassé 6 caractere")
                # self.user = self.text_pseudo.get()[:6] + "."
            # -------------------       CONEXION CLIENT         ---------------------------
            myClient_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                myClient_socket.connect(("localhost", 5500))
                print(self.text_pseudo.get())
                self.right_frame.pack_forget()
                self.left_frame.pack_forget()
                InterfaceChat(self, self.first_frame,
                              myClient_socket, self.user)
            except ConnectionRefusedError:
                msgs = "Serveur non démarré"
                print(msgs)
# _________________FVAIRE UNE INTERFACE AVEC LABEL Serveur non demare

                showerror("OUPS ! Erreur ", "Serveur non démarré")
        else:
            print("non authentifié")
# _________________FVAIRE UNE INTERFACE AVEC LABEL NON AUTHENTIFIé
            showerror("OUPS! ", "Veillez saisir le champs svp")


class InterfaceChat(Canvas):
    def __init__(self, parent, first_frame, myClient_socket, user):
        super().__init__(parent, bg=parent.color_second)

        # ---------------------------       INFOS CLIENT        ---------------------
        self.myClient_socket = myClient_socket
        self.user = user

        self.window = 'InterfaceChat'

        self.first_frame = first_frame
        self.first_frame.pack_forget()

        self.parent = parent

        self.parent.protocol("WM_DELETE_WINDOW")  # , self.on_closing)
        # Dimensionnement de la fenetre
        self.parent.geometry("500x800")

        self.y = 140
        # ima = PhotoImage(
        #     file='icon-us.png')
        # self.canvas = Canvas(self, width=250,
        #                      height=200,
        #                      bg="white")
        # self.canvas.create_image(5, 10, anchor=NW, image=ima)
        # self.canvas.pack( side=RIGHT)
        self.create_text(250, 20, text="| @_"+self.user+" | ",
                         font="lucida 18 bold", fill="white")
        # --------------------          FRAME POUR BOXMESSAGE POUR LE CHAT            -----------------------------------------------
        # Creation d'un Frame boxMessage
        boxMessage = Frame(self, padx=0, pady=0, )
        boxMessage.place(x=30, y=50, width=400, height=400,)

        # Creation d'un canvas pour l'affichage des messages envoyés et recus
        self.canvas = Canvas(
            boxMessage, bg=self.parent.color_third)  # #595656

        # Creation d'un frame scrollabre a l'interieur du canvas de boxMessage
        self.frame_avec_bar_def = Frame(
            self.canvas, bg=self.parent.color_third)

        scrollable_window = self.canvas.create_window(
            (0, 0), window=self.frame_avec_bar_def, anchor="nw")

        def configure_scroll_region(e):
            self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        def resize_frame(e):
            self.canvas.itemconfig(scrollable_window, width=e.width)

        self.frame_avec_bar_def.bind("<Configure>", configure_scroll_region)

        # Creation d'une barre de défilement pour le conteneur
        self.bar_def_vertical = Scrollbar(
            boxMessage, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.bar_def_vertical.set)
        self.yview_moveto(1.0)
        self.bar_def_vertical.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", resize_frame)
        self.canvas.pack(fill="both", expand=True)

        #  Creation champs de formulaire du message a envoyer
        self.txt_message = Text(self, font="lucida 10 bold", width=38,
                                height=2, highlightcolor="blue", highlightthickness=1)
        self.txt_message.place(x=40, y=510)
        self.txt_message.focus_set()

        # Creation du bouton d'envoi du message
        bt_envoyer = Button(self, text="Envoyer", fg="#83eaf7", font="lucida 11 bold", bg="#7d7d7d", padx=10,
                            relief="solid", bd=2, command=self.envoyerMessage)
        bt_envoyer.place(x=340, y=510)

        self.pack(fill="both", expand=True)

        # Creation du THREAD CLIENT USER
        thread_user = threading.Thread(target=self.receptionMessage)
        thread_user.setDaemon(True)
        thread_user.start()

# LES FONCTIONS      reception et envoie de message
    def receptionMessage(self):
        while True:
            data = self.myClient_socket.recv(1024).decode("utf-8")
            print(data)
            self.recevoirMessage(data)

    def envoyerMessage(self):
        print(self.parent.user)
        # Recuperation de l'heure d'envoi du message
        heure_msg = datetime.now().strftime('%H:%M')
        dateHeure_msg=datetime.now().strftime('%d-%Y-%m %H:%M')
        msg = self.txt_message.get('1.0', 'end').strip()
        if msg and msg != "":
            print(msg)
            txt = "De @-" + self.parent.user + " Le " + dateHeure_msg + "  : \n  \t " + msg
            msg_post = " @Moi  : \t" + msg + " \n à " + heure_msg
            print(txt)
            message_frame = Frame(self.frame_avec_bar_def,
                                  )
            message_frame.columnconfigure(0, weight=1)

            label_message_frame = Label(message_frame, wraplength=250, text=msg_post, fg="white", bg=self.parent.color_second,
                                        font="lucida 11 bold", justify="left",
                                        anchor="e")  # bg="#40C961"
            label_message_frame.grid(
                row=1, column=0, padx=2, pady=2, sticky="e")
            message_frame.pack(pady=10, padx=10, fill="x",
                               expand=True, anchor="e")

            # ENVOI DU MESSAGE AU SERVEUR
            self.myClient_socket.send(txt.encode('utf-8'))

            #  Vider le contenue du input du formulaire
            self.txt_message.delete("1.0", "end")

            # Forcer le frame BOXMESSAGE a s'actualiser automatiquement
            self.canvas.update_idletasks()
            self.canvas.yview_moveto(1.0)

        else:
            print('not get')
            showerror("OUPS! ", "Veillez saisir votre message")

    def recevoirMessage(self, msg_from_user):
        msg_from_other = msg_from_user
      
        # Creation d'un frame pour contenir les messages recus
        message_from_user_frame = Frame(
            self.frame_avec_bar_def, bg=self.parent.color_first)
        message_from_user_frame.columnconfigure(1, weight=1)
        # Creation d'un frame pour le message recu
        # if msg_from_user!="":
        #     msg_from_other="\n ___--HISTORIQUE DES DISCUSSIONS--___ \n \t"+msg_from_other
        
        label_message_from_user_frame = Label(message_from_user_frame, wraplength=250, fg="white",
                                              text=msg_from_other, font="lucida 11 bold", justify="left",
                                              anchor="w", bg=self.parent.color_first)
        label_message_from_user_frame.grid( row=1,column=1,
             padx=2, pady=2, sticky="w")

        message_from_user_frame.pack(
            pady=10, padx=10, fill="x", expand=True, anchor="e")

        #  force le frame BOXMESSAGE a s'actualisé automatiquement
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)


InterfaceLogin()
# class NotificationInterface(Canvas):
#     def __init__(self, parent,msgs):
#         super().__init__(parent, bg=parent.color_first)
#         self.msgs=msgs

#         self.window = 'Notification'

#         # self.first_frame = first_frame
#         # self.first_frame.pack_forget()

#         self.parent = parent

#         self.parent.protocol("WM_DELETE_WINDOW")  # , self.on_closing)
#         # Dimensionnement de la fenetre
#         self.parent.geometry("520x580")

#         self.y = 140

#         self.canvas.bind("<Configure>", resize_frame)
#         self.canvas.pack(fill="both", expand=True)

#         #  force le frame BOXMESSAGE a s'actualisé automatiquement
#         self.canvas.update_idletasks()
#         self.canvas.yview_moveto(1.0)
