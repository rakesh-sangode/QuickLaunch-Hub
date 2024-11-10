# SoftGenie

SoftGenie is a user-friendly application launcher built with Python and CustomTkinter. It allows users to easily add, manage, and launch both traditional executable applications and Universal Windows Platform (UWP) apps from a single interface.

## Features

- **Add Applications**: Easily add .exe files or UWP apps to your list.
- **Remove Applications**: Remove applications from your list with a simple click.
- **Launch Applications**: Launch all added applications with a single button.
- **First-Time Setup**: A guided setup process for first-time users.
- **Dark and Light Mode**: Automatically adapts to your system's appearance mode.
- **Website Management**: Add and manage frequently visited websites.
- **Bulk Launch**: Launch all applications and websites with a single click.
- **UWP Support**: Native support for Windows 10/11 UWP applications.
- **Persistent Storage**: Automatically saves your application and website lists.
- **Modern UI**: Clean and intuitive interface with customizable appearance.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rakesh-sangode/softgenie-auto-application-start.git
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

- **Adding Applications**:

  - Click "Add Application" to add a new .exe file
  - Choose "No" when prompted to add UWP apps like Calculator
  - Select the executable file from your system

- **Adding Websites**:

  - Click "Add Website" to add a new website
  - Enter the complete URL (e.g., https://www.example.com)

- **Removing Items**:

  - Select an application or website from the list
  - Click "Remove Application" or "Remove Website" accordingly

- **Launching**:
  - "Launch Applications": Starts all added applications
  - "Launch Websites": Opens all websites in your default browser
  - "Launch Apps & Websites": Launches everything with one click

## Configuration

- The application stores its configuration in `config.json` and the list of applications in `applications.json`.
- The first-time setup is tracked using the `first_launch` flag in `config.json`.
- Website URLs are stored in `websites.json`
- All configuration files are automatically created on first run

## System Requirements

- Windows 10 or later (for UWP app support)
- Python 3.7 or later
- Internet connection (for website features)

## Dependencies

- customtkinter
- tkinter (included with Python)
- webbrowser (included with Python)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Known Issues

- UWP app support is limited to pre-configured applications
- Some applications may require administrative privileges to launch

## Future Enhancements

- Custom categories for applications and websites
- Import/Export functionality for settings
- Hotkey support for quick launch
- Application launch scheduling
- More UWP app support

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for a modern UI.
- Inspired by the need for a simple, efficient application launcher.
- Thanks to all contributors and users for their support and feedback.

## Support

For issues, feature requests, or general questions:

- Open an issue on GitHub
- Fork the repository and submit a pull request
- Contact the maintainer through GitHub

## Version History

- v1.0.0: Initial release with basic application and website management
- Future versions will be documented here
