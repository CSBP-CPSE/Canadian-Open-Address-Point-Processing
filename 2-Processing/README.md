These are the scripts developed for post processing the data after collection with the modified OpenAddresses pipeline. In most cases, the Python scripts process a single source, and there is therefore also a Python notebook to build a shell script to automate running the code for every source.
All the sources used, and the date they were downloaded, is stored in the valid sources excel sheet.
In a future update, the sources file will be changed from an Excel sheet to a CSV, and will be automatically updated when the collection pipelines are run so that the date column can show the most recent download of the data without the user needing to update the file themselves.

Additionally, in a future update the processing scripts will be wrapped into a Kubeflow pipeline for convenience, but in the meantime they can be run with the help of the shell scripts and shell-script-generating Python functions.

To run these scripts on the Advanced Analytics Workspace, it is necessary to create a new Conda environment and install the dependencies. 

To install the necessary dependencies, the following commands can be run in a terminal:

```
bash
conda create --name process
conda activate process
conda install geopandas xlrd openpyxl 
```

For the standardisation script, the modified version of RASK also needs to be installed. To do this, navigate to the modified-rask-python-master folder, and run

```
python setup.py install --user
```

