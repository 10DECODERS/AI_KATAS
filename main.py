import os
import ast
import time
import uvicorn
import logging
import requests
from pydantic import BaseModel
from sqlglot import parse_one, exp
from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

load_dotenv(find_dotenv())

url = os.getenv('url')
driver = os.getenv('driver')
db_url = os.getenv('db_url')
sql_url = os.getenv('sql_url')
expire_secs = os.getenv('expire_secs')

engine = create_engine(db_url)

app = FastAPI()
router = APIRouter()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger('watchfiles.main').setLevel(logging.WARNING)            


class PromptTemplate:

    def __init__(self, question: str, schema: str | None):
        self.question: str = question
        self.schema: str | None = schema
    
    def default_sql_template(self):
        def_template = f"""Given an input question, first create a syntactically correct postgres SELECT query should be case-insensitive to run. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most 10 results. You can order the results by a relevant column to return the most interesting examples in the database.
        
            Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
        
            Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
        
            Additionally, all searches will be case-insensitive, ensuring that values are found regardless of case. Use the case-insensitive searches in your SQL queries.
        
            Use the following format:
        
            Question: Question here
            SQLQuery: SQL Query to run
                
                use_distinct: True # for indexed id
            """
        return def_template
        
    def sql_query_prompt(self):
        start_time = time.time()
        template = self.default_sql_template()
        prompt = f"""
            ### Task
                    Generate a SQL query to answer [QUESTION]{self.question}[/QUESTION]

                    ### Instructions
                    - {template}
                    
                    ### Database Schema
                    Generate an SQL query based strictly on the provided schema
                    {self.schema}

                    ### Answer
                    Given the database schema, here is the SQL query that answers. avoid hallucinating any additional columns or tables. Ensure the query is valid and corresponds to the real structure of the database.[QUESTION]{self.question}[/QUESTION]
                    [SQL]
                """

        elapsed_time = time.time() - start_time
        logging.info(f"SQL query prompt generated in {elapsed_time:.2f}s")
        return prompt 
    
    def textual_prompt(self, result):
        start_time = time.time()
        prompt = f"""
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        Understand the intent of the question {self.question}. Understand the question {self.question} and answer from database {result}.frame the response as a chatbot to answer the {self.question},don't hallucinate. Don't give explanation. Avoid greetings in the beginning of the answer. Make sure to generate text answers.
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {self.question}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        """
        elapsed_time = time.time() - start_time
        logging.info(f"Textual prompt generated in {elapsed_time:.2f}s")
        return prompt

class LLMRequest:

    def __init__(self, url: str, prompt: str, stream: bool, n_predict: int):
        self.url: str = url
        self.prompt: str = prompt
        self.stream: bool = stream
        self.n_predict: int = n_predict

    def get_llm_response(self):
        start_time = time.time()
        try:
            headers = {"Content-Type": "application/json"}
            print("************\n",self.prompt)
            data = {"temperature": 0, "prompt": self.prompt, "n_predict": self.n_predict, "stop": ["</s>"], "stream": self.stream}
            response = requests.post(url=self.url, headers=headers, json=data, timeout=1000)
            elapsed_time = time.time() - start_time
            logging.info(f"LLM request completed in {elapsed_time:.2f}s")
            return response
        except Exception as e:
            logging.error(f"Error during LLM request: {e}")
            raise Exception(f"Error during LLM request: {e}")
        
class QueryValidator:

    def __init__(self, sql_query, driver=None):
        self.sql_query = sql_query
        self.driver = driver

    def extract_query_tables(self):
        try:
            start_time = time.time()
            query_tab = set()
            for table in parse_one(self.sql_query,read=self.driver).find_all(exp.Table):
                query_tab.add(table.name)
            if not query_tab:
                raise Exception("No table was found from the query.")
            elapsed_time = time.time() - start_time
            logging.info(f"Extracted tables in {elapsed_time:.2f}s")
            return query_tab
        except Exception as e:
            logging.error(f"Error parsing tables: {str(e)}")
            raise Exception(f"Could not parse tables from the query: {str(e)}")

    def extract_query_columns(self, data_schema):
        try:
            # values = {v.lower() for sublist in data_schema.values() for v in sublist}
            start_time = time.time()
            query_col = set()
            for select in parse_one(self.sql_query,read=self.driver).find_all(exp.Select):
                for projection in select.expressions:
                    if (type(projection) == exp.Column):
                        query_col.add(projection.name)
                    elif (type(projection) == exp.Star):
                        print(projection.name)
                        query_col.update(data_schema)
                    else:
                        print(F'It is not a column: {projection.output_name}')
            if not query_col:
                query_col.update(data_schema)
            elapsed_time = time.time() - start_time
            logging.info(f"Extracted tables in {elapsed_time:.2f}s")
            return query_col
        except Exception as e:
            raise Exception(f"Sorry! {str(e)}")
    
    def get_table_col(self):
        try:
            start_time = time.time()
            folder_path = "./table_data"
            file_name = "schema.txt"
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding="utf-8") as file:
                schema_data = file.read()
            print(schema_data)
            tables_columns = ast.literal_eval(schema_data)
            elapsed_time = time.time() - start_time
            logging.info(f"Fetched table columns in {elapsed_time:.2f}s")
            return tables_columns
        except Exception as e:
            logging.error(f"Error fetching table columns: {str(e)}")
            raise Exception(f"Could not fetch table columns: {str(e)}")

    def query_parser(self):
        try:
            start_time = time.time()
            table_columns = self.get_table_col()
            table_s = [key for key in table_columns]
            tables = self.extract_query_tables()
            if all(elem in table_s for elem in tables):
                cols = [col for key, value in table_columns.items() for table in tables if key == table for col in value]
                columns = self.extract_query_columns(cols)
                matching_columns = [col for table in tables if table in table_columns for col in table_columns[table]]
                is_valid = all(elem in matching_columns for elem in columns)
                elapsed_time = time.time() - start_time
                logging.info(f"Query parsed in {elapsed_time:.2f}s")
                return is_valid
            else:
                logging.warning("Some tables in the query are not valid.")
                return False
        except Exception as e:
            logging.error(f"Error parsing query: {str(e)}")
            raise Exception(f"Error parsing query: {str(e)}")


class QueryExecuter:

    def execute_query(self, db_uri, sqlquery):
        try:
            start_time = time.time()
            with engine.connect() as conn:
                query_result = conn.execute(text(sqlquery))
                result = []
                if query_result.returns_rows:
                    fetched_data = query_result.fetchall()
                    if fetched_data:
                        result.extend(fetched_data)
                    else:
                        scalar_data = query_result.scalar()
                        if scalar_data is not None:
                            result.append(scalar_data)
                        else:
                            logging.info(f"No results found for the query: {sqlquery}")
                            return f"No result found for the query."
                else:
                    logging.info(f"Query cannot generate results: {sqlquery}")
                    return f"The query cannot be generated."
                query_result.close()
                conn.commit()
                elapsed_time = time.time() - start_time
                logging.info(f"Query executed in {elapsed_time:.2f}s")
                return result
        except Exception as e:
            logging.error(f"Failed to execute query: {str(e)}")
            raise Exception(f"Failed to execute query: {str(e)}")   
            

class ChatResponse:

    def __init__(self, data: dict):
        self.question: str = data.question
        self.session_id: str = data.session_id
        self.query_executer = QueryExecuter()
 
    def create_directory(self, folder_path):
        """Creates a directory if it doesn't exist."""
        try:
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            return True
        except Exception as e:
            raise Exception(f"{e}")

    def get_create_statements(self) -> str:
        """Extracts table create statements based on schema."""
        try:
            folder_path ="./table_data"
            file_path = os.path.join(folder_path, "metadata.sql")
            with open(file_path,'r', encoding="utf-8") as file:
                schema = file.read()
            return schema
        except Exception as e:
            raise Exception(f"{e}")

    def get_schema(self) -> str:
        """Giving the schema"""
        try:
            schema: str = self.get_create_statements()
            return schema
        except Exception as e:
            raise Exception(f"{e}")
        
    def get_sql_query(self) -> str:
        """Generates SQL query based on the question and schema."""
        try:
            schema = self.get_schema()
            prompt_template = PromptTemplate(question = self.question,schema=schema)
            prompt: str = prompt_template.sql_query_prompt()
            n_predict: int = 512
            response = LLMRequest(url=sql_url, prompt=prompt, stream=False, n_predict=n_predict)
            sql_query = response.get_llm_response()
            print("SqL_query",sql_query.json()['content'])
            return sql_query.json()['content']
        except Exception as e:
            raise Exception(f"{e}")
        
    def get_query_result(self):
        """Executes the SQL query and returns the result."""
        sql_query = self.get_sql_query()
        print(sql_query.strip())
        query_validation = QueryValidator(sql_query.strip()).query_parser()
        if query_validation:
            result = self.query_executer.execute_query(db_uri=db_url, sqlquery=sql_query.strip())
            return result
        else:
            raise Exception(f"Generated SQL query is not valid: {sql_query}")
    
    def get_text_response(self) -> str:
        """Generates a text response by combining the SQL query result and chat history."""
        try:
            query_result = self.get_query_result()
            print("query_result", query_result)
            prompt_template = PromptTemplate(self.question, schema=None)
            prompt: str = prompt_template.textual_prompt(result=query_result)
            n_predict: int = 1024
            response = LLMRequest(url=url, prompt=prompt, stream=False, n_predict=n_predict)
            text_generator = response.get_llm_response()
            response = text_generator.json()['content']
            print(response)
            return response.replace('\n','<br>')
        except Exception as e:
            raise Exception(f"{e}")      

class ChatPayload(BaseModel):
    """Payload structure for the chat request."""
    question: str
    session_id: str


@app.post("/v1/chat")
async def process_chat_query(payload: ChatPayload):
    """API endpoint for processing chat queries."""
    try:
        st = time.time()
        response = ChatResponse(payload)
        text_response = response.get_text_response()
        et = time.time()
        print(f"Time taken : {et - st}")
        return text_response
    except Exception as e:
        raise Exception(f"{e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)   
