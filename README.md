# Dental Insurance Verification AI Agent

## Introduction

An AI-powered system that automates dental insurance verification processes, capable of handling real-time conversations, accent variations, and data extraction. The system reduces verification time from 
14 minutes to near real-time processing while helping prevent claim denials.

## Quicklinks

* [Blog Post](https://nycdatascience.com/blog/?p=100015&preview=true&aiEnableCheckShortcode=true)

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
   * First, follow the instructions in the Python 3.10 virtual environment setup file to ensure proper configuration
   * Then create and activate the virtual environment:
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# macOS/Linux
python -m venv myenv
source myenv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
   * Rename `api_key_example.env` to `.env` and paste your GOOGLE_API_KEY in there

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
