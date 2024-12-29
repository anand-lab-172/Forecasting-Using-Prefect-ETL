# Project Title

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
1. Start the Prefect server:
    ```sh
    prefect server start
    ```
2. Deploy the VLSTM pipeline:
    ```sh
    prefect deploy --prefect-file prefect.yaml --name "VLSTM Pipeline"
    ```
3. Create a work pool named "Automation":
    ```sh
    prefect work-pool create "Automation"
    ```
4. Start a worker in the "Automation" pool:
    ```sh
    prefect worker start --pool "Automation"
    ```
5. Stop the worker in the "Automation" pool:
    ```sh
    prefect worker stop --pool "Automation"
    ```
6. Delete the "Automation" work pool:
    ```sh
    prefect work-pool delete "Automation"
    ```
7. List all work pools:
    ```sh
    prefect work-pool ls
    ```

## Contributing
Guidelines for contributing to the project.

## License
Information about the project's license.
