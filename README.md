## Business statement:
The inputs of various sensors for different wafers have been provided. In electronics, a wafer (also called a slice or substrate) is a thin slice of semiconductor used for the fabrication of integrated circuits. The goal is to build a machine learning model which predicts whether a wafer needs to be replaced or not (i.e. whether it is working or not) based on the inputs from various sensors. These are two classes: +1 and -1.
+1: Wafer is in a working condition, doesn’t need to be replaced
-1: Wafer is not in a working condition, do need to be replaced

## Solution Proposed 
In this project, The goal is to build a machine learning model which predicts whether a wafer needs to be replaced or not (i.e. whether it is working or not) based on the inputs from various sensors. These are two classes: +1 and -1.
+1: Wafer is in a working condition, doesn’t need to be replaced
-1: Wafer is not in a working condition, do need to be replaced

The problem is to identify which sensor need to replace and which sensor doesn't need to replace. reduce the cost due to unnecessary replacement. So it is required to minimize the false predictions.

## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS IAM
2. AWS ECR
3. AWS App Runner
4. Git Actions

## How to run?
Before we run the project, make sure that you are having AWS account. We are using AWS services such as IAM, ECR, App Runner. For detailed guidance to run the project kindly follow the documentation/LLD.

## Project Architecture
![Project Architecture.jpg](documentation%2Futils%2FProject%20Architecture.jpg)

## Functional Architecture
![Functional Architecture.jpg](documentation%2Futils%2FFunctional%20Architecture.jpg)

## Technical Architecture
![Technical Architecture.jpg](documentation%2Futils%2FTechnical%20Architecture.jpg)

## Clone the repository
```bash
https://github.com/bhagwat-chate/wafer_fault_detection.git
```
### Step 2- Create a conda environment after opening the repository

```bash
conda create -n wafer python=3.8.15 -y
```

```bash
conda activate wafer
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Export the environment variable
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

export MONGODB_URL="mongodb+srv://<username>:<password>@ineuron-ai-projects.7eh1w4s.mongodb.net/?retryWrites=true&w=majority"
```

### Step 5 - Run the application server
```bash
python app.py
```

### Step 6. Train application
```bash
http://127.0.0.1:5000
```

### Step 7. Prediction application
```bash
http://127.0.0.1:5000
```

## Run locally

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION> --build-arg MONGODB_URL=<MONGODB_URL> . 
```

3. Run the Docker image
```
docker run -d -p 8080:8080 <IMAGE_NAME>
```

