# motivate_me
Europe: Paris Hackathon

---

## Quick Start

This project uses **`uv`**.

1.  **Install `uv`**:
    * `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux)
    * `irm https://astral.sh/uv/install.ps1 | iex` (Windows PowerShell)
    * pip install uv

2.  **Environment Setup**:
    Create a `.env` file in the project root with the following variables:
    ```env
    MISTRAL_API_KEY=your_mistral_api_key_here
    GOOGLE_API_KEY=your_google_api_key_here             # https://developers.google.com/custom-search/v1/overview
    GOOGLE_CSE_ID=your_google_custom_search_engine_id_here     # https://programmablesearchengine.google.com/
    ```

3.  **Clone & Run**:
    ```bash
    git clone https://github.com/adnane-errazine/motivate_me
    cd motivate_me
    uv sync
    uv run app.py
    ```