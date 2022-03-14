include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/lib")
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/lib/date")
include(FetchContent)
FetchContent_Declare(
googletest
GIT_REPOSITORY https://github.com/google/googletest.git
GIT_TAG main
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)
add_executable(unit_tests
calc_test.cpp
../src/AgentFactory.cpp
../src/AgentImmediate.cpp
../src/AlgorithmMinCov.cpp
../src/calc.cpp
../src/Engine.cpp
../src/Monitor.cpp
../src/PetriNetwork.cpp
../src/PlaceTransitionNet.cpp
../src/pugixml.cpp
../src/Queue.cpp
../src/ReadXML.cpp
../src/ReadJSON.cpp
../src/TemporalHourAgent.cpp
../src/TemporalMicroAgent.cpp
../src/TemporalMilliAgent.cpp
../src/TemporalMinuteAgent.cpp
../src/TemporalNanoAgent.cpp
../src/TemporalPlaceTransitionNet.cpp
../src/TemporalSecondAgent.cpp
)
set_property(TARGET unit_tests PROPERTY CXX_STANDARD 20)
target_link_libraries(unit_tests PRIVATE sut gtest_main)
target_link_libraries(unit_tests PUBLIC tbb)
include(GoogleTest)
gtest_discover_tests(unit_tests)