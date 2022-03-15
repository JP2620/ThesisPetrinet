#include <gtest/gtest.h>
#include "../include/calc.h"
#include "../include/ReadJSON.hpp"
#include <string>
class ReadJSONTestSuite : public ::testing::Test
{
protected:
  ReadJSON sut_;
};

TEST_F(ReadJSONTestSuite, readFileTest)
{
  std::string filename = "../../test.json";
  EXPECT_EQ(1, sut_.readFile(filename));

  EXPECT_EQ(9, sut_.getNumberPlaces());
  EXPECT_EQ(6, sut_.getNumberTransitions());
  EXPECT_EQ(true, sut_.isTemporal());
  EXPECT_EQ(Timescale_Choice::unit::MILLISECOND, sut_.getTimeScale());
}
