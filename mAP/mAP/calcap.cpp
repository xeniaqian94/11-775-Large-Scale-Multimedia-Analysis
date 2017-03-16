#include "calcap.h"
#include <cstdlib>
using namespace std;

float calcap(float* labels, float* rank, int len)
{
    int* idx = (int*)std::malloc(len*sizeof(int));
    assert(idx != NULL);

    for(int i = 0; i < len; i++)
    {
        idx[i] = i;
    }
    for(int i = 0; i < len; i++)
    {
        for(int j = i + 1; j < len; j++)
        {
            if(rank[i] < rank[j])
            {
                //swap
                float temp = rank[i];
                rank[i] = rank[j];
                rank[j] = temp;

                //swap idx
                int temp_index = idx[i];
                idx[i] = idx[j];
                idx[j] = temp_index;
            }
        }
    }
    int poss = 0;
    for(int i = 0; i < len; i ++)
    {
        if(labels[i] == 1)
        {
            poss ++;
        }
    }
    float accpos = 0;
    float ap = 0;
    for(int u = 0; u < len; u++)
    {
        if(labels[idx[u]] == 1)
        {
            accpos = accpos + 1;
        }
        if(u == (len - 1))
        {
        }
        else if(rank[u] != rank[u+1])
        {
        }
        else
        {
            continue;
        }
        if(accpos != 0)
        {
            vector<int> above_threshold;
            for(int j = 0; j <= u; j++)
            {
                above_threshold.push_back(idx[j]);
            }
            vector<float> retrieved;
            for(int j = 0; j <= u; j++)
            {
                retrieved.push_back(labels[above_threshold[j]]);
            }
            int re_pos = 0;
            for(int t = 0; t <= u; t++)
            {
                if(retrieved[t] == 1)
                {
                    re_pos ++;
                }
            }
            ap = ap + (float) re_pos / (u+1) * accpos;
            accpos = 0;
        }
    }
    ap = ap / poss;
    std::free(idx);
    return ap;
}
