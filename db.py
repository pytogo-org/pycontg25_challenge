from config import supabase

def get_some_thing(table_name: str):
    """
    Fetches data from a specified table in the Supabase database.
    
    Args:
        table_name (str): The name of the table to query.
        
    Returns:
        list: A list of records from the specified table.
    """
    response = supabase.table(table_name).select("*").execute()
    return response.data if response.data else []


def insert_into_table(table_name: str, data: dict):
    """
    Inserts a new record into a specified table in the Supabase database.
    
    Args:
        table_name (str): The name of the table to insert data into.
        data (dict): A dictionary containing the data to insert.
        
    Returns:
        dict: The inserted record or an error message if the insertion fails.
    """
    response = supabase.table(table_name).insert(data).execute()
    print(response)
    if not response:
        return {"error": "Insertion failed"}
    return True if response.data else False

def update_table(table_name: str, record_id: int, data: dict):
    """
    Updates a record in a specified table in the Supabase database.
    
    Args:
        table_name (str): The name of the table to update.
        record_id (int): The ID of the record to update.
        data (dict): A dictionary containing the updated data.
        
    Returns:
        dict: The updated record or an error message if the update fails.
    """
    response = supabase.table(table_name).update(data).eq("id", record_id).execute()
    if response.error:
        return {"error": response.error.message}
    return response.data[0] if response.data else {}

def get_record_by_email(table_name: str, email: str):
    """
    Fetches a record from a specified table in the Supabase database by email.
    
    Args:
        table_name (str): The name of the table to query.
        email (str): The email to search for.
        
    Returns:
        dict: The record with the specified email or None if not found.
    """
    response = supabase.table(table_name).select("*").eq("email", email).execute()
    return response.data[0] if response.data else None

def get_some_where(table_name: str, column1: str, value1: str, column2: str, value2: str):
    """
    Fetches records from a specified table in the Supabase database where two columns match their respective values.

    Args:
        table_name (str): The name of the table to query.
        column1 (str): The first column to filter by.
        value1 (str): The value to match in the first column.
        column2 (str): The second column to filter by.
        value2 (str): The value to match in the second column.

    Returns:
        list: A list of records that match the criteria.
    """
    response = supabase.table(table_name).select("*").eq(column1, value1).eq(column2, value2).execute()
    return response.data if response.data else []
    