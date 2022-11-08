cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Release)
include(mu/bricks/support.cmake)

project(mu_package)
find_package(PkgConfig REQUIRED)

set(LIBS ${LIBS} pthread)

set(MU_DIR ${CMAKE_SOURCE_DIR}/mu/mu)
pkg_check_modules(GLIB REQUIRED poppler-glib)
pkg_check_modules(ICU REQUIRED icu-uc)

set(LIBS ${LIBS} ${GLIB_LINK_LIBRARIES} ${ICU_LINK_LIBRARIES})
set(INCLS ${INCLS} ${CMAKE_SOURCE_DIR}/mu/bricks ${MU_DIR} ${GLIB_INCLUDE_DIRS} ${ICU_INCLUDE_DIRS})
set(CFLAGS ${CFLAGS} ${GLIB_CFLAGS} ${ICU_CFLAGS})

add_executable(mu "${MU_DIR}/main.cpp" "${MU_DIR}/doc/convert.cpp")
add_executable(mu-pic "${MU_DIR}/pic.cpp")
add_executable(svgtex "${MU_DIR}/svgtex.cpp")

target_link_libraries(mu ${LIBS} )
target_link_libraries(mu-pic ${LIBS})
target_link_libraries(svgtex ${LIBS})

target_include_directories(mu SYSTEM PUBLIC  ${INCLS})
target_include_directories(mu-pic SYSTEM PUBLIC ${INCLS})
target_include_directories(svgtex SYSTEM PUBLIC ${INCLS})

target_compile_options(mu PUBLIC ${CFLAGS})
target_compile_options(mu-pic PUBLIC ${CFLAGS})
target_compile_options(svgtex PUBLIC ${CFLAGS})
