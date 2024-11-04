<h1 align="center">Tugas Besar 1 IF3170 Inteligensi Artifisial</h1>
<h1 align="center">Semester I tahun 2024/2025</h1>
<h1 align="center">Pencarian Solusi Diagonal Magic Cube dengan Local Search</h1>

## Table of Contents

- [Deskripsi Program](#deskripsi-program)
- [Setup](#set-up-program)
- [Run](#how-to-run)
- [Pembagian Tugas](#pembagian-tugas)

## Deskripsi Program
Program ini merupakan program untuk mencari solusi dari diagonal magic cube dengan beberapa jenis algoritma local search seperti Steepest Ascent Hill-Climbing, Hill-Climbing with Sideways Move, Random Restart Hill-Climbing, Stochastic Hill-Climbing, Simulated Annealing, dan Genetic Algorithm.

## Set Up Program
1. Sebelum dapat menjalankan program, clone github terlebih dahulu dengan command seperti berikut di terminal
```bash
   git clone https://github.com/wegeh/IF3170_Tubes1.git
```
2. Masuk ke dalam directory folder yang telah di clone tadi
```bash
   cd IF3170_Tubes1/src
```
3. Jalankan command berikut untuk menginstall seluruh module yang dibutuhkan untuk program ini
```bash
   pip install -r requirements.txt
```
4. Program telah siap untuk dijalankan

## How to Run
1. Untuk menjalankan program, cukup masukkan command berikut dan program akan langsung berjalan
```bash
   cd src
   python -u main.py
```

## Pembagian Tugas
| NIM      | Nama                    | Tugas                                                                                           |
| -------- | ----------------------- | ----------------------------------------------------------------------------------------------- |
| 13522111 | Ivan Hendrawan Tan      | Stochastic HC, eksperimen dan analisis, laporan                                                 |
| 13522113 | William Glory Henderson | Genetic algorithm, simulated annealing, HC with sideways move, eksperimen dan analisis, laporan |
| 13522116 | Naufal Adnan            | Random restart HC, eksperimen dan analisis, laporan                                             |
| 13522117 | Mesach Harmasendro      | Steepest Ascent HC, GUI, genetic algorithm, eksperimen dan analisis, laporan                    |
