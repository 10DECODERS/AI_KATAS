# To run python application

### Prerequisites

- [Python 3.9 or higher](https://www.geeksforgeeks.org/how-to-install-python-on-linux/)
- Installation of Python virtual environment (`virtualenv`)

### Clone the repository:

```
git clone https://github.com/10DECODERS/AI_KATAS.git
```

### Navigate to the project directory:

```
cd AI_KATAS
```

### Set up a virtual environment:

```
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
```

### Install the required dependencies:

```
pip install -r requirements.txt
```

### Run the application

```
python main.py
```

### Environmental variables

```
url= Url for text generated model
sql_url= Url for text to sql model
db_url=postgresql+psycopg2://<db username>:<password>@<db host>:<db port>/<db name> (External database)
expire_secs=expire seconds to set automatic data deletion
driver = postgres
```

# To run UI

### Installation

```
pip install streamlit
```

### Run streamlit app

```
streamlit run sample_ui.py
```
