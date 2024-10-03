import logging
from typing import Any, Dict

import config_settings
from mod_data_loader import load_data
from data_processor import process_data
from mod_tree_generator import generate_tree
from mod_visualization import Visualization
from mod_ui import UserInterface
from mod_interaction import Interaction
from event_manager import EventManager
import sys
from profiling import run_profiler, print_profiler_stats

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_process_data(settings: Dict[str, Any]) -> Any:
    try:
        raw_data = load_data(settings['data_file'])
        processed_data = process_data(raw_data)
        return processed_data
    except Exception as e:
        logging.error(f"Error loading or processing data: {e}")
        raise

def initialize_components(settings: Dict[str, Any], processed_data: Any) -> (Visualization, UserInterface, Interaction):
    try:
        tree = generate_tree(processed_data)
        event_manager = EventManager()
        viz = Visualization(tree, settings, event_manager)
        ui = UserInterface(settings, viz, event_manager)
        interaction = Interaction(viz, ui)
        return viz, ui, interaction
    except Exception as e:
        logging.error(f"Error initializing components: {e}")
        raise

def main() -> None:
    setup_logging()
    logging.info("Starting the application")

    try:
        settings = config_settings.load_settings()
        processed_data = load_and_process_data(settings)
        viz, ui, interaction = initialize_components(settings, processed_data)

        ui.show()
        viz.run()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")

if __name__ == "__main__":
    if "--profile" in sys.argv:
        run_profiler()
        print_profiler_stats()
    else:
        main()