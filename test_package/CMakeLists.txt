cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(APPLE OR MSVC)
    # TODO: test on mac and win is basically disabled
    add_executable(example example-mac.cpp)
else()
    add_executable(example example.cpp)
    target_link_libraries(example ${CONAN_LIBS})
endif()


# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
