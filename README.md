# Evolution3DVisualizer

## Overview

**Evolution3DVisualizer** is an interactive Python application that visualizes evolutionary relationships in a 3D space. Users can explore genetic trees, zoom into species to see individual relationships, and observe how individuals are related within and across species.

## Features

- **3D Tree Structure**: Visualize evolutionary trees with nodes representing species or individuals.
- **Interactive Zooming**: Click on species to zoom in and explore detailed relationships.
- **Color Coding**: Differentiate taxonomic levels or genetic similarities using colors.
- **Search & Filter**: Easily find and highlight specific species or traits.
- **Time-based Evolution**: Observe how species evolved over time with an interactive timeline.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/Evolution3DVisualizer.git
    cd Evolution3DVisualizer
    ```

2. **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Prepare Data**:

    - Ensure your data is in `data_sample_dataset.csv` or `data_sample_dataset.json`.
    - The CSV should contain columns like `species` and `genetic_marker`.

2. **Run the Application**:

    ```bash
    python main_app.py
    ```

3. **Interact with the Visualization**:

    - Use the UI buttons to zoom in, zoom out, or reset the view.
    - Click on nodes to explore relationships.

## Configuration

- **Settings**: Modify `config_settings.json` to adjust visualization parameters like colors, node sizes, and data file paths.

## Contributing

Contributions are welcome! Please open issues and submit pull requests for improvements.

## License

MIT License. See `LICENSE` file for details.
