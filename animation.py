import subprocess
exe_path = "foundation.exe"
proc = subprocess.Popen([exe_path])
proc.wait()






from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
import os
import time 
from google import genai
import google.generativeai as genai
genai.configure(api_key="AIzaSyCiK7HKBg8TzWUIg-Ueg_DDP_qcgifQMTU")
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.configure(fg_color="#000000") # Pitch black background
app.resizable(False, False)
app.wm_overrideredirect(True)
app.attributes("-topmost", True)  # come on top of apps

# Center the window
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 900
window_height = 600
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{x}+{y}")


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


def page2():
    app.configure(fg_color="#000000")

    # Destroy old widgets
    for widget in app.winfo_children():
        widget.destroy()
    show_loading_screen("walk.gif", size=(400, 600), duration=4000)
    
    app.after(4000, build_form)


    #Frame setup
def build_form():

    form_frame = ctk.CTkFrame(
        app,
        fg_color="#24272b",  # Dark gray
        corner_radius=15,
        width=300,
        height=500,
        border_color="#ff7b00",
        border_width=2
    )
    form_frame.place(x=50, y=50) # change frame postion
    form_frame.pack_propagate(False)
   
    def maybe_show_loading_screen(gif_name, size=(300, 300), duration=None):
        if duration is None or duration == 0:
            # Show loading screen forever
            show_loading_screen(gif_name, size=size, duration=99999999)
        else:
            show_loading_screen(gif_name, size=size, duration=duration)

    maybe_show_loading_screen("sun.gif", size=(600, 600), duration=None)
    # Move the loading gif 
    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkLabel) and widget.cget("image"):
            widget.place_configure(relx=0.4, rely=0.0, anchor="nw")
        img2 = Image.open("switch.png")
    ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(25, 25))
    door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
    door_label.place(relx=0.05, rely=0.95
                     , anchor="ne")                                       #exit image to close the app
    door_label.bind("<Button-1>", lambda event: close_app())
    def close_app(event=None):
        app.destroy()
        
    title_label = ctk.CTkLabel( # label
        form_frame,
        text="Statistics Form",
        font=("Segoe UI", 20, "bold"),
        text_color="#C0C1C7"
    )
    title_label.pack(pady=(20, 10))

    entry_kwargs = { # button styling
        "width": 200,
        "font": ("Segoe UI", 14),
        "text_color": "#cfd3db",
        "border_color": "#2b2d32"
    }

    # button and entries 
    weight_entry = ctk.CTkEntry(form_frame, placeholder_text="Weight in kg", fg_color="#2b2b2b" ,**entry_kwargs)
    weight_entry.pack(pady=10)

    height_entry = ctk.CTkEntry(form_frame, placeholder_text="Height in cm",fg_color="#2b2b2b", **entry_kwargs)
    height_entry.pack(pady=10)

    age_entry = ctk.CTkEntry(form_frame, placeholder_text="Age in years",fg_color="#2b2b2b", **entry_kwargs)
    age_entry.pack(pady=10)

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

    ctk.CTkButton(                              #calculate button
        form_frame,
        text="Calculate",
        corner_radius=30,
        fg_color="#48965d",
        hover_color="#00AAF8",
        font=("Segoe UI", 13),
        command=lambda: handler2(weight_entry, height_entry, age_entry, gender_combo, goal_combo, activity_combo, gym_access_combo)
    ).pack(pady=20)


# hander starts here 


def handler2(weight_entry, height_entry, age_entry, gender_combo, goal_combo, activity_combo, gym_access_combo):
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        age = int(age_entry.get())
        gender = gender_combo.get().lower()
        goal = goal_combo.get()
        activity = activity_combo.get()
        gym_access = gym_access_combo.get()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight, height, and age.")
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
        "Age": age_entry.get(),
        "Gender": gender_combo.get(),
        "Goal": goal_combo.get(),
        "Activity Level": activity_combo.get(),
        "Gym Access": gym_access_combo.get()
    }

    prompt = build_prompt(user)

    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)
        print("✅ Gemini Response:\n")
        print(response.text)
        page3(response, send)  # Pass send to page3
    except Exception as e:
        print(f"❌ Error generating content: {e}")

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
def page3(response=None, send=None):
    for widget in app.winfo_children():
        widget.destroy()
    build_textbox(response, send)

def build_textbox(response, send=None):
    # Show loading animation before displaying the textbox
    show_loading_screen("load.gif", size=(50, 50), duration=1500)
    app.configure(fg_color="#303030")

    def show_textbox():
        # Insert nutrition info from send if available
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
                import webbrowser
                app.attributes("-topmost", False) 
                webbrowser.open("https://criticalthreads.netlify.app/")  # Open URL in default browser
                time.sleep(2) 
                app.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open cookbook.exe: {e}")

        btn4 = ctk.CTkButton(
            master=app, 
            text="Get Cookbooks", 
            corner_radius=30, 
            fg_color="#00AAF8", 
            hover_color="#08962C", 
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

        img2 = Image.open("switch.png")
        ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
        door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
        door_label.place(relx=0.1, rely=0.85, anchor="ne")  # exit image to close the app
        door_label.bind("<Button-1>", lambda event: close_app())

    def close_app(event=None):
        app.destroy()

    app.after(1500, show_textbox)

btn = ctk.CTkButton(master=app, text="Go to Page 2", corner_radius=30, fg_color="#5BA15F", hover_color="#00AAF8", font=("Segoe UI", 13,))
btn.configure(command=page2) 
btn.place(relx=0.45, rely=0.5, anchor="center")


img2 = Image.open("switch.png")
ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
door_label.place(relx=0.1, rely=0.85, anchor="ne")                                       #exit image to close the app
door_label.bind("<Button-1>", lambda event: close_app())

def close_app(event=None):
    app.destroy()



app.mainloop()