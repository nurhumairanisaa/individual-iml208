import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Initialize hotel data
rooms = {
    101: {"type": "Single", "price": 150, "booked": False},
    102: {"type": "Single", "price": 150, "booked": False},
    103: {"type": "Single", "price": 150, "booked": False},
    104: {"type": "Single", "price": 150, "booked": False},
    105: {"type": "Single", "price": 150, "booked": False},
    201: {"type": "Double", "price": 300, "booked": False},
    202: {"type": "Double", "price": 300, "booked": False},
    203: {"type": "Double", "price": 300, "booked": False},
    204: {"type": "Double", "price": 300, "booked": False},
    205: {"type": "Double", "price": 300, "booked": False},
    301: {"type": "Suite", "price": 500, "booked": False},
    302: {"type": "Suite", "price": 500, "booked": False},
    303: {"type": "Suite", "price": 500, "booked": False},
    304: {"type": "Suite", "price": 500, "booked": False},
    305: {"type": "Suite", "price": 500, "booked": False},
}
bookings = []
tax_rate = 0.10

def list_available_rooms():
    month = datetime.now().month
    seasonal_price_multiplier = 1.5 if month == 12 else 1
    return [
        {
            "room": num,
            "type": info["type"],
            "price": info["price"] * seasonal_price_multiplier,
        }
        for num, info in rooms.items()
        if not info["booked"]
    ]

def book_room(room_no, guest_name, contact_email, contact_number, check_in, check_out):
    if room_no not in rooms or rooms[room_no]["booked"]:
        return None, f"Room {room_no} is unavailable or invalid."

    try:
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        if check_out_date <= check_in_date:
            return None, "Check-out date must be after check-in date."

        nights = (check_out_date - check_in_date).days
        room_price = rooms[room_no]["price"]
        tax = room_price * nights * tax_rate
        total_cost = (room_price * nights) + tax

        return {
            "room": room_no,
            "guest": guest_name,
            "email": contact_email,
            "contact": contact_number,
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "total": total_cost,
        }, None
    except ValueError:
        return None, "Invalid date format. Use YYYY-MM-DD."

def confirm_booking(booking, payment_method):
    rooms[booking["room"]]["booked"] = True
    booking["payment_method"] = payment_method
    bookings.append(booking)
    return (
        f"Room {booking['room']} booked for {booking['guest']} from "
        f"{booking['check_in']} to {booking['check_out']}\n"
        f"Total: RM{booking['total']:.2f} (including tax).\n"
        f"Payment Method: {payment_method}."
    )

def view_bookings():
    if not bookings:
        return "No bookings have been made."
    return "\n\n".join(
        f"Room {b['room']} booked by {b['guest']} ({b['check_in']} to {b['check_out']}): RM{b['total']:.2f}, Email: {b['email']}, Contact: {b['contact']}, Payment: {b['payment_method']}"
        for b in bookings
    )

def delete_booking(room_no):
    for booking in bookings:
        if booking["room"] == room_no:
            bookings.remove(booking)
            rooms[room_no]["booked"] = False
            return f"Booking for room {room_no} has been deleted."
    return f"No booking found for room {room_no}."

class HotelBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MaiKim's Hotel Booking System")
        self.root.geometry("1024x768")
        self.root.configure(bg="#f0f0f0")

        messagebox.showinfo("Welcome", "Welcome to MaiKim Hotel!")

        tk.Button(
            root,
            text="List Available Rooms",
            command=self.list_rooms,
            width=30,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=10)

        tk.Button(
            root,
            text="Book a Room",
            command=self.book_room,
            width=30,
            bg="#2196F3",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=10)

        tk.Button(
            root,
            text="Delete a Booking",
            command=self.delete_booking,
            width=30,
            bg="#FF5722",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=10)

        tk.Button(
            root,
            text="View All Bookings",
            command=self.view_bookings,
            width=30,
            bg="#FFC107",
            fg="black",
            font=("Arial", 16),
        ).pack(pady=10)

        tk.Button(
            root,
            text="Exit",
            command=root.quit,
            width=30,
            bg="#F44336",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=10)

    def list_rooms(self):
        rooms = list_available_rooms()
        room_window = tk.Toplevel(self.root)
        room_window.title("Available Rooms")
        room_window.geometry("400x400")
        room_window.configure(bg="#ffffff")

        tk.Label(
            room_window, text="Available Rooms:", font=("Arial", 16), bg="#ffffff"
        ).pack(pady=10)
        room_list = tk.Listbox(room_window, width=50, height=15, font=("Arial", 14))
        room_list.pack(pady=5)

        if rooms:
            for room in rooms:
                room_list.insert(
                    tk.END,
                    f"Room {room['room']} ({room['type']}) - RM{room['price']:.2f}/night",
                )
        else:
            room_list.insert(tk.END, "No rooms available.")

        tk.Button(
            room_window,
            text="Close",
            command=room_window.destroy,
            bg="#F44336",
            fg="white",
            font=("Arial", 14),
        ).pack(pady=10)

    def book_room(self):
        window = tk.Toplevel(self.root)
        window.title("Book a Room")
        window.geometry("600x600")
        window.configure(bg="#ffffff")

        available_rooms = list_available_rooms()
        room_options = [
            f"{room['room']} ({room['type']})" for room in available_rooms
        ]

        tk.Label(window, text="Select Room:", font=("Arial", 16), bg="#ffffff").grid(
            row=0, column=0, padx=10, pady=10
        )
        room_dropdown = ttk.Combobox(window, values=room_options, font=("Arial", 14))
        room_dropdown.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(window, text="Guest Name:", font=("Arial", 16), bg="#ffffff").grid(
            row=1, column=0, padx=10, pady=10
        )
        guest_name_entry = tk.Entry(window, font=("Arial", 14))
        guest_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(window, text="Email:", font=("Arial", 16), bg="#ffffff").grid(
            row=2, column=0, padx=10, pady=10
        )
        email_entry = tk.Entry(window, font=("Arial", 14))
        email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(window, text="Contact Number:", font=("Arial", 16), bg="#ffffff").grid(
            row=3, column=0, padx=10, pady=10
        )
        contact_number_entry = tk.Entry(window, font=("Arial", 14))
        contact_number_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(
            window, text="Check-in Date (YYYY-MM-DD):", font=("Arial", 16), bg="#ffffff"
        ).grid(row=4, column=0, padx=10, pady=10)
        check_in_entry = tk.Entry(window, font=("Arial", 14))
        check_in_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(
            window, text="Check-out Date (YYYY-MM-DD):", font=("Arial", 16), bg="#ffffff"
        ).grid(row=5, column=0, padx=10, pady=10)
        check_out_entry = tk.Entry(window, font=("Arial", 14))
        check_out_entry.grid(row=5, column=1, padx=10, pady=10)

        def next_payment():
            selected_room = room_dropdown.get()
            guest = guest_name_entry.get()
            email = email_entry.get()
            contact_number = contact_number_entry.get()
            check_in = check_in_entry.get()
            check_out = check_out_entry.get()

            if not selected_room or not guest or not email or not contact_number:
                messagebox.showerror("Error", "Please fill all fields.")
                return

            try:
                room_no = int(selected_room.split()[0])
                booking, error = book_room(room_no, guest, email, contact_number, check_in, check_out)
                if error:
                    messagebox.showerror("Error", error)
                else:
                    window.destroy()
                    self.payment_widget(booking)
            except ValueError:
                messagebox.showerror("Error", "Invalid room selection.")

        tk.Button(
            window,
            text="Next: Payment",
            command=next_payment,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 16),
        ).grid(row=6, column=0, columnspan=2, pady=20)

    def payment_widget(self, booking):
        window = tk.Toplevel(self.root)
        window.title("Payment Method")
        window.geometry("400x400")
        window.configure(bg="#ffffff")

        tk.Label(
            window, text="Select Payment Method:", font=("Arial", 16), bg="#ffffff"
        ).pack(pady=10)

        payment_method_var = tk.StringVar(value="Pay at the Counter")
        payment_method_dropdown = ttk.Combobox(
            window,
            textvariable=payment_method_var,
            values=["Pay at the Counter", "Card Payment",],
            font=("Arial", 14),
        )
        payment_method_dropdown.pack(pady=10)

        # Voucher Code Field
        tk.Label(window, text="Voucher Code (Optional):", font=("Arial", 16), bg="#ffffff").pack(pady=10)
        voucher_code_entry = tk.Entry(window, font=("Arial", 14))
        voucher_code_entry.pack(pady=10)

        def apply_voucher():
            voucher_code = voucher_code_entry.get().strip()
            if voucher_code == "DISCOUNT10":  # Example voucher code
                discount = 0.10  # 10% discount
                discounted_total = booking["total"] * (1 - discount)
                return discounted_total, discount
            elif voucher_code == "DISCOUNT20":  # Another example voucher code
                discount = 0.20  # 20% discount
                discounted_total = booking["total"] * (1 - discount)
                return discounted_total, discount
            else:
                return booking["total"], 0

        def confirm_payment():
            discounted_total, discount = apply_voucher()
            booking["total"] = discounted_total  # Update booking total

            if discount > 0:
                messagebox.showinfo(
                    "Voucher Applied", f"Voucher applied! You get a {int(discount * 100)}% discount."
                )

            payment_method = payment_method_var.get()
            result = confirm_booking(booking, payment_method)
            messagebox.showinfo("Booking Confirmation", result)
            window.destroy()

        tk.Button(
            window,
            text="Confirm Payment",
            command=confirm_payment,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=20)

    def delete_booking(self):
        window = tk.Toplevel(self.root)
        window.title("Delete Booking")
        window.geometry("400x300")
        window.configure(bg="#ffffff")

        tk.Label(window, text="Enter Room Number:", font=("Arial", 16), bg="#ffffff").pack(pady=20)
        room_number_entry = tk.Entry(window, font=("Arial", 14))
        room_number_entry.pack(pady=10)

        def delete():
            try:
                room_no = int(room_number_entry.get())
                result = delete_booking(room_no)
                messagebox.showinfo("Delete Booking", result)
                window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid room number.")

        tk.Button(
            window,
            text="Delete",
            command=delete,
            bg="#F44336",
            fg="white",
            font=("Arial", 16),
        ).pack(pady=20)

    def view_bookings(self):
        bookings_info = view_bookings()
        messagebox.showinfo("Bookings", bookings_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelBookingApp(root)
    root.mainloop()