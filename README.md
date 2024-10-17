# L.I.O.N Report Management App

## Overview

The L.I.O.N Report Management App allows managers to track their activities and generate Weekly L.I.O.N (Last week, Issues, Opportunities, Next week) reports. Built with Python and Flask, it offers an intuitive user interface for data entry, storage, and report generation.

## Features

- **User Authentication** (Optional)
- **Data Entry Forms** for Last Week Achievements, Issues, Opportunities, and Next Week Commitments
- **CRUD Functionality** for L.I.O.N entries
- **Search and Filter** past entries
- **Report Generation** with export options (PDF, Word, Markdown)
- **Email Integration** to send reports
- **Responsive UI** using Bootstrap 5
- **Database Support** for SQLite (development) and PostgreSQL (production)
- **Unit and Integration Testing** with pytest

## Installation

### Prerequisites

- [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Python 3.11 or newer

### Setup Environment

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/lion_report_app.git
    cd lion_report_app
    ```

2. **Create a Conda environment:**

    ```bash
    conda env create -f environment.yml
    ```

3. **Activate the environment:**

    ```bash
    conda activate lion_report_env
    ```

### Database Migration

1. **Initialize the database:**

    ```bash
    flask db init
    flask db migrate -m "Add authentication and CRUD operations"
    flask db upgrade
    ```

### Running the Application

- **For Web App:**

    ```bash
    python app.py
    ```

    Access the app at `http://localhost:5000`.

- **For Desktop App:**

    *To be implemented.*

### Testing

- **Run tests using pytest:**

    ```bash
    pytest
    ```

## Contribution

Contributions are welcome! Please open an issue or submit a pull request.

## License

[MIT License](LICENSE)
