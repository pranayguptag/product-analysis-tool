🛒 Product Analysis Tool

Product Analysis Tool is a Flask-based web application that allows users to search products across Amazon, Flipkart, and Myntra, analyze product details and pricing, store data in a SQLite database, and visualize insights with interactive plots.

The tool is designed to make e-commerce product comparison simple, fast, and visually appealing.

✨ Key Features

🔍 Multi-Platform Search → Search products on Amazon, Flipkart, and Myntra

🗂️ Database Integration → Save all results into SQLite for structured access

📊 Visual Analytics → Compare prices and analyze insights with interactive plots

📥 Downloadable Reports → Export results to CSV for further use

🎨 Modern UI → Built with TailwindCSS, responsive, and user-friendly

⚡ Automation Ready → Scraping runs automatically when user searches

📂 Project Structure
product-analysis-tool/
│
├── app.py                 # Flask entry point
├── Scraper.py             # Core scraping logic (Amazon, Flipkart, Myntra)
├── models.py              # SQLite DB models
├── requirements.txt       # Python dependencies
├── templates/             # HTML Templates
│   ├── base.html          # Common layout
│   ├── home.html          # Home/Search page
│   ├── products.html      # Products table page
│   └── visuals.html       # Visualization/plots page
├── README.md              # Documentation
└── LICENSE                # Open-source license

🛠️ Tech Stack

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, TailwindCSS

Scraping: BeautifulSoup, Requests

Visualization: Matplotlib, Pandas

🚀 Getting Started

Follow these steps to run the project locally:

1️⃣ Clone the Repository
git clone https://github.com/pranayguptag/product-analysis-tool.git
cd product-analysis-tool

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Locally
python app.py


App will be live at → http://127.0.0.1:5000

🖼️ Screenshots
🔎 Home Page

Users can search and select platforms (Amazon, Myntra, Flipkart)


📋 Product Results

Clean tabular view of products scraped from platforms


📊 Visual Analysis

Compare product prices and insights visually


🎥 Demo Video

📹 Click here to watch demo

👨‍💻 Author

Pranay Gupta

🎓 B.Tech Student @ NIET, Greater Noida

🌐 LinkedIn

💻 GitHub

🙏 Acknowledgements

This project was made possible thanks to:

Flask
 – lightweight web framework

TailwindCSS
 – for modern UI design

Matplotlib
 & Pandas
 – for analysis & visualization

BeautifulSoup
 – for scraping product data

Special thanks to OpenAI ChatGPT for technical assistance and guidance during development

📜 License

This project is licensed under the MIT License – see the LICENSE
 file for details.