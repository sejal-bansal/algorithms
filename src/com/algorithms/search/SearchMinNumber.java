package com.algorithms.search;

public class SearchMinNumber {
    public static void main(String[] args) {
        int[] arr = {10, 20, 78, 98, 67, 56, 80, -2};
        int target = 98;
        System.out.println(minNum(arr));
    }

    static int minNum(int[] arr){
        int min = arr[0];
        for (int i = 1; i < arr.length; i++){
            if(arr[i] < min){
                min = arr[i];
            }
        }
        return min;
    }
}
