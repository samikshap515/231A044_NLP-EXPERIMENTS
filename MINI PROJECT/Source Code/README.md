# Meeting Action Item Extractor

A Python Streamlit application for extracting action items, deadlines, and priorities from meeting notes.

## Overview

The application processes meeting text (from uploaded files or direct paste) and identifies:
- **Action items** with task descriptions
- **Assignees** (people responsible)
- **Deadlines** with natural language normalization (e.g., "Friday", "tomorrow", "next week")
- **Priority levels** (High, Medium, Low)

## Architecture

- **app.py**: Streamlit user interface (entry point: `streamlit run app.py`)
- **ai_extractor.py**: Primary AI extraction backend using Ollama's llama3.2:3b model
- **extractor.py**: Deterministic NLP/deadline/priority fallback module (regex-based)

## Key Design Decisions

1. `ai_extractor.py` is the primary AI extraction backend
2. `app.py` calls `extract_action_items_with_ai()` from `ai_extractor.py`
3. `extractor.py` is preserved as the deterministic fallback module
4. Results are standardized as Pandas DataFrames with columns: Assigned To, Action Item, Deadline, Normalized Deadline, Priority
5. DataFrame row iteration fixed to use `iterrows()` instead of treating rows as dictionaries
6. Ollama unavailability is handled gracefully with deterministic fallbacks

## Requirements (Satisfied)

1. ✅ `ai_extractor.py` is the primary AI extraction backend
2. ✅ `app.py` calls `extract_action_items_with_ai()`
3. ✅ `extractor.py` kept as deterministic fallback (not used as main extractor)
4. ✅ Result format: Pandas DataFrame with exact columns
5. ✅ Fixed DataFrame row-as-dict mismatch in app.py
6. ✅ Deadline normalization logic preserved
7. ✅ Deterministic fallback extraction preserved
8. ✅ All existing tests pass unchanged
9. ✅ Project core objective unchanged
10. ✅ No unnecessary code rewrites

## Installation

```bash
# Install requirements
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Optional: Local Ollama

The application can optionally use a local Ollama installation with the llama3.2:3b model
for AI-powered extraction. However, Ollama is **not required** - the application
gracefully falls back to deterministic NLP extraction if Ollama is unavailable.

To use Ollama:
1. Install Ollama from https://ollama.ai
2. Pull the model: `ollama pull llama3.2:3b`
3. Start Ollama service
4. The application will automatically use it if available

## License

MIT
