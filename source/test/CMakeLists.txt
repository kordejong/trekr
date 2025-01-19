add_test(
    NAME python_tests
    COMMAND ${Python3_EXECUTABLE}
        -m unittest discover
        --verbose
        --start-directory ${CMAKE_CURRENT_SOURCE_DIR}
        --pattern "*_test.py"
)

set_tests_properties(python_tests
    PROPERTIES
        ENVIRONMENT_MODIFICATION
            PYTHONPATH=path_list_prepend:${PROJECT_SOURCE_DIR}/source/package
)
