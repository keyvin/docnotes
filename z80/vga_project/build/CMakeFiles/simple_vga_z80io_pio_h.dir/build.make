# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/keyvin/vga_project

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/keyvin/vga_project/build

# Utility rule file for simple_vga_z80io_pio_h.

# Include the progress variables for this target.
include CMakeFiles/simple_vga_z80io_pio_h.dir/progress.make

CMakeFiles/simple_vga_z80io_pio_h: z80io.pio.h


z80io.pio.h: ../z80io.pio
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/keyvin/vga_project/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating z80io.pio.h"
	pioasm/pioasm -o c-sdk /home/keyvin/vga_project/z80io.pio /home/keyvin/vga_project/build/z80io.pio.h

simple_vga_z80io_pio_h: CMakeFiles/simple_vga_z80io_pio_h
simple_vga_z80io_pio_h: z80io.pio.h
simple_vga_z80io_pio_h: CMakeFiles/simple_vga_z80io_pio_h.dir/build.make

.PHONY : simple_vga_z80io_pio_h

# Rule to build all files generated by this target.
CMakeFiles/simple_vga_z80io_pio_h.dir/build: simple_vga_z80io_pio_h

.PHONY : CMakeFiles/simple_vga_z80io_pio_h.dir/build

CMakeFiles/simple_vga_z80io_pio_h.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/simple_vga_z80io_pio_h.dir/cmake_clean.cmake
.PHONY : CMakeFiles/simple_vga_z80io_pio_h.dir/clean

CMakeFiles/simple_vga_z80io_pio_h.dir/depend:
	cd /home/keyvin/vga_project/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/keyvin/vga_project /home/keyvin/vga_project /home/keyvin/vga_project/build /home/keyvin/vga_project/build /home/keyvin/vga_project/build/CMakeFiles/simple_vga_z80io_pio_h.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/simple_vga_z80io_pio_h.dir/depend

