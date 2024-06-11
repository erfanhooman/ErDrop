# Contributing to ErDrop

👋 Thank you for your interest in contributing to ErDrop! Our project is designed to be easily extendable. we are using the `abc.ABC` module so you can inherit from our base classes and develop your own components. Here’s how:


### Inheriting from Base Classes

1. **Locate the Base Class**:
    - The project has two main parts: `sender` and `receiver`. You can modify the desired part within each directory.
    - Base classes are located in each directory with the name `***Base.py`. For example, to modify our download manager, use the `DownloadManager` class in `DownloadManagerBase.py`.

2. **Create Your Own Class**:
    - Create a new file in the same directory as the `***Base.py` file and inherit from the base class. For example, `CustomDownloadManager.py`:

    ```python
    from receiver.downloadmanager.DownloadManagerBase import DownloadManager

    class CustomDownloadManager(DownloadManager):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Your custom initialization here

        def download_file(self):
            # Implement your custom transfer logic here
            pass
    ```

3. **Modify the Configuration File**:
    - The configuration file `Config.yaml` will be automatically created after the first run of the program.
    - This file contains settings for the modules and components used in the project.
    - To use your custom module, update the configuration file by changing the module and class names in the appropriate section.

#### Example Configuration File

Here's a`Config.yaml` file:
```yaml
Module:
  Receiver:
    user_interface_class: QtWindow
    user_interface_module: QtGUI
    # ...
  Sender:
    discover_receiver_class: DefaultDiscoveringImplementation
    discover_receiver_module: DefaultDiscoveringImplementation
    # ...

Settings:
  Receiver:
    name: receiver_name # use the hostname as default
    path: null
    receive_port: 5000
    receiver_host: 0.0.0.0
  Sender:
    name: sender_name # use the hostname as default
    discovery_port: 5000
    discovery_timeout: 1.0
    send_port: 25622
```

4. **Updating the Configuration File**:
   - After running the program once, the `Config.yaml` file will be created in the root directory.
   - Update the module and class names in the `Module` section to point to your custom implementations. For example, if you created a custom download manager, update the `download_manager_class` and `download_manager_module` fields.
   - You can also modify the `Settings` section in the `Config.yaml` file to adjust the base settings of the program according to your requirements. For instance, you can change the `name`, `path`, `port`, and other parameters for both `Receiver` and `Sender`.

### Testing Your Component

1. **Run the Program**:
    - Ensure your custom component is configured correctly and run the program as usual:

    ```sh
    python main.py
    ```
   
### Sharing Your Module

If you develop a new module and want to share it with us, follow these steps:

1. **Fork the Repository**: Click the "Fork" button at the top-right corner of the repository page to create your own copy of the repository.

2. **Clone Your Fork**: Clone your forked repository to your local machine:

    ```sh
    git clone https://github.com/erfanhooman/erdrop.git
    cd erdrop
    ```

3. **Create a New Branch**: Create and switch to a new branch for your changes:

    ```sh
    git checkout -b new-module-branch
    ```

4. **Make Your Changes**: Develop your new module by following the guidelines in the "Extending the Project" section.

5. **Commit Your Changes**: Stage and commit your changes:

    ```sh
    git add .
    git commit -m "Add new module for [description]"
    ```

6. **Push Your Changes**: Push the changes to your forked repository:

    ```sh
    git push origin new-module-branch
    ```

7. **Create a Pull Request**: Go to your forked repository on GitHub and click the "New pull request" button. Provide a title and description for your pull request, then click "Create pull request".

I will review your pull request and provide feedback. Once approved, your changes will be merged into the main repository. Thank you for your contributions!

By following these steps, you can extend the functionality of ErDrop by creating custom components that inherit from the base classes. This allows for flexible and modular development tailored to your needs.
