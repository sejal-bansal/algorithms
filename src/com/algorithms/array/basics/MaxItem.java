package com.algorithms.array.basics;

public class MaxItem {
    public static void main(String[] args) {
        int[] arr = {2, 56, 8, 45, 90};
        System.out.println("Max Value in the array: "+max(arr));
        System.out.print("Between the Range: "+maxRange(arr,1,3));

    }

    static int max(int[] arr){
        int maxvalue = arr[0];
        for(int i = 1; i < arr.length; i++){
            if(arr[i] > maxvalue){
                maxvalue = arr[i];
            }
        }
        return maxvalue;
    }

    static int maxRange(int[] arr, int start, int end){
        int maxvalue = arr[start];
        for(int i = start; i <= end; i++){
            if(arr[i] > maxvalue){
                maxvalue = arr[i];
            }
        }
        return maxvalue;
    }
}
