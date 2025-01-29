
# Summify

A FastAPI-based document summarization service that supports both **extractive** and **abstractive** summarization. It allows users to upload documents (PDF or text files) and receive summaries based on their preferred summarization approach.

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [API Routes](#api-routes)
3. [How to Use](#how-to-use)
4. [Installation](#installation)
5. [Connect with Me](#connect-with-me)

---

## Project Structure

```
Summify/
├── src/                              
│   ├── assets/                       
│   │   └── test_cases/               
│   │       ├── nativepdf_ar.pdf
│   │       ├── nativepdf_fr.pdf
│   │       ├── scanned_ar1.pdf
│   │       ├── scanned_ar2.pdf
│   │       ├── scannedpdf_en.pdf
│   │       └── text.txt
│   ├── config/                       
│   │   ├── __init__.py
│   │   └── settings.py               
│   ├── controllers/                  
│   │   ├── __init__.py
│   │   ├── BaseController.py         
│   │   └── SummaryController.py      
│   ├── core/                         
│   │   ├── __init__.py
│   │   ├── file_parser.py            
│   │   └── summarizer.py             
│   ├── helpers/                      
│   │   ├── enums/                    
│   │   │   ├── __init__.py
|   |   |   ├── extraction_enums.py
|   |   |   ├── scan_enums.py
|   |   |   ├── summary_enums.py
|   |   |   └── validation_enums.py
│   │   ├── file_validation.py        
│   │   ├── lang_detection.py         
│   │   ├── scan_checker.py           
│   │   └── text_processing.py        
│   └── routes/                       
│       ├── __init__.py
|       ├── base.py
│       ├── summary.py                
│       └── schemas/                      
│           ├── __init__.py
│           └── upload_request.py                  
│                            
├── .env                              
├── .env.example                      
├── .gitignore                        
├── main.py                           
├── requirements.txt                  
├── LICENSE                           
└── README.md                         
```

---

## API Routes

### **Get `/welcome`**
For Welcome message

### **POST `/data/summary/file`**
Summarize a document (PDF or text file).

#### Request:
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `file`: The document to summarize (PDF or text file).
  - `summ_approach`: The summarization approach (`abstractive` or `extractive`).
  - `max_length`: The maximum length of the summary (required for `abstractive`).
  - `sentences_num` : The maximum sentence count of the summary (required for `extractive`).

#### Example Request:
```bash
curl -X POST "http://localhost:8000/data/summary/file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "summ_approach=abstractive" \
  -F "max_length=500"
```

#### Response:
```json
{
  "summary": "generated summary of the document..."
}
```

---

## How to Use

### 1. **Install Dependencies**
Make sure you have Python 3.8<  3.13> installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. **Run the Application**
Start the FastAPI server:

```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000`.

### 3. **Test the API**
You can use tools like **Postman** to test the API. Refer to the [API Routes](#api-routes) section for examples.

---

## Installation

### Prerequisites
- Python 3.8 - 3.12.8
- Pip (Python package manager)

### Steps
1. Clone the repository:

    ```bash
    git clone https://github.com/tawfikhammad/Summify.git
    cd Summify
    ```

2. Set up a virtual environment:

    ```bash
    conda create --name summify python=3.12.8
    conda activate summify
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    cd src
    python main.py
    ```

---

## Connect with Me

If you have any questions, suggestions, or just want to connect, feel free to reach out to me on LinkedIn:

👉 [Tawfik Hammad](https://www.linkedin.com/in/tawfikhammad)

Let’s connect and collaborate!

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
