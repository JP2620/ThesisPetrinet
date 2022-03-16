#include <unordered_set>
#include <gtest/gtest.h>
#include "../include/AlgorithmMinCov.hpp"
#include "../include/Engine.hpp"
#include "../lib/json.hpp"

using json = nlohmann::json;

class AlgorithmMinCovTestSuite : public ::testing::Test
{
protected:
    AlgorithmMinCov sut_;
};

TEST_F(AlgorithmMinCovTestSuite, minCovTest)
{
    std::string input_filename = "../../test.json";
    std::string output_filename = "./mincov_aout.json";

    std::ifstream file(input_filename.c_str());
    if (file.bad() || !file.is_open())
    {
        FAIL() << "File " << input_filename << " not found";
    }

    // First we run the minCov algorithm
    auto engine = std::make_unique<Engine>();
    engine->run(std::move(input_filename), 1);

    std::ifstream file_out(output_filename.c_str());
    if (file_out.bad() || !file_out.is_open())
    {
        FAIL() << "File " << output_filename << " not found";
    }
    FAIL();

    // Then we read the JSON file outputted by the algorithm
    std::unordered_set<std::string> markings{
        "[1 0 0 1 1 0 1 0 0 ]",
        "[0 1 0 0 0 0 1 0 0 ]",
        "[0 0 1 0 1 1 1 0 0 ]",
        "[1 0 0 0 1 1 1 0 0 ]",
        "[0 0 1 0 0 0 0 1 0 ]",
        "[1 0 0 0 0 0 0 1 0 ]",
        "[0 0 1 1 1 0 0 0 1 ]",
        "[1 0 0 1 1 0 0 0 1 ]",
        "[0 0 1 1 1 0 1 0 0 ]",
        "[0 1 0 0 0 0 0 0 1 ]",
        "[0 0 1 0 1 1 0 0 1 ]",
        "[1 0 0 0 1 1 0 0 0 ]"};

    json output_json = json::parse(output_filename);

    for (json node : output_json["nodes"])
    {
        std::string node_marking = node["state"];
        // Check if node marking is in the set of markings
        ASSERT_TRUE(markings.find(node_marking) != markings.end());
    }
    EXPECT_EQ(0, 0);
};
