
## :information_source: Overview

The Quiz Maker takes input in .PDF, .TXT, or .DOCX format such as notes, lecture slides, textbook readings, and more. Once the file is uploaded, it is analyzed by Google Gemini AI and generates a multiple choice quiz based on the content of the uploaded document. 

## :book: How it works

- Running the program prompts the user to upload a file. The user is only able to pick files with .PDF, .TXT, or .DOCX file extensions as specified above. If no file is selected before continuing, an error message is displayed. 
- The user is asked to enter a number greater than 0 and less than 40. This corresponds to the number of multiple-choice questions that will be generated. If no number is entered before continuing, an error message is displayed. 
- A prompt is sent to Google's Gemini AI instructing it to generate a quiz in a specified multiple choice format based on all text extracted from the uploaded document. 
- Once the quiz is generated, the questions are displayed on screen. Clicking the incorrect answer highlights it in red, while clicking the correct one highlights it green. 
- The questions and answers generated in the quiz can be downloaded from this same page in either .PDF or .TXT format.

## :arrow_down_small: Installation

Install `Quiz Maker` and run `app.py`

To run tests, install the following packages:

```bash
pip install python-dotenv
```
```bash
pip install flask
```
```bash
pip install fpdf
```
```bash
pip install google.generativeai
```
```bash
pip install pdfplumber
```
```bash
pip install python-docx
```


## :key: Environment Variables

Obtain a Google Gemini API key from https://ai.google.dev/

To run this project, you will need to assign your  API key to the  `GEMINI_API_KEY` environment variable in `.env`


## :camera: Screenshots

1. Choose a file and enter number of questions.

![Pic 1](https://raw.githubusercontent.com/haiderwaheed/Quiz-Generator-Using-Machine-Learning/refs/heads/main/Screenshots/Capture0.PNG)

2. Select an answer - which will then be shown as correct or incorrect.

![Pic 2](https://raw.githubusercontent.com/haiderwaheed/Quiz-Generator-Using-Machine-Learning/refs/heads/main/Screenshots/Capture1.PNG)
