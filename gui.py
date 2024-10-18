import scraper
from tkinter import *
from tkinter.ttk import Label, Entry, Button, Combobox, Treeview
from tkinter import messagebox
import tkinter as tk

def addGame():
    url = urlEntry.get()
    if ("https://store.steampowered.com/app/" in url) and (url not in scraper.URLS):
        urlEntry.delete(0, END)
        all.append(scraper.getSingleInfo(url))
        scraper.URLS.append(url)
        updateCombobox()
        updateDisplay("all")
    else:
        messagebox.showerror("")

def removeGame():
    toRemove = removeTitle.get()
    for name in all:
        if toRemove == name["name"]:
            removeURL(name["appid"])
            break

def removeURL(appid):
    index = 0
    while index < len(all):
        game = all[index]
        if game["appid"] == appid:
            del all[index]
        index += 1
    
    index = 0
    while index < len(scraper.URLS):
        if appid in scraper.URLS[index]:
            del scraper.URLS[index]
        index += 1
    
    updateCombobox()
    updateDisplay("all")
       
def updateCombobox():
    removeTitle['values'] = [game["name"] for game in all]
    removeTitle.set('')

def closeApp():
    scraper.writeLinks(scraper.URLS)
    root.destroy()

def updateDisplay(filter):
    
    for item in listInfo.get_children():
        listInfo.delete(item)
    
    onlyDate = scraper.onlyDate(all)
    noReleaseDate = scraper.noReleaseDate(all)
    alreadyReleased = scraper.alreadyReleased(onlyDate)
    unreleasedDate = scraper.unreleasedDate(onlyDate)
    releasingToday = scraper.releasingToday(onlyDate)
    games = []

    if filter == "all":
        games = all
    elif filter == "releasing today":
        games = releasingToday
    elif filter == "upcoming date":
        games = unreleasedDate
    elif filter == "upcoming no date":
        games = noReleaseDate
    

    for game in games:
        listInfo.insert("", "end", values=(game["name"], game["release date"], game["drm"], game["store url"]))

    visible_rows = len(games)
    listInfo.configure(height=visible_rows)

scraper.URLS = scraper.readLinks(scraper.URLS)

all = scraper.getInfo(scraper.URLS)
onlyDate = scraper.onlyDate(all)
noReleaseDate = scraper.noReleaseDate(all)
alreadyReleased = scraper.alreadyReleased(onlyDate)
unreleasedDate = scraper.unreleasedDate(onlyDate)
releasingToday = scraper.releasingToday(onlyDate)

root = Tk()
root.title("Drop Manager")

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "dark")

button_frame = Frame(root)
button_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky=W)

url = Label(button_frame, text='Add a Game:')
url.grid(row=0, column=0, padx=10, pady=10)

urlEntry = Entry(button_frame)
urlEntry.grid(row=0, column=1, padx=10, pady=10)

addButton = Button(button_frame, text="Add Game", command=addGame)
addButton.grid(row=0, column=2, padx=10, pady=10)

remove = Label(button_frame, text="Remove a Game:")
remove.grid(row=1, column=0, padx=10, pady=10)

removeTitle = Combobox(button_frame, values=[game["name"] for game in all])
removeTitle.grid(row=1, column=1)

removeButton = Button(button_frame, text="Remove Game", command=removeGame)
removeButton.grid(row=1, column=2, padx=10, pady=10)

filter_frame = Frame(root)
filter_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=30)

showAll = Button(filter_frame, text='All Games', command=lambda: updateDisplay("all"))
showAll.grid(row=0, column=0, padx=10, pady=10)

releasingToday = Button(filter_frame, text='Releasing Today', command=lambda: updateDisplay("releasing today"))
releasingToday.grid(row=0, column=1, padx=10, pady=10)

upcomingDate = Button(filter_frame, text='Upcoming (Date)', command=lambda: updateDisplay("upcoming date"))
upcomingDate.grid(row=0, column=2, padx=10, pady=10)

upcomingNoDate = Button(filter_frame, text='Upcoming (No Date)', command=lambda: updateDisplay("upcoming no date"))
upcomingNoDate.grid(row=0, column=3, padx=10, pady=10)

columns = ("Name", "Release Date", "DRM", "Store Page")
listInfo = Treeview(root, columns=columns, show='headings', height=10)

listInfo.column("Name", width=250, anchor="center", stretch=NO)
listInfo.column("Release Date", width=150, anchor="center", stretch=NO)
listInfo.column("DRM", width=100, anchor="center", stretch=NO)
listInfo.column("Store Page", width=550, anchor="center", stretch=NO)

listInfo.heading("Name", text="Name")
listInfo.heading("Release Date", text="Release Date")
listInfo.heading("DRM", text="DRM")
listInfo.heading("Store Page", text="Store Page")

listInfo.grid(row=2, column=0, columnspan=5, sticky=NSEW, padx=20, pady=20)

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

endButton = Button(root, text='Exit', command=closeApp)
endButton.grid(row=3, column=0, columnspan=5, padx=10, pady=30)

updateDisplay("all")

root.mainloop()