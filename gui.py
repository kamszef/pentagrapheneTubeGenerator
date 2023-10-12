import customtkinter
import main

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def generateTube():
    h_value = float(h.get())
    d22_value = float(d22.get())
    x_value = int(x.get())
    y_value = int(y.get())
    isPeriodic = bool(checkbox.get())
    print(h_value, d22_value, x_value, y_value, isPeriodic)
    main.main(d22_value, h_value, x_value, y_value, isPeriodic)
    

def switch_event():
    print(switch_var.get())
    if switch_var.get() == "on":
        h.delete(0, "end")
        h.insert(0, "0.1648")
        h.configure(state="disabled")
        d22.delete(0, "end")
        d22.insert(0, "0.3677")
        d22.configure(state="disabled")
    elif switch_var.get() == "off":
        h.configure(state="normal")
        d22.configure(state="normal")    

app = customtkinter.CTk()
app.title("Pentagraphene Based Tube Generator")
app.geometry("800x500")
app.grid_columnconfigure((0), weight=1)

appName = customtkinter.CTkLabel(master=app, text="Pentagraphene Based Tube Generator", font=("Roboto", 28))
appName.grid(row=0, column=0, pady=20)

switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(app, text="Pentagraphene", variable=switch_var, onvalue="on", offvalue="off", font=("Roboto", 14), command=switch_event)
switch.grid(row=1, column=0, pady=20)

dataFrame = customtkinter.CTkFrame(master=app)
dataFrame.grid(row=2, column=0)


h = customtkinter.CTkEntry(master=dataFrame, placeholder_text="h")
h.grid(row=0, column=0, padx=20, pady=20)

d22 = customtkinter.CTkEntry(master=dataFrame, placeholder_text="d22")
d22.grid(row=0, column=1, padx=20, pady=20)

repetitionFrame = customtkinter.CTkFrame(master=app)
repetitionFrame.grid(row=3, column=0, pady=20)

x = customtkinter.CTkEntry(master=repetitionFrame, placeholder_text="x")
x.grid(row=1, column=0, padx=20, pady=20)

y = customtkinter.CTkEntry(master=repetitionFrame, placeholder_text="y")
y.grid(row=1, column=1, padx=20, pady=20)

checkbox = customtkinter.CTkCheckBox(master=app, text="Periodic", font=("Roboto", 14))
checkbox.grid(row=4, column=0, columnspan=2, padx=20, pady=5)

button = customtkinter.CTkButton(master=app, text="Generate", command=generateTube, font=("Roboto", 18), width=200, height=50)
button.grid(row=5, column=0, columnspan=2, padx=20, pady=25)

switch_event()

app.mainloop()
