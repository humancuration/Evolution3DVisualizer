import pytest
from mod_data_loader import load_data
from mod_tree_generator import generate_tree
from mod_visualization import Visualization

def test_data_pipeline():
    settings = {"data_file": "sample_data.json", "visualization_params": {"node_size": 10}}
    data = load_data(settings["data_file"])
    tree = generate_tree(data)
    viz = Visualization(tree, settings)
    assert viz.tree is not None