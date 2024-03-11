<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-aws-open.svg" width="100" />
</p>
<p align="center">
    <h1 align="center">Cognito Clean</h1>
</p>
<p align="center">
    <em>Automated Cognito Hygiene</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/XargsUK/cognito-clean?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/XargsUK/cognito-clean?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/XargsUK/cognito-clean?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/XargsUK/cognito-clean?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Poetry-60A5FA.svg?style=flat&logo=Poetry&logoColor=white" alt="Poetry">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
	<img src="https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white" alt="Pytest">
</p>
<hr>

##  Quick Links

> - [ Overview](#overview)
> - [ Features](#features)
> - [ Repository Structure](#repository-structure)
> - [ Modules](#modules)
> - [ Getting Started](#getting-started)
>   - [ Installation](#installation)
>   - [ Tests](#tests)
> - [ Contributing](#contributing)
> - [ License](#license)
---

##  Overview

`cognito-clean` stands as a streamlined solution for managing AWS Cognito user pools, specifically targeting the perennial issue of unconfirmed user accounts. It provides a simple, automated way to clean up unconfirmed user accounts, ensuring that only active, verified users remain in the user pool. This project is designed to be run as a scheduled Lambda function, ensuring that user pools are kept clean and efficient without manual intervention.

---

##  Features

|    | Feature          | Description |
|----|------------------|--------------------------------------------------------------------|
| ⚙️  | **Architecture** | This project utilises AWS Lambda for cleaning up unconfirmed Cognito user accounts.  |
| 🔩 | **Code Quality** | Adheres to PEP8 guidelines, enforced by flake8 and pylint. The code is structured around modular Python scripts, enhancing readability and maintainability. |
| 🔌 | **Integrations** | Integrates with AWS services like Lambda, S3, SNS and of course, Cognito. GitHub Actions is used for CI/CD, ensuring automated testing and deployment. |
| 🧪 | **Testing**      | Uses pytest and pytest-cov for running tests and measuring code coverage, ensuring reliability and functionality across updates. |
| 📦 | **Dependencies** | Depends on `boto3` for AWS interactions, `pytest`, `pytest-cov`, and `coverage` for testing, and `flake8` for linting. Managed with `poetry` for dependency resolution. |

---

##  Repository Structure

```sh
└── cognito-clean/
  ├── CONTRIBUTING.md
  ├── LICENSE
  ├── README.md
  ├── cognito_clean
  │   ├── cognito_cleaner.py
  │   ├── cognito_manager.py
  │   ├── file_manager.py
  │   └── notification_service.py
  ├── poetry.lock
  ├── pylintrc
  ├── pyproject.toml
  ├── sonar-project.properties
  ├── template.yaml
  └── tests
      ├── test_cognito_manager.py
      ├── test_file_manager.py
      └── test_notification_service.py
  ```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                                      | Summary                                                                                                                                                                                                                                                                                                                             |
| ---                                                                                       | ---                                                                                                                                                                                                                                                                                                                                 |
| [pylintrc](https://github.com/XargsUK/cognito-clean/blob/master/pylintrc)             | The `pylintrc` file defines linting rules for the `cognito-clean` repository, aiming to enforce code quality standards and error prevention across the Python modules.
| [pyproject.toml](https://github.com/XargsUK/asg-scaler-lambda/blob/master/pyproject.toml) | This `pyproject.toml` configures the cognito-clean project, defining dependencies, build settings, and test configurations.                                                                                  |
| [poetry.lock](https://github.com/XargsUK/cognito-clean/blob/master/poetry.lock)       |  A record of all the exact versions of the dependencies used in `cognito-clean`                                                                 |

</details>

<details closed><summary>cognito_clean</summary>

| File                                                             | Summary                                                                                                                                                                                                              |
| ---                                                              | ---                                                                                                                                                                                                                  |
| [notification_service.py](cognito_clean/notification_service.py) | Sends email notifications via AWS SNS for deleted users info. Validates inputs and formats messages before publishing to the specified SNS topic. Handles errors during message sending process.           |
| [cognito_cleaner.py](cognito_clean/cognito_cleaner.py)           | Configures AWS services, processes unconfirmed users, and handles deletions. Deletes users based on specified criteria, stores data in S3, and sends notifications. Caches processed data for efficient future runs. |
| [file_manager.py](cognito_clean/file_manager.py)                 | Writes deleted user data to an S3 bucket in JSON format, logging successful or failed write attempts. Skips write operation if necessary S3 bucket details are missing.                                              |
| [cognito_manager.py](cognito_clean/cognito_manager.py)           | Manages user listing and deletion in Cognito User Pool based on specified criteria and cache. It filters users older than a set age or since the last run time, handling deletion and cache updates.                 |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version 3.10+`
* **Poetry**: `version 1.8.2+`

###  Installation

1. Clone the cognito-clean repository:

```sh
git clone https://github.com/XargsUK/cognito-clean
```

2. Change to the project directory:

```sh
cd cognito-clean
```

3. Install the dependencies with Poetry:

```sh
poetry install
```

###  Tests

Use the following command to run tests:

```sh
poetry run pytest
```

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/XargsUK/cognito-clean/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Report Issues](https://github.com/XargsUK/cognito-clean/issues)**: Submit bugs found or log feature requests for the `cognito-clean` project.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/XargsUK/cognito-clean
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

##  License

This project is protected under the [MIT](https://choosealicense.com/licenses/mit/) License.


---
