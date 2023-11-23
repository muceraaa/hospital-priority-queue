import tkinter as tk
from tkinter import messagebox

class PriorityQueueGUI:
    def __init__(self, root):
        self.root = root #Initialize the priorityqueGUI with a tkinter root window
        self.root.title("Priority Queue Visualization") #set the title of the window

        self.priority_queue = [] #Initialize an empty list to rep the priority queue
        self.max_queue_size = 9  # Maximum limit for the priority queue

        self.create_widgets() #call the method to create the widgets of the GUI

    def create_widgets(self):
        # Hospital diagram
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Draw the hospital rectangle
        self.draw_hospital()

        # Priority Queue Operations
        # Create a frame for priority queue operations on the right side of the window
        operations_frame = tk.Frame(self.root)
        operations_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        #Entry for patient name
        tk.Label(operations_frame, text="PATIENT NAME:").grid(row=0, column=0, pady=5)
        self.name_entry = tk.Entry(operations_frame)
        self.name_entry.grid(row=0, column=1, pady=5)

        #Entry for patient age
        tk.Label(operations_frame, text="PATIENT AGE:").grid(row=1, column=0, pady=5)
        self.age_entry = tk.Entry(operations_frame)
        self.age_entry.grid(row=1, column=1, pady=5)
            
        #creating the buttons for the operations
        tk.Button(operations_frame, text="ADD PATIENT", command=self.add_patient, relief=tk.RAISED, bg='pink').grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(operations_frame, text="MIN", command=self.get_min, relief=tk.RAISED, bg='pink').grid(row=3, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="REMOVE MIN", command=self.remove_min, relief=tk.RAISED, bg='pink').grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="REMOVE PATIENT", command=self.remove_patient, relief=tk.RAISED, bg='pink').grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="UPDATE PRIORITY", command=self.update_priority, relief=tk.RAISED, bg='pink').grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="IS EMPTY", command=self.is_empty, relief=tk.RAISED, bg='pink').grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(operations_frame, text="QUEUE LENGTH", command=self.queue_length, relief=tk.RAISED, bg='pink').grid(row=8, column=0, columnspan=2, pady=5)

    def draw_hospital(self):
        # Draw the hospital rectangle
        self.canvas.create_line(50, 50, 750, 50, width=2)  # Top line
        self.canvas.create_line(50, 50, 50, 550, width=2)  # Left line
        self.canvas.create_line(50, 550, 750, 550, width=2)  # Bottom line
        self.canvas.create_line(750, 50, 750, 550, width=2)  # Right line

        # Draw HOSPITAL text centered at the top of the hospital rectangle
        hospital_text_x = (50 + 750) // 2
        hospital_text_y = 50 // 2
        self.canvas.create_text(hospital_text_x, hospital_text_y, text="HOSPITAL", font=('calibri', 16, 'bold'), fill='black')

        # Draw reception rectangle
        reception_x1 = 550
        reception_y1 = 400
        reception_x2 = 750
        reception_y2 = 550
        self.canvas.create_rectangle(reception_x1, reception_y1, reception_x2, reception_y2, outline='black', width=2, fill='pink')
        self.canvas.create_text((reception_x1 + reception_x2) // 2, (reception_y1 + reception_y2) // 2, text="RECEPTION", font=('calibri', 16, 'bold'))

    def add_patient(self):
        if len(self.priority_queue) >= self.max_queue_size: #check if PQ has reached its maximum limit
            self.show_error(f"Cannot add more patients. Maximum limit reached ({self.max_queue_size}).") #if limit is reached
            return

        #retrieve patient name and age from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        #check if both name and age are provided
        if name and age:
            try:
                age = int(age) #convert the age to an integer
                patient_id = len(self.priority_queue) #generate unique id for each patient using PQ length
                # Append the patient information to the priority queue as a tuple (age, name, patient_id)
                self.priority_queue.append((age, name, patient_id)) 
                # Arrange the patients in ascending order based on age
                self.priority_queue.sort(key=lambda x: x[0])

                # Visualize the patient in the hospital
                self.visualize_patients()

            except ValueError:
                self.show_error("Invalid age. Please enter a valid integer.") #if age is not valid int

        else:
            self.show_error("Please enter both name and age.") #if both name and age are not provided

    def get_min(self):
        if self.priority_queue: #checks if the PQ is empty, if not
            min_patient = self.priority_queue[0] #retrieves patient with the minimum key; the 1st element in the PQ
            message = f"Min: {min_patient[1]} ({min_patient[0]})" #creates a message with the patient info
            self.show_info(message) #display the message
        else:
            self.show_error("The priority queue is empty.") #if empty

    def remove_min(self):
        if self.priority_queue: #check if PQ is empty, if not
            removed_patient = self.priority_queue.pop(0) #removes patient with the minimum key; the 1st element in the PQ
            message = f"Removed Min: {removed_patient[1]} ({removed_patient[0]})" #creates a message w patient info
            self.show_info(message) #display message

            # Remove the visual representation of the patient from the hospital
            patient_id = removed_patient[2]
            self.canvas.delete(f"patient_{patient_id}")

            # Adjust the space between patients and visualize them
            self.visualize_patients()

        else:
            self.show_error("The priority queue is empty.") #if empty

    def remove_patient(self):
        #Retrieve patient name and age from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        #check if both name and age are provided
        if name and age:
            try:
                age = int(age) #convert the age to an integer

                # Find the patient in the priority queue
                for patient in self.priority_queue:
                    if patient[1] == name and patient[0] == age:
                        #retrieve patient id for visual removal
                        patient_id = patient[2]
                        self.priority_queue.remove(patient) #remove patient from the PQ

                        # Remove the visual representation of the patient from the hospital
                        self.canvas.delete(f"patient_{patient_id}")

                        # Adjust the space between patients and visualize them
                        self.visualize_patients()
                        # show info message w the patient info
                        message = f"Removed Patient: {name} ({age} )"
                        self.show_info(message)
                        return
                    
                #error message if patient is not in the PQ
                self.show_error("Patient not found in the priority queue.")
           
            except ValueError:
                 #error message if age is not an integer
                self.show_error("Invalid age. Please enter a valid integer.")
                
        else:
            #error message if both age and name are not provided
            self.show_error("Please enter both name and age.")

    def update_priority(self):
        # Retrieve patient name and age from the entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()

        if name and age:  # Check if both name and age are provided
            try:
                age = int(age)  # Convert the age to an integer

                # Find the patient in the priority queue
                for i, patient in enumerate(self.priority_queue):
                    if patient[1] == name and patient[0] == age:
                        # Open a new window to get the updated key from the user
                        update_window = tk.Toplevel(self.root)
                        update_window.title("Update Priority")

                        # Create an entry field for the user to enter the new key
                        tk.Label(update_window, text="Enter New Key:").grid(row=0, column=0, pady=5)
                        new_age_entry = tk.Entry(update_window)
                        new_age_entry.grid(row=0, column=1, pady=5)

                        # Create a button to confirm the update
                        tk.Button(update_window, text="Update", command=lambda i=i: self.update_priority_confirm(i, new_age_entry.get(), update_window), relief=tk.RAISED, bg='pink').grid(row=1, column=0, columnspan=2, pady=10)

                        return

                self.show_error("Patient not found in the priority queue.") #if patient is not in PQ

            except ValueError:
                self.show_error("Invalid age. Please enter a valid integer.") #if age is not a valid int

        else:
            self.show_error("Please enter both name and age.") #if both age and name have not been entered.

    def update_priority_confirm(self, index, new_age, update_window):
        try:
            new_age = int(new_age) #convert new key to int
            old_patient = self.priority_queue[index] #retrieve info about the old patient
            new_patient = (new_age, old_patient[1], old_patient[2]) #create a tuple with new updated key

            # Update the key (age) of the patient
            self.priority_queue[index] = new_patient

            # Arrange the patients in ascending order based on the updated key
            self.priority_queue.sort(key=lambda x: x[0])

            # Visualize the patient in the hospital
            self.visualize_patients()

            #display message about the update
            message = f"Updated Priority for Patient: {old_patient[1]} (New key: {new_age})"
            self.show_info(message)

            update_window.destroy() #close update window

        except ValueError:
            self.show_error("Invalid age. Please enter a valid integer.") #error if age is not valid int

    def visualize_patients(self):
        # Clear previous patient visualizations
        self.canvas.delete("all")

        # Draw the hospital and reception
        self.draw_hospital()

        # Adjust the space between patients and visualize them
        for i, (age, name, patient_id) in enumerate(self.priority_queue):
            x = 550 - (i + 1) * 50
            y = 500
            oval = self.canvas.create_oval(x - 20, y - 55, x + 20, y + 15, fill='brown', tags=f"patient_{patient_id}")
            text = self.canvas.create_text(x, y - 65, text=f"{age}", font=('calibri', 10), anchor='center', tags=f"patient_{patient_id}") #above
            text = self.canvas.create_text(x, y + 30, text=f"{name}", font=('calibri', 10), anchor='center', tags=f"patient_{patient_id}") #below


    def is_empty(self): #check if PQ is empty
        if not self.priority_queue:
            self.show_info("True.")
        else:
            self.show_info("False.")

    def queue_length(self): #get length of PQ
        message = f"Queue Length: {len(self.priority_queue)}"
        self.show_info(message)

    # Display an information message box with the provided message   
    def show_info(self, message):
        messagebox.showinfo("Information", message)

    # Display an error message box with the provided message    
    def show_error(self, message):
        messagebox.showerror("Error", message)

if __name__ == "__main__": #checks if script is being run as the main program
    root = tk.Tk() #create tkinter root window
    app = PriorityQueueGUI(root)
    root.mainloop() #starts the event loop to run the GUI
