#include <algorithm>
#include <iostream>
#include <fstream>
#include <streambuf>
#include <string>
#include <sstream>

#include "zlib.h"

// trim from start (in place)
static inline void ltrim(std::string &s) {
  s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) {
      return !std::isspace(ch);
  }));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
  s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
      return !std::isspace(ch);
  }).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
  ltrim(s);
  rtrim(s);
}

int main() {

  // Open NASDAQ file
  std::ifstream inFile("sp_list.txt");
  if(!inFile) {
    std::cout << "Cannot open input file.\n";
    return 1;
  }

  // Open output file
  # std::ofstream outFile("C:\\Users\\Matt\\Google Drive\\business_stuff\\websites\\plutocracy\\plutocracy.js");

  // Names declaration
  std::string names = "var names = [";

  // Ticker declaration
  std::string tickers = "var tickers = [";

  bool start = true;
  std::string line;
  std::string endLine = "File";
  std::string name, check, ticker;
  
  size_t firstBar, secondBar, dashPos;
  size_t pos, startPos, endPos;  
  
  while(inFile) {

    // Check for last line
    getline(inFile, line);
    if(line.substr(0, endLine.size()) != endLine) {

      // Split line into tokens
      tokens = line.split()
    
      // Remove periods
      name = line.substr(secondBar+1, dashPos - (secondBar + 1));
      pos = name.find(".");
      while(pos != std::string::npos) {
        name = name.substr(0, pos) + name.substr(pos + 1, std::string::npos);
        pos = name.find(".");
      }

      // Remove commas
      pos = name.find(",");
      while(pos != std::string::npos) {
        name = name.substr(0, pos) + name.substr(pos + 1, std::string::npos);
        pos = name.find(",");
      }

      // Remove text in parentheses
      startPos = name.find("(");
      while(startPos != std::string::npos) {
        endPos = name.find(")", startPos + 1);
        name = name.substr(0, startPos) + name.substr(endPos + 1, std::string::npos);
        startPos = name.find("<rStart:");
      }        
      
      // Change quotes
      pos = name.find("\'");
      if(pos != std::string::npos) {
        name = name.substr(0, pos) + "\\'" + name.substr(pos + 1, std::string::npos);
      }

      // Check if there's already a similar entry in the list
      trim(name);
      check = std::string("\'").append(name).append(" (");
      if(names.find(check) == std::string::npos) {

        // Write ticker symbol to list
        ticker = line.substr(firstBar + 1, secondBar - (firstBar + 1));
        tickers.append(std::string("\'"));
        tickers.append(ticker).append(" (").append(name).append(")");
        tickers.append(std::string("\', "));

        // Write name to list
        names.append("\'");
        names.append(name).append(" (").append(ticker).append(")");
        names.append("\', ");
      }
    }
  }

  // Write strings to file
  names.erase(names.end()-2, names.end());
  names.append("];");
  tickers.erase(tickers.end()-2, tickers.end());
  tickers.append("];");

  // Read code from JS file
  std::ifstream program("program.js");
  std::string program_code((std::istreambuf_iterator<char>(program)),
                            std::istreambuf_iterator<char>());
  
  // std::ostringstream outStream;
  // outStream << names << std::endl << std::endl << tickers << std::endl << std::endl << program_code << std::endl;

  #outFile << names << std::endl << std::endl << tickers << std::endl << std::endl << program_code << std::endl;
  
  // Close streams
  inFile.close();
  #outFile.close();
  
  // Compress plutocracy.js to plutocracy.min.js
  /*
  gzFile gzfp = gzopen("C:\\Users\\Matt\\Google Drive\\business_stuff\\websites\\plutocracy\\plutocracy.min.js", "wb");
  gzwrite(gzfp, outStream.str().data(), outStream.str().size());
  gzclose(gzfp);
  */
  return 0;
}