#include <string>
void readFileTest();
void minCovTest();

int main(int argc, char *argv[])
{
  if (argc < 2 || argv[1] == std::string("1"))
    readFileTest();
  if (argc < 2 || argv[1] == std::string("2"))
    minCovTest();
}