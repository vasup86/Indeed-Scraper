import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urljoin
from tkinter import *   # * means import everything
from PIL import ImageTk, Image
import pandas as pd

def interface():
    global root
    root = Tk()
    root.geometry("750x500")
    root.resizable(0,0)
    root.configure(bg="white")
    root.title("VP - Indeed Scraper")
    title = Label(root,bg="white", text="Scraper", font="arial 25 bold")
    title.place(x=360,y=10)
    image = Image.open(r'c:\Users\vasu0\Downloads\indeed-logo.png')
    image = image.resize((150,35), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    logo_pic = Label(root, image=img)
    logo_pic.place(x=200, y=10)

    jobTitle= StringVar()
    Label(root, text="Job Title", bg="white", font="arial 15").place(x=60,y=60)
    job_enter = Entry(root,bg="#F7FEF9", width=70, textvariable=jobTitle).place(x=165, y=65)

    #location need to be in Toronto, ON format 'city, state(2 letters caps)'
    location = StringVar()
    Label(root, text="Location",bg="white", font="arial 15").place(x=60,y=90)
    location_enter = Entry(root,bg="#F7FEF9", width=70, textvariable=location)
    #location_enter.insert(0,"Ex: Toronto, ON")
    location_enter.place(x=165, y=95)

    fileName = StringVar()
    Label(root, text="File Name",bg="white", font="arial 15").place(x=60,y=120)
    file_enter = Entry(root,bg="#F7FEF9", width=40, textvariable=fileName).place(x=165, y=125)

    pages = IntVar()
    Label(root, text="Pages",bg="white", font="arial 10").place(x=430,y=123)
    pages_enter = Entry(root,bg="#F7FEF9", width=5, textvariable=pages).place(x=480, y=125)

    #dropdown menu for location
    distanceOptions = ['Distance in KM', 'Exact', '5','10', '15','25','50', '100']
    distance= StringVar(root)  
    distance.set(distanceOptions[0])
    distance_enter = OptionMenu(root, distance,*distanceOptions)
    distance_enter.config(width=10, font=('arial 7'),bg='white')
    distance_enter.place(x=163, y=150)

    #dropdown menu for time
    timeOptions = ['Date Posted', '24 hrs', '3 days','7 days', '14 days']
    time = StringVar(root)  
    time.set(timeOptions[0])
    time_enter = OptionMenu(root, time,*timeOptions)
    time_enter.config(width=10, font= ('arial 7'),bg='white')
    time_enter.place(x=275, y=150)

    #since extract requires argument, we need to use lambda expression
    Button(root, text="Go", font='arial 25 bold', bg='#F7E7CE', padx=2, command=lambda: backend(jobTitle.get(),location.get(),fileName.get(),pages.get(), distance.get(), time.get())).place(x=300, y=250)
    root.mainloop()

# where the backend process starts and finishes
def backend(jobTitle, location, fileName, pages, distance, time):
    #its only upto pages since 0 is pg: 1
    #url changes at the end by, 0=pg1,  &start=10 (pg 2), &start=20 (pg 3), etc  
    #key words: software developer, use .replace(" ", "+"), to replace jobtile space " " with +
    #location: (place)%2C+(state(2 letter)) ex: Toronto, ON
    url = 'https://ca.indeed.com/jobs?q='
    combUrl = url + (jobTitle.replace(" ", "+")) + "&l=" + (location.replace(", ", "%2C+"))
    
    time = time[:1]  #only first index since other days contains space in index 2
    try:
        time = int(time)
    except:
        time = 'D'
    if(distance == 'Exact'):
        distance=0
    if(time == 1): #for 14 days
        time = 14
    elif(time == 2): #for 24 hrs
        time = 1

    if(distance== "Distance in KM" and time == 'D'):   #neither is selected
        for i in range(0, (pages*10), 10): #(0 to 30 in step of 10)
            c = extract(i, combUrl) # i is the page # of the url search
            transform(c)
    elif(distance!="Distance in KM" and time=='D'):   #only distance is selected
        #distance: &radius=(#of km), exact=0
        combUrl = combUrl + "&radius="+ str(distance)
        for i in range(0, (pages*10), 10): #(0 to 30 in step of 10)
            c = extract(i,combUrl) # i is the page # of the url search
            transform(c)
    elif(distance=="Distance in KM" and time!='D'): #only time is selected
        #time: &fromage=(time), 24 hr = 1
        combUrl = combUrl + "&fromage=" + str(time)
        for i in range(0, (pages*10), 10): #(0 to 30 in step of 10)
            c = extract(i,combUrl) # i is the page # of the url search
            transform(c)
    else:    #if both are selected
        combUrl = combUrl + "&radius="+ str(distance) + "&fromage=" + str(time)
        for i in range(0, (pages*10), 10): #(0 to 30 in step of 10)
            c = extract(i,combUrl) # i is the page # of the url search
            transform(c)
    

    #save the found items in a excel file
    fileName = fileName + ".xlsx"
    df = pd.DataFrame(joblist)
    df.to_excel(fileName)
    #print(len(joblist))

    #display file saved message 
    timed_complete = Label(root,bg="white", text="File Saved", font="arial 20 bold")
    timed_complete.pack()
    timed_complete.place(x=275, y=350)
    root.after(2000, timed_complete.destroy) #destory label after 2 seconds
    joblist.clear()  #clear the list of jobs after its stored in pandas
    
def extract(page, combUrl):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    #{}, .format is for the the page# 
    combUrl = (combUrl+ "&start={}").format(page)
    print(combUrl)
    r = requests.get(combUrl, headers)
    soup = BS(r.content, "lxml")
    return soup

def transform(soup):
    #divs = soup.find_all('div', class_ = 'jobsearch-SerpJobCard')  #basic class name for each job post shell
    divs = soup.find_all('a', class_ = 'tapItem')  #basic class name for each job post shell
    linkJob = []
    i=0
    #links to indeed job posting
    for job in soup.select('.result'):
            #(job.select_one('.jobTitle').get_text(' '))
            #extract 'data-jk' from main 'a' tag: and add it to this link 
            link = (f'https://ca.indeed.com/viewjob?jk={job["data-jk"]}')
            linkJob.append(link)
            
    for item in divs:
        urlMain = "https://ca.indeed.com"

        #title = item.find('a').text.strip()  #class title, is an 'a' tag, and has title as text
        title = item.find('h2', class_ = 'jobTitle').text.strip('').replace('new', '') #class jobTitle, is an 'h2' tag, and has title as text
        print(title)

        #company = item.find('span', class_ = "company").text.strip()
        company = item.find('span', class_ = "companyName").text.strip()

        #links to indeed job posting
        #people = item.find_all('h2', class_ = 'title')
        # for i in people:
        #     for link in i.find_all('a', href=True):
        #         linkJob =  urlMain + link.get('href')
    

        #since salary is not there for every job, trial it
        try:
            #salary = item.find('span', class_ = "salaryText").text.strip()
            salary = item.find('span', class_ = "salary-snippet").text.strip()
        except:
            salary = ' '

        #summary = item.find('div', class_ = "summary").text.strip().replace('\n', '')
        summary = item.find('div', class_ = "job-snippet").text.strip().replace('\n', '')
        job = {
            'title': title,
            'company': company,
            'salary': salary,
            'jobLink':linkJob[i],  #use i as a ref for which itteration of for loop is on, and insert the link accordingly
            'summary': summary
        }
        joblist.append(job)
        i+=1
        
joblist = []
interface()