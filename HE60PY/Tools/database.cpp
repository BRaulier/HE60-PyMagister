//
//  database.cpp
//  
//
//  Created by Bastian Raulier on 2022-04-19.
//

#include "database.hpp"

bool IsPathExist(const std::string &s)
{
  struct stat buffer;
  return (stat (s.c_str(), &buffer) == 0);
}


class DataBase {
  public:
    const char* pathToSimulationResults;
    const char* pathToDatabase = "/Users/braulier/Documents/DataBase";
    const char* pathToLogFile = "/Users/braulier/Documents/DataBase/logfile.txt";
    std::fstream logFile;
    int mkdir_status;
    void createDir() {
        if (IsPathExist(pathToDatabase) == 0){
            mkdir_status = mkdir(pathToDatabase, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        }
    }
    void setSimPath(const char* pathToSim){
        pathToSimulationResults = pathToSim;
    }
    void createLogFile(){
        if (IsPathExist(pathToLogFile) == 0){
            std::ofstream outfile (pathToLogFile);
            outfile << "my text here!" << std::endl;
            outfile.close();
            std::cout << "File created";
        }
    }
    void initialize(const char* pathToSim){
        createDir();
        setSimPath(pathToSim);
        createLogFile();
    }
    void writeToLogFile(const char* string){
        logFile.open(pathToLogFile, std::ios_base::app);
        logFile << string << std::endl;
        logFile.close();
    }
    void verifyLogFile(){
        logFile.open(pathToLogFile,ios::in);
        while(getline(newfile, line)){
            if (IsPathExist(line) == 0){
                
            }
              }
    }
};


int main(int argc, char** argv) {
    DataBase myObj;   
    myObj.initialize(argv[1]);
    myObj.writeToLogFile("Dummy test");
    myObj.writeToLogFile("Dummy test 2");

    
    return 0;
}
