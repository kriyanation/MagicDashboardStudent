import tkinter as tk
import DashLeaderBoard
from tkinter import ttk, PhotoImage

class MagicDashboard(tk.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.configure(background="gray25")
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('time.Label', background='dark slate gray', foreground='peachpuff2', font=('arial', 30, 'bold'))
        s.configure('dash.TButton', background='gray25', foreground='peachpuff2', borderwidth=0)
        s.map('dash.TButton', background=[('pressed', 'peachpuff'), ('active', '!disabled', 'gray44')],
              foreground=[('pressed', 'peachpuff2'), ('active', 'peachpuff2')])

        s.configure('dash.TLabelframe', background='gray25',bordercolor='peachpuff2',borderwidth=3)
        s.configure('dash.TLabelframe.Label', font=('courier', 14, 'bold', 'italic'))
        s.configure('dash.TLabelframe.Label', foreground='peachpuff2',background="gray25")
        s.configure('dashheader.Label', background='steel blue', foreground='snow', font=('comic sans', 12, 'bold','italic'))
        s.configure('dashdata.Label', background='steel blue', foreground='snow', font=('arial', 50, 'bold'))
        s.configure('dash2header.Label', background='gray16', foreground='snow',
                    font=('comic sans', 12, 'bold', 'italic'))
        s.configure('dash2data.Label', background='gray16', foreground='snow', font=('arial', 50, 'bold'))

        self.dashboard_launcher_labelframe= ttk.LabelFrame(self,text="Launcher",style="dash.TLabelframe")
        self.dashboard_launcher_labelframe.grid(row=0,column=0)

        self.image_timer = PhotoImage(file="../images/Timer.png")
        self.image_edit = PhotoImage(file="../images/edit_lesson.png")
        self.image_flash = PhotoImage(file="../images/flashcards.png")
        self.image_print_assessment = PhotoImage(file="../images/print_assessment.png")
        self.image_class = PhotoImage(file="../images/class_data.png")
        self.image_player = PhotoImage(file="../images/player_button.png")
        self.lesson_notes = PhotoImage(file="../images/notes.png")
        self.list_lessons = PhotoImage(file="../images/List_Lessons.png")
        self.image_create = PhotoImage(file="../images/create_lesson.png")

        self.timer_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_timer, style="dash.TButton",
                                           command="")
        self.edit_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_edit,
                                            style="dash.TButton",
                                            command="")
        self.flash_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_flash,
                                            style="dash.TButton",
                                            command="")
        self.print_assessment_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_print_assessment,
                                            style="dash.TButton",
                                            command="")
        self.class_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_class,
                                            style="dash.TButton",
                                            command="")
        self.player_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_player,
                                            style="dash.TButton",
                                            command="")
        self.notes_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.lesson_notes,
                                            style="dash.TButton",
                                            command="")
        self.lessons_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.list_lessons,
                                            style="dash.TButton",
                                            command="")
        self.create_button = ttk.Button(self.dashboard_launcher_labelframe, text="", image=self.image_create,
                                            style="dash.TButton",
                                            command="")
        self.timer_button.grid(row=0,column=0,sticky=tk.NW)
        self.edit_button.grid(row=0, column=1, sticky=tk.NW)
        self.print_assessment_button.grid(row=0, column=4, sticky=tk.NE)
        self.flash_button.grid(row=0, column=3, sticky=tk.NE)
        self.class_button.grid(row=1, column=4, sticky=tk.SE)
        self.notes_button.grid(row=1, column=3,padx=60, sticky=tk.SE)
        self.lessons_button.grid(row=1, column=0, sticky=tk.SW)
        self.create_button.grid(row=1, column=1, sticky=tk.SW)
        self.player_button.grid(row=0, column=2, rowspan=2,sticky=tk.NSEW)

        self.dashboard_info_labelframe = ttk.LabelFrame(self, text="Interesting Information", style="dash.TLabelframe")
        self.dashboard_info_labelframe.grid(row=1, column=0,pady= 30)
        self.lessons_frame=tk.Frame(self.dashboard_info_labelframe,background="steel blue",highlightbackground='black',highlightthickness=3)
        self.lessons_header_label = ttk.Label(self.lessons_frame,text="Number of Lessons", style="dashheader.Label")
        self.lessons_data_label = ttk.Label(self.lessons_frame, text="10",
                                       style="dashdata.Label")
        self.lessons_frame.grid(row=0,column=0,sticky=tk.NW)
        self.lessons_header_label.grid(row=0,column=0)
        self.lessons_data_label.grid(row=1, column=0)

        self.participants_frame = tk.Frame(self.dashboard_info_labelframe, background="gray16",
                                      highlightbackground='aquamarine', highlightthickness=3)
        self.participants_header_label = ttk.Label(self.participants_frame, text="Number of Participants", style="dash2header.Label")
        self.participants_data_label = ttk.Label(self.participants_frame, text="22",
                                            style="dash2data.Label")
        self.participants_frame.grid(row=0, column=1, sticky=tk.NW,padx=20)
        self.participants_header_label.grid(row=0, column=0)
        self.participants_data_label.grid(row=1, column=0)

        self.leader_frame = tk.Frame(self.dashboard_info_labelframe, background="steel blue",
                                      highlightbackground='black', highlightthickness=3)
        self.leaderboard = DashLeaderBoard.MagicLeaderBoard(self.leader_frame)
        self.leader_frame.grid(row=0, rowspan=2,column=4, sticky=tk.NE)
        self.leaderboard.grid(row=0,column=0)



if __name__== "__main__":
    dashboard_app = tk.Tk()
    dashboard_app.configure(background="gray25")
    dashboard_app.title("Learning Room Dashboard")
    dashboard_app.geometry("800x800")
    frame = MagicDashboard(dashboard_app)
    #dashboard_app.rowconfigure(0,weight=1)
    dashboard_app.columnconfigure(0, weight=1)
    frame.grid(row=0,column=0)
    dashboard_app.mainloop()


