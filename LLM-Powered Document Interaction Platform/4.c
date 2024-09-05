#include<stdio.h>
#define pi 3.14
int main()
{
	float r, area;
	printf("Enter the radius of the circle = ");
	scanf("%f",&r);
	area = pi*r*r;
	printf("The area of the circle is =%f", area);
	return 0;
}
