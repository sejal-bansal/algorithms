package com.algorithms.array;

public class ZerosArray {
    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static void zerosToEnd(int[] arr, int n) {
        int j = 0;
        for (int i = 0; i < n; i++) {
            if (arr[i] != 0 && arr[j] == 0) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
            if (arr[j] != 0) {
                j++;
            }
        }
    }

    public static void main(String[] args) {
        int[] num = {9, 0, 8, 0, 7, 9};
        printArray(num);
        zerosToEnd(num,num.length);
        printArray(num);

        

    }
}
