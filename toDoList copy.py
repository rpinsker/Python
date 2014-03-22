#!/usr/bin/env python3.3

import xml.etree.ElementTree as ET
from sys import argv
from sys import stdin
from datetime import date
import time
    
def isNone(text):
    if text is None:
        return ""
    else:
        return text

def printUncomplete():
    currentDate = time.strftime("%Y%m%d")
    items = map(Item,doc.findall('.//item'))
    items.sort()
    for i in items:
        if i.complete == "n":
            if int(currentDate) > i.date:
                format = '\033[91;1;4m'
            elif i.date - int(currentDate) == 1:
                format = '\033[93;1;4m'
            else:
                format = '\033[92;1;4m'
            if i.dueDate == "":
                due = ""
            else:
                due = " DUE: " + i.dueDate
            if i.notes == "":
                note = ""
            else:
                note = " NOTES: " + i.notes
            print(format + i.name + '\033[0m' + due +'\033[95m' + note + '\033[0m' + "\n")

def printCompleted():
    items = map(Item,doc.findall('.//item'))
    for i in items:
        if i.complete == "y":
            format = '\033[0m'
            if i.dueDate == "":
                due = ""
            else:
                due = " DUE: " + i.dueDate
            if i.notes == "":
                note = ""
            else:
                note = " NOTES: " + i.notes
            print(format + i.name + '\033[0m' + due +'\033[95m' + note + '\033[0m' + "\n")

def printByDate():
    print('\n\n\n')
    items = map(Item,doc.findall('.//item'))
    items.sort()    

    currentDate = time.strftime("%Y%m%d")
    past = 1
    today = 1
    future = 1
    noDate = 1
    format = '\033[0m'
    for i in items:
        if past == 1:
            if int(currentDate) > i.date:
                print("Tasks due before today:\n---------------------------------")
                past = 0
        if today == 1:
            if int(currentDate) == i.date:
                print("Tasks due today:\n----------------------------")
                today = 0
        if future == 1:
            if int(currentDate) < i.date:
                print("Tasks due after today:\n----------------------")
                future = 0
        if noDate == 1:
            if i.dueDate == "":
                print("Other tasks:\n----------------------")
                noDate = 0
        if int(currentDate) > i.date:
            if i.complete == "y" :
                format = '\033[0m'
            else:
                format = '\033[91;1;4m'
        elif i.date == int(currentDate):
            format = '\033[93;1;4m'
        elif i.date - int(currentDate) == 1:
            format = '\033[1;4;34;40m'
        else:
            format = '\033[92;1;4m'
        if i.complete == "y":
            format = '\033[0m'
        if i.dueDate == "":
            due = ""
        else:
            due = " DUE: " + i.dueDate
        if i.notes == "":
            note = ""
        else:
            note = " NOTES: " + i.notes
        print(format + i.name + '\033[0m' + due +'\033[95m' + note + '\033[0m' + "\n")
    nearestDueDate = 10000000000000
    nearestDate = ""
    for i in items:
        if i.date >= int(currentDate):
            if i.date < nearestDueDate:
                nearestDueDate = i.date
                nearestDate = i.dueDate

    print('\033[0m' + "Nearest due date is: " + nearestDate)
    print('\n\n\n')

def editTask():
    print("Enter name of task. Options include: ")
    for i in doc.findall('.//item'):
        print(i.get("name"))
    taskToEdit = stdin.readline()
    taskToEdit = taskToEdit[:-1]
    for i in doc.findall('.//item'):
        if i.get("name") == taskToEdit:
            print('Please enter new due date in the format: "yyyy-mm-dd" (no quotes) (To leave due date, hit return.)')
            newDate = stdin.readline()
            newDate = newDate[:-1]
            if newDate != "":
                i.find('.//dueDate').text = newDate
            print('Please enter notes: (To leave notes, hit return.)')
            newNotes = stdin.readline()
            newNotes = newNotes[:-1]
            newNotes = " " + newNotes
            if newNotes != " ":
                print('Would you like to add this to the notes or overwrite the current notes? ("a" to add, "o" to overwrite)')
                answer = stdin.readline()
                if answer == 'a\n':
                    i.find('.//Notes').text = isNone(i.find('.//Notes').text) + newNotes
                else:
                    i.find('.//Notes').text = newNotes
                

class Item(object):
    def __init__(self,element):
        self.name = element.get("name")
        self.complete = element.get("complete")
        self.dueDate = isNone(element.find('.//dueDate').text)
        self.notes = isNone(element.find('.//Notes').text)
        self.date = 10000000000
        if self.dueDate != "":
            self.year,self.month,self.day = self.dueDate.split('-')
            dateString = self.year + self.month + self.day
            self.date = int(dateString)
    def __lt__(self,other):
        return self.date < other.date 

doc = ET.parse(argv[1])
list = doc.getroot()

done = 1
while done == 1:
    input = ""
    print("Type 'x' to mark a task as complete, 'a' to add a task, 'r' to remove a task, 'd' to sort by due date, 'c' to show tasks completed, 'n' to show tasks not completed, 'e' to edit a task's due date and notes, and 'q' to quit")
    input = stdin.readline()
    if input == "a\n":
        print("Add task.\nPlease enter a name for your task: ")
        name = stdin.readline()
        name = name[:-1]
        newItem = ET.SubElement(list, "item", attrib={"name":name,"complete":"n"})
        print('Please enter due date in the format: "yyyy-mm-dd" (no quotes)')
        date = stdin.readline()
        date = date[:-1]
        dateElement = ET.SubElement(newItem, "dueDate")
        dateElement.text = date
        print('Please enter notes for your task')
        notes = stdin.readline()
        notes = notes[:-1]
        noteElement = ET.SubElement(newItem, "Notes")
        noteElement.text = notes
    elif input == "r\n":
        print("Enter name of task. Options include: ")
        for i in doc.findall('.//item'):
            print(i.get("name"))
        taskToRemove = stdin.readline()
        taskToRemove = taskToRemove[:-1]
        for i in doc.findall('.//item'):
            if i.get("name") == taskToRemove:
                list.remove(i)
    elif input == "x\n":
        print("Enter name of task. Options include: ")
        for i in doc.findall('.//item'):
            print(i.get("name"))
        taskToMark = stdin.readline()
        taskToMark = taskToMark[:-1]
        for i in doc.findall('.//item'):
            if i.get("name") == taskToMark:
                i.set("complete","y")  
    elif input == "d\n":
        printByDate()
    elif input == "e\n":
        editTask()
    elif input == "c\n":
        printCompleted()
    elif input == "n\n":
        printUncomplete()
    else:
        print("Quit.")
        done = 0
    doc.write('toDoList.xml',encoding="utf-8")

