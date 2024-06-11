# ErDrop

Simple File Transfer between Linux & Windows Systems

## Getting Started

### Prerequisites

Ensure you have the following installed on your computer:
- Python 3.x
- pip (Python package installer)

### Installing

1. Download or clone the repository:
    ```sh
    git clone https://github.com/yourusername/erdrop.git
    cd erdrop
    ```

2. Install the required dependencies:
    - For Linux users:
        ```sh
        python3 -m pip install -r requirements.txt
        ```
    - For Windows users:
        ```sh
        python -m pip install -r requirements.txt
        ```

### Executing the Program

1. Run the program:
    - For Linux users:
        ```sh
        python3 main.py
        ```
    - For Windows users:
        ```sh
        python main.py
        ```

**Note**: Ensure that both systems are connected to the same network to transfer files.

### Extending the Project (Developer Guide)

Our project is designed to be easily extendable. You can inherit from our base classes using the `abc.ABC` module and develop your own components. 
Please read the [CONTRIBUTING.md](CONTRIBUTING.md) for details on the code of conduct and the process for submitting pull requests.

### Bug Reports

If you encounter any issues or bugs, please report them by opening an issue on GitHub:
[https://github.com/erfanhooman/erdrop/issues](https://github.com/erfanhooman/erdrop/issues)

Provide as much detail as possible, including steps to reproduce the issue and any error messages you received.


### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.