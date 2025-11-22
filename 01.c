#include<stdio.h>
int main(){
    int num=0;
    scanf("%d",&num);
    for(int i=0;i<num;i++){
        for(int j=0;j<num;j++){
            printf("*");
        }
        if(i!=num-1)
            printf("\n");
    }
    return 0;
}