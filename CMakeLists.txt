cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_BUILD_TYPE Debug)
include(mu/bricks/support.cmake)

project(mu_package)
find_package(PkgConfig REQUIRED)

set(LIBS ${LIBS} pthread)

# vcpkg
# ICU
find_package(ICU REQUIRED COMPONENTS uc dt in io)
set(LIBS ${LIBS}
 ${ICU_UC_LIBRARY_RELEASE}
 ${ICU_DT_LIBRARY_RELEASE}
 ${ICU_IN_LIBRARY_RELEASE}
 ${ICU_IO_LIBRARY_RELEASE})

# glib
pkg_search_module(GLIB2 REQUIRED glib-2.0 IMPORTED_TARGET)
set(LIBS ${LIBS} ${GLIB2_LINK_LIBRARIES})
set(INCLS ${INCLS} ${GLIB2_INCLUDE_DIRS})
set(CFLAGS ${CFLAGS} ${GLIB2_CFLAGS})

# poppler
find_package(unofficial-poppler CONFIG REQUIRED)
set(LIBS ${LIBS}
   unofficial::poppler::poppler-cpp 
   unofficial::poppler::poppler-private)

pkg_search_module(POPPLER REQUIRED poppler-glib IMPORTED_TARGET)
set(LIBS ${LIBS} ${POPPLER_LINK_LIBRARIES} 
"${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/lib/libgio-2.0.a"
"${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/lib/libgmodule-2.0.a"
"${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/lib/libgthread-2.0.a"
)
set(INCLS ${INCLS} ${POPPLER_INCLUDE_DIRS})
set(CFLAGS ${CFLAGS} ${POPPLER_CFLAGS})


# end of vcpkg

set(MU_DIR ${CMAKE_SOURCE_DIR}/mu/mu)

set(LIBS ${LIBS})
set(INCLS ${INCLS} ${CMAKE_SOURCE_DIR}/mu/bricks ${MU_DIR})

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
