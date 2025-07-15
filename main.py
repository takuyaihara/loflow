import tkinter as tk

def main():
    root = tk.Tk()
    root.title("LoFlow")
    root.geometry("400x200")
    label = tk.Label(root, text="🎵 LoFlow - AI Lo-fi BGM Generator", font=("Arial", 14))
    label.pack(pady=50)

    root.mainloop()

if __name__ == "__main__":
    main()
