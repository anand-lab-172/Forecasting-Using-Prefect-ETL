# Forecasting-Using-Prefect-ETL

## Description
This project involves using a Variational Long Short-Term Memory (VLSTM) model for time series forecasting. The project also utilizes Prefect for orchestrating and managing workflows.

## Installation
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up the Prefect API URL by running:
    ```sh
    export PREFECT_API_URL=http://127.0.0.1:4200
    ```

## Usage
### Running the VLSTM Model
1. Open the [vlstm.py](http://_vscodecontentref_/0) file and configure the model parameters as needed.
2. Run the script:
    ```sh
    python vlstm.py
    ```

### Using Prefect
1. Define the asynchronous function in your Prefect flow:
    ```python
    async def fetch_work_pools():
        client = get_client()
        work_pools = await client.read_work_pools()
        print(work_pools)
    ```
2. Set the Prefect API URL in your environment:
    ```sh
    export PREFECT_API_URL=http://127.0.0.1:4200
    ```
3. Verify the environment variable is set:
    ```python
    import os
    api_url = os.getenv('PREFECT_API_URL')
    if api_url:
        print(f"PREFECT_API_URL is set to: {api_url}")
    else:
        print("PREFECT_API_URL is not set.")
    ```

## Contributing
Guidelines for contributing to the project.

## License
Information about the project's license.
