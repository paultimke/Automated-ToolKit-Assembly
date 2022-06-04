/**
 * @file wrapper.cpp
 * @brief  The purpose of this file is to create an exectuable
 *         that can be moved anywhere in the computer and run 
 *         by double-clicking to run the main python script without
 *         having to manually call the python interpreter. This, with
 *         the intention of being friendlier to the user.
 */

#include <string>
#include <cstdlib>

int main()
{
    const std::string PATH = "/Users/paultimke/dev/Python_projects/ToolKits";
    const std::string RUN_CMD = "python3 main.py";

    std::string command = "cd " + PATH + "\n" + RUN_CMD;

    system(command.c_str());

    return 0;
}