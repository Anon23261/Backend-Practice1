# Backend Practice 1

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)
![Code Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Description
This project is designed to showcase backend development skills and practices. It allows users to manage customers, vehicles, mechanics, and service tickets in an automotive service context. The application provides a comprehensive platform for managing the workflow of an automotive service center, including customer and vehicle information, mechanic assignments, and service ticket management.

## Features
- **Add, view, update, and delete customers.**
- **Add, view, update, and delete vehicles associated with customers.**
- **Add, view, update, and delete mechanics.**
- **Add, view, update, and delete service tickets.**
- **Manage service mechanics associated with service tickets.**
- **Assign mechanics to service tickets.**
- **Update the status of service tickets.**
- **Comprehensive unit tests for all classes, ensuring functionality and reliability.**

## Installation
To install this project, clone the repository:
```bash
git clone https://github.com/Anon23261/Backend-Practice1.git
cd Backend-Practice1
```

## Usage
To run the application, use the following command:
```bash
python practice1.py
```

To run the tests, use the following command:
```bash
python3 -m unittest test_practice1.py
```

Follow the on-screen prompts to interact with the application. Here are some usage examples:
* To add a new customer, select the "Add Customer" option and enter the customer's name, email, and phone number.
* To view all customers, select the "View Customers" option.
* To assign a mechanic to a service ticket, select the "Assign Mechanic" option and choose the mechanic and service ticket.

## Testing
The application includes unit tests to ensure the reliability of its features. To run the tests, execute the command:
```bash
python3 -m unittest test_practice1.py
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue. When contributing, please follow these guidelines:
* Make sure to test your changes thoroughly before submitting a pull request.
* Use descriptive commit messages and follow the standard commit message format.
* Keep your changes focused on a single feature or bug fix.
* Use Markdown formatting for your commit messages and pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
