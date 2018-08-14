from tkinter import *
import sqlite3
import requests
from bs4 import BeautifulSoup

window = Tk()

conn = sqlite3.connect("movies.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS movies (title TEXT, director TEXT, year TEXT)")
conn.commit()
conn.close()

def insert(title, director, year):
    conn = sqlite3.connect("movies.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO movies VALUES(?, ?, ?)", (title, director, year))
    conn.commit()
    conn.close()

def add():
    title = e_title_val.get()
    director = e_director_val.get()
    year = e_year_val.get()
    if len(title) == 0 or len(director) == 0 or len(year) == 0:
        pass
    else:
        insert(title, director, year)
        print(title)
        print(director)
        print(year)
        e_title.delete(0, 'end')
        e_director.delete(0, 'end')
        e_year.delete(0, 'end')

def view():
    display.delete('1.0', END)
    conn = sqlite3.connect("movies.db")

    cur = conn.cursor()

    cur.execute("SELECT * FROM movies")

    rows = cur.fetchall()

    conn.close()

    for movie in rows:
        for info in movie:
            display.insert(END, str(info) + '\n')
        display.insert(END, '\n')

def search():
    display.delete('1.0', END)
    title = e_title_val.get()
    director = e_director_val.get()
    year = e_year_val.get()

    conn = sqlite3.connect("movies.db")

    cur = conn.cursor()

    cur.execute("SELECT * FROM movies WHERE title = ? OR director = ? OR year = ?", (title, director, year))

    rows = cur.fetchall()

    conn.close()

    for movie in rows:
        for info in movie:
            display.insert(END, str(info) + '\n')
        display.insert(END, '\n')

def imdb():
    conn = sqlite3.connect("movies.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM movies")
    conn.commit()
    conn.close()
    r = requests.get("https://www.imdb.com/chart/top")

    c = r.content

    soup = BeautifulSoup(c, "html.parser")

    items = soup.find_all("td", {"class" : "titleColumn"})

    titles = list()
    directors = list()
    years = list()

    for i in range(10):
        title = soup.find_all("td", {"class" : "titleColumn"})[i].find("a", recursive = False)
        year = soup.find_all("span", {"class" : "secondaryInfo"})[i].text
        titles.append(title.text)
        directors.append(title.get('title').split("(")[0])
        years.append(year[1:5])
    
    for title, director, year in zip(titles, directors, years):
        insert(title, director, year)

l_title = Label(window, text = "Title: ")
l_title.grid(row = 0, column = 0)

e_title_val = StringVar()
e_title = Entry(window, textvariable = e_title_val)
e_title.grid(row = 0, column = 1)

l_director = Label(window, text = "Director: ")
l_director.grid(row = 0, column = 2)

e_director_val = StringVar()
e_director = Entry(window, textvariable = e_director_val)
e_director.grid(row = 0, column = 3)

l_year = Label(window, text = "Year: ")
l_year.grid(row = 1, column = 0)

e_year_val = StringVar()
e_year = Entry(window, textvariable = e_year_val)
e_year.grid(row = 1, column = 1)

button_group = LabelFrame(window, text = "Controls")


b_add = Button(button_group, text = "Add", command = add)
b_add.pack()
# b_add.grid(row = 1, column = 2, columnspan = 3)

b_show = Button(button_group, text = "Display", command = view)
b_show.pack()
# b_show.grid(row = 2, column = 2, columnspan = 3)

b_search = Button(button_group, text = "Search", command = search)
b_search.pack()

b_imdb = Button(button_group, text = "IMDb 250", command = imdb)
b_imdb.pack()

button_group.grid(row = 2, column = 2, columnspan = 3)

display = Text(window, height = 20, width = 30)
display.grid(row = 2, column = 0, columnspan = 2)

window.mainloop()