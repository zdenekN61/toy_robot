"""Toy robot task

   Command:
       - PLACE x,y, facing
           -facing(NOTRH, WEST, EAST, SOUTH)
       - REPORT
       - MOVE
       - LEFT, RIGHT
       - END(stopping)
"""

import os
import re
import sys
from robot_toy import robot_toy

_all__ = ["Robot"]

MAX_UNITS = 5
ROTATION_SUPPORTED = ["north", "east" , "south", "west"]
FACING_SUPPORTED = {"north": ["y", "+"], "east": ["x", "+"],
                    "south": ["y", "-"], "west": ["x", "-"]}
COMMAND = ["move", "place", "left", "right", "report", "end"]

class Robot:
    def __init__(self):
        self.robot = robot_toy()
        self._input_command()

    # Reads user imput.
    def _input_command(self):
        while(True):
           print ('Your command:')
           command = input()
           command = command.lower()
           list_c = self._read_command(command)
           self._executing_commands(list_c)

    # Exeting commands.
    def _executing_commands(self, commands):
        count_comm = len(commands)
        first_place = False
        for comm in range(0, len(commands)):
            is_valid = self._check_command(commands[comm])
            if is_valid:
                if commands[comm] == "place":
                    if (comm+1) < len(commands):
                        first_place = self._command_PLACE(commands[comm:])
                elif first_place:
                    if commands[comm] == "report":
                        self._command_REPORT()
                    elif commands[comm] == "move":
                        self._command_MOVE()
                    elif commands[comm] in ["left", "right"]:
                        self._command_ROTATE(commands[comm])
                    elif commands[comm] == "end":
                        self._exit()

    # Check command.
    def _check_command(self, command):
        valid = True
        if command not in COMMAND:
            valid = False
        return valid

    # Start over, new command.
    def _start_over(self):
        self._input_command()

    # Processing commands.
    def _read_command(self, command):
        comm_list = re.split(" ", command)
        return comm_list

    # Calculating 'MOVE' command(+1 step toward my facing).
    def _command_MOVE(self):
        face = self.robot['face']
        way = FACING_SUPPORTED[face]
        curr_pos = self.robot[way[0]]
        if way[1] == "+":
            new_pos = (curr_pos+1)
            if new_pos < MAX_UNITS and new_pos >= 0:
                self.robot[way[0]] = new_pos
        elif way[1] == "-":
            new_pos = (curr_pos-1)
            if new_pos < MAX_UNITS and new_pos >= 0:
                self.robot[way[0]] = new_pos

    # Calculating 'PLACE' command.
    def _command_PLACE(self, comm):
        place_success = False
        if comm:
            x_y_f = re.split(',', comm[1])
            if len(x_y_f) == 3:
                new_x = x_y_f[0]
                new_y = x_y_f[1]
                new_face = x_y_f[2]
                try:
                    self.robot['x'] = int(new_x)
                    self.robot['y'] = int(new_y)
                    if new_face in ROTATION_SUPPORTED: 
                        self.robot['face'] = new_face
                        place_success = True
                except:
                    err_message = ("Something went wrong with your command: "
                                   "%s, check it and try again." % comm[1])
                    print (err_message)
            
        return place_success

    # Calculating 'REPORT' command.
    def _command_REPORT(self):
        x_pos = self.robot['x']
        y_pos = self.robot['y']
        facing = self.robot['face']
        report = r"%s,%s,%s" %(x_pos, y_pos, facing)
        print ('Output:' + report.upper())

    # Rotate(left, right)
    def _command_ROTATE(self, direction):
        curr_face = self.robot['face']
        curr_face_index = ROTATION_SUPPORTED.index(curr_face)
        new_face_index = 0
        if direction == "right":
            if (curr_face_index+1) < len(ROTATION_SUPPORTED):
                new_face_index = (curr_face_index+1)
        elif direction == "left":
            new_face_index = 3
            if (curr_face_index-1) >= 0:
                new_face_index = (curr_face_index-1)
        self.robot['face'] = ROTATION_SUPPORTED[new_face_index]

    # Calculating new F(acing) position.
    def _position_F(self, move_to):
        if move_to in FACING_SUPPORTED:
            self.robot['face'] = move_to
 
    # Stopping.
    def _exit(self):
        sys.exit()

if __name__=='__main__':
    robot = Robot()
