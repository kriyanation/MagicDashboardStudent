import logging

import webbrowser
from logging.handlers import RotatingFileHandler


import tkinter as tk

from tkinter import ttk, PhotoImage

import DataCaptureDashboard
import FlashCard

import Lesson_List_Display
import Timer_Display
import assessment_viewer

import magiccontainer
import snapshot_view


from MagicTeacherUse import MagicTeacherUse


handler = RotatingFileHandler("../MagicLogs.log", maxBytes=1 * 1024 * 1024,
                              backupCount=3)
form = logging.Formatter("%(asctime)s- %(name)s: %(message)s")
logger = logging.getLogger("MagicLogger")
handler.setFormatter(form)
logger.setLevel(logging.WARNING)
logger.addHandler(handler)

BACKGROUND_COLOR = "gray18"
BOX_BACKGROUND_COLOR = "gray21"
BOX_FOREGROUND_COLOR = "white"
FOREGROUND_COLOR = "peachpuff2"
ACTIVE_BUTTON_COLOR = "gray44"
BOX_BUTTON_BACKGROUND_COLOR="dark slate gray"
BOX_BUTTON_FOREGROUND_COLOR= "white"
ACTIVE_BOX_BUTTON_COLOR= "slate gray"


class MagicDashboard(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        logger.info("Entering MagicDashboard Initialize")
        #teacher_check = MagicTeacherUse(self,parent)
        self.configure(background=BACKGROUND_COLOR)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Blue.TButton', background='white', foreground='royalblue4', font=('helvetica', 10, 'bold'),
                    bordercolor="royalblue4")
        s.map('Blue.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])

        s.configure('time.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        s.configure("dash.TButton",background=BACKGROUND_COLOR,foreground=FOREGROUND_COLOR)
        s.map('dash.TButton', background=[('pressed', FOREGROUND_COLOR), ('active', '!disabled', ACTIVE_BUTTON_COLOR)],
              foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])
        s.map('dash1.TButton', background=[('active', '!disabled', ACTIVE_BUTTON_COLOR), ('pressed', FOREGROUND_COLOR)],
             foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])

        s.configure('dash.TLabelframe', background=BACKGROUND_COLOR,bordercolor=FOREGROUND_COLOR,borderwidth=3)
        s.configure('dash.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('dash.TLabelframe.Label', foreground=FOREGROUND_COLOR,background=BACKGROUND_COLOR)
        s.configure('dashheader.Label', background='steel blue', foreground='snow', font=('courier', 10, 'bold','italic'))
        s.configure('dashdata.Label', background='steel blue', foreground='snow', font=('courier', 50, 'bold'))
        s.configure('dash2header.Label', background='gray16', foreground='snow',
                    font=('comic sans', 12, 'bold', 'italic'))
        s.configure('dash3data.Label', background='steel blue', foreground='snow',
                    font=('courier', 20, 'bold', 'italic'))
        s.configure('dash2data.Label', background='gray16', foreground='snow', font=('courier', 40, 'bold'))
        s.configure('dash4header.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                    font=('comic sans', 10, 'bold', 'italic'))
        s.configure('dashboxheader.Label', background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR,
                    font=('comic sans', 8, 'bold'))
        s.configure('dashboxbutton.TButton', background=BOX_BUTTON_BACKGROUND_COLOR, foreground=BOX_BUTTON_FOREGROUND_COLOR,
                    font=('comic sans', 8, 'bold'))
        s.map('dashboxbutton.TButton', background=[('active', '!disabled', ACTIVE_BOX_BUTTON_COLOR), ('pressed', BOX_BUTTON_FOREGROUND_COLOR)],
              foreground=[('pressed', BOX_BUTTON_FOREGROUND_COLOR), ('active', BOX_BUTTON_FOREGROUND_COLOR)])
        self.image_logo = PhotoImage(file="../images/logo_bg.png")
        self.logo_button = ttk.Button(self, text="", image=self.image_logo,
                                       style="dash.TButton",width=5,
                                       command=self.launch_website)
        #self.Lessons_Frame_Create()
        #self.Participants_Frame_Create()
        self.tools_frame_create()
        self.flash_frame_create()
        #self.star_frame_create()
        self.logo_button.grid(row=0, column=0,columnspan=2, sticky=tk.N)


    def flash_image_display_scroll(self,frame,list,index):
        logger.info("Entering Flash Image Display")
        try:
            if hasattr(self,"flash_display_lessons"):
                self.flash_display_lessons.grid_forget()
            self.flash_display_lessons = tk.Label(frame,text=list[index][1],width=20,
                                             font=("Helvetica", 14, 'bold'),height=1,
                                             background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

            self.flash_display_lessons.grid(row=0,column=0,sticky=tk.W)
        except:
            logger.info("Flash Term could not be found")
            logger.exception("Flash Term could not be found")
        if index == len(list) - 1:
            return
        else:
            index += 1
        self.after(10000,self.flash_image_display_scroll,frame,list,index)


    def launch_website(self):
        webbrowser.open_new_tab("http://www.wondersky.in/")



    def launch_flashcard(self):
        launch_flashcard = FlashCard.MagicFlashApplication(self)
        launch_flashcard.geometry("1500x800+120+20")

    def launch_assessment_pdf(self):
        launch_assessment = assessment_viewer.MagicAssessmentPrint(self)
        launch_assessment.geometry("800x400+300+300")

    def lessons_list(self):
        launch_lessonlist = Lesson_List_Display.MagicLessonList(self)
        launch_lessonlist.geometry(str(self.winfo_screenwidth())+"x"+str(self.winfo_screenheight())+"+0+0")

    def launch_player(self):
        launch_player = magiccontainer.MagicApplication(self)
        launch_player.geometry(str(self.winfo_screenwidth())+"x"+str(self.winfo_screenheight())+"+0+0")

    def launch_pdf_notes(self):
        launch_notes = snapshot_view.SnapshotView(self)
        launch_notes.geometry("800x400+300+300")



    def launch_timer(self):
        launch_timer = Timer_Display.TimerDisplay(self)
        launch_timer.resizable(width=False,height=False)
        launch_timer.attributes("-topmost", True)
        launch_timer.geometry("240x250+20+20")

    def tools_frame_create(self):
        logger.info("Entering Tools Frame Create")
        self.tools_group_frame = tk.Frame(self, padx=10, pady=10,highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.tools_group_frame.grid(row=1, column=1, padx=10,pady = 10,sticky=tk.N)
        self.image_tools = PhotoImage(file="../images/tools.png")
        self.tools_header_label = tk.Label(self.tools_group_frame, compound=tk.LEFT,
                                                  image=self.image_tools,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text="Tools", font=("Helvetica", 12, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.tools_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)

        self.lesson_button = ttk.Button(self.tools_group_frame, text="View",
                                       width=8,
                                       command=self.lessons_list, style="dashboxbutton.TButton")
        self.print_notes_button = ttk.Button(self.tools_group_frame, text="Notes",
                                      width=8,
                                      command=self.launch_pdf_notes, style="dashboxbutton.TButton")
        self.print_assessment_button = ttk.Button(self.tools_group_frame, text="Assess",
                                             width=8,
                                             command=self.launch_assessment_pdf, style="dashboxbutton.TButton")


        self.lesson_label = tk.Label(self.tools_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Add Mini Lesson",
                                    font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
       

        self.notes_label = tk.Label(self.tools_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Audio and Print Notes",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.assessment_label = tk.Label(self.tools_group_frame, borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Assessments",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.lesson_label.grid(row=1, column=0, pady=10)
        self.lesson_button.grid(row=1, column=1, pady=10)



        self.notes_label.grid(row=4, column=0, pady=8)
        self.print_notes_button.grid(row=4, column=1, pady=8)

        self.assessment_label.grid(row=5, column=0, pady=10)
        self.print_assessment_button.grid(row=5, column=1, pady=10)

    def flash_frame_create(self):
        logger.info("Entering Flash Card Frame Create")
        self.flash_group_frame = tk.Frame(self, padx=10, pady=10,highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.flash_group_frame.grid(row=1, column=0, padx=10,pady =10,sticky=tk.N)
        self.image_flash = PhotoImage(file="../images/chalkboard.png")
        self.flash_header_label = tk.Label(self.flash_group_frame, compound=tk.LEFT,
                                                  image=self.image_flash,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Interactions", font=("Helvetica", 12, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.flash_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.flash_image_scroll_frame = tk.Frame(self.flash_group_frame, 
                                                   background="gray18")
        self.flash_image_scroll_frame.rowconfigure(0, weight=1)
        self.flash_image_scroll_frame.columnconfigure(0, weight=1)
        self.flash_image_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.flash_list = DataCaptureDashboard.get_flash_names()
        flash_list_index = 0
        self.flash_image_display_scroll(self.flash_image_scroll_frame, self.flash_list, flash_list_index)
        self.play_button = ttk.Button(self.flash_group_frame, text="Start",
                                       width=7,
                                       command=self.launch_player, style="dashboxbutton.TButton")
        self.cards_button = ttk.Button(self.flash_group_frame, text="Play",
                                      width=7,
                                      command=self.launch_flashcard, style="dashboxbutton.TButton")


        self.play_label = tk.Label(self.flash_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Mini Lesson Class",
                                    font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
        self.cards_label = tk.Label(self.flash_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Flashcards",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.timer_button = ttk.Button(self.flash_group_frame, text="Timer",
                                                  width=8,
                                                  command=self.launch_timer, style="dashboxbutton.TButton")
        self.timer_label = tk.Label(self.flash_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Launch Timer",
                                   font=("Helvetica", 10, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.play_label.grid(row=2, column=0, pady=5)
        self.play_button.grid(row=2, column=1, pady=5)

        self.cards_label.grid(row=3, column=0, pady=5)
        self.cards_button.grid(row=3, column=1, pady=5)

        self.timer_label.grid(row=4,column=0,pady=5)
        self.timer_button.grid(row=4,column=1,pady=5)



if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.iconphoto(True, tk.PhotoImage(file='../images/lr_logo.png'))
    dashboard_app.configure(background="gray18")
    dashboard_app.title("Learning Room Dashboard")
    screen_width = dashboard_app.winfo_screenwidth()
    screen_height = dashboard_app.winfo_screenheight()

    screen_half_width = int(dashboard_app.winfo_screenwidth())
    screen_half_height = int(dashboard_app.winfo_screenheight())
    dashboard_app.geometry("800x400+200+220")
    frame = MagicDashboard(dashboard_app)

    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0,sticky=tk.EW)
    dashboard_app.mainloop()

