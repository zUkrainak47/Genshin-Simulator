import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Toplevel
from artifact_simulator import transmute, sets, substats, artifact_types, type_to_main_stats, set_to_image


def update_button_state():
    selected_substats = sum([var.get() for var in substat_vars])
    if selected_substats == 2:
        transmute_button.configure(state="normal")
    else:
        transmute_button.configure(state="disabled")


def on_transmute():
    artifact_set = artifact_set_var.get()
    artifact_type = artifact_type_var.get()
    main_stat = main_stat_var.get()
    selected_substats = [substats[i] for i, var in enumerate(substat_vars) if var.get()]
    preset = [artifact_type, main_stat] + selected_substats + [artifact_set]
    art, _ = transmute(preset)
    art.print_stats()


def update_main_stats(*args):
    artifact_type = artifact_type_var.get()
    new_main_stats = type_to_main_stats.get(artifact_type, [])
    main_stat_menu.configure(values=new_main_stats)
    main_stat_var.set(new_main_stats[0])


def choose_artifact_set(set_name, image):
    artifact_set_var.set(set_name)
    artifact_set_button.configure(image=image, text=set_name)
    dropdown_window.destroy()


def open_artifact_set_dropdown():
    global dropdown_window
    dropdown_window = Toplevel(app)
    dropdown_window.geometry("250x400")  # Adjust size as needed

    scrollable_frame = ctk.CTkScrollableFrame(dropdown_window, width=230, height=350)
    scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

    for artifact_set, image in set_to_image.items():
        btn_image = ctk.CTkImage(Image.open(image), size=(26, 26))
        btn = ctk.CTkButton(scrollable_frame, text=artifact_set, image=btn_image, compound="left",
                            command=lambda a_set=artifact_set, img=btn_image: choose_artifact_set(a_set, img))
        btn.pack(padx=10, pady=5)


# Initialize the tkinter window
app = ctk.CTk()
app.title("Artifact Simulator")

# Artifact Set Dropdown (Custom)
artifact_set_var = ctk.StringVar(value=sets[0])
button_image = ctk.CTkImage(Image.open(set_to_image[sets[0]]), size=(26, 26))
artifact_set_button = ctk.CTkButton(app, text=sets[0], image=button_image,
                                    compound="left", command=open_artifact_set_dropdown)
artifact_set_button.grid(row=0, column=1, padx=10, pady=10)

# Artifact Type Dropdown
artifact_type_var = ctk.StringVar(value=artifact_types[0])
artifact_type_var.trace_add("write", update_main_stats)
artifact_type_label = ctk.CTkLabel(app, text="Artifact Type")
artifact_type_label.grid(row=1, column=0, padx=10, pady=10)
artifact_type_menu = ctk.CTkOptionMenu(app, variable=artifact_type_var, values=artifact_types)
artifact_type_menu.grid(row=1, column=1, padx=10, pady=10)

# Main Stat Dropdown
main_stat_var = ctk.StringVar(value=type_to_main_stats[artifact_types[0]][0])
main_stat_label = ctk.CTkLabel(app, text="Main Stat")
main_stat_label.grid(row=2, column=0, padx=10, pady=10)
main_stat_menu = ctk.CTkOptionMenu(app, variable=main_stat_var, values=type_to_main_stats[artifact_types[0]])
main_stat_menu.grid(row=2, column=1, padx=10, pady=10)

# Sub Stats Checkboxes
substat_vars = [ctk.BooleanVar() for _ in substats]
substat_label = ctk.CTkLabel(app, text="Choose 2 Sub Stats")
substat_label.grid(row=3, column=0, padx=10, pady=10)

for i, substat in enumerate(substats):
    checkbox = ctk.CTkCheckBox(app, text=substat, variable=substat_vars[i], command=update_button_state)
    checkbox.grid(row=4 + i, column=0, columnspan=2, padx=10, pady=5)

# Transmute Button (initially disabled)
transmute_button = ctk.CTkButton(app, text="Transmute", command=on_transmute, state="disabled")
transmute_button.grid(row=4 + len(substats), column=0, columnspan=2, padx=10, pady=20)

# Run the application
app.mainloop()
