from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
import os
import time 


app = ctk.CTk()
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
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



def page2():
    app.configure(fg_color="#000000")

    # Destroy old widgets
    for widget in app.winfo_children():
        widget.destroy()
        build_form()


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
    page3(round(cal), protein, carbs, fat) 




































def page3(cals, protien, carbs, fat):
    for widget in app.winfo_children():
        widget.destroy()
    icon  = ctk.CTkTextbox(
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
    text = ctk.CTkTextbox(
        master=app,
        width=400,
        height=450,
        corner_radius=10,
        fg_color="#504A4A",
        text_color="#FFFFFF",
        font=("Segoe UI", 14),
        border_color="#F1ED00",
        border_width=2,
        scrollbar_button_color="#F1C500",
        activate_scrollbars=True,
        scrollbar_button_hover_color="#FFFFFF",
    )

    btn4 = ctk.CTkButton(master=app, text="Get Cookbooks", 
                         corner_radius=30, 
                         fg_color="#00AAF8", 
                         hover_color="#08962C", 
                         font=("Segoe UI", 13,),
                         command=lambda: hand()
                         )
    btn4.place(relx=0.2, rely=0.55, anchor="center")
    def hand():
        try: 
            import webbrowser
            app.attributes("-topmost", False) 
            webbrowser.open("https://criticalthreads.netlify.app/")  # Open URL in default browser
            time.sleep(2) 
            app.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open cookbook.exe: {e}")

    icon.insert("1.0", "✅ Daily Nutrition Info:\n\n")
    icon.insert("2.0", f"Calories: {cals} kcal\nProtein: {protien} g\nCarbs: {carbs} g\nFat: {fat} g")
    icon.insert("3.0", "Daily 10,000 steps\n\n")
    icon.configure(state="disabled")
    icon.place(relx=0.2, rely=0.3, anchor="center")

    # Insert workout plan into text textbox
    text_content = (
        "✅ Response:\n\n"
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
    text.insert("1.0", text_content)
    text.configure(state="disabled")
    text.place(relx=0.7, rely=0.5, anchor="center")


    
    

    # Add hover effect for border color
    def on_enter(event):
        text.configure(border_color="#00AAF8") 

    def on_leave(event):
        text.configure(border_color="#F1ED00")  

    text.bind("<Enter>", on_enter)
    text.bind("<Leave>", on_leave)



    slid = ctk.CTkSlider(app, from_=16, to=90, width=200, height=20, fg_color="#ECC618", button_color="#5BA15F", progress_color="#00AAF8",)
    if slid.get == 70 >= 90:
        messagebox.showinfo("old", "too old to use this go hosipital")
    def slide(value):
        label.configure(text=f"Age: {int(value)}")
    label = ctk.CTkLabel(app, text="Age: 16", font=("Segoe UI", 16), text_color="#FFFFFF")
    label.place(relx=0.3, rely=0.85, anchor="center")
    slid.configure(command=slide)
    slid.place(relx=0.3, rely=0.9, anchor="center")

    height = ctk.CTkSlider(app, from_=150, to=200, width=200, height=20, fg_color="#ECC618", button_color="#5BA15F", progress_color="#00AAF8",)
    if height.get == 150 >= 200:
        messagebox.showinfo("tall", "too tall to use this go hosipital")
    def slide1(value):
        label1.configure(text=f"height: {int(value)} in cm")
    label1 = ctk.CTkLabel(app, text="Height", font=("Segoe UI", 16), text_color="#FFFFFF")
    label1.place(relx=0.3, rely=0.6, anchor="center")
    height.configure(command=slide1)
    height.place(relx=0.3, rely=0.65, anchor="center")

    weight = ctk.CTkSlider(app, from_=35, to=200, width=200, height=20, fg_color="#ECC618", button_color="#5BA15F", progress_color="#00AAF8",)
    if weight.get == 35 >= 200:
        messagebox.showinfo("light", "too light to use this go hosipital")
    def slide2(value):
        label2.configure(text=f"Weight: {int(value)} in kg")
    label2 = ctk.CTkLabel(app, text="Weight", font=("Segoe UI", 16), text_color="#FFFFFF")
    label2.place(relx=0.3, rely=0.75, anchor="center")
    weight.configure(command=slide2)
    weight.place(relx=0.3, rely=0.8, anchor="center")
    




btn = ctk.CTkButton(master=app, text="Go to Page 2", corner_radius=30, fg_color="#5BA15F", hover_color="#00AAF8", font=("Segoe UI", 13,))
btn.configure(command=lambda:page2())
btn.place(relx=0.45, rely=0.5, anchor="center")



app.mainloop()