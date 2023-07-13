package com.algorithms.array.leetcode;

public class RunningSum {

    public void printArray(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.print(arr[i] + " ");
        }
    }

    public int[] runningSum(int[] num) {
        for (int i = 1; i < num.length; i++) {
            num[i] = num[i - 1] + num[i];
        }
        return num;
    }

    public static void main(String[] args) {
        RunningSum runningSum = new RunningSum();
        int[] nums = {3,3};
        runningSum.printArray(nums);
        System.out.println();
        int[] result = runningSum.runningSum(nums);
        System.out.print("Running Sum: ");
        runningSum.printArray(result);
    }
}
