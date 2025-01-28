set(MUJOCO_VERSION "3.2.7")

include(FetchContent)
set(FETCHCONTENT_QUIET OFF)

set(CMAKE_POLICY_DEFAULT_CMP0077 NEW)
set(ENABLE_DOUBLE_PRECISION ON)
set(CCD_HIDE_ALL_SYMBOLS ON)
set(BUILD_TESTING OFF)
# I have no idea how to apply a patch after mujoco fetches all its dependencies
# For now I explicitly fetch them while using the same version
FetchContent_Declare(
  ccd
  GIT_REPOSITORY https://github.com/danfis/libccd.git
  # https://github.com/google-deepmind/mujoco/blob/main/cmake/MujocoDependencies.cmake#L33-L36
  GIT_TAG 7931e764a19ef6b21b443376c699bbc9c6d4fba8
  GIT_PROGRESS TRUE
  UPDATE_DISCONNECTED 1
  EXCLUDE_FROM_ALL
  PATCH_COMMAND git apply ${CMAKE_SOURCE_DIR}/dependencies/patches/libccd.patch)
FetchContent_MakeAvailable(ccd)

set(MUJOCO_BUILD_TESTS OFF)
set(MUJOCO_BUILD_EXAMPLES OFF)
set(MUJOCO_BUILD_SIMULATE OFF)
set(MUJOCO_TEST_PYTHON_UTILS OFF)
FetchContent_Declare(
  mujoco
  GIT_REPOSITORY https://github.com/google-deepmind/mujoco
  GIT_TAG ${MUJOCO_VERSION}
  GIT_PROGRESS TRUE
  UPDATE_DISCONNECTED 1
  EXCLUDE_FROM_ALL
  PATCH_COMMAND git apply ${CMAKE_SOURCE_DIR}/dependencies/patches/mujoco.patch)
FetchContent_MakeAvailable(mujoco)

find_package(Python3 REQUIRED)
execute_process(
  COMMAND ${Python3_EXECUTABLE} ${CMAKE_SOURCE_DIR}/src/parse_mjxmacro.py
          ${mujoco_SOURCE_DIR} RESULT_VARIABLE result)

