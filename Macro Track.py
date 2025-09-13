import subprocess
import ctypes

try:
    import customtkinter
    import google.generativeai
    import PIL

    import cv2
    ctypes.windll.user32.MessageBoxW(
        0,
        "Modules Installed!",
        "Requirements",
        0x40 | 0x1000  
    )

except ImportError as e:
    ctypes.windll.user32.MessageBoxW(
         0, "Failed to install modules!"
         , "Requiremnts"
         , 0x40 | 0x1000 
         )
    exe_path = "foundation.exe"
    proc = subprocess.Popen([exe_path])
    proc.wait()



# ========== GUI Application Code ========== 



import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import random
import tkinter as tk
from PIL import Image, ImageTk
import cv2
from google import genai
import google.generativeai as genai
import time
genai.configure(api_key="Enter your API key here")
messagebox.showinfo("Info", "This app uses Gemini API by Google.")
conn = sqlite3.connect('keys.db')

c = conn.cursor()


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.resizable(False, False)
app.wm_overrideredirect(True)                            #this the window creation process
screen_width = app.winfo_screenwidth()                   ######
screen_height = app.winfo_screenheight()
app.attributes("-topmost", True) 
window_width = 900
window_height = 600
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{x}+{y}")
app.configure(fg_color="#000000") 



# Load video using OpenCV
cap = cv2.VideoCapture("sn.mp4")  

# make vido as background
label = tk.Label(app)
label.place(x=0, y=0, relwidth=1, relheight=1)

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (900, 600))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        label.configure(image=img)
        label.image = img
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) #loop video
    label.after(30, update_frame)  #frame adjustment 

update_frame()


def show_loading_screen(gif_name, size=(50, 50), duration=2000):
    """
    Shows a loading screen with the specified gif
    Args:
        gif_name (str): Name of the gif file (must be in same directory)
        size (tuple): Size to display the gif (width, height)
        duration (int): How long to show loading screen in milliseconds
    """
    try:
        loading_gif = Image.open(gif_name)
        frames = []
        
        try:
            while True:
                frame = loading_gif.copy().resize(size, Image.LANCZOS)
                frames.append(ImageTk.PhotoImage(frame))
                loading_gif.seek(loading_gif.tell() + 1)
        except EOFError:
            pass

        loading_label = ctk.CTkLabel(app, text="")
        loading_label.place(relx=0.46, rely=0.49, anchor="center")

        def animate(idx=0):
            if not hasattr(animate, "running"):
                animate.running = True
            loading_label.configure(image=frames[idx])
            idx = (idx + 1) % len(frames)
            if animate.running:
                app.after(100, animate, idx)
            else:
                loading_label.destroy()

        animate()
        app.after(duration, lambda: setattr(animate, "running", False))
        
    except FileNotFoundError:
        print(f"Error: Could not find gif file '{gif_name}'")
        return




def handler():
    print(f"Button clicked with entry value: {entry.get()}")
    num = entry.get()
    if num.strip() == "":
        messagebox.showerror("Error", "Username cannot be empty.")
        return
    if not num[-4:] == ".com":
        messagebox.showerror("Error", "Username must end with .com")
    else:
        c.execute("SELECT COUNT(*) FROM keys WHERE username = ?", (num,))
    result = c.fetchone()
    if result[0] > 0:                                                   #this is used to validate username
        messagebox.showinfo("Success", "Username is valid.")
        load = page2()
    else:
        messagebox.showerror("Error", "Username is worng or does not exist.")

                


img = Image.open("icon.png") 
ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(25, 25))

entry = ctk.CTkEntry(app, width=200,  placeholder_text="Enter Username here", font=("Segoe UI", 14), text_color= "#AAAAAA", border_color="#5BA15F")  # username entry


entry.place(relx=0.49, rely=0.4, anchor="center")
btn = ctk.CTkButton(master=app, text="Submit", 
                    corner_radius=30, 
                    fg_color="#5BA15F", 
                    image=ctk_img, hover_color="#7FB77E", 
                    command=handler,
                    font=("Segoe UI", 13, "bold") # submit button 
)
btn.place(relx=0.49, rely=0.48, anchor="center")
app.bind('<Return>', lambda event: handler())      #button bind with enter key


def create_account():
    new_window = ctk.CTkToplevel(app)
    new_window.geometry("400x300")
    new_window.title("Create Account")
    new_window.resizable(False, False)
    new_window.attributes("-topmost", True) 
    entry_username = ctk.CTkEntry(new_window, width=200, placeholder_text="Enter new username")         #seperate window for creating account
    entry_username.pack(pady=20)
    def on_key_release(event):
        current_text = entry_username.get()
        char = 5
        if not current_text.isalpha():
            entry_username.delete(len(current_text) - 1, tk.END)
            messagebox.showerror("Input Error", "Please enter only alphabetic characters.")
        if len(current_text) > char:
            entry_username.delete(char, tk.END)
    entry_username.bind("<KeyRelease>", on_key_release)

    btn0 = ctk.CTkButton(
        master=new_window,
        text="CREATE",
        corner_radius=30,
        fg_color="#5BA15F",
        hover_color="#000000",#
        font=("Segoe UI", 13, "bold"),
        command=lambda: create(entry_username)
    )
    btn0.place(relx=0.5, rely=0.3, anchor="center")
    btn0.pack(pady=20)
    new_window.bind('<Return>', lambda event: create(entry_username   ))
    

def create(entry_username):

    
    username = entry_username.get()
    if username.strip() == "":
        messagebox.showerror("Error", "Username cannot be empty.")
        return
    print(f"create account clicked: {username}")
    c.execute("SELECT COUNT(*) FROM keys WHERE username = ?", (username,))
    result = c.fetchone()
    if result[0] > 0:
        messagebox.showerror("Error", "Username already exists.")        # subroutine to create account
    else:
        num = random.randint(1, 10000)
        number = str(num)
        com = ".com"
        key = username + str(number) + com
        
        with open('key.txt', 'a') as f:    
            f.write(key + '\n')
        try:
            c.execute("INSERT INTO keys (username) VALUES (?)", (key,))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully. Login using the key: " + key)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")




btn2= ctk.CTkButton(master=app, text="Create account", corner_radius=30, fg_color="#5BA15F",hover_color="#88C089", font=("Segoe UI", 13, "bold"))  
btn2.pack(pady=20)
btn2.place(relx=0.49, rely=0.55, anchor="center")         #button to open the window and create account
if btn2:
    btn2.configure(command=create_account)



def page2():
    app.configure(fg_color="#000000")

    # Destroy old widgets
    for widget in app.winfo_children():
        widget.destroy()
    show_loading_screen("load.gif", size=(50, 50), duration=4000)
    
    app.after(4000, build_form)



def build_form():
    form_frame = ctk.CTkFrame(
        app,
        fg_color="#24272b",  # Dark gray
        corner_radius=15,
        width=350,
        height=500,
        border_color="#ff7b00",
        border_width=2
    )
    form_frame.place(x=50, y=50)  # change frame position
    form_frame.pack_propagate(False)


    def maybe_show_loading_screen(gif_name, size=(300, 300), duration=None):
        if duration is None or duration == 0:
            show_loading_screen(gif_name, size=size, duration=99999999)
        else:
            show_loading_screen(gif_name, size=size, duration=duration)

    maybe_show_loading_screen("sun.gif", size=(600, 600), duration=None)

    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and widget.cget("image"):
            widget.place_configure(relx=0.45, rely=0.0, anchor="nw")


    img2 = Image.open("switch.png")
    ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
    door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
    door_label.place(relx=0.95, rely=0.08, anchor="ne")  # exit image page 2


    def close_app(event=None):
        messagebox.YESNO = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if messagebox.YESNO == True:
            app.destroy()
        else:
            pass
    door_label.bind("<Button-1>", close_app)

    title_label = ctk.CTkLabel(
        form_frame,
        text="Statistics Form",
        font=("Segoe UI", 20, "bold"),
        text_color="#C0C1C7"
    )
    title_label.pack(pady=(20, 10))




#slider labels start here


    def update_height_label(value):
        height_label.configure(text=f"Height (cm): {int(value)}")

    def update_weight_label(value):
        weight_label.configure(text=f"Weight (kg): {int(value)}")

    def update_age_label(value):
        age_label.configure(text=f"Age: {int(value)}")


#height slider start here

    height_label = ctk.CTkLabel(form_frame, text="Height (cm): 150", font=("Segoe UI", 16), text_color="#FFFFFF")
    height_label.pack(pady=(10, 5))
    height_entry = ctk.CTkSlider(
        form_frame, from_=150, to=200, width=200, height=20, fg_color="#cfd3db",
        button_color="#cfd3db", progress_color="#ff7b00", button_hover_color="#ff7b00",
        command=update_height_label
    )
    height_entry.pack(pady=(0, 10))


#weight slider start here 


    weight_label = ctk.CTkLabel(form_frame, text="Weight (kg): 35", font=("Segoe UI", 16), text_color="#FFFFFF")
    weight_label.pack(pady=(10, 5))
    weight_entry = ctk.CTkSlider(
        form_frame, from_=35, to=200, width=200, height=20, fg_color="#cfd3db",
        button_color="#cfd3db", progress_color="#ff7b00", button_hover_color="#ff7b00",
        command=update_weight_label
    )
    weight_entry.pack(pady=(0, 10))


#age slider start here
    age_label = ctk.CTkLabel(form_frame, text="Age: 16", font=("Segoe UI", 16), text_color="#FFFFFF")
    age_label.pack(pady=(10, 5))
    slid = ctk.CTkSlider(
        form_frame, from_=16, to=90, width=200, height=20, fg_color="#cfd3db",
        button_color="#cfd3db", progress_color="#ff7b00", button_hover_color="#ff7b00",
        command=update_age_label
    )
    slid.pack(pady=(0, 10))


 # combo box and button start here



    gender_combo = ctk.CTkComboBox(
        form_frame,
        values=["male", "female"],
        width=200,
        border_color="#2b2d32",
        font=("Segoe UI", 14),
        text_color="#AAAAAA",
        fg_color="#2b2b2b",
        dropdown_font=("Segoe UI", 14),
        dropdown_hover_color="#252926",
        state="readonly",
        corner_radius=10
    )
    gender_combo.set("Select Gender")
    gender_combo.pack(pady=10)


    goal_combo = ctk.CTkComboBox(
        form_frame,
        values=["Weight Loss", "Muscle Gain", "Maintenance"],
        width=200,
        border_color="#2b2d32",
        font=("Segoe UI", 14),
        text_color="#AAAAAA",
        fg_color="#2b2b2b",
        dropdown_font=("Segoe UI", 14),
        dropdown_hover_color="#252926",
        state="readonly",
        corner_radius=10
    )
    goal_combo.set("Select Goal")
    goal_combo.pack(pady=10)


    activity_combo = ctk.CTkComboBox(
        form_frame,
        values=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
        width=200,
        border_color="#2b2d32",
        font=("Segoe UI", 14),
        text_color="#AAAAAA",
        fg_color="#2b2b2b",
        dropdown_font=("Segoe UI", 14),
        dropdown_hover_color="#252926",
        state="readonly",
        corner_radius=10
    )
    activity_combo.set("Select Activity Level")
    activity_combo.pack(pady=10)


    gym_access_combo = ctk.CTkComboBox(
        form_frame,
        values=["Yes", "No"],
        width=200,
        border_color="#2b2d32",
        font=("Segoe UI", 14),
        text_color="#AAAAAA",
        fg_color="#2b2b2b",
        dropdown_font=("Segoe UI", 14),
        dropdown_hover_color="#252926",
        state="readonly",
        corner_radius=10
    )
    gym_access_combo.set("Gym Access")
    gym_access_combo.pack(pady=10)



    btn = ctk.CTkButton(
        master=app,
        text="Calculate",
        corner_radius=30,
        fg_color="#48965d",
        hover_color="#00AAF8",
        font=("Segoe UI", 13),
        command=lambda: handler2(weight_entry, height_entry, slid, gender_combo, goal_combo, activity_combo, gym_access_combo)
    )
    btn.place(x=640, y=510)


import threading

def handler2(weight_entry, height_entry, slid, gender_combo, goal_combo, activity_combo, gym_access_combo):
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        age = int(slid.get())
        gender = gender_combo.get().lower()
        goal = goal_combo.get()
        activity = activity_combo.get()
        gym_access = gym_access_combo.get()
    except Exception:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight, height, and age.")
        return



    # Check for empty 
    if gender_combo.get() == "Select Gender" or not gender:
        messagebox.showerror("Invalid", "Please select a gender.")
        return
    if goal_combo.get() == "Select Goal" or not goal:
        messagebox.showerror("Invalid", "Please select a goal.")
        return
    if activity_combo.get() == "Select Activity Level" or not activity:
        messagebox.showerror("Invalid", "Please select an activity level.")
        return
    if gym_access_combo.get() == "Gym Access" or not gym_access:
        messagebox.showerror("Invalid", "Please select gym access.")
        return

    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        messagebox.showerror("Invalid", "Gender input. Please select 'male' or 'female'.")
        return
    cal = bmr*1.2
    protein = round(weight * 2) 
    fat = round(weight * 0.9) 
    protein_cal = protein * 4
    fat_cal = fat * 9
    carbs = round((cal - (protein_cal + fat_cal)) / 4) 

    send = {
        "calories": round(cal),
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }

    user = {
        "Weight": weight_entry.get(),
        "Height": height_entry.get(),
        "Age": slid.get(),
        "Gender": gender_combo.get(),
        "Goal": goal_combo.get(),
        "Activity Level": activity_combo.get(),
        "Gym Access": gym_access_combo.get()
    }

    prompt = build_prompt(user)


    for widget in app.winfo_children():
        widget.destroy()
    show_loading_screen("load.gif", size=(50, 50), duration=2800)
     


    def gemini_thread():
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content(prompt)
            app.after(1, lambda: page3(response, send))
        except Exception as e:
            app.after(1, lambda: messagebox.showerror("Error", f"Error generating content: {e}"))
            app.after(1, lambda: page3(None, send))

    threading.Thread(target=gemini_thread, daemon=True).start()

def build_prompt(data):
    return f"""
You are a professional fitness coach. Based on the following user data, generate a **simple and clean fitness program** to help them achieve their goal. Use clear section headers and short lists.

### User Info:
- Age: {data["Age"]}
- Gender: {data["Gender"]}
- Height: {data["Height"]} cm
- Weight: {data["Weight"]} kg
- Activity Level: {data["Activity Level"]}
- Goal: {data["Goal"]}
- Gym Access: {data["Gym Access"]}

### Program Format (Keep it short and clean):
1. **Workout Split**: Which days, and what types of workouts (e.g., Upper/Lower/Full Body/Cardio)?
2. **Session Example**: One sample day with key exercises, sets, and reps.
3. **Mobility & Recovery**: Short suggestions (e.g., foam rolling, light stretching).
4. **Progression Advice**: How to increase intensity over time.
5. **Extra Tips**: Short list of useful tips (1-3 lines max).
6: response in the format of a markdown text exactly like this using "\n" to separate lines:
        "**"✅ Response:\n\n"
        "**1. Workout Split:**\n"
        "* Monday: Upper Body Strength\n"
        "* Tuesday: Lower Body Strength\n"
        "* Wednesday: Cardio & Core\n"
        "* Thursday: Rest or Active Recovery (light walk)\n"
        "* Friday: Full Body Circuit\n"
        "* Saturday: Rest or Active Recovery\n"
        "* Sunday: Rest\n\n"
        "**2. Session Example (Monday - Upper Body):**\n"
        "* **Bench Press:** 3 sets of 8-12 reps\n"
        "* **Overhead Press:** 3 sets of 8-12 reps\n"
        "* **Bent-Over Rows:** 3 sets of 8-12 reps\n"
        "* **Bicep Curls:** 3 sets of 10-15 reps\n"
        "* **Triceps Extensions:** 3 sets of 10-15 reps\n\n"
        "**3. Mobility & Recovery:**\n"
        "* Foam roll chest, back, and shoulders after each workout\n"
        "* Perform light stretching focusing on major muscle groups post-workout.\n\n"
        "**4. Progression Advice:**\n"
        "* Gradually increase weight or resistance as you get stronger.\n"
        "* Increase reps or sets when the weight feels easy for 2-3 weeks.\n"
        "* Consider adding more challenging variations of exercises as you progress.\n\n"
        "**5. Extra Tips:**\n"
        "* Prioritize sleep (7-9 hours) and hydration\n"
        "* Focus on a balanced calorie deficit diet (consult a nutritionist if needed).\n"
        "* Listen to your body and take rest days when necessary.\n"
    )


Make the response clear, concise, and suitable for putting inside a GUI textbox.
"""





def page3(response=None,send=None):
    for widget in app.winfo_children():
        widget.destroy()
    app.configure(fg_color="#504A4A")


    img3 = Image.open("back.png")
    ctk_img3 = ctk.CTkImage(light_image=img3, dark_image=img3, size=(25, 25))
    back_label = ctk.CTkLabel(master=app, image=ctk_img3, text="", cursor="hand2") #back image page 3
    back_label.place(relx=0.07, rely=0.02, anchor="ne")
    back_label.bind("<Button-1>", lambda event: page2())

    
    def show_textbox():

        if send:
            cals = send.get("calories", "")
            protein = send.get("protein", "")
            carbs = send.get("carbs", "")
            fat = send.get("fat", "")
        else:
            cals = protein = carbs = fat = ""

        icon = ctk.CTkTextbox(
            master=app,
            width=280,
            height=180,
            corner_radius=10,
            fg_color="#504A4A",
            text_color="#FFFFFF",
            font=("Segoe UI", 14),
            border_color="#F1C500",
            border_width=2,
            scrollbar_button_color="#F1C500",
            activate_scrollbars=True,
            scrollbar_button_hover_color="#FFFFFF",
        )
        icon.place(relx=0.2, rely=0.3, anchor="center")
        icon.insert("1.0", "✅ Daily Nutrition Info:\n\n")
        icon.insert("end", f"Calories: {cals} kcal\nProtein: {protein} g\nCarbs: {carbs} g\nFat: {fat} g\n")
        icon.insert("end", "Daily 10,000 steps\n\n")
        icon.configure(state="disabled")

        def hand():
            try:
                messagebox.showinfo("Cookbook", "You are leaving the app.")
                time.sleep(1) 
                import webbrowser
                app.attributes("-topmost", False) 
                webbrowser.open("https://criticalthreads.netlify.app/")  # Open URL in default browser
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open cookbook.exe: {e}")

        btn4 = ctk.CTkButton(
            master=app, 
            text="Get Cookbooks", 
            corner_radius=30, 
            fg_color="#08962C", 
            hover_color="#00AAF8", 
            font=("Segoe UI", 13,),
            command=hand
        )
        btn4.place(relx=0.2, rely=0.55, anchor="center")



        text = ctk.CTkTextbox(
            master=app,
            width=425,
            height=520,
            corner_radius=10,
            fg_color="#504A4A",
            text_color="#FFFFFF",
            font=("Segoe UI", 14),
            border_color="#F1ED00",
            border_width=2,
            scrollbar_button_color="#F1C500",
            activate_scrollbars=True,
            scrollbar_button_hover_color="#FFFFFF"
        )
        text.place(relx=0.7, rely=0.5, anchor="center")
        text_content = response.text if response else ""
        text.insert("end", text_content)
        text.configure(state="disabled")

        def on_enter(event):
            text.configure(border_color="#00AAF8")
        def on_leave(event):
            text.configure(border_color="#F1ED00")

        text.bind("<Enter>", on_enter)
        text.bind("<Leave>", on_leave)

        def off(event):
            icon.configure(border_color="#F1ED00")
        def on(event):
            icon.configure(border_color="#00AAF8")
        icon.bind("<Enter>", on)
        icon.bind("<Leave>", off)
        with open ('program.txt', 'w') as f:    
            f.write(text_content)

        img2 = Image.open("switch.png")
        ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
        door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
        door_label.place(relx=0.1, rely=0.85, anchor="ne")  # exit image for the page 3
        door_label.bind("<Button-1>", lambda event: close_app())

    def close_app(event=None):
        app.destroy()

    app.after(100, show_textbox)

img2 = Image.open("switch.png")
ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
door_label.place(relx=0.1, rely=0.85, anchor="ne")                                       #exit image for the login
door_label.bind("<Button-1>", lambda event: close_app())

def close_app(event=None):
    app.destroy()


app.mainloop()
cap.release()