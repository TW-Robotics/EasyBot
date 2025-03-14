# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_easyrobot_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED easyrobot_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(easyrobot_FOUND FALSE)
  elseif(NOT easyrobot_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(easyrobot_FOUND FALSE)
  endif()
  return()
endif()
set(_easyrobot_CONFIG_INCLUDED TRUE)

# output package information
if(NOT easyrobot_FIND_QUIETLY)
  message(STATUS "Found easyrobot: 0.0.0 (${easyrobot_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'easyrobot' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT easyrobot_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(easyrobot_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${easyrobot_DIR}/${_extra}")
endforeach()
