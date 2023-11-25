# Real-time Trading Agent

## Overview

The Real-time Trading Agent is an auto-trading bot project that utilizes reinforcement learning to make trading decisions based on historical price data. The project simulates streaming data by leveraging Apache Kafka and processes historical price data crawled from Cafef.

## Features

- Reinforcement learning-based auto-trading bot.
- Simulation of streaming data using historical price data.
- Integration with Apache Kafka for data streaming.
- Data crawled from Cafef for historical price information.

## Dependencies

- Python 3.x
- [Apache Kafka](https://kafka.apache.org/)
- [Reinforcement Learning Library (e.g., TensorFlow, PyTorch)](https://github.com/openai/gym)
- Other dependencies specified in `requirements.txt`

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/real-time-trading-agent.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up and configure Apache Kafka.**

4. **Run the project:**

    ```bash
    python main.py
    ```

## Configuration

- Modify the configuration file (`config.yaml`) to specify trading parameters, Kafka broker information, and other settings.

## Usage

1. **Train the reinforcement learning model:**

    ```bash
    python train_model.py
    ```

2. **Run the real-time trading agent:**

    ```bash
    python main.py
    ```

## Contributing

Contributions are welcome! Please follow the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [Cafef](https://www.cafef.vn/) for providing historical price data.

## Contact

For any inquiries or issues, please contact:

- Your Name
- Your Email
