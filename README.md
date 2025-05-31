# motivaty
**{Tech: Europe} AI Hackathon in Paris**

---

## Project Description

Motivaty was conceived during the {Tech: Europe} Paris Hackathon, addressing a common challenge in education. Many students find it difficult to connect abstract concepts, formulas, or theorems to their real-world significance. This often leads to diminished motivation, where learning becomes a task to complete for a grade rather than an engaging exploration.

Motivaty tackles this by providing context. Users can input a concept, formula, theorem, or an entire syllabus. The application then identifies and presents engaging, real-world applications tailored to the user's interests. Furthermore, it generates a personalized learning roadmap, aiming to make each lesson feel relevant and inspiring.

For instance, knowing that the Fourier transform is the fundamental technology behind music identification services like Shazam can greatly enhance a student's desire to understand it.

### Tech Stack
The project is built using the following technologies:
*   **Backend:** FastAPI, LangGraph for agent orchestration, Mistral AI (Mistral OCR and Mistral Small) for document parsing and understanding.
*   **Frontend:** React, Vite.

### Future Development
We have plans to further develop Motivaty by incorporating features such as:
*   Internet-powered search capabilities using MCPs.
*   Knowledge-graph-based Retrieval Augmented Generation (RAG) leveraging public datasets.
*   Tools for evaluation.
*   Comprehensive logging and tracing.
*   Containerization for easier deployment.
*   Integration of local vision-language models.
*   Additional parsing tools for broader content compatibility.

Feel free to contact us for collaborations or inquiries!

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
