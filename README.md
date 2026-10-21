# CopyCraft AI

### Automated Copywriting & Tone Transformer

CopyCraft AI is an AI-powered marketing content generation application developed for the **DecodeLabs Generative AI Industrial Training Program 2026**.

It generates professional marketing copy for LinkedIn, Instagram, and Email using Google Gemini.

## Features

- AI-powered marketing copy generation
- Platform-specific content for LinkedIn, Instagram, and Email
- Six writing tones
- Temperature and Top-P customization
- Pydantic structured-output validation
- Asynchronous batch generation
- CSV upload and download
- Session-based generation history
- Command-line interface using argparse
- Professional Streamlit dashboard

## Technology Stack

- Python
- Streamlit
- Google Gemini 3.5 Flash-Lite
- Pydantic
- Pandas
- asyncio
- argparse

## Installation

Clone the repository:

```bash
git clone https://github.com/humeesao126-pixel/CopyCraft-AI.git
cd CopyCraft-AI
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file:

```dotenv
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key.

## Run the Application

```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Command-Line Usage

```bash
python cli.py --product "Wireless Headphones" --description "Noise cancellation and 30-hour battery life" --platform Instagram --tone Exciting
```

## Batch Generation

Upload a CSV containing:

```csv
product_name,description,platform,tone
Wireless Headphones,Noise cancellation and 30-hour battery life,Instagram,Exciting
Smart Watch,Fitness tracking and heart rate monitoring,LinkedIn,Professional
```

The application supports concurrent generation with a limit of two simultaneous requests and exports results to CSV.

## Limitations

- Gemini API usage depends on model access and available quota.
- Generation history lasts only for the active Streamlit session.
- AI-generated marketing claims should be reviewed before publication.

## Future Improvements

CopyCraft AI v2.0 is planned to include a React and FastAPI architecture, a premium content editor, enhanced brand controls, content refinement, and persistent history.

## Developer

**Humeesa Obaid**

DecodeLabs Generative AI Industrial Training Program — 2026

**Version:** 1.0.0