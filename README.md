# Amharic E-commerce Data Extractor
This project ingests raw messages from Ethiopian Telegram e-commerce channels, cleans & normalises Amharic text, and structures the output so that downstream models (e.g. entity-extractors or LLM fine-tuning pipelines) can discover seller insights.

```text
├── fetch/              # CLI entry-points & quick scripts
├── src/                # Importable Python modules
│   ├── core/      # Telegram fetching logic
│   ├── utils/          # Shared helpers (text prep, IO)
│   ├──services 
│   └── config.py       # Paths & environment variables
├── notebooks/          # Exploratory notebooks
├── scriptss/          # Executable scripts
├── data/
│   ├── raw/            # Appended JSONL straight from Telegram
│   └── processed/      # Tokenised / cleaned records
├── requirements.txt
└── .env.example        # Fill with your Telegram API creds
```

## Environment setup
1. Clone the repo and create a virtual environment (recommended)
   ```bash
   git clone https://github.com/Naod-Mergiya/Amharic-E-commerce-Data-Extractor.git
   cd Amharic-E-commerce-Data-Extractor
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```
2. Install runtime requirements
   ```bash
   pip install -r requirements.txt
   ```
   Extra tooling used in notebooks can be installed at any time:
   ```bash
   pip install regex conllu jupyter
   ```
3. Obtain Telegram API credentials
   • Go to <https://my.telegram.org/apps> and create an application.  
   • Copy `api_id` and `api_hash`.
4. Configure credentials
   ```bash
   cp .env.example .env
   # then edit .env and fill TELEGRAM_API_ID, TELEGRAM_API_HASH, (optional) PHONE_NUMBER
   ```

## Quick start
1. Install deps
```bash
pip install -r requirements.txt
```
2. Copy `.env.example` → `.env` and fill `TELEGRAM_API_ID` & `TELEGRAM_API_HASH` (grab from [my.telegram.org](https://my.telegram.org)).
3. Run the ingestor with at least five channel handles:
```bash
python fetch/run_ingestion.py channel1 channel2 channel3 channel4 channel5
```
Messages are appended to `data/raw/<channel>.jsonl` as they arrive.

Feel free to share the collected JSONL files amongst the team—more data means better fine-tuning.

## Task 2 – Generate a labelled CoNLL subset
This step converts a small slice of the raw messages into tab-separated CoNLL (`token\ttag`) format so you can inspect rule-based entity labels or bootstrap an NER model.

### Requirements
```
pip install regex conllu
```
`regex` is used by the text tokenizer and `conllu` is only needed if you want to parse the file back into Python objects for analysis.

### Run from the command line
```
python -m src.labeling.conll_labeler
```
• If `data/preview_messages.csv` doesn’t exist the script writes a 1-row placeholder so the pipeline still runs.
• The output is written to `data/labels/subset.conll`.

### Run inside the notebook
Open `notebooks/labeling_demo.ipynb`. The first cell automatically:
1. Locates the repo root and fixes `sys.path` so `import src.…` works anywhere.
2. Creates a placeholder CSV if the preview file is missing.
3. Executes the labelling module.
4. Prints the first 60 lines of `subset.conll` and, if `conllu` is installed, parses the file and reports sentence & token counts.

### Entities currently covered
| Tag        | Example tokens            |
|------------|---------------------------|
| B-PRICE    | `2700`, `150`, `90 birr`  |
| B-LOC      | `ቦሌ`, `Bole`, `Megenagna` |

Future work: add PRODUCT, MATERIAL, DELIVERY_FEE and CONTACT_INFO entity detectors.

---

## Commit conventions
We follow the Conventional Commits style to make the history readable and automate release notes:
```
<type>(optional scope): <short summary>

[optional body explaining *why* and any context]
```
Common `<type>` values: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.  Example:
```
feat(labeling): add DELIVERY_FEE entity detector
```
Please write imperative, present-tense summaries no longer than 72 chars.
