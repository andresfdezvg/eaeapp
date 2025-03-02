import json
import pg8000

def lambda_handler(event, context):

    # Setup MySQL Connection
    conn = pg8000.connect(
        host= '',
        user= 'postgres',
        password= 'secret01',
        database= 'postgres',
        ssl_context=True
    )

    cursor = conn.cursor()

    # Execute MySQL Query
    query = """
    SELECT job_title, ROUND(AVG(salary_in_usd))::INTEGER as average_salary
    FROM salaries
    GROUP BY job_title
    ORDER BY average_salary DESC
    LIMIT 10
    """
    cursor.execute(query)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Get column names
    column_names = [i[0] for i in cursor.description]

    # Convert data to JSON format
    result = []
    for row in rows:
        data_dict = {}
        for i in range(len(column_names)):
            data_dict[column_names[i]] = row[i]
        result.append(data_dict)

    # Close connections
    cursor.close()
    conn.close()

    # Construct response
    response = {
        "statusCode": 200,
        "data": json.dumps(result)  # Convert data to JSON
    }

    return response
