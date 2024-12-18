# pydanticai-price-monitoring-agent

## Overview

The `pydanticai-price-monitoring-agent` is a price monitoring agent that utilizes the PydanticAI library to extract pricing information from product URLs and compare it with the information in the database.

## Features

- Extracts pricing information from product URLs.
- Compares the extracted pricing information with the information in the database.
- Sends email notifications when a price difference is detected.
- Stores the pricing information in the database.

## Prerequisites

- Python 3.x
- PydanticAI library
- SendGrid API key
- OpenAI API key
- Database connection URL

## Installation

1. Clone the repository:

2. Install the required dependencies:

3. Set up the environment variables:

- Copy the `.env-example-file` to a new file named `.env` in the project root directory.
- Fill in the required environment variables:

4. Run the agent:

## Usage

1. Provide the URL of the product you want to monitor.
2. The agent will extract the pricing information from the URL.
3. The agent will compare the extracted pricing information with the information in the database.
4. If a price difference is detected, the agent will send an email notification.
5. The agent will store the pricing information in the database.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
