# Splunk2Hive

## Index
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Future Improvements](#future-improvements)

## Overview

Splunk2Hive is a powerful integration tool designed to streamline cybersecurity incident management. It connects Splunk and TheHive, enabling seamless alert handling and case creation. When an alert is triggered in Splunk, this project collects the last triggered alert, creates an alert in TheHive, and generates a case. The case description is automatically enriched using Llama3 AI, providing insightful context for incident response.

Key Note: When you run the code, it will collect the last alert from Splunk and process it accordingly.

## Features

+ Alert Collection: Automatically fetches the most recent alert triggered in Splunk.
+ TheHive Integration: Creates an alert in TheHive based on Splunk data.
+ AI-Powered Descriptions: Utilizes Llama3 to generate detailed and meaningful case descriptions.
+ Incident Management: Promotes TheHive alerts to cases for efficient tracking and resolution.
+ Streamlined Workflow: Helps organizations manage and respond to cybersecurity incidents effectively.

## Technologies Used

+ Programming Language: Python
  
+ **Tools & Platforms:**

    + Splunk: For alert generation and monitoring.
    + TheHive: For case management and incident response.
    + TheHive4Py: Python client for interacting with TheHive API.
    + Splunk-SDK: Python SDK for Splunk integration.
    + Llama3: AI model for generating enriched case descriptions.
 

## Setup Instructions

**Step 1: Prerequisites**

Ensure you have the following installed:

  + Python 3.8 or later
  + Splunk
  + TheHive
  + ollama 
  
**Step 2: Clone the Repository**
```
git clone https://github.com/kaykRodr1gu3s/Splunk2Hive.git
cd Splunk2Hive
```

**Step 3: Install Required Libraries**
Install the necessary Python dependencies using pip and [poetry](https://python-poetry.org/) 
```
pip install poetry
poetry add splunk-sdk
poetry add "thehive4py>=2.0.0b"
poetry add ollama
poetry add langchain_ollama
poetry shell
```

**Step 4: Configure Environment Variables**
Create a .env file in the project root and configure the required environment variables:
```
splunk_host = "splunk-host"
splunk_token ="Splunk-Token"
slack_webhook = "slack-webhook"
slack_channel = "slack-channel"
thehive_api= "thehive-api"
thehive_endpoint = "thehive-endpoint"
```

**Step 5: Run the Application**

```
python main.py
```

## Usage

Once the application is running:

1- Trigger an alert in Splunk: The project will automatically collect the alert.
2- Create alerts in TheHive: Alerts from Splunk will be synced and transformed into actionable alerts in TheHive.
3- Generate cases: Alerts are promoted to cases in TheHive with AI-generated descriptions.


**Example Output:**


![image](https://github.com/user-attachments/assets/2f1a9619-88e4-4146-bc6d-42b3b2d98962)

---

## Future Improvements

+ Automated Alert Handling: Enable the project to automatically process alerts as soon as they are triggered in Splunk, without needing to manually run the script.
+ Advanced AI Descriptions: Utilize Llama3 for even richer and more context-aware descriptions.
