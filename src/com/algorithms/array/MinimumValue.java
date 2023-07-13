package com.algorithms.array;

public class MinimumValue {

    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int minimumArray(int[] arr) {
        if(arr == null || arr.length == 0){
            throw new IllegalArgumentException("Invalid Input");
        }
        int min = arr[0];
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] < min) {
                min = arr[i];
            }
        }
        return min;
    }

    public static int secondMaxValue(int[] arr){
        int max = Integer.MIN_VALUE;
        int secondMax = Integer.MIN_VALUE;
        for(int i = 0; i < arr.length; i++){
            if(arr[i] > max){
                secondMax = max;
                max = arr[i];
            }else if( arr[i] > secondMax && arr[i] != max){
                secondMax = arr[i];
            }
        } return secondMax;
    }

    public static void main(String[] args) {
        int[] num = {8, 7, 10, 46, 9, 1};
        printArray(num);
        int minValue = minimumArray(num);
        System.out.println("Minimum Value in an array: " + minValue);
        int secondMinValue = secondMaxValue(num);
        System.out.println("Second Maximum Value in an array: " + secondMinValue);
    }
}
