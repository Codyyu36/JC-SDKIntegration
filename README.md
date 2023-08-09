# JC-SDKIntegration

Welcome to JC-SDKIntegration, a project designed to enhance the integration of JC's software development kit (SDK) using Python 3.8.

## Getting Started

To get started, follow these steps:

1. Download the Code: Obtain the PyQt5Demo code from the repository.
2. Set Up a Virtual Environment: It's recommended to use Python 3.8. Set up a virtual environment to manage dependencies.
3. Activate the Virtual Environment: Activate the virtual environment you've created to isolate dependencies.
4. Install Dependencies: Install the required dependencies by executing either of these commands:

   ```shell
   pip install -r pip_requirements.txt

   conda create --name <env> --file conda_requirements.txt


## SDK Integration Workflow

The following steps outline the workflow for integrating the Camera and Pattern Generator software development kits (SDK):

1. PG Software Setup: Open the PG software and submit all relevant images into the PG software for processing.
2. Camera Software Configuration: Open the Camera software. First, click "Disconnect" to ensure the camera is properly uninitialized.
3. Run IntegrationRunner.py: Execute the IntegrationRunner.py script to initiate the workflow. This script takes in test1.csv, so make sure to include that file in the directory as argument. A sample test1.csv file has been included in this repository for reference.

## Data Analysis

If you're interested in data analysis, RGB Filter.ipynb provides comprehensive scripts. Simply open the notebook to delve into data analysis capabilities.
