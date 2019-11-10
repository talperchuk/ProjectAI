# **ProjectAI**
This project was made as part of Project in Artificial Intelligence course taken during my BSc in Computer Science in the Technion.
Our main goal was to learn the basics of weather prediction - using machine learning techniques such as linear regression, and what might be the impact of it in the future. 


_Project files_:
#### DataRetrival.py
Used for retriving data from the Israeli Meteorological Service API.

#### DataProcess.py
Used for processing the data retrieved.
* Creating DataFrames.
* Add features.

#### GetChannels.py
Used for converting features name to its API id number.

#### LocationBasedDataProcess.py
Used for creating data from multiple stations. 

#### findFeaturesScript.py
Used for finding all features combinations for each regressor.

#### mainScript
Used for finding best parameters for each regressor, based on findFeaturesScript.py results.

#### main.py
Contains examples of code usages. 

#### PredictTempTechnion.py
Used for testing Technion's final model.

#### libs.txt
Contains all packages which were used within the project development environment.


