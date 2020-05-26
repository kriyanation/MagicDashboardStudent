import logging
import os
import subprocess
import traceback
import webbrowser
from logging.handlers import RotatingFileHandler

import sys
import tkinter as tk

from tkinter import ttk, PhotoImage, simpledialog

import DataCaptureDashboard
import FlashCard

import Lesson_List_Display
import MagicEditWizard
import Timer_Display
import assessment_viewer

import create_explainer_content
import magic_classroom_info
import magiccontainer
import snapshot_view
import tooltip

from PIL import Image, ImageTk

handler = RotatingFileHandler("../MagicLogs.log", maxBytes=1 * 1024 * 1024,
                              backupCount=3)
form = logging.Formatter("%(asctime)s- %(name)s: %(message)s")
logger = logging.getLogger("MagicLogger")
handler.setFormatter(form)
logger.setLevel(logging.DEBUG)
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
        self.configure(background=BACKGROUND_COLOR)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('time.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        s.configure("dash.TButton",background=BACKGROUND_COLOR,foreground=FOREGROUND_COLOR)
        s.map('dash.TButton', background=[('pressed', FOREGROUND_COLOR), ('active', '!disabled', ACTIVE_BUTTON_COLOR)],
              foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])
        s.map('dash1.TButton', background=[('active', '!disabled', ACTIVE_BUTTON_COLOR), ('pressed', FOREGROUND_COLOR)],
             foreground=[('pressed', FOREGROUND_COLOR), ('active', FOREGROUND_COLOR)])

        s.configure('dash.TLabelframe', background=BACKGROUND_COLOR,bordercolor=FOREGROUND_COLOR,borderwidth=3)
        s.configure('dash.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('dash.TLabelframe.Label', foreground=FOREGROUND_COLOR,background=BACKGROUND_COLOR)
        s.configure('dashheader.Label', background='steel blue', foreground='snow', font=('courier', 12, 'bold','italic'))
        s.configure('dashdata.Label', background='steel blue', foreground='snow', font=('courier', 50, 'bold'))
        s.configure('dash2header.Label', background='gray16', foreground='snow',
                    font=('comic sans', 12, 'bold', 'italic'))
        s.configure('dash3data.Label', background='steel blue', foreground='snow',
                    font=('courier', 20, 'bold', 'italic'))
        s.configure('dash2data.Label', background='gray16', foreground='snow', font=('courier', 40, 'bold'))
        s.configure('dash4header.Label', background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR,
                    font=('comic sans', 10, 'bold', 'italic'))
        s.configure('dashboxheader.Label', background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR,
                    font=('comic sans', 10, 'bold'))
        s.configure('dashboxbutton.TButton', background=BOX_BUTTON_BACKGROUND_COLOR, foreground=BOX_BUTTON_FOREGROUND_COLOR,
                    font=('comic sans', 8, 'bold'))
        s.map('dashboxbutton.TButton', background=[('active', '!disabled', ACTIVE_BOX_BUTTON_COLOR), ('pressed', BOX_BUTTON_FOREGROUND_COLOR)],
              foreground=[('pressed', BOX_BUTTON_FOREGROUND_COLOR), ('active', BOX_BUTTON_FOREGROUND_COLOR)])





        self.image_logo = PhotoImage(file="../images/logo_bg.png")
        self.logo_button = ttk.Button(self, text="", image=self.image_logo,
                                       style="dash.TButton",width=5,
                                       command=self.launch_website)



        self.Lessons_Frame_Create()
        self.Participants_Frame_Create()
        self.tools_frame_create()
        self.flash_frame_create()
        self.star_frame_create()

        #self.launcher_display()

        #self.info_display()

        self.logo_button.grid(row=0, column=0,columnspan=2, sticky=tk.N)
    def Participants_Frame_Create(self):
        self.participants_group_frame = tk.Frame(self, padx=10, pady=10, width=300, height=300, highlightthickness=3,
                                            highlightbackground="gray30", highlightcolor="gray30", background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.participants_group_frame.grid(row=1, column=1, padx=10)
        self.image_participants = PhotoImage(file="../images/business-class.png")
        self.participants_header_label = tk.Label(self.participants_group_frame, compound=tk.LEFT, image=self.image_participants,
                                             borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                             text=" Participants", font=("Helvetica", 16, 'bold'),
                                             background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.participants_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.participants_names_scroll_frame = tk.Frame(self.participants_group_frame, width=200, height=200,
                                                   background="gray18")
        self.participants_names_scroll_frame.rowconfigure(0, weight=1)
        self.participants_names_scroll_frame.columnconfigure(0, weight=1)
        self.participants_names_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.participant_list = DataCaptureDashboard.get_participants()
        participants_index = 0
        self.show_participants_names(self.participants_names_scroll_frame, self.participant_list, participants_index)
        self.class_button = ttk.Button(self.participants_group_frame, text="Maintain",
                                        width=8,
                                        command=self.launch_class_data, style="dashboxbutton.TButton")
        self.bday_button = ttk.Button(self.participants_group_frame, text="Play",
                                      width=8,
                                      command=self.bday_play, style="dashboxbutton.TButton")

        self.class_label = tk.Label(self.participants_group_frame,
                                     borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                     text="Classroom Information",
                                     font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                     foreground=BOX_FOREGROUND_COLOR)
        self.bday_label = tk.Label(self.participants_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Play B'Day Song",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.class_label.grid(row=2, column=1, pady=5)
        self.class_button.grid(row=2, column=2, pady=5)
        self.bday_label.grid(row=3, column=1, pady=5)
        self.bday_button.grid(row=3, column=2, pady=5)


    def Lessons_Frame_Create(self):
        self.lessons_group_frame = tk.Frame(self, padx=10, pady=10, width=300, height=300, highlightthickness=3,
                                            highlightbackground="gray30", highlightcolor="gray30", background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.lessons_group_frame.grid(row=1, column=0,rowspan=2, padx=10,sticky=tk.N)
        self.image_lessons = PhotoImage(file="../images/books.png")
        self.lessons_header_label = tk.Label(self.lessons_group_frame, compound=tk.LEFT, image=self.image_lessons,
                                             borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                             text=" Lessons", font=("Helvetica", 16, 'bold'),
                                             background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.lessons_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.lessons_image_scroll_frame = tk.Frame(self.lessons_group_frame, width=200, height=200,
                                                   background="gray18")
        self.lessons_image_scroll_frame.rowconfigure(0, weight=1)
        self.lessons_image_scroll_frame.columnconfigure(0, weight=1)
        self.lessons_image_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.image_list = DataCaptureDashboard.get_title_images()
        title_image_index = 0
        self.lesson_image_display_scroll(self.lessons_image_scroll_frame, self.image_list, title_image_index)
        self.create_button = ttk.Button(self.lessons_group_frame, text="Create",
                                        width=6,
                                        command=self.create_lesson, style="dashboxbutton.TButton")
        self.edit_button = ttk.Button(self.lessons_group_frame, text="Edit",
                                      width=6,
                                      command=self.launch_lesson_edit, style="dashboxbutton.TButton")
        self.view_button = ttk.Button(self.lessons_group_frame, text="View",
                                      width=6,
                                      command=self.lessons_list, style="dashboxbutton.TButton")
        self.create_label = tk.Label(self.lessons_group_frame,
                                     borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                     text="Create a New Lesson",
                                     font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                     foreground=BOX_FOREGROUND_COLOR)
        self.edit_label = tk.Label(self.lessons_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                   text="Edit your Lessons",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)
        self.lessons_label = tk.Label(self.lessons_group_frame,
                                      borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=20,
                                      text="List all Lessons",
                                      font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                      foreground=BOX_FOREGROUND_COLOR)
        self.create_label.grid(row=2, column=1, pady=5)
        self.create_button.grid(row=2, column=2, pady=5)
        self.edit_label.grid(row=3, column=1, pady=5)
        self.edit_button.grid(row=3, column=2, pady=5)
        self.lessons_label.grid(row=4, column=1, pady=5)
        self.view_button.grid(row=4, column=2, pady=5)

    def show_participants_names(self, frame,list, n_index):

        if len(list) == 0:
            return
        if (hasattr(self,"participants_names_display")) and self.participants_names_display is not None:
            self.participants_names_display.grid_forget()
        self.participants_names_display = tk.Label(frame, text=list[n_index][0],borderwidth=3, highlightcolor="gray18", width=25,
                                             font=("Helvetica", 16, 'bold'),
                                             background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)
        self.participants_names_display.grid(row=0, column=0)
        if (n_index == len(list)-1):
            n_index = 0
        else:
           n_index += 1

        self.after(5000, self.show_participants_names, frame, list, n_index)



    def flash_image_display_scroll(self,frame,list,index):
        lesson_folder = "Lesson"+str(list[index][0])
        image_root = DataCaptureDashboard.lesson_root+os.path.sep+lesson_folder+os.path.sep+"images"
        image_file = image_root+os.path.sep+list[index][1]
        try:
            image_display = Image.open(image_file)
            image_display = image_display.resize((150,150),Image.ANTIALIAS)
            image_frame = ImageTk.PhotoImage(image_display)
            self.flash_resized_lessons_list = []
            self.flash_resized_lessons_list.append(image_frame)
            self.flash_display_lessons = ttk.Label(frame,image=image_frame)
            self.flash_display_lessons.grid(row=0,column=0)
        except:
            logger.info("Image could not be found or opened")
        if index == len(list) - 1:
            index =0
        else:
            index += 1
        self.after(5000,self.flash_image_display_scroll,frame,list,index)

    def lesson_image_display_scroll(self,frame,list,index):
        lesson_folder = "Lesson"+str(list[index][0])
        image_root = DataCaptureDashboard.lesson_root+os.path.sep+lesson_folder+os.path.sep+"images"
        image_file = image_root+os.path.sep+list[index][1]
        try:
            image_display = Image.open(image_file)
            image_display = image_display.resize((150,150),Image.ANTIALIAS)
            image_frame = ImageTk.PhotoImage(image_display)
            self.image_resized_lessons_list = []
            self.image_resized_lessons_list.append(image_frame)
            self.image_display_lessons = ttk.Label(frame,image=image_frame)
            self.image_display_lessons.grid(row=0,column=0)
        except:
            logger.info("Image could not be found or opened")
        if index == len(list) - 1:
            index =0
        else:
            index += 1
        self.after(5000,self.lesson_image_display_scroll,frame,list,index)

    def launch_content(self):
        webbrowser.open_new_tab("https://www.dropbox.com/home/Learning%20Room")

    def launch_website(self):
        webbrowser.open_new_tab("http://www.wondersky.in/")

    def info_display(self):
        lesson_count = DataCaptureDashboard.get_Lessons_count()
        self.dashboard_info_labelframe = ttk.LabelFrame(self, text="Learning Info", style="dash.TLabelframe")
        self.dashboard_info_labelframe.grid(row=2, column=0, pady=30)
        self.lessons_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                      highlightbackground='gray16', highlightthickness=3)
        self.lessons_frame.tooltip = tooltip.ToolTip(self.lessons_frame, "Number of Lessons Created")
        self.lessons_header_label = ttk.Label(self.lessons_frame, text=" Lessons ", style="dashheader.Label")
        self.lessons_data_label = ttk.Label(self.lessons_frame, text=lesson_count[0],
                                            style="dashdata.Label")
        student_count = DataCaptureDashboard.get_participants_count()
        self.lessons_frame.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)
        self.lessons_header_label.grid(row=0, column=0)
        self.lessons_data_label.grid(row=1, column=0, pady=5)
        self.participants_frame = tk.Frame(self.dashboard_info_labelframe, background="gray16",
                                           highlightbackground='aquamarine', highlightthickness=3)
        self.participants_frame.tooltip = tooltip.ToolTip(self.participants_frame, "Current Number of Participants")

        self.participants_header_label = ttk.Label(self.participants_frame, text=" Participants ",
                                                   style="dash2header.Label")
        self.participants_data_label = ttk.Label(self.participants_frame, text=student_count[0],
                                                 style="dash2data.Label")

        self.participants_frame.grid(row=0, column=1, sticky=tk.NW, padx=40, pady=10)
        self.participants_header_label.grid(row=0, column=0)
        self.participants_data_label.grid(row=1, column=0, pady=5)


        self.leader_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                     highlightbackground='gray16', highlightthickness=3,width=150,height=60)
        self.leader_frame.tooltip = tooltip.ToolTip(self.leader_frame, "Participants with Level 1 Badge")

        self.leader_header_label = ttk.Label(self.leader_frame, text=" Stars ",
                                             style="dashheader.Label")
        self.leader_data_label = ttk.Label(self.leader_frame,wraplength=200,
                                           style="dash3data.Label")
        self.leader_frame.grid(row=0, column=2, sticky=tk.NE, padx=40, pady=10,ipadx=20,ipady=20)
        self.leader_frame.grid_propagate(False)
        self.leader_header_label.grid(row=0, column=0,sticky=tk.EW,padx=50)
        self.leader_data_label.grid(row=1, column=0, pady=10)
        names = DataCaptureDashboard.get_badge_1_count()
        n_index = 0
        self.show_names(names, n_index)
        flash_card_count = lesson_count[0]*3
        self.flash_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                    highlightbackground='gray16', highlightthickness=3)
        self.flash_frame.tooltip = tooltip.ToolTip(self.flash_frame, "Number of Flashcards to Play")

        self.flash_header_label = ttk.Label(self.flash_frame, text=" Flashcards ",
                                            style="dashheader.Label")
        self.flash_data_label = ttk.Label(self.flash_frame, text=flash_card_count,
                                          style="dashdata.Label")
        self.flash_frame.grid(row=0, column=4, sticky=tk.NE, padx=40, pady=8)
        self.flash_header_label.grid(row=0, column=0)
        self.flash_data_label.grid(row=1, column=0)

        no_steps = DataCaptureDashboard.get_skill_steps_count()
        self.skill_frame = tk.Frame(self.dashboard_info_labelframe, background="gray16",
                                    highlightbackground='aquamarine', highlightthickness=3)
        self.skill_frame.tooltip = tooltip.ToolTip(self.skill_frame, "Number of steps used in the Skill Board")

        self.skill_header_label = ttk.Label(self.skill_frame, text=" Skill Steps ",
                                            style="dash2header.Label")
        self.skill_data_label = ttk.Label(self.skill_frame, text=no_steps[0],
                                          style="dash2data.Label")
        self.skill_frame.grid(row=0, column=3, padx=40, sticky=tk.NE, pady=10)
        self.skill_header_label.grid(row=0, column=0)
        self.skill_data_label.grid(row=1, column=0)
        self.badge_image_bday = tk.PhotoImage(file='../images/BDay.png')
        self.bday_button = ttk.Button(self.dashboard_info_labelframe, image=self.badge_image_bday,
                                      style="dash.TButton",
                                      command=self.bday_play)
        self.bday_button.tooltip = tooltip.ToolTip(self.bday_button, "Wish Happy B'Day to your student")

        self.bday_button.grid(row=0, column=5, padx=40, sticky=tk.NE, pady=3)

    def bday_play(self):

        self.name = simpledialog.askstring("B'Day Student", "Name",
                                        parent=self)
        if self.name is None:
            self.name = ""

        win = tk.Toplevel()
        win.wm_title("Happy B'Day "+self.name)
        win.wm_geometry('500x400+500+200')
        win.resizable(False, False)
        win.configure(background='dark slate gray')
        win.attributes('-topmost', 'true')
        self.bday_label = ttk.Label(win, text="Happy B'Day "+self.name,
                                            style="time.Label")
        self.bday_wish = tk.PhotoImage(file='../images/bday_wish.png')
        self.bday_image = ttk.Label(win, image=self.bday_wish)

        self.bday_label.pack(pady=20)
        self.bday_image.pack(pady=20)
        current_location = os.getcwd()
        file_song_path = os.path.abspath(os.path.join(current_location,"..","images","bday_song.mp3"))

        if sys.platform == "win32":
            os.startfile(file_song_path)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_song_path])

        b = ttk.Button(win, text="Close", style='dash1.TButton', command=win.destroy)
        b.pack()

    def launcher_display(self):
        self.dashboard_launcher_labelframe = ttk.LabelFrame(self, text="Launcher", style="dash.TLabelframe")
        self.dashboard_launcher_labelframe.grid(row=1, column=0)
        self.image_timer = PhotoImage(file="../images/Timer.png")
        self.image_edit = PhotoImage(file="../images/edit_lesson.png")
        self.image_flash = PhotoImage(file="../images/flashcards.png")
        self.image_print_assessment = PhotoImage(file="../images/print_assessment.png")
        self.image_class = PhotoImage(file="../images/class_data.png")
        self.image_player = PhotoImage(file="../images/player_button.png")
        self.lesson_notes = PhotoImage(file="../images/notes.png")
        self.list_lessons = PhotoImage(file="../images/List_Lessons.png")
        self.image_create = PhotoImage(file="../images/create_lesson.png")
        self.timer_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_timer,
                                       style="dash.TButton",
                                       command=self.launch_timer)
        self.image_content = PhotoImage(file="../images/content.png")
        self.content_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_content,
                                       style="dash.TButton",
                                       command=self.launch_content)
        self.timer_button.tooltip = tooltip.ToolTip(self.timer_button, "Launch Timer Screen")

        self.edit_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_edit,
                                      style="dash.TButton",
                                      command=self.launch_lesson_edit)
        self.edit_button.tooltip = tooltip.ToolTip(self.edit_button, "Edit Existing Lesson")

        self.flash_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_flash,
                                       style="dash.TButton",
                                       command=self.launch_flashcard)
        self.flash_button.tooltip = tooltip.ToolTip(self.flash_button, "Play a game of Flash Cards")

        self.print_assessment_button = ttk.Button(self.dashboard_launcher_labelframe, text="",
                                                  image=self.image_print_assessment,
                                                  style="dash.TButton",
                                                  command=self.launch_assessment_pdf)
        self.print_assessment_button.tooltip = tooltip.ToolTip(self.print_assessment_button, "Print PDF of Assessment Questions")

        self.class_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_class,
                                       style="dash.TButton",
                                       command=self.launch_class_data)
        self.class_button.tooltip = tooltip.ToolTip(self.class_button, "Maintain Classroom Information")

        self.player_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_player,
                                        style="dash.TButton",
                                        command=self.launch_player)
        self.player_button.tooltip = tooltip.ToolTip(self.player_button, "Conduct the Interactive Session for your Lesson")

        self.notes_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.lesson_notes,
                                       style="dash.TButton",
                                       command=self.launch_pdf_notes)
        self.notes_button.tooltip = tooltip.ToolTip(self.notes_button, "Print Notes for your Lesson")

        self.lessons_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.list_lessons,
                                         style="dash.TButton",
                                         command=self.lessons_list)
        self.lessons_button.tooltip = tooltip.ToolTip(self.lessons_button, "View Lessons Created")

        self.create_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_create,
                                        style="dash.TButton",
                                        command=self.create_lesson)
        self.create_button.tooltip = tooltip.ToolTip(self.create_button, "Create a new Lesson")
        self.timer_button.grid(row=0, column=0, padx=20, sticky=tk.NW)
        self.edit_button.grid(row=0, column=1, padx=20, sticky=tk.NW)
        self.print_assessment_button.grid(row=0, column=4, sticky=tk.NE)
        self.flash_button.grid(row=0, column=3, sticky=tk.NE)
        self.class_button.grid(row=1, column=4, sticky=tk.SE)
        self.notes_button.grid(row=1, column=3, padx=50, sticky=tk.SE)
        self.lessons_button.grid(row=1, column=0, sticky=tk.SW)
        self.create_button.grid(row=1, column=1, padx=20, sticky=tk.SW)
        self.player_button.grid(row=0, column=2, padx=20, sticky=tk.NE)
        self.content_button.grid(row=1, column=2, sticky=tk.SW,padx=20)

    def show_names(self,frame, names,n_index):
        #try:
            if(n_index == len(names)):
                n_index = 0
            if len(names) == 0:
                return
            self.leader_data_label = tk.Label(frame,text=names[n_index][0],borderwidth=3, highlightcolor="gray16", width=25,
                                             font=("Helvetica", 16, 'bold'),
                                             background="gray16", foreground=FOREGROUND_COLOR)
            self.leader_data_label.grid(row=1,column=0)
            self.after(5000,self.show_names,frame,names,n_index+1)
        #except:
         #   logger.info("Exception in retrieving lessons information")
          #  logger.info(traceback.print_exc()),

    def launch_lesson_edit(self):

        launch_edit = MagicEditWizard.MagicEditWizard(self)
        launch_edit.geometry("1300x700+20+20")
        #if os.name == "nt":
         #   print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Edit"+os.path.sep+"Lesson_Edit.exe"))
         #   #os.system(os.getcwd() + os.path.sep + "app" + os.path.sep + "lesson_edit.exe")
         #   subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Edit"+os.path.sep+"Lesson_Edit.exe"))

    def launch_flashcard(self):
        launch_flashcard = FlashCard.MagicFlashApplication(self)
        launch_flashcard.geometry("1300x700+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Revise"+os.path.sep+"Lesson_Revise.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Revise"+os.path.sep+"Lesson_Revise.exe"))

    def launch_assessment_pdf(self):
        launch_assessment = assessment_viewer.MagicAssessmentPrint(self)
        launch_assessment.geometry("700x300+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Assess"+os.path.sep+"Lesson_Assess.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Assess"+os.path.sep+"Lesson_Assess.exe"))

    def launch_class_data(self):
        launch_class = magic_classroom_info.MagicClassRoomData(self)
        launch_class.geometry("1300x700+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Class_Data"+os.path.sep+"Lesson_Class_Data.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Class_Data"+os.path.sep+"Lesson_Class_Data.exe"))

    def launch_player(self):
        launch_player = magiccontainer.MagicApplication(self)
        launch_player.geometry("1400x800+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Play"+os.path.sep+"Lesson_Play.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Play"+os.path.sep+"Lesson_Play.exe"))

    def launch_pdf_notes(self):
        launch_notes = snapshot_view.SnapshotView(self)
        launch_notes.geometry("700x300+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_PDF_Notes"+os.path.sep+"Lesson_PDF_Notes.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_PDF_Notes"+os.path.sep+"Lesson_PDF_Notes.exe"))

    def lessons_list(self):
        launch_lessonlist = Lesson_List_Display.MagicLessonList(self)
        launch_lessonlist.geometry("1000x700+20+20")
         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_List"+os.path.sep+"Lesson_List.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_PDF_Notes"+os.path.sep+"Lesson_PDF_Notes.exe"))

    def create_lesson(self):
        launch_Create = create_explainer_content.MagicWizard(self)
        launch_Create.geometry("1300x700+20+20")


         # if os.name == "nt":
         #    print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Create"+os.path.sep+"Lesson_Create.exe"))
         #    subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Create"+os.path.sep+"Lesson_Create.exe"))

    def launch_timer(self):
        launch_timer = Timer_Display.TimerDisplay(self)
        launch_timer.resizable(width=False,height=False)
        launch_timer.attributes("-topmost", True)
        launch_timer.geometry("240x250+20+20")
        #if os.name == "nt":
         #   print(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Timer"+os.path.sep+"Lesson_Timer.exe"))
          #  subprocess.Popen(os.path.abspath(os.getcwd() + os.path.sep + ".." + os.path.sep + "Lesson_Timer"+os.path.sep+"Lesson_Timer.exe"))

    def tools_frame_create(self):
        self.tools_group_frame = tk.Frame(self, padx=10, pady=10, width=300, height=300, highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.tools_group_frame.grid(row=2, column=1, padx=10,pady = 10)
        self.image_tools = PhotoImage(file="../images/tools.png")
        self.tools_header_label = tk.Label(self.tools_group_frame, compound=tk.LEFT,
                                                  image=self.image_tools,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Teacher Tools", font=("Helvetica", 16, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.tools_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)

        self.content_button = ttk.Button(self.tools_group_frame, text="Download",
                                       width=9,
                                       command=self.launch_content, style="dashboxbutton.TButton")
        self.print_notes_button = ttk.Button(self.tools_group_frame, text="Notes",
                                      width=8,
                                      command=self.launch_pdf_notes, style="dashboxbutton.TButton")
        self.print_assessment_button = ttk.Button(self.tools_group_frame, text="Assess",
                                             width=8,
                                             command=self.launch_assessment_pdf, style="dashboxbutton.TButton")
        self.timer_button = ttk.Button(self.tools_group_frame, text="Timer",
                                                  width=8,
                                                  command=self.launch_timer, style="dashboxbutton.TButton")

        self.content_label = tk.Label(self.tools_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Images and Videos",
                                    font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
        self.timer_label = tk.Label(self.tools_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Launch Timer",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.notes_label = tk.Label(self.tools_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Audio and Print Notes",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.assessment_label = tk.Label(self.tools_group_frame, borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="Assessments",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)

        self.content_label.grid(row=1, column=0, pady=5)
        self.content_button.grid(row=1, column=1, pady=5)

        self.timer_label.grid(row=2, column=0, pady=5)
        self.timer_button.grid(row=2, column=1, pady=5)

        self.notes_label.grid(row=4, column=0, pady=5)
        self.print_notes_button.grid(row=4, column=1, pady=5)

        self.assessment_label.grid(row=5, column=0, pady=5)
        self.print_assessment_button.grid(row=5, column=1, pady=5)

    def flash_frame_create(self):
        self.flash_group_frame = tk.Frame(self, padx=10, pady=10, width=300, height=300, highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.flash_group_frame.grid(row=3, column=0, padx=10,pady = 0,sticky=tk.N)
        self.image_flash = PhotoImage(file="../images/chalkboard.png")
        self.flash_header_label = tk.Label(self.flash_group_frame, compound=tk.LEFT,
                                                  image=self.image_flash,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=250,
                                                  text=" Interactions", font=("Helvetica", 16, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.flash_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.flash_image_scroll_frame = tk.Frame(self.flash_group_frame, width=200, height=200,
                                                   background="gray18")
        self.flash_image_scroll_frame.rowconfigure(0, weight=1)
        self.flash_image_scroll_frame.columnconfigure(0, weight=1)
        self.flash_image_scroll_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.flash_list = DataCaptureDashboard.get_flash_images()
        flash_image_index = 0
        self.flash_image_display_scroll(self.flash_image_scroll_frame, self.flash_list, flash_image_index)
        self.play_button = ttk.Button(self.flash_group_frame, text="Start",
                                       width=7,
                                       command=self.launch_player, style="dashboxbutton.TButton")
        self.cards_button = ttk.Button(self.flash_group_frame, text="Play",
                                      width=7,
                                      command=self.launch_flashcard, style="dashboxbutton.TButton")


        self.play_label = tk.Label(self.flash_group_frame,
                                    borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                    text="Lesson for your Class",
                                    font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                    foreground=BOX_FOREGROUND_COLOR)
        self.cards_label = tk.Label(self.flash_group_frame,
                                   borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=25,
                                   text="A game of Flashcards",
                                   font=("Helvetica", 12, 'bold'), background=BOX_BACKGROUND_COLOR,
                                   foreground=BOX_FOREGROUND_COLOR)



        self.play_label.grid(row=2, column=0, pady=5)
        self.play_button.grid(row=2, column=1, pady=5)

        self.cards_label.grid(row=3, column=0, pady=5)
        self.cards_button.grid(row=3, column=1, pady=5)


    def star_frame_create(self):
        self.star_group_frame = tk.Frame(self, padx=10, pady=10, width=300, height=300, highlightthickness=3,
                                                 highlightbackground="gray30", highlightcolor="gray30",
                                                 background="gray18")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.star_group_frame.grid(row=3, column=1, padx=10,pady = 10)
        self.image_star = PhotoImage(file="../images/cup_icon.png")
        self.star_header_label = tk.Label(self.star_group_frame, compound=tk.LEFT,
                                                  image=self.image_star,
                                                  borderwidth=3, highlightcolor="gray18", anchor=tk.W, width=30,
                                                  text=" Celebrate", font=("Helvetica", 16, 'bold'),
                                                  background=BOX_BACKGROUND_COLOR, foreground=BOX_FOREGROUND_COLOR)
        self.star_header_label.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.star_image_frame = tk.Frame(self.star_group_frame, width=200, height=200,
                                                   background="gray16")
        self.star_image_frame.rowconfigure(0, weight=1)
        self.star_image_frame.columnconfigure(0, weight=1)
        self.star_image_frame.grid(row=1, columnspan=3, sticky=tk.NSEW)
        self.star_list = DataCaptureDashboard.get_badge_1_count()
        self.star_image = PhotoImage(file="../images/stars.png")
        self.star_image_display=tk.Label(self.star_image_frame,image=self.star_image,borderwidth=3, highlightcolor="gray16",
                                           background="gray16", foreground=BOX_FOREGROUND_COLOR)
        self.star_image_display.grid(row=0,column=0,pady=2)
        star_image_index = 0
        self.show_names(self.star_image_frame, self.star_list, star_image_index)




if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.configure(background="gray18")
    dashboard_app.title("Learning Room Dashboard")
    screen_width = dashboard_app.winfo_screenwidth()
    screen_height = dashboard_app.winfo_screenheight()

    screen_half_width = int(dashboard_app.winfo_screenwidth())
    screen_half_height = int(dashboard_app.winfo_screenheight())
    dashboard_app.geometry("1300x700+20+20")
    frame = MagicDashboard(dashboard_app)

    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0,sticky=tk.EW)
    dashboard_app.mainloop()

