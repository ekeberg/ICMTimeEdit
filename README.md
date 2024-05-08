# Installing the software
1. run `pip install .`

# Downloading TimeEdit data

1. Log in to TimeEdit and choose "Schedule".
2. In the search box, change the dropdown list from "Course" to "Staff"
3. In the box "Institution" choose "152 Cell- o molekylärbiolog".
5. Click the box that says "Add: Staff: 152_Cell- o molekylärbiologi". This will add the criteria to your search box.
6. Click "Show schedule". This will bring up a TimeEdit schedule for all teaching by ICM staff.
7. Select the range that you want to download in the top-left view changer. Select for example 2023-01-01 to 2023-12-31.
8. From the "Download" menue, select "Excel (xlsx)"
9. You can leave the options as they are and click "Create Excel (xlsx)". This should start the download.

# Downloading a list of all employees per research program
1. After installing these tools you can run `icm_download_names OUTFILE` to parse the ICM home page for all names listed under each research program. (IMPORTANT: This does not work since the hompage was updated)
2. Then run `icm_save_program_tables PEOPLE_FILE TIME_EDIT_FILE OUTDIR` to generate an excel file per program containing a summary of the teaching hours per person.

# 


