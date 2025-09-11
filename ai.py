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

cals = 2000
protien = 150
carbs = 250
fat = 70

def page3(cals, protien, carbs, fat):
    for widget in app.winfo_children():
        widget.destroy()
    text = ctk.CTkTextbox(
        master=app,
        width=400,
        height=520,
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
    text.place(relx=0.7, rely=0.5, anchor="center")
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
    icon  = ctk.CTkTextbox(
        master=app,
        width=280,
        height=200,
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
    text.insert("end", f"Calories: {cals} kcal\nProtein: {protien} g\nCarbs: {carbs} g\nFat: {fat} g")

    # Add hover effect for border color
    def on_enter(event):
        text.configure(border_color="#00AAF8") 

    def on_leave(event):
        text.configure(border_color="#F1ED00")  

    text.bind("<Enter>", on_enter)
    text.bind("<Leave>", on_leave)
    text.bind("<Enter>", on_enter)
    text.bind("<Leave>", on_leave)
    text.insert("end", text_content)
    text.configure(state="disabled")
    icon.configure(state="disabled")

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
btn.configure(command=lambda: page3(cals, protien, carbs, fat))
btn.place(relx=0.45, rely=0.5, anchor="center")


app.mainloop()