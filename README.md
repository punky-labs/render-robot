![Robot Render Logo](https://cdn.myportfolio.com/e297cf82-f515-476d-ab0e-bf9fc0fb3342/0e830878-2385-4b0b-a156-bbd9ca10c35b_rw_1920.png?h=463de7de87dbe7e1c2881942c4be4a80)

Robot Render is A GUI that facilitates After Effects comp rendering automation. 

Robot Render uses the After Effects command line renderer to render a queue of After Effects compositions. It is built for After Effects compositions using an external CSV file to dynamically update fields within its compositions. Using a secondary file containing variations, it will update the base CSV file before rendering each variation.

![Example Robot Render UI](https://cdn.myportfolio.com/e297cf82-f515-476d-ab0e-bf9fc0fb3342/e69399e0-251a-4393-a6df-84a4d099d08b_rw_1920.png?h=561719b5a17c86d66147f38161081077)

## How to use
(The sample files included with the download are helpful)
### Step 1
Set up your Afte Effects comp to use a CSV file as the data source. The link below explains this really well. Before running Robot Render, ensure all your linking works, and you can do a single test render from within the After Effects render queue.
### Step 2
Create a CSV file with the same setup as your original settings file but with extra rows containing all the file variations you would like.
### Step 3
Fire up Render Robot and fill in the information below.
#### After Effects Project
This should point to your base After Effects file. 
#### Project Settings File
This is the base CSV file that you created and tested in Step 1
#### Variations File
This is the file that you created in Step 2. This can be a local CSV file or point to an online URL. Note that the online URL must be a CSV file. See below for instructions on creating a CSV URL for a Google Sheet.
#### After Effects Composition
This is the name of the composition within your After Effects file. You can either enter the name manually or have a column in your variations file that lists the composition name. This allows you to render more than one composition in one run.
#### Output folder
This should point to where you would like your final renders.
#### File Naming
The first option lets you create a programmatically generated name for each file. Note that the extension is not detected from the output module, so it will be created as selected.
The second option lets you use a column in your variations file to set the file name.
#### Output Module
This field uses a column in your variations file to set the After Effects Output Module with which the file will be rendered. 
#### After Effects Folder
This field should point to the location of your base After Effects Installation. It should be the folder that contains the 'aerender.exe' file.​​​​​​​
## Creating an online CSV link for Google Sheets.
Within your Google Sheet, select File > Share > Publish to Web
Staying in the 'Link' tab, select the name of your Sheet, and select the option 'Comma-separated values (.csv)'
Select 'Publish'
You will be given a URL ending with '&output=csv.' 
