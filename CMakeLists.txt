cmake_minimum_required(VERSION 3.24...4.0)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

option(BUILD_DEPS OFF)

find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED
  ${SKBUILD_SABI_COMPONENT}
)

include(UseCython)
include(GNUInstallDirs)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

if (NOT "${SKBUILD_SABI_VERSION}" STREQUAL "")
  if ("${SKBUILD_SABI_VERSION}" VERSION_LESS "3.11")
    message(FATAL_ERROR "ABI3 requires python>=3.11")
  endif()
  set(USE_SABI USE_SABI ${SKBUILD_SABI_VERSION})
endif()

cython_transpile(src/cy_src/cy_polygons.pyx LANGUAGE C OUTPUT_VARIABLE cy_polygons_c)
python_add_library(cy_polygons
                   MODULE "${cy_polygons_c}"
                   src/cy_src/c_point_in_polygon.c
                   WITH_SOABI
                   ${USE_SABI}
                  )
target_link_libraries(cy_polygons PUBLIC Python::NumPy)
install(TARGETS cy_polygons DESTINATION geometry_utils)

cython_transpile(src/cy_src/cy_line_crossings.pyx LANGUAGE C OUTPUT_VARIABLE cy_line_crossings_c)
python_add_library(cy_line_crossings MODULE "${cy_line_crossings_c}" WITH_SOABI ${USE_SABI})
target_link_libraries(cy_line_crossings PUBLIC Python::NumPy)
install(TARGETS cy_line_crossings DESTINATION geometry_utils)

cython_transpile(src/cy_src/cy_rect.pyx LANGUAGE C OUTPUT_VARIABLE cy_rect_c)
python_add_library(cy_rect MODULE "${cy_rect_c}" WITH_SOABI ${USE_SABI})
target_link_libraries(cy_rect PUBLIC Python::NumPy)
install(TARGETS cy_rect DESTINATION geometry_utils)
