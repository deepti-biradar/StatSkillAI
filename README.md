\# StatSkillAI



An AI-powered skill development and progress-tracking application built using Python, Streamlit, and Google's Gemini API.



\## About the Project



StatSkillAI provides an interactive platform for skill development and progress tracking, using AI-driven assistance to support users in their learning journey.



\## Tech Stack



\- \*\*Programming Language:\*\* Python

\- \*\*Frontend:\*\* Streamlit

\- \*\*AI Integration:\*\* Google Gemini API

\- \*\*Data Storage:\*\* JSON



\## Features



\- Interactive Streamlit application

\- AI-powered assistance using Gemini

\- Progress tracking

\- User-friendly interface



\## Project Structure



```text

StatSkillAI/

├── app.py

├── background.jpg.jpg

├── progress.json

├── requirements.txt

├── .gitignore

└── .streamlit/

&#x20;   └── secrets.toml.example

```



\## Installation and Setup



1\. Clone the repository:



&#x20;  ```bash

&#x20;  git clone https://github.com/deepti-biradar/StatSkillAI.git

&#x20;  cd StatSkillAI

&#x20;  ```



2\. Install dependencies:



&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



3\. Create `.streamlit/secrets.toml` and add your Gemini API key:



&#x20;  ```toml

&#x20;  GEMINI\_API\_KEY = "your\_api\_key\_here"

&#x20;  ```



4\. Run the application:



&#x20;  ```bash

&#x20;  streamlit run app.py

&#x20;  ```



\## Environment Variables



The application requires a Gemini API key. Keep your actual API key private and never commit your `secrets.toml` file.



\## Author



\*\*Deepti Biradar\*\*



GitHub: \[@deepti-biradar](https://github.com/deepti-biradar)

