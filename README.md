# 📄 Indeed Job Scraper (Python + Playwright)

A Python-based scraper for [Indeed](https://www.indeed.com) built with **Playwright**.  
It extracts job listings with details such as job title, company, location, posting date, description snippet, and job URL — and saves results in **CSV** format.  

---

## 🚀 Features
- Input parameters: **designation**, **skills**, **location**
- Scrapes multiple pages with **pagination**
- Extracts:
  - Job title  
  - Company name  
  - Location  
  - Posting date  
  - Job description snippet  
  - Job URL  
- Anti-bot measures:
  - Rotating **User-Agent** strings  
  - Configurable wait times  
- Clean, modular Python code  
- Export results to **CSV** (ready for Excel, Pandas, or BI tools)

---

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/UMAR6545/job-scraper.git
   cd jobs-scrapper-playwright
   
2. Create a virtual environment (recommended):
    ```bash
      python -m venv venv
      source venv/bin/activate   # Mac/Linux
      venv\Scripts\activate      # Windows
    ```

3. Install dependencies:
    ```bash
      pip install -r requirements.txt
    ```

4. Install Playwright browsers:
    ```
    playwright install
    ```

## ▶️ Usage

Run the scraper with default values:
```
  python runner.py --site all --designation "python" --skills "python sql" --location "Lahore" --out results.json
```
  


