import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

class CubeVisualizer:
    def __init__(self, root, cube):
        # Inisialisasi GUI dan menghubungkan cube yang akan divisualisasikan
        self.root = root
        self.cube = cube

        # Membuat figure Matplotlib untuk tampilan 3D
        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Tampilkan cube pertama kali
        self.display_cube()

        # Tambahkan tombol untuk menghasilkan successor acak
        self.random_button = tk.Button(self.root, text="Generate Random Successor", command=self.generate_random_successor)
        self.random_button.pack()

    def display_cube(self):
        # Menampilkan cube dalam bentuk 3D
        ax = self.figure.add_subplot(111, projection='3d')
        ax.clear()  # Bersihkan plot sebelum menggambar ulang

        n = self.cube.size
        offset = 1.5  # Tambahkan jarak yang lebih besar antara elemen cube

        # Loop untuk setiap elemen dalam cube, dengan jarak antar layer
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    # Gambar cube sebagai titik kotak dengan transparansi
                    ax.bar3d(i + offset * i, j + offset * j, k + offset * k, 1, 1, 1, shade=True, color='lightblue', edgecolor='black', alpha=0.3)

                    # Tambahkan angka di tengah cube
                    ax.text(i + 0.5 + offset * i, j + 0.5 + offset * j, k + 0.5 + offset * k,
                            str(self.cube.cube[i, j, k]), color='black', ha='center', va='center', fontsize=12, weight='bold')

        # Atur tampilan sudut pandang kamera
        ax.view_init(elev=30, azim=45)

        # Sesuaikan jarak tampilan (zoom in atau zoom out)
        ax.set_box_aspect([1, 1, 1])  # Pastikan setiap dimensi cube proporsional

        # Perbarui tampilan canvas
        self.canvas.draw()

    def generate_random_successor(self):
        # Menghasilkan successor acak dan memperbarui tampilan cube
        self.cube = self.cube.generate_random_successor()
        self.display_cube()  # Gambar ulang cube dengan successor acak
