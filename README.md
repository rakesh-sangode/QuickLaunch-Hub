# QuickLaunch - Hub

QuickLaunch - Hub is a powerful Windows application manager built with Python and CustomTkinter. It provides an intuitive interface to discover, manage, and launch both traditional executable applications and Universal Windows Platform (UWP) apps.

## Features

- **Smart Application Discovery**:

  - Automatically detects installed Windows applications
  - Supports both traditional .exe files and UWP apps
  - Registry-based application detection

- **Advanced Selection Features**:

  - Multi-select functionality with checkboxes
  - Select/Unselect all applications with one click
  - Visual feedback with green highlighting for selected apps
  - Intuitive icon-based controls

- **Application Management**:

  - Add applications to your personal collection
  - Remove applications with a single click
  - Bulk application launching
  - Website management and launching

- **Modern User Interface**:

  - Clean, minimal design with custom icons
  - Theme-adaptive interface (Dark/Light mode)
  - Tabbed organization (All Apps, My Applications, Websites)
  - Smooth visual feedback and transitions

- **Persistent Storage**:
  - Automatic saving of application lists
  - Website URL management
  - Configuration persistence

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/rakesh-sangode/QuickLaunch-Hub.git
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

- **Managing Applications**:

  - Browse all installed applications in the "All Apps" tab
  - Select applications using checkboxes
  - Click the "+" icon to add selected apps to My Applications
  - Click the "-" icon to remove apps from My Applications
  - Use "Select All" and "Unselect All" for bulk operations

- **Website Management**:

  - Add websites in the dedicated Websites tab
  - Launch websites in your default browser
  - Manage website collections easily

- **Launching**:
  - Launch individual applications with a click
  - Bulk launch multiple selected applications
  - Open websites directly from the interface

## System Requirements

- Windows 10 or later (for UWP app support)
- Python 3.7 or later
- Required Python packages:
  - customtkinter
  - Pillow (for icon generation)
  - tkinter (included with Python)

## Configuration

The application maintains several configuration files:

- `applications.json`: Stores your personal application collection
- `websites.json`: Manages website URLs
- `config.json`: Handles application settings and preferences

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Future Enhancements

- Enhanced filtering and search capabilities
- Application categories and tags
- Custom icon themes
- Performance optimization for large application lists
- Cross-platform compatibility

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with CustomTkinter for modern UI components
- Uses Pillow for dynamic icon generation
- Inspired by the need for efficient application management on Windows
