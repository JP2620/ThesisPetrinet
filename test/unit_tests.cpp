#include <string>
void readFileTest();

int main(int argc, char *argv[])
{
  if (argc < 2 || argv[1] == std::string("1"))
    readFileTest();
}