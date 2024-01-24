import time
import psutil
import tkinter as tk
import GPUtil

def display_usage():
    current_time = time.strftime("%H:%M:%S")
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    gpu_info = get_gpu_info()

    update_labels(cpu_percent, ram_percent, current_time, gpu_info)
    update_chart(cpu_percent, ram_percent, current_time)

    root.after(500, display_usage)

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]  # Assume only one GPU, you may need to modify this if you have multiple GPUs
            gpu_percent = gpu.load * 100
            gpu_temperature = gpu.temperature
            return gpu_percent, gpu_temperature
        else:
            return None, None
    except Exception as e:
        print(f"Error retrieving GPU information: {e}")
        return None, None

def update_labels(cpu_percent, ram_percent, current_time, gpu_info):
    cpu_bar = chr(0x2588) * int(cpu_percent) + '-' * (100 - int(cpu_percent))
    ram_bar = chr(0x2588) * int(ram_percent) + '-' * (100 - int(ram_percent))

    gpu_percent, gpu_temperature = gpu_info
    gpu_percent = gpu_percent if gpu_percent is not None else 0  # Set a default value if gpu_percent is None
    gpu_bar = chr(0x2588) * int(gpu_percent) + '-' * (100 - int(gpu_percent))

    cpu_label.config(text=f"CPU Usage: |{cpu_bar}| {cpu_percent:.2f}%")
    ram_label.config(text=f"RAM Usage: |{ram_bar}| {ram_percent:.2f}%")
    gpu_label.config(text=f"GPU Usage: |{gpu_bar}| {gpu_percent:.2f}%\nTemperature: {gpu_temperature}°C")
    time_label.config(text=f"Time: {current_time}")


def update_chart(cpu_percent, ram_percent, current_time):
    x = len(cpu_data)

    cpu_data.append(cpu_percent)
    ram_data.append(ram_percent)
    time_data.append(current_time)

    gpu_info = get_gpu_info()
    gpu_percent, _ = gpu_info
    gpu_data.append(gpu_percent if gpu_percent is not None else 0)  # Set a default value if gpu_percent is None

    if x > max_data_points:
        start_index = x - max_data_points
    else:
        start_index = 0

    canvas.delete("chart")

    # Draw the frame
    canvas.create_rectangle(0, 0, canvas_width, canvas_height, outline="black", tags="frame")

    # Draw X-axis label
    for i in range(start_index, x, 10):
        x_coord = (i - start_index) * x_spacing
        canvas.create_text(x_coord, canvas_height + 10, text=time_data[i], font=("Arial", 8), anchor="n", fill="black")

    # Draw Y-axis labels
    for y in range(0, 110, 10):
        y_coord = canvas_height - (y * canvas_height / 100)
        canvas.create_text(canvas_width + 10, y_coord, text=f"{y}%", font=("Arial", 8), anchor="e", fill="black")

    # Draw time elapsed
    elapsed_time = time.time() - start_time
    canvas.create_text(canvas_width // 2, canvas_height + 30, text=f"Time Elapsed: {format_time(elapsed_time)}", font=("Arial", 12), fill="black")

    # Draw CPU line chart
    for i in range(start_index, x - 1):
        x_coord1 = (i - start_index) * x_spacing
        x_coord2 = (i + 1 - start_index) * x_spacing
        y_coord1 = canvas_height - cpu_data[i]
        y_coord2 = canvas_height - cpu_data[i + 1]
        canvas.create_line(x_coord1, y_coord1, x_coord2, y_coord2, fill="blue", width=2, tags="chart")

    # Draw RAM line chart
    for i in range(start_index, x - 1):
        x_coord1 = (i - start_index) * x_spacing
        x_coord2 = (i + 1 - start_index) * x_spacing
        y_coord1 = canvas_height - ram_data[i]
        y_coord2 = canvas_height - ram_data[i + 1]
        canvas.create_line(x_coord1, y_coord1, x_coord2, y_coord2, fill="green", width=2, tags="chart")

    # Draw GPU line chart
    for i in range(start_index, x - 1):
        x_coord1 = (i - start_index) * x_spacing
        x_coord2 = (i + 1 - start_index) * x_spacing
        y_coord1 = canvas_height - gpu_data[i]
        y_coord2 = canvas_height - gpu_data[i + 1]
        canvas.create_line(x_coord1, y_coord1, x_coord2, y_coord2, fill="red", width=2, tags="chart")

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


# Tkinter setup
root = tk.Tk()
root.title("System Usage Monitor")

canvas_height = 300
canvas_width = 600
max_data_points = 60
x_spacing = canvas_width // max_data_points

cpu_data = [0]
ram_data = [0]
gpu_data = [0]
time_data = []

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
canvas.pack()

cpu_label = tk.Label(root, text="", fg="black")
ram_label = tk.Label(root, text="", fg="black")
gpu_label = tk.Label(root, text="", fg="black")
time_label = tk.Label(root, text="", fg="black")

cpu_label.pack()
ram_label.pack()
gpu_label.pack()
time_label.pack()

start_time = time.time()

display_usage()

root.mainloop()
