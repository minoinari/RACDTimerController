# CPack properties
if("${CPACK_BUILD_CONFIG}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  set_property(INSTALL "RACDTimerController/RACDTimerController.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "RACDTimerController.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  set_property(INSTALL "RACDTimerController/RACDTimerController.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "RACDTimerController.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  set_property(INSTALL "RACDTimerController/RACDTimerController.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "RACDTimerController.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  set_property(INSTALL "RACDTimerController/RACDTimerController.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "RACDTimerController.py")
endif()
if("${CPACK_BUILD_CONFIG}" MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  set_property(INSTALL "Timer/Timer.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "Timer.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  set_property(INSTALL "Timer/Timer.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "Timer.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  set_property(INSTALL "Timer/Timer.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "Timer.py")
elseif("${CPACK_BUILD_CONFIG}" MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  set_property(INSTALL "Timer/Timer.py" PROPERTY "CPACK_START_MENU_SHORTCUTS" "Timer.py")
endif()
