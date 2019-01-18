cmake_minimum_required(VERSION 2.8)

project(rpg)
	

#For the shared library:
set ( PROJECT_LINK_LIBS ncurses)
link_directories( /usr/lib/)
 
add_executable(${PROJECT_NAME} "main.cpp" "world.cpp")
target_link_libraries(rpg ${PROJECT_LINK_LIBS} )
