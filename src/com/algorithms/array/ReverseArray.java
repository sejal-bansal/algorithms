package com.algorithms.array;

public class ReverseArray {

    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static void reverseArray(int[] num, int start, int end) {
        while (start < end) {
            int temp = num[start];
            num[start] = num[end];
            num[end] = temp;
            start++;
            end--;
        }
    }

    public static void main(String[] args) {
        int[] num = {3, 4, 5, 6, 7};
        printArray(num);
        reverseArray(num, 0, num.length - 1);
        printArray(num);
    }

}
