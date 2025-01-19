cmake_minimum_required(
    VERSION 3.26)
project(Trekr
    LANGUAGES NONE
    VERSION 0.0.0
    DESCRIPTION "Trekr TODO"
    HOMEPAGE_URL "https://trekr.todo"
)

enable_testing()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/environment/cmake)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(TREKR_PYTHONPATH
    "${PROJECT_SOURCE_DIR}/source/package"
    "$ENV{PYTHONPATH}"
)
cmake_path(CONVERT "${TREKR_PYTHONPATH}" TO_NATIVE_PATH_LIST TREKR_PYTHONPATH)
string(TOLOWER ${CMAKE_HOST_SYSTEM_NAME} TREKR_HOST_SYSTEM_NAME_LOWER_CASE)

add_subdirectory(documentation)
add_subdirectory(source)
