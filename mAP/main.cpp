#include <iostream>
#include <stdlib.h>
#include <cstdlib>
#include <fstream>
#include "calcap.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    if(argc != 3)
    {
        cout << "Usage: ./ap label_file prediction_file" << endl;
        return 1;
    }
    char* label_file = argv[1];
    char* prediction_file = argv[2];


    // Reading the label file
    ifstream ifs;
    ifs.open(label_file);
    string line;
    int num = 0;
    while(getline(ifs, line))
    {
        num ++;
    }
    ifs.close();
    float* label = (float*)std::malloc(sizeof(float)*num);
    int index = 0;
    ifs.open(label_file);
    while(getline(ifs, line))
    {
        label[index++] = (float)atof(line.c_str());
    }
    ifs.close();
    assert(num == index);
    float* prediction = (float*)std::malloc(sizeof(float)*num);
    ifs.open(prediction_file);
    index = 0;
    while(getline(ifs, line))
    {
        prediction[index++] = (float)atof(line.c_str());
    }
    ifs.close();
    assert(num == index);

    float ap = calcap(label, prediction, num);

    cout << "ap: " << ap << endl;
}
