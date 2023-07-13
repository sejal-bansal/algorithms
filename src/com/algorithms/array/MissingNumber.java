package com.algorithms.array;

public class MissingNumber {

    public static void printArray(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static int findMissingNumber(int[] arr) {
        int n = arr.length + 1;
        int sum = n * (n + 1) / 2;
        for (int num : arr) {
            sum = sum - num;
        }
        return sum;
    }

    public static void main(String[] args) {
        int[] num = {1,2,3,4,5,7};
//        MissingNumber missingNumber = new MissingNumber();
//        missingNumber.findMissingNumber(num);
        int num1 = findMissingNumber(num);
        System.out.println(num1);
//        missingNumber.printArray();
    }
}
