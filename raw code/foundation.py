from tkinter import messagebox
import tkinter as tk
import subprocess
import tempfile
import customtkinter as ctk
from PIL import Image
from PIL import Image, ImageTk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("400x400")
app.resizable(False, False)
app.wm_overrideredirect(True)
app.attributes("-topmost", True)#

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 400
window_height = 400
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
app.geometry(f"{window_width}x{window_height}+{x}+{y}")

def setup_engine():
    messagebox.showinfo("info", "Restart Vs Code after installation")
    powershell_script = r'''
$host.UI.RawUI.WindowTitle = "GRAPE Setup Engine"
Clear-Host

# ASCII Art
Write-Host ''
Write-Host '   _____            _                   ______    _____                      '
Write-Host '  / ____|          | |                 |  ____|  |  __ \                     '
Write-Host ' | (___   ___  _ __| |_ _   _ _ __ ___ | |__     | |__) |   ___   _ __ ___   '
Write-Host '  \___ \ / _ \| ''__| __| | | | ''__/ _ \|  __|    |  _  /   / _ \ | ''_ ` _ \  '
Write-Host '  ____) | (_) | |  | |_| |_| | | |  __/| |____   | | \ \  | (_) || | | | | | '
Write-Host ' |_____/ \___/|_|   \__|\__,_|_|  \___||______|  |_|  \_\  \___/ |_| |_| |_| '
Write-Host ''
Write-Host '   _____                      _                                            '
Write-Host '  | ____|_  ___ __   ___ _ __| |_ ___  ___                                '
Write-Host '  |  _| \ \/ / ''_ \ / _ \ ''__| __/ _ \/ __|                               '
Write-Host '  | |___ >  <| |_) |  __/ |  | ||  __/\__ \                               '
Write-Host '  |_____/_/\_\ .__/ \___|_|   \__\___||___/                               '
Write-Host '             |_|                                                         '
Write-Host ''

# "Developed by GRAPE"
Write-Host -NoNewline 'Developed by '
$colors = @('Magenta','DarkMagenta','Cyan','DarkCyan','Yellow','DarkYellow')
$grape = 'UMAR'.ToCharArray()
for ($i = 0; $i -lt $grape.Length; $i++) {
    $color = $colors[$i % $colors.Length]
    Write-Host $grape[$i] -ForegroundColor $color -NoNewline
}
Write-Host "`n"

# animation from github.com/
$spinner = @('/','-','\','|')
for ($i = 0; $i -lt 10; $i++) {
    foreach ($s in $spinner) {
        Write-Host "`rInstalling [$s]" -NoNewline
        Start-Sleep -Milliseconds 200
    }
}
Write-Host "`rInstalling [OK]"

# installer
$pipInstalls = @(
    @{ label = 'Pyhton version'; command = 'python -m pip install --upgrade pip' },
    @{ label = 'customtkinter'; command = 'pip install --upgrade customtkinter' },
    @{ label = 'AI'; command = 'pip install --upgrade google-generativeai' },
    @{ label = 'pillow'; command = 'pip install --upgrade pillow' },
    @{ label = 'requests'; command = 'pip install requests' },
    @{ label = 'OpenCV'; command = 'pip install --upgrade opencv-python' }
    
)
foreach ($item in $pipInstalls) {
    Write-Host "Installing $($item.label)..."
    cmd /c $item.command | Out-Null
}

# Success banner
Write-Host ''
Write-Host '+------------------------------+' -ForegroundColor Green
Write-Host '|  [OK] All packages installed!  |' -ForegroundColor Green
Write-Host '+------------------------------+' -ForegroundColor Green

# Auto-close after 4 seconds
Write-Host ''
Write-Host "Closing in 4 seconds..."
Start-Sleep -Seconds 4
exit
'''

    # Write to a temporary .ps1 file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ps1", mode="w", encoding="utf-8") as temp_script:
        temp_script.write(powershell_script)
        temp_path = temp_script.name


    subprocess.run([
        "powershell",
        "-Command",
        f'Start-Process powershell -ArgumentList \'-ExecutionPolicy Bypass -File "{temp_path}"\''
    ])

text = ctk.CTkTextbox(
        master=app,
        width=200,
        height=100,
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
text.place(relx=0.5, rely=0.4, anchor="center")
text.insert("2.0", "To Use This App\n")
text.insert("1.0", "Install Requirements \n")
text.insert("0.0", "You Must\n")
text.configure(state="disabled")



btn = ctk.CTkButton(master=app, text="Install ", 
                    hover_color="#57615F",  
                    font=("Segoe UI", 13, "bold"),
                    corner_radius=32, fg_color="transparent",
                    border_color="#FFFFFF", 
                    border_width=1.5,
                    command=setup_engine,
                    )

btn.place(relx=0.48, rely=0.63, anchor="center")

img2 = Image.open("switch.png")
ctk_img2 = ctk.CTkImage(light_image=img2, dark_image=img2, size=(50, 50))
door_label = ctk.CTkLabel(master=app, image=ctk_img2, text="", cursor="hand2")
door_label.place(relx=0.2, rely=0.8, anchor="ne")                                       #exit image to close the app
door_label.bind("<Button-1>", lambda event: close_app())

def close_app(event=None):
    app.destroy()


app.mainloop()


