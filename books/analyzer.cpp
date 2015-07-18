#include <QCoreApplication>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <algorithm>
#include <fstream>
#include <map>
#include <string>
#include <cstring>

using namespace std;

typedef struct wordpair {
    int count;
    string word;
} word_pair;

bool sorter (word_pair i,word_pair j) { return (i.count>j.count); }

int main(int argc, char *argv[])
{
    int numwords = 0;
    int pauser = 0;
    ifstream input;
    ofstream output;
    string sinput;
    vector<word_pair> v;
    word_pair pair;
    string filetoproc;
    string outputfile;
    if (argc > 1)
        filetoproc = argv[1];
    else {
        cout << "No arg";
        return 1;
    }
    outputfile = filetoproc;
    outputfile = filetoproc;
    outputfile.append(".out");
    cout << filetoproc << endl;
    input.open(filetoproc.c_str());
    output.open(outputfile.c_str());
    map <string, int> wordcount;
    map <int, string> index_map;
    while (input >> sinput){
        //cout << sinput << endl;
       // sinput = "3,";
        badgoto:
        //cout << sinput << endl;
        if (sinput.length()==1 || sinput.length() == 0) continue;
        while (sinput.length() !=1 && !isalpha(sinput[0]))
            sinput = sinput.substr(1, sinput.length());
        if (sinput.length() == 1) continue;

        while (sinput.length() != 0 && !isalpha(sinput[sinput.length()-1])){
            sinput = sinput.substr(0, sinput.length()-1);
         }

        for (int z = 0; z < sinput.length(); z++){
            sinput[z] = tolower(sinput[z]);
        }
        int pos = 0;
        pos = 0;
        string second;
        if ( (pos = sinput.find('--')) != -1) {
            if ((pos + 2) < sinput.length()){
                second = sinput.substr(pos+2);
                sinput = sinput.substr(0, pos);
                if (!isalpha(second[0])){
                    second = sinput.substr(1,sinput.length());
                }

            }
        }
        while (sinput.length() !=1 && !isalpha(sinput[0]))
            sinput = sinput.substr(1, sinput.length());
        while (sinput.length() != 0 && !isalpha(sinput[sinput.length()-1]))
            sinput = sinput.substr(0, sinput.length()-1);
        if (sinput[sinput.length()-1] == 's' && sinput.length() > 2 && sinput[sinput.length() -2]=='\''){
            sinput = sinput.substr(0, sinput.length() -2);
        }
        wordcount[sinput]++;
        if (second != ""){
            sinput = second;
            goto badgoto;
        }
    }


    for(map<string,int>::iterator it = wordcount.begin(); it != wordcount.end(); ++it) {

        pair.count = wordcount[it->first];
        pair.word = it->first;
        v.push_back(pair);
        numwords++;
    }


    sort(v.begin(), v.end(), sorter);

    for (int i = 0; i < v.size(); i++){
        output << v[i].count << " - " << v[i].word << endl;
    }
    output << numwords << endl;
    cout << "done" << endl;
    //cin >> pauser;
    return 0;


}
