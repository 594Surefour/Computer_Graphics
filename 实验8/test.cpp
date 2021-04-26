#include <iostream>
using namespace std;

int  comb(int m, int k)//(C(m,k))
{
	int i,count = 0;
	for (i = m; i >= k; i--)
	{
		if (k>1)
		{	comb(i - 1, k - 1);	}
		else
		{	count++;	}
	}
	return count;
}

int main(void)
{
    int n,k;
    cin>>n>>k;
    cout<<comb(n,k)<<endl;
    return 0;
}