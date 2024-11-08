# SoftGenie

SoftGenie is a user-friendly application launcher built with Python and CustomTkinter. It allows users to easily add, manage, and launch both traditional executable applications and Universal Windows Platform (UWP) apps from a single interface.

## Features

- **Add Applications**: Easily add .exe files or UWP apps to your list.
- **Remove Applications**: Remove applications from your list with a simple click.
- **Launch Applications**: Launch all added applications with a single button.
- **First-Time Setup**: A guided setup process for first-time users.
- **Dark and Light Mode**: Automatically adapts to your system's appearance mode.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/softgenie.git
   cd softgenie
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Usage

- **Adding Applications**: Click "Add Application" to add a new .exe or UWP app.
- **Removing Applications**: Select an application from the list and click "Remove Application".
- **Launching Applications**: Click "Launch" to start all applications in your list.

## Configuration

- The application stores its configuration in `config.json` and the list of applications in `applications.json`.
- The first-time setup is tracked using the `first_launch` flag in `config.json`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern UI.
- Inspired by the need for a simple, efficient application launcher.
