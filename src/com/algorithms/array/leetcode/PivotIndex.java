package com.algorithms.array.leetcode;

public class PivotIndex {

    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int pivotIndex(int[] num) {
        int total_sum = 0;
        for (int i = 0; i < num.length; i++) {
            total_sum += num[i];
        }

        int left_sum = 0;
        for (int i = 0; i < num.length; i++) {
            if (i != 0) left_sum += num[i - 1];
            if (total_sum - left_sum - num[i] == left_sum) {
                return i;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] arr = {1, 7, 3, 6, 5, 6};
        int result = pivotIndex(arr);
        System.out.println("Pivot Index is: " + result);


    }
}
