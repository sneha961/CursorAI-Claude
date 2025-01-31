# 2D Car Racing Game

<img width="898" alt="image" src="https://github.com/user-attachments/assets/af679de5-5b14-48c7-a1aa-7cdd80d94a8b" />

A simple 2D car racing game built with Python and Pygame where players control a car to avoid oncoming traffic.

## Project Overview

This game was created as an experimental project to test the capabilities of Claude-3.5-sonnet, an AI language model by Anthropic. The entire codebase was generated through a series of prompts and interactions with the AI, demonstrating the potential of AI-assisted game development.

### Sample Prompts Used

1. Initial Game Creation:
```
"build a 2D car racing game in which the car keeps moving forward while avoiding the obstacles which are actually other cars"
```

2. Image Integration:
```
"I have moved all the images mpcCar.png, playerCar.png, tree.png with the 'images' subfolder in the same directory. Can you modify the path accordingly for the images in the code"
```

The AI successfully generated the complete game structure, including the main game logic, project documentation, and necessary configuration files.

## Prerequisites

- Python 3.6 or higher
- Pygame library

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:


## How to Play

1. Run the game:

2. Game Controls:
   - LEFT ARROW: Move car left
   - RIGHT ARROW: Move car right
   - Close window to quit game

3. Game Rules:
   - Avoid the black cars coming from the top
   - Each successfully avoided car adds 1 point to your score
   - Game ends if you collide with any obstacle car

## Project Structure

```
CarRace/
├── main.py
├── requirements.txt
├── README.md
└── images/
    ├── playerCar.png
    ├── npcCar.png
    ├── tree.png
    └── bkc.png
```

## Features

- Simple and intuitive controls
- Score tracking
- Scrolling road effect
- Increasing difficulty as you play
- Collision detection

## Future Enhancements

- Add car sprites instead of rectangles
- Include sound effects
- Add different types of obstacles
- Implement varying difficulties
- Add a high score system
- Include power-ups
- Add multiple lanes
- Implement a proper game over screen

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## License

This project is open source and available under the MIT License.
