# pdf_visualisation
Visualisation of Samsung 2018 Catalogue using Python and Dash
This tool uses Python to visualise the energy consumption of electrical applications from Samsung's 2018 catalogue(https://image-us.samsung.com/SamsungUS/samsungbusiness/samsung-builder/pdfs/Samsung_Home_Appliances_2018_Product_Catalog.pdf). It calculates the prices using Kenya's Domestic Consumption price in October 2022(https://www.stimatracker.com/historic). A web scrapper function creates a data frame of the historical cost per KilowattHour. The price data frame is passed onto the main pdf visualization file. Graphs are generated using Dash.
![image](https://user-images.githubusercontent.com/57504251/199781375-ebf4be12-ad3e-4f19-9ae3-67e2141ce89b.png)
