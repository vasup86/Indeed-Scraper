# Indeed-Scraper

Searching for job posting on Indeed is a time-consuming experience to find the perfect posting. Each page has about 10 postings and finding a perfect positing can take a while. This project is an Indeed job posting scraper created using python and aims to solve this issue. The user enters their preferred job title, location, file name for the excel, and location and time to showcase revelant job positing. The application then takes these choices and generates an excel sheet with relevant job title, salary, company, job link and a brief description.

The projects is created using requests, Beautiful Soup, pandas and tkinter. Requests is used to get the HTML of the website, Beautiful Soup is used to search through the HTML and find revelant information, pandas is used to create an excel sheet and tkinter is used to develop the frontend GUI interface.<br/>

![Screenshot (304)](https://user-images.githubusercontent.com/83378929/147377316-71e23a56-df9c-4aee-a383-89b9495dbf63.png)
<br/>
The GUI is created using the tkinter library. The interface has multiple fields to find specific job title and/or location realted postings to scrape. Enter  prefered job title and/or location, file name, amount of pages to scrape, distance and positing date to get more revelant postings.
<br/>
<br/>
<br/>
![Screenshot (303)](https://user-images.githubusercontent.com/83378929/147377319-75d34231-2025-432b-83fd-035d8b9e01cd.png)
![Screenshot (302)](https://user-images.githubusercontent.com/83378929/147377321-acec6921-a111-466c-9f03-313229a06d58.png)
<br/>
The interface also allows the user to decide the distance and the posting date to get more accurate and recent result. 
<br/>
<br/>
<br/>

![Screenshot (301)](https://user-images.githubusercontent.com/83378929/147377326-9880297b-9686-4926-b38a-e89d8911ecc3.png)
Users can define the number of pages to scrape and the file is saved as an excel workbook in cwd and is titled the name defined by user in *File Name* field.
