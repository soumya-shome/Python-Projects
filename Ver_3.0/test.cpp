#include<iostream>
using namespace std;
int main(){
    enum days 
    {
        mon,tues,wed ,thurs,fri,sat,sun
    };
    for (int num=mon;num<=sun;num++)
        cout<<num++ +(days(num));
    return 0;
}