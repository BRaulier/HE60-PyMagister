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
    std::string pathToDatabase = "/Users/braulier/Documents/DataBase";
    std::string pathToLogFile = "/Users/braulier/Documents/DataBase/logfile.txt";
    std::fstream logFile;
    int mkdir_status;
    void createDir() {
        if (IsPathExist(pathToDatabase) == 0){
            mkdir_status = mkdir(pathToDatabase.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        }
    }
    void setSimPath(const char* pathToSim){
        pathToSimulationResults = pathToSim;
    }
    void createLogFile(){
        if (IsPathExist(pathToLogFile) == 0){
            std::ofstream outfile (pathToLogFile);
            outfile.close();
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
        std::fstream newLogFile;
        const char* pathToNewLogFile = "/Users/braulier/Documents/DataBase/newlogfile.txt";
        std::string line;
        logFile.open(pathToLogFile, std::ios::in);
        newLogFile.open(pathToNewLogFile, std::ios_base::app);
        int i = 1;
        while(getline(logFile, line)){
            std::string pathToResultsFolder = pathToDatabase+"/"+line;
            if (IsPathExist(pathToResultsFolder) == 0){
            } // do nothing
            else {
                std::cout << pathToResultsFolder;
                
                if (IsPathExist(pathToResultsFolder+"/hermes.pickle") &&
                    IsPathExist(pathToResultsFolder+"/zenith_profiles.txt") &&
                    IsPathExist(pathToResultsFolder+"/eudos_iops.csv")){
                    newLogFile << i << std::endl;
                    i = i + 1;
                }
                else {
                    std::__fs::filesystem::remove_all(pathToResultsFolder); // Deletes one or more files recursively.

                }
              }
        }
        logFile.close();
        std::remove(pathToLogFile.c_str()); // Remove old LogFile
        newLogFile.close();
        rename(pathToNewLogFile, pathToLogFile.c_str()); // Replace the oldLogFile with the new one
    }
};


int main(int argc, char** argv) {
    DataBase myObj;   
    myObj.initialize(argv[1]);
//    myObj.writeToLogFile("1");
//    myObj.writeToLogFile("2");
//    myObj.writeToLogFile("3");
//    myObj.writeToLogFile("4");
    myObj.verifyLogFile();

    
    return 0;
}
