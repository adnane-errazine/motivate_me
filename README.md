# motivaty
**{Tech: Europe} AI Hackathon in Paris**

---

## Quick Start

### Run backend
This project uses **`uv`**.

1.  **Clone**:
    ```bash
    git clone https://github.com/adnane-errazine/motivate_me
    cd motivate_me/backend
    ```

2.  **Install `uv`**:
    ```bash
    * `curl -LsSf https://astral.sh/uv/install.sh | sh` (macOS/Linux)
    * `irm https://astral.sh/uv/install.ps1 | iex` (Windows PowerShell)
    * pip install uv
    ```

4.  **Environment Setup**:
    ```bash
    # Create an `.env` file in the backend, check .env-example
    touch .env
    ```

5.  **Install dependencies & Run**:
    ```bash
    uv sync
    uv run app.py
    ```

### Run frontend

1.  **Install dependencies & Run**:
    ```bash
    cd motivate_me/frontend
    npm install
    npm run dev
    ```
