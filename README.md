# Dental Insurance Verification AI Agent

## Introduction

An AI-powered system that automates dental insurance verification processes, capable of handling real-time conversations, accent variations, and data extraction. The system reduces verification time from 
14 minutes to near real-time processing while helping prevent claim denials.

## Quicklinks

* [Blog Post](https://nycdatascience.com/blog/student-works/the-smart-solution-to-health-insurance-verification-ai-powered-intelligence/)

## Industry Challenges & Impact

The healthcare industry faces significant verification challenges:

* Insurance denials are increasing for 70% of providers, with 27% of denials related to registration and eligibility issues. The system addresses these challenges by automating verification,
  potentially saving the industry $12.8 billion.

* Current industry statistics show concerning trends:
  * 90% of claim denials are preventable, yet denial rates average 8-10%
  * Denials constitute approximately 20% of practice expenses
  * Each claim resubmission costs between $25-$118
  * 65% of denied claims are never resubmitted
  * 69% of practices report increased denials, averaging a 17% increase
  * Manual verification requires up to 14 minutes per transaction

## System Architecture

![Dental Insurance AI Agent Architecture](https://github.com/newking9088/dental_office_ai_agent/blob/main/ai_agent_architecture.png)

*Figure 1: High-level architecture diagram of the Dental Insurance AI Agent showing the interaction between speech processing, NLP, and verification components*

### Core Components

1. **Speech Recognition**
   * Leverages OpenAI Whisper for accurate transcription
   * Handles diverse accents and speech patterns

2. **Natural Language Processing**
   * Implements Gemini LLM for context understanding
   * Processes complex insurance-related queries

3. **Text-to-Speech**
   * Utilizes Coqui TTS for natural speech output
   * Provides clear, understandable responses

4. **Accent Handling**
   * Employs FAISS vector database for semantic search
   * Performs real-time accent correction
   * Uses HuggingFace Instruct Embeddings
   * Provides confidence scores for corrections

5. **Data Processing**
   * Generates structured JSON output
   * Integrates with PostgreSQL databases

## Project Structure

```
dental_office_ai_agent/
├── .env                       # Environment variables
├── .gitignore                 # Git ignore rules
├── api_key_example.env        # Example API keys template
├── concepts_and_goals         # Project documentation (16 KB)
├── correction_lookup          # Accent correction data (36 KB)
├── correction_lookup_with_faiss # FAISS-based correction data (19 KB)
├── dental_ai_notebook         # Jupyter notebook with examples (215 KB)
├── flow/                      # Conversation flow management (13 KB)
├── insurance_qa_sample        # Insurance QA templates (8 KB)
├── llm/                       # LLM integration (1 KB)
├── main.py                    # Main application entry (10 KB)
├── requirements.txt           # Python dependencies (9 KB)
├── stt/                      # Speech-to-text processing (2 KB)
├── test/                     # Test files (141 KB)
├── tts/                      # Text-to-speech processing (2 KB)
├── utils/                    # Utility functions (12 KB)
└── verification/             # Verification logic (19 KB)
```

## Installation & Setup

### Prerequisites

* Python 3.10 or higher (Recommended Python 3.10)
* Working microphone
* System-specific audio processing libraries

### System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev
```

#### MacOS
```bash
brew install portaudio
```

#### Windows
```bash
pip install pyaudio
```

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/newking9088/dental_office_ai_agent.git
cd dental_office_ai_agent
```

2. Set up Python 3.10 virtual environment:

**✅ Recommended: Using uv (Faster Alternative)**

i. Install uv first:
```bash
pip install uv
```

ii. Create and activate a virtual environment:
```bash
uv venv

-- Activate: Windows
.venv\Scripts\activate

-- Activate: macOS/Linux
source .venv/bin/activate
```

iii. Install dependencies (after activation):
```bash
-- Install using uv (much faster)
uv pip install -r requirements.txt
```

**Traditional Method**

If you prefer using the standard Python virtual environment:

i. Create a virtual environment:
```bash
-- Windows/macOS/Linux
python -m venv .venv
```

ii. Activate virtual environment:
```bash
-- Windows
.venv\Scripts\activate

-- macOS/Linux
source .venv/bin/activate
```

iii. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note**
- The `.venv` directory should be added to your `.gitignore`
- Make sure you have Python 3.10 or later installed
- Always activate the virtual environment before installing packages

3. Setting Up Your API Key Securely

Recommended Method ✅

i. Create or modify the `.env` file securely:
   * Create the file (if it doesn't exist):
   ```bash
   touch .env
   ```
   * Open the file in your preferred text editor
   * Add your API key:
   ```text
   GOOGLE_API_KEY=your_api_key_here
   ```
Alternatively, rename the example environment file and set up your API key (not recommended). Rename the example file:
```bash
mv api_key_example.env .env
```

ii. Set proper file permissions:
```bash
chmod 600 .env
```

iii. [Optional] Load the environment variables:
```bash
source .env
```

⚠️ Warning: Unsafe Method to Avoid

Avoid using the following method as it may expose your API key:
```bash
echo "GOOGLE_API_KEY='your_api_key_here'" > .env  # Not recommended
```

Why avoid echo?
- API key may be saved in shell history
- Key could be visible in process listings
- Risk of accidental file overwrite

Best Practices 🔒

- Never commit your `.env` file to version control

- Add `.env` to your `.gitignore`

- Keep a clean example file (`.env.example`) for reference

- Regularly rotate your API keys

- Use different keys for development and production

## Features & Benefits

### Automated Verification Capabilities

* Real-time eligibility checks
* 7-day advance verification
* Network status confirmation
* Benefit validation
* Prior authorization tracking

### Error Prevention Mechanisms

* Predictive error detection
* Data validation checks
* Coverage requirement verification
* Code accuracy confirmation
* Documentation completeness validation

### Operational Improvements

* Verification time reduction from 14 minutes to near real-time
* Daily manual task reduction of 4-6 hours
* Increased accuracy through automated validation
* 24/7 verification capabilities

## Future Improvements

### Enhanced Accent Handling
* Collection of more diverse speech samples
* Expanded vector database for FAISS correction
* FAISS correction database for each insurance verification question with the filed being the context in which we look for FAISS correction

### Conversation Optimization
* Additional conversation patterns
* Improved error-correction capabilities

### Integration Expansions
* Support for more insurance providers
* Enhanced database connectivity

## Benefits Summary

* Industry savings potential: $12.8 billion
* Verification time reduction: 14 minutes per transaction
* Denial prevention rate: up to 90%
* Operational efficiency improvement: 4-6 hours daily
* 24/7 verification capability

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.
