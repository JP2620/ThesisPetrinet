#include <gtest/gtest.h>
#include "../include/calc.h"
#include "../include/Engine.hpp"
#include <string>
class CalcTestSuite : public ::testing::Test
{
protected:
  Calc sut_;
  Engine engine;
};

TEST_F(CalcTestSuite, SumAddsTwoInts)
{
  EXPECT_EQ(4, sut_.Sum(2, 2));
}
TEST_F(CalcTestSuite, MultiplyMultipliesTwoInts)
{
  EXPECT_EQ(12, sut_.Multiply(3, 4));
}

TEST_F(CalcTestSuite, ValidateFilename)
{
  std::string filename = "test/calc_test.cpp";
  EXPECT_EQ(true, engine.validateFilename(filename));
}
