package com.algorithms.array;

public class ArrayUtil {
    public void printArray(int[] arr){
        int n = arr.length;
        for(int i =0; i < n; i++){
            System.out.println(arr[i] + "");
        }
    }
    public void arrayDemo(){
        int[] myArr = {1,2,4,3,5}; //default values
        printArray(myArr);
        System.out.println(myArr[myArr.length - 1]);
        System.out.println(myArr.length);
    }

    public static void main(String[] args) {
        ArrayUtil arrayUtil = new ArrayUtil();
        arrayUtil.arrayDemo();
    }
}
