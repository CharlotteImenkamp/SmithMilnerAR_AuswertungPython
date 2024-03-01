# Evaluate Visuoconstruction

The application contains all the necessary scripts for analysing the data.

## Folder
- "evaluation_python\Data":  
	Required .json and .xlsx files for analysis
	Each new data set must be assigned a new id, which does not yet exist in the folder structure. 
	To add a new data set to one for analysis, a new subfolder User*id* (analysis_python\Data\User*id) 
	must be created and the files to be analysed must be saved in it. 
	The required files are the outputs of the Unity application, which are accessible in the Windows Device Portal.
	The names of the files are: EndObjectLocations*id*, HeadDataLocations*id*, HeadDataPrices*id*, MovingObjectLocations*id*, StartLocationPrices*id* 
	and StartObjectLocations*id*. In the last step, the ID in the main file must be added to the variable "allIDs" (line 16).
	
	
- "Results": Results of the analysis in .png or .xlsx format. The files are created by the application

## Scripts
- Load:
    - Load the start and end positions of the objects to calculate the absolute and relative error
- AbsoluteError: 
    - Images of the positioning of each subject
    - Absolute error distances, as well as their mean values and standard deviations
- RelativeError:
    - Diagram and direct neighbours according to Voronoi (output: image)
    - Diagram and direct neighbours according to Delaunay (output: image)
    - Relative error using quadrant comparison (output: Excel file)
- Rotations / Times: 
    - Differences in rotation and times
    - Results in Excel file
- ObjectMovement / HeadDirections: 
    - Reading and visualisation of the corresponding .json files 
- Test battery: 
    - Calculation of mean value and standard deviations of the neuropsychological test battery
    - uses class "NeuroData" 
    - Visualisation of the groups using boxplots




