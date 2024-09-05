#include<iostream>
using namespace std;
class shape
{
    public:
    int width;
    float height;
    void data()
    {
        cout<<"Enter width:";
        cin>>width;
        cout<<"Enter height:";
        cin>>height;
    }
};
class triangle:public shape
{
    public:
    float base;
    float area1;
    // void data()
    // {
    //     shape::data();
    //     cout<<"Enter Base:";
    //     cin>>base;
    // }
    void area()
    {
        area1=(width*height)*(0.5);
        cout<<"Area of triange is:"<<area1<<endl;
    }
};
class rectangle:public shape
{
    public:
    int lenght;
    float area2;
    // void data()
    // {
    //     shape::data();
    //     cout<<"Enter Length:";
    //     cin>>lenght;
    // }
    void area()
    {
        area2=lenght*width;
        cout<<"Area of rectangle is:"<<area2<<endl;
    }
};
int main()
{
    rectangle r;
    triangle t;
    r.shape::data();
    // t.data();
    t.area();
    // r.data();
    r.area();
    return 0;
}
