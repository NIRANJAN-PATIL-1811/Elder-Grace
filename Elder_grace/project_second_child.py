from datetime import datetime
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import IntVar, StringVar, filedialog, messagebox, ttk
from customtkinter import *
from screeninfo import get_monitors
from tkcalendar import *
from io import BytesIO
from fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import sys


COLOR = '#4C2A85'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def list_to_string(s):
    str1 = ""
    return (str1.join(s))

def listtostring(s):
    str1 = ""
    return (str1.join(s))

pention_list = []

def tuple_to_string(s):
    result_string = ''.join(map(str, s))
    return result_string


def capitalize_input(input_str):
    words = input_str.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)



win = tk.Tk()

for monitor in get_monitors():
    WIDTH = monitor.width
    HEIGHT = monitor.height

win.title("Second ChildHood")
win.geometry(f"{WIDTH}x{HEIGHT}")

icon_image = Image.open(resource_path("shantai.ico"))  # Use the actual path and image format
icon_photo = ImageTk.PhotoImage(icon_image)

win.wm_iconphoto(False, icon_photo)




def first_page():
    first_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
    
    def inner_first_page():
        image1 = Image.open(resource_path("shantai_original.png"))
        resized_image2 = image1.resize((WIDTH, HEIGHT))
        img = ImageTk.PhotoImage(resized_image2)

        # Create a Label Widget to display the text or Image
        label1 = CTkLabel(win, image = img)
        label1.image = img
        label1.place(relx=0.5, rely=0.5, anchor='center')

        frame1 = CTkFrame(label1, width=500, height=420, fg_color='#D6D7E8')
        frame1.place(relx=0.5, rely=0.5, anchor='center')
        
        # Login label
        login_label = CTkLabel(frame1, text='Login', text_color=COLOR, font=("Times New Roman", 40), fg_color='#D6D7E8').place(relx=0.5, rely=0.1, anchor='center')

        username_entry = CTkEntry(frame1, width=400, font=("Times New Roman", 20), border_color=COLOR, placeholder_text="Username")
        username_entry.place(relx=0.5, rely=0.3, anchor='center')

        password_entry = CTkEntry(frame1, width=400, font=("Times New Roman", 20), border_color=COLOR, placeholder_text="Password", show="*")
        password_entry.place(relx=0.5, rely=0.5, anchor='center')


        def after_login():
            conn = sqlite3.connect(resource_path("second_child.db"))
            cr = conn.cursor()
            usernamex = cr.execute("SELECT username from new_account").fetchall()
            passwordx = cr.execute("SELECT password from new_account").fetchall()
            
            def check_username():
                for i in range(len(usernamex)):
                    if username_entry.get() != tuple_to_string(usernamex[i]):
                        return False
                    else:
                        return True
                    
            def check_password():
                for i in range(len(passwordx)):
                    if password_entry.get() != tuple_to_string(passwordx[i]):
                        return False
                    else:
                        return True



            if username_entry.get() == '':
                messagebox.showerror("Error", "Please Enter Valid Username!")
                username_entry.delete(0, 'end')

            elif password_entry.get() == '':
                messagebox.showerror("Error", "Please Enter Valid Password!")
                password_entry.delete(0, 'end')

            elif check_username() == False:
                messagebox.showerror("Error", "Entered Username Not Found!")
                username_entry.delete(0, 'end')

            elif check_password() == False:
                messagebox.showerror("Error", "Entered password Not Found!")
                password_entry.delete(0, 'end')

            else:
                def home_page():
                    # ==========================
                    def view_all_users():
                        # ========================
                        view_user_information_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
                        view_user_information_frame.place(relx=0.5, rely=0.5, anchor='center')

                        # search bar
                        search_bar = CTkEntry(view_user_information_frame, width=400, border_color=COLOR, font=("Times New Roman", 20), placeholder_text="eg. Name")
                        search_bar.place(relx=0.46, rely=0.2, anchor='center')

                        conn = sqlite3.connect(resource_path("second_child.db"))
                        cr = conn.cursor()



                        # ======================================================================
                        
                        def verify_data(final_residence):
                            def fetch_data():
                                # Connect to the SQLite database
                                conn = sqlite3.connect(resource_path('second_child.db'))
                                cursor = conn.cursor()

                                # Fetch all data from the 'students' table
                                if final_residence is None:
                                    cursor.execute("SELECT first_name, last_name, username, password FROM new_account")
                                    data = cursor.fetchall()
                                    return data
                                else:
                                    try:
                                        cursor.execute(f"SELECT first_name, last_name, username, password FROM new_account where first_name = '{final_residence}'")
                                        data5 = cursor.fetchall()
                                        return data5
                                    except:
                                        messagebox.showerror("Error", "This Name Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')


                            columns = ('First Name', 'Last Name', 'Username', 'Password')
                            tree = ttk.Treeview(view_user_information_frame, columns=columns, show='headings')

                            tree.column("First Name", width=100) 
                            tree.column("Last Name", width=100)
                            tree.column("Username", width=100)
                            tree.column("Password", width=100)
                        

                            def set_alternate_row_colors(tree, color1, color2):
                                for i, item in enumerate(tree.get_children()):
                                    color = color1 if i % 2 == 0 else color2
                                    tree.item(item, tags=(f"row_{i}",))
                                    tree.tag_configure(f"row_{i}", background=color)

                            for col in columns:
                                tree.heading(col, text=col)
                                tree.column(col, anchor='center')

                            # Populate the Treeview with data
                            data = fetch_data()
                            for row in data:
                                tree.insert('', 'end', values=row)
                                tree.tag_configure(tagname=row, background='cyan')
                                set_alternate_row_colors(tree, "lightblue", "#ebc7f9")
                                # tree.tag_add(tag_name, row_index)

                            style = ttk.Style()
                
                            # Set font size for column headings
                            style.configure("Treeview.Heading", font=("Times New Roman", 14))
                            style.configure("Treeview", font=("Times New Roman", 12))
                                        

                            # Add a vertical scrollbar to the Treeview
                            scrollbar = ttk.Scrollbar(view_user_information_frame, orient='vertical', command=tree.yview)
                            tree.configure(yscrollcommand=scrollbar.set)
                            # Pack the Treeview and Scrollbar
                            tree.place(relx=0.495, rely=0.475, anchor='center', width=WIDTH, height=600)
                            # tree.pack(expand=True, fill="both")
                            scrollbar.place(relx=0.895, rely=0.475, anchor='center', height=600)

                            def delete_all_record():                                
                                try:
                                    selected_item = tree.selection()
                                    username = tree.item(selected_item, "values")[2]

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()

                                    
                                    try:
                                        cr.execute(f"DELETE FROM new_account WHERE username = '{username}'")
                                        messagebox.showinfo("Detete Information", "Record Has Been Deleted!")
                                        conn.commit()
                                        view_all_users()
                                    except:
                                        pass
                                                                        
                                except:
                                    messagebox.showerror("Error", "Please Select A row")

                            # delete btn
                            delete_btn = CTkButton(view_user_information_frame, text='Delete', font=("Times New Roman", 22), fg_color=COLOR, command=delete_all_record).place(relx=0.5, rely=0.76, anchor='center')


                        def search_data():
                            residence_name = capitalize_input(search_bar.get())

                            if residence_name == "":
                                messagebox.showerror("Error", "Please Enter Name")
                            else:   
                                try:                                
                                    resi_var2 = cr.execute(f"SELECT first_name from new_account where first_name = '{residence_name}'")
                                    final_residence2 = resi_var2.fetchone()
                                    final_residence3 = list_to_string(final_residence2)

                                    if residence_name in final_residence3:                                    
                                        verify_data(residence_name)
                                    else:
                                        pass
                                except:
                                    messagebox.showerror("Error", "Entered Value Does Not Exist In This System!")
                                    search_bar.delete(0, 'end')
                                    

                        # search button
                        search_button = CTkButton(view_user_information_frame, text="Search", font=("Times New Roman", 22), fg_color="#3377ff", command=search_data)
                        search_button.place(relx=0.62, rely=0.2, anchor='center')

                        verify_data(final_residence=None)
                        # ======================



                    # ===========================
                
                    def add_information():
                        add_information_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
                        add_information_frame.place(relx=0.5, rely=0.5, anchor='center')

                        # residence information label
                        residence_label = CTkLabel(add_information_frame, text="New Residence Information", font=("Times New Roman", 50), text_color=COLOR)
                        residence_label.place(relx=0.5, rely=0.175, anchor='center')


                        # Name entry
                        name_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), width=600, border_color=COLOR,placeholder_text='Full Name *')
                        name_entry.place(relx=0.3, rely=0.25, anchor='center')

                        # Age label
                        age_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), width=600, border_color=COLOR,placeholder_text='Age *')
                        age_entry.place(relx=0.3, rely=0.348, anchor='center')
                        
                        
                         # date_update = datetime.date.today()
                        def cal_fun_first():
                            # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                            calender_toplevel = tk.Toplevel(add_information_frame, bg=COLOR)
                            calender_toplevel.title("Registration Date")
                            calender_toplevel.geometry("400x400")
                            calender_toplevel.resizable(False, False)

                            # cal_var = StringVar()
                            def selectDate(): 
                                global registration_date      
                                myDate = mycal1.get_date()
                                registration_date = myDate
                                selectDate = CTkLabel(add_information_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                selectDate.place(relx=0.3, rely=0.45, anchor='center')
                                calender_toplevel.destroy()
                                

                            mycal1 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                            mycal1.place(relx=0.5, rely=0.4, anchor='center')

                            open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectDate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                            

                            
                            
                        # cal_button
                        cal_button = CTkButton(add_information_frame, text='Choose Registration Date', font=("Times New Roman", 18), command=cal_fun_first).place(relx=0.195, rely=0.45, anchor='center')
                        

                        # Gender label
                        gender_label = CTkLabel(add_information_frame, text="Gender", font=("Times New Roman", 28), width=50)
                        gender_label.place(relx=0.166, rely=0.55, anchor='center')


                        gender = StringVar()
                        gender.set("Male")

                        # Gender Male
                        gender_male = CTkRadioButton(add_information_frame, text="Male", value="Male", variable=gender, font=("Times New Roman", 18))
                        gender_male.place(relx=0.29, rely=0.55, anchor='center')

                        # Gender Female
                        gender_female = CTkRadioButton(add_information_frame, text="Female", value="Female", variable=gender, font=("Times New Roman", 18))
                        gender_female.place(relx=0.37, rely=0.55, anchor='center')

                        # Gender Other
                        gender_other = CTkRadioButton(add_information_frame, text="Other", value="Other", variable=gender, font=("Times New Roman", 18))
                        gender_other.place(relx=0.445, rely=0.55, anchor='center')





                        # Address line 1 entry
                        address_line_1_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Address Line 1 *')
                        address_line_1_entry.place(relx=0.3, rely=0.65, anchor='center')



                        # line_2 = StringVar()


                        # Address line 2 entry
                        address_line_2_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Address Line 2 *')
                        address_line_2_entry.place(relx=0.3, rely=0.75, anchor='center')


                        # Aadhar number entry
                        adhar_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Adhar Number *')
                        adhar_entry.place(relx=0.7, rely=0.25, anchor='center')


                        mobile_entry = CTkEntry(add_information_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Mobile Number *')
                        mobile_entry.place(relx=0.7, rely=0.35, anchor='center')                 
                        
                        
                        # select image button
                        # global image_path
                        def select_image():
                            # global image_path
                            
                            image_path = filedialog.askopenfilename(initialdir='/', title="Select Image", filetypes=[("png files", ".png"), ("jpg files", ".jpg"), ("jpeg files", ".jpeg")])
                              
                            image = Image.open(resource_path(image_path))

                            resized_image = image.resize((200, 250))
                            image2 = ImageTk.PhotoImage(resized_image)

                            label = CTkLabel(add_information_frame, image=image2, text="")
                            label.image = image2
                            label.place(relx=0.704, rely=0.5, anchor='center')

                            try:
                                return image_path
                            except:
                                return ""

                               
                            
                        # select_image_button = CTkButton(add_information_frame, text="Add Image", width=200, font=("Times New Roman", 18), command=select_image)
                        # select_image_button.place(relx=0.705, rely=0.65, anchor='center')

                        # Dummy image
                        image = Image.open(resource_path("old_human_dummy2.png"))

                        resized_image = image.resize((200, 250))
                        image2 = ImageTk.PhotoImage(resized_image)

                        image_label = CTkLabel(add_information_frame, image=image2, text="")
                        image_label.image = image2
                        image_label.place(relx=0.704, rely=0.5, anchor='center')


                        def get_all_registration_info():
                            Name = name_entry.get()
                            Age = age_entry.get()
                            Gender = gender.get()
                            
                            try:
                                Date = registration_date
                            except:
                                current_date = datetime.now()

                                # Format the date as "dd/mm/yy"
                                Date = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'
                            

                            Line_1 = address_line_1_entry.get()
                            Line_2 = address_line_2_entry.get()
                            Adhar = adhar_entry.get()

                            Mobile = mobile_entry.get()
                            
                            
                            # try:
                            #     with open(image_path, 'rb') as image_file:
                            #         Photo = image_file.read()                            
                            # except:
                            #     Photo = ""
                            
                            try:
                                image_path = select_image()
                                with open(image_path, 'rb') as image_file:
                                    Photo = image_file.read()                            
                            except:
                                Photo = ""
                                
                            conn = sqlite3.connect(resource_path("second_child.db"))
                            cr = conn.cursor()
                            cr.execute("PRAGMA foreign_keys = ON")


                            def adhar_val():
                                try:
                                    adhar_details = cr.execute("SELECT adhar FROM residence_registration_table")
                                    adhar_det = adhar_details.fetchall()
                                    adhar_det2 = tuple_to_string(adhar_det)
                                    print(len(adhar_det2))
                                    print(adhar_det2)
                                    if Adhar in adhar_det2:
                                        return True
                                    else:
                                        return False
                                except:
                                    pass


                            
                            # # validation
                            if Name.isnumeric() == True or Name == "":
                                messagebox.showerror("Error", "Please Enter Valid Name")
                                name_entry.delete(0, 'end')
                            elif Age.isnumeric() == False or Age == "" :
                                messagebox.showerror("Error", "Please Enter Valid Age")
                                age_entry.delete(0, 'end')                  
                            elif Line_1 == "":
                                messagebox.showerror("Error", "Please Fill Address Line 1")
                            elif Line_2 == "":
                                messagebox.showerror("Error", "Please Fill Address Line 2")
                            elif Adhar.isnumeric() == False or Adhar == "" or len(Adhar) != 12:
                                messagebox.showerror("Error", "Please Enter Valid Adhar")
                                adhar_entry.delete(0, 'end')
                            elif adhar_val() == True:
                                messagebox.showerror("Error", "Adhar Number Is Already Exists In System")
                                adhar_entry.delete(0, 'end')
                            elif Mobile.isnumeric() == False or Mobile == "" or len(Mobile) != 10:
                                messagebox.showerror("Error", "Please Enter Valid Mobile")
                                mobile_entry.delete(0, 'end')
                            # elif Photo == "":
                            #     messagebox.showerror("Error", "Please Select Photo")
                            else: 

                                
                                # Capitalize the first letter of each word
                                capitalized_name = capitalize_input(Name)
                                                

                                #residence registration table
                                try:
                                    cr.execute('''create table if not exists residence_registration_table(
                                            name text, 
                                            age text, 
                                            date text, 
                                            gender text, 
                                            address_line_1 text, 
                                            address_line_2 text, 
                                            adhar TEXT PRIMARY KEY,
                                            mobile TEXT,
                                            photo BLOB
                                            )''')
                                    
                                    cr.execute('''insert into residence_registration_table(
                                            name, 
                                            age, 
                                            date, 
                                            gender, 
                                            address_line_1, 
                                            address_line_2, 
                                            adhar,
                                            mobile,
                                            photo
                                            ) values(?,?,?,?,?,?,?,?,?)''',
                                            (capitalized_name, Age, Date, Gender, Line_1, Line_2, Adhar, Mobile, sqlite3.Binary(Photo)))
                                
                                    conn.commit()
                                                                
                                    
                                except:
                                    pass
                                        
                                # pention
                                try:
                                    if listtostring(pention_list) == "":
                                        pass
                                    else:
                                        cr.execute('''CREATE TABLE IF NOT EXISTS residence_pention(
                                                amount TEXT, 
                                                adhar TEXT, 
                                                FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))
                                                ''')
                                        
                                        cr.execute('''INSERT INTO residence_pention(
                                                amount, 
                                                adhar) values(?,?)''',
                                                (listtostring(pention_list), Adhar))
                                        conn.commit()
                                except:
                                    pass

                                # operation 1
                        #         try:
                        #             try:
                        #                 operation_date2 = operation_date
                        #             except:
                        #                 # current_date2 = datetime.now()
                        #                 operation_date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                        #             if name_of_operation == "":
                        #                 pass
                        #             else:
                        #                 cr.execute('''CREATE TABLE IF NOT EXISTS residence_operation_first(
                        #                         name TEXT, 
                        #                         date TEXT, 
                        #                         adhar TEXT, 
                        #                         FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))
                        #                         ''')
                                        
                        #                 cr.execute('''INSERT INTO residence_operation_first(
                        #                         name, 
                        #                         date, 
                        #                         adhar) values(?,?,?)''',
                        #                         (name_of_operation, operation_date2, Adhar)
                        #                         )
                                        
                        #                 conn.commit()
                        #         except:
                        #             pass

                        #         # operation 2
                        #         try:
                        #             try:
                        #                 operation_date22 = operation_date2
                        #             except:
                        #                 # current_date2 = datetime.now()
                        #                 operation_date22 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                        #             if name_of_operation2 == "":
                        #                 pass
                        #             else:
                        #                 cr.execute('''CREATE TABLE IF NOT EXISTS residence_operation_second(
                        #                         name TEXT, 
                        #                         date TEXT, 
                        #                         adhar TEXT, 
                        #                         FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))
                        #                         ''')
                                        
                        #                 cr.execute('''INSERT INTO residence_operation_second(
                        #                         name, 
                        #                         date, 
                        #                         adhar) values(?,?,?)''',
                        #                         (name_of_operation2, operation_date22, Adhar)
                        #                         )
                                        
                        #                 conn.commit()
                        #         except:
                        #             pass


                        #         # operation 3
                        #         try:
                        #             try:
                        #                 operation_date33 = operation_date3
                        #             except:
                        #                 # current_date2 = datetime.now()
                        #                 operation_date33 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                        #             if name_of_operation3 == "":
                        #                 pass
                        #             else:
                        #                 cr.execute('''CREATE TABLE IF NOT EXISTS residence_operation_third(
                        #                         name TEXT, 
                        #                         date TEXT, 
                        #                         adhar TEXT, 
                        #                         FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))
                        #                         ''')
                                        
                        #                 cr.execute('''INSERT INTO residence_operation_third(
                        #                         name, 
                        #                         date, 
                        #                         adhar) values(?,?,?)''',
                        #                         (name_of_operation3, operation_date33, Adhar)
                        #                         )
                                        
                        #                 conn.commit()
                        #         except:
                        #             pass


                        #         # operation 4
                        #         try:
                        #             try:
                        #                 operation_date44 = operation_date4
                        #             except:
                        #                 # current_date2 = datetime.now()
                        #                 operation_date44 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                        #             if name_of_operation4 == "":
                        #                 pass
                        #             else:
                        #                 cr.execute('''CREATE TABLE IF NOT EXISTS residence_operation_fourth(
                        #                         name TEXT, 
                        #                         date TEXT, 
                        #                         adhar TEXT, 
                        #                         FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))
                        #                         ''')
                                        
                        #                 cr.execute('''INSERT INTO residence_operation_fourth(
                        #                         name, 
                        #                         date, 
                        #                         adhar) values(?,?,?)''',
                        #                         (name_of_operation4, operation_date44, Adhar)
                        #                         )
                                        
                        #                 conn.commit()
                        #         except:
                        #             pass

                                
                        #         # cr.execute('''create table if not exists residence_relative_first(relative_name text, relative_relation text, address_line_1 text, address_line_2 text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                        #         # cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_second(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #         # cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_third(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #         # cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_fourth(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #         # relative info
                        #         try:
                        #             if name_of_relative == "" and relation_with_recidence == "" and relative_line_1 == "" and relative_line_2 == "" and relative_mobile == "" and relative_adhar == "":
                        #                 pass
                        #             else:                               

                        #                 cr.execute('''create table if not exists residence_relative_first(relative_name text, relative_relation text, address_line_1 text, address_line_2 text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                        #                 cr.execute("insert into residence_relative_first (relative_name, relative_relation, address_line_1, address_line_2, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?,?)", (capitalize_input(name_of_relative), relation_with_recidence, relative_line_1, relative_line_2, relative_mobile, relative_adhar, Adhar))
                        #                 conn.commit()

                        #         except:
                        #             pass

                        #         try:
                        #             # ============
                        #             if name_of_relative2 == "" and relation_with_recidence2 == "" and relative_line_12 == "" and relative_line_22 == "" and relative_mobile2 == "" and relative_adhar2 == "":
                        #                 pass
                        #             else:                                   

                        #                 cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_second(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #                 cr.execute("INSERT INTO residence_relative_second(relative_name, relative_relation, address_line_1, address_line_2, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?,?)", (capitalize_input(name_of_relative2), relation_with_recidence2, relative_line_12, relative_line_22, relative_mobile2, relative_adhar2, Adhar))
                        #                 conn.commit()
                        #             # ============
                        #         except:
                        #             pass

                                
                        #         try:
                        #             # ==============
                        #             if name_of_relative23 == "" and relation_with_recidence23 == "" and relative_line_123 == "" and relative_line_223 == "" and relative_mobile23 == "" and relative_adhar23 == "":
                        #                 pass
                        #             else:                                       

                        #                 cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_third(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #                 cr.execute("INSERT INTO residence_relative_third(relative_name, relative_relation, address_line_1, address_line_2, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?,?)", (capitalize_input(name_of_relative23), relation_with_recidence23, relative_line_123, relative_line_223, relative_mobile23, relative_adhar23, Adhar))
                        #                 conn.commit()
                        #             # ===========
                        #         except:
                        #             pass


                        #         try:
                        #             # =============
                        #             if name_of_relative234 == "" and relation_with_recidence234 == "" and relative_line_1234 == "" and relative_line_2234 == "" and relative_mobile234 == "" and relative_adhar234 == "":
                        #                 pass
                        #             else:
                        #                 cr.execute("CREATE TABLE IF NOT EXISTS residence_relative_fourth(relative_name TEXT, relative_relation TEXT, address_line_1 TEXT, address_line_2 TEXT, relative_mobile TEXT, relative_adhar TEXT, adhar TEXT, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                        #                 cr.execute("INSERT INTO residence_relative_fourth(relative_name, relative_relation, address_line_1, address_line_2, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?,?)", (capitalize_input(name_of_relative234), relation_with_recidence234, relative_line_1234, relative_line_2234, relative_mobile234, relative_adhar234, Adhar))
                        #                 conn.commit()
                        # # ==============
                        #         except:
                        #             pass
                                
                                    
                                # conn.commit()
                                # conn.close()
                                
                                messagebox.showinfo("Information","Record Has Been Succesfully Saved!")
                                add_information()
                                
                                
                            
                        # Resister button
                        resister_button = CTkButton(add_information_frame, text="Add Image & Resister", font=("Times New Roman",20), width=800, fg_color=COLOR, command=get_all_registration_info)
                        resister_button.place(relx=0.5, rely=0.8, anchor='center')


                    def add_new_relative():
                        add_new_relative_frame = CTkFrame(win, width=WIDTH, height=HEIGHT, fg_color='white')
                        add_new_relative_frame.place(relx=0.5, rely=0.5, anchor='center')

                        common_adhar = CTkEntry(add_new_relative_frame, width=400, border_color=COLOR, font=("Times New Roman", 20), placeholder_text="Residence Adhar Number *")
                        common_adhar.place(relx=0.5, rely=0.2, anchor='center')

                        # Create a parent frame
                        child_frame1 = CTkFrame(add_new_relative_frame, width=(WIDTH / 2.75), height=(HEIGHT / 1.75))
                        child_frame1.place(relx=0.3, rely=0.53, anchor='center')

                        def relative_1():
                            relative_name1 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relative Full Name *", border_color=COLOR)
                            relative_name1.place(relx=0.5, rely=0.2, anchor='center')
                            
                            relative_relation1 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relation * ", border_color=COLOR)
                            relative_relation1.place(relx=0.5, rely=0.35, anchor='center')
                            
                            relative_address1 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Full Address *", border_color=COLOR)
                            relative_address1.place(relx=0.5, rely=0.5, anchor='center')
                                                        
                            relative_adhar1 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Adhar *", border_color=COLOR)
                            relative_adhar1.place(relx=0.5, rely=0.65, anchor='center')
                            
                            relative_mobile1 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Mobile *", border_color=COLOR)
                            relative_mobile1.place(relx=0.5, rely=0.8, anchor='center')

                            def get_relative_info_1():
                                name = relative_name1.get()
                                relation = relative_relation1.get()
                                address = relative_address1.get()
                                adhar = relative_adhar1.get()
                                Adhar = common_adhar.get()
                                mobile = relative_mobile1.get()

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence's Adhar")
                                    common_adhar.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    relative_name1.delete(0, 'end')

                                elif relation == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Relation")
                                    relative_relation1.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")
                                    relative_address1.delete(0, 'end')

                                elif adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Adhar")
                                    relative_adhar1.delete(0, 'end')

                                elif mobile == "" or mobile.isnumeric() == False or len(mobile) != 10:
                                    messagebox.showerror("Error", "Please Enter Valid Mobile")
                                    relative_mobile1.delete(0, 'end')

                                else:

                                    # Relative Adhar
                                    adhar_first = cr.execute("SELECT relative_adhar FROM residence_relative_first").fetchall()
                                    get_adhar_first = tuple_to_string(adhar_first)

                                    adhar_second = cr.execute("SELECT relative_adhar FROM residence_relative_second").fetchall()
                                    get_adhar_second = tuple_to_string(adhar_second)

                                    adhar_third = cr.execute("SELECT relative_adhar FROM residence_relative_third").fetchall()
                                    get_adhar_third = tuple_to_string(adhar_third)

                                    adhar_fourth = cr.execute("SELECT relative_adhar FROM residence_relative_fourth").fetchall()
                                    get_adhar_fourth = tuple_to_string(adhar_fourth)
                                    

                                    residence_adhar = cr.execute("SELECT adhar FROM residence_registration_table").fetchall()
                                    get_residence_adhar = tuple_to_string(residence_adhar)



                                    # Residence Adhar
                                    residence_adhar_first = cr.execute("SELECT adhar FROM residence_relative_first").fetchall()
                                    get_residence_adhar_first = tuple_to_string(residence_adhar_first)

                                    # residence_adhar_second = cr.execute("SELECT adhar FROM residence_relative_second").fetchall()
                                    # get_residence_adhar_second = tuple_to_string(residence_adhar_second)

                                    # residence_adhar_third = cr.execute("SELECT adhar FROM residence_relative_third").fetchall()
                                    # get_residence_adhar_third = tuple_to_string(residence_adhar_third)

                                    # residence_adhar_fourth = cr.execute("SELECT adhar FROM residence_relative_fourth").fetchall()
                                    # get_residence_adhar_fourth = tuple_to_string(residence_adhar_fourth)
                                    
                                    if Adhar not in get_residence_adhar:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")

                                    elif Adhar in get_residence_adhar_first:
                                        messagebox.showerror("Error", "The Residence Adhar Number Can Not Be Inseted Again For Relative 1")

                                    elif adhar in get_adhar_first or Adhar in get_adhar_second or Adhar in get_adhar_third or Adhar in get_adhar_fourth:
                                        messagebox.showerror("Error", "The Relative Adhar Number Can Not Be Inserted Again")                                                                           
                                                                        
                                    else:
                                        cr.execute('''create table if not exists residence_relative_first(relative_name text, relative_relation text, relative_address text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                                        cr.execute("insert into residence_relative_first (relative_name, relative_relation, relative_address, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(relation), address, mobile, adhar, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Relative 1 has been inserted!")
                                    

                            # register button
                            CTkButton(child_frame1, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=get_relative_info_1).place(relx=0.5, rely=0.95, anchor='center')

                        CTkButton(child_frame1, text='Relative 1', font=("Times New Roman", 20), fg_color=COLOR, command=relative_1).place(relx=0.175, rely=0.05, anchor='center')


                        def relative_2():
                            relative_name2 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relative Full Name *", border_color=COLOR)
                            relative_name2.place(relx=0.5, rely=0.2, anchor='center')
                            
                            relative_relation2 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relation * ", border_color=COLOR)
                            relative_relation2.place(relx=0.5, rely=0.35, anchor='center')
                            
                            relative_address2 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Full Address *", border_color=COLOR)
                            relative_address2.place(relx=0.5, rely=0.5, anchor='center')
                                                        
                            relative_adhar2 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Adhar *", border_color=COLOR)
                            relative_adhar2.place(relx=0.5, rely=0.65, anchor='center')
                            
                            relative_mobile2 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Mobile *", border_color=COLOR)
                            relative_mobile2.place(relx=0.5, rely=0.8, anchor='center')

                           
                            def get_relative_info_2():
                                name = relative_name2.get()
                                relation = relative_relation2.get()
                                address = relative_address2.get()
                                adhar = relative_adhar2.get()
                                Adhar = common_adhar.get()
                                mobile = relative_mobile2.get()

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence's Adhar")
                                    common_adhar.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    relative_name2.delete(0, 'end')

                                elif relation == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Relation")
                                    relative_relation2.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")
                                    relative_address2.delete(0, 'end')

                                elif adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Adhar")
                                    relative_adhar2.delete(0, 'end')

                                elif mobile == "" or mobile.isnumeric() == False or len(mobile) != 10:
                                    messagebox.showerror("Error", "Please Enter Valid Mobile")
                                    relative_mobile2.delete(0, 'end')

                                else:

                                    # Relative Adhar
                                    adhar_first = cr.execute("SELECT relative_adhar from residence_relative_first").fetchall()
                                    get_adhar_first = tuple_to_string(adhar_first)

                                    adhar_second = cr.execute("SELECT relative_adhar from residence_relative_second").fetchall()
                                    get_adhar_second = tuple_to_string(adhar_second)

                                    adhar_third = cr.execute("SELECT relative_adhar from residence_relative_third").fetchall()
                                    get_adhar_third = tuple_to_string(adhar_third)

                                    adhar_fourth = cr.execute("SELECT relative_adhar from residence_relative_fourth").fetchall()
                                    get_adhar_fourth = tuple_to_string(adhar_fourth)
                                    

                                    residence_adhar = cr.execute("SELECT adhar from residence_registration_table").fetchall()
                                    get_residence_adhar = tuple_to_string(residence_adhar)
                                                                        
                                    # Residence Adhar
                                    # residence_adhar_first = cr.execute("SELECT adhar FROM residence_relative_first").fetchall()
                                    # get_residence_adhar_first = tuple_to_string(residence_adhar_first)

                                    residence_adhar_second = cr.execute("SELECT adhar FROM residence_relative_second").fetchall()
                                    get_residence_adhar_second = tuple_to_string(residence_adhar_second)

                                    # residence_adhar_third = cr.execute("SELECT adhar FROM residence_relative_third").fetchall()
                                    # get_residence_adhar_third = tuple_to_string(residence_adhar_third)

                                    # residence_adhar_fourth = cr.execute("SELECT adhar FROM residence_relative_fourth").fetchall()
                                    # get_residence_adhar_fourth = tuple_to_string(residence_adhar_fourth)
                                    
                                    if Adhar not in get_residence_adhar:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")

                                    elif Adhar in get_residence_adhar_second:
                                        messagebox.showerror("Error", "The Residence Adhar Number Can Not Be Inseted Again For Relative 2")
                                    
                                    elif adhar in get_adhar_first or Adhar in get_adhar_second or Adhar in get_adhar_third or Adhar in get_adhar_fourth:
                                        messagebox.showerror("Error", "The Relative Adhar Number Can Not Be Inserted Again")                                                                           
                                                                        
                                    else:
                                        cr.execute('''create table if not exists residence_relative_second(relative_name text, relative_relation text, relative_address text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                                        cr.execute("insert into residence_relative_second (relative_name, relative_relation, relative_address, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(relation), address, mobile, adhar, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Relative 2 has been inserted!")
                                    

                           
                            # register button
                            CTkButton(child_frame1, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=get_relative_info_2).place(relx=0.5, rely=0.95, anchor='center')
                        

                        CTkButton(child_frame1, text='Relative 2', font=("Times New Roman", 20), fg_color=COLOR, command=relative_2).place(relx=0.392, rely=0.05, anchor='center')


                        def relative_3():
                            relative_name3 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relative Full Name *", border_color=COLOR)
                            relative_name3.place(relx=0.5, rely=0.2, anchor='center')
                            
                            relative_relation3 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relation * ", border_color=COLOR)
                            relative_relation3.place(relx=0.5, rely=0.35, anchor='center')
                            
                            relative_address3 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Full Address *", border_color=COLOR)
                            relative_address3.place(relx=0.5, rely=0.5, anchor='center')
                                                        
                            relative_adhar3 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Adhar *", border_color=COLOR)
                            relative_adhar3.place(relx=0.5, rely=0.65, anchor='center')
                            
                            relative_mobile3 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Mobile *", border_color=COLOR)
                            relative_mobile3.place(relx=0.5, rely=0.8, anchor='center')

                            def get_relative_info_3():
                                name = relative_name3.get()
                                relation = relative_relation3.get()
                                address = relative_address3.get()
                                adhar = relative_adhar3.get()
                                Adhar = common_adhar.get()
                                mobile = relative_mobile3.get()

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence's Adhar")
                                    common_adhar.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    relative_name3.delete(0, 'end')

                                elif relation == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Relation")
                                    relative_relation3.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")
                                    relative_address3.delete(0, 'end')

                                elif adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Adhar")
                                    relative_adhar3.delete(0, 'end')

                                elif mobile == "" or mobile.isnumeric() == False or len(mobile) != 10:
                                    messagebox.showerror("Error", "Please Enter Valid Mobile")
                                    relative_mobile3.delete(0, 'end')

                                else:

                                    # Relative Adhar
                                    adhar_first = cr.execute("SELECT relative_adhar from residence_relative_first").fetchall()
                                    get_adhar_first = tuple_to_string(adhar_first)

                                    adhar_second = cr.execute("SELECT relative_adhar from residence_relative_second").fetchall()
                                    get_adhar_second = tuple_to_string(adhar_second)

                                    adhar_third = cr.execute("SELECT relative_adhar from residence_relative_third").fetchall()
                                    get_adhar_third = tuple_to_string(adhar_third)

                                    adhar_fourth = cr.execute("SELECT relative_adhar from residence_relative_fourth").fetchall()
                                    get_adhar_fourth = tuple_to_string(adhar_fourth)
                                    

                                    residence_adhar = cr.execute("SELECT adhar from residence_registration_table").fetchall()
                                    get_residence_adhar = tuple_to_string(residence_adhar)
                                    
                                    # Residence Adhar
                                    # residence_adhar_first = cr.execute("SELECT adhar FROM residence_relative_first").fetchall()
                                    # get_residence_adhar_first = tuple_to_string(residence_adhar_first)

                                    # residence_adhar_second = cr.execute("SELECT adhar FROM residence_relative_second").fetchall()
                                    # get_residence_adhar_second = tuple_to_string(residence_adhar_second)

                                    residence_adhar_third = cr.execute("SELECT adhar FROM residence_relative_third").fetchall()
                                    get_residence_adhar_third = tuple_to_string(residence_adhar_third)

                                    # residence_adhar_fourth = cr.execute("SELECT adhar FROM residence_relative_fourth").fetchall()
                                    # get_residence_adhar_fourth = tuple_to_string(residence_adhar_fourth)
                                    
                                    if Adhar not in get_residence_adhar:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")

                                    elif Adhar in get_residence_adhar_third:
                                        messagebox.showerror("Error", "The Residence Adhar Number Can Not Be Inseted Again For Relative 3")
                                   
                                    elif adhar in get_adhar_first or Adhar in get_adhar_second or Adhar in get_adhar_third or Adhar in get_adhar_fourth:
                                        messagebox.showerror("Error", "The Relative Adhar Number Can Not Be Inserted Again")                                                                           
                                                                        
                                    else:
                                        cr.execute('''create table if not exists residence_relative_third(relative_name text, relative_relation text, relative_address text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                                        cr.execute("insert into residence_relative_third (relative_name, relative_relation, relative_address, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(relation), address, mobile, adhar, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Relative 3 has been inserted!")
                                    


                            # register button
                            CTkButton(child_frame1, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=get_relative_info_3).place(relx=0.5, rely=0.95, anchor='center')

                        CTkButton(child_frame1, text='Relative 3', font=("Times New Roman", 20), fg_color=COLOR, command=relative_3).place(relx=0.608, rely=0.05, anchor='center')


                        def relative_4():
                            relative_name4 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relative Full Name *", border_color=COLOR)
                            relative_name4.place(relx=0.5, rely=0.2, anchor='center')
                            
                            relative_relation4 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Relation * ", border_color=COLOR)
                            relative_relation4.place(relx=0.5, rely=0.35, anchor='center')
                            
                            relative_address4 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Full Address *", border_color=COLOR)
                            relative_address4.place(relx=0.5, rely=0.5, anchor='center')
                            
                            relative_adhar4 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Adhar *", border_color=COLOR)
                            relative_adhar4.place(relx=0.5, rely=0.65, anchor='center')

                            relative_mobile4 = CTkEntry(child_frame1, width=500, font=("Times New Roman", 20), placeholder_text="Mobile *", border_color=COLOR)
                            relative_mobile4.place(relx=0.5, rely=0.8, anchor='center')

                            def get_relative_info_4():
                                name = relative_name4.get()
                                relation = relative_relation4.get()
                                address = relative_address4.get()
                                adhar = relative_adhar4.get()
                                Adhar = common_adhar.get()
                                mobile = relative_mobile4.get()

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence's Adhar")
                                    common_adhar.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    relative_name4.delete(0, 'end')

                                elif relation == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Relation")
                                    relative_relation4.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")
                                    relative_address4.delete(0, 'end')

                                elif adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Adhar")
                                    relative_adhar4.delete(0, 'end')

                                elif mobile == "" or mobile.isnumeric() == False or len(mobile) != 10:
                                    messagebox.showerror("Error", "Please Enter Valid Mobile")
                                    relative_mobile4.delete(0, 'end')

                                else:
                                    # Relative Adhar
                                    adhar_first = cr.execute("SELECT relative_adhar from residence_relative_first").fetchall()
                                    get_adhar_first = tuple_to_string(adhar_first)

                                    adhar_second = cr.execute("SELECT relative_adhar from residence_relative_second").fetchall()
                                    get_adhar_second = tuple_to_string(adhar_second)

                                    adhar_third = cr.execute("SELECT relative_adhar from residence_relative_third").fetchall()
                                    get_adhar_third = tuple_to_string(adhar_third)

                                    adhar_fourth = cr.execute("SELECT relative_adhar from residence_relative_fourth").fetchall()
                                    get_adhar_fourth = tuple_to_string(adhar_fourth)
                                    

                                    residence_adhar = cr.execute("SELECT adhar from residence_registration_table").fetchall()
                                    get_residence_adhar = tuple_to_string(residence_adhar)
                                    

                                    residence_adhar_fourth = cr.execute("SELECT adhar FROM residence_relative_fourth").fetchall()
                                    get_residence_adhar_fourth = tuple_to_string(residence_adhar_fourth)
                                    
                                    if Adhar not in get_residence_adhar:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")

                                    elif Adhar in get_residence_adhar_fourth:
                                        messagebox.showerror("Error", "The Residence Adhar Number Can Not Be Inseted Again For Relative 4")
                                    elif adhar in get_adhar_first or Adhar in get_adhar_second or Adhar in get_adhar_third or Adhar in get_adhar_fourth:
                                        messagebox.showerror("Error", "The Relative Adhar Number Can Not Be Inserted Again")                                                                           
                                                                        
                                    else:
                                        cr.execute('''create table if not exists residence_relative_fourth(relative_name text, relative_relation text, relative_address text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                                        cr.execute("insert into residence_relative_fourth (relative_name, relative_relation, relative_address, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(relation), address, mobile, adhar, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Relative 4 has been inserted!")
                                    

                            # register button
                            CTkButton(child_frame1, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=get_relative_info_4).place(relx=0.5, rely=0.95, anchor='center')

                        CTkButton(child_frame1, text='Relative 4', font=("Times New Roman", 20), fg_color=COLOR, command=relative_4).place(relx=0.825, rely=0.05, anchor='center')


                        
                        # CTkLabel(child_frame1, text='Relative 1', font=("Times New Roman", 20), text_color='red').place(relx=0.5, rely=0.1, anchor='center')

                        child_frame2 = CTkFrame(add_new_relative_frame, width=(WIDTH / 2.75), height=(HEIGHT / 1.75))
                        child_frame2.place(relx=0.7, rely=0.53, anchor='center')

                        pention_label = CTkLabel(child_frame2, text="Pention Information", font=("Times New Roman", 40), text_color=COLOR)
                        pention_label.place(relx=0.5, rely=0.1, anchor='center')

                        bank_name = CTkEntry(child_frame2, width=500, font=("Times New Roman", 20), placeholder_text="Banking Name *", border_color=COLOR)
                        bank_name.place(relx=0.5, rely=0.2, anchor='center')

                        bank_ifsc = CTkEntry(child_frame2, width=500, font=("Times New Roman", 20), placeholder_text="Bank IFSC Code *", border_color=COLOR)
                        bank_ifsc.place(relx=0.5, rely=0.35, anchor='center')

                        account_number = CTkEntry(child_frame2, width=500, font=("Times New Roman", 20), placeholder_text="Account Number *", border_color=COLOR)
                        account_number.place(relx=0.5, rely=0.5, anchor='center')

                        branch_name = CTkEntry(child_frame2, width=500, font=("Times New Roman", 20), placeholder_text="Branch Name *", border_color=COLOR)
                        branch_name.place(relx=0.5, rely=0.65, anchor='center')

                        pention_amount = CTkEntry(child_frame2, width=500, font=("Times New Roman", 20), placeholder_text="Pention Amount *", border_color=COLOR)
                        pention_amount.place(relx=0.5, rely=0.8, anchor='center')

                        def add_pention():
                            name = bank_name.get()
                            ifsc = bank_ifsc.get()
                            account = account_number.get()
                            branch = branch_name.get()
                            pention = pention_amount.get()
                            adhar = common_adhar.get()

                            if adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                                messagebox.showerror("Error", "Please Enter Valid Adhar")
                                common_adhar.delete(0, 'end')

                            elif name == "" or name.isnumeric() == True:
                                messagebox.showerror("Error", "Please Enter Valid Name")
                                bank_name.delete(0, 'end')

                            elif ifsc == "" or len(ifsc) != 11:
                                messagebox.showerror("Error", "Please Enter Valid IFSC Code")
                                bank_ifsc.delete(0, 'end')

                            elif account == "" or account.isnumeric() == False or len(account) == 13 or len(account) < 11 or len(account) > 14:
                                messagebox.showerror("Error", "Please Enter Valid Account Number")
                                account_number.delete(0, 'end')

                            elif branch == "" or branch.isnumeric() == True:
                                messagebox.showerror("Error", "Please Enter Valid Branch Name")
                                branch_name.delete(0, 'end')

                            elif pention == "" or pention.isnumeric() == False:
                                messagebox.showerror("Error", "Please Enter Valid Pention Amount")
                                pention_amount.delete(0, 'end')

                            else:
                                adhar_from_res = cr.execute("SELECT adhar from residence_registration_table")
                                converted_val = adhar_from_res.fetchall()
                                resi_result = tuple_to_string(converted_val)

                                res_pention = cr.execute("SELECT adhar from residence_pention")
                                res_con = res_pention.fetchall()
                                res_result = tuple_to_string(res_con)
                                
                                if adhar not in resi_result:
                                    messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")
                                
                                elif adhar in res_result:
                                    messagebox.showerror("Error", "The Residence Adhar Number Is Already Present In Pention")

                                else:
                                    cr.execute("create table if not exists residence_pention (name text, ifsc text, account text, branch text, pention text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                                    cr.execute("insert into residence_pention (name, ifsc, account, branch, pention, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), ifsc, account, capitalize_input(branch), pention, adhar))

                                    conn.commit()
                                    messagebox.showinfo("Information", "Pention Has Been Added")
                                
                        CTkButton(child_frame2, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=add_pention).place(relx=0.5, rely=0.95, anchor='center')





                    def view_information():
                        view_information_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
                        view_information_frame.place(relx=0.5, rely=0.5, anchor='center')

                        # search bar
                        search_bar = CTkEntry(view_information_frame, width=400, border_color=COLOR, font=("Times New Roman", 20), placeholder_text="eg. Name or Adhar")
                        search_bar.place(relx=0.46, rely=0.2, anchor='center')

                        conn = sqlite3.connect(resource_path("second_child.db"))
                        cr = conn.cursor()



                        # ======================================================================
                        
                        def verify_data(final_residence):
                            def fetch_data():
                                # Connect to the SQLite database
                                conn = sqlite3.connect(resource_path('second_child.db'))
                                cursor = conn.cursor()

                                # Fetch all data from the 'students' table
                                if final_residence is None:
                                    cursor.execute(f'SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table')
                                    data = cursor.fetchall()
                                    return data
                                elif final_residence.isnumeric() == True:
                                    try:
                                        resi_var = cr.execute(f"SELECT adhar from residence_registration_table where adhar = '{final_residence}'")
                                        final_residence2 = resi_var.fetchone()
                                        final_residence3 = list_to_string(final_residence2)
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table where adhar = '{final_residence3}'")
                                        data2 = cursor.fetchall()
                                        return data2
                                    except:
                                        messagebox.showerror("Error", "This Adhar Number Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                else:
                                    try:
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table where name = '{final_residence}'")
                                        data5 = cursor.fetchall()
                                        return data5
                                    except:
                                        messagebox.showerror("Error", "This Name Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')


                            columns = ('Name', 'Age', 'Gender', 'Address line 1', 'Address line 2', 'Adhar', 'Mobile')
                            tree = ttk.Treeview(view_information_frame, columns=columns, show='headings')

                            tree.column("Name", width=500) 
                            tree.column("Age", width=50)
                            tree.column("Gender", width=50)
                            tree.column("Address line 1", width=400)
                            tree.column("Address line 2", width=400)
                            tree.column("Adhar", width=100)
                            tree.column("Mobile", width=100)

                            def set_alternate_row_colors(tree, color1, color2):
                                for i, item in enumerate(tree.get_children()):
                                    color = color1 if i % 2 == 0 else color2
                                    tree.item(item, tags=(f"row_{i}",))
                                    tree.tag_configure(f"row_{i}", background=color)

                            for col in columns:
                                tree.heading(col, text=col)
                                tree.column(col, anchor='center')

                            # Populate the Treeview with data
                            data = fetch_data()
                            for row in data:
                                tree.insert('', 'end', values=row)
                                tree.tag_configure(tagname=row, background='cyan')
                                set_alternate_row_colors(tree, "lightblue", "#ebc7f9")
                                # tree.tag_add(tag_name, row_index)

                            style = ttk.Style()
                
                            # Set font size for column headings
                            style.configure("Treeview.Heading", font=("Times New Roman", 14))
                            style.configure("Treeview", font=("Times New Roman", 12))
                                        

                            # Add a vertical scrollbar to the Treeview
                            scrollbar = ttk.Scrollbar(view_information_frame, orient='vertical', command=tree.yview)
                            tree.configure(yscrollcommand=scrollbar.set)
                            # Pack the Treeview and Scrollbar
                            tree.place(relx=0.495, rely=0.475, anchor='center', width=WIDTH, height=600)
                            # tree.pack(expand=True, fill="both")
                            # scrollbar.place(relx=0.995, rely=0.42, anchor='center', height=600)
                            scrollbar.place(relx=0.895, rely=0.475, anchor='center', height=600)
                        

                            def show_more_info(tree):
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]
                                    view_information_frame2 = CTkFrame(view_information_frame, width=WIDTH, height=HEIGHT).place(relx=0.5, rely=0.5, anchor='center')
                                    
                                    # Connect to the SQLite database
                                    conn2 = sqlite3.connect(resource_path('second_child.db'))
                                    cursor2 = conn2.cursor()
                                    

                                    # ===========================
                                    def get_image_data():
                                        conn = sqlite3.connect(resource_path('second_child.db'))
                                        cursor = conn.cursor()
                                        cursor.execute(f"SELECT * FROM residence_registration_table WHERE adhar = '{adhar_number}'")
                                        image_data = cursor.fetchone()[8]
                                        conn.close()
                                        return image_data

                                    def display_image_on_label():
                                        image_data = get_image_data()
                                        image = Image.open(BytesIO(image_data))
                                        resized_image2 = image.resize((180, 185))
                                        photo = ImageTk.PhotoImage(resized_image2)

                                        label = tk.Label(view_information_frame2, image=photo)
                                        label.photo = photo  # Keep a reference to the photo to prevent garbage collection
                                        label.place(relx=0.1, rely=0.1, anchor='center')

                                    display_image_on_label()
                                    # =======================

                                    columns2 = ('Name', 'Age', 'Date', 'Gender', 'Address_line_1', 'Address_line_2', 'Adhar', 'Mobile')

                                    tree2 = ttk.Treeview(view_information_frame2, columns=columns2, show='headings')
                                    tree2.place(relx=0.5, rely=0.24, anchor='center', width=WIDTH, height=50)

                                    tree2.column("Name", width=500) 
                                    tree2.column("Age", width=50)
                                    tree2.column("Date", width=100)
                                    tree2.column("Gender", width=50)
                                    tree2.column("Address_line_1", width=400)
                                    tree2.column("Address_line_2", width=400)
                                    tree2.column("Adhar", width=100)
                                    tree2.column("Mobile", width=100)
                                    # tree2.column("Pention", width=100)

                                    def fetch_data3():
                                        # Connect to the SQLite database
                                        conn = sqlite3.connect(resource_path('second_child.db'))
                                        cursor = conn.cursor()

                                        # Fetch all data from the 'students' table
                                        cursor.execute(f'SELECT name, age, date, gender, address_line_1, address_line_2,adhar, adhar, mobile FROM residence_registration_table where adhar = {adhar_number}')
                                        data = cursor.fetchall()

                                        return data

                                    for col2 in columns2:
                                        tree2.heading(col2, text=col2)
                                        tree2.column(col2, anchor='center')

                                    data = fetch_data3()
                                    for row in data:
                                        tree2.insert('', 'end', values=row)                            
                                    

                                    columns41 = ('Name', 'IFSC', 'Account', 'Branch', 'Pention')
                                    tree41 = ttk.Treeview(view_information_frame2, columns=columns41, show='headings')
                                    tree41.place(relx=0.5, rely=0.325, anchor='center', width=WIDTH, height=50)


                                    tree41.column("Name", width=200)
                                    tree41.column("IFSC", width=200)
                                    tree41.column("Account", width=200)
                                    tree41.column("Branch", width=200)
                                    tree41.column("Pention", width=200)

                                    # for col41 in columns41:
                                    for col41 in columns41:
                                        tree41.heading(col41, text=col41)
                                        tree41.column(col41, anchor='center')

                                    try:
                                        rel11 = cursor2.execute(f"SELECT name, ifsc, account, branch, pention FROM residence_pention where adhar = '{adhar_number}'")
                                        rel_info1x = rel11.fetchall()

                                        for rel_info11 in rel_info1x:
                                            tree41.insert('', 'end', values=rel_info11)
                                    except:
                                        pass                    

                                    # opearation first 
                                    columns3 = ('Operation', 'Doctor', 'Hospital', 'Address', 'Date')
                                    tree3 = ttk.Treeview(view_information_frame2, columns=columns3, show='headings')
                                    tree3.place(relx=0.5, rely=0.44, anchor='center', width=WIDTH, height=110)

                                    tree3.column("Operation", width=400) 
                                    tree3.column("Doctor", width=400)
                                    tree3.column("Hospital", width=400)
                                    tree3.column("Address", width=400)
                                    tree3.column("Date", width=50)

                                    for col3 in columns3:
                                        tree3.heading(col3, text=col3)
                                        tree3.column(col3, anchor='center')

                                    
                                    try:
                                        try:
                                            operation_first = cursor2.execute(f"select name, doctor, hospital, address, date from residence_operation_first where adhar = '{adhar_number}'")
                                            converted_operation_first = operation_first.fetchall()
                                            for row3 in converted_operation_first:
                                                tree3.insert('', 'end', values=row3)
                                                style3 = ttk.Style()

                                            # # Set font size for column headings
                                            style3.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style3.configure("Treeview", font=("Times New Roman", 12))
                                        except:
                                            pass

                                        try:
                                            operation_first2 = cursor2.execute(f"select name, doctor, hospital, address, date from residence_operation_second where adhar = '{adhar_number}'")
                                            converted_operation_first2 = operation_first2.fetchall()
                                            for row32 in converted_operation_first2:
                                                tree3.insert('', 'end', values=row32)
                                                style32 = ttk.Style()

                                            # # Set font size for column headings
                                            style32.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style32.configure("Treeview", font=("Times New Roman", 12))
                                        except:
                                            pass

                                        try:
                                            operation_first3 = cursor2.execute(f"select name, doctor, hospital, address, date from residence_operation_third where adhar = '{adhar_number}'")
                                            converted_operation_first3 = operation_first3.fetchall()
                                            for row33 in converted_operation_first3:
                                                tree3.insert('', 'end', values=row33)
                                                style33 = ttk.Style()

                                            # # Set font size for column headings
                                            style33.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style33.configure("Treeview", font=("Times New Roman", 12))
                                        except:
                                            pass

                                        try:
                                            operation_first4 = cursor2.execute(f"select name, doctor, hospital, address, date from residence_operation_fourth where adhar = '{adhar_number}'")
                                            converted_operation_first4 = operation_first4.fetchall()
                                            for row34 in converted_operation_first4:
                                                tree3.insert('', 'end', values=row34)
                                                style34 = ttk.Style()

                                            # # Set font size for column headings
                                            style34.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style34.configure("Treeview", font=("Times New Roman", 12))
                                        except:
                                            pass
                                    except:
                                        pass

                                   

                                    columns4 = ('Name', 'Relation', 'Address', 'Mobile', 'Adhar')
                                    tree4 = ttk.Treeview(view_information_frame, columns=columns4, show='headings')
                                    tree4.place(relx=0.5, rely=0.56, anchor='center', width=WIDTH, height=110)

                                    tree4.column("Name", width=500) 
                                    tree4.column("Relation", width=100)
                                    tree4.column("Address", width=500)
                                    tree4.column("Mobile", width=50)
                                    tree4.column("Adhar", width=50)

                                    for col4 in columns4:
                                        tree4.heading(col4, text=col4)
                                        tree4.column(col4, anchor='center')

                            
                                    try:
                                        try:
                                            conv1 = cursor2.execute(f'SELECT relative_name, relative_relation, relative_address, relative_mobile, relative_adhar FROM residence_relative_first where adhar = {adhar_number}')
                                            data1 = conv1.fetchall()
                                            
                                            for row1 in data1:
                                                tree4.insert('', 'end', values=row1)
                                                style1 = ttk.Style()
                                
                                            # Set font size for column headings
                                            style1.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style1.configure("Treeview", font=("Times New Roman", 12))                       
                                        except:
                                            pass

                                        try:
                                            conv2 = cursor2.execute(f'SELECT relative_name, relative_relation, relative_address, relative_mobile, relative_adhar FROM residence_relative_second where adhar = {adhar_number}')
                                            data2 = conv2.fetchall()
                                            
                                            for row2 in data2:
                                                tree4.insert('', 'end', values=row2)
                                                style2 = ttk.Style()
                                
                                            # Set font size for column headings
                                            style2.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style2.configure("Treeview", font=("Times New Roman", 12))                       
                                        except:
                                            pass

                                        try:
                                            conv3 = cursor2.execute(f'SELECT relative_name, relative_relation, relative_address, relative_mobile, relative_adhar FROM residence_relative_third where adhar = {adhar_number}')
                                            data3 = conv3.fetchall()
                                            
                                            for row3 in data3:
                                                tree4.insert('', 'end', values=row3)
                                                style3 = ttk.Style()
                                
                                            # Set font size for column headings
                                            style3.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style3.configure("Treeview", font=("Times New Roman", 12))                       
                                        except:
                                            pass

                                        try:
                                            conv4 = cursor2.execute(f'SELECT relative_name, relative_relation, relative_address, relative_mobile, relative_adhar FROM residence_relative_fourth where adhar = {adhar_number}')
                                            data4 = conv4.fetchall()
                                            
                                            for row4 in data4:
                                                tree4.insert('', 'end', values=row4)
                                                style4 = ttk.Style()
                                
                                            # Set font size for column headings
                                            style4.configure("Treeview.Heading", font=("Times New Roman", 14))
                                            style4.configure("Treeview", font=("Times New Roman", 12))                       
                                        except:
                                            pass
                                    except:
                                        pass




                                    
                                    def save_as_pdf():
                                        pdf = FPDF()
                                        file_path = filedialog.asksaveasfilename(defaultextension="_Information.pdf")
                                        # print(file_path)
                                        def create_pdf(file_path, data):
                                            
                                            pdf.add_page()

                                            # Adjust coordinates and dimensions


                                            # Set font
                                            pdf.set_font("Arial", size=11)

                                            # Add data to the PDF
                                            for line in data:
                                                pdf.cell(200, 5, txt=line, ln=True)  # Adjust width (200) based on your layout                                   
                                            

                                            # Save the PDF document
                                            pdf.output(file_path)

                                            
                                        if __name__ == "__main__":
                                            # pdf.save()

                                            name_ = cr.execute(f"select name from residence_registration_table where adhar = {adhar_number}")
                                            name_1 = name_.fetchone()
                                            name = list_to_string(name_1)

                                            age_ = cr.execute(f"select age from residence_registration_table where adhar = {adhar_number}")
                                            age_1 = age_.fetchone()
                                            age = list_to_string(age_1)

                                            date_ = cr.execute(f"select date from residence_registration_table where adhar = {adhar_number}")
                                            date_1 = date_.fetchone()
                                            date = list_to_string(date_1)

                                            gender_ = cr.execute(f"select gender from residence_registration_table where adhar = {adhar_number}")
                                            gender_1 = gender_.fetchone()
                                            gender = list_to_string(gender_1)

                                            address_line_1_ = cr.execute(f"select address_line_1 from residence_registration_table where adhar = {adhar_number}")
                                            address_line_1_1 = address_line_1_.fetchone()
                                            address_line_1 = list_to_string(address_line_1_1)

                                            address_line_2_ = cr.execute(f"select address_line_2 from residence_registration_table where adhar = {adhar_number}")
                                            address_line_2_1 = address_line_2_.fetchone()
                                            address_line_2 = list_to_string(address_line_2_1)

                                            adhar_ = cr.execute(f"select adhar from residence_registration_table where adhar = {adhar_number}")
                                            adhar_1 = adhar_.fetchone()
                                            adhar = list_to_string(adhar_1)

                                            mobile_ = cr.execute(f"select mobile from residence_registration_table where adhar = {adhar_number}")
                                            mobile_1 = mobile_.fetchone()
                                            mobile = list_to_string(mobile_1)

                                            try:
                                                pention_name = cr.execute(f"select name from residence_pention where adhar = {adhar_number}")
                                                pention_name_1 = pention_name.fetchone()
                                                pentionname = list_to_string(pention_name_1)
                                            except:
                                                pentionname = ""
                                                
                                            try:
                                                pention_ifsc = cr.execute(f"select ifsc from residence_pention where adhar = {adhar_number}")
                                                pention_ifsc_1 = pention_ifsc.fetchone()
                                                pentionifsc = list_to_string(pention_ifsc_1)
                                            except:
                                                pentionifsc = ""

                                            try:
                                                pention_account = cr.execute(f"select account from residence_pention where adhar = {adhar_number}")
                                                pention_account_1 = pention_account.fetchone()
                                                pentionaccount = list_to_string(pention_account_1)
                                            except:
                                                pentionaccount = ""

                                            try:
                                                pention_branch = cr.execute(f"select branch from residence_pention where adhar = {adhar_number}")
                                                pention_branch_1 = pention_branch.fetchone()
                                                pentionbranch = list_to_string(pention_branch_1)
                                            except:
                                                pentionbranch = ""

                                            try:
                                                pention_pention = cr.execute(f"select pention from residence_pention where adhar = {adhar_number}")
                                                pention_pention_1 = pention_pention.fetchone()
                                                pentionpention = list_to_string(pention_pention_1)
                                            except:
                                                pentionpention = ""
                                            
                                            # operation first
                                            try:
                                                operation_first_name = list_to_string(cr.execute(f"select name from residence_operation_first where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_first_name = ""

                                            try:
                                                operation_first_doctor = list_to_string(cr.execute(f"select doctor from residence_operation_first where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_first_doctor = ""

                                            try:
                                                operation_first_hospital = list_to_string(cr.execute(f"select hospital from residence_operation_first where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_first_hospital = ""

                                            try:
                                                operation_first_address = list_to_string(cr.execute(f"select address from residence_operation_first where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_first_address = ""

                                            try:
                                                operation_date_first = list_to_string(cr.execute(f"select date from residence_operation_first where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_date_first = ""

                                            
                                            # operation second
                                            try:
                                                operation_second_name = list_to_string(cr.execute(f"select name from residence_operation_second where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_second_name = ""

                                            try:
                                                operation_second_doctor = list_to_string(cr.execute(f"select doctor from residence_operation_second where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_second_doctor = ""

                                            try:
                                                operation_second_hospital = list_to_string(cr.execute(f"select hospital from residence_operation_second where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_second_hospital = ""

                                            try:
                                                operation_second_address = list_to_string(cr.execute(f"select address from residence_operation_second where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_second_address = ""

                                            try:
                                                operation_date_second = list_to_string(cr.execute(f"select date from residence_operation_second where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_date_second = ""

                                            
                                            # operation third
                                            try:
                                                operation_third_name = list_to_string(cr.execute(f"select name from residence_operation_third where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_third_name = ""

                                            try:
                                                operation_third_doctor = list_to_string(cr.execute(f"select doctor from residence_operation_third where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_third_doctor = ""

                                            try:
                                                operation_third_hospital = list_to_string(cr.execute(f"select hospital from residence_operation_third where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_third_hospital = ""

                                            try:
                                                operation_third_address = list_to_string(cr.execute(f"select address from residence_operation_third where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_third_address = ""

                                            try:
                                                operation_date_third = list_to_string(cr.execute(f"select date from residence_operation_third where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_date_third = ""


                                            # operation fourth
                                            try:
                                                operation_fourth_name = list_to_string(cr.execute(f"select name from residence_operation_fourth where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_fourth_name = ""

                                            try:
                                                operation_fourth_doctor = list_to_string(cr.execute(f"select doctor from residence_operation_fourth where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_fourth_doctor = ""

                                            try:
                                                operation_fourth_hospital = list_to_string(cr.execute(f"select hospital from residence_operation_fourth where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_fourth_hospital = ""

                                            try:
                                                operation_fourth_address = list_to_string(cr.execute(f"select address from residence_operation_fourth where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_fourth_address = ""

                                            try:
                                                operation_date_fourth = list_to_string(cr.execute(f"select date from residence_operation_fourth where adhar = {adhar_number}").fetchone())
                                            except:
                                                operation_date_fourth = ""



                                            # relative first
                                            try:
                                                relative_first = cr.execute(f"select relative_name from residence_relative_first where adhar = {adhar_number}")
                                                relative_1_name = relative_first.fetchone()
                                                relative_first_name = list_to_string(relative_1_name)
                                            except:
                                                relative_first_name = ""

                                            try:
                                                relative_first_rel = cr.execute(f"select relative_relation from residence_relative_first where adhar = {adhar_number}")
                                                relative_first_relation = list_to_string(relative_first_rel.fetchone())
                                            except:
                                                relative_first_relation = ""

                                            try:
                                                rel_add_line_1_1 = cr.execute(f"select relative_address from residence_relative_first where adhar = {adhar_number}")
                                                relative_address_line_1_1 = list_to_string(rel_add_line_1_1.fetchone())
                                            except:
                                                relative_address_line_1_1 = ""


                                            try:
                                                rel_mobile_1 = cr.execute(f"select relative_mobile from residence_relative_first where adhar = {adhar_number}")
                                                relative_mobile_1 = list_to_string(rel_mobile_1.fetchone())
                                            except:
                                                relative_mobile_1 = ""
                                            

                                            try:
                                                rel_adhar_1 = cr.execute(f"select adhar from residence_relative_first where adhar = {adhar_number}")
                                                relative_adhar_1 = list_to_string(rel_adhar_1.fetchone())
                                            except:
                                                relative_adhar_1 = ""



                                            # relative second
                                            try:
                                                relative_second = cr.execute(f"select relative_name from residence_relative_second where adhar = {adhar_number}")
                                                relative_2_name = relative_second.fetchone()
                                                relative_second_name = list_to_string(relative_2_name)
                                            except:
                                                relative_second_name = ""


                                            try:
                                                relative_second_rel = cr.execute(f"select relative_relation from residence_relative_second where adhar = {adhar_number}")
                                                relative_second_relation = list_to_string(relative_second_rel.fetchone())
                                            except:
                                                relative_second_relation = ""


                                            try:
                                                rel_add_line_1_2 = cr.execute(f"select relative_address from residence_relative_second where adhar = {adhar_number}")
                                                relative_address_line_1_2 = list_to_string(rel_add_line_1_2.fetchone())
                                            except:
                                                relative_address_line_1_2 = ""


                                            try:
                                                rel_mobile_2 = cr.execute(f"select relative_mobile from residence_relative_second where adhar = {adhar_number}")
                                                relative_mobile_2 = list_to_string(rel_mobile_2.fetchone())
                                            except:
                                                relative_mobile_2 = ""

                                            
                                            try:
                                                rel_adhar_2 = cr.execute(f"select adhar from residence_relative_second where adhar = {adhar_number}")
                                                relative_adhar_2 = list_to_string(rel_adhar_2.fetchone())
                                            except:
                                                relative_adhar_2 = ""



                                            # relative third
                                            try:
                                                relative_third = cr.execute(f"select relative_name from residence_relative_third where adhar = {adhar_number}")
                                                relative_3_name = relative_third.fetchone()
                                                relative_third_name = list_to_string(relative_3_name)
                                            except:
                                                relative_third_name = ""

                                            
                                            try:
                                                relative_third_rel = cr.execute(f"select relative_relation from residence_relative_third where adhar = {adhar_number}")
                                                relative_third_relation = list_to_string(relative_third_rel.fetchone())
                                            except:
                                                relative_third_relation = ""


                                            try:
                                                rel_add_line_1_3 = cr.execute(f"select relative_address from residence_relative_third where adhar = {adhar_number}")
                                                relative_address_line_1_3 = list_to_string(rel_add_line_1_3.fetchone())
                                            except:
                                                relative_address_line_1_3 = ""


                                            try:
                                                rel_mobile_3 = cr.execute(f"select relative_mobile from residence_relative_third where adhar = {adhar_number}")
                                                relative_mobile_3 = list_to_string(rel_mobile_3.fetchone())
                                            except:
                                                relative_mobile_3 = ""


                                            try:
                                                rel_adhar_3 = cr.execute(f"select adhar from residence_relative_third where adhar = {adhar_number}")
                                                relative_adhar_3 = list_to_string(rel_adhar_3.fetchone())
                                            except:
                                                relative_adhar_3 = ""



                                            # relative fourth
                                            try:
                                                relative_fourth = cr.execute(f"select relative_name from residence_relative_fourth where adhar = {adhar_number}")
                                                relative_4_name = relative_fourth.fetchone()
                                                relative_fourth_name = list_to_string(relative_4_name)
                                            except:
                                                relative_fourth_name = ""

                                            try:
                                                relative_fourth_rel = cr.execute(f"select relative_relation from residence_relative_fourth where adhar = {adhar_number}")
                                                relative_fourth_relation = list_to_string(relative_fourth_rel.fetchone())
                                            except:
                                                relative_fourth_relation = ""


                                            try:
                                                rel_add_line_1_4 = cr.execute(f"select relative_address from residence_relative_fourth where adhar = {adhar_number}")
                                                relative_address_line_1_4 = list_to_string(rel_add_line_1_4.fetchone())
                                            except:
                                                relative_address_line_1_4 = ""



                                            try:
                                                rel_mobile_4 = cr.execute(f"select relative_mobile from residence_relative_fourth where adhar = {adhar_number}")
                                                relative_mobile_4 = list_to_string(rel_mobile_4.fetchone())
                                            except:
                                                relative_mobile_4 = ""


                                            try:
                                                rel_adhar_4 = cr.execute(f"select adhar from residence_relative_fourth where adhar = {adhar_number}")
                                                relative_adhar_4 = list_to_string(rel_adhar_4.fetchone())
                                            except:
                                                relative_adhar_4 = ""



                                            
                                            # Sample data to be stored in the PDF
                                            data = [
                                                "1. General Information -----------------------------------------------------------------------------------------------------------------",
                                                f"  Name: {name}",
                                                f"  Age: {age}",
                                                f"  Date: {date}                                                                         Gender: {gender}",
                                                f"  Address Line 1: {address_line_1}",
                                                f"  Address Line 2: {address_line_2}",
                                                f"  Adhar: {adhar}                                                         Mobile: {mobile}",
                                                "",
                                                "",
                                                "2. Pention Information -----------------------------------------------------------------------------------------------------------------",
                                                f"  Banking Name: {pentionname}",
                                                f"  IFSC: {pentionifsc}",
                                                f"  Account Number: {pentionaccount}",
                                                f"  Branch: {pentionbranch}",
                                                f"  Pention: {pentionpention}",
                                                "",
                                                "",
                                                "3. Operation Information ---------------------------------------------------------------------------------------------------------------",
                                                f"  Operation 1: {operation_first_name}",
                                                f"  Doctor Name: {operation_first_doctor}",
                                                f"  Hospital Name: {operation_first_hospital}",
                                                f"  Address: {operation_first_address}",
                                                f"  Date: {operation_date_first}",
                                                "",
                                                "",
                                                f"  Operation 2: {operation_second_name}",
                                                f"  Doctor Name: {operation_second_doctor}",
                                                f"  Hospital Name: {operation_second_hospital}",
                                                f"  Address: {operation_second_address}",
                                                f"  Date: {operation_date_second}",
                                                "",
                                                "",
                                                f"  Operation 3: {operation_third_name}",
                                                f"  Doctor Name: {operation_third_doctor}",
                                                f"  Hospital Name: {operation_third_hospital}",
                                                f"  Address: {operation_third_address}",
                                                f"  Date: {operation_date_third}",
                                                "",
                                                "",
                                                f"  Operation 4: {operation_fourth_name}",
                                                f"  Doctor Name: {operation_fourth_doctor}",
                                                f"  Hospital Name: {operation_fourth_hospital}",
                                                f"  Address: {operation_fourth_address}",
                                                f"  Date: {operation_date_fourth}",
                                                "",
                                                "",
                                                "4. Relative Information -----------------------------------------------------------------------------------------------------------------",
                                                f"  Relative 1: {relative_first_name}",
                                                f"  Relation: {relative_first_relation}",
                                                f"  Relative Address: {relative_address_line_1_1}",
                                                f"  Relative Mobile: {relative_mobile_1}",
                                                f"  Relative Adhar: {relative_adhar_1}",
                                                "",
                                                "",
                                                f"  Relative 2: {relative_second_name}",
                                                f"  Relation: {relative_second_relation}",
                                                f"  Relative Address: {relative_address_line_1_2}",
                                                f"  Relative Mobile: {relative_mobile_2}",
                                                f"  Relative Adhar: {relative_adhar_2}",
                                                "",
                                                "",
                                                f"  Relative 3: {relative_third_name}",
                                                f"  Relation: {relative_third_relation}",
                                                f"  Relative Address: {relative_address_line_1_3}",
                                                f"  Relative Mobile: {relative_mobile_3}",
                                                f"  Relative Adhar: {relative_adhar_3}",
                                                "",
                                                "",
                                                f"  Relative 4: {relative_fourth_name}",
                                                f"  Relation: {relative_fourth_relation}",
                                                f"  Relative Address: {relative_address_line_1_4}",
                                                f"  Relative Mobile: {relative_mobile_4}",
                                                f"  Relative Adhar: {relative_adhar_4}",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",      
                                                "", 
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",
                                                "",          
                                                "",
                                                "",
                                                "",   
                                                "",
                                                "",
                                                "",
                                                "",                       
                                                "****************************************************************************************************************************",
                                                "Shantai (Shantamma) Vruddhashrama Jamboti Road, Kuttalwadi, Karnataka 590014, India"

                                            ]

                                            # Specify the path where you want to save the PDF
                                            pdf_file_path = f"{file_path}"

                                            # Create and store data in the PDF
                                            create_pdf(pdf_file_path, data)
                                    
                                    # Save As PDF btn
                                    CTkButton(view_information_frame2, text="Save As PDF", font=("Times New Roman", 22), fg_color=COLOR, command=save_as_pdf).place(relx=0.2, rely=0.1, anchor='center')
                                    
                                    # Back Button                       
                                    CTkButton(view_information_frame2, text='< Back', font=("Times New Roman", 22), fg_color=COLOR, command=view_information).place(relx=0.5, rely=0.8, anchor='center')
                                except:
                                    messagebox.showerror("Error", "Please Select A Row")

                            # view more info button
                            view_more_info_btn = CTkButton(view_information_frame, text="View More", font=("Times New Roman", 22), fg_color=COLOR, command=lambda: show_more_info(tree))
                            view_more_info_btn.place(relx=0.45, rely=0.76, anchor='center')


                            def delete_all_record():
                                
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()

                                    
                                    try:
                                        cr.execute(f"delete from residence_registration_table where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_relative_first where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_relative_second where adhar = '{adhar_number}'")
                                    except:
                                        pass



                                    try:
                                        cr.execute(f"delete from reisidence_relative_third where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_relative_fourth where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_first where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_second where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_third where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_operation_fourth where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_pention where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    conn.commit()
                                    conn.close()

                                    messagebox.showinfo("Detete Information", "Record Has Been Deleted!")
                                    view_information()
                                except:
                                    messagebox.showerror("Error", "Please Select A row")

                            # delete btn
                            delete_btn = CTkButton(view_information_frame, text='Delete', font=("Times New Roman", 22), fg_color=COLOR, command=delete_all_record).place(relx=0.55, rely=0.76, anchor='center')

                            def update_registration_info():
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]

                                    update_registration = tk.Toplevel(view_information_frame)
                                    update_registration.geometry("900x600")
                                    # ===============
                                    update_registration.title("Update Information")
                                    update_registration.resizable(False, False)
                                    

                                    # name of relation entry
                                    name_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Full Name')
                                    name_entry.place(relx=0.5, rely=0.13, anchor='center')


                                    # relation with person entry
                                    address_line_1_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Address Line 1')
                                    address_line_1_entry.place(relx=0.5, rely=0.29, anchor='center')

                                    # relative address 1 entry
                                    address_line_2_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Address Line 2')
                                    address_line_2_entry.place(relx=0.5, rely=0.45, anchor='center')

                                    # relative address 2 entry
                                    adhar_number_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Adhar Number')
                                    adhar_number_entry.place(relx=0.5, rely=0.61, anchor='center')

                                    # relative phone entry
                                    phone_number_entry = CTkEntry(update_registration, font=("Times New Roman", 18), width=700, placeholder_text='Phone Number')
                                    phone_number_entry.place(relx=0.5, rely=0.77, anchor='center')

                                    def registration_validation():
                                        conn = sqlite3.connect(resource_path("second_child.db"))
                                        cr = conn.cursor()

                                        if name_entry.get() == "" and address_line_1_entry.get() == "" and address_line_2_entry.get() == "" and adhar_number_entry.get() == "" and phone_number_entry.get() == "":
                                            messagebox.showinfo("Update Information", "Data is not updated!")
                                            update_registration.destroy()
                                            view_information()
                                        else:
                                            if name_entry.get() == "": 
                                                pass
                                            else:          
                                                if name_entry.get().isnumeric() == True:
                                                    messagebox.showerror("Error", "Name can not be inserted")
                                                else:
                                                    cr.execute(f"update residence_registration_table set name = '{capitalize_input(name_entry.get())}' where adhar = '{adhar_number}'")
                                                    

                                            if address_line_1_entry.get() == "":
                                                pass
                                            else:
                                                cr.execute(f"update residence_registration_table set address_line_1 = '{address_line_1_entry.get()}' where adhar = '{adhar_number}'")

                                            if address_line_2_entry.get() == "":
                                                pass
                                            else:
                                                cr.execute(f"update residence_registration_table set address_line_2 = '{address_line_2_entry.get()}' where adhar = '{adhar_number}'")
                                                
                                            if adhar_number_entry.get() == "":
                                                pass
                                            else:
                                                if adhar_number_entry.get().isnumeric() == False or adhar_number_entry.get() == "" or len(adhar_number_entry.get()) != 12:
                                                    messagebox.showerror("Error", "Adhar number can not be inserted")
                                                    adhar_number_entry.delete(0, 'end')
                                                else:
                                                    cr.execute(f"update residence_registration_table set adhar = '{adhar_number_entry.get()}' where adhar = '{adhar_number}'")

                                            if phone_number_entry.get() == "":
                                                pass
                                            else:
                                                if phone_number_entry.get().isnumeric() == False or phone_number_entry.get() == "" or len(phone_number_entry.get()) != 10:
                                                    messagebox.showerror("Error", "Mobile number can not be inserted")
                                                    phone_number_entry.delete(0, 'end')      
                                                else:
                                                    cr.execute(f"update residence_registration_table set mobile = '{phone_number_entry.get()}' where adhar = '{adhar_number}'")                              
                                            
                                            # conn.commit()
                                            # conn.close()
                                            update_registration.destroy()
                                            messagebox.showinfo("Update Information", "Successfully Updated!")
                                            conn.commit()
                                            conn.close()
                                            view_information()
                                            
                                    CTkButton(update_registration, text='Save', font=("Times New Roman", 18), width=200, fg_color=COLOR, command=registration_validation).place(relx=0.5, rely=0.93, anchor='center')


                                    # relative adhar number
                                    # relative_adhar_entry1 = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text="Adhar Number *")
                                    # relative_adhar_entry1.place(relx=0.5, rely=0.84, anchor='center')

                                    # ===============

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()
                                except:
                                    messagebox.showerror("Error", "Please Select A row")
                            # update btn
                            CTkButton(view_information_frame, text='Update', font=("Times New Roman", 22), fg_color=COLOR, command=update_registration_info).place(relx=0.35, rely=0.76, anchor='center')


                            def generate_pdf():
                                # ===============
                                file_path = filedialog.asksaveasfilename(defaultextension="_All_Information.pdf")

                                # =========
                                def create_pdf(names, ages, genders, adhars, mobiles, output_filename):
                                    # Create a PDF document
                                    pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)

                                    # Set up column coordinates
                                    column_width = letter[0] / 5
                                    column_height = letter[1] - 50

                                    # Set up font
                                    pdf_canvas.setFont("Helvetica", 12)

                                    # Draw column headers
                                    pdf_canvas.drawString(65, column_height, "Name")
                                    pdf_canvas.drawString(column_width + 87, column_height, "Age")
                                    pdf_canvas.drawString(column_width + 190, column_height, "Gender")
                                    pdf_canvas.drawString(column_width + 305, column_height, "Adhar")
                                    pdf_canvas.drawString(column_width + 405, column_height, "Mobile")

                                    # Draw data in columns
                                    for i, (name, age, gender, adhar, mobile) in enumerate(zip(names, ages, genders, adhars, mobiles), start=1):
                                        row_height = column_height - i * 15
                                        pdf_canvas.drawString(35, row_height, name)
                                        pdf_canvas.drawString(column_width + 90, row_height, str(age))
                                        pdf_canvas.drawString(column_width + 195, row_height, str(gender))
                                        pdf_canvas.drawString(column_width + 280, row_height, str(adhar))
                                        pdf_canvas.drawString(column_width + 390, row_height, str(mobile))


                                    # Save the PDF
                                    pdf_canvas.save()

                                # Example data

                                name_ = cr.execute(f"select name from residence_registration_table")
                                name_1 = name_.fetchall()

                                age_ = cr.execute(f"select age from residence_registration_table")
                                age_1 = age_.fetchall()

                                gender_ = cr.execute(f"select gender from residence_registration_table")
                                gender_1 = gender_.fetchall()

                                adhar_ = cr.execute(f"select adhar from residence_registration_table")
                                adhar_1 = adhar_.fetchall()

                                mobile_ = cr.execute(f"select mobile from residence_registration_table")
                                mobile_1 = mobile_.fetchall()

                                cleaned_names = []
                                for n in name_1:
                                    cleaned_names.append(n[0])

                                cleaned_age = []
                                for a in age_1:
                                    cleaned_age.append(a[0])

                                cleaned_gender = []
                                for g in gender_1:
                                    cleaned_gender.append(g[0])

                                
                                cleaned_adhar = []
                                for ad in adhar_1:
                                    cleaned_adhar.append(ad[0])

                                cleaned_mobile = []
                                for m in mobile_1:
                                    cleaned_mobile.append(m[0])
                                    

                                # Output PDF filename
                                output_filename = f"{file_path}"

                                # Generate PDF
                                create_pdf(cleaned_names, cleaned_age, cleaned_gender, cleaned_adhar, cleaned_mobile, output_filename)
                                # ========
                                
                            # generate pdf button
                            CTkButton(view_information_frame, text='Generate PDF', font=("Times New Roman", 22), fg_color=COLOR, command=generate_pdf).place(relx=0.65, rely=0.76, anchor='center')

                            # ======================================================================



                        def search_data():
                            def capitalize_input(input_str):
                                words = input_str.split()
                                capitalized_words = [word.capitalize() for word in words]
                                return ' '.join(capitalized_words)
                            # Capitalize the first letter of each word
                            residence_name = capitalize_input(search_bar.get())

                            if residence_name == "":
                                messagebox.showerror("Error", "Please Enter Name or Adhar")
                            else:                    
                                if residence_name.isnumeric() == True and len(residence_name) == 12: # numbers
                                    verify_data(residence_name)
                                        
                                else:     
                                    try:                                
                                        resi_var2 = cr.execute(f"SELECT name from residence_registration_table where name = '{residence_name}'")
                                        final_residence2 = resi_var2.fetchone()
                                        final_residence3 = list_to_string(final_residence2)

                                        if residence_name in final_residence3:

                                            
                                            verify_data(residence_name)
                                        else:
                                            pass
                                    except:
                                        messagebox.showerror("Error", "Entered Value Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                    

                        # search button
                        search_button = CTkButton(view_information_frame, text="Search", font=("Times New Roman", 22), fg_color="#3377ff", command=search_data)
                        search_button.place(relx=0.62, rely=0.2, anchor='center')

                        verify_data(final_residence=None)




                    def add_healthcare_information():
                        healthcare_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)

                        # heading
                        name_label = CTkLabel(healthcare_frame, text="HealthCare Information", font=("Times New Roman", 50), text_color=COLOR)
                        name_label.place(relx=0.5, rely=0.175, anchor='center')

                        # name of patient adhar entry
                        name_of_patient_adhar_entry = CTkEntry(healthcare_frame, font=("Times New Roman", 20), width=600, border_color=COLOR, placeholder_text='Adhar Number Of Patient *')
                        name_of_patient_adhar_entry.place(relx=0.3, rely=0.25, anchor='center')


                        # name of doctor entry
                        name_of_doctor_entry = CTkEntry(healthcare_frame, font=("Times New Roman", 20), width=600, border_color=COLOR, placeholder_text='Name Of Doctor *')
                        name_of_doctor_entry.place(relx=0.3, rely=0.35, anchor='center')                         
                        
                        # type of desease entry
                        # type_of_disease_entry = CTkEntry(healthcare_frame, font=("Times New Roman", 20), width=600, border_color=COLOR, placeholder_text='Name Of Disease *')
                        # type_of_disease_entry.place(relx=0.3, rely=0.35, anchor='center')
                        
                        data = [
                            "Alzheimer's disease",
                            "Arthritis",
                            "Atherosclerosis",
                            "Cataracts",
                            "Chronic kidney disease",
                            "Chronic liver disease",
                            "Chronic pain",
                            "Chronic obstructive pulmonary disease (COPD)",
                            "Dementia",
                            "Depression",
                            "Diabetes",
                            "Heart disease",
                            "Hypertension",
                            "Hearing loss",
                            "Macular degeneration",
                            "Osteoarthritis",
                            "Osteoporosis",
                            "Parkinson's disease",
                            "Peripheral artery disease",
                            "Pneumonia",
                            "Prostate problems",
                            "Rheumatoid arthritis",
                            "Shingles",
                            "Sleep apnea",
                            "Skin cancer",
                            "Stroke",
                            "Type 2 diabetes",
                            "Urinary incontinence",
                            "Varicose veins",
                            "Vision impairment",                            
                            "Other"
                        ]

                        def get_diseases():
                            try:
                                result = var.get()
                                return result
                            except:
                                return ""

                        var = StringVar()
                        CTkComboBox(healthcare_frame, variable=var, command=get_diseases, values=data, state='readonly', font=("Times New Roman", 20), width=600).place(relx=0.3, rely=0.45, anchor='center')
                        
                        
                            
                        
                        def cal_fun():
                            # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                            calender_toplevel = tk.Toplevel(healthcare_frame, bg=COLOR)
                            calender_toplevel.title("Checkup Date")
                            calender_toplevel.geometry("400x400")
                            calender_toplevel.resizable(False, False)

                            # cal_var = StringVar()
                            def selectdate():
                                global healthcare_date       
                                myDate = mycal10.get_date()                        
                                healthcare_date = myDate
                                selectDate = CTkLabel(healthcare_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                selectDate.place(relx=0.3, rely=0.55, anchor='center')
                                calender_toplevel.destroy()
                                

                            mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                            mycal10.place(relx=0.5, rely=0.4, anchor='center')

                            open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                            
                        # cal_button
                        cal_button = CTkButton(healthcare_frame, text='Choose Checkup Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.19, rely=0.55, anchor='center')
                        


                        
                        # Doctor Prescription label
                        doctor_prescription_label = CTkLabel(healthcare_frame, text="Doctor Prescription", font=("Times New Roman", 22), width=50)
                        doctor_prescription_label.place(relx=0.595, rely=0.25, anchor='center')

                        # # doctor prescription on Text
                        # doctor_prescription = tk.Text(healthcare_frame, width=50, height=15, wrap="word", font=("Times New Roman", 20))
                        # doctor_prescription.place(relx=0.705, rely=0.4, anchor='center')

                        prevar = StringVar()

                        doctor_prescription_entry = CTkTextbox(healthcare_frame, border_color=COLOR, font=("Times New Roman", 20), border_width=2, width=600, height=500)
                        doctor_prescription_entry.place(relx=0.705, rely=0.5, anchor='center')


                        def get_all_healthcare_info():
                            # print(name_of_patient_adhar_entry.get())
                            # print(name_of_doctor_entry.get())
                            # print(type_of_disease_entry.get())
                            try:
                                Date2 = healthcare_date
                                # print(Date2)
                            except:
                                # print(e)
                                current_date = datetime.now()
                                # Format the date as "dd/mm/yy"
                                Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'
                                # print(Date2)

                            # print(gender.get())
                            # print(doctor_prescription_entry.get('1.0', END))
                            # print(prevar)
                            # print(doctor_prescription_entry.get("1.0","end-1c"))
                            conn = sqlite3.connect(resource_path("second_child.db"))
                            cr = conn.cursor()
                            if name_of_patient_adhar_entry.get() == "" or name_of_patient_adhar_entry.get().isnumeric() == False or len(name_of_patient_adhar_entry.get()) != 12:
                                messagebox.showerror("Error", "Please Enter Valid Adhar")
                                name_of_patient_adhar_entry.delete(0, 'end')

                            elif name_of_doctor_entry.get() == "" or name_of_doctor_entry.get().isnumeric() == True:
                                messagebox.showerror("Error", "Please Enter Valid Doctor Name")
                                name_of_doctor_entry.delete(0, 'end')
                                
                            # elif type_of_disease_entry.get() == "" or type_of_disease_entry.get().isnumeric() == True:
                            #     messagebox.showerror("Error", "Please Enter Valid Name Of Disease")
                            #     type_of_disease_entry.delete(0, 'end')
                            elif get_diseases() == "":
                                messagebox.showerror("Error", "Please Select A disease")
                            else:
                                # conn.commit()
                                # residence_registration_table
                                columm1 = cr.execute(f"select adhar from residence_registration_table where adhar = '{name_of_patient_adhar_entry.get()}'")
                                result = columm1.fetchone()

                                # gender_new = cr.execute(f"select gender from residence_registration_table where adhar = '{name_of_patient_adhar_entry.get()}'")
                                # genderx = gender_new.fetchone()

                                if result:
                                    
                                    
                                    message_text = doctor_prescription_entry.get('1.0', END)
                                    lines = message_text.split("\n")
                                    
                                    my_string = ""

                                    for i in range(len(lines)):
                                        my_string = my_string + f"{lines[i]}\n" 

                                    cr.execute('''CREATE TABLE IF NOT EXISTS residence_healthcare(id INTEGER PRIMARY KEY AUTOINCREMENT, adhar TEXT, doctor TEXT, disease TEXT, date TEXT, prescription TEXT)''')
                                    cr.execute('''INSERT INTO residence_healthcare(adhar, doctor, disease, date, prescription) values(?,?,?,?,?)''', (name_of_patient_adhar_entry.get(), name_of_doctor_entry.get(), get_diseases(), Date2, my_string))
                                    conn.commit()
                                    messagebox.showinfo("Information","Record Has Been Succesfully Saved!")
                                    add_healthcare_information()
                                else:
                                    messagebox.showerror("Error", "Adhar Number Does Not Match")
                                    name_of_patient_adhar_entry.delete(0, 'end')

                            

                        
                        # Save healthcare information
                        healthcare_info = CTkButton(healthcare_frame, text="Save HealthCare Information", font=("Times New Roman", 20), width=800, fg_color=COLOR, command=get_all_healthcare_info)
                        healthcare_info.place(relx=0.5, rely=0.8, anchor='center')


                        healthcare_frame.place(relx=0.5, rely=0.5, anchor='center')

                    def add_operation_information():
                        operation_information = CTkFrame(win, width=WIDTH, height=HEIGHT, fg_color='white')
                        operation_information.place(relx=0.5, rely=0.5, anchor='center')

                        adhar_entry = CTkEntry(operation_information, font=("Times New Roman", 20), width=400, border_color=COLOR, placeholder_text='Residence Adhar Number *')
                        adhar_entry.place(relx=0.5, rely=0.2, anchor='center')

                        child_frame = CTkFrame(operation_information, width=(WIDTH / 2.75), height=(HEIGHT / 1.75))
                        child_frame.place(relx=0.5, rely=0.53, anchor='center')



                        # def get_operation_info_1():
                        #         name = relative_name1.get()
                        #         relation = relative_relation1.get()
                        #         address = relative_address1.get()
                        #         adhar = relative_adhar1.get()
                        #         Adhar = common_adhar.get()
                        #         mobile = relative_mobile1.get()

                        #         if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                        #             messagebox.showerror("Error", "Please Enter Valid Residence's Adhar")
                        #             common_adhar.delete(0, 'end')

                        #         elif name == "" or name.isnumeric() == True:
                        #             messagebox.showerror("Error", "Please Enter Valid Name")
                        #             relative_name1.delete(0, 'end')

                        #         elif relation == "" or name.isnumeric() == True:
                        #             messagebox.showerror("Error", "Please Enter Valid Relation")
                        #             relative_relation1.delete(0, 'end')

                        #         elif address == "":
                        #             messagebox.showerror("Error", "Please Enter Valid Address")
                        #             relative_address1.delete(0, 'end')

                        #         elif adhar == "" or adhar.isnumeric() == False or len(adhar) != 12:
                        #             messagebox.showerror("Error", "Please Enter Valid Adhar")
                        #             relative_adhar1.delete(0, 'end')

                        #         elif mobile == "" or mobile.isnumeric() == False or len(mobile) != 10:
                        #             messagebox.showerror("Error", "Please Enter Valid Mobile")
                        #             relative_mobile1.delete(0, 'end')

                        #         else:

                        #             # Relative Adhar
                        #             adhar_first = cr.execute("SELECT relative_adhar FROM residence_relative_first").fetchall()
                        #             get_adhar_first = tuple_to_string(adhar_first)

                        #             adhar_second = cr.execute("SELECT relative_adhar FROM residence_relative_second").fetchall()
                        #             get_adhar_second = tuple_to_string(adhar_second)

                        #             adhar_third = cr.execute("SELECT relative_adhar FROM residence_relative_third").fetchall()
                        #             get_adhar_third = tuple_to_string(adhar_third)

                        #             adhar_fourth = cr.execute("SELECT relative_adhar FROM residence_relative_fourth").fetchall()
                        #             get_adhar_fourth = tuple_to_string(adhar_fourth)
                                    

                        #             residence_adhar = cr.execute("SELECT adhar FROM residence_registration_table").fetchall()
                        #             get_residence_adhar = tuple_to_string(residence_adhar)



                        #             # Residence Adhar
                        #             residence_adhar_first = cr.execute("SELECT adhar FROM residence_relative_first").fetchall()
                        #             get_residence_adhar_first = tuple_to_string(residence_adhar_first)

                        #             # residence_adhar_second = cr.execute("SELECT adhar FROM residence_relative_second").fetchall()
                        #             # get_residence_adhar_second = tuple_to_string(residence_adhar_second)

                        #             # residence_adhar_third = cr.execute("SELECT adhar FROM residence_relative_third").fetchall()
                        #             # get_residence_adhar_third = tuple_to_string(residence_adhar_third)

                        #             # residence_adhar_fourth = cr.execute("SELECT adhar FROM residence_relative_fourth").fetchall()
                        #             # get_residence_adhar_fourth = tuple_to_string(residence_adhar_fourth)
                                    
                        #             if Adhar not in get_residence_adhar:
                        #                 messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")

                        #             elif Adhar in get_residence_adhar_first:
                        #                 messagebox.showerror("Error", "The Residence Adhar Number Can Not Be Inseted Again For Relative 1")

                        #             elif adhar in get_adhar_first or Adhar in get_adhar_second or Adhar in get_adhar_third or Adhar in get_adhar_fourth:
                        #                 messagebox.showerror("Error", "The Relative Adhar Number Can Not Be Inserted Again")                                                                           
                                                                        
                        #             else:
                        #                 cr.execute('''create table if not exists residence_relative_first(relative_name text, relative_relation text, relative_address text, relative_mobile text, relative_adhar text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))''')
                        #                 cr.execute("insert into residence_relative_first (relative_name, relative_relation, relative_address, relative_mobile, relative_adhar, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(relation), address, mobile, adhar, Adhar))
                        #                 conn.commit()
                        #                 messagebox.showinfo("Information", "Relative 1 has been inserted!")
                                    

                        #     # register button
                        #     CTkButton(child_frame1, text='Register', font=("Times New Roman", 22), width=400, fg_color=COLOR, command=get_operation_info_1).place(relx=0.5, rely=0.95, anchor='center')
                        
                        def operation_1():
                            
                            operation_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Operation *')
                            operation_name.place(relx=0.5, rely=0.2, anchor='center')

                            doctor_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Doctor *')
                            doctor_name.place(relx=0.5, rely=0.35, anchor='center')

                            hospital_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Hospital *')
                            hospital_name.place(relx=0.5, rely=0.5, anchor='center')

                            address_of_hospital = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Address Of Hospital *')
                            address_of_hospital.place(relx=0.5, rely=0.65, anchor='center')

                            # date
                            def cal_fun():
                                # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                                calender_toplevel = tk.Toplevel(child_frame, bg=COLOR)
                                calender_toplevel.title("Checkup Date")
                                calender_toplevel.geometry("400x400")
                                calender_toplevel.resizable(False, False)

                                # cal_var = StringVar()
                                def selectdate():
                                    global operation_date       
                                    myDate = mycal10.get_date()                        
                                    operation_date = myDate
                                    selectDate = CTkLabel(child_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                    selectDate.place(relx=0.5, rely=0.8, anchor='center')
                                    calender_toplevel.destroy()
                                    

                                mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                                mycal10.place(relx=0.5, rely=0.4, anchor='center')

                                open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                                
                            # cal_button
                            cal_button = CTkButton(child_frame, text='Choose Operation Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.275, rely=0.8, anchor='center')
                            
                            def get_operation_info():
                                name = operation_name.get()
                                doctor = doctor_name.get()
                                hos_name = hospital_name.get()
                                address = address_of_hospital.get()
                                Adhar = adhar_entry.get()

                                try:
                                    Date2 = healthcare_date
                                    # print(Date2)
                                except:
                                    # print(e)
                                    current_date = datetime.now()
                                    # Format the date as "dd/mm/yy"
                                    Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence Adhar Number")
                                    adhar_entry.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    operation_name.delete(0, 'end')

                                elif doctor == "" or doctor.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Doctor Name")
                                    doctor_name.delete(0, 'end')

                                elif hos_name == "" or hos_name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Hospital Name")
                                    hospital_name.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")

                                else:
                                    adhar_from_res = cr.execute("SELECT adhar from residence_registration_table")
                                    converted_val = adhar_from_res.fetchall()
                                    resi_result = tuple_to_string(converted_val)

                                    res_pention = cr.execute("SELECT adhar from residence_operation_first")
                                    res_con = res_pention.fetchall()
                                    res_result = tuple_to_string(res_con)
                                    
                                    if Adhar not in resi_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")
                                    
                                    elif Adhar in res_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Already Present In Operation 1")

                                    else:
                                        cr.execute("create table if not exists residence_operation_first (name text, doctor text, hospital text, address text, date text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                                        cr.execute("insert into residence_operation_first (name, doctor, hospital, address, date, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(doctor), capitalize_input(hos_name), address, Date2, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Infromation Of Operation 1 Has Been Inserted")
                                
                                
                            
                            CTkButton(child_frame, text="Register", font=("Times New Roman", 20), width=400, fg_color=COLOR, command=get_operation_info).place(relx=0.5, rely=0.95, anchor='center')



                        def operation_2():
                            
                            operation_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Operation *')
                            operation_name.place(relx=0.5, rely=0.2, anchor='center')

                            doctor_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Doctor *')
                            doctor_name.place(relx=0.5, rely=0.35, anchor='center')

                            hospital_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Hospital *')
                            hospital_name.place(relx=0.5, rely=0.5, anchor='center')

                            address_of_hospital = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Address Of Hospital *')
                            address_of_hospital.place(relx=0.5, rely=0.65, anchor='center')

                            # date
                            def cal_fun():
                                # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                                calender_toplevel = tk.Toplevel(child_frame, bg=COLOR)
                                calender_toplevel.title("Checkup Date")
                                calender_toplevel.geometry("400x400")
                                calender_toplevel.resizable(False, False)

                                # cal_var = StringVar()
                                def selectdate():
                                    global operation_date       
                                    myDate = mycal10.get_date()                        
                                    operation_date = myDate
                                    selectDate = CTkLabel(child_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                    selectDate.place(relx=0.5, rely=0.8, anchor='center')
                                    calender_toplevel.destroy()
                                    

                                mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                                mycal10.place(relx=0.5, rely=0.4, anchor='center')

                                open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                                
                            # cal_button
                            cal_button = CTkButton(child_frame, text='Choose Operation Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.275, rely=0.8, anchor='center')
                            
                            def get_operation_info():
                                name = operation_name.get()
                                doctor = doctor_name.get()
                                hos_name = hospital_name.get()
                                address = address_of_hospital.get()
                                Adhar = adhar_entry.get()

                                try:
                                    Date2 = healthcare_date
                                    # print(Date2)
                                except:
                                    # print(e)
                                    current_date = datetime.now()
                                    # Format the date as "dd/mm/yy"
                                    Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence Adhar Number")
                                    adhar_entry.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    operation_name.delete(0, 'end')

                                elif doctor == "" or doctor.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Doctor Name")
                                    doctor_name.delete(0, 'end')

                                elif hos_name == "" or hos_name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Hospital Name")
                                    hospital_name.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")

                                else:
                                    adhar_from_res = cr.execute("SELECT adhar FROM residence_registration_table")
                                    converted_val = adhar_from_res.fetchall()
                                    resi_result = tuple_to_string(converted_val)

                                    res_pention = cr.execute("SELECT adhar FROM residence_operation_second")
                                    res_con = res_pention.fetchall()
                                    res_result = tuple_to_string(res_con)
                                    
                                    if Adhar not in resi_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")
                                    
                                    elif Adhar in res_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Already Present In Operation 2")

                                    else:
                                        cr.execute("create table if not exists residence_operation_second (name text, doctor text, hospital text, address text, date text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                                        cr.execute("insert into residence_operation_second (name, doctor, hospital, address, date, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(doctor), capitalize_input(hos_name), address, Date2, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Infromation Of Operation 2 Has Been Inserted")
                                
                            
                            CTkButton(child_frame, text="Register", font=("Times New Roman", 20), width=400, fg_color=COLOR, command=get_operation_info).place(relx=0.5, rely=0.95, anchor='center')


                        def operation_3():
                            
                            operation_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Operation *')
                            operation_name.place(relx=0.5, rely=0.2, anchor='center')

                            doctor_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Doctor *')
                            doctor_name.place(relx=0.5, rely=0.35, anchor='center')

                            hospital_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Hospital *')
                            hospital_name.place(relx=0.5, rely=0.5, anchor='center')

                            address_of_hospital = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Address Of Hospital *')
                            address_of_hospital.place(relx=0.5, rely=0.65, anchor='center')

                            # date
                            def cal_fun():
                                # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                                calender_toplevel = tk.Toplevel(child_frame, bg=COLOR)
                                calender_toplevel.title("Checkup Date")
                                calender_toplevel.geometry("400x400")
                                calender_toplevel.resizable(False, False)

                                # cal_var = StringVar()
                                def selectdate():
                                    global operation_date       
                                    myDate = mycal10.get_date()                        
                                    operation_date = myDate
                                    selectDate = CTkLabel(child_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                    selectDate.place(relx=0.5, rely=0.8, anchor='center')
                                    calender_toplevel.destroy()
                                    

                                mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                                mycal10.place(relx=0.5, rely=0.4, anchor='center')

                                open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                                
                            # cal_button
                            cal_button = CTkButton(child_frame, text='Choose Operation Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.275, rely=0.8, anchor='center')
                            
                            def get_operation_info():
                                name = operation_name.get()
                                doctor = doctor_name.get()
                                hos_name = hospital_name.get()
                                address = address_of_hospital.get()
                                Adhar = adhar_entry.get()

                                try:
                                    Date2 = healthcare_date
                                    # print(Date2)
                                except:
                                    # print(e)
                                    current_date = datetime.now()
                                    # Format the date as "dd/mm/yy"
                                    Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence Adhar Number")
                                    adhar_entry.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    operation_name.delete(0, 'end')

                                elif doctor == "" or doctor.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Doctor Name")
                                    doctor_name.delete(0, 'end')

                                elif hos_name == "" or hos_name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Hospital Name")
                                    hospital_name.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")

                                else:
                                    adhar_from_res = cr.execute("SELECT adhar FROM residence_registration_table")
                                    converted_val = adhar_from_res.fetchall()
                                    resi_result = tuple_to_string(converted_val)

                                    res_pention = cr.execute("SELECT adhar FROM residence_operation_third")
                                    res_con = res_pention.fetchall()
                                    res_result = tuple_to_string(res_con)
                                    
                                    if Adhar not in resi_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")
                                    
                                    elif Adhar in res_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Already Present In Operation 3")

                                    else:
                                        cr.execute("create table if not exists residence_operation_third (name text, doctor text, hospital text, address text, date text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                                        cr.execute("insert into residence_operation_third (name, doctor, hospital, address, date, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(doctor), capitalize_input(hos_name), address, Date2, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Infromation Of Operation 3 Has Been Inserted")
                                    
                                
                            
                            CTkButton(child_frame, text="Register", font=("Times New Roman", 20), width=400, fg_color=COLOR, command=get_operation_info).place(relx=0.5, rely=0.95, anchor='center')


                        def operation_4():
                            
                            operation_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Operation *')
                            operation_name.place(relx=0.5, rely=0.2, anchor='center')

                            doctor_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Doctor *')
                            doctor_name.place(relx=0.5, rely=0.35, anchor='center')

                            hospital_name = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Name Of Hospital *')
                            hospital_name.place(relx=0.5, rely=0.5, anchor='center')

                            address_of_hospital = CTkEntry(child_frame, font=("Times New Roman", 20), width=500, border_color=COLOR, placeholder_text='Address Of Hospital *')
                            address_of_hospital.place(relx=0.5, rely=0.65, anchor='center')

                            # date
                            def cal_fun():
                                # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                                calender_toplevel = tk.Toplevel(child_frame, bg=COLOR)
                                calender_toplevel.title("Checkup Date")
                                calender_toplevel.geometry("400x400")
                                calender_toplevel.resizable(False, False)

                                # cal_var = StringVar()
                                def selectdate():
                                    global operation_date       
                                    myDate = mycal10.get_date()                        
                                    operation_date = myDate
                                    selectDate = CTkLabel(child_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                    selectDate.place(relx=0.5, rely=0.8, anchor='center')
                                    calender_toplevel.destroy()
                                    

                                mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                                mycal10.place(relx=0.5, rely=0.4, anchor='center')

                                open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')

                                
                            # cal_button
                            cal_button = CTkButton(child_frame, text='Choose Operation Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.275, rely=0.8, anchor='center')
                            
                            def get_operation_info():
                                name = operation_name.get()
                                doctor = doctor_name.get()
                                hos_name = hospital_name.get()
                                address = address_of_hospital.get()
                                Adhar = adhar_entry.get()

                                try:
                                    Date2 = healthcare_date
                                    # print(Date2)
                                except:
                                    # print(e)
                                    current_date = datetime.now()
                                    # Format the date as "dd/mm/yy"
                                    Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                                if Adhar == "" or Adhar.isnumeric() == False or len(Adhar) != 12:
                                    messagebox.showerror("Error", "Please Enter Valid Residence Adhar Number")
                                    adhar_entry.delete(0, 'end')

                                elif name == "" or name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Name")
                                    operation_name.delete(0, 'end')

                                elif doctor == "" or doctor.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Doctor Name")
                                    doctor_name.delete(0, 'end')

                                elif hos_name == "" or hos_name.isnumeric() == True:
                                    messagebox.showerror("Error", "Please Enter Valid Hospital Name")
                                    hospital_name.delete(0, 'end')

                                elif address == "":
                                    messagebox.showerror("Error", "Please Enter Valid Address")

                                else:
                                    adhar_from_res = cr.execute("SELECT adhar FROM residence_registration_table")
                                    converted_val = adhar_from_res.fetchall()
                                    resi_result = tuple_to_string(converted_val)

                                    res_pention = cr.execute("SELECT adhar FROM residence_operation_fourth")
                                    res_con = res_pention.fetchall()
                                    res_result = tuple_to_string(res_con)
                                    
                                    if Adhar not in resi_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Not Present In System, Please Register First")
                                    
                                    elif Adhar in res_result:
                                        messagebox.showerror("Error", "The Residence Adhar Number Is Already Present In Operation 4")

                                    else:
                                        cr.execute("create table if not exists residence_operation_fourth (name text, doctor text, hospital text, address text, date text, adhar text, FOREIGN KEY (adhar) REFERENCES residence_registration_table(adhar))")
                                        cr.execute("insert into residence_operation_fourth (name, doctor, hospital, address, date, adhar) values(?,?,?,?,?,?)", (capitalize_input(name), capitalize_input(doctor), capitalize_input(hos_name), address, Date2, Adhar))
                                        conn.commit()
                                        messagebox.showinfo("Information", "Infromation Of Operation 4 Has Been Inserted")
                                
                                
                            
                            CTkButton(child_frame, text="Register", font=("Times New Roman", 20), width=400, fg_color=COLOR, command=get_operation_info).place(relx=0.5, rely=0.95, anchor='center')


                        CTkButton(child_frame, text='Operation 1', font=("Times New Roman", 20), fg_color=COLOR, command=operation_1).place(relx=0.175, rely=0.05, anchor='center')
                        CTkButton(child_frame, text='Operation 2', font=("Times New Roman", 20), fg_color=COLOR, command=operation_2).place(relx=0.392, rely=0.05, anchor='center')
                        CTkButton(child_frame, text='Operation 3', font=("Times New Roman", 20), fg_color=COLOR, command=operation_3).place(relx=0.608, rely=0.05, anchor='center')
                        CTkButton(child_frame, text='Operation 4', font=("Times New Roman", 20), fg_color=COLOR, command=operation_4).place(relx=0.825, rely=0.05, anchor='center')


                        def cal_fun():
                            # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                            calender_toplevel = tk.Toplevel(child_frame, bg=COLOR)
                            calender_toplevel.title("Checkup Date")
                            calender_toplevel.geometry("400x400")
                            calender_toplevel.resizable(False, False)

                            # cal_var = StringVar()
                            def selectdate():
                                global healthcare_date       
                                myDate = mycal10.get_date()                        
                                healthcare_date = myDate
                                selectDate = CTkLabel(child_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                selectDate.place(relx=0.3, rely=0.45, anchor='center')
                                calender_toplevel.destroy()
                                

                            mycal10 = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                            mycal10.place(relx=0.5, rely=0.4, anchor='center')

                            open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectdate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')



                        def get_all_healthcare_info():
                            try:
                                Date2 = healthcare_date
                                # print(Date2)
                            except:
                                # print(e)
                                current_date = datetime.now()
                                # Format the date as "dd/mm/yy"
                                Date2 = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'


                        



                    def view_healthcare_information():
                        view_information_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
                        view_information_frame.place(relx=0.5, rely=0.5, anchor='center')

                        # search bar
                        search_bar = CTkEntry(view_information_frame, width=400, border_color=COLOR, font=("Times New Roman", 20), placeholder_text="eg. Name or Adhar")
                        search_bar.place(relx=0.46, rely=0.2, anchor='center')

                        conn = sqlite3.connect(resource_path("second_child.db"))
                        cr = conn.cursor()



                        # ======================================================================
                        
                        def verify_data(final_residence):
                            def fetch_data():
                                # Connect to the SQLite database
                                conn = sqlite3.connect(resource_path('second_child.db'))
                                cursor = conn.cursor()

                                # Fetch all data from the 'students' table
                                if final_residence is None:
                                    cursor.execute(f'SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table')
                                    data = cursor.fetchall()
                                    return data
                                elif final_residence.isnumeric() == True:
                                    try:
                                        resi_var = cr.execute(f"SELECT adhar from residence_registration_table where adhar = '{final_residence}'")
                                        final_residence2 = resi_var.fetchone()
                                        final_residence3 = list_to_string(final_residence2)
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table where adhar = '{final_residence3}'")
                                        data2 = cursor.fetchall()
                                        return data2
                                    except:
                                        messagebox.showerror("Error", "This Adhar Number Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                else:
                                    try:
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile FROM residence_registration_table where name = '{final_residence}'")
                                        data5 = cursor.fetchall()
                                        return data5
                                    except:
                                        messagebox.showerror("Error", "This Name Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')


                            columns = ('Name', 'Age', 'Gender', 'Address line 1', 'Address line 2', 'Adhar', 'Mobile')
                            tree = ttk.Treeview(view_information_frame, columns=columns, show='headings')

                            tree.column("Name", width=500) 
                            tree.column("Age", width=50)
                            tree.column("Gender", width=50)
                            tree.column("Address line 1", width=400)
                            tree.column("Address line 2", width=400)
                            tree.column("Adhar", width=100)
                            tree.column("Mobile", width=100)

                            def set_alternate_row_colors(tree, color1, color2):
                                for i, item in enumerate(tree.get_children()):
                                    color = color1 if i % 2 == 0 else color2
                                    tree.item(item, tags=(f"row_{i}",))
                                    tree.tag_configure(f"row_{i}", background=color)

                            for col in columns:
                                tree.heading(col, text=col)
                                tree.column(col, anchor='center')

                            # Populate the Treeview with data
                            data = fetch_data()
                            for row in data:
                                tree.insert('', 'end', values=row)
                                tree.tag_configure(tagname=row, background='cyan')
                                set_alternate_row_colors(tree, "lightblue", "#ebc7f9")
                                # tree.tag_add(tag_name, row_index)

                            style = ttk.Style()
                
                            # Set font size for column headings
                            style.configure("Treeview.Heading", font=("Times New Roman", 14))
                            style.configure("Treeview", font=("Times New Roman", 12))
                                        
                            # Pack the Treeview and Scrollbar
                            scrollbar = ttk.Scrollbar(view_information_frame, orient='vertical', command=tree.yview)
                            tree.configure(yscrollcommand=scrollbar.set)
                            tree.place(relx=0.495, rely=0.475, anchor='center', width=WIDTH, height=600)
                            scrollbar.place(relx=0.895, rely=0.475, anchor='center', height=600)
                            # Add a vertical scrollbar to the Treeview
                            
                            

                            def show_more_info(tree):
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]
                                    view_information_frame2 = CTkFrame(view_information_frame, width=WIDTH, height=HEIGHT).place(relx=0.5, rely=0.5, anchor='center')
                                    
                                    # Connect to the SQLite database
                                    conn2 = sqlite3.connect(resource_path('second_child.db'))
                                    cursor2 = conn2.cursor()
                                    

                                    # ===========================
                                    def get_image_data():
                                        conn = sqlite3.connect(resource_path('second_child.db'))
                                        cursor = conn.cursor()
                                        cursor.execute(f"SELECT * FROM residence_registration_table WHERE adhar = '{adhar_number}'")
                                        image_data = cursor.fetchone()[8]
                                        conn.close()
                                        return image_data

                                    def display_image_on_label():
                                        image_data = get_image_data()
                                        image = Image.open(BytesIO(image_data))
                                        resized_image2 = image.resize((180, 185))
                                        photo = ImageTk.PhotoImage(resized_image2)

                                        label = tk.Label(view_information_frame2, image=photo)
                                        label.photo = photo  # Keep a reference to the photo to prevent garbage collection
                                        label.place(relx=0.1, rely=0.1, anchor='center')

                                    display_image_on_label()
                                    # =======================

                                    columns2 = ('Name', 'Age', 'Date', 'Gender', 'Address_line_1', 'Address_line_2', 'Adhar', 'Mobile')

                                    tree2 = ttk.Treeview(view_information_frame2, columns=columns2, show='headings')
                                    tree2.place(relx=0.5, rely=0.24, anchor='center', width=WIDTH, height=50)
                                    
                                    
                                    tree2.column("Name", width=500) 
                                    tree2.column("Age", width=50)
                                    tree2.column("Date", width=200)
                                    tree2.column("Gender", width=50)
                                    tree2.column("Address_line_1", width=400)
                                    tree2.column("Address_line_2", width=400)
                                    tree2.column("Adhar", width=100)
                                    tree2.column("Mobile", width=100)
                                    # tree2.column("Pention", width=100)

                                    def fetch_data3():
                                        # Connect to the SQLite database
                                        conn = sqlite3.connect(resource_path('second_child.db'))
                                        cursor = conn.cursor()

                                        # Fetch all data from the 'students' table
                                        cursor.execute(f'SELECT name, age, date, gender, address_line_1, address_line_2,adhar, adhar, mobile FROM residence_registration_table where adhar = {adhar_number}')
                                        data4 = cursor.fetchall()

                                        return data4

                                    for col2 in columns2:
                                        tree2.heading(col2, text=col2)
                                        tree2.column(col2, anchor='center')

                                    data2 = fetch_data3()
                                    for row2 in data2:
                                        tree2.insert('', 'end', values=row2)  




                                    columns3 = ('ID', 'Doctor Name', 'Disease Name', 'Checkup Date')

                                    tree3 = ttk.Treeview(view_information_frame2, columns=columns3, show='headings')
                                    
                                    
                                    tree3.column("ID", width=100)
                                    tree3.column("Doctor Name", width=700) 
                                    tree3.column("Disease Name", width=700)
                                    tree3.column("Checkup Date", width=100)

                                    

                                    for col3 in columns3:
                                        tree3.heading(col3, text=col3)
                                        tree3.column(col3, anchor='center')

                                    try:
                                        # Fetch all data from the 'students' table
                                        cursor = cursor2.execute(f'SELECT id, doctor, disease, date from residence_healthcare where adhar = {adhar_number}')
                                        data3 = cursor.fetchall()
                                        for row3 in data3:
                                            tree3.insert('', 'end', values=row3)                                    
                                    except:
                                        pass

                                    vsb2 = ttk.Scrollbar(view_information_frame2, orient='vertical', command=tree3.yview)
                                    tree3.configure(yscrollcommand=vsb2.set)
                                    tree3.place(relx=0.495, rely=0.4, anchor='center', width=WIDTH, height=200)
                                    vsb2.place(relx=0.995, rely=0.4, anchor='center', height=200)
                                    
                                    

                                    

                                    def show_prescription():
                                        try:
                                            
                                            selected_item21 = tree3.selection()
                                            checkupdate21 = tree3.item(selected_item21, "values")[0]



                                            # ===========
                                            columns41 = ('Prescription')

                                            tree41 = ttk.Treeview(view_information_frame2, columns=columns41, show='headings')


                                            tree41.column("Prescription", width=1000)
                                            tree41.heading(0, text="Prescription")
                                            tree41.column(0, anchor='center')

                                        
                                            fetched_data = cr.execute(f"SELECT prescription from residence_healthcare where id = '{checkupdate21}'").fetchone()
                                            result = tuple_to_string(fetched_data)
                                            x = result.split('\n')
                                            
                                            try:
                                                for i in x:
                                                    tree41.insert("", 'end', values=(i,))
                                            except:
                                                pass

                                            vsb = ttk.Scrollbar(view_information_frame2, orient="vertical", command=tree41.yview)
                                            tree41.configure(yscrollcommand=vsb.set)
                                            tree41.place(relx=0.495, rely=0.64, anchor='center', width=WIDTH, height=200)
                                            vsb.place(relx=0.995, rely=0.64, anchor='center', height=200)
                                            # ===========

                                            
                                        except:
                                            messagebox.showerror("Error", "Please Select A Row")    


                                    CTkButton(view_information_frame2, text='Show Prescription', font=("Times New Roman", 22), fg_color=COLOR, command=show_prescription).place(relx=0.5, rely=0.8, anchor='center')               

                                    def delete_healthcare_record():
                                        # =======================
                                        try:
                                            selected_item33 = tree3.selection()
                                            adhar_number33 = tree3.item(selected_item33, "values")[0]

                                            conn33 = sqlite3.connect(resource_path("second_child.db"))
                                            cr33 = conn33.cursor()

                                            
                                            try:
                                                cr33.execute(f"delete from residence_healthcare where id = {adhar_number33}")
                                            except:
                                                pass

                                            conn33.commit()
                                            conn33.close()

                                            messagebox.showinfo("Detete Information", "Record Has Been Deleted!")
                                            view_healthcare_information()
                                        except:
                                            messagebox.showerror("Error", "Please Select A row")
                                                # =======================

                                    CTkButton(view_information_frame2, text='Delete', font=("Times New Roman", 22), fg_color=COLOR, command=delete_healthcare_record).place(relx=0.64, rely=0.8, anchor='center')
                                    # Back Button                       
                                    CTkButton(view_information_frame2, text='< Back', font=("Times New Roman", 22), fg_color=COLOR, command=view_healthcare_information).place(relx=0.36, rely=0.8, anchor='center')
                                except:
                                    messagebox.showerror("Error", "Please Select A Row")

                            # view more info button
                            view_more_info_btn = CTkButton(view_information_frame, text="View More", font=("Times New Roman", 22), fg_color=COLOR, command=lambda: show_more_info(tree))
                            view_more_info_btn.place(relx=0.45, rely=0.76, anchor='center')


                            def delete_all_record():
                                
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()

                                    
                                    try:
                                        cr.execute(f"delete from residence_registration_table where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_relative_first where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_relative_second where adhar = '{adhar_number}'")
                                    except:
                                        pass



                                    try:
                                        cr.execute(f"delete from reisidence_relative_third where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_relative_fourth where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_first where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_second where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_operation_third where adhar = '{adhar_number}'")
                                    except:
                                        pass


                                    try:
                                        cr.execute(f"delete from reisidence_operation_fourth where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    try:
                                        cr.execute(f"delete from reisidence_pention where adhar = '{adhar_number}'")
                                    except:
                                        pass

                                    conn.commit()
                                    conn.close()

                                    messagebox.showinfo("Detete Information", "Record Has Been Deleted!")
                                    view_information()
                                except:
                                    messagebox.showerror("Error", "Please Select A row")

                            # delete btn
                            delete_btn = CTkButton(view_information_frame, text='Delete', font=("Times New Roman", 22), fg_color=COLOR, command=delete_all_record).place(relx=0.55, rely=0.76, anchor='center')

                            



                        def search_data():
                            def capitalize_input(input_str):
                                words = input_str.split()
                                capitalized_words = [word.capitalize() for word in words]
                                return ' '.join(capitalized_words)
                            # Capitalize the first letter of each word
                            residence_name = capitalize_input(search_bar.get())

                            if residence_name == "":
                                messagebox.showerror("Error", "Please Enter Name or Adhar")
                            else:                    
                                if residence_name.isnumeric() == True and len(residence_name) == 12: # numbers
                                    verify_data(residence_name)
                                        
                                else:     
                                    try:                                
                                        resi_var2 = cr.execute(f"SELECT name from residence_registration_table where name = '{residence_name}'")
                                        final_residence2 = resi_var2.fetchone()
                                        final_residence3 = list_to_string(final_residence2)

                                        if residence_name in final_residence3:

                                            
                                            verify_data(residence_name)
                                        else:
                                            pass
                                    except:
                                        messagebox.showerror("Error", "Entered Value Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                    

                        # search button
                        search_button = CTkButton(view_information_frame, text="Search", font=("Times New Roman", 22), fg_color="#3377ff", command=search_data)
                        search_button.place(relx=0.62, rely=0.2, anchor='center')

                        verify_data(final_residence=None)


                    def add_new_donar():
                        add_new_donar_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)

                        # new donar heading
                        name_label = CTkLabel(add_new_donar_frame, text="New Donar", font=("Times New Roman", 50), text_color=COLOR)
                        name_label.place(relx=0.5, rely=0.175, anchor='center')

            
                        # name entry
                        name_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Name Of Donar *')
                        name_entry.place(relx=0.3, rely=0.25, anchor='center')
                        
                        # mobile no entry
                        mobile_no_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Donar Mobile Number *')
                        mobile_no_entry.place(relx=0.3, rely=0.34, anchor='center')

                        # Age no entry
                        age_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Age *')
                        age_entry.place(relx=0.3, rely=0.44, anchor='center')

                        # age label
                        # age_label = CTkLabel(add_new_donar_frame, text="Age", font=("Times New Roman", 28), width=50)
                        # age_label.place(relx=0.155, rely=0.34, anchor='center')


                        # def age_fun(val):
                        #     # Age reflection
                        #     CTkLabel(add_new_donar_frame, text=str(val), font=("Times New Roman", 18), width=100).place(relx=0.32, rely=0.31, anchor='center')
                        
                        
                        # dum = IntVar()
                        # CTkLabel(add_new_donar_frame, text=dum.get(), font=("Times New Roman", 18), width=100).place(relx=0.32, rely=0.31, anchor='center')
                        
                        # Age entry
                        # CTkSlider(add_new_donar_frame, from_=0, to=120, number_of_steps=120, width=500, command=age_fun, variable=dum).place(relx=0.327, rely=0.34, anchor='center')





                        # gender label
                        gender_label = CTkLabel(add_new_donar_frame, text="Gender", font=("Times New Roman", 28), width=50)
                        gender_label.place(relx=0.165, rely=0.54, anchor='center')


                        Gender = StringVar()
                        Gender.set("Male")

                        # Gender Male
                        gender_male = CTkRadioButton(add_new_donar_frame, text="Male", font=("Times New Roman", 18), value="Male", variable=Gender)
                        gender_male.place(relx=0.245, rely=0.54, anchor='center')

                        # Gender Female
                        gender_female = CTkRadioButton(add_new_donar_frame, text="Female", font=("Times New Roman", 18), value="Female", variable=Gender)
                        gender_female.place(relx=0.345, rely=0.54, anchor='center')

                        # Gender Other
                        gender_other = CTkRadioButton(add_new_donar_frame, text="Other", font=("Times New Roman", 18), value="Other", variable=Gender)
                        gender_other.place(relx=0.445, rely=0.54, anchor='center')



                        

                        # address label 1 label
                        # address_label_1_label = tk.Label(add_new_donar_frame, text="Address Line 1", font=("Times New Roman", 20))
                        # address_label_1_label.place(x=1000, y=130)

                        # address label 1 entry
                        address_label_1_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Address Line 1 *')
                        address_label_1_entry.place(relx=0.7, rely=0.25, anchor='center')

                        # address entry 2 label
                        # address_label_2 = tk.Label(add_new_donar_frame, text="Address Line 2", font=("Times New Roman", 20))
                        # address_label_2.place(x=1000, y=230)

                        # address entry 2 entry
                        address_label_2_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text="Address Line 2 *")
                        address_label_2_entry.place(relx=0.7, rely=0.34, anchor='center')

                        # type of donation label
                        # type_of_donation_label = tk.Label(add_new_donar_frame, text="Donation", font=("Times New Roman", 20))
                        # type_of_donation_label.place(x=1000, y=330)


                        # adhar no entry
                        adhar_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text='Donar Adhar Numbar *')
                        adhar_entry.place(relx=0.7, rely=0.44, anchor='center')



                        # type of donation entry
                        type_of_donation_entry = CTkEntry(add_new_donar_frame, font=("Times New Roman", 20), border_color=COLOR, width=600, placeholder_text="Donation *")
                        type_of_donation_entry.place(relx=0.7, rely=0.54, anchor='center')



                        def cal_fun():
                            # cal = DateEntry(operation_form, width=20, background=COLOR, foreground=COLOR, borderwidth=2, font=("Times New Roman", 16), placeholder_text="DD/MM/YYYY").place(relx=0.45, rely=0.58, anchor='center')
                            calender_toplevel = tk.Toplevel(add_new_donar_frame, bg=COLOR)
                            calender_toplevel.title("Donation Date")
                            calender_toplevel.geometry("400x400")
                            calender_toplevel.resizable(False, False)

                            # cal_var = StringVar()
                            def selectDate():
                                global donation_date                         
                                myDate = mycal.get_date()
                                donation_date = myDate
                                selectDate = CTkLabel(add_new_donar_frame,text=myDate, width=10, font=("Times New Roman", 18))
                                selectDate.place(relx=0.3, rely=0.65, anchor='center')
                                calender_toplevel.destroy()
                                

                            mycal = Calendar(calender_toplevel, setmode='day', date_pattern='d/m/yy', font=("Times New Roman", 18))
                            mycal.place(relx=0.5, rely=0.4, anchor='center')

                            open_cal = CTkButton(calender_toplevel, text='Set Date', command=selectDate, font=("Times New Roman", 18)).place(relx=0.5, rely=0.9, anchor='center')


                        # cal_button
                        cal_button = CTkButton(add_new_donar_frame, text='Choose Donation Date', font=("Times New Roman", 18), command=cal_fun).place(relx=0.19, rely=0.65, anchor='center')
                        


                        def get_all_donar_info():                    
                            # donar validation
                            Age = age_entry.get()

                            try:
                                Date = donation_date
                            except:
                                current_date = datetime.now()
                                Date = f'{current_date.day}/{current_date.month}/{current_date.year % 100:02}'

                            if name_entry.get().isnumeric() == True or name_entry.get() == "":
                                messagebox.showerror("Error", "Please Enter Valid Name")
                                name_entry.delete(0, 'end')

                            
                            elif mobile_no_entry.get().isnumeric() == False or mobile_no_entry.get() == "" or len(mobile_no_entry.get()) != 10:
                                messagebox.showerror("Error", "Please Enter Valid Mobile No.")
                                mobile_no_entry.delete(0, 'end')

                            elif Age == "" or Age.isnumeric() == False:
                                messagebox.showerror("Error", "Please Enter Valid Age")
                                age_entry.delete(0, 'end')

                        
                            elif address_label_1_entry.get() == "":
                                messagebox.showerror("Error", "Please Fill Address Line 1")

                            elif address_label_2_entry.get() == "":
                                messagebox.showerror("Error", "Please Fill Address Line 2")

                            elif adhar_entry.get().isnumeric() == False or adhar_entry.get() == "" or len(adhar_entry.get()) != 12:
                                messagebox.showerror("Error", "Please Enter Valid Adhar")
                                adhar_entry.delete(0, 'end')

                            elif type_of_donation_entry.get() == "":
                                messagebox.showerror("Error", "Please Enter Valid Donation")

                            else:
                                def capitalize_input(input_str):
                                    words = input_str.split()
                                    capitalized_words = [word.capitalize() for word in words]
                                    return ' '.join(capitalized_words)
                                
                                conn = sqlite3.connect(resource_path("second_child.db"))
                                cr = conn.cursor()
                                cr.execute("CREATE TABLE IF NOT EXISTS donar_info(name TEXT, mobile TEXT, age TEXT, gender TEXT, date TEXT, address_line_1 TEXT, address_line_2 TEXT, adhar TEXT, type_of_donation TEXT)")
                                cr.execute("INSERT INTO donar_info(name, mobile, age, gender, date, address_line_1, address_line_2, adhar, type_of_donation) values(?,?,?,?,?,?,?,?,?)", (capitalize_input(name_entry.get()), mobile_no_entry.get(), Age, Gender.get(), Date, address_label_1_entry.get(), address_label_2_entry.get(), adhar_entry.get(), type_of_donation_entry.get()))
                                conn.commit()
                                messagebox.showinfo("Information","Record Has Been Succesfully Saved!")
                                add_new_donar()


                        # register donar button
                        register_donar_button = CTkButton(add_new_donar_frame, text="Register Donar", font=("Times New Roman", 20),fg_color=COLOR, width=800, command=get_all_donar_info)
                        register_donar_button.place(relx=0.5, rely=0.8, anchor='center')

                        add_new_donar_frame.place(relx=0.5, rely=0.5, anchor='center')


                    def view_donar_information():
                        # ========================
                        view_donar_information_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)
                        view_donar_information_frame.place(relx=0.5, rely=0.5, anchor='center')

                        # search bar
                        search_bar = CTkEntry(view_donar_information_frame, width=400, border_color=COLOR, font=("Times New Roman", 20), placeholder_text="eg. Name or Adhar")
                        search_bar.place(relx=0.46, rely=0.2, anchor='center')

                        conn = sqlite3.connect(resource_path("second_child.db"))
                        cr = conn.cursor()



                        # ======================================================================
                        
                        def verify_data(final_residence):
                            def fetch_data():
                                # Connect to the SQLite database
                                conn = sqlite3.connect(resource_path('second_child.db'))
                                cursor = conn.cursor()

                                # Fetch all data from the 'students' table
                                if final_residence is None:
                                    cursor.execute(f'SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile, type_of_donation, date FROM donar_info')
                                    data = cursor.fetchall()
                                    return data
                                elif final_residence.isnumeric() == True:
                                    try:
                                        resi_var = cr.execute(f"SELECT adhar from donar_info where adhar = '{final_residence}'")
                                        final_residence2 = resi_var.fetchone()
                                        final_residence3 = list_to_string(final_residence2)
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile, type_of_donation, date FROM donar_info where adhar = '{final_residence3}'")
                                        data2 = cursor.fetchall()
                                        return data2
                                    except:
                                        messagebox.showerror("Error", "This Adhar Number Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                else:
                                    try:
                                        cursor.execute(f"SELECT name, age, gender, address_line_1, address_line_2,adhar, mobile, type_of_donation, date FROM donar_info where name = '{final_residence}'")
                                        data5 = cursor.fetchall()
                                        return data5
                                    except:
                                        messagebox.showerror("Error", "This Name Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')


                            columns = ('Name', 'Age', 'Gender', 'Address line 1', 'Address line 2', 'Adhar', 'Mobile', 'Donation', 'Date')
                            tree = ttk.Treeview(view_donar_information_frame, columns=columns, show='headings')

                            tree.column("Name", width=500) 
                            tree.column("Age", width=50)
                            tree.column("Gender", width=50)
                            tree.column("Address line 1", width=300)
                            tree.column("Address line 2", width=300)
                            tree.column("Adhar", width=100)
                            tree.column("Mobile", width=100)
                            tree.column("Donation", width=100)
                            tree.column("Date", width=100)

                            def set_alternate_row_colors(tree, color1, color2):
                                for i, item in enumerate(tree.get_children()):
                                    color = color1 if i % 2 == 0 else color2
                                    tree.item(item, tags=(f"row_{i}",))
                                    tree.tag_configure(f"row_{i}", background=color)

                            for col in columns:
                                tree.heading(col, text=col)
                                tree.column(col, anchor='center')

                            # Populate the Treeview with data
                            data = fetch_data()
                            for row in data:
                                tree.insert('', 'end', values=row)
                                tree.tag_configure(tagname=row, background='cyan')
                                set_alternate_row_colors(tree, "lightblue", "#ebc7f9")
                                # tree.tag_add(tag_name, row_index)

                            style = ttk.Style()
                
                            # Set font size for column headings
                            style.configure("Treeview.Heading", font=("Times New Roman", 14))
                            style.configure("Treeview", font=("Times New Roman", 12))
                                        

                            # Add a vertical scrollbar to the Treeview
                            scrollbar = ttk.Scrollbar(view_donar_information_frame, orient='vertical', command=tree.yview)
                            tree.configure(yscrollcommand=scrollbar.set)
                            # Pack the Treeview and Scrollbar
                            tree.place(relx=0.495, rely=0.475, anchor='center', width=WIDTH, height=600)
                            # tree.pack(expand=True, fill="both")
                            scrollbar.place(relx=0.895, rely=0.475, anchor='center', height=600)

                            def delete_all_record():
                                
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()

                                    
                                    try:
                                        cr.execute(f"delete from donar_info where adhar = '{adhar_number}'")
                                    except:
                                        pass
                                    conn.commit()
                                    conn.close()

                                    messagebox.showinfo("Detete Information", "Record Has Been Deleted!")
                                    view_donar_information()
                                except:
                                    messagebox.showerror("Error", "Please Select A row")

                            # delete btn
                            delete_btn = CTkButton(view_donar_information_frame, text='Delete', font=("Times New Roman", 22), fg_color=COLOR, command=delete_all_record).place(relx=0.5, rely=0.76, anchor='center')

                            def update_registration_info():
                                try:
                                    selected_item = tree.selection()
                                    adhar_number = tree.item(selected_item, "values")[5]

                                    update_registration = tk.Toplevel(view_donar_information_frame)
                                    update_registration.geometry("900x600")
                                    # ===============
                                    update_registration.title("Update Information")
                                    update_registration.resizable(False, False)
                                    

                                    # name of relation entry
                                    name_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Full Name')
                                    name_entry.place(relx=0.5, rely=0.13, anchor='center')


                                    # relation with person entry
                                    address_line_1_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Address Line 1')
                                    address_line_1_entry.place(relx=0.5, rely=0.29, anchor='center')

                                    # relative address 1 entry
                                    address_line_2_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Address Line 2')
                                    address_line_2_entry.place(relx=0.5, rely=0.45, anchor='center')

                                    # relative address 2 entry
                                    adhar_number_entry = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text='Adhar Number')
                                    adhar_number_entry.place(relx=0.5, rely=0.61, anchor='center')

                                    # relative phone entry
                                    phone_number_entry = CTkEntry(update_registration, font=("Times New Roman", 18), width=700, placeholder_text='Phone Number')
                                    phone_number_entry.place(relx=0.5, rely=0.77, anchor='center')

                                    def registration_validation():
                                        conn = sqlite3.connect(resource_path("second_child.db"))
                                        cr = conn.cursor()

                                        if name_entry.get() == "" and address_line_1_entry.get() == "" and address_line_2_entry.get() == "" and adhar_number_entry.get() == "" and phone_number_entry.get() == "":
                                            messagebox.showinfo("Update Information", "Data is not updated!")
                                            update_registration.destroy()
                                            view_donar_information()
                                        else:
                                            if name_entry.get() == "": 
                                                pass
                                            else:          
                                                if name_entry.get().isnumeric() == True:
                                                    messagebox.showerror("Error", "Name can not be inserted")
                                                else:
                                                    cr.execute(f"update donar_info set name = '{capitalize_input(name_entry.get())}' where adhar = '{adhar_number}'")
                                                    

                                            if address_line_1_entry.get() == "":
                                                pass
                                            else:
                                                cr.execute(f"update donar_info set address_line_1 = '{address_line_1_entry.get()}' where adhar = '{adhar_number}'")

                                            if address_line_2_entry.get() == "":
                                                pass
                                            else:
                                                cr.execute(f"update donar_info set address_line_2 = '{address_line_2_entry.get()}' where adhar = '{adhar_number}'")
                                                
                                            if adhar_number_entry.get() == "":
                                                pass
                                            else:
                                                if adhar_number_entry.get().isnumeric() == False or adhar_number_entry.get() == "" or len(adhar_number_entry.get()) != 12:
                                                    messagebox.showerror("Error", "Adhar number can not be inserted")
                                                    adhar_number_entry.delete(0, 'end')
                                                else:
                                                    cr.execute(f"update donar_info set adhar = '{adhar_number_entry.get()}' where adhar = '{adhar_number}'")

                                            if phone_number_entry.get() == "":
                                                pass
                                            else:
                                                if phone_number_entry.get().isnumeric() == False or phone_number_entry.get() == "" or len(phone_number_entry.get()) != 10:
                                                    messagebox.showerror("Error", "Mobile number can not be inserted")
                                                    phone_number_entry.delete(0, 'end')      
                                                else:
                                                    cr.execute(f"update donar_info set mobile = '{phone_number_entry.get()}' where adhar = '{adhar_number}'")                              
                                            
                                            # conn.commit()
                                            # conn.close()
                                            update_registration.destroy()
                                            messagebox.showinfo("Update Information", "Successfully Updated!")
                                            conn.commit()
                                            conn.close()
                                            view_donar_information()
                                            
                                    CTkButton(update_registration, text='Save', font=("Times New Roman", 18), width=200, fg_color=COLOR, command=registration_validation).place(relx=0.5, rely=0.93, anchor='center')


                                    # relative adhar number
                                    # relative_adhar_entry1 = CTkEntry(update_registration, font=("Times New Roman", 20), width=700, placeholder_text="Adhar Number *")
                                    # relative_adhar_entry1.place(relx=0.5, rely=0.84, anchor='center')

                                    # ===============

                                    conn = sqlite3.connect(resource_path("second_child.db"))
                                    cr = conn.cursor()
                                except:
                                    messagebox.showerror("Error", "Please Select A row")
                            # update btn
                            CTkButton(view_donar_information_frame, text='Update', font=("Times New Roman", 22), fg_color=COLOR, command=update_registration_info).place(relx=0.4, rely=0.76, anchor='center')


                            def generate_pdf():
                                # ===============
                                file_path = filedialog.asksaveasfilename(defaultextension="_All_Donar_Information.pdf")

                                # =========
                                def create_pdf(names, ages, donations, adhars, mobiles, dates, output_filename):
                                    # Create a PDF document
                                    pdf_canvas = canvas.Canvas(output_filename, pagesize=letter)

                                    # Set up column coordinates
                                    column_width = letter[0] / 5
                                    column_height = letter[1] - 50

                                    # Set up font
                                    pdf_canvas.setFont("Helvetica", 12)

                                    # Draw column headers
                                    pdf_canvas.drawString(45, column_height, "Name")
                                    pdf_canvas.drawString(column_width + 67, column_height, "Age")
                                    pdf_canvas.drawString(column_width + 130, column_height, "Donation")
                                    pdf_canvas.drawString(column_width + 240, column_height, "Adhar")
                                    pdf_canvas.drawString(column_width + 345, column_height, "Mobile")
                                    pdf_canvas.drawString(column_width + 430, column_height, "Date")

                                    # Draw data in columns
                                    for i, (name, age, donation, adhar, mobile, date) in enumerate(zip(names, ages, donations, adhars, mobiles, dates), start=1):
                                        row_height = column_height - i * 15
                                        pdf_canvas.drawString(15, row_height, name)
                                        pdf_canvas.drawString(column_width + 68, row_height, str(age))
                                        pdf_canvas.drawString(column_width + 130, row_height, str(donation))
                                        pdf_canvas.drawString(column_width + 215, row_height, str(adhar))
                                        pdf_canvas.drawString(column_width + 330, row_height, str(mobile))
                                        pdf_canvas.drawString(column_width + 425, row_height, str(date))


                                    # Save the PDF
                                    pdf_canvas.save()

                                # Example data

                                name_ = cr.execute(f"select name from donar_info")
                                name_1 = name_.fetchall()

                                age_ = cr.execute(f"select age from donar_info")
                                age_1 = age_.fetchall()

                                donation_ = cr.execute(f"select type_of_donation from donar_info")
                                donation_1 = donation_.fetchall()

                                adhar_ = cr.execute(f"select adhar from donar_info")
                                adhar_1 = adhar_.fetchall()

                                mobile_ = cr.execute(f"select mobile from donar_info")
                                mobile_1 = mobile_.fetchall()

                                date_ = cr.execute(f"select date from donar_info")
                                date_1 = date_.fetchall()

                                cleaned_names = []
                                for n in name_1:
                                    cleaned_names.append(n[0])

                                cleaned_age = []
                                for a in age_1:
                                    cleaned_age.append(a[0])

                                cleaned_donation = []
                                for g in donation_1:
                                    cleaned_donation.append(g[0])

                                
                                cleaned_adhar = []
                                for ad in adhar_1:
                                    cleaned_adhar.append(ad[0])

                                cleaned_mobile = []
                                for m in mobile_1:
                                    cleaned_mobile.append(m[0])

                                cleaned_date = []
                                for m in date_1:
                                    cleaned_date.append(m[0])
                                    

                                # Output PDF filename
                                output_filename = f"{file_path}"

                                # Generate PDF
                                create_pdf(cleaned_names, cleaned_age, cleaned_donation, cleaned_adhar, cleaned_mobile, cleaned_date, output_filename)
                                # ========
                                
                            # generate pdf button
                            CTkButton(view_donar_information_frame, text='Generate PDF', font=("Times New Roman", 22), fg_color=COLOR, command=generate_pdf).place(relx=0.6, rely=0.76, anchor='center')

                            # ======================================================================



                        def search_data():
                            def capitalize_input(input_str):
                                words = input_str.split()
                                capitalized_words = [word.capitalize() for word in words]
                                return ' '.join(capitalized_words)
                            # Capitalize the first letter of each word
                            residence_name = capitalize_input(search_bar.get())

                            if residence_name == "":
                                messagebox.showerror("Error", "Please Enter Name or Adhar")
                            else:                    
                                if residence_name.isnumeric() == True and len(residence_name) == 12: # numbers
                                    verify_data(residence_name)
                                        
                                else:     
                                    try:                                
                                        resi_var2 = cr.execute(f"SELECT name from donar_info where name = '{residence_name}'")
                                        final_residence2 = resi_var2.fetchone()
                                        final_residence3 = list_to_string(final_residence2)

                                        if residence_name in final_residence3:

                                            
                                            verify_data(residence_name)
                                        else:
                                            pass
                                    except:
                                        messagebox.showerror("Error", "Entered Value Does Not Exist In This System!")
                                        search_bar.delete(0, 'end')
                                    

                        # search button
                        search_button = CTkButton(view_donar_information_frame, text="Search", font=("Times New Roman", 22), fg_color="#3377ff", command=search_data)
                        search_button.place(relx=0.62, rely=0.2, anchor='center')

                        verify_data(final_residence=None)
                        # ======================



                    frame1.destroy()
                    after_login_frame = CTkFrame(win, width=WIDTH, height=HEIGHT)

                    
                    path2 = resource_path('second_childhood3.png')

                    # Create an object of tkinter ImageTk
                    image1 = Image.open(path2)
                    resized_image2 = image1.resize((WIDTH, HEIGHT))
                    img = ImageTk.PhotoImage(resized_image2)

                    # Create a Label Widget to display the text or Image
                    label1 = CTkLabel(after_login_frame, image = img, text="")
                    label1.image = img
                    label1.place(relx=0.5, rely=0.5, anchor='center')

                    path = resource_path('shantai.png')
                    image2 = Image.open(path)
                    resized_image2 = image2.resize((200, 200))

                    image3 = ImageTk.PhotoImage(resized_image2)
                    label2 = CTkLabel(after_login_frame, image=image3, text="")
                    label2.image = image3
                    label2.place(relx=0.2, rely=0.3, anchor='center')

                    my_menu = tk.Menu(win, font=("Times New Roman", 30))
                    win.config(menu=my_menu)

                    edit_menu = tk.Menu(my_menu)
                    my_menu.add_cascade(label='  Home  ', menu=edit_menu)
                    edit_menu.add_command(label='                   Home                    ', font=("Times New Roman", 16), command=home_page)
                    

                    file_menu = tk.Menu(my_menu)
                    my_menu.add_cascade(label='  Residence  ', menu=file_menu)
                    file_menu.add_command(label='        Add New Residence        ', font=("Times New Roman", 16), command=add_information)
                    file_menu.add_separator()
                    file_menu.add_command(label='    Add New Relative & Pention   ', font=("Times New Roman", 16), command=add_new_relative)
                    file_menu.add_separator()
                    file_menu.add_command(label='        View Information         ', font=("Times New Roman", 16), command=view_information)
                    
                    service_menu = tk.Menu(my_menu)
                    my_menu.add_cascade(label="HealthCare", menu=service_menu)
                    service_menu.add_command(label='Add HealthCare Information ', font=("Times New Roman", 16), command=add_healthcare_information)
                    service_menu.add_separator()
                    service_menu.add_command(label='Add Operation Information  ', font=("Times New Roman", 16), command=add_operation_information)
                    service_menu.add_separator()
                    service_menu.add_command(label='View HealthCare Information', font=("Times New Roman", 16), command=view_healthcare_information)


                    information_menu = tk.Menu(my_menu)
                    my_menu.add_cascade(label='  Donations  ', menu=information_menu)
                    information_menu.add_command(label='         Add New Donar        ', font=("Times New Roman", 16), command=add_new_donar)
                    information_menu.add_separator()
                    information_menu.add_command(label='         View All Donations       ', font=("Times New Roman", 16), command=view_donar_information)
                    
                    user_menu = tk.Menu(my_menu)
                    my_menu.add_cascade(label='  More  ', menu=user_menu)
                    user_menu.add_command(label='               View All Users              ', font=("Times New Roman", 16), command=view_all_users)

                    after_login_frame.place(relx=0.5, rely=0.5, anchor='center')
                home_page()
        # Submit button
        submit_button = CTkButton(frame1, text="Submit", font=("Times New Roman", 20), fg_color=COLOR, command=after_login)
        submit_button.place(relx=0.5, rely=0.7, anchor='center')

        # Account Form
        def create_an_account():
            frame1.destroy()
            name_frame = CTkFrame(win, width=500, height=500, fg_color='#D6D7E8').place(relx=0.5, rely=0.5, anchor='center')

            # create an account label
            CTkLabel(name_frame, text='Create An Account', text_color=COLOR, font=("Times New Roman", 40), fg_color='#D6D7E8').place(relx=0.5, rely=0.25, anchor='center')

            
            # first name text input
            first_name_entry = CTkEntry(name_frame, width=400, font=("Times New Roman", 20), placeholder_text="First Name")
            first_name_entry.place(relx=0.5, rely=0.36, anchor='center')

            # last name text input
            last_name_entry = CTkEntry(name_frame, width=400, font=("Times New Roman", 20), placeholder_text="Last Name")
            last_name_entry.place(relx=0.5, rely=0.46, anchor='center')


            # username text input
            username_entry = CTkEntry(name_frame, width=400, font=("Times New Roman", 20), placeholder_text="Username")
            username_entry.place(relx=0.5, rely=0.56, anchor='center')


            # Password text input
            password_entry = CTkEntry(name_frame, width=400, font=("Times New Roman", 20), placeholder_text="Password")
            password_entry.place(relx=0.5, rely=0.66, anchor='center')


            def new_account():
                if first_name_entry.get() == "" or first_name_entry.get().isnumeric() == True:
                    messagebox.showerror("Error", "Please Enter Valid First Name")
                    first_name_entry.delete(0, 'end')

                elif last_name_entry.get() == "" or last_name_entry.get().isnumeric() == True:
                    messagebox.showerror("Error", "Please Enter Valid Last Name")
                    last_name_entry.delete(0, 'end')

                elif username_entry.get() == "":
                    messagebox.showerror("Error", "Please Enter Username")
                    username_entry.delete(0, 'end')

                elif password_entry.get() == "":
                    messagebox.showerror("Error", "Please Enter Password")
                    password_entry.delete(0, 'end')

                else:
                    conn = sqlite3.connect(resource_path("second_child.db"))
                    cr = conn.cursor()
                    try:
                        cr.execute("CREATE TABLE IF NOT EXISTS new_account (first_name TEXT, last_name TEXT, username TEXT PRIMARY KEY, password TEXT)")
                        cr.execute("INSERT INTO new_account (first_name, last_name, username, password) values(?,?,?,?)", (capitalize_input(first_name_entry.get()), capitalize_input(last_name_entry.get()), username_entry.get(), password_entry.get()))
                        messagebox.showinfo("Information", "User Is Added!")
                        first_page()
                    except:
                        messagebox.showerror("Error", "Username Already Exists!")
                        username_entry.delete(0, 'end')
                    conn.commit()
                    conn.close()
                    


            # Submit Button
            submit_button = CTkButton(name_frame, text="Submit", font=("Times New Roman", 20), fg_color=COLOR, command=new_account)
            submit_button.place(relx=0.45, rely=0.76, anchor='center')

            # login page Button
            go_to_login_button = CTkButton(name_frame, text="Go To Login", font=("Times New Roman", 20), fg_color=COLOR, command=first_page)
            go_to_login_button.place(relx=0.55, rely=0.76, anchor='center')

        # Create an account button
        create_accout_button = CTkButton(frame1, text="Create an Account", width=400, font=("Times New Roman", 20), fg_color=COLOR, command=create_an_account)
        create_accout_button.place(relx=0.5, rely=0.9, anchor='center')


    inner_first_page()
    
    first_frame.place(relx=0.5, rely=0.5, anchor='center')

first_page()

win.mainloop()