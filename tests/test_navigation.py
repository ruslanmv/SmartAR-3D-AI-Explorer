# tests/test_navigation.py

import pytest
from app.modules.navigation import NavigationAssistance

@pytest.fixture
def navigation_instance():
    """
    Provides a fresh NavigationAssistance object with a mock building_model.
    """
    fake_building_model = {
        "geometry": None,
        "objects": [],
        "format": "OBJ"  # Just a stub
    }
    return NavigationAssistance(fake_building_model)

def test_start_navigation(navigation_instance, capsys):
    """
    Verify that calling start_navigation with a target name 
    sets the internal state and prints instructions.
    """
    # Initially, we are not navigating anywhere
    assert not navigation_instance.is_navigating
    assert navigation_instance.destination is None

    navigation_instance.start_navigation("fridge")
    assert navigation_instance.is_navigating
    assert navigation_instance.destination == "fridge"

    captured = capsys.readouterr()
    assert "Starting navigation towards 'fridge'" in captured.out
    assert "Begin walking toward fridge" in captured.out

def test_update_navigation_not_navigating(navigation_instance, capsys):
    """
    If we call update_navigation without having started navigation,
    it should do nothing.
    """
    navigation_instance.update_navigation()
    captured = capsys.readouterr()
    assert captured.out == ""

def test_update_navigation_in_progress(navigation_instance, capsys):
    """
    If navigation is in progress, update_navigation should print 
    a stub message indicating we are guiding the user.
    """
    navigation_instance.start_navigation("kitchen")
    capsys.readouterr()  # clear buffer

    navigation_instance.update_navigation(user_position=(0, 0, 0))
    captured = capsys.readouterr()
    assert "[Navigation] Currently guiding user... (stub update)" in captured.out

def test_stop_navigation(navigation_instance, capsys):
    """
    stop_navigation should reset the internal state and print a message
    if we were navigating.
    """
    navigation_instance.start_navigation("door")
    capsys.readouterr()  # clear buffer

    navigation_instance.stop_navigation()
    captured = capsys.readouterr()
    assert not navigation_instance.is_navigating
    assert navigation_instance.destination is None
    assert "Navigation to 'door' canceled or completed." in captured.out
