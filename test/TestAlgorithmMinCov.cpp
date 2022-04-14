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

TEST_F(AlgorithmMinCovTestSuite, minCovTestProdCons)
{
    std::string input_filename = "../../test/petri_nets/prod_cons.json";
    std::string output_filename = "./mincov_out.json";

    // Validate input filename

    std::ifstream file(input_filename.c_str());
    if (file.bad() || !file.is_open())
    {
        FAIL() << "File " << input_filename << " not found";
    }

    // Run the minCov algorithm
    auto engine = std::make_unique<Engine>();
    engine->run(std::move(input_filename), 1);

    // Validate output filename

    std::ifstream file_out(output_filename.c_str());
    if (file_out.bad() || !file_out.is_open())
    {
        FAIL() << "File " << output_filename << " not found";
    }

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
        "[1 0 0 0 1 1 0 0 1 ]"};

    json output_json = json::parse(file_out);

    for (json node : output_json["nodes"])
    {
        // Check if node marking is in the set of markings
        std::string node_marking = node["state"];
        ASSERT_TRUE(markings.find(node_marking) != markings.end());
    }
};

TEST_F(AlgorithmMinCovTestSuite, minCovTestOmegaCuatro)
{
    std::string input_filename = "../../test/petri_nets/omega_4p.json";
    std::string output_filename = "./mincov_out.json";

    // Validate input filename

    std::ifstream file(input_filename.c_str());
    if (file.bad() || !file.is_open())
    {
        FAIL() << "File " << input_filename << " not found";
    }

    // Run the minCov algorithm
    auto engine = std::make_unique<Engine>();
    engine->run(std::move(input_filename), 1);

    // Validate output filename

    std::ifstream file_out(output_filename.c_str());
    if (file_out.bad() || !file_out.is_open())
    {
        FAIL() << "File " << output_filename << " not found";
    }

    // Then we read the JSON file outputted by the algorithm
    std::unordered_set<std::string> markings{
        "[1 0 0 0 ]",
        "[0 0 0 1 ]", // TODO: El error
        "[0 1 0 0 ]",
        "[1 0 W 0 ]",
        "[0 1 W 0 ]",
        "[0 0 W 1 ]"};

    json output_json = json::parse(file_out);

    for (json node : output_json["nodes"])
    {
        // Check if node marking is in the set of markings
        std::string node_marking = node["state"];
        ASSERT_TRUE(markings.find(node_marking) != markings.end());
    }
};

TEST_F(AlgorithmMinCovTestSuite, minCovTestEjemplo4)
{
    std::string input_filename = "../../test/petri_nets/4.json";
    std::string output_filename = "./mincov_out.json";

    // Validate input filename

    std::ifstream file(input_filename.c_str());
    if (file.bad() || !file.is_open())
    {
        FAIL() << "File " << input_filename << " not found";
    }

    // Run the minCov algorithm
    auto engine = std::make_unique<Engine>();
    engine->run(std::move(input_filename), 1);

    // Validate output filename

    std::ifstream file_out(output_filename.c_str());
    if (file_out.bad() || !file_out.is_open())
    {
        FAIL() << "File " << output_filename << " not found";
    }

    // Then we read the JSON file outputted by the algorithm
    std::unordered_set<std::string> markings{
        "[1 0 0 ]",
        "[1 W 0 ]",
        "[0 0 1 ]", // TODO: El error
        "[0 W 1 ]"};

    json output_json = json::parse(file_out);

    for (json node : output_json["nodes"])
    {
        // Check if node marking is in the set of markings
        std::string node_marking = node["state"];
        ASSERT_TRUE(markings.find(node_marking) != markings.end());
    }
};
