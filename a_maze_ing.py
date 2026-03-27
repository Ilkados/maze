import sys
import random
from mazegen.maze import Maze
from mazegen.parser import load_config
from mazegen.io_handler import to_visual_grid, print_pretty_maze # <-- Import here

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = load_config(sys.argv[1])
        if "SEED" in config:
            random.seed(config["SEED"])

        maze = Maze(config["WIDTH"], config["HEIGHT"])
        maze.place_42_pattern()
        maze.generate(config["ENTRY"][0], config["ENTRY"][1])
        
        if not config["PERFECT"]:
            maze.make_imperfect()
        
        path, path_str = maze.solve(config["ENTRY"], config["EXIT"])

        # 1. Save the Hex file (Mandatory)
        maze.write_output(config["OUTPUT_FILE"], config["ENTRY"], config["EXIT"], path_str)

        # 2. Show the "Pretty" Maze in terminal (Visual Requirement)
        visual_grid = maze.get_visual_grid(config["ENTRY"], config["EXIT"], path)
        
        print("\n" + "="*30)
        print("   MAZE GENERATION COMPLETE")
        print("="*30 + "\n")
        
        print_pretty_maze(visual_grid) # <-- Call the pretty printer
        
        print(f"\nSuccess! Hex data saved to {config['OUTPUT_FILE']}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()