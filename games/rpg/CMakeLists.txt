cmake_minimum_required(VERSION 2.8)

project(rpg)
	

#For the shared library:
#set ( PROJECT_LINK_LIBS ncurses)
#set ( CMAKE_BUILD_TYPE Debug)
find_package(SDL2 CONFIG REQUIRED)
#link_directories( /usr/lib/)
add_executable(${PROJECT_NAME} "main.cpp" "world.cpp" "screen.cpp" "controller.cpp")
#target_link_libraries(rpg ${PROJECT_LINK_LIBS} )
target_link_libraries(rpg PRIVATE SDL2::SDL2 SDL2::SDL2main)
