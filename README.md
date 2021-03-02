# Canadian Open Address Point Processing (COAPP)

This is the project directory containing the scripts needed to download, process, and produce the Open Database of Addresses (ODA).

The script and documentation are part of work in progress and subject to continuous development. The technical documentation is available in English only.

# Traitement des points d'adresse ouverts au Canada (TPAOC)

Voici le répertoire pour les scripts nécessaires afin de télécharger, traiter et produire la Base de données ouvertes d'adresses (BDOA).

Le script et la documentation font partie du travail en cours et font l'objet d'un développement continu. La documentation technique est disponible en anglais uniquement.

--------

The COAPP scripts are run on Statistics Canada's Advanced Analytics Workspace (AAW), a cloud environment with Jupyter notebook servers, Kubeflow pipelines, and MinIO storage. 

The basic workflow is

1. Collect data and perform basic processing with a modified version of the OpenAddresses () processing pipeline, integrated into a Kubeflow pipeline.
2. Pass the individual CSVs produced in step 1 to a series of four Python scripts that perform:
   *  Processing of street names, types, and directions into standard forms in new columns, and infer city names where missing in the original data,
   *  Remove records with missing coordinates or street names, and truncate geocoordinates to five decimal points and deduplicate address points,
   *  Spatially join address points with Statistics Canada Census Subdivision (CSD) boundary files to determine the CSDs of the address points,
   *  Merge all sources into one file, perform a second deduplication step, and assign unique identifiers and group identifiers.

The final output is a single Canada-wide address file, as well as separate files produced for each province and territory where data is available.
